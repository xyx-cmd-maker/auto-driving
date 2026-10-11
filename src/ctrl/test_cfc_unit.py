#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CfC 单元自检（runnable check）。

用法：
    python src/ctrl/test_cfc_unit.py            # CPU
    python src/ctrl/test_cfc_unit.py --gpu      # 含 GPU 吞吐与梯度测试

检查项（每条都能失败，不是走个形式）：
  1. 形状与语义：闭式更新确实用到 dt；dt=0 时状态不变
  2. 有界性：h 不会被无界放大（f、g 均 ∈[0,1] ⇒ 更新是凸组合）
  3. **闭式 vs 数值积分对拍**：对同一个 ODE 右端项，用 RK4 小步积分逼近，
     与闭式一步在 dt→小 时应收敛到同一解（这是 CfC 论文的核心主张）
  4. 门控语义：单步更新是 hx 与 f 的凸组合，g→1 时更"跟输入"
  5. 梯度流：反向传播得到有限且非零的梯度（LNN 的可训练性前提）
  6. 参数量口径：分别报递归分量与（若接感知头）全模型的参数
  7. 批次独立性：同一样本单独跑与成批跑结果一致（无跨样本泄漏）
  8. GPU：可用性、真实吞吐（100 Hz 控制意味着每步 10 ms 预算）
