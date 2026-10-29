#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把 author-year 引用转成 IEEE 编号制（按正文首次出现顺序编号）。

规则（IEEE）：
- 正文里第一次引用某文献时编号为 [1]，之后复用同一编号；
- 多篇同时引用 → [1], [2]（本稿目前没有多篇并引，脚本仍支持）；
- `Huang (2023)` 这类叙述式 → `Huang [n]`。

输入：papers/p1/manuscript-draft.md + papers/p1/refs.bib
输出：papers/p1/manuscript-ieee.md（含按首次出现排序的 References 段）
      papers/p1/references-ieee.md（单独的参考文献清单，便于投稿系统粘贴）

用法：py -3.12 scripts/to_ieee_citations.py
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
SRC = os.path.join(P, "manuscript-draft.md")
BIB = os.path.join(P, "refs.bib")
OUT = os.path.join(P, "manuscript-ieee.md")
OUTREF = os.path.join(P, "references-ieee.md")

# 正文里出现的 author-year 形式 → bib key
CITES = [
    (r"\((Ploeg et al\., 2014)\)", "ploeg2014lp", "Ploeg et al."),
    (r"\((Stern et al\., 2018)\)", "stern2018dissipation", "Stern et al."),
    (r"\((Wang et al\., 2023)\)", "wang2023deeplcc", "Wang et al."),
    (r"\((Hasani et al\., 2022)\)", "hasani2022cfc", "Hasani et al."),
    (r"\((Antonelo et al\., 2024)\)", "antonelo2024pinn", "Antonelo et al."),
    (r"\((Helbing and Molnár, 1995)\)", "helbing1995social", "Helbing and Molnár"),
    (r"Huang et al\. \(2021a\)", "huang2021sensors", "Huang et al."),
    (r"Huang et al\. \(2021b\)", "huang2021jat", "Huang et al."),
    (r"\(Huang et al\., 2021a\)", "huang2021sensors", ""),
    (r"\(Huang et al\., 2021b\)", "huang2021jat", ""),
    (r"Huang \(2023\)", "huang2023thesis", "Huang"),
]


def parse_bib(path):
    """极简 BibTeX 解析：key → {field: value}。"""
    txt = io.open(path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"@\w+\{([^,]+),([\s\S]*?)\n\}", txt):
        key, body = m.group(1).strip(), m.group(2)
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*\{([\s\S]*?)\}\s*,?\s*\n", body + "\n"):
            fields[fm.group(1).lower()] = fm.group(2).strip()
        out[key] = fields
    return out


def ieee_entry(f):
    """拼 IEEE 风格条目。作者名保持 bib 里的全名（未做缩写转换，避免姓氏出错）。"""
    au = f.get("author", "").replace(" and ", ", ")
    ti = f.get("title", "").strip("{}")
    jr = f.get("journal", "")
    yr = f.get("year", "")
    vol = f.get("volume", "")
    num = f.get("number", "")
    pg = f.get("pages", "")
    doi = f.get("doi", "")
    s = "%s, \"%s,\" %s" % (au, ti, jr) if jr else "%s, \"%s\"" % (au, ti)
    if vol:
        s += ", vol. %s" % vol
    if num:
        s += ", no. %s" % num
    if pg:
        s += ", pp. %s" % pg
    if yr:
        s += ", %s" % yr
    if doi:
        s += ", doi: %s" % doi
    return s + "."


def main() -> int:
    if not (os.path.exists(SRC) and os.path.exists(BIB)):
        print("  ✗ 缺输入文件")
        return 2
    text = io.open(SRC, encoding="utf-8").read()
    bib = parse_bib(BIB)

    # 1) 按首次出现排序
    # ★ 关键：Markdown 会把引用**跨行拆开**（实测 "(Hasani et al.,\n2022)"），
    #   所以模式里的空格必须写成 \s+，否则匹配不到、也不会被残留检查发现。
    def flex(pat):
        return pat.replace(" ", r"\s+")

    order = []
    for pat, key, _ in CITES:
        m = re.search(flex(pat), text)
        if m:
            order.append((m.start(), key))
    order.sort()
    num = {}
    for _, key in order:
        if key not in num:
            num[key] = len(num) + 1

    # 2) 替换
    out = text
    for pat, key, name in CITES:
        if key not in num:
            continue
        n = num[key]
        if name.startswith("Huang"):
            out = re.sub(flex(pat), "Huang [%d]" % n, out)
        else:
            out = re.sub(flex(pat), "[%d]" % n, out)

    # 3) 参考文献段
    lines = ["## References", ""]
    for key, n in sorted(num.items(), key=lambda kv: kv[1]):
        if key == "huang2023thesis":
            lines.append(("[%d] Mengyuan Huang. Research on behavioural decision making for automated " + 
                 "vehicles based on overtaking frequency. Ph.D. dissertation, Jilin University, " + 
                 "Changchun, China, 2023 (in Chinese).") % n)
        elif key in bib:
            lines.append("[%d] %s" % (n, ieee_entry(bib[key])))
        else:
            lines.append("[%d] （缺条目：%s）" % (n, key))

    body = out.rstrip() + "\n\n" + "\n".join(lines) + "\n"
    body = body.replace("<!-- BEGIN-MANUSCRIPT -->", "<!-- BEGIN-MANUSCRIPT -->\n\n> IEEE 编号制版本（由 scripts/to_ieee_citations.py 自动生成，勿手改）")

    io.open(OUT, "w", encoding="utf-8").write(body)
    io.open(OUTREF, "w", encoding="utf-8").write("\n".join(lines) + "\n")

    print("  已写 %s" % OUT)
    print("  已写 %s" % OUTREF)
    print("  编号映射（按首次出现）：")
    for key, n in sorted(num.items(), key=lambda kv: kv[1]):
        print("    [%d] %s" % (n, key))
    # 残留检查也必须允许换行，否则会像第一次那样把跨行引用漏报成 0
    left = re.findall(r"\([A-Z][A-Za-z]+\s+et\s+al\.,\s+\d{4}\)|Huang\s+\(2023\)", out)
    print("  残留 author-year 引用：%d %s" % (len(left), "OK" if not left else left))
    return 0 if not left else 1


if __name__ == "__main__":
    sys.exit(main())
