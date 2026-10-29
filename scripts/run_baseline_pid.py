#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""跑 PID 跟驰基线（外部参照控制器）——需要 CARLA 运行中。

用途：给 A1 的复合代价一个**外部标尺**。本仓库此前没有任何基线（Red-Team D1）。
本脚本用与 A1 完全相同的环境、场景、种子、指标与代价权重，只把控制器换成 `GapPID`。

用法：
    # 0) 不连 CARLA，只打印计划（默认）
    py -3.12 scripts/run_baseline_pid.py

    # 1) 真正跑 20 局（需先启动 CARLA；约 20–40 min）
    py -3.12 scripts/run_baseline_pid.py --run

    # 2) 只有 CARLA 在别处时
    py -3.12 scripts/run_baseline_pid.py --run --host 127.0.0.1 --port 2000

产物：results/p1/baseline_pid_s1.json
  { "experiment": "baseline_pid", "params": {...}, "cases": [ {scenario, seed, cost,
    metrics, guard, wall_s}, ... ], "aggregate": {cost_mean, cost_sd, n} }

诚实边界（会写进产物）：
  · 参数**未调优**（`DEFAULT`）；若要做"公平基线"，须另做扫描并同时报告扫描过程。
  · 它不含换道、不含 OTF，因此**不能**用来论证 OTF 的优劣，只回答"代价量级是否合理"。
  · 与 CfC 臂的预算**不等**（PID 是确定性单策略，无 12 候选搜索）；报告时必须写明。
"""
import argparse
import io
import json
import os
import sys
import time

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
_HERE = os.path.join(ROOT, "src", "ctrl")
for _p in (_HERE, os.path.join(ROOT, "src", "envs"), os.path.join(ROOT, "src", "eval"),
           os.path.join(ROOT, "src", "otf")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from pid_baseline import GapPID, DEFAULT      # noqa: E402
from metrics import Trace, summarize          # noqa: E402

OUT = os.path.join(ROOT, "results", "p1", "baseline_pid_s1.json")
SCENARIOS = ["none", "cutin", "lead-brake", "lead-exit"]
SEEDS = [0, 1, 2, 3, 4]
EPISODE_S = 60.0
TRAFFIC = 16


def cost_from_metrics(m):
    """与 `src/ctrl/train_cfc.py: cost_from_metrics` **同一权重**（此处内联以便独立运行）。"""
    c = 0.0
    c += 1.0 * (m["following_rmse_m"] if m["following_rmse_m"] is not None else 10.0) / 10.0
    c += 1.0 * (m["accel_sq_integral_mps3"] or 0.0) / 50.0
    c += 0.5 * (m["jerk_peak_mps3"] or 0.0) / 50.0
    c += 0.5 * (m["lane_center_dev_m"] or 0.0) / 0.5
    c += 10.0 * (m["collision_count"] or 0)
    return float(c)


def roll_pid(env, pid, scenario, seed):
    st = env.reset(scenario=scenario, seed=seed)
    tr = Trace(); tr.push(st)
    p0 = env.ego.get_transform().location
    n = int(EPISODE_S / (env.dt * env.ctrl_every))
    for _ in range(n):
        v = pid.target_speed(
            gap_m=(st.lead_gap_m if st.lead_gap_m is not None else 200.0),
            rel_speed_mps=(st.rel_speed_mps or 0.0),
            v_ego_mps=st.ego_speed_mps)
        st = env.step_speed(target_speed_mps=v)
        tr.push(st)
        if st.meta.get("done"):
            break
    p1 = env.ego.get_transform().location
    travelled = ((p1.x - p0.x) ** 2 + (p1.y - p0.y) ** 2) ** 0.5
    m = summarize(tr)
    return m, dict(travelled_m=round(travelled, 3), n_frames=len(tr),
                   valid=bool(travelled > 20.0))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="真正连接 CARLA 跑仿真")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=2000)
    args = ap.parse_args()

    pid = GapPID()
    plan = dict(experiment="baseline_pid", controller="GapPID", params=DEFAULT,
                scenarios=SCENARIOS, seeds=SEEDS, episode_s=EPISODE_S, traffic=TRAFFIC,
                episodes=len(SCENARIOS) * len(SEEDS))
    print("  PID 基线计划")
    print("    控制器 = GapPID(kp=%.2f, kd=%.2f, h=%.1f s, s0=%.1f m, vmax=%.1f m/s)"
          % (pid.kp, pid.kd, pid.headway_s, pid.s0_m, pid.v_max_mps))
    print("    局数 = %d（%d 场景 × %d 种子）｜每局 %.0f s ｜交通 %d 辆"
          % (plan["episodes"], len(SCENARIOS), len(SEEDS), EPISODE_S, TRAFFIC))
    print("    说明：PID 是确定性单策略，无 12 候选搜索 → 与 CfC 臂的**预算不等**，报告须写明。")

    if not args.run:
        print("\n  （dry-run）未连接 CARLA。加 --run 才会真正仿真。")
        return 0

    try:
        from carla_town04 import Town04Env  # noqa: E402
    except Exception as e:
        print("  ✗ 无法导入环境：%s" % e)
        return 2

    env = Town04Env(host=args.host, port=args.port, n_traffic=TRAFFIC,
                    max_episode_s=EPISODE_S + 10.0, verbose=False)
    cases = []
    try:
        for sc in SCENARIOS:
            for sd in SEEDS:
                t0 = time.perf_counter()
                m, guard = roll_pid(env, pid, sc, sd)
                rec = dict(scenario=sc, seed=sd, cost=cost_from_metrics(m),
                           metrics=m, guard=guard, wall_s=round(time.perf_counter() - t0, 1))
                cases.append(rec)
                print("    %-11s s%d  cost=%.3f  travelled=%.1f m"
                      % (sc, sd, rec["cost"], guard["travelled_m"]))
    finally:
        try:
            env.close()
        except Exception:
            pass

    costs = [c["cost"] for c in cases if c["guard"]["valid"]]
    agg = dict(n_valid=len(costs),
               cost_mean=(sum(costs) / len(costs)) if costs else None,
               cost_sd=(__import__("statistics").stdev(costs) if len(costs) > 1 else None))
    plan.update(cases=cases, aggregate=agg,
                note="参数未调优；PID 单策略与 CfC 12 候选预算不等；不含 OTF/换道")
    with io.open(OUT, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    print("\n  有效局 %d/%d ｜ cost 均值 %.3f ｜ SD %s"
          % (agg["n_valid"], len(cases), agg["cost_mean"] or -1,
             ("%.3f" % agg["cost_sd"]) if agg["cost_sd"] else "n/a"))
    print("  已写 %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
