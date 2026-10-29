#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""改投 T-ITS 的重定位补丁（默认 dry-run，不改文件）。

背景（Round 15 判断矩阵）：
  现稿以"OTF 是否有用"为问题，负结果 + 描述性地图，T-IV Regular 的强贡献门槛不足。
  T-ITS 更接受"系统/实践/评估方法"类贡献，因此改投需要**换叙事入口**，不动数据。

三处改动：
  R1 标题：从"提问式"改为"方法/实践式"
  R2 摘要开头两句：把"先测可用性再消融"提到最前（数字、结论全部不动）
  R3 贡献列表：把"可用性地图"提到第 1 条，并加一句给实践者的程序性建议

用法：
    py -3.12 scripts/apply_retarget.py            # dry-run
    py -3.12 scripts/apply_retarget.py --apply    # 应用并重建
"""
import argparse
import io
import os
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
P = os.path.join(ROOT, "papers", "p1")

EDITS = [
    dict(id="R1", file="01-abstract-final.md",
         why="T-ITS 标题：提问式 → 方法/实践式",
         old="**When Is Overtaking Frequency Informative? A Pre-Registered Closed-Loop Ablation and an Availability Map**",
         new="**Measure the Signal Before You Ablate It: Availability of a Traffic-Level Scalar and a Pre-Registered Closed-Loop Equivalence Study**"),

    dict(id="R2", file="01-abstract-final.md",
         why="T-ITS 摘要入口：把程序性缺口提到最前",
         old=("Multi-lane highways produce a continuous stream of lane changes around any vehicle, and a scalar summary\n"
              "of that pressure is an attractive controller input because it costs no extra sensor. Whether such a\n"
              "scalar is ever non-zero is rarely measured before it is ablated, and in a sparse simulator it may never\n"
              "be. We make that measurement before the ablation."),
         new=("A scalar summary of the traffic around a vehicle is an attractive controller input because it costs\n"
              "no extra sensor, and multi-lane highways supply a continuous stream of lane changes to compute it\n"
              "from. Whether such a scalar is ever non-zero is rarely measured before it is ablated, and in a sparse\n"
              "simulator it may never be. We make that measurement before the ablation.")),

    dict(id="R3", file="02-introduction-discussion.md",
         why="T-ITS 贡献顺序：测量优先，并加程序性建议",
         old=("This paper makes three contributions.\n\n"
              "1. A closed-loop ablation of OTF under an equal search budget, reported per scenario with an\n"
              "   equivalence test that was registered before the data were collected. Two of four scenarios are\n"
              "   statistically equivalent on composite driving cost within a 10% margin (TOST p = 0.020 and 0.006);\n"
              "   the other two are inconclusive.\n"
              "2. A measured map of OTF availability as a function of traffic flow and window length, obtained with\n"
              "   the same OTF definition used by the controller. The map shows that availability is governed by\n"
              "   density and window jointly, and that our closed-loop setting is in its lower region.\n"
              "3. An explicit account of why the experiment cannot support a superiority claim even if a difference exists:\n"
              "   with five seeds the exact paired test cannot reach significance after multiplicity correction. We\n"
              "   therefore target equivalence, and we report the equal-K sensitivity analysis that reverses the sign\n"
              "   of the effect estimate."),
         new=("This paper makes three contributions, ordered from measurement to inference.\n\n"
              "1. A measured map of OTF availability as a function of traffic flow and window length, obtained with\n"
              "   the same OTF definition used by the controller. The map shows that availability is governed by\n"
              "   density and window jointly, and that our closed-loop setting is in its lower region.\n"
              "2. A closed-loop ablation of OTF under an equal search budget, reported per scenario with an\n"
              "   equivalence test that was registered before the data were collected. Two of four scenarios are\n"
              "   statistically equivalent on composite driving cost within a 10% margin (TOST p = 0.020 and 0.006);\n"
              "   the other two are inconclusive.\n"
              "3. An explicit account of why the experiment cannot support a superiority claim even if a difference exists:\n"
              "   with five seeds the exact paired test cannot reach significance after multiplicity correction. We\n"
              "   therefore target equivalence, and we report the equal-K sensitivity analysis that reverses the sign\n"
              "   of the effect estimate.\n\n"
              "The recommendation for practice is procedural rather than numerical: measure availability before\n"
              "ablating a traffic-level signal, and report the operating point alongside the ablation.")),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    report, ok_all = [], True
    for e in EDITS:
        path = os.path.join(P, e["file"])
        txt = io.open(path, encoding="utf-8").read()
        n = txt.count(e["old"])
        ok = (n == 1)
        ok_all &= ok
        report.append((e["id"], e["file"], "OK" if ok else ("DUP" if n > 1 else "MISSING"), n))
        if args.apply and ok:
            io.open(path, "w", encoding="utf-8", newline="").write(txt.replace(e["old"], e["new"], 1))

    print("  模式 = %s ｜ %d 处改动" % ("APPLY" if args.apply else "DRY-RUN", len(EDITS)))
    print("  %-4s %-32s %-10s %4s" % ("id", "file", "状态", "命中"))
    for i, f, st, n in report:
        print("  %-4s %-32s %-10s %4d" % (i, f, st, n))
    if not ok_all:
        print("\n  ✗ 有锚点不唯一，未应用")
        return 1
    if not args.apply:
        print("\n  ✓ 三处锚点唯一：py -3.12 scripts/apply_retarget.py --apply")
        return 0

    print("\n  已应用，重建产物 …")
    for cmd in (["py", "-3.12", os.path.join(ROOT, "scripts", "assemble_manuscript.py")],
                ["py", "-3.12", os.path.join(ROOT, "scripts", "to_ieee_citations.py")],
                ["py", "-3.12", os.path.join(ROOT, "scripts", "to_latex.py")]):
        if subprocess.run(cmd, cwd=ROOT).returncode != 0:
            print("  ✗ 失败：%s" % " ".join(cmd))
            return 1
    print("  ✓ 已重建（PDF 需在 papers/p1 下再跑 pdflatex ×2）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
