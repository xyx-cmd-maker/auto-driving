#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把 manuscript-ieee.md 转成可编译的 IEEEtran LaTeX。

只处理本稿实际用到的 Markdown 子集：标题层级、段落、管道表格、加粗/斜体、
少量数学符号（− ≤ × Δ Φ ±）；其余字符做 LaTeX 转义。

产物：papers/p1/manuscript.tex
注意：本机**未安装 LaTeX**，脚本只能生成源码，**无法在此验证编译与真实页数**。
      请在装有 TeX Live / Overleaf 的环境编译后核对页数（Regular 上限 10 页）。

用法：py -3.12 scripts/to_latex.py
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
SRC = os.path.join(P, "manuscript-ieee.md")
OUT = os.path.join(P, "manuscript.tex")

SYM = {
    "\u2212": "$-$", "\u2264": "$\\leq$", "\u2265": "$\\geq$", "\u00d7": "$\\times$",
    "\u0394": "$\\Delta$", "\u03a6": "$\\Phi$", "\u00b1": "$\\pm$", "\u2013": "--",
    "\u2014": "---", "\u2018": "'", "\u2019": "'", "\u201c": "``", "\u201d": "''",
    "\u2192": "$\\rightarrow$", "\u00b0": "$^\\circ$",
}


def esc(s: str) -> str:
    for k, v in SYM.items():
        s = s.replace(k, v)
    s = s.replace("\\", r"\textbackslash{}")
    for ch, rep in (("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
                    ("_", r"\_"), ("{", r"\{"), ("}", r"\}")):
        s = s.replace(ch, rep)
    # 上面把 \$ 也替换了，数学符号里的 $ 需要还原
    s = s.replace(r"\textbackslash{}\$", "$")
    s = re.sub(r"\\\$\\times\\\$", r"$\\times$", s)
    return s


def inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\\textit{\1}", s)
    s = s.replace(r"\$", "$")
    return s


def table(rows):
    """rows: ['| a | b |', '|---|---|', ...] → tabular。"""
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [c for c in cells if not all(re.fullmatch(r":?-{3,}:?", x or "-") for x in c)]
    if not cells:
        return ""
    n = max(len(r) for r in cells)
    spec = "l" + "r" * (n - 1)
    out = [r"\begin{table}[!t]", r"\centering", r"\footnotesize",
           r"\begin{tabular}{%s}" % spec, r"\hline"]
    for i, r in enumerate(cells):
        r = r + [""] * (n - len(r))
        out.append(" & ".join(inline(x) for x in r) + r" \\")
        if i == 0:
            out.append(r"\hline")
    out += [r"\hline", r"\end{tabular}", r"\end{table}", ""]
    return "\n".join(out)


def main() -> int:
    if not os.path.exists(SRC):
        print("  ✗ 缺 %s" % SRC)
        return 2
    lines = io.open(SRC, encoding="utf-8").read().split("\n")

    body, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("<!--"):                     # 注释跳过
            i += 1
            continue
        if ln.strip() in ("---", ""):
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            lvl, txt = len(m.group(1)), inline(m.group(2))
            cmd = {1: "section", 2: "subsection", 3: "subsubsection", 4: "paragraph"}[lvl]
            body.append("\\%s*{%s}" % (cmd, txt) if lvl == 1 else "\\%s{%s}" % (cmd, txt))
            i += 1
            continue
        if ln.lstrip().startswith("|"):                # 表格块
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(lines[i]); i += 1
            body.append(table(rows))
            continue
        if ln.lstrip().startswith("- "):               # 列表
            body.append(r"\begin{itemize}")
            while i < len(lines) and lines[i].lstrip().startswith("- "):
                body.append(r"  \item " + inline(lines[i].lstrip()[2:]))
                i += 1
            body.append(r"\end{itemize}")
            continue
        body.append(inline(ln))
        i += 1

    tex = r"""\documentclass[journal]{IEEEtran}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{cite}

\begin{document}

\title{Overtaking Pressure on Multi-Lane Highways as a Control Input\\ for Continuous-Time Car-Following}

\author{Xia~Yuxuan and Huang~Mengyuan% <- 通讯作者
\thanks{Manuscript received XXXX; revised XXXX.}
\thanks{X.~Yuxuan and H.~Mengyuan are with Shenzhen Polytechnic University, Shenzhen, China
(e-mail: xiayuxuan@mail.szpu.edu.cn; huangmy2215@szpu.edu.cn).}}

\maketitle

\begin{abstract}
%(abstract)s
\end{abstract}

\begin{IEEEkeywords}
overtaking frequency, traffic-flow scalar, continuous-time neural control, equivalence testing
\end{IEEEkeywords}

%(body)s

\section*{Acknowledgment}
%(ack)s

\begin{thebibliography}{1}
%(refs)s
\end{thebibliography}

\end{document}
"""

    # 抽出摘要与正文、参考文献
    text = "\n".join(body)
    m_abs = re.search(r"\\section\*\{Abstract\}\s*(.+?)\\section", text, re.S)
    abstract = m_abs.group(1).strip() if m_abs else "ABSTRACT PLACEHOLDER"
    text = re.sub(r"\\section\*\{Abstract\}.*?\\section", r"\\section", text, flags=re.S)
    text = re.sub(r"\\section\*\{Keywords\}.*?\\section", r"\\section", text, flags=re.S)

    m_ref = re.search(r"\\section\*\{References\}(.*)$", text, re.S)
    refs_raw = m_ref.group(1) if m_ref else ""
    text = re.sub(r"\\section\*\{References\}.*$", "", text, flags=re.S)

    bib = []
    for ln in refs_raw.split("\n"):
        mm = re.match(r"\[(\d+)\]\s+(.*)", ln.strip())
        if mm:
            bib.append(r"\bibitem{ref%s} %s" % (mm.group(1), mm.group(2)))
    if not bib:
        bib = [r"\bibitem{ref1} REFERENCES PENDING"]

    # 图占位：正文里若有 figs/ 引用，插入 figure 环境
    figblock = r"""\begin{figure}[!t]
\centering
\includegraphics[width=\columnwidth]{figs/fig1_scenario.pdf}
\caption{Overtaking pressure and its measurement. See the caption file for the full text.}
\label{fig:fig1}
\end{figure}"""

    out = tex % {
        "abstract": abstract,
        "body": text.strip() + "\n\n" + figblock,
        "ack": "The authors thank the Federal Highway Administration for releasing the TGSIM corpus in the public domain.",
        "refs": "\n".join(bib),
    }
    io.open(OUT, "w", encoding="utf-8").write(out)
    print("  已写 %s（%d 行）" % (OUT, out.count("\n")))
    print("  ⚠ 本机未装 LaTeX：**无法在此编译**，页数需在 Overleaf/TeX Live 上核对（Regular 上限 10 页）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
