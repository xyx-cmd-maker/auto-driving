#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P0-2（数字溯源层）：把摘要与 Fig.2 图注里的每个数字指回源文件。

为什么单独做这一层：
    前三层（统计/择优/补充组）验证的是"表里的数字对不对"，
    但**摘要与图注**里的数字同样会被审稿人引用，且更容易与源脱节。
    本脚本对每个数字打印（论文值 → 源 → 重算值 → PASS/FAIL）。

依赖：标准库。
用法：py -3.12 scripts/audit_number_sources.py
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
SUMO = os.path.join(ROOT, "results", "p1", "otf_density_sweep_sumo_s1-2-3_fine.json")
TGSIM = os.path.join(ROOT, "results", "p1", "otf_real_tgsim_s1.json")


def load_cases(group):
    return [json.load(io.open(f, encoding="utf-8"))
            for f in sorted(glob.glob(os.path.join(CASES, group, "case_*.json")))]


def carla_phi(group, seeds=(0, 1, 2, 3, 4)):
    rows = load_cases(group)
    vals = []
    for f in sorted(glob.glob(os.path.join(CASES, group, "case_*.json"))):
        sd = int(f.split("_s")[-1].split(".")[0])
        if sd not in seeds:
            continue
        d = json.load(io.open(f, encoding="utf-8"))
        vals.append(d["arms"]["a1_otf_on"].get("phi_nonzero_ratio"))
    return st.mean(vals), vals


def main() -> int:
    fails, rows = [], []

    def add(label, where, paper, got, tol):
        ok = got is not None and abs(got - paper) <= tol
        rows.append((label, where, paper, got, "PASS" if ok else "FAIL"))
        if not ok:
            fails.append((label, paper, got))

    # ── SUMO 扫描 ──
    sw = json.load(io.open(SUMO, encoding="utf-8"))["table"]
    w5 = {k: v["W=5"]["nonzero_fraction_mean"] for k, v in sw.items()}
    add("SUMO @600 veh/h, W=5", "摘要", 0.12, w5.get("600"), 5e-3)
    add("SUMO @4800 veh/h, W=5", "摘要", 0.56, w5.get("4800"), 5e-3)
    mid = [w5.get("1800"), w5.get("2400")]
    mid = [x for x in mid if x is not None]
    add("SUMO @1800–2400, W=5（Fig.2）", "Fig.2", 0.39, (sum(mid) / len(mid)) if mid else None, 1e-2)

    # ── TGSIM ──
    tg = json.load(io.open(TGSIM, encoding="utf-8"))
    t5 = tg["aggregate"]["W=5"]["nonzero_fraction_mean"]
    add("TGSIM real, W=5", "摘要/Fig.2", 0.53, t5, 5e-3)

    # ── CARLA 闭环 ──
    m5, v5 = carla_phi("main")
    add("CARLA W=5（跨场景共享值=最小）", "摘要/Fig.2", 0.084, min(v5), 1e-3)
    m10, v10 = carla_phi("window10")
    add("CARLA W=10（跨场景共享值=最小）", "Fig.2", 0.167, min(v10), 2e-3)
    m20, v20 = carla_phi("window20")
    add("CARLA, W=20（lead-brake）", "Fig.2", 0.334, m20, 1e-3)
    m20b, vals20b = carla_phi("window20extra", seeds=(0, 1, 2, 3, 4))
    hi = max(vals20b) if vals20b else None
    add("CARLA, W=20 第三场景上界", "Fig.2", 0.497, hi, 1e-3)

    # ── 设计常数 ──
    ex = load_cases("main")[0]["exec"]
    add("交通车辆数", "摘要（sixteen）", 16, ex.get("traffic"), 0)
    add("控制频率 Hz", "方法", 20.0, ex.get("control_hz"), 1e-9)

    # ── 口径对照：论文取"最小值"，而 TGSIM/SUMO 取"汇总量"。二者不可混用，故单列一行 ──
    rows.append(("CARLA W=5 合并均值（对照）", "口径差异", 0.094, m5, "WARN"))
    rows.append(("CARLA W=10 合并均值（对照）", "口径差异", 0.1916, m10, "WARN"))

    print("  %-28s %-10s %8s %10s %6s" % ("数字", "出处", "论文值", "重算值", "判定"))
    for label, where, paper, got, verdict in rows:
        gs = ("%.4f" % got) if isinstance(got, float) else str(got)
        print("  %-28s %-10s %8.3f %10s %6s" % (label, where, paper, gs, verdict))

    print()
    if fails:
        print("  ✗ 有 %d 个数字与源不一致：" % len(fails))
        for f in fails:
            print("     %-28s 论文 %.4f  源 %s" % (f[0], f[1], f[2]))
        return 1
    print("  ✓ 摘要与 Fig.2 的全部数字均可在仓库内找到源")
    return 0


if __name__ == "__main__":
    sys.exit(main())
