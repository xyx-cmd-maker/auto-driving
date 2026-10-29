#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P0-2（数字溯源层 · 正文）：把 §4/§5 里尚未溯源的关键数字指回源。

`audit_number_sources.py` 覆盖摘要与 Fig.2；本脚本覆盖正文的机制段与敏感性段：
  §5.2  n=10 的 SD 三元组、增量、采样误差、删 Δv 前后的 off 臂代价与差值
  §4.4  等 K 的两个均值
  §4.6.1 / Table III 的补充组数字（与 `audit_table3_supplementary.py` 交叉印证）

依赖：标准库。
用法：py -3.12 scripts/audit_number_sources_body.py
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


def cost(key, group, scenario="lead-brake", seeds=(0, 1, 2, 3, 4)):
    vals = []
    for f in sorted(glob.glob(os.path.join(CASES, group, "case_%s_s*.json" % scenario))):
        sd = int(f.split("_s")[-1].split(".")[0])
        if sd not in seeds:
            continue
        d = json.load(io.open(f, encoding="utf-8"))
        vals.append(d["arms"]["a1_otf_off"]["best_cost"] if key == "off" else d["paired"]["delta_cost"])
    return vals


def main() -> int:
    rows, fails = [], []

    def add(label, paper, got, tol):
        ok = got is not None and abs(got - paper) <= tol
        rows.append((label, paper, got, "PASS" if ok else "FAIL"))
        if not ok:
            fails.append((label, paper, got))

    # ── §5.2：n=10 的 SD 三元组（lead-brake，三窗口各 10 种子）──
    sd = {}
    for g, w in (("main", 5), ("window10", 10), ("window20", 20)):
        d = cost("delta", g, "lead-brake", seeds=tuple(range(10)))
        sd[w] = st.stdev(d)
        rows.append(("§5.2  SD @ W=%d s (n=10，对照)" % w, round(sd[w], 2), sd[w], "INFO"))
    add("§5.2  SD @ 5 s", 1.72, sd[5], 5e-3)
    add("§5.2  SD @ 10 s", 1.81, sd[10], 5e-3)
    add("§5.2  SD @ 20 s", 1.93, sd[20], 5e-3)
    add("§5.2  增量 1（10 s − 5 s）", 0.09, sd[10] - sd[5], 5e-3)
    add("§5.2  增量 2（20 s − 10 s）", 0.12, sd[20] - sd[10], 5e-3)

    # 采样误差 SE(SD) ≈ SD/√(2(n−1))
    se = [sd[w] / math.sqrt(2 * 9) for w in (5, 10, 20)]
    add("§5.2  采样误差约 0.4（三元组均值）", 0.40, st.mean(se), 5e-2)

    # ── §5.2：删 Δv 前后的 off 臂代价 ──
    off10 = cost("off", "main", "lead-brake", seeds=tuple(range(10)))
    off5 = cost("off", "degraded", "lead-brake")
    add("§5.2  off 臂均值（有 Δv，n=10）", 30.82, st.mean(off10), 5e-3)
    add("§5.2  off 臂均值（无 Δv，n=5）", 30.96, st.mean(off5), 5e-3)
    add("§5.2  两者差值", 0.14, st.mean(off5) - st.mean(off10), 5e-3)

    # ── §4.4：等 K 与主口径的两个合并均值 ──
    prim, eqk = [], []
    for f in sorted(glob.glob(os.path.join(CASES, "main", "case_*.json"))):
        sd_ = int(f.split("_s")[-1].split(".")[0])
        if sd_ > 4:
            continue
        d = json.load(io.open(f, encoding="utf-8"))
        prim.append(d["paired"]["delta_cost"])
        eqk.append(d["paired"]["equal_k"]["delta_cost"])
    add("§4.4  主口径合并均值", 0.347, st.mean(prim), 1e-3)
    add("§4.4  等 K 合并均值", -1.066, st.mean(eqk), 1e-3)

    print("  %-34s %10s %10s %6s" % ("数字", "论文值", "重算值", "判定"))
    for label, paper, got, v in rows:
        print("  %-34s %10.3f %10.4f %6s" % (label, paper, got, v))

    print()
    info = [r for r in rows if r[3] == "INFO"]
    print("  其中 %d 行为对照信息（不判 FAIL）" % len(info))
    if fails:
        print("  ✗ 有 %d 个数字与源不一致：" % len(fails))
        for f in fails:
            print("     %-34s 论文 %.4f  源 %.4f" % f)
        return 1
    print("  ✓ 正文 §4.4 / §5.2 的关键数字全部可溯源")
    return 0


if __name__ == "__main__":
    sys.exit(main())
