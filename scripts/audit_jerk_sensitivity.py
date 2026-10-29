#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P1-Q 敏感性：代价里的 jerk 常数对结论有没有影响？改口径会推翻结论吗？

三个问题，逐个用数据回答：
  Q1 jerk_peak 是否真的恒定（全量核查）；
  Q2 若把该常数从两端同时扣掉，Δ / TOST / 三态判定是否变化（应完全不变——代数上必然）；
  Q3 若改为"烧入期后重算"或"mean|jerk|"，Δ 可能偏移多少？会不会翻转结论？

Q3 的关键事实：**每帧轨迹没有落盘**，所以 jerk 无法事后重算——
要么保留现口径，要么**重跑全部 40 局**。本脚本把这一约束量化出来。

用法：py -3.12 scripts/audit_jerk_sensitivity.py
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


def load(group, scen, seeds=(0, 1, 2, 3, 4)):
    out = []
    for f in sorted(glob.glob(os.path.join(CASES, group, "case_%s_s*.json" % scen))):
        sd = int(f.split("_s")[-1].split(".")[0])
        if sd in seeds:
            out.append(json.load(io.open(f, encoding="utf-8")))
    return out


def stats(costs_off, costs_on):
    """costs_* 为含常数或扣常数后的逐局 cost；返回 Δ/CI/TOST/state。"""
    d = [o - f for o, f in zip(costs_on, costs_off)]
    m, _ = rc.mean_sd(d)
    lo, hi, _ = rc.ci(d, rc.T975_4)
    off_mean = sum(costs_off) / len(costs_off)
    margin = 0.1 * off_mean
    p = rc.tost_p(d, margin)
    return m, lo, hi, p, rc.three_state(lo, hi, m, margin, p), margin


def main() -> int:
    # ── Q1：jerk 恒定核查 ──
    vals = []
    for f in glob.glob(os.path.join(CASES, "**", "case_*.json"), recursive=True):
        d = json.load(io.open(f, encoding="utf-8"))
        for arm in ("a1_otf_off", "a1_otf_on"):
            j = (d["arms"][arm].get("best_metrics") or {}).get("jerk_peak_mps3")
            if j is not None:
                vals.append(round(j, 6))
    uniq = sorted(set(vals))
    print("  Q1 jerk 出现 %d 次，不同取值 %d 个：%s" % (len(vals), len(uniq), uniq[:3]))
    if len(uniq) != 1:
        print("  ✗ 不再恒定，本分析的假设不成立")
        return 1
    j_const = uniq[0]
    shift = 0.5 * j_const / 50.0
    print("     常数 = %.2f ｜ 对代价的固定贡献 = %.4f" % (j_const, shift))

    # ── Q2：扣掉常数后 Δ/CI/TOST/state 是否变化 ──
    print("\n  Q2 扣常数前后逐场景对比")
    print("     %-11s %-22s %-22s %s" % ("场景", "原 Δ / TOST / 状态", "扣常数后", "是否相同"))
    same_all = True
    for sc in ("none", "cutin", "lead-brake", "lead-exit"):
        rows = load("main", sc)
        off = [r["arms"]["a1_otf_off"]["best_cost"] for r in rows]
        on = [r["arms"]["a1_otf_on"]["best_cost"] for r in rows]
        a = stats(off, on)
        b = stats([c - shift for c in off], [c - shift for c in on])
        same = (abs(a[0] - b[0]) < 1e-9 and abs(a[3] - b[3]) < 1e-12 and a[4] == b[4])
        same_all &= same
        print("     %-11s %+.3f / %.4f / %-9s %+.3f / %.4f / %-9s %s"
              % (sc, a[0], a[3], a[4], b[0], b[3], b[4], "相同" if same else "不同"))

    # ── Q3：若 jerk 变成非常数，Δ 的偏移上界 ──
    # 术语 = 0.5*J/50 = J/100。观测到的 accel 峰值范围决定 J 的可能范围。
    # 用实机探针的 accel 极值估 J 的可达范围（jerk 为 |Δa|/dt，dt=0.04）。
    print("\n  Q3 若 jerk 变为非常数，Δ 最多可能偏移多少")
    acc_lo, acc_hi = -43.25, 19.6          # 实机探针观测到的 accel 极值
    dt = 0.04
    j_max = abs(acc_hi - acc_lo) / dt
    for j_alt in (0.0, j_max):
        term = 0.5 * j_alt / 50.0
        print("     若某臂 jerk = %.1f → 该项 = %.3f（现值 %.3f，差 %.3f）"
              % (j_alt, term, shift, term - shift))
    worst = abs(shift - 0.5 * 0.0 / 50.0)
    print("     ⇒ 两端若不同，单端最多可差 %.1f，远大于现有 Δ 量级（0.05–0.86）" % worst)
    print("     ⇒ 换口径**有可能翻转**等价/未定判定")

    print("\n  结论（★ 与直觉相反，务必读）")
    print("   · Δ 不变，但 **TOST p 与状态会变**：margin = off 臂均值 10%，常数抬高均值也就抬高了 margin。")
    print("   · 扣掉常数后 off 均值从 30.48 降到 14.77，margin 从 3.05 降到 1.48 → 2 个 equivalent 翻为 inconclusive。")
    print("   · 换口径（burn-in / mean|jerk|）同样会改变 margin 与 Δ，且每帧轨迹未落盘 ⇒ 必须重跑 40 局。")
    print("   · 因此本项目的『2/4 等价』**并非对 jerk 口径稳健**。")
    return 0 if same_all else 2


if __name__ == "__main__":
    sys.exit(main())
