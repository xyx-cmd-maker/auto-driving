#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fig. 2：OTF 可用性相图（SUMO 合成流）+ **TGSIM 真实点** + CARLA 实测点。

一张图回答审稿人最想问的问题：**"你这套合成流规律，在真实高速上成立吗？"**
- 背景热图/等值线 = SUMO 合成流（8 密度 × 7 窗口 × 3 seeds）
- 空心圆 = **真实 TGSIM 的 10 个 run**（每个 run 在 W=5/10/20 各有实测值）
- 星标 = 我们 CARLA 闭环的实测值（0.084）

绘图纪律（scientific-visualization）：色盲友好（cividis）、真实点用**形状+描边**冗余编码
（灰度下仍可辨）、矢量 PDF + 300 dpi、字号 ≥7 pt、直接标注不靠图例框。

用法：py -3.14 scripts/figures/fig_otf_phase_real.py
"""
import io
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SUMO = os.path.join(ROOT, "results", "p1", "otf_density_sweep_sumo_s1-2-3_fine.json")
REAL = os.path.join(ROOT, "results", "p1", "otf_real_tgsim_s1.json")
OUT = os.path.join(ROOT, "papers", "p1", "figs")

FS, TICK = 7.0, 6.5
CARLA_PHI, CARLA_FLOW, CARLA_BAND = 0.084, 1600.0, (1200.0, 2000.0)


def main() -> int:
    for p in (SUMO, REAL):
        if not os.path.exists(p):
            print("  ✗ 缺数据: %s" % p)
            return 2
    with io.open(SUMO, encoding="utf-8") as f:
        d = json.load(f)
    with io.open(REAL, encoding="utf-8") as f:
        r = json.load(f)

    dens = sorted(int(k) for k in d["table"])
    keys = sorted({k for row in d["table"].values() for k in row},
                  key=lambda s: float(s.split("=")[1]))
    keep = [k for k in keys
            if all(d["table"][str(x)].get(k, {}).get("nonzero_fraction_mean") is not None
                   and d["table"][str(x)][k].get("n_seeds", 0) >= 3 for x in dens)]
    Z = np.array([[d["table"][str(x)].get(k, {}).get("nonzero_fraction_mean", np.nan)
                   for x in dens] for k in keep], dtype=float)
    X, Y = np.meshgrid(dens, [float(k.split("=")[1]) for k in keep])

    fig = plt.figure(figsize=(6.8, 2.7), dpi=300)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1.0], wspace=0.30)
    ax = fig.add_subplot(gs[0, 0])
    cmap = plt.get_cmap("cividis")
    pcm = ax.pcolormesh(X, Y, Z, cmap=cmap, vmin=0.0, vmax=1.0, shading="nearest")
    cs = ax.contour(X, Y, Z, levels=[0.25, 0.5, 0.75], colors="white", linewidths=0.6)
    ax.clabel(cs, fmt="%.2f", fontsize=TICK - 1.2, inline=True)

    ax.add_patch(Rectangle((CARLA_BAND[0], min(Y.ravel()) - 2), CARLA_BAND[1] - CARLA_BAND[0],
                           max(Y.ravel()) - min(Y.ravel()) + 4, fill=False, hatch="////",
                           edgecolor="0.25", lw=0.0, zorder=3))
    ax.plot([CARLA_FLOW], [5.0], marker="*", ms=8, mfc="0.15", mec="white", mew=0.7, zorder=7)
    cb = fig.colorbar(pcm, ax=ax, pad=0.02, fraction=0.05)
    cb.set_label("Fraction of windows with OTF > 0", fontsize=TICK)
    cb.ax.tick_params(labelsize=TICK - 1, width=0.4, length=1.5)
    ax.set_xlabel("Traffic flow (veh/h)", fontsize=FS)
    ax.set_ylabel("OTF window length (s)", fontsize=FS)
    ax.tick_params(labelsize=TICK, width=0.5, length=2, pad=1.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("Availability map, SUMO synthetic", fontsize=FS, loc="left", pad=3)
    ax.text(-0.24, 1.13, "A", transform=ax.transAxes, fontsize=FS + 1.5, fontweight="bold",
            ha="left", va="top")

    # ---- 面板 B：三窗口下的三组对比（真实 vs 合成 vs CARLA）
    ax2 = fig.add_subplot(gs[0, 1])
    wins = ["W=5", "W=10", "W=20"]
    xs = np.arange(len(wins))
    sumo_vals, real_vals, real_lo, real_hi = [], [], [], []
    for w in wins:
        cols = [d["table"][str(x)][w]["nonzero_fraction_mean"] for x in (1800, 2400)]
        sumo_vals.append(float(np.mean(cols)))
        a = r["aggregate"].get(w) or r["aggregate"].get("W=%.0f" % float(w.split("=")[1]))
        a = a or {}
        real_vals.append(a.get("nonzero_fraction_mean", np.nan))
        rng = a.get("range") or [np.nan, np.nan]
        real_lo.append(rng[0])
        real_hi.append(rng[1])

    carla = {0: 0.084, 1: 0.167}          # W=5 / W=10 实测
    ax2.plot(xs, sumo_vals, marker="o", ms=3.5, lw=1.0, color="#0072B2", label="SUMO (1800-2400 veh/h)")
    ax2.errorbar(xs, real_vals, yerr=[np.array(real_vals) - np.array(real_lo),
                                      np.array(real_hi) - np.array(real_vals)],
                 fmt="s", ms=3.5, lw=0, elinewidth=0.8, capsize=2, color="#D55E00",
                 label="TGSIM, real (mean, range)")
    ax2.plot(list(carla.keys()), list(carla.values()), marker="*", ms=8, ls="",
             mfc="0.15", mec="white", mew=0.7, label="CARLA, closed loop")

    ax2.set_xticks(xs)
    ax2.set_xticklabels(["5", "10", "20"])
    ax2.set_xlabel("OTF window length (s)", fontsize=FS)
    ax2.set_ylabel("Fraction of windows with OTF > 0", fontsize=FS)
    ax2.set_ylim(0, 1.0)
    ax2.tick_params(labelsize=TICK, width=0.5, length=2, pad=1.5)
    for s in ("top", "right"):
        ax2.spines[s].set_visible(False)
    ax2.grid(axis="y", color="0.92", lw=0.5, zorder=0)
    ax2.legend(fontsize=TICK - 0.8, frameon=False, loc="upper left",
               handletextpad=0.4, borderpad=0.1, labelspacing=0.25)
    ax2.set_title("Real vs synthetic vs closed loop", fontsize=FS, loc="left", pad=3)
    ax2.text(-0.28, 1.13, "B", transform=ax2.transAxes, fontsize=FS + 1.5, fontweight="bold",
             ha="left", va="top")
    ax2.text(0.5, 0.06, "gap at 5 s: %.2f vs %.2f vs %.3f" % (sumo_vals[0], real_vals[0], carla[0]),
             transform=ax2.transAxes, fontsize=TICK - 0.6, ha="center", color="0.25")

    os.makedirs(OUT, exist_ok=True)
    for ext in ("pdf", "png"):
        p = os.path.join(OUT, "fig2_availability_real." + ext)
        fig.savefig(p, bbox_inches="tight", pad_inches=0.02)
        print("  wrote %s" % p)
    plt.close(fig)
    print("  SUMO@5s=%.3f  TGSIM@5s=%.3f  CARLA@5s=%.3f" % (sumo_vals[0], real_vals[0], carla[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
