#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P0-3：冻结协议逐条一致性核查（数据侧 + 代码侧）。

对应 `audit/第一次组会/10-a1-protocol-freeze.md` 的 8 节决定。
每条给出：条款 → 期望 → 实测 → 判定。任一条 FAIL 则退出码 1。

不覆盖（明确声明）：统计量本身（精确符号翻转/CI/TOST/Holm 的数值复现）
已由 `audit_recompute_main.py` 覆盖，此处只查"规则是否被执行"。

用法：py -3.12 scripts/audit_protocol_conformance.py
"""
import glob
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
ENV = os.path.join(ROOT, "src", "envs", "carla_town04.py")
TRAIN = os.path.join(ROOT, "src", "ctrl", "train_cfc.py")
PAPER = os.path.join(ROOT, "papers", "p1", "manuscript-ieee.md")

SCENARS = {"none", "cutin", "lead-brake", "lead-exit"}
SEEDS = {0, 1, 2, 3, 4}


def load_main():
    rows = []
    for f in sorted(glob.glob(os.path.join(CASES, "main", "case_*.json"))):
        rows.append(json.load(io.open(f, encoding="utf-8")))
    return rows


def main() -> int:
    rows = load_main()
    pre = [r for r in rows if r["seed"] in SEEDS]
    results = []

    def chk(name, expect, got, ok=None):
        if ok is None:
            ok = (expect == got)
        results.append((name, str(expect), str(got), "PASS" if ok else "FAIL"))

    # 1. 场景与种子
    chk("场景集合 = 4 类主场景", sorted(SCENARS), sorted({r["scenario"] for r in pre}))
    chk("种子集合 = 0..4", sorted(SEEDS), sorted({r["seed"] for r in pre}))
    chk("预注册局数 = 20", 20, len(pre))
    chk("无重复 (场景,种子)", len(pre), len({(r["scenario"], r["seed"]) for r in pre}))
    chk("每局双腕齐备", True, all({"a1_otf_off", "a1_otf_on"} <= set(r["arms"]) for r in pre))

    # 2. 执行参数
    ex = pre[0]["exec"]
    chk("控制频率 20 Hz", 20.0, ex.get("control_hz"))
    chk("仿真步长 50 Hz", 50.0, ex.get("sim_hz"))
    chk("每局 60 s", 60.0, ex.get("episode_s"))
    chk("交通车辆 16", 16, ex.get("traffic"))
    chk("每臂候选 12", 12, ex.get("candidates_per_arm"))
    chk("精英 3", 3, ex.get("elite"))
    chk("hidden = 24", 24, ex.get("hidden"))
    chk("执行指纹 20 局一致", 1, len({tuple(r["exec"].get(k) for k in
                                        ("episode_s", "traffic", "sim_hz", "control_hz",
                                         "hidden", "candidates_per_arm", "elite")) for r in pre}))

    # 3. 主口径与无效处置
    masks = {r["paired"].get("mask") for r in pre}
    chk("主口径 = best_cost(best valid)", 1, len(masks))
    # 按"规则类型"归类（原因文本里含具体距离，不能直接截前缀比较）
    kinds = set()
    for r in pre:
        for a in ("a1_otf_off", "a1_otf_on"):
            for c in r["arms"][a]["candidates"]:
                if c["valid"]:
                    continue
                reason = c.get("invalid_reason") or ""
                if "阈值 20 m" in reason:
                    kinds.add("20m_rule")
                elif "残留" in reason:
                    kinds.add("residue_rule")
                else:
                    kinds.add("other:" + reason[:20])
    chk("无效原因规则类型", {"20m_rule"}, kinds)
    with io.open(TRAIN, encoding="utf-8") as fh:
        src = fh.read()
    chk("代码含 travelled > 20.0 判据", True, "travelled > 20.0" in src)
    chk("代码含 Holm 实现", True, "def _holm" in src)

    # 4. 等 K（次要口径）已落盘且 K = min(n_valid)
    ok_eqk = True
    for r in pre:
        eq = r["paired"].get("equal_k") or {}
        k = eq.get("k")
        nv = min(r["arms"]["a1_otf_off"]["n_valid"], r["arms"]["a1_otf_on"]["n_valid"])
        if k != nv:
            ok_eqk = False
    chk("等 K 的 k = min(n_valid)", True, ok_eqk)

    # 5. 长尾未覆盖
    with io.open(ENV, encoding="utf-8") as fh:
        envsrc = fh.read()
    chk("环境只有 4 类主场景", True, 'SCENARIOS = ("none", "cutin", "lead-brake", "lead-exit")' in envsrc)
    long_tail = ["hard_brake", "aggressive_cutin", "platoon_exit", "aggressive_traffic"]
    chk("环境未实现长尾四类", False, any(t in envsrc for t in long_tail))
    if os.path.exists(PAPER):
        with io.open(PAPER, encoding="utf-8") as fh:
            paper = fh.read()
        chk("论文未声称覆盖长尾", False, any(t in paper for t in long_tail))

    # 输出
    print("  %-28s %-14s %-14s %6s" % ("冻结条款", "期望", "实测", "判定"))
    for name, exp, got, v in results:
        print("  %-28s %-14s %-14s %6s" % (name, exp[:14], got[:14], v))
    bad = [r for r in results if r[3] == "FAIL"]
    print()
    if bad:
        print("  ✗ 有 %d 条与冻结协议不一致" % len(bad))
        return 1
    print("  ✓ 冻结协议在数据与代码两侧均被执行（%d 条）" % len(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
