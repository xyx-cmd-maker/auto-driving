#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fig: OTF 可用性相图（密度 × 窗口），并标出我们 CARLA 闭环设定的位置。

数据：results/p1/otf_density_sweep_sumo_s1-2-3_fine.json（SUMO，3 seeds × 8 密度 × 7 窗口）
标注：
  · 竖带 = 我们 CARLA 闭环设定的**等效流量估计**（16 辆混行车 / 约 420 m / 3 车道，标注为 estimate）
  · 空心星 = CARLA 里**实测**的 Φ_OTF>0 比例（0.084，W = 5 s）
两者不一致本身就是发现：CARLA 的 Traffic Manager 换道率远低于 SUMO 的 LC2013，
所以我们必须注入脚本化 cut-in 才能得到可用信号。

绘图纪律（scientific-visualization）：单栏宽、色盲友好、等值线 + 色标、
直接标注、无 chartjunk、矢量 PDF + 300 dpi PNG。

用法（本机仅 py3.14 有 matplotlib）：
  py -3.14 scripts/figures/fig_otf_phase.py
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

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(ROOT, "results", "p1", "otf_density_sweep_sumo_s1-2-3_fine.json")
OUT = os.path.join(ROOT, "papers", "p1", "figs")

CARLA_PHI = 0.084          # 来自 runs/p1/cases 的 phi_nonzero_ratio 实测（W = 5 s）
CARLA_FLOW = 1600.0        # 等效流量估计（16 辆 / 0.42 km / 3 车道 × 12 m/s）
CARLA_BAND = (1200.0, 2000.0)


def main() -> int:
    if not os.path.exists(SRC):
        print("  ✗ 缺数据: %s" % SRC)
        return 2
    with io.open(SRC, encoding="utf-8") as f:
        d = json.load(f)

    dens = sorted(int(k) for k in d["table"])
    # 只保留所有密度都有值的窗口，避免大片 NaN
    win_keys = sorted({k for row in d["table"].values() for k in row},
                      key=lambda s: float(s.split("=")[1]))
    wins = [float(k.split("=")[1]) for k in win_keys]
    keep = [k for k in win_keys
            if all(d["table"][str(x)].get(k, {}).get("nonzero_fraction_mean") is not None
                   and d["table"][str(x)][k].get("n_seeds", 0) >= 3 for x in dens)]

    Z = np.full((len(keep), len(dens)), np.nan)
    for i, k in enumerate(keep):
        for j, x in enumerate(dens):
            v = d["table"][str(x)].get(k, {}).get("nonzero_fraction_mean")
            if v is not None:
                Z[i, j] = v

    fig, ax = plt.subplots(figsize=(3.5, 2.9), dpi=300)
    X, Y = np.meshgrid(dens, [float(k.split("=")[1]) for k in keep])
    cmap = plt.get_cmap("cividis")          # 色盲友好且打印友好
    pcm = ax.pcolormesh(X, Y, Z, cmap=cmap, vmin=0.0, vmax=1.0, shading="nearest")
    cs = ax.contour(X, Y, Z, levels=[0.25, 0.5, 0.75], colors="white", linewidths=0.7)
    ax.clabel(cs, fmt="%.2f", fontsize=6, inline=True)

    # CARLA 等效流量带（估计）
    ax.add_patch(Rectangle((CARLA_BAND[0], min(Y.ravel()) - 2),
                           CARLA_BAND[1] - CARLA_BAND[0], max(Y.ravel()) - min(Y.ravel()) + 4,
                           fill=False, hatch="////", edgecolor="0.25", lw=0.0, alpha=0.9, zorder=3))
    ax.axvline(CARLA_FLOW, color="white", lw=0.8, ls=(0, (2, 2)), zorder=4)

    # CARLA 实测点（W = 5 s）——数值留给图注，图内只留一行标记，避免压住等值线
    ax.plot([CARLA_FLOW], [5.0], marker="*", ms=9, mfc="none", mec="#D55E00",
            mew=1.2, zorder=6)
    ax.text(0.975, 0.965, "$\\star$ CARLA (measured, W = 5 s)",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=6, color="#D55E00", zorder=7)

    cb = fig.colorbar(pcm, ax=ax, pad=0.02, fraction=0.05)
    cb.set_label("Fraction of windows with OTF > 0", fontsize=7)
    cb.ax.tick_params(labelsize=6, width=0.5, length=2)

    ax.set_xlabel("Traffic flow (veh/h)", fontsize=8)
    ax.set_ylabel("OTF window length (s)", fontsize=8)
    ax.tick_params(labelsize=7, width=0.6, length=2.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    # 直接在图上标注竖带（不用图例）
    ax.text(CARLA_BAND[0] - 60, max(Y.ravel()) + 1.5, "CARLA setting (est.)",
            fontsize=6, color="0.25", ha="right", va="bottom", rotation=90)

    os.makedirs(OUT, exist_ok=True)
    for ext in ("pdf", "png"):
        p = os.path.join(OUT, "fig_otf_phase." + ext)
        fig.savefig(p, bbox_inches="tight", pad_inches=0.02)
        print("  wrote %s" % p)
    plt.close(fig)

    csv = os.path.join(OUT, "fig_otf_phase.csv")
    with io.open(csv, "w", encoding="utf-8") as f:
        f.write("flow_veh_per_hour," + ",".join("W=%g" % float(k.split("=")[1]) for k in keep) + "\n")
        for j, x in enumerate(dens):
            f.write(str(x) + "," + ",".join(
                "" if np.isnan(Z[i, j]) else "%.4f" % Z[i, j] for i in range(len(keep))) + "\n")
    print("  wrote %s" % csv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