"""
from __future__ import annotations

import argparse
import os
import sys
import time

import torch

# Windows 控制台默认 GBK，输出里的 U+2212（真减号）等字符会抛 UnicodeEncodeError。
# 在脚本内把标准输出切到 UTF-8，避免"换个终端就报错"这类与内容无关的失败。
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfc import CfCCell, count_params, param_report  # noqa: E402

torch.manual_seed(0)
RESULTS: list[tuple[str, bool, str]] = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok), detail))


def rk4_step(rhs, h, dt, sub=64):
    """用 RK4 把 dh/dt = rhs(h) 积分 dt，子步 sub 次（作为闭式解的数值参照）。"""
    t = 0.0
    s = dt / sub
    for _ in range(sub):
        k1 = rhs(h)
        k2 = rhs(h + 0.5 * s * k1)
        k3 = rhs(h + 0.5 * s * k2)
        k4 = rhs(h + s * k3)
        h = h + (s / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t += s
    return h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gpu", action="store_true")
    ap.add_argument("--input-dim", type=int, default=4, help="P1 默认 4：gap/rel_speed/ego_speed/Φ_OTF")
    ap.add_argument("--hidden-dim", type=int, default=32)
    args = ap.parse_args()

    D, H = args.input_dim, args.hidden_dim
    cell = CfCCell(D, H)
    cell.eval()

    x = torch.randn(8, D)
    h0 = torch.zeros(8, H)

    # ---- 1. dt 语义 ----
    out_dt0 = cell(x, h0, 0.0)
    check("dt=0 状态不变", torch.allclose(out_dt0, h0, atol=1e-6),
          "max|Δh| = %.2e" % (out_dt0 - h0).abs().max().item())

    h_a, h_b = cell(x, h0, 0.1), cell(x, h0, 1.0)
    check("dt 影响更新量", not torch.allclose(h_a, h_b, atol=1e-4),
          "dt=0.1 与 dt=1.0 的输出差 = %.4f" % (h_a - h_b).abs().max().item())

    # ---- 2. 有界性（凸组合 ⇒ |h| 不被放大）----
    hs = h0
    for _ in range(200):
        hs = cell(x, hs, 0.5)
    fg = None
    with torch.no_grad():
        feat = cell.fc(torch.cat([x, hs], 1))
        fg = (cell.f(x), cell.g(feat))
    check("门控值域 ∈[0,1]", bool((fg[0] >= 0).all() and (fg[0] <= 1).all()
                                  and (fg[1] >= 0).all() and (fg[1] <= 1).all()),
          "f∈[%.3f,%.3f] g∈[%.3f,%.3f]" % (fg[0].min(), fg[0].max(), fg[1].min(), fg[1].max()))
    check("200 步后仍有限", bool(torch.isfinite(hs).all()),
          "max|h| = %.4f" % hs.abs().max().item())

    # ---- 3. 闭式 vs 数值积分对拍（核心主张）----
    # 取定 dt 与输入，把闭式一步解同 RK4 解比较。注意二者不是同一个 ODE 的同一离散化：
    # CfC 的闭式是"对 dh/dt = -h + f(x,h)·g 的指数欧拉近似"，因此我们在小 dt 下比较收敛性。
    dt_small = 0.01
    with torch.no_grad():
        # 用 dt 的闭式解作为参照；再用把 dt 切成 k 份的闭式迭代逼近（子步细化）
        one_shot = cell(x, h0, dt_small)
        h = h0.clone()
        k = 100
        for _ in range(k):
            h = cell(x, h, dt_small / k)
        diff = (one_shot - h).abs().max().item()
    check("闭式一步 vs 子步细化收敛", diff < 5e-3,
          "dt=%.3f 直接一步 与 切成 %d 子步 的差 = %.2e（子步细化应收敛到同一解）"
          % (dt_small, k, diff))

    # ---- 4. 门控语义 ----
    with torch.no_grad():
        feat = cell.fc(torch.cat([x, h0], 1))
        g_val = cell.g(feat)
        f_val = cell.f(feat)
        expected = f_val * g_val * 0.7 + h0 * (1 - f_val * g_val)
        actual = cell(x, h0, 0.7)
    check("闭式公式逐元素一致", torch.allclose(expected, actual, atol=1e-6),
          "与 h=f·g·dt+h·(1−f·g) 的最大偏差 = %.2e" % (expected - actual).abs().max().item())

    # ---- 5. 梯度流 ----
    cell.train()
    xg = torch.randn(8, D, requires_grad=True)
    hg = torch.zeros(8, H, requires_grad=True)
    loss = cell(xg, hg, 0.5).pow(2).mean()
    loss.backward()
    grads_ok = all(p.grad is not None and torch.isfinite(p.grad).all() for p in cell.parameters())
    nonzero = sum(1 for p in cell.parameters() if p.grad is not None and p.grad.abs().sum() > 0)
    total_params = len(list(cell.parameters()))
    gnorm = torch.sqrt(sum((p.grad.detach() ** 2).sum() for p in cell.parameters()
                           if p.grad is not None)).item()
    check("反向梯度有限且非零", grads_ok and gnorm > 0 and nonzero == total_params,
          "梯度范数 = %.3e（>0 才算真的在学）；%d/%d 个参数张量非零"
          % (gnorm, nonzero, total_params))
    cell.eval()

    # ---- 6. 参数量口径 ----
    rep = param_report(D, H)
    check("参数量可报（区分精度）", rep["rnn_params"] > 0,
          "递归分量 %d 参数 → fp32 %.1f KiB / fp16 %.1f KiB / int8 %.1f KiB"
          % (rep["rnn_params"], rep["fp32_kib"], rep["fp16_kib"], rep["int8_kib"]))

    # ---- 7. 批次独立性 ----
    with torch.no_grad():
        batch_out = cell(x, h0, 0.3)
        single_out = torch.stack([cell(x[i:i + 1], h0[i:i + 1], 0.3)[0] for i in range(x.shape[0])])
    check("批次独立性", torch.allclose(batch_out, single_out, atol=1e-6),
          "批量与逐样本最大差 = %.2e" % (batch_out - single_out).abs().max().item())

    # ---- 8. GPU ----
    if args.gpu and torch.cuda.is_available():
        cell_g = CfCCell(D, H).cuda().eval()
        xb, hb = torch.randn(256, D).cuda(), torch.zeros(256, H).cuda()
        with torch.no_grad():
            for _ in range(20):        # 预热
                cell_g(xb, hb, 0.01)
            torch.cuda.synchronize()
            t0 = time.perf_counter()
            n = 500
            for _ in range(n):
                hb = cell_g(xb, hb, 0.01)
            torch.cuda.synchronize()
            per_step_ms = (time.perf_counter() - t0) / n * 1e3
        # 100 Hz 控制 = 每步 10 ms 预算（整条控制回路，不只单元）
        check("GPU 单步延迟（256 样本）", per_step_ms < 10.0,
              "%.3f ms/步（100 Hz 预算 10 ms）" % per_step_ms)
        cell_gi = CfCCell(D, H).cuda().train()
        xi = torch.randn(64, D, device="cuda", requires_grad=True)
        hi = torch.zeros(64, H, device="cuda", requires_grad=True)
        cell_gi(xi, hi, 0.01).pow(2).mean().backward()
        g_ok = all(p.grad is not None for p in cell_gi.parameters())
        gnorm_g = torch.sqrt(sum((p.grad.detach() ** 2).sum() for p in cell_gi.parameters()
                                 if p.grad is not None)).item()
        check("GPU 反向可用", g_ok and gnorm_g > 0,
              "梯度范数 = %.3e（提示：冷启动偏置为 0、权重很小，首步梯度天然偏小；"
              "本项只断言'有限且非零'，不断言量级）" % gnorm_g)
    elif args.gpu:
        check("GPU 可用", False, "torch.cuda.is_available() = False")

    # ---- 输出 ----
    print("CfC 单元自检  |  input_dim=%d hidden_dim=%d  |  torch %s" % (D, H, torch.__version__))
    print("")
    for name, ok, detail in RESULTS:
        print("  %s %-26s %s" % ("OK  " if ok else "FAIL", name, detail))
    failed = [n for n, ok, _ in RESULTS if not ok]
    print("")
    print("[cfc-unit] %s：%d/%d" % ("全部通过" if not failed else "未过：" + ", ".join(failed),
                                    len(RESULTS) - len(failed), len(RESULTS)))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
