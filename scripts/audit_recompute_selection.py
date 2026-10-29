#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P0-2（第二轮）：独立复算**择优层**与等 K 敏感性，并量化"无效候选与场景解耦"。

与 `audit_recompute_main.py` 的分工：
  上一轮只从 `paired.*`（已聚合的配对差）复算统计量；
  本轮从 `arms.*.candidates[*]`（逐候选 cost / valid / travelled_m）**重建择优**：
    n_valid、invalid_ratio、best_cost、elite_costs、等 K 均值与配对差
  再与落盘字段、与论文正文（+0.347 / −1.066）逐项比对。

依赖：标准库。
用法：py -3.12 scripts/audit_recompute_selection.py [--tol 1e-6]
"""
import argparse
import io
import json
import math
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CASES = os.path.join(ROOT, "results", "p1", "cases", "main")
SCENARIOS = ["none", "cutin", "lead-brake", "lead-exit"]
SEEDS = [0, 1, 2, 3, 4]
ELITE = 3

PAPER_PRIMARY_MEAN = 0.347    # §4.4 正文
PAPER_EQUAL_K_MEAN = -1.066   # §4.4 正文


def load():
    out = {}
    for sc in SCENARIOS:
        out[sc] = []
        for sd in SEEDS:
            f = os.path.join(CASES, "case_%s_s%d.json" % (sc, sd))
            if not os.path.exists(f):
                raise SystemExit("  ✗ 缺文件：%s" % f)
            out[sc].append(json.load(io.open(f, encoding="utf-8")))
    return out


def arm_recompute(arm):
    """从逐候选记录重建该臂的聚合量。"""
    cands = arm["candidates"]
    valid = [c for c in cands if c["valid"]]
    vc = sorted(c["cost"] for c in valid)
    return dict(
        n_total=len(cands),
        n_valid=len(valid),
        invalid_ratio=round(1.0 - len(valid) / max(len(cands), 1), 4),
        best_cost=vc[0] if vc else None,
        elite_costs=vc[:ELITE],
        valid_costs=vc,
    )


def corr(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sx = math.sqrt(sum((a - mx) ** 2 for a in xs))
    sy = math.sqrt(sum((b - my) ** 2 for b in ys))
    return sxy / (sx * sy) if sx and sy else float("nan")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tol", type=float, default=1e-6)
    args = ap.parse_args()

    rows_by_sc = load()
    fails = []
    prim, eqk = [], []
    n_unequal = 0

    print("  === 择优层重建（逐局比对落盘字段）===")
    print("  %-11s %2s %6s %6s %9s %9s %8s" % ("场景", "s", "nV_off", "nV_on", "best_off", "best_on", "Δprimary"))
    for sc in SCENARIOS:
        for i, r in enumerate(rows_by_sc[sc]):
            sd = SEEDS[i]
            off = arm_recompute(r["arms"]["a1_otf_off"])
            on = arm_recompute(r["arms"]["a1_otf_on"])

            for name, rec, arm in (("off", off, r["arms"]["a1_otf_off"]), ("on", on, r["arms"]["a1_otf_on"])):
                if rec["n_valid"] != arm["n_valid"]:
                    fails.append((sc, sd, name + ".n_valid", rec["n_valid"], arm["n_valid"]))
                if abs(rec["invalid_ratio"] - arm["invalid_ratio"]) > 1e-4:
                    fails.append((sc, sd, name + ".invalid_ratio", rec["invalid_ratio"], arm["invalid_ratio"]))
                if rec["best_cost"] is not None and abs(rec["best_cost"] - arm["best_cost"]) > args.tol:
                    fails.append((sc, sd, name + ".best_cost", rec["best_cost"], arm["best_cost"]))
                for a, b in zip(rec["elite_costs"], arm["elite_costs"]):
                    if abs(a - b) > args.tol:
                        fails.append((sc, sd, name + ".elite", a, b))
                        break

            if off["best_cost"] is not None and on["best_cost"] is not None:
                d = on["best_cost"] - off["best_cost"]
                prim.append(d)
                if abs(d - r["paired"]["delta_cost"]) > 1e-6:
                    fails.append((sc, sd, "delta_cost", d, r["paired"]["delta_cost"]))

            # 等 K：K = min(n_valid_off, n_valid_on)，各取前 K 个有效候选的均值
            K = min(off["n_valid"], on["n_valid"])
            if K >= 1:
                mo = sum(off["valid_costs"][:K]) / K
                mn = sum(on["valid_costs"][:K]) / K
                dk = mn - mo
                eqk.append(dk)
                rec_eq = r["paired"]["equal_k"]
                if abs(dk - rec_eq["delta_cost"]) > 1e-6:
                    fails.append((sc, sd, "equal_k.delta_cost", dk, rec_eq["delta_cost"]))
                if K != rec_eq["k"]:
                    fails.append((sc, sd, "equal_k.k", K, rec_eq["k"]))

            if off["n_valid"] != on["n_valid"]:
                n_unequal += 1
            print("  %-11s %2d %6d %6d %9.3f %9.3f %+8.3f" % (
                sc, sd, off["n_valid"], on["n_valid"],
                off["best_cost"] or float("nan"), on["best_cost"] or float("nan"),
                (on["best_cost"] - off["best_cost"]) if off["best_cost"] and on["best_cost"] else float("nan")))

    print()
    pm = sum(prim) / len(prim)
    em = sum(eqk) / len(eqk)
    print("  === 汇总（20 局，跨场景合并仅作描述）===")
    print("  主口径均值 Δcost      = %+0.3f（论文 §4.4: %+0.3f）" % (pm, PAPER_PRIMARY_MEAN))
    print("  等 K 口径均值 Δcost   = %+0.3f（论文 §4.4: %+0.3f）" % (em, PAPER_EQUAL_K_MEAN))
    print("  方向是否反转          = %s" % ("是" if pm * em < 0 else "否"))
    print("  两臂 n_valid 不等的局数 = %d / 20" % n_unequal)
    if abs(pm - PAPER_PRIMARY_MEAN) > 1e-3:
        fails.append(("ALL", "primary_mean", pm, PAPER_PRIMARY_MEAN))
    if abs(em - PAPER_EQUAL_K_MEAN) > 1e-3:
        fails.append(("ALL", "equal_k_mean", em, PAPER_EQUAL_K_MEAN))

    # P1-F：同种子跨场景 travelled_m 的相关（按臂）
    print()
    print("  === P1-F：无效候选是否由参数化主导（同种子、同候选 k 的 travelled_m 跨场景相关）===")
    for arm in ("a1_otf_off", "a1_otf_on"):
        series = {}
        for sc in SCENARIOS:
            vals = []
            for i in range(len(rows_by_sc[sc])):
                cands = rows_by_sc[sc][i]["arms"][arm]["candidates"]
                vals.extend([c["travelled_m"] for c in sorted(cands, key=lambda x: x["k"])])
            series[sc] = vals
        base = series["none"]
        cs = {sc: corr(base, series[sc]) for sc in SCENARIOS[1:]}
        print("  %-11s r(none,cutin)=%.3f  r(none,brake)=%.3f  r(none,exit)=%.3f" % (
            arm, cs["cutin"], cs["lead-brake"], cs["lead-exit"]))

    print()
    if fails:
        print("  ✗ 与落盘字段/正文不一致 %d 处：" % len(fails))
        for sc, sd, lab, got, want in fails[:15]:
            print("     %-11s s%-2s %-20s got %s want %s" % (sc, sd, lab, got, want))
        return 1
    print("  ✓ 择优层、等K、以及正文两处汇总值全部一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
