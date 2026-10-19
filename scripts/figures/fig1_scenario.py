#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fig. 1：三联概念图（T-IV 要求 Figure 1 必须是交通场景示意图）。

(a) 场景示意：三车道高速，ego + 前车 + 邻道车，一辆车跨越 ego 车道（= 一次 OTF 事件）
(b) 计数几何：时间—车道平面上的轨迹，跨越 ego 车道 +1，驶离 −1，窗口 W
(c) 可用性相图：密度 × 窗口的非零比例（数据来自 SUMO 细扫描）

绘图纪律（scientific-visualization）：单行三栏、色盲友好（Okabe–Ito）、
直接标注不靠图例、无 chartjunk、矢量 PDF + 300 dpi PNG、字号按印刷尺寸设定。

用法（本机仅 py3.14 有 matplotlib）：
  py -3.14 scripts/figures/fig1_scenario.py
"""
import io
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(ROOT, "results", "p1", "otf_density_sweep_sumo_s1-2-3_fine.json")
OUT = os.path.join(ROOT, "papers", "p1", "figs")

BLUE, ORANGE, GREEN, GREY = "#0072B2", "#D55E00", "#009E73", "#666666"
FS = 7.0          # 轴标签字号（scientific-visualization: 轴标签 7–9 pt）
TICK = 6.5        # 刻度字号（6–8 pt）
PANEL = FS + 1.5  # 面板字母（加粗）


def panel_a(ax):
    """场景示意：三车道 + ego + 前车 + 邻道车 + 一次跨车道事件。"""
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.6)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    # 三条车道（y 带宽 1.0）
    for i in range(3):
        ax.add_patch(Rectangle((0, i), 10, 1.0, facecolor="#f7f7f7" if i % 2 == 0 else "white",
                               edgecolor="none", zorder=0))
    for y in (1.0, 2.0):
        ax.plot([0, 10], [y, y], color="0.55", lw=0.8, ls=(0, (5, 4)), zorder=1)
    ax.plot([0, 10], [0, 0], color="0.35", lw=1.0, zorder=1)
    ax.plot([0, 10], [3.0, 3.0], color="0.35", lw=1.0, zorder=1)

    def car(x, y, color, label=None, w=1.15, h=0.44, fs=FS - 1.2):
        ax.add_patch(Rectangle((x - w / 2, y + 0.5 - h / 2), w, h, facecolor=color,
                               edgecolor="white", lw=0.6, zorder=4))
        if label:
            ax.text(x, y + 0.5, label, ha="center", va="center", color="white",
                    fontsize=fs, zorder=5)

    # ego 在中间车道
    car(2.0, 1.0, BLUE, "ego")
    # 前车
    car(5.2, 1.0, GREY, "lead")
    # 邻道车（上道）—— 靠近 ego 的那辆正好是跨车道事件的起点
    car(3.1, 2.0, "#999999", "")
    car(7.6, 2.0, "#999999", "")
    # 邻道车（下道）
    car(6.4, 0.0, "#bbbbbb", "")

    # 跨车道事件：上道车 t1 位置 → 切到 ego 道（放在 ego 与前车之间，避开遮挡）
    ax.add_patch(FancyArrowPatch((3.1, 2.28), (3.1, 1.44), arrowstyle="-|>",
                                 mutation_scale=7, lw=1.1, color=ORANGE, zorder=6))
    ax.text(3.28, 2.02, "+1", fontsize=FS - 0.5, color=ORANGE, ha="left", va="bottom", zorder=7)

    # 定量事实（前车搜索 ≤150 m、v≤30 m/s、窗口 5 s）放在**图注**里，
    # 不画进示意图：实测加上尺寸箭头后与 "OTF +1"/"ego"/"lead" 标签互相遮挡，
    # 清晰性优先于信息密度（2026-10-18 自审）。
    ax.set_title("Three-lane highway", fontsize=FS, loc="left", pad=3, color="black")
    ax.text(-0.02, 1.16, "A", transform=ax.transAxes, fontsize=PANEL,
            fontweight="bold", ha="left", va="top")


def panel_b(ax):
    """计数几何：时间—车道平面的轨迹与窗口。"""
    ax.set_xlim(0, 10); ax.set_ylim(-0.2, 3.2)
    ax.set_yticks([0.5, 1.5, 2.5])
    ax.set_yticklabels(["lane 1", "lane 2 (ego)", "lane 3"], fontsize=FS - 0.5)
    ax.set_xlabel("time (s)", fontsize=FS, labelpad=1.5)
    ax.tick_params(labelsize=FS - 0.5, width=0.5, length=2, pad=1.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(0.5)

    # ego 车道带
    ax.add_patch(Rectangle((0, 1.0), 10, 1.0, facecolor=BLUE, alpha=0.07, edgecolor="none", zorder=0))
    for y in (1.0, 2.0):
        ax.plot([0, 10], [y, y], color="0.8", lw=0.5, zorder=1)

    # 车 A：从 lane 3 切入 ego 车道（+1）
    ax.plot([1.0, 4.2], [2.5, 2.5], color=ORANGE, lw=1.2, zorder=3)
    ax.plot([4.2, 4.9], [2.5, 1.5], color=ORANGE, lw=1.2, zorder=3)
    ax.plot([4.9, 9.0], [1.5, 1.5], color=ORANGE, lw=1.2, zorder=3)
    ax.plot([4.55], [2.0], marker="o", ms=3.2, color=ORANGE, zorder=4)
    ax.text(4.62, 2.12, "+1", fontsize=FS, color=ORANGE, va="bottom")

    # 车 B：从 ego 车道驶出到 lane 1（−1）
    ax.plot([1.4, 6.6], [1.5, 1.5], color=GREEN, lw=1.2, zorder=3)
    ax.plot([6.6, 7.3], [1.5, 0.5], color=GREEN, lw=1.2, zorder=3)
    ax.plot([7.3, 9.4], [0.5, 0.5], color=GREEN, lw=1.2, zorder=3)
    ax.plot([6.95], [1.0], marker="o", ms=3.2, color=GREEN, zorder=4)
    ax.text(7.55, 0.80, "−1", fontsize=FS, color=GREEN, va="bottom", ha="left", zorder=5)

    # 窗口 W
    ax.axvspan(3.6, 8.6, facecolor="0.5", alpha=0.10, edgecolor="none", zorder=0)
    ax.annotate("", xy=(8.6, 3.02), xytext=(3.6, 3.02),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.7, color="0.25", mutation_scale=5))
    ax.text(6.1, 3.08, "window $W$", fontsize=FS - 0.5, ha="center", va="bottom", color="0.25")

    ax.set_title("Crossing the ego lane", fontsize=FS, loc="left", pad=3)
    ax.text(-0.10, 1.16, "B", transform=ax.transAxes, fontsize=PANEL,
            fontweight="bold", ha="left", va="top")


def panel_c(ax):
    """可用性相图（紧凑版）。"""
    with io.open(SRC, encoding="utf-8") as f:
        d = json.load(f)
    dens = sorted(int(k) for k in d["table"])
    keys = sorted({k for row in d["table"].values() for k in row},
                  key=lambda s: float(s.split("=")[1]))
    keep = [k for k in keys
            if all(d["table"][str(x)].get(k, {}).get("nonzero_fraction_mean") is not None for x in dens)]
    Z = np.array([[d["table"][str(x)].get(k, {}).get("nonzero_fraction_mean", np.nan) for x in dens]
                  for k in keep], dtype=float)
    X, Y = np.meshgrid(dens, [float(k.split("=")[1]) for k in keep])

    pcm = ax.pcolormesh(X, Y, Z, cmap="cividis", vmin=0.0, vmax=1.0, shading="nearest")
    cs = ax.contour(X, Y, Z, levels=[0.25, 0.5, 0.75], colors="white", linewidths=0.6)
    ax.clabel(cs, fmt="%.2f", fontsize=FS - 1.6, inline=True)

    # CARLA 设定带 + 实测点
    ax.add_patch(Rectangle((1200, min(Y.ravel()) - 2), 800, max(Y.ravel()) - min(Y.ravel()) + 4,
                           fill=False, hatch="////", edgecolor="0.25", lw=0.0))
    # 灰度可读：实心星 + 白色描边（仅靠颜色区分在灰度下会消失）
    ax.plot([1600], [5.0], marker="*", ms=7, mfc="0.15", mec="white", mew=0.7, zorder=6)
    ax.annotate('our loop', xy=(1600, 5.0), xytext=(8, 14), textcoords='offset points', fontsize=FS - 1.5, color='0.1', ha='left', va='center', zorder=7)

    ax.set_xlabel("flow (veh/h)", fontsize=FS, labelpad=1.5)
    ax.set_ylabel("window $W$ (s)", fontsize=FS, labelpad=1.5)
    ax.tick_params(labelsize=FS - 0.5, width=0.5, length=2, pad=1.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    cb = plt.colorbar(pcm, ax=ax, pad=0.02, fraction=0.05)
    cb.set_label("$P(\\mathrm{OTF}>0)$", fontsize=FS - 0.5)
    cb.ax.tick_params(labelsize=FS - 1.2, width=0.4, length=1.5)
    ax.set_title("Signal availability", fontsize=FS, loc="left", pad=3)
    ax.text(-0.24, 1.16, "C", transform=ax.transAxes, fontsize=PANEL,
            fontweight="bold", ha="left", va="top")


def main() -> int:
    fig = plt.figure(figsize=(4.9, 2.3), dpi=300)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.38)
    panel_a(fig.add_subplot(gs[0, 0]))
    panel_b(fig.add_subplot(gs[0, 1]))

    os.makedirs(OUT, exist_ok=True)
    for ext in ("pdf", "png"):
        p = os.path.join(OUT, "fig1_scenario." + ext)
        fig.savefig(p, bbox_inches="tight", pad_inches=0.03)
        print("  wrote %s" % p)
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
