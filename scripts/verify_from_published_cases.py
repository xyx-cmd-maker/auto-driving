#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""外审自验脚本：只读 `results/p1/cases/` 下已发布的逐局 JSON，重算论文关键数字。

为什么单独写这个脚本而不复用 `verify_a1_numbers.py`：
    后者读的是 `runs/p1/cases/`（体积大、未入库）。外审拿到的只有
    `results/p1/cases/` 的脱敏副本，所以这里给一条**对方可独立运行**的路径。

用法：
    py -3.12 scripts/verify_from_published_cases.py

预期输出（2026-10-29 发布时实测）：
    窗口       n    Δcost 均值    Δcost SD
    main       10   +0.409        1.718
    window10   10   +0.587        1.809
    window20   10   +0.558        1.926
    降级检验：有 Δv 10 局 off 臂 cost 均值 30.82 → 无 Δv 5 局 30.96（+0.14）

若你算出的数与上面不符，说明仓库中的逐局数据与稿件不一致——请直接告知作者。
"""
import glob
import io
import json
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

GROUPS = [("main", "main"), ("window10", "window10"), ("window20", "window20")]


def load(group, scenario=None):
    pat = os.path.join(CASES, group, "case_*.json")
    rows = []
    for f in sorted(glob.glob(pat)):
        d = json.load(io.open(f, encoding="utf-8"))
        if scenario and d.get("scenario") != scenario:
            continue
        rows.append(d)
    return rows


def main() -> int:
    if not os.path.isdir(CASES):
        print("  ✗ 找不到 %s" % CASES)
        return 2

    print("  %-10s %3s  %10s  %8s" % ("窗口", "n", "Δcost 均值", "Δcost SD"))
    for g, _ in GROUPS:
        rows = load(g, scenario="lead-brake")
        d = [r["paired"]["delta_cost"] for r in rows]
        if not d:
            print("  %-10s   0  （无数据）" % g)
            continue
        print("  %-10s %3d  %+10.3f  %8.3f" % (g, len(d), st.mean(d), st.stdev(d) if len(d) > 1 else 0.0))

    print()
    print("  机制检验（删掉相对速度）：off 臂复合代价")
    base = [r["arms"]["a1_otf_off"]["best_cost"] for r in load("main", "lead-brake")]
    degr = [r["arms"]["a1_otf_off"]["best_cost"] for r in load("degraded", "lead-brake")]
    if base and degr:
        print("    有 Δv（main 全部）     n=%d  均值 %.2f" % (len(base), st.mean(base)))
        print("    无 Δv（degraded）     n=%d  均值 %.2f" % (len(degr), st.mean(degr)))
        print("    差值 %+.2f" % (st.mean(degr) - st.mean(base)))
    else:
        print("    （缺数据，跳过）")

    print()
    print("  主实验四场景的配对差（main 组，seeds 0-4）")
    print("  %-12s %8s  %10s" % ("场景", "n", "Δcost 均值"))
    for sc in ("none", "cutin", "lead-brake", "lead-exit"):
        d = [r["paired"]["delta_cost"] for r in load("main", sc)]
        if d:
            print("  %-12s %8d  %+10.3f" % (sc, len(d), st.mean(d)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
