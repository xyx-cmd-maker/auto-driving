#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""补证：60 s 稀疏 SUMO 场景里，整个车队完成了几次换道、其中几次跨越 ego 车道？

对应论文 §5.3 的一句：
    "over a 60 s probe the whole fleet completed two lane changes, none of them across the ego lane"

该句支撑"必须脚本注入 OTF 事件"这一关键设计决定，但此前仓库里**没有任何产物**（Round 12 标为 U）。
本脚本复用 `scripts/sumo/otf_sparsity_sumo.py` 的场景构造与 FCD 解析，跑一次 60 s 探针并把结果落盘：
    results/p1/sumo_lanecount_probe_s1.json

用法：py -3.12 scripts/probe_sumo_lanecount.py [--seed 0] [--veh-per-hour 960] [--minutes 1]
"""
import argparse
import importlib.util
import io
import json
import os
import sys
import tempfile

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "results", "p1", "sumo_lanecount_probe_s1.json")

spec = importlib.util.spec_from_file_location(
    "sumo_mod", os.path.join(ROOT, "scripts", "sumo", "otf_sparsity_sumo.py"))
sm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sm)  # noqa: E402


def count_changes(tracks, ego_lane_idx):
    """统计换道次数与跨 ego 车道的换道次数。"""
    total, across, per_veh = 0, 0, {}
    for vid, tr in tracks.items():
        n = 0
        for i in range(1, len(tr)):
            l0 = sm.lane_index(tr[i - 1][1])
            l1 = sm.lane_index(tr[i][1])
            if l0 is None or l1 is None or l0 == l1:
                continue
            n += 1
            # 跨越 ego 车道：一端是 ego lane，另一端是相邻车道
            if l0 == ego_lane_idx and abs(l1 - ego_lane_idx) == 1:
                across += 1
            elif l1 == ego_lane_idx and abs(l0 - ego_lane_idx) == 1:
                across += 1
        if n:
            per_veh[vid] = n
        total += n
    return total, across, per_veh


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--veh-per-hour", type=int, default=960,
                    help="960 ≈ 60 s 内到达 16 辆车，对应 CARLA 主实验的稀疏度")
    ap.add_argument("--minutes", type=float, default=1.0)
    ap.add_argument("--lanes", type=int, default=3)
    ap.add_argument("--length", type=float, default=1200.0)
    args = ap.parse_args()

    if not os.path.exists(sm.SUMO_BIN):
        print("  ✗ 找不到 SUMO：%s" % sm.SUMO_BIN)
        return 2

    d = tempfile.mkdtemp(prefix="sumo_probe_")
    cfg = sm.write_scenario(d, args.seed, args.minutes, args.lanes, args.length,
                            33.3, args.veh_per_hour)
    sm.build_net(d)
    sm.run_sumo(cfg, d)
    tracks = sm.parse_fcd(os.path.join(d, "fcd.xml"))
    ego_lane = args.lanes // 2          # 中间车道当 ego 车道
    total, across, per_veh = count_changes(tracks, ego_lane)

    rec = dict(experiment="sumo_lanecount_probe", seed=args.seed,
               veh_per_hour=args.veh_per_hour, minutes=args.minutes,
               lanes=args.lanes, length_m=args.length, ego_lane_index=ego_lane,
               vehicles=len(tracks), lane_changes_total=total,
               lane_changes_across_ego=across, per_vehicle=per_veh,
               note="60 s 稀疏探针：复现论文 §5.3 的『整队仅发生两次换道』观察")
    with io.open(OUT, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    print("  车辆 %d ｜ 换道总数 %d ｜ 跨越 ego(中间) 车道 %d" % (len(tracks), total, across))
    print("  已写 %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
