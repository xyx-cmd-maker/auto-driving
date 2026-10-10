# 把 meeting2 的核心卡片装配进主报告（含标题降级）。
# 用法: python assemble_meeting2_report.py
import os, re

NOTES = r"D:\Deepseek Harness\auto-driving\literature\meeting2\notes"
REPORT = r"D:\Deepseek Harness\auto-driving\literature\meeting2\01-P1核心文献阅读总结.md"
MARKER = "<!-- INSERT_CARDS -->"

CORE = [
    ("icml2018-td3.md", "核心 #1", "TD3 原文（ICML 2018）"),
    ("scirebotics2023-chahine-lnn-flight.md", "核心 #2", "Chahine：LNN 分布外鲁棒飞行（Science Robotics 2023）"),
    ("ltc-aaai2021.md", "核心 #3", "LTC 液态时间常数网络（AAAI 2021）"),
    ("cfc-nmi2022.md", "核心 #4", "CfC 闭式连续时间神经网络（NMI 2022）"),
    ("ral2022-interpretable-flight-ncp.md", "核心 #5", "NCP 可解释自主飞行（RA-L 2022）"),
    ("tits2025-gnn-mpc-interactive.md", "核心 #6", "GNN+MPC 分层交互决策 HDM（T-ITS 2025）"),
    ("tits2022-drl-ad-survey-kiran.md", "核心 #7", "DRL 自动驾驶综述 Kiran（T-ITS 2022）"),
    ("nmi2023-fptt-snn.md", "核心 #8", "FPTT 在线训练脉冲网络（NMI 2023）"),
    ("tits2026-safety-enhanced-drl-mistakes.md", "核心 #9", "敢犯错的动态安全引导 DRL（T-ITS 2026）"),
    ("tits2020-highway-motion-planning-review.md", "核心 #10", "高速公路运动规划综述（T-ITS 2020）"),
    ("tits2025-lead.md", "核心 #11", "LEAD：博弈+最大熵 IRL（T-ITS 2025）"),
]

APPENDIX = ("nmi2021-deeponet-VoR.md", "附录卡 A", "DeepONet NMI 2021 正式版核验卡")


def slice_card(path):
    t = open(path, encoding="utf-8").read()
    i = t.find("## 1. 标题")
    j = t.find("## 6.")
    if i < 0:
        raise SystemExit("no section 1 in " + path)
    body = t[i:j].rstrip() if j > i else t[i:].rstrip()
    out = []
    for line in body.split("\n"):
        m = re.match(r"^(#{2,5}) (.*)$", line)
        out.append("#" + m.group(1) + " " + m.group(2) if m else line)
    return "\n".join(out)


def block(fname, tag, label):
    body = slice_card(os.path.join(NOTES, fname))
    return ("#### %s ｜ %s\n\n"
            "> 卡片全文（含「对 P1 的用处 / 缺失信息 / 关键数字表 / 内部不一致」）：[`notes/%s`](notes/%s)\n\n"
            "%s\n" % (tag, label, fname, fname, body))


parts = [block(*c) for c in CORE]
parts.append("#### 5.1 附录：DeepONet 正式版核验卡（不计入核心 11 篇）\n\n"
             "> 这是 `notes/nmi2021-deeponet.md`（依据 arXiv v3 预印本）的**正式版配套卡**，"
             "解决的是「这篇到底是哪一版、哪些数字能引」的问题。\n\n" + block(*APPENDIX))
assembled = "\n---\n\n".join(parts)

t = open(REPORT, encoding="utf-8").read()
if MARKER not in t:
    raise SystemExit("marker missing - report already assembled?")
t = t.replace(MARKER, assembled)
open(REPORT, "w", encoding="utf-8").write(t)
print("SPLICED core=%d + appendix=1, report chars=%d lines=%d"
      % (len(CORE), len(t), t.count("\n") + 1))
for f, tag, _ in CORE:
    print("  %-46s -> %s" % (f, tag))
print("  %-46s -> %s" % (APPENDIX[0], APPENDIX[1]))
