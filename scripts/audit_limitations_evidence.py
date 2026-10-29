#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P0-4 支撑：把 §5.5 的六条 Limitations 逐条与证据对照。

目的：Limitations 是审稿人判断"作者是否诚实"的第一入口。
若限制写得比证据更弱（漏报），会被认为隐瞒；写得比证据更强（虚报），会被认为不自信。
本脚本把能机器核的核掉，核不了的标 U（无产物），并**不**把 U 当错误。

用法：py -3.12 scripts/audit_limitations_evidence.py
"""
import glob
import importlib.util
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
TGSIM = os.path.join(ROOT, "results", "p1", "otf_real_tgsim_s1.json")
ENV = os.path.join(ROOT, "src", "envs", "carla_town04.py")

spec = importlib.util.spec_from_file_location("rc", os.path.join(ROOT, "scripts", "audit_recompute_main.py"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)  # noqa: E402


def phi_pre():
    vals = []
    for f in glob.glob(os.path.join(CASES, "main", "case_*.json")):
        sd = int(f.split("_s")[-1].split(".")[0])
        if sd > 4:
            continue
        d = json.load(io.open(f, encoding="utf-8"))
        vals.append(d["arms"]["a1_otf_on"]["phi_nonzero_ratio"])
    return vals


def primitive():
    prim, eqk = [], []
    for f in glob.glob(os.path.join(CASES, "main", "case_*.json")):
        sd = int(f.split("_s")[-1].split(".")[0])
        if sd > 4:
            continue
        d = json.load(io.open(f, encoding="utf-8"))
        prim.append(d["paired"]["delta_cost"])
        eqk.append(d["paired"]["equal_k"]["delta_cost"])
    return st.mean(prim), st.mean(eqk)


def main() -> int:
    rows = []

    # 1. Power
    p_min = rc.exact_signflip_p([1.0] * 5)
    rows.append(("1 Power：n=5 时可达最小 exact p", "0.0625", "%.4f" % p_min,
                 "PASS" if abs(p_min - 0.0625) < 1e-12 else "FAIL"))
    holm = 0.05 / 4
    rows.append(("1 Power：Holm 阈值 α/4", "0.0125", "%.4f" % holm, "PASS"))

    # 2. Metric dependence
    prim, eqk = primitive()
    ok2 = abs(prim - 0.35) < 0.01 and abs(eqk + 1.07) < 0.01
    rows.append(("2 Metric：主口径 → +0.35", "+0.35", "%+.3f" % prim, "PASS" if ok2 else "FAIL"))
    rows.append(("2 Metric：等 K → −1.07", "−1.07", "%+.3f" % eqk, "PASS" if ok2 else "FAIL"))

    # 3. Regime
    v = phi_pre()
    lo, hi = min(v), max(v)
    ok3 = abs(lo - 0.084) < 1e-3 and abs(hi - 0.168) < 1e-3
    rows.append(("3 Regime：主实验 8%–17%", "0.084–0.168", "%.3f–%.3f" % (lo, hi), "PASS" if ok3 else "FAIL"))
    sup = st.mean([json.load(io.open(f, encoding="utf-8"))["arms"]["a1_otf_on"]["phi_nonzero_ratio"]
                   for f in glob.glob(os.path.join(CASES, "window20", "case_*.json"))])
    rows.append(("3 Regime：补充组 33%", "0.334", "%.3f" % sup, "PASS" if abs(sup - 0.334) < 1e-3 else "FAIL"))
    tg = json.load(io.open(TGSIM, encoding="utf-8"))["aggregate"]["W=5"]["nonzero_fraction_mean"]
    rows.append(("3 Regime：真实交通 53%", "0.53", "%.4f" % tg, "PASS" if abs(tg - 0.53) < 5e-3 else "FAIL"))

    # 4. Constructed traffic（代码证据）
    with io.open(ENV, encoding="utf-8") as fh:
        envsrc = fh.read()
    has_inject = "force_lane_change" in envsrc or "teleport" in envsrc or "_inject" in envsrc
    rows.append(("4 Constructed：脚本化注入存在", "True", str(has_inject), "PASS" if has_inject else "FAIL"))

    # 5. Platform
    d = json.load(io.open(glob.glob(os.path.join(CASES, "main", "case_*.json"))[0], encoding="utf-8"))
    ex = d["exec"]
    ok5 = abs(ex.get("control_hz", 0) - 20.0) < 1e-9
    rows.append(("5 Platform：控制 20 Hz", "20.0", str(ex.get("control_hz")), "PASS" if ok5 else "FAIL"))

    # 6. Real trajectories open loop only（缺失即证据）
    closed = glob.glob(os.path.join(CASES, "**", "*tgsim*"), recursive=True)
    rows.append(("6 Open loop：无 TGSIM 闭环产物", "0 个", "%d 个" % len(closed), "PASS" if not closed else "FAIL"))

    # U：§5.3 说的是 **CARLA Traffic Manager** 的 60 s 探针（两次换道）
    #    注意：SUMO 侧的同类探针（本轮新增）**不能**顶替它——换了模拟器。
    carla_probe = [p for p in glob.glob(os.path.join(ROOT, "results", "p1", "*lanecount*"))
                   if "sumo" not in os.path.basename(p)]
    rows.append(("U 探针：CARLA 两次换道的产物", "≥1 个", "%d 个" % len(carla_probe),
                 "U（无产物）" if not carla_probe else "PASS"))

    # INFO：SUMO 侧的同类探针（本轮新增，是另一个事实，不是上一条的证据）
    sumo_p = os.path.join(ROOT, "results", "p1", "sumo_lanecount_probe_s1.json")
    if os.path.exists(sumo_p):
        d = json.load(io.open(sumo_p, encoding="utf-8"))
        rows.append(("INFO SUMO 60 s 探针（另一模拟器）", "—",
                     "换道 %d 次 / 跨 ego %d 次" % (d.get("lane_changes_total", -1),
                                                     d.get("lane_changes_across_ego", -1)), "INFO"))
    else:
        rows.append(("INFO SUMO 60 s 探针（另一模拟器）", "—", "无产物", "INFO"))

    print("  %-34s %-14s %-16s %s" % ("Limitations 条目", "论文值", "证据/重算", "判定"))
    for a, b, c, v_ in rows:
        print("  %-34s %-14s %-16s %s" % (a, b, c, v_))
    print()
    fails = [r for r in rows if r[3] == "FAIL"]
    u = [r for r in rows if r[3].startswith("U")]
    print("  PASS = %d ｜ FAIL = %d ｜ U（无产物）= %d" % (len(rows) - len(fails) - len(u), len(fails), len(u)))
    if fails:
        return 1
    print("  ✓ 六条 Limitations 均不弱于证据；其中 1 条证据缺失（U，建议补产物）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
