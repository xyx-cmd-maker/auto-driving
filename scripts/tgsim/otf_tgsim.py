#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""在 **TGSIM 真实轨迹**上计算 OTF 可用性，并与 SUMO 合成流的相图对比。

定义与控制器**完全相同**（`src/otf/otf_core.py` 的 `_crossed`）：
只有当某车跨越 ego 所在车道时计数，方向由纵向位移符号决定。

为什么这一步重要
----------------
主实验与相图都来自**我们自己造的仿真**。TGSIM 是 FHWA 的公开真实轨迹（美国公有领域），
含 ACC 测试车与人工车混行。在同一套定义下算它的 OTF 可用性，可以直接回答：
**"SUMO 上那条规律在真实高速上成立吗？"** 这是把"无真实数据"从 Limitations 里去掉的关键一步。

数据：data/tgsim/TGSIM_I294_L1.csv（92.9 MB，1 024 281 行，827 车，10 个 run，dt=0.1 s）
用法：py -3.14 scripts/tgsim/otf_tgsim.py [--windows 5,10,20] [--dt 0.5]
产出：results/p1/otf_real_tgsim_s1.json
"""
import argparse
import io
import json
import os
import sys

import numpy as np
import pandas as pd

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(ROOT, "data", "tgsim", "TGSIM_I294_L1.csv")
OUT = os.path.join(ROOT, "results", "p1", "otf_real_tgsim_s1.json")


def run_otf(df: pd.DataFrame, windows, dt: float):
    """对单个 run 计算 OTF 可用性。

    返回 {W: {"samples","nonzero_fraction","mean","p95","max"}} 与每个 ego 的事件数。
    """
    df = df.sort_values(["id", "time"], kind="mergesort")
    g = df.groupby("id", sort=False)

    lanes = g["lane_kf"].apply(lambda s: s.to_numpy())
    times = g["time"].apply(lambda s: s.to_numpy())
    ypos = g["yloc_kf"].apply(lambda s: s.to_numpy())
    ids = lanes.index.to_numpy()

    # 1) 换道事件：t, from_lane, to_lane, dy(纵向位移符号)
    events = []           # (t, from_lane, to_lane, sign)
    for vid in ids:
        L = lanes[vid]
        T = times[vid]
        Y = ypos[vid]
        if len(L) < 3:
            continue
        ch = np.where(L[1:] != L[:-1])[0]      # L[i] -> L[i+1]
        for i in ch:
            dy = Y[i + 1] - Y[i]
            if dy == 0:
                continue
            events.append((float(T[i + 1]), float(L[i]), float(L[i + 1]), 1.0 if dy > 0 else -1.0))
    if not events:
        return {w: {"samples": 0} for w in windows}, 0
    events.sort()
    et = np.array([e[0] for e in events])
    ef = np.array([e[1] for e in events])
    eu = np.array([e[2] for e in events])

    # 2) 每个 ego：在其每一采样时刻，数窗口内"跨越 ego 车道"的事件数
    out = {w: [] for w in windows}
    for vid in ids:
        T = times[vid]
        L = lanes[vid]
        if len(T) < 20:
            continue
        t0, t1 = T[0], T[-1]
        grid = np.arange(t0 + max(windows), t1, dt)
        if len(grid) < 5:
            continue
        # ego 在 grid 时刻的车道（最近邻）
        idx = np.searchsorted(T, grid).clip(0, len(T) - 1)
        ego_lane = L[idx]
        for w in windows:
            lo = np.searchsorted(et, grid - w, side="left")
            hi = np.searchsorted(et, grid, side="left")
            cnt = np.zeros(len(grid), dtype=np.int32)
            # 事件落进窗口则检查是否跨越该时刻 ego 车道
            for k in range(len(grid)):
                if hi[k] <= lo[k]:
                    continue
                sel = slice(lo[k], hi[k])
                el = ego_lane[k]
                hit = ((ef[sel] == el) & (np.abs(eu[sel] - el) == 1)) | \
                      ((eu[sel] == el) & (np.abs(ef[sel] - el) == 1))
                cnt[k] = int(hit.sum())
            out[w].extend(cnt.tolist())
    res = {}
    for w in windows:
        v = np.array(out[w], dtype=float)
        if v.size == 0:
            res["W=%.0f" % w] = {"samples": 0}
            continue
        vs = np.sort(v)
        res["W=%.0f" % w] = {
            "samples": int(v.size),
            "nonzero_fraction": round(float((v > 0).mean()), 4),
            "mean": round(float(v.mean()), 4),
            "p95": float(vs[int(0.95 * (len(vs) - 1))]),
            "max": float(vs[-1]),
        }
    return res, len(events)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--windows", default="5,10,20")
    ap.add_argument("--dt", type=float, default=0.5)
    args = ap.parse_args()
    windows = [float(x) for x in args.windows.split(",")]

    if not os.path.exists(SRC):
        print("  ✗ 缺数据: %s" % SRC)
        return 2

    df = pd.read_csv(SRC, usecols=["id", "time", "yloc_kf", "lane_kf", "acc", "run_index"],
                     low_memory=False)
    df["acc_flag"] = df["acc"].astype(str).str.strip().str.lower().eq("yes")

    out = {"experiment": "otf_real_tgsim", "source": "data/tgsim/TGSIM_I294_L1.csv",
           "note": ("真实轨迹（FHWA TGSIM, 美国公有领域）。OTF 定义与 src/otf/otf_core.py 完全相同；"
                    "仅计跨越 ego 车道的事件。"),
           "rows": int(len(df)), "runs": {}}

    for run, g in df.groupby("run_index"):
        dur = float(g["time"].max() - g["time"].min())
        nveh = int(g["id"].nunique())
        acc_v = int(g[g["acc_flag"]]["id"].nunique())
        flow = 3600.0 * nveh / dur if dur > 0 else 0.0
        res, nev = run_otf(g, windows, args.dt)
        out["runs"]["run_%s" % run] = {
            "vehicles": nveh, "acc_vehicles": acc_v, "duration_s": round(dur, 1),
            "flow_veh_per_h_est": round(flow, 1), "lane_change_events": nev,
            "lanes": sorted(float(x) for x in g["lane_kf"].dropna().unique()),
            "availability": res,
        }
        a5 = res.get("W=5", {}).get("nonzero_fraction")
        print("  run %-3s 车辆 %3d (ACC %2d) ｜ %5.0f s ｜ 估算流量 %5.0f veh/h ｜ 换道 %4d ｜ W=5 非零 %s"
              % (run, nveh, acc_v, dur, flow, nev,
                 ("%.3f" % a5) if a5 is not None else "n/a"))

    # 汇总（按 W）
    print()
    agg = {}
    for w in windows:
        key = "W=%.0f" % w
        vals = [r["availability"][key]["nonzero_fraction"] for r in out["runs"].values()
                if r["availability"].get(key, {}).get("samples")]
        samples = sum(r["availability"][key]["samples"] for r in out["runs"].values()
                      if r["availability"].get(key, {}).get("samples"))
        if vals:
            agg[key] = {"nonzero_fraction_mean": round(float(np.mean(vals)), 4),
                        "range": [round(min(vals), 4), round(max(vals), 4)],
                        "samples_total": int(samples), "n_runs": len(vals)}
            print("  %-6s 非零比例 均值 %.3f ｜ 范围 [%.3f, %.3f] ｜ 样本 %d ｜ runs %d"
                  % (key, agg[key]["nonzero_fraction_mean"], agg[key]["range"][0],
                     agg[key]["range"][1], samples, len(vals)))
    out["aggregate"] = agg

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = OUT + ".tmp"
    with io.open(tmp, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    os.replace(tmp, OUT)
    print("\n  已写 %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
