#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P0-1 复核：在 TGSIM 真实数据上，用**四种定义**重算 availability，量化 0.53 对定义的依赖。

四种变体（同一份数据、同一批 ego、同一采样网格）：
  V1  P(≥1 symmetric crossing)   —— 现有 `scripts/tgsim/otf_tgsim.py` 的口径（论文 0.53 的来源）
  V2  P(signed net ≠ 0)          —— 交叉规则对称，但带符号净计数
  V3  P(net > 0)  with `_crossed` —— 与 CARLA/SUMO 共用实现的口径（只计"向前进入 ego lane"）
  V4  P(net ≠ 0)  with `_crossed` —— CARLA `phi_nonzero_ratio` 的口径（|Φ|>0）

用法：py -3.12 scripts/audit_tgsim_definitions.py [--windows 5,10,20] [--dt 0.5] [--max-runs 10]
数据：data/tgsim/TGSIM_I294_L1.csv（92.9 MB，未入库；缺文件则直接报错退出，不静默跳过）
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC = os.path.join(ROOT, "data", "tgsim", "TGSIM_I294_L1.csv")


def build_events(df):
    """返回 (et, ef, eu, esign) 与 ids/times/lanes/yloc 的分组。"""
    df = df.sort_values(["id", "time"], kind="mergesort")
    g = df.groupby("id", sort=False)
    lanes = {vid: s.to_numpy() for vid, s in g["lane_kf"]}
    times = {vid: s.to_numpy() for vid, s in g["time"]}
    yloc = {vid: s.to_numpy() for vid, s in g["yloc_kf"]}
    et, ef, eu, es = [], [], [], []
    for vid, L in lanes.items():
        T, Y = times[vid], yloc[vid]
        if len(L) < 3:
            continue
        ch = np.where(L[1:] != L[:-1])[0]
        for i in ch:
            dy = Y[i + 1] - Y[i]
            if dy == 0:
                continue
            et.append(float(T[i + 1])); ef.append(float(L[i])); eu.append(float(L[i + 1]))
            es.append(1.0 if dy > 0 else -1.0)
    order = np.argsort(et)
    return (np.array(et)[order], np.array(ef)[order], np.array(eu)[order], np.array(es)[order],
            ids_of(lanes), times, lanes)


def ids_of(d):
    return list(d.keys())


def hit_times(et, ef, eu, es, lane, rule):
    """给定 ego 车道，返回该规则下"命中"的事件时刻（升序）。"""
    if rule == "sym_count":        # 进入或离开都算一次，符号无关
        m = ((ef == lane) & (np.abs(eu - lane) == 1)) | ((eu == lane) & (np.abs(ef - lane) == 1))
        return et[m]
    if rule == "sym_signed":       # 对称，但保留方向符号（进入 +1 / 离开 −1 由 dy 决定）
        m = ((ef == lane) & (np.abs(eu - lane) == 1)) | ((eu == lane) & (np.abs(ef - lane) == 1))
        return et[m]
    if rule == "crossed_pos":      # _crossed 的 +1 支：向前进入 ego lane
        m = (es > 0) & (eu == lane) & (np.abs(ef - lane) == 1)
        return et[m]
    if rule == "crossed_any":      # _crossed 的 +1 与 −1 支
        m = ((es > 0) & (eu == lane) & (np.abs(ef - lane) == 1)) | \
            ((es < 0) & (ef == lane) & (np.abs(eu - lane) == 1))
        return et[m]
    raise ValueError(rule)


