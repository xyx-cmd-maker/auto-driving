# 把 fresh2024 的 11 张卡装配进增量报告（标题降一级）
import os, re

NOTES = r"D:\Deepseek Harness\auto-driving\literature\fresh2024\notes"
REPORT = r"D:\Deepseek Harness\auto-driving\literature\fresh2024\01-2024增量分诊.md"
MARKER = "<!-- INSERT_CARDS -->"

CARDS = [
    ("natcommun2025-platoon-knowledge-guided.md", "增量 #1", "知识引导自学习混行编队控制（Nature Communications 2025）· 20/20 · A"),
    ("arxiv2026-lnn-edge-compression.md", "增量 #2", "LNN 边缘压缩（ICPR 2026）· 15/20 · A(分)/C(材料)"),
    ("arxiv2025-platoon-risk-potential-field.md", "增量 #3", "多车道编队重构：风险势场+博弈+RL（arXiv 2025）· 14/20 · A(分)/C(材料)"),
    ("arxiv2026-lateral-string-stability.md", "增量 #4", "横向弦稳定性（ACC 2026 / arXiv 2026）· 14/20 · B"),
    ("tcst2024-physics-augmented-deeplcc.md", "增量 #5", "物理增强 DeeP-LCC（IEEE TCST 2024）· 14/20 · A(临界)"),
    ("electronics2026-overtaking-hierarchical-rl.md", "增量 #6", "超车分层强化学习（Electronics 2026）· 14/20 · B"),
    ("inffus2026-platoon-physics-encoded-dl.md", "增量 #7", "物理编码的编队动力学建模（Information Fusion 2026）· 13/20 · B"),
    ("trc2024-stopandgo-learning-cf.md", "增量 #8", "停走波与学习型跟驰训练（TR-C 2024 / ISTTT 25）· 13/20 · B"),
    ("trf2025-overtaking-truck-platoons-human-drivers.md", "增量 #9", "超越自动卡车编队的人因研究（TR-F 2025）· 13/20 · B"),
    ("tiv2024-safe-rl-mixed-platoon.md", "增量 #10", "混行编队系统级安全 RL（IEEE T-IV 2024）· 11/20 · B"),
    ("sensors2025-tinyml-ondevice-survey.md", "增量 #11", "TinyML 与端侧推理综述（Sensors 2025）· 11/20 · B"),
]


def slice_card(path):
    t = open(path, encoding="utf-8").read()
    i = t.find("## 1. 标题")
    if i < 0:  # 有的卡用别的写法，退回到第一个二级标题
        m = re.search(r"^## ", t, re.M)
        i = m.start() if m else 0
    j = t.find("## 6.")
    body = t[i:j].rstrip() if j > i else t[i:].rstrip()
    out = []
    for line in body.split("\n"):
        m = re.match(r"^(#{2,5}) (.*)$", line)
        out.append("#" + m.group(1) + " " + m.group(2) if m else line)
    return "\n".join(out)


parts = []
for fname, tag, label in CARDS:
    p = os.path.join(NOTES, fname)
    if not os.path.exists(p):
        print("MISSING", fname); continue
    parts.append("#### %s ｜ %s\n\n> 卡片全文（含「对 P1 的用处 / 缺失信息 / 关键数字表 / 内部不一致」）：[`notes/%s`](notes/%s)\n\n%s\n"
                 % (tag, label, fname, fname, slice_card(p)))
assembled = "\n---\n\n".join(parts)

t = open(REPORT, encoding="utf-8").read()
if MARKER not in t:
    raise SystemExit("marker missing")
t = t.replace(MARKER, assembled)
open(REPORT, "w", encoding="utf-8").write(t)
print("SPLICED %d cards, report chars=%d lines=%d" % (len(parts), len(t), t.count("\n") + 1))
