#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""导出 A1 全量 20 局的逐局明细（供 audit/15 引用；用完即弃）。

输出：audit/第一次组会/15-a1-full-results.data.md（表格）+ 控制台摘要
"""
import glob
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
CASES = os.path.join(ROOT, "runs", "p1", "cases")
OUT = os.path.join(ROOT, "audit", "第一次组会", "15-a1-full-results.data.md")

files = sorted(glob.glob(os.path.join(CASES, "case_*.json")))
if not files:
    print("  ✗ 无结果文件")
    sys.exit(1)

rows = []
for f in files:
    d = json.load(io.open(f, encoding="utf-8"))
    on, off = d["arms"]["a1_otf_on"], d["arms"]["a1_otf_off"]
    p = d["paired"]
    eq = p.get("equal_k") or {}
    rows.append({
        "case": "%s/s%d" % (d["scenario"], d["seed"]),
        "scenario": d["scenario"],
        "seed": d["seed"],
        "cost_off": off["best_cost"],
        "cost_on": on["best_cost"],
        "d_cost": p["delta_cost"],
        "d_cost_eqk": eq.get("delta_cost"),
        "k": eq.get("k"),
        "n_valid_off": off.get("n_valid"),
        "n_valid_on": on.get("n_valid"),
        "d_rmse": p.get("delta_following_rmse"),
        "d_accel": p.get("delta_accel_sq_integral"),
        "d_coll": p.get("delta_collision"),
        "phi": on.get("phi_nonzero_ratio"),
        "travelled_off": (d.get("guards", {}).get("a1_otf_off") or {}).get("travelled_m"),
        "travelled_on": (d.get("guards", {}).get("a1_otf_on") or {}).get("travelled_m"),
        "exec": d.get("exec"),
    })

rows.sort(key=lambda r: (["none", "cutin", "lead-brake", "lead-exit"].index(r["scenario"]), r["seed"]))

hdr = ["case", "Δcost", "Δcost等K", "K", "off有效", "on有效",
       "Δ跟车RMSE", "Δ加速度", "Δ碰撞", "Φ_OTF"]
lines = ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
for r in rows:
    lines.append("| %s | %+.3f | %s | %s | %s | %s | %s | %s | %+d | %.3f |" % (
        r["case"], r["d_cost"],
        ("%+.3f" % r["d_cost_eqk"]) if r["d_cost_eqk"] is not None else "n/a",
        r["k"], r["n_valid_off"], r["n_valid_on"],
        ("%+.2f" % r["d_rmse"]) if r["d_rmse"] is not None else "n/a",
        ("%+.2f" % r["d_accel"]) if r["d_accel"] is not None else "n/a",
        r["d_coll"], r["phi"] or 0.0))

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("# A1 全量 20 局逐局明细（自动生成，勿手改）\n\n")
    f.write("> 来源：`runs/p1/cases/case_*.json`；生成脚本 `scripts/dump_a1_cases.py`。\n")
    f.write("> 负值 Δ = on 臂更小（更好）；Δcost 为**主口径**（各取最好有效候选），Δcost等K 为敏感性分析。\n\n")
    f.write("\n".join(lines) + "\n\n")
    ex = rows[0]["exec"]
    f.write("执行指纹（20 局应完全一致）：`%s`\n" % json.dumps(ex, ensure_ascii=False))

print("  已写 %s（%d 局）" % (OUT, len(rows)))
print()
print("  逐局 Δcost（主口径）与 Δcost(等K)：")
for r in rows:
    print("    %-16s best %+7.3f ｜ eqK %s ｜ K=%s ｜ 有效 off/on = %d/%d ｜ Φ=%.3f"
          % (r["case"], r["d_cost"],
             ("%+7.3f" % r["d_cost_eqk"]) if r["d_cost_eqk"] is not None else "   n/a",
             r["k"], r["n_valid_off"], r["n_valid_on"], r["phi"] or 0.0))

# 关键汇总
import statistics as st
d_best = [r["d_cost"] for r in rows]
d_eqk = [r["d_cost_eqk"] for r in rows if r["d_cost_eqk"] is not None]
coll = [r["d_coll"] for r in rows]
print()
print("  主口径 Δcost：均值 %+.4f ｜ 中位 %+.4f ｜ 最小 %+.4f ｜ 最大 %+.4f"
      % (st.mean(d_best), st.median(d_best), min(d_best), max(d_best)))
print("  等K  Δcost：均值 %+.4f ｜ 中位 %+.4f ｜ 最小 %+.4f ｜ 最大 %+.4f"
      % (st.mean(d_eqk), st.median(d_eqk), min(d_eqk), max(d_eqk)))
print("  碰撞 Δ 合计 = %d（全 0 表示两臂都无碰撞）" % sum(coll))
print("  Φ_OTF 取值集合 = %s" % sorted({round(r["phi"], 4) for r in rows if r["phi"] is not None}))
print("  执行指纹一致 = %s" % (len({json.dumps(r["exec"], sort_keys=True) for r in rows}) == 1))
