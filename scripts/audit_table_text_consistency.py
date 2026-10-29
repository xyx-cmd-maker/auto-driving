#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P0-2（表格 ↔ 源）：把 manuscript-ieee.md 里三张表的**每个单元格**与重算值比对。

与前三轮的分工：
  Round 02/03/04 验证的是"源 → 论文数字"；
  本脚本验证反方向"**论文表格单元格 → 源**"，即渲染进 PDF 的那张表本身。

依赖：标准库 + 复用 `audit_recompute_main.py` 的 t 分布与检验实现。
用法：py -3.12 scripts/audit_table_text_consistency.py
"""
import glob
import importlib.util
import io
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CASES = os.path.join(ROOT, "results", "p1", "cases")
PAPER = os.path.join(ROOT, "papers", "p1", "manuscript-ieee.md")

spec = importlib.util.spec_from_file_location("rc", os.path.join(ROOT, "scripts", "audit_recompute_main.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)  # noqa: E402  （只取函数，不跑 main）

NUM = r"[-−+]?\d+(?:\.\d+)?"


def num(s):
    s = s.replace("−", "-").replace("+", "").strip()
    m = re.match(NUM, s)
    return float(m.group(0)) if m else None


def load(group, scen, seeds=(0, 1, 2, 3, 4)):
    out = []
    for f in sorted(glob.glob(os.path.join(CASES, group, "case_%s_s*.json" % scen))):
        sd = int(f.split("_s")[-1].split(".")[0])
        if sd in seeds:
            out.append(json.load(io.open(f, encoding="utf-8")))
    return out


def cost_stats(rows):
    d = [r["paired"]["delta_cost"] for r in rows]
    m, s = rc.mean_sd(d)
    lo95, hi95, _ = rc.ci(d, rc.T975_4)
    lo90, hi90, _ = rc.ci(d, rc.T95_4)
    off = sum(r["arms"]["a1_otf_off"]["best_cost"] for r in rows) / len(rows)
    margin = 0.1 * off
    p_tost = rc.tost_p(d, margin)
    st = rc.three_state(lo95, hi95, m, margin, p_tost)
    return dict(mean=m, off=off, lo95=lo95, hi95=hi95, lo90=lo90, hi90=hi90,
                p_exact=rc.exact_signflip_p(d), p_tost=p_tost, state=st)


def parse_tables(text):
    lines = text.split("\n")
    tables, cur = [], None
    for ln in lines:
        if ln.startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if cur is None:
                cur = []
            cur.append(cells)
        else:
            if cur and len(cur) >= 3:
                tables.append(cur)
            cur = None
    if cur and len(cur) >= 3:
        tables.append(cur)
    return tables


def main() -> int:
    text = io.open(PAPER, encoding="utf-8").read()
    tabs = parse_tables(text)
    by_head = {}
    for t in tabs:
        head = t[0]
        if head[:2] == ["Scenario", "n"]:
            by_head["T1"] = t
        elif head[:2] == ["Scenario", "Endpoint"]:
            by_head["T2"] = t
        elif head[:1] == ["Group"]:
            by_head["T3"] = t

    fails, checks = [], 0

    def cmp(label, got, want, tol):
        nonlocal checks
        checks += 1
        if got is None or want is None or abs(got - want) > tol:
            fails.append((label, want, got))

    # ── Table I ──
    if "T1" not in by_head:
        print("  ✗ 未找到 Table I")
        return 1
    t1 = by_head["T1"]
    body = [r for r in t1[2:] if r and r[0] in ("none", "cutin", "lead-brake", "lead-exit")]
    print("  Table I：%d 行" % len(body))
    for r in body:
        sc = r[0]
        s = cost_stats(load("main", sc))
        cmp("T1/%s/n" % sc, float(r[1]), 5.0, 0)
        cmp("T1/%s/mean" % sc, num(r[2]), s["mean"], 6e-3)
        cmp("T1/%s/off" % sc, num(r[3]), s["off"], 6e-3)
        ci95 = [num(x) for x in re.findall(NUM, r[4])]
        ci90 = [num(x) for x in re.findall(NUM, r[5])]
        cmp("T1/%s/lo95" % sc, ci95[0], s["lo95"], 6e-3)
        cmp("T1/%s/hi95" % sc, ci95[1], s["hi95"], 6e-3)
        cmp("T1/%s/lo90" % sc, ci90[0], s["lo90"], 6e-3)
        cmp("T1/%s/hi90" % sc, ci90[1], s["hi90"], 6e-3)
        cmp("T1/%s/pexact" % sc, num(r[6]), s["p_exact"], 6e-3)
        cmp("T1/%s/ptost" % sc, num(r[7]), s["p_tost"], 6e-3)
        checks += 1
        if r[8].strip() != s["state"]:
            fails.append(("T1/%s/state" % sc, s["state"], r[8]))

    # ── Table II ──
    t2 = by_head.get("T2")
    if t2:
        body2 = [r for r in t2[2:] if r and r[0] in ("none", "cutin", "lead-brake", "lead-exit")]
        print("  Table II：%d 行" % len(body2))
        inc = 0
        for r in body2:
            sc, ep = r[0], r[1]
            key = "delta_following_rmse" if ep.startswith("RMSE") else "delta_accel_sq_integral"
            rows = load("main", sc)
            d = [x["paired"][key] for x in rows]
            m, _ = rc.mean_sd(d)
            vals = [num(x) for x in re.findall(NUM, r[2])]
            cmp("T2/%s/%s/mean" % (sc, ep[:5]), vals[0], m, 6e-3)
            lo, hi, _ = rc.ci(d, rc.T975_4)
            cmp("T2/%s/%s/lo" % (sc, ep[:5]), vals[1], lo, 6e-3)
            cmp("T2/%s/%s/hi" % (sc, ep[:5]), vals[2], hi, 6e-3)
            # TOST margin 用该端点自身 off 均值
            offkey = "following_rmse_m" if ep.startswith("RMSE") else "accel_sq_integral_mps3"
            off = sum(x["arms"]["a1_otf_off"]["best_metrics"][offkey] for x in rows) / len(rows)
            p = rc.tost_p(d, 0.1 * off)
            cmp("T2/%s/%s/ptost" % (sc, ep[:5]), num(r[3]), p, 6e-3)
            if p >= 0.05:
                inc += 1
        checks += 1
        if inc != 8:
            fails.append(("T2/同结论条数", 8, inc))
        print("    TOST p ≥ 0.05 的行数 = %d（正文称 All eight tests are inconclusive）" % inc)

    # ── Table III ──
    t3 = by_head.get("T3")
    if t3:
        spec3 = {"Main": ("main", "lead-brake", "lead-brake"),
                 "A,": ("highdensity", "lead-brake", "lead-brake"),
                 "B,": ("window20", "lead-brake", "lead-brake")}
        body3 = [r for r in t3[2:] if r and r[0] in ("Main", "A, density", "B, window")]
        print("  Table III：%d 行" % len(body3))
        for r in body3:
            g = r[0]
            grp = "main" if g == "Main" else ("highdensity" if g.startswith("A") else "window20")
            s = cost_stats(load(grp, "lead-brake"))
            cmp("T3/%s/mean" % g, num(r[4]), s["mean"], 6e-3)
            ci = [num(x) for x in re.findall(NUM, r[5])]
            cmp("T3/%s/lo" % g, ci[0], s["lo95"], 6e-3)
            cmp("T3/%s/hi" % g, ci[1], s["hi95"], 6e-3)
            cmp("T3/%s/width" % g, num(r[6]), s["hi95"] - s["lo95"], 6e-3)
            phi = sum(x["arms"]["a1_otf_on"]["phi_nonzero_ratio"] for x in load(grp, "lead-brake")) / 5
            cmp("T3/%s/avail" % g, num(r[3]), phi, 6e-3)

    print()
    print("  共比对 %d 个单元格/字符" % checks)
    if fails:
        print("  ✗ %d 处不一致：" % len(fails))
        for f in fails[:15]:
            print("     %-34s 表内 %s  源 %s" % f)
        return 1
    print("  ✓ 三张表的每个单元格都与源一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