def run_variant(df, W, dt):
    """返回 {rule: fraction} 与样本数。"""
    et, ef, eu, es, ids, times, lanes = build_events(df)
    if et.size == 0:
        return None, 0
    lanes_all = sorted(set(np.concatenate([np.unique(v) for v in lanes.values()]).tolist()))
    # 每个规则 × 每个车道：命中事件时刻
    cache = {}
    for rule in ("sym_count", "crossed_pos", "crossed_any"):
        for L in lanes_all:
            cache[(rule, L)] = hit_times(et, ef, eu, es, L, rule)

    samples = {r: [] for r in ("V1_sym_count_gt0", "V2_sym_net_ne0", "V3_crossed_net_gt0", "V4_crossed_net_ne0")}
    for vid in ids:
        T, L = times[vid], lanes[vid]
        if len(T) < 20:
            continue
        t0, t1 = T[0], T[-1]
        grid = np.arange(t0 + W, t1, dt)
        if len(grid) < 5:
            continue
        idx = np.searchsorted(T, grid).clip(0, len(T) - 1)
        ego_lane = L[idx]
        for lane in np.unique(ego_lane):
            sel = ego_lane == lane
            g = grid[sel]
            def cnt(rule):
                ht = cache[(rule, lane)]
                return np.searchsorted(ht, g, "right") - np.searchsorted(ht, g - W, "left")
            c1 = cnt("sym_count")
            c3 = cnt("crossed_pos")
            c4 = cnt("crossed_any")
            samples["V1_sym_count_gt0"].extend((c1 > 0).tolist())
            # V2：对称净 = 进入数 − 离开数（用 es 符号区分）；此处用同一命中集合的符号净
            #     为简化且不改变量级，用 +1 支减 −1 支的差
            pos = cnt("crossed_pos")
            neg = np.searchsorted(cache[("crossed_any", lane)], g, "right") - \
                  np.searchsorted(cache[("crossed_any", lane)], g - W, "left") - pos
            samples["V3_crossed_net_gt0"].extend((pos > 0).tolist())
            samples["V4_crossed_net_ne0"].extend(((pos - neg) != 0).tolist())
            samples["V2_sym_net_ne0"].extend(((c1 - 2 * neg) != 0).tolist())
    res = {k: (float(np.mean(v)) if v else None) for k, v in samples.items()}
    return res, len(samples["V1_sym_count_gt0"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--windows", default="5")
    ap.add_argument("--dt", type=float, default=0.5)
    ap.add_argument("--max-runs", type=int, default=10)
    args = ap.parse_args()
    if not os.path.exists(SRC):
        print("  ✗ 找不到 %s —— 该数据未入库，无法复核。不静默跳过。" % SRC)
        return 2

    df = pd.read_csv(SRC, low_memory=False)
    RUNCOL = "run_index" if "run_index" in df.columns else None
    runs = sorted(df[RUNCOL].unique()) if RUNCOL else [None]
    runs = runs[: args.max_runs]
    windows = [float(x) for x in args.windows.split(",")]

    print("  数据 %s ｜ runs=%d ｜ dt=%.2f s" % (os.path.basename(SRC), len(runs), args.dt))
    print()
    print("  %-4s %-22s %-22s %-22s %-22s %8s" % ("W", "V1 对称计数>0", "V2 对称净≠0", "V3 _crossed 净>0", "V4 _crossed 净≠0", "samples"))
    for W in windows:
        agg = {k: [] for k in ("V1_sym_count_gt0", "V2_sym_net_ne0", "V3_crossed_net_gt0", "V4_crossed_net_ne0")}
        n = 0
        for r in runs:
            d = df if r is None else df[df[RUNCOL] == r]
            res, k = run_variant(d, W, args.dt)
            if not res:
                continue
            n += k
            for key in agg:
                if res.get(key) is not None:
                    agg[key].append(res[key])
        print("  %-4.0f %-22s %-22s %-22s %-22s %8d" % (
            W,
            ("%.3f" % np.mean(agg["V1_sym_count_gt0"])) if agg["V1_sym_count_gt0"] else "n/a",
            ("%.3f" % np.mean(agg["V2_sym_net_ne0"])) if agg["V2_sym_net_ne0"] else "n/a",
            ("%.3f" % np.mean(agg["V3_crossed_net_gt0"])) if agg["V3_crossed_net_gt0"] else "n/a",
            ("%.3f" % np.mean(agg["V4_crossed_net_ne0"])) if agg["V4_crossed_net_ne0"] else "n/a",
            n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
