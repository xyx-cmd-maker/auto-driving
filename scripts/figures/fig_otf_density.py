#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fig: OTF 的可用性随交通密度的变化（非零窗口比例 vs 密度，按窗口长度分层）。

数据来源：results/p1/otf_density_sweep_sumo_s1-2-3.json（SUMO，3 seeds × 5 密度）
绘图纪律（scientific-visualization）：色盲友好、直接标注不靠图例、无 chartjunk、
矢量 PDF + 300 dpi PNG、坐标轴从 0 开始、网格极淡。

用法（注意：本机只有 py3.14 装了 matplotlib）：
  py -3.14 scripts/figures/fig_otf_density.py
"""
import io
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(ROOT, "results", "p1", "otf_density_sweep_sumo_s1-2-3.json")
OUT = os.path.join(ROOT, "papers", "p1", "figs")

# Okabe–Ito 色盲友好三色
COLORS = {"W=5": "#0072B2", "W=10": "#D55E00", "W=20": "#009E73"}


def main() -> int:
    if not os.path.exists(SRC):
        print("  ✗ 缺数据: %s（先跑 scripts/sumo/otf_density_sweep.py）" % SRC)
        return 2
    with io.open(SRC, encoding="utf-8") as f:
        d = json.load(f)

    dens = sorted(int(k) for k in d["table"])
    windows = ["W=5", "W=10", "W=20"]

    fig, ax = plt.subplots(figsize=(3.5, 2.6), dpi=300)   # 单栏宽（IEEE 约 88 mm）
    for w in windows:
        ys = [d["table"][str(x)].get(w, {}).get("nonzero_fraction_mean") for x in dens]
        pairs = [(x, y) for x, y in zip(dens, ys) if y is not None]
        if not pairs:
            continue
        xs, yy = zip(*pairs)
        ax.plot(xs, yy, marker="o", ms=3.2, lw=1.4, color=COLORS[w], label=w.replace("W=", "W = ") + " s",
                clip_on=False, zorder=3)
        # 直接标注在末端，省掉图例框
        ax.annotate(w.replace("W=", "W = ") + " s", xy=(xs[-1], yy[-1]),
                    xytext=(4, 0), textcoords="offset points",
                    va="center", ha="left", fontsize=7, color=COLORS[w])

    ax.set_xlabel("Traffic density (veh/h)", fontsize=8)
    ax.set_ylabel("Fraction of windows with OTF > 0", fontsize=8)
    ax.set_xlim(min(dens) - 200, max(dens) + 900)   # 右侧留白给直接标注
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.tick_params(labelsize=7, width=0.6, length=2.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(0.6)
    ax.grid(axis="y", color="0.9", lw=0.5, zorder=0)

    os.makedirs(OUT, exist_ok=True)
    for ext in ("pdf", "png"):
        p = os.path.join(OUT, "fig_otf_density." + ext)
        fig.savefig(p, bbox_inches="tight", pad_inches=0.02)
        print("  已写 %s" % p)
    plt.close(fig)

    # 同时导出可复现的 CSV（审稿人要数据时直接给）
    csv = os.path.join(OUT, "fig_otf_density.csv")
    with io.open(csv, "w", encoding="utf-8") as f:
        f.write("density_veh_per_hour," + ",".join(w for w in windows) + "\n")
        for x in dens:
            row = [str(x)]
            for w in windows:
                v = d["table"][str(x)].get(w, {}).get("nonzero_fraction_mean")
                row.append("" if v is None else "%.4f" % v)
            f.write(",".join(row) + "\n")
    print("  已写 %s" % csv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
