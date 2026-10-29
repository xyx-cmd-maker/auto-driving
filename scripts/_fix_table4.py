# -*- coding: utf-8 -*-
"""把 09-appendix.md 的 Table IV 收窄到单栏宽度（Overfull hbox 75pt 修复）。

做法：
  1. 去掉末尾的 Group 列（信息改为表下一句说明）；
  2. 保持其余 7 列与短场景名。
"""
import io
import re

P = "papers/p1/09-appendix.md"
t = io.open(P, encoding="utf-8").read()
lines = t.split("\n")
out = []
removed = 0
for ln in lines:
    m = re.match(r"^(\|.*?)\s*\|\s*(main|no-dv)\s*\|\s*$", ln)
    if m and ln.strip().startswith("|"):
        out.append(m.group(1) + " |")
        removed += 1
    else:
        out.append(ln)
t2 = "\n".join(out)
if "no-dv" not in t2.split("##")[0]:
    pass
# 在表后（文件末尾的空行前）补一句分组说明
if "first twenty rows" not in t2:
    t2 = t2.rstrip("\n") + (
        "\n\nThe first twenty rows are the main group; the last five repeat the "
        "lead-brake scenario with relative speed removed from the observation.\n")
io.open(P, "w", encoding="utf-8", newline="").write(t2)
print("  去掉 Group 列的行数 =", removed)
print("  新表头 =", [l for l in t2.split("\n") if l.startswith("| Scen")][0])
