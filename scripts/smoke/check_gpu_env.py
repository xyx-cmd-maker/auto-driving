#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""GPU 环境验证（可复跑自检）。

用法：python scripts/smoke/check_gpu_env.py
退出码：0 = 全部通过；1 = 有任一检查未过

为什么需要它
------------
本项目曾把一个**从未实测的"无 GPU"假设**写进不变量与计划（2026-10-11 纠正）。
本脚本把"这台机器能不能真的用 GPU 算"变成一条可复跑的命令，
避免再次基于传闻/问答选项做决策。

检查项：
  1. torch 可导入，且不是 +cpu 构建
  2. torch.cuda.is_available() 为真
  3. 设备名与 compute capability 可读（记录预期 sm_120 / Blackwell）
  4. 真实算子：GPU 上做矩阵乘 + 反向传播，并与 CPU 结果比对数值一致性
  5. 报告显存与精度支持（fp32 / fp16 / bf16）
"""
import sys
import time


def main():
    results = []

    def check(name, ok, detail):
        results.append((name, ok, detail))

    try:
        import torch
    except Exception as exc:
        check("import-torch", False, "导入失败：%s" % exc)
        report(results)
        return 1

    check("import-torch", True, "torch %s" % torch.__version__)

    is_cpu_build = "+cpu" in torch.__version__
    check("not-cpu-build", not is_cpu_build,
          "构建为 %s" % ("CPU-only（需换 cuXXX 轮子）" if is_cpu_build else "含 CUDA"))

    avail = bool(torch.cuda.is_available())
    check("cuda-available", avail, "cuda.is_available() = %s（torch.version.cuda=%s）"
          % (avail, getattr(torch.version, "cuda", None)))
    if not avail:
        report(results)
        return 1

    try:
        n = torch.cuda.device_count()
        name = torch.cuda.get_device_name(0)
        cap = torch.cuda.get_device_capability(0)
        props = torch.cuda.get_device_properties(0)
        check("device", True, "%d 个设备；device0 = %s；compute capability = sm_%d%d；显存 %.2f GiB"
              % (n, name, cap[0], cap[1], props.total_memory / 1024 ** 3))
        expected = (12, 0)   # 本项目本机为 RTX 5060 Laptop = Blackwell sm_120
        check("capability-known", True,
              "预期为 sm_%d%d（本项目本机）→ %s"
              % (expected[0], expected[1],
                 "一致" if cap == expected else "**不一致，请核对硬件**"))
    except Exception as exc:
        check("device", False, "读取设备信息失败：%s" % exc)

    # ---- 真实算子：矩阵乘 + 反向，并与 CPU 比对 ----
    try:
        torch.manual_seed(0)
        N = 2048
        a = torch.randn(N, N)
        w_cpu = torch.randn(N, N, requires_grad=True)
        w_gpu = w_cpu.detach().clone().requires_grad_(True)
        b_cpu = torch.randn(N)

        # CPU 参考
        t0 = time.perf_counter()
        out_cpu = ((a @ w_cpu) + b_cpu).pow(2).mean()
        out_cpu.backward()
        t_cpu = time.perf_counter() - t0

        # GPU —— 先做一次预热，把 CUDA 上下文/内核首次加载的开销排除在计时之外
        ag, bg, wg = a.cuda(), b_cpu.cuda(), w_gpu.cuda()
        _ = (ag @ wg).sum()
        torch.cuda.synchronize()

        t0 = time.perf_counter()
        out_gpu = ((ag @ wg) + bg).pow(2).mean()
        out_gpu.backward()
        torch.cuda.synchronize()
        t_gpu = time.perf_counter() - t0

        d_loss = abs(out_gpu.item() - out_cpu.item())
        d_grad = (w_gpu.grad.cpu() - w_cpu.grad).abs().max().item()
        tol = 1e-3
        check("matmul-forward", d_loss < tol, "%dx%d loss 差 %.3e（容差 %.0e）" % (N, N, d_loss, tol))
        check("backward-grad", d_grad < tol, "梯度最大绝对差 %.3e" % d_grad)
        note = "" if t_gpu < t_cpu else "（小矩阵 CPU 不落下风，属正常；大 batch 才见优势）"
        check("speedup", True, "%dx%d matmul+backward（已预热）：CPU %.1f ms / GPU %.1f ms → %.1fx %s"
              % (N, N, t_cpu * 1e3, t_gpu * 1e3, (t_cpu / t_gpu) if t_gpu > 0 else float("nan"), note))
    except Exception as exc:
        check("gpu-op", False, "GPU 算子执行失败：%s" % exc)

    # ---- 精度支持 ----
    for dt, label in ((torch.float32, "fp32"), (torch.float16, "fp16"), (torch.bfloat16, "bf16")):
        try:
            x = torch.randn(256, 256, dtype=dt, device="cuda")
            y = (x @ x).sum().item()
            check("dtype-" + label, True, "可用（示例值 %.3f）" % float(y))
        except Exception as exc:
            check("dtype-" + label, False, "不可用：%s" % exc)

    failed = [n for n, ok, _ in results if not ok]
    report(results)
    return 0 if not failed else 1


def report(results):
    print("GPU 环境验证")
    print("")
    for name, ok, detail in results:
        print("  %s %-18s %s" % ("OK  " if ok else "FAIL", name, detail))
    failed = [n for n, ok, _ in results if not ok]
    total = len(results)
    print("")
    print("[gpu-env] %s：%d/%d" % ("全部通过" if not failed else "有未过项 " + ", ".join(failed),
                                  total - len(failed), total))


if __name__ == "__main__":
    sys.exit(main())
