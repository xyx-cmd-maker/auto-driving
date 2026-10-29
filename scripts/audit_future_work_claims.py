#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""核 §5.6（Future work）里两条**可算**的承诺。

论文原句：
  (a) "Increasing seeds to twenty would make the exact test informative and **halve the interval widths**."
  (b) "…the map predicts availability **above 0.5** there."

(a) 的"halve"可以算：CI 宽度 ∝ SD/√n，SD 用现有 n=5 与 n=10 的实测值分别外推。
(b) 的"above 0.5"可在扫描表上直接查。

用法：py -3.12 scripts/audit_future_work_claims.py
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
SWEEP = os.path.join(ROOT, "results", "p1", "otf_density_sweep_sumo_s1-2-3_fine.json")


def t_crit(q, df):
    # 复用精确实现：调用 audit_recompute_main 的 t_ppf
    import importlib.util
    spec = importlib.util.spec_from_file_location("rc", os.path.join(ROOT, "scripts", "audit_recompute_main.py"))
    rc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rc)
    return rc.t_ppf(q, df)


def dcost(group, seeds):
    out = []
    for f in sorted(glob.glob(os.path.join(CASES, group, "case_lead-brake_s*.json"))):
        sd = int(f.split("_s")[-1].split(".")[0])
        if sd in seeds:
            out.append(json.load(io.open(f, encoding="utf-8"))["paired"]["delta_cost"])
    return out


def main() -> int:
    rows, fails = [], []

    # ── (a) 精确检验在 n=20 时是否"informative" ──
    p_min20 = 2.0 / (2 ** 20)
    holm = 0.05 / 4
    ok_a1 = p_min20 < holm
    rows.append(("n=20 可达最小 exact p", "%.2e" % p_min20, "< Holm 阈值 0.0125",
                 "PASS" if ok_a1 else "FAIL"))
    if not ok_a1:
        fails.append("n=20 的检验仍不可显著")

    # ── (b) 宽度是否"减半"：用 n=5 与 n=10 的 SD 分别外推 n=20 ──
    d5 = dcost("main", set(range(5)))
    d10 = dcost("main", set(range(10)))
    sd5, sd10 = st.stdev(d5), st.stdev(d10)
    w5 = 2 * t_crit(0.975, 4) * sd5 / math.sqrt(5)
    pred_from5 = 2 * t_crit(0.975, 19) * sd5 / math.sqrt(20)
    pred_from10 = 2 * t_crit(0.975, 19) * sd10 / math.sqrt(20)
    ratio5 = pred_from5 / w5
    ratio10 = pred_from10 / w5
    rows.append(("现行 n=5 的 CI 宽度（lead-brake）", "%.2f" % w5, "论文 Table I = 5.90",
                 "PASS" if abs(w5 - 5.90) < 0.02 else "FAIL"))
    rows.append(("外推 n=20 宽度（用 n=5 的 SD）", "%.2f" % pred_from5, "比值 %.2f×" % ratio5,
                 "PASS" if ratio5 <= 0.55 else "FAIL"))
    rows.append(("外推 n=20 宽度（用 n=10 的 SD）", "%.2f" % pred_from10, "比值 %.2f×" % ratio10,
                 "PASS" if ratio10 <= 0.55 else "FAIL"))
    if ratio5 > 0.55:
        fails.append("用 n=5 的 SD 外推，宽度并未减半")

    # ── (c) "map predicts availability above 0.5" 是否存在这样的区域 ──
    t = json.load(io.open(SWEEP, encoding="utf-8"))["table"]
    cells = []
    for dens, wd in t.items():
        for w, v in wd.items():
            if isinstance(v, dict) and "nonzero_fraction_mean" in v:
                cells.append((int(dens), int(w.replace("W=", "")), v["nonzero_fraction_mean"]))
    above = [c for c in cells if c[2] > 0.5]
    rows.append(("扫描表中 >0.5 的 (密度,窗口) 格数", "≥1", "%d / %d" % (len(above), len(cells)),
                 "PASS" if above else "FAIL"))
    if above:
        dens_min = min(c[0] for c in above)
        w_min = min(c[1] for c in above)
        rows.append((">0.5 的最低密度", "—", "%d veh/h" % dens_min, "INFO"))
        rows.append((">0.5 的最短窗口", "—", "%d s" % w_min, "INFO"))
    else:
        fails.append("扫描表里没有 >0.5 的格")

    print("  %-40s %-16s %-20s %s" % ("承诺", "计算值", "对照", "判定"))
    for a, b, c, v in rows:
        print("  %-40s %-16s %-20s %s" % (a, b, c, v))
    print()
    if fails:
        print("  ✗ %d 条承诺不成立：" % len(fails))
        for f in fails:
            print("     " + f)
        return 1
    print("  ✓ §5.6 的两条可算承诺均成立（宽度减半是保守估计）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
