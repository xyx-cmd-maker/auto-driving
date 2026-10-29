#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""待作者批准的补丁集（默认 dry-run，不改文件）。

背景（T-IV 红队 Round 07/09/10）：
  - P1-M：Fig.2 三个来源用了三种统计量，且论文从未定义。
  - P0-1-B：论文写"进入 +1/离开 −1"，实现里正常驶出返回 0。
  - P1-N：§4.1 的局数写错（16/4），数据是 17/3。
  - P0-1 术语：§5.2 写 windows，实际统计量是 control cycles（帧）。
  - P2（可选）：无 Δv 组的 OTF 开/关结果未写进正文。

本脚本把这些编辑写成**可审查的 old→new 对**：
  默认 dry-run，只报告每个锚点是否**恰好出现一次**（可安全替换）；
  加 --apply 才真正写入，并自动重拼装 + 重转换 + 重编译。

用法：
    py -3.12 scripts/apply_pending_edits.py            # 只看能不能改
    py -3.12 scripts/apply_pending_edits.py --apply    # 真改
    py -3.12 scripts/apply_pending_edits.py --apply --with-dv-result   # 连带写无Δv结果
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
    # ── E1：摘要补范围（+2 词，仍在 250 词内）───────────────────────────
    dict(id="E1", why="P1-M：摘要只写了最小值，补上范围",
         file="01-abstract-final.md",
         old="loop, with sixteen mixed vehicles, reaches only 0.084.",
         new="loop, with sixteen mixed vehicles, reaches only 0.084 to 0.168."),

    # ── E2：Fig.2 图注声明统计量不同 ─────────────────────────────────
    dict(id="E2", why="P1-M：三个来源的统计量不同，必须显式声明",
         file="05-figures.md",
         old="by two of the three scenarios. At a 5 s window the fractions are 0.39, 0.53 and 0.084.",
         new=("by two of the three scenarios. At a 5 s window the fractions are 0.39, 0.53 and 0.084. "
              "Each source uses its own statistic: a mean over runs for SUMO and TGSIM, and the value "
              "shared by three scenarios for our loop. The three points are descriptive rather than "
              "like-for-like.")),

    # ── E3：§4.1 局数纠错 + 定义（帧 vs 窗口）────────────────────────
    dict(id="E3", why="P1-N：16/4 与数据不符；并定义统计量是帧不是窗口",
         file="_results-fragment.md",
         old=("The treatment variable was active in every run. The fraction of control cycles with OTF > 0 was 0.084\n"
              "in sixteen runs and 0.167 in four."),
         new=("The treatment variable was active in every run. The fraction of control cycles with a non-zero net\n"
              "crossing in the trailing window was 0.084 in seventeen runs and 0.168 in three. A control cycle is\n"
              "one 20 Hz observation step, so this is a fraction of time rather than of disjoint windows.")),

    # ── E4：§5.2 术语从 windows 改为 control cycles ───────────────────
    dict(id="E4", why="P0-1 术语：同一统计量在 5.2 里被写成 windows，与 4.1 冲突",
         file="02-introduction-discussion.md",
         old=("main experiment the fraction of windows with OTF > 0 was 0.084 to 0.167, so the fourth input was zero\n"
              "for most of every episode."),
         new=("main experiment the fraction of control cycles with a non-zero net crossing was 0.084 to 0.168, so\n"
              "the fourth input was zero for most of every episode.")),

    # ── E7：§5.3 的 0.32 未写明流量，且与 Fig.2 的 0.39 不同 ─────────
    dict(id="E7", why="P1-O：0.32 是未声明流量的插值；表中无此行",
         file="02-introduction-discussion.md",
         old=("At the flow equivalent of our CARLA setting, the SUMO map predicts an availability near 0.32, while\n"
              "CARLA produced 0.084."),
         new=("At the flow equivalent of our CARLA setting, about 1400 vehicles per hour, the SUMO map predicts an\n"
              "availability near 0.32 when interpolated between its 1200 and 1800 rows, while CARLA produced 0.084.")),
    # ── E5：§5.3 给 TGSIM 的 0.53 加上统计量说明 ─────────────────────
    dict(id="E5", why="P1-M：0.53 是 10 次 run 的均值，正文未说明",
         file="02-introduction-discussion.md",
         old="1800 to 2400 vehicles per hour, the measured fraction at a 5 s window was 0.53.",
         new="1800 to 2400 vehicles per hour, the measured fraction at a 5 s window was 0.53, averaged over ten runs."),
]

EDIT_DV = dict(
    id="E6", why="P2：无 Δv 组的 OTF 开/关结论（本轮新分析，n=5，p=0.375）",
    file="02-introduction-discussion.md",
    old="off-arm cost moved by 0.14, from 30.82 with ten runs to 30.96 with five, and the two ranges overlap",
    new=("off-arm cost moved by 0.14, from 30.82 with ten runs to 30.96 with five, and the two ranges overlap\n"
         "almost exactly. Removing the input did not make OTF useful either: in the same five runs the paired\n"
         "difference between the two arms was +1.26, with a 95 percent interval of -2.17 to +4.68 and an exact\n"
         "p of 0.375."),
)


def apply_one(edit, do_apply, report):
    path = os.path.join(P, edit["file"])
    if not os.path.exists(path):
        report.append((edit["id"], edit["file"], "FILE-MISSING", 0, False))
        return
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(edit["old"])
    ok = (n == 1)
    report.append((edit["id"], edit["file"], "OK" if ok else "ANCHOR-%s" % ("DUP" if n > 1 else "MISSING"), n, ok))
    if do_apply and ok:
        io.open(path, "w", encoding="utf-8", newline="").write(txt.replace(edit["old"], edit["new"], 1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="真正写入（默认 dry-run）")
    ap.add_argument("--with-dv-result", action="store_true", help="连带应用 E6（无 Δv 结果）")
    args = ap.parse_args()

    edits = list(EDITS) + ([EDIT_DV] if args.with_dv_result else [])
    report = []
    for e in edits:
        apply_one(e, args.apply, report)

    print("  模式 = %s ｜ 编辑数 = %d" % ("APPLY" if args.apply else "DRY-RUN", len(edits)))
    print("  %-4s %-34s %-14s %4s %5s" % ("id", "file", "状态", "命中", "可应用"))
    for i, f, st, n, ok in report:
        print("  %-4s %-34s %-14s %4d %5s" % (i, f, st, n, "YES" if ok else "NO"))
    bad = [r for r in report if not r[4]]
    if bad:
        print()
        print("  ✗ %d 条锚点不唯一，未应用任何改动（dry-run 不写盘，apply 也只跳过坏锚点）" % len(bad))
        return 1
    if not args.apply:
        print()
        print("  ✓ 全部锚点唯一，可用于一键应用：py -3.12 scripts/apply_pending_edits.py --apply")
        return 0

    print()
    print("  已应用，开始重拼装/重转换/重编译 …")
    for cmd in (["py", "-3.12", os.path.join(ROOT, "scripts", "assemble_manuscript.py")],
                ["py", "-3.12", os.path.join(ROOT, "scripts", "to_ieee_citations.py")],
                ["py", "-3.12", os.path.join(ROOT, "scripts", "to_latex.py")]):
        r = subprocess.run(cmd, cwd=ROOT)
        if r.returncode != 0:
            print("  ✗ 失败：%s" % " ".join(cmd))
            return 1
    print("  ✓ 三份产物已重建（PDF 需在 papers/p1 下再跑 pdflatex ×2）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
