#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把分散的章节拼成一份完整初稿 papers/p1/manuscript-draft.md。

纪律：
- 只取各文件 `<!-- BEGIN-MANUSCRIPT -->` 与 `<!-- END-MANUSCRIPT -->` 之间的**稿件正文**，
  元信息（数字来源、待核实引用、写作备注）一律不进入初稿。
- 顺序：Title/Abstract/Keywords → 1 Introduction → 2 Methods → 3 Related work
        → 4 Results（来自 _results-fragment.md）→ 5 Discussion → 图表注。
- 输出文件整体加 MANUSCRIPT 标记，便于 `_check_manuscript.mjs` 直接跑全文合规检查。

用法：py -3.12 scripts/assemble_manuscript.py
"""
import io
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
P = os.path.join(ROOT, "papers", "p1")
OUT = os.path.join(P, "manuscript-draft.md")

B, E = "<!-- BEGIN-MANUSCRIPT -->", "<!-- END-MANUSCRIPT -->"


def body(name: str) -> str:
    with io.open(os.path.join(P, name), encoding="utf-8") as f:
        s = f.read()
    a, b = s.find(B), s.find(E)
    if a >= 0 and b > a:
        return s[a + len(B):b].strip()
    return s.strip()


def after(text: str, marker: str) -> str:
    i = text.find(marker)
    if i < 0:
        raise SystemExit("缺少标记: %s" % marker)
    return text[i:].strip()


def before(text: str, marker: str) -> str:
    i = text.find(marker)
    if i < 0:
        raise SystemExit("缺少标记: %s" % marker)
    return text[:i].strip()


# 1) 标题 + 摘要 + 关键词
a = body("01-abstract-final.md")
head = before(a, "## 主张")      # 去掉"主张→证据映射"及之后

# 2) Introduction + Discussion（同一文件）
d = body("02-introduction-discussion.md")
intro = before(d, "# 5. Discussion")
disc = after(d, "# 5. Discussion")

# 3) Methods / Related
methods = body("03-methods.md")
related = body("04-related-work.md")

# 4) Results + 图注
rf = body("_results-fragment.md")
results = before(rf, "## 图注")
caps = after(rf, "## 图注")

parts = [
    B,
    "# Overtaking Pressure on Multi-Lane Highways as a Control Input for Continuous-Time Car-Following",
    "",
    after(head, "## Abstract"),
    "",
    "---",
    "",
    intro,
    "",
    methods,
    "",
    related,
    "",
    results,
    "",
    disc,
    "",
    "# Figure and table captions",
    "",
    caps,
    "",
    E,
    "",
    "---",
    "",
    "> **本文件是自动拼装的初稿**（`scripts/assemble_manuscript.py`）。",
    "> 章节来源：`01-abstract-final.md` / `02-introduction-discussion.md` / `03-methods.md` /",
    "> `04-related-work.md` / `_results-fragment.md`。**改稿请改源文件再重新拼装**，不要直接改本文件。",
    "> 图表：Fig.1 `figs/fig1_scenario.pdf`（A 场景 / B 计数规则）｜ Fig.2 `figs/fig2_availability_real.pdf`（A 可用性相图 / B 三来源对比）。",
]

out = "\n".join(parts) + "\n"
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(out)

words = len(re.findall(r"[A-Za-z][A-Za-z'\-]+", out))
print("  已写 %s" % OUT)
print("  英文字词数 ≈ %d ｜ 行数 %d" % (words, out.count("\n")))
for name, seg in (("Abstract", after(head, "## Abstract")), ("Intro", intro),
                  ("Methods", methods), ("Related", related),
                  ("Results", results), ("Discussion", disc)):
    print("    %-11s %5d words" % (name, len(re.findall(r"[A-Za-z][A-Za-z'\-]+", seg))))
