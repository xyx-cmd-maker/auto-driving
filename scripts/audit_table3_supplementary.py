#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P0-2（第三层）：从已发布逐局数据重建论文 Table III 与 Fig.2 的补充组数字。

本轮之前，Table III 的 A 组与 Fig.2 的 W=20 s 另两场景**没有公开逐局数据**
（只在作者机器 `runs/` 下），属可复现性缺口。2026-10-29 已把这两组发布到：
    results/p1/cases/highdensity/    （A 组：32 辆 / 5 s）
    results/p1/cases/window20extra/  （B2 组：20 s 窗口的另两个场景）
本脚本用**已发布**数据重算，并与论文 Table III / Fig.2 图注逐项比对。

依赖：标准库。
用法：py -3.12 scripts/audit_table3_supplementary.py
"""
import glob
import io
import json
import math
import os
import statistics as st
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CASES = os.path.join(ROOT, "results", "p1", "cases")
T975_4 = 2.776445  # t(0.975, df=4)

# 论文 Table III（`_results-fragment.md`）与 Fig.2 图注（`05-figures.md`）
PAPER_T3 = {
    "Main": dict(mean=0.858, lo=-2.092, hi=3.808, width=5.90, phi=0.084, traffic=16, window=5.0),
    "A, density": dict(mean=1.372, lo=-2.326, hi=5.069, width=7.40, phi=0.084, traffic=32, window=5.0),
    "B, window": dict(mean=0.707, lo=-2.709, hi=4.122, width=6.83, phi=0.334, traffic=16, window=20.0),
}
PAPER_B2_PHI_RANGE = (0.334, 0.497)   # Fig.2 图注："between 0.334 and 0.497 in the third"


def pick(group, scenario, seeds=(0, 1, 2, 3, 4)):
    out = []
    for f in glob.glob(os.path.join(CASES, group, "case_%s_s*.json" % scenario)):
        sd = int(f.split("_s")[-1].split(".")[0])
        if sd in seeds:
            out.append(f)
    return sorted(out)


def stats(files):
    rows = [json.load(io.open(f, encoding="utf-8")) for f in files]
    if not rows:
        return None
    d = [r["paired"]["delta_cost"] for r in rows]
    m, s = st.mean(d), (st.stdev(d) if len(d) > 1 else 0.0)
    se = s / math.sqrt(len(d))
    phi = [r["arms"]["a1_otf_on"].get("phi_nonzero_ratio") for r in rows]
    return dict(n=len(d), mean=m, sd=s, lo=m - T975_4 * se, hi=m + T975_4 * se,
                width=2 * T975_4 * se, phi_mean=st.mean(phi), phi=phi)


def main() -> int:
    fails = []
    print("  === Table III 重建（数据源：results/p1/cases/*，已发布）===")
    print("  %-12s %3s %8s %9s %9s %7s %7s %6s %5s" % (
        "组", "n", "Δ均值", "CI下", "CI上", "CI宽", "Φ均值", "车辆", "窗口"))
    mapping = {"Main": ("main", "lead-brake"),
               "A, density": ("highdensity", "lead-brake"),
               "B, window": ("window20", "lead-brake")}
    for label, paper in PAPER_T3.items():
        grp, scen = mapping[label]
        s = stats(pick(grp, scen))
        if s is None:
            print("  %-12s ✗ 无数据（%s/%s）" % (label, grp, scen))
            fails.append((label, "missing"))
            continue
        print("  %-12s %3d %+8.3f %9.3f %9.3f %7.2f %7.3f %6s %5.1f" % (
            label, s["n"], s["mean"], s["lo"], s["hi"], s["width"],
            s["phi_mean"], "-", 5.0 if label != "B, window" else 20.0))
        for k, tol in (("mean", 1e-3), ("lo", 1e-3), ("hi", 1e-3), ("width", 5e-3)):
            if abs(s[k] - paper[k]) > tol:
                fails.append((label, k, s[k], paper[k]))
        if abs(s["phi_mean"] - paper["phi"]) > 1e-3:
            fails.append((label, "phi", s["phi_mean"], paper["phi"]))
        if s["n"] != 5:
            fails.append((label, "n", s["n"], 5))

    print()
    print("  === Fig.2 的 W=20 s 另两场景（B2 组）===")
    phis = {}
    for scen in ("cutin", "lead-exit"):
        s = stats(pick("window20extra", scen))
        if s is None:
            print("  %-11s ✗ 无数据" % scen)
            fails.append((scen, "missing"))
            continue
        phis[scen] = s["phi"]
        print("  %-11s n=%d Φ均值=%.3f 范围=[%.3f, %.3f]" % (
            scen, s["n"], s["phi_mean"], min(s["phi"]), max(s["phi"])))
    # lead-brake 的 W=20 已有
    s_lb = stats(pick("window20", "lead-brake"))
    if s_lb:
        phis["lead-brake"] = s_lb["phi"]
        print("  %-11s n=%d Φ均值=%.3f" % ("lead-brake", s_lb["n"], s_lb["phi_mean"]))
    spreads = sorted(max(v) for v in phis.values())
    if spreads:
        lo_expected, hi_expected = PAPER_B2_PHI_RANGE
        got_lo, got_hi = min(spreads), max(spreads)
        print("  三个场景的 Φ 最大值：%.3f / %.3f / %.3f" % tuple(spreads) if len(spreads) == 3 else "")
        if abs(got_lo - lo_expected) > 1e-3 or abs(got_hi - hi_expected) > 1e-3:
            fails.append(("Fig2", "phi_range", (got_lo, got_hi), PAPER_B2_PHI_RANGE))

    print()
    if fails:
        print("  ✗ 与论文不一致 %d 处：" % len(fails))
        for f in fails[:12]:
            print("     ", f)
        return 1
    print("  ✓ Table III 三行 + Fig.2 补充组 Φ 范围全部与论文一致（tol=1e-3）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
