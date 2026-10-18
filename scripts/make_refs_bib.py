#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""从**已核验**的 P1 文献库生成 IEEE 模板可直接 \\cite 的 BibTeX。

纪律
----
- **只从 `literature/library/P1-library.jsonl` 取数**（该库每条带 `verification.verdict`），
  **不接受手写条目**，避免把记忆里的作者/页码写进 .bib。
- 只输出 `verdict == OK` 的条目；任何非 OK 条目**跳过并打印警告**。
- 条目键用 `第一作者姓+年份+关键词`，与稿件正文的 author-year 一一对应。

用法：py -3.12 scripts/make_refs_bib.py
产出：papers/p1/refs.bib
"""
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
LIB = os.path.join(ROOT, "literature", "library", "P1-library.jsonl")
OUT = os.path.join(ROOT, "papers", "p1", "refs.bib")

# 稿件正文实际引用的条目（title 子串 → bib key）
WANT = [
    ("Lp String Stability of Cascaded Systems", "ploeg2014lp"),
    ("Dissipation of stop-and-go waves", "stern2018dissipation"),
    ("DeeP-LCC", "wang2023deeplcc"),
    ("Closed-form continuous-time neural networks", "hasani2022cfc"),
    ("Physics-informed neural nets for control", "antonelo2024pinn"),
    ("Social force model for pedestrian dynamics", "helbing1995social"),
]


def esc(s: str) -> str:
    s = (s or "")
    # 弯引号/破折号会让 pdflatex 在部分编码下报错，统一成 ASCII
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2013", "--").replace("\u2014", "---")
    return s.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")


def authors_bib(names):
    """**原样保留**库内作者名，只做 and 连接。

    ★ 为什么不做 "姓, 名" 转换（2026-10-18 修）：
    naive 的"最后一词为姓"规则会把荷兰/意大利姓氏切坏——
    `Nathan van de Wouw` → `Wouw, N. v. d.`，`Maria Laura Delle Monache` → `Monache, M. L. D.`，
    两者都是错的。BibTeX 的 author 字段**原生接受** "First von Last" 全名顺序，
    所以最安全的是**不转换**。宁可格式朴素，不可姓名出错。
    """
    return " and ".join(n.strip() for n in names if n and n.strip())


def main() -> int:
    if not os.path.exists(LIB):
        print("  ✗ 缺库文件: %s" % LIB)
        return 2
    rows = []
    with io.open(LIB, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except Exception:
                    pass

    entries, missing, skipped = [], [], []
    for sub, key in WANT:
        hit = [r for r in rows if sub.lower() in (r.get("title") or "").lower()]
        if not hit:
            missing.append(sub)
            continue
        r = hit[0]
        v = r.get("verification") or {}
        if str(v.get("verdict", "")).upper() != "OK":
            skipped.append((sub, v.get("verdict")))
            continue
        venue = r.get("venue") or ""
        kind = "article"
        fields = [
            ("author", authors_bib(r.get("authors") or [])),
            ("title", "{%s}" % esc(r.get("title"))),
            ("journal", esc(venue)),
            ("year", str(r.get("year") or "")),
            ("volume", str(r.get("volume") or "")),
            ("number", str(r.get("issue") or "")),
            ("pages", (r.get("page") or "").replace("-", "--")),
            ("doi", r.get("doi") or ""),
        ]
        body = ",\n".join("  %s = {%s}" % (k, val) for k, val in fields if val)
        entries.append("@%s{%s,\n%s\n}" % (kind, key, body))

    head = [
        "% 由 scripts/make_refs_bib.py 自动生成，**请勿手改**。",
        "% 数据源：literature/library/P1-library.jsonl（仅收录 verification.verdict = OK 的条目）。",
        "%% 条目数：%d" % len(entries),
        "",
    ]
    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(head) + "\n\n".join(entries) + "\n")

    print("  已写 %s（%d 条）" % (OUT, len(entries)))
    for sub, key in WANT:
        ok = any(k == key for k in re.findall(r"@article\{(\w+),", "\n".join(entries)))
        print("    %-12s %s" % (key, "OK" if ok else "缺失"))
    if missing:
        print("  ✗ 库内未找到：%s" % "; ".join(missing))
    if skipped:
        print("  ⚠ 因核验状态非 OK 而跳过：%s" % "; ".join("%s(%s)" % x for x in skipped))
    return 0 if not missing and not skipped else 1


if __name__ == "__main__":
    sys.exit(main())
