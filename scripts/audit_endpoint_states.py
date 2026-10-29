#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""路线 C：在**不含常数伪迹**的端点上重做三态判定（等价 / 有意义 / 未定）。

为什么需要它（Round 25 的 P0）：
    复合代价含 51.1% 的常数（jerk 伪迹），而 TOST margin = off 臂均值 10%，
    常数抬高均值也就抬高了 margin，使"等价"更容易成立。扣掉常数后 2/4 等价 → 0/4。
    因此需要一个**不依赖该常数**的端点集合来检验"等价"这一结论是否还站得住。

本脚本对 4 场景 × 2 端点（following RMSE、加速度平方积分）逐个计算：
    Δ（on − off）、95% CI、0.1 × off 均值（预注册 margin）、精确符号翻转 p、TOST p、三态。

用法：py -3.12 scripts/audit_endpoint_states.py
"""
import glob
import importlib.util
import io
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CASES = os.path.join(ROOT, "results", "p1", "cases")
spec = importlib.util.spec_from_file_location("rc", os.path.join(ROOT, "scripts", "audit_recompute_main.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

ENDPOINTS = [
    ("following_rmse_m", "delta_following_rmse", "RMSE (m)"),
    ("accel_sq_integral_mps3", "delta_accel_sq_integral", "accel² (m²/s³)"),
]
SCEN = ["none", "cutin", "lead-brake", "lead-exit"]


def load(scen, seeds=(0, 1, 2, 3, 4)):
    out = []
    for f in sorted(glob.glob(os.path.join(CASES, "main", "case_%s_s*.json" % scen))):
        sd = int(f.split("_s")[-1].split(".")[0])
        if sd in seeds:
            out.append(json.load(io.open(f, encoding="utf-8")))
    return out


def main() -> int:
    print("  路线 C：不含常数伪迹的端点，逐场景三态判定")
    print("  %-11s %-14s %10s %-24s %8s %8s %8s %s"
          % ("场景", "端点", "Δ", "95% CI", "off均值", "margin", "TOST p", "状态"))
    tally = {"equivalent": 0, "meaningful": 0, "inconclusive": 0}
    rows = []
    for sc in SCEN:
        data = load(sc)
        for key, dkey, label in ENDPOINTS:
            off = [r["arms"]["a1_otf_off"]["best_metrics"][key] for r in data]
            on = [r["arms"]["a1_otf_on"]["best_metrics"][key] for r in data]
            d = [o - f for o, f in zip(on, off)]
            off_mean = sum(off) / len(off)
            margin = 0.1 * off_mean
            m, _ = rc.mean_sd(d)
            lo, hi, _ = rc.ci(d, rc.T975_4)
            p = rc.tost_p(d, margin)
            state = rc.three_state(lo, hi, m, margin, p)
            tally[state] += 1
            rows.append((sc, label, m, lo, hi, off_mean, margin, p, state))
            print("  %-11s %-14s %+10.3f [%+8.3f,%+8.3f] %8.2f %8.2f %8.4f %s"
                  % (sc, label, m, lo, hi, off_mean, margin, p, state))

    print("\n  汇总：等价 %d ｜ 有意义差异 %d ｜ 未定 %d（共 %d 个端点）"
          % (tally["equivalent"], tally["meaningful"], tally["inconclusive"], len(rows)))
    if tally["equivalent"] == 0:
        print("  ⚠ 在这两个不含伪迹的端点上，**没有任何场景可以主张等价**——")
        print("     论文的『2/4 等价』只在含 jerk 常数的复合代价上成立。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
