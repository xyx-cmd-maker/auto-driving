#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Graphical abstract（T-IV 投稿系统里最显眼的一张图）。

三块布局（缩略图尺寸下仍可读，因此**不用热图、用条形**）：
  左  场景示意：三车道 + ego + 邻道车 + 跨车道箭头（OTF +1）
  中  可用性对比：W = 5 s 下三个来源的非零窗口比例（recorded 0.53 / synthetic 0.39 / our loop 0.084）
  右  结论条：Explainability, not performance.

纪律：Okabe–Ito 配色；灰度可读（条形有数值标签）；不出现 real-world validation；
不得把 0.084 画成"提升"。数字来源 results/p1/otf_real_tgsim_s1.json 与 otf_density_sweep_*_fine.json。

用法：py -3.14 scripts/figures/fig_graphical_abstract.py
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "papers", "p1", "figs")

BLUE, ORANGE, GREEN, GREY = "#0072B2", "#D55E00", "#009E73", "#555555"
FS = 8.0


def panel_scene(ax):
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.2)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    for i in range(3):
        ax.add_patch(Rectangle((0, i), 10, 1.0, facecolor="#f6f6f6" if i % 2 == 0 else "white",
                               edgecolor="none", zorder=0))
    for y in (1.0, 2.0):
        ax.plot([0, 10], [y, y], color="0.6", lw=0.9, ls=(0, (5, 4)))
    ax.plot([0, 10], [0, 0], color="0.3", lw=1.1)
    ax.plot([0, 10], [3.0, 3.0], color="0.3", lw=1.1)

    def car(x, y, c, label=None, w=1.0, h=0.44):
        ax.add_patch(Rectangle((x - w / 2, y + 0.5 - h / 2), w, h, facecolor=c,
                               edgecolor="white", lw=0.8, zorder=4))
        if label:
            ax.text(x, y + 0.5, label, ha="center", va="center", color="white",
                    fontsize=FS - 1, zorder=5)

    car(2.0, 1.0, BLUE, "ego")
    car(5.4, 1.0, GREY, "lead")
    car(3.2, 2.0, "#9a9a9a")
    car(7.6, 2.0, "#9a9a9a")
    ax.add_patch(FancyArrowPatch((3.2, 2.26), (3.2, 1.46), arrowstyle="-|>",
                                 mutation_scale=10, lw=1.6, color=ORANGE, zorder=6))
    ax.text(2.95, 2.42, "OTF +1", fontsize=FS, color=ORANGE, ha="right", va="bottom", zorder=7)
    ax.set_title("overtaking pressure", fontsize=FS, loc="left", pad=2)


def panel_bars(ax):
    labels = ["recorded\n(TGSIM)", "synthetic\n(SUMO)", "our loop\n(CARLA)"]
    vals = [0.532, 0.390, 0.084]
    colors = [GREEN, BLUE, ORANGE]
    x = np.arange(3)
    ax.bar(x, vals, width=0.55, color=colors, edgecolor="white", lw=0.6, zorder=3)
    for xi, v in zip(x, vals):
        # 第三个数保留三位（0.084 是全文反复引用的关键值），前两个两位即可
        txt = "%.3f" % v if v < 0.1 else "%.2f" % v
        ax.text(xi, v + 0.03, txt, ha="center", va="bottom", fontsize=FS - 0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=FS - 1.2)
    ax.set_ylim(0, 0.72)
    ax.set_ylabel("P(OTF > 0) at $W$ = 5 s", fontsize=FS - 0.5)
    ax.tick_params(labelsize=FS - 1.2, width=0.5, length=2, pad=1.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="0.92", lw=0.5, zorder=0)
    ax.set_title("how often the signal is non-zero", fontsize=FS, loc="left", pad=2)


def panel_claim(ax):
    ax.axis("off")
    ax.text(0.0, 0.66, "Explainability,", fontsize=FS + 5, fontweight="bold",
            va="center", ha="left", color="0.1")
    ax.text(0.0, 0.40, "not performance.", fontsize=FS + 5, fontweight="bold",
            va="center", ha="left", color=ORANGE)
    ax.text(0.0, 0.14, "same cost, no extra sensor", fontsize=FS - 0.5,
            va="center", ha="left", color="0.35")


def main() -> int:
    fig = plt.figure(figsize=(7.2, 2.1), dpi=300)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.05, 1.0, 1.0], wspace=0.32)
    panel_scene(fig.add_subplot(gs[0, 0]))
    panel_bars(fig.add_subplot(gs[0, 1]))
    panel_claim(fig.add_subplot(gs[0, 2]))

    os.makedirs(OUT, exist_ok=True)
    for ext in ("png", "pdf"):
        p = os.path.join(OUT, "graphical_abstract." + ext)
        fig.savefig(p, bbox_inches="tight", pad_inches=0.04)
        print("  wrote %s" % p)
    plt.close(fig)
    print("  尺寸 %.1f x %.1f in @300 dpi = %d px 宽" % (7.2, 2.1, int(7.2 * 300)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
