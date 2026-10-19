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
    # 上标（"1 s⁻¹" 之类）：pdflatex 对 U+207B/U+2075 直接报 Unicode 错
    "\u207b\u00b9": "$^{-1}$", "\u207b": "$^{-}$", "\u2075": "$^{5}$",
    "\u00b9": "$^{1}$", "\u00b2": "$^{2}$", "\u00b3": "$^{3}$", "\u2074": "$^{4}$",
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
    # ★ 必须限制宽度：直接排 tabular 会超出栏宽并与相邻浮动体重叠（2026-10-19 实测）。
    #   用 resizebox 缩到栏宽，是 IEEE 模板里最稳的做法。
    out = [r"\begin{table}[!t]", r"\centering",
           r"\resizebox{\columnwidth}{!}{%",
           r"\begin{tabular}{%s}" % spec, r"\hline"]
    for i, r in enumerate(cells):
        r = r + [""] * (n - len(r))
        out.append(" & ".join(inline(x) for x in r) + r" \\")
        if i == 0:
            out.append(r"\hline")
    out += [r"\hline", r"\end{tabular}", r"}", r"\end{table}", ""]
    return "\n".join(out)


def main() -> int:
    if not os.path.exists(SRC):
        print("  ✗ 缺 %s" % SRC)
        return 2
    lines = io.open(SRC, encoding="utf-8").read().split("\n")

    body, i = [], 0
    while i < len(lines):
        ln = lines[i]
        # ★ 跳过含中日韩字符的行：这些是元信息（如自动生成的"IEEE 编号制版本"注），
        #   pdflatex 遇到 U+7F16 会直接 Fatal error（实测）。
        if re.search(r"[\u3000-\u303f\u3040-\u30ff\u4e00-\u9fff\uff00-\uffef]", ln):
            i += 1
            continue
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

\title{When Is Overtaking Frequency Informative? A Pre-Registered\\ Closed-Loop Ablation and an Availability Map}

\author{Xia~Yuxuan and Huang~Mengyuan% corresponding author
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

%(bios)s

\end{document}
"""

    # 抽出摘要与正文、参考文献
    # ★ 标题层级：Markdown 的 `## Abstract` 会转成 \subsection{Abstract}，
    #   所以正则必须同时接受 \section / \subsection（首版只匹配 \section，导致摘要丢失）。
    SEQ = r"\\(?:sub)?section\*?"
    text = "\n".join(body)
    m_abs = re.search(SEQ + r"\{Abstract\}\s*(.+?)" + SEQ + r"\{", text, re.S)
    abstract = m_abs.group(1).strip() if m_abs else "ABSTRACT PLACEHOLDER"
    text = re.sub(SEQ + r"\{Abstract\}.*?" + SEQ, r"\\section", text, flags=re.S)
    text = re.sub(SEQ + r"\{Keywords\}.*?" + SEQ, r"\\section", text, flags=re.S)

    m_ref = re.search(SEQ + r"\{References\}(.*)$", text, re.S)
    refs_raw = m_ref.group(1) if m_ref else ""
    text = re.sub(SEQ + r"\{References\}.*$", "", text, flags=re.S)

    bib = []
    for ln in refs_raw.split("\n"):
        mm = re.match(r"\[(\d+)\]\s+(.*)", ln.strip())
        if mm:
            bib.append(r"\bibitem{ref%s} %s" % (mm.group(1), mm.group(2)))
    if not bib:
        bib = [r"\bibitem{ref1} REFERENCES PENDING"]

    # 图占位：正文里若有 figs/ 引用，插入 figure 环境
    # ★ 图注与作者小传从源文件读取，避免 .tex 与 markdown 分叉（2026-10-19）
    def grab_para(md: str, prefix: str) -> str:
        """取以 prefix 开头的段落（到空行为止），转 LaTeX。"""
        lines = md.split("\n")
        for k, ln in enumerate(lines):
            if ln.strip().startswith(prefix):
                buf = [ln.strip()]
                j = k + 1
                # 取到下一个二级标题为止（首版只取到空行，导致 Fig.2 的"三条限制"整段丢失）
                while j < len(lines) and not lines[j].startswith("## "):
                    s = lines[j].strip()
                    if s:
                        buf.append(s.lstrip("- ").strip())
                    j += 1
                return inline(" ".join(buf))
        return ""

    figs_md = io.open(os.path.join(P, "05-figures.md"), encoding="utf-8").read()
    cap1 = grab_para(figs_md, "**Overtaking pressure")
    cap2 = grab_para(figs_md, "**Availability in synthetic")

    figblock = "\n".join([
        r"\begin{figure}[!t]",
        r"\centering",
        r"\includegraphics[width=\columnwidth]{figs/fig1_scenario.pdf}",
        r"\caption{%s}" % cap1,
        r"\label{fig:fig1}",
        r"\end{figure}",
        "",
        r"\begin{figure}[!t]",
        r"\centering",
        r"\includegraphics[width=\columnwidth]{figs/fig2_availability_real.pdf}",
        r"\caption{%s}" % cap2,
        r"\label{fig:fig2}",
        r"\end{figure}",
    ])

    # 作者小传：**硬编码**（2026-10-19 由抓取改为固定文本）。
    # 抓取版会把 markdown 的 ">" 前缀、中文核对注、以及重复变体一起带进来，
    # 编译后出现 "> Huang Mengyuan ..." 与乱码——实测事故，不再抓取。
    bio_huang = (
        "Huang Mengyuan received the B.E. degree in automotive operation engineering from Jilin "
        "University, Changchun, China, in 2017, and the Ph.D. degree in vehicle operation "
        "engineering from Jilin University in 2023. She is currently a Lecturer with Shenzhen "
        "Polytechnic University, Shenzhen, China. Her research interests include perception, "
        "prediction, and decision making for autonomous driving, and vehicle-road cooperation."
    )
    bio_xia = (
        "Xia Yuxuan is currently pursuing the B.Eng. degree in intelligent connected vehicle "
        "engineering with Shenzhen Polytechnic University, Shenzhen, China. His research interests "
        "include autonomous driving, embodied intelligence, and large language models."
    )
    bioblock = ("\\section*{Author Biographies}\n\n"
                "\\noindent\\textbf{Huang Mengyuan}\\par\\noindent " + bio_huang + "\n\n"
                "\\noindent\\textbf{Xia Yuxuan}\\par\\noindent " + bio_xia + "\n")
    bioblock = (appblock + "\n\n" + bioblock).strip()

    # ★ 不能用 `%` 格式化：LaTeX 模板里到处是 `%`（注释符），会触发
    #   "unsupported format character"。改用逐项 replace。
    out = tex
    for key, val in (("%(abstract)s", abstract),
                     ("%(body)s", text.strip() + "\n\n" + figblock),
                     ("%(ack)s", "The authors thank the Federal Highway Administration for releasing the TGSIM corpus in the public domain."),
                     ("%(refs)s", "\n".join(bib)),
                     ("%(bios)s", bioblock)):
        out = out.replace(key, val)
    # 最终兜底：剥掉任何中文/全角字符（版本注释、核对注记等），
    # pdflatex 遇到 U+4E00 以上会 Fatal error。
    out = re.sub(r"[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]+", " ", out)
    io.open(OUT, "w", encoding="utf-8").write(out)
    print("  已写 %s（%d 行）" % (OUT, out.count("\n")))
    print("  ⚠ 本机未装 LaTeX：**无法在此编译**，页数需在 Overleaf/TeX Live 上核对（Regular 上限 10 页）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
