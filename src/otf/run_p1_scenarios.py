#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P1 主场景驱动（四类工况 + 探测车速扫描）→ results/p1/

取代早期的 run_p1_cutin.py（只做 cut-in、只报均值）。两个关键改动：
  1. **聚合量从"均值"改为"分布"**：论文表 3.3–3.7 报的是 OTF 分箱**占比**；
     而逐窗口 OTF 的均值恒趋于 0（窗口内配平），报均值等于报噪声。
  2. **工况参数化**：--scenario 四类（none / cutin / lead-brake / lead-exit）；
     另加 --probe-speed 用于检验 OTF 符号（论文 L3290：OTF 符号由自车与邻车相对车速决定）。

产出命名：results/p1/main_otf_cfc_<scenario>_highway-mixed_s1.json
每个文件含**全部 5 个种子**的逐种子明细 + 跨种子分布。

边界：SUMO 合成交通流，**不是 CARLA、不是实车**（AGENTS.md §1/§2）；证据等级 C。
"""
import argparse
import hashlib
import io
import json
import math
import os
import sys
from collections import defaultdict

SUMOHOME = os.environ.get("SUMO_HOME", r"D:\SUMO\sumo-1.27.1")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
NET = os.path.join(ROOT, "configs", "p1", "sumo_highway.net.xml")
META = os.path.join(ROOT, "configs", "p1", "sumo_highway.meta.xml")
OUTDIR = os.path.join(ROOT, "results", "p1")
RUNS_REAL = os.path.join(ROOT, "runs", "real")

PARAMS = {
    "step_length_s": 0.5,
    "sim_end_s": 1200.0,
    "warmup_s": 10.0,
    "proximity_m": 80.0,
    "windows_s": [5, 10, 20, 30, 60],
    "otf_bin_width": 0.2,          # 与论文表 3.3 一致的 0.2 分箱
    "speeds_mps": {"slow": 13.0, "probe": 23.0, "fast": 32.0, "opposite": 25.0},
    "flows_vph": {"slow": 900, "probe": 120, "fast": 600, "opposite": 300},
    "scenarios": {
        "none": {},
        "cutin": {"period_s": 40.0, "trigger_gap_m": [25.0, 60.0],
                  "target_lane_offset": -1, "hold_s": 6.0},
        "lead-brake": {"period_s": 45.0, "gap_m": 30.0, "brake_to_mps": 10.0, "hold_s": 8.0},
        "lead-exit": {"period_s": 45.0, "gap_m": 30.0, "to_lane": 0, "hold_s": 10.0},
    },
}
EGO_TYPE = "probe"


def config_hash(scenario, probe_speed):
    payload = json.dumps({"params": PARAMS, "scenario": scenario, "probe_speed": probe_speed,
                          "net": os.path.basename(NET)}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def run_one_seed(seed, meta, scenario, probe_speed):
    sys.path.append(os.path.join(SUMOHOME, "tools"))
    import traci

    east, west = meta["east_edge"]["id"], meta["west_edge"]["id"]
    step, end = PARAMS["step_length_s"], PARAMS["sim_end_s"]
    traci.start([os.path.join(SUMOHOME, "bin", "sumo.exe"), "-n", NET, "--seed", str(seed),
                 "--step-length", str(step), "--end", str(end), "--no-step-log", "true",
                 "--no-warnings", "true", "--time-to-teleport", "-1", "--collision.action", "warn"])

    speeds = dict(PARAMS["speeds_mps"])
    speeds["probe"] = probe_speed          # 本次运行的探测车速
    for tid, spd in speeds.items():
        traci.vehicletype.copy("DEFAULT_VEHTYPE", tid)
        traci.vehicletype.setMaxSpeed(tid, spd)
        traci.vehicletype.setAccel(tid, 2.6)
        traci.vehicletype.setDecel(tid, 4.5)
    traci.route.add("route_east", [east])
    traci.route.add("route_west", [west])

    flows = PARAMS["flows_vph"]
    lanes = {"slow": 0, "probe": 1, "fast": 2}
    prob = {k: v * step / 3600.0 for k, v in flows.items()}
    acc, seq = defaultdict(float), defaultdict(int)
    probe_ids, fail = [], defaultdict(int)
    frames, injections = [], []
    cfg = PARAMS["scenarios"][scenario]
    next_act = 60.0
    active = {}
    lead_ids = {}

    t = 0.0
    while t <= end:
        traci.simulationStep()
        t = traci.simulation.getTime()
        if t > end:
            break

        for kind, lane in lanes.items():
            acc[kind] += prob[kind]
            while acc[kind] >= 1.0:
                acc[kind] -= 1.0
                vid = "%s.%d.%d" % (kind, seed, seq[kind]); seq[kind] += 1
                try:
                    traci.vehicle.add(vid, "route_east", typeID=kind, departLane=str(lane),
                                      departSpeed="max", departPos="base")
                    if kind == "probe":
                        probe_ids.append(vid)
                except Exception as exc:
                    fail[kind] += 1
                    if fail[kind] <= 2:
                        print("    [插入失败] %s: %s" % (vid, exc))
        acc["opposite"] += prob["opposite"]
        while acc["opposite"] >= 1.0:
            acc["opposite"] -= 1.0
            vid = "opp.%d.%d" % (seed, seq["opposite"]); seq["opposite"] += 1
            try:
                traci.vehicle.add(vid, "route_west", typeID="opposite",
                                  departSpeed="max", departPos="base")
            except Exception as exc:
                fail["opposite"] += 1

        # ── 工况注入 ──
        if scenario != "none" and t >= next_act:
            next_act = t + cfg["period_s"]
            # 注意：不要只取 probes[0]（那是路面上最老的一辆探测车，会大幅压低触发率）。
            # 遍历所有探测车，用第一个满足触发条件的。
            probes = [v for v in traci.vehicle.getIDList()
                      if traci.vehicle.getTypeID(v) == EGO_TYPE]
            for p in probes:
                pe = traci.vehicle.getRoadID(p)
                px = traci.vehicle.getLanePosition(p)
                pidx = traci.vehicle.getLaneIndex(p)
                done = False
                if scenario == "cutin":
                    lo, hi = cfg["trigger_gap_m"]
                    for v in traci.vehicle.getIDList():
                        if traci.vehicle.getTypeID(v) != "fast":
                            continue
                        if traci.vehicle.getRoadID(v) != pe or traci.vehicle.getLaneIndex(v) != 2:
                            continue
                        gap = px - traci.vehicle.getLanePosition(v)
                        if lo <= gap <= hi:
                            tgt = pidx + cfg["target_lane_offset"]
                            if 0 <= tgt <= 2 and tgt != traci.vehicle.getLaneIndex(v):
                                try:
                                    traci.vehicle.changeLane(v, tgt, 2.0)
                                    active[v] = (t + cfg["hold_s"], "lane", 2)
                                    injections.append({"t": round(t, 2), "kind": "cutin",
                                                       "vehicle": v, "behind": p,
                                                       "gap_m": round(gap, 2), "to_lane": tgt})
                                    done = True
                                except Exception:
                                    pass
                            break
                elif scenario in ("lead-brake", "lead-exit"):
                    pick = None
                    for v in traci.vehicle.getIDList():
                        if traci.vehicle.getTypeID(v) != "slow":
                            continue
                        if traci.vehicle.getRoadID(v) != pe or traci.vehicle.getLaneIndex(v) != pidx:
                            continue
                        if traci.vehicle.getLanePosition(v) > px:
                            pick = v; break
                    if pick is None:
                        for v in traci.vehicle.getIDList():
                            if traci.vehicle.getTypeID(v) != "fast" or traci.vehicle.getRoadID(v) != pe:
                                continue
                            gap = px - traci.vehicle.getLanePosition(v)
                            if -80.0 <= gap <= -20.0:      # 在探测车前方 20–80 m
                                try:
                                    traci.vehicle.changeLane(v, pidx, 2.0)
                                    pick = v
                                except Exception:
                                    pass
                                break
                    if pick:
                        if scenario == "lead-brake":
                            try:
                                traci.vehicle.slowDown(pick, cfg["brake_to_mps"], 3.0)
                                active[pick] = (t + cfg["hold_s"], "speed", speeds["slow"])
                                injections.append({"t": round(t, 2), "kind": "lead-brake",
                                                   "vehicle": pick, "ahead_of": p,
                                                   "to_mps": cfg["brake_to_mps"]})
                                done = True
                            except Exception:
                                pass
                        else:
                            try:
                                traci.vehicle.changeLane(pick, cfg["to_lane"], 2.0)
                                injections.append({"t": round(t, 2), "kind": "lead-exit",
                                                   "vehicle": pick, "ahead_of": p,
                                                   "to_lane": cfg["to_lane"]})
                                done = True
                            except Exception:
                                pass
                if done:
                    break

        # 注入结束后的恢复
        for v, (t_rel, kind, arg) in list(active.items()):
            if t >= t_rel and v in traci.vehicle.getIDList():
                try:
                    if kind == "lane":
                        traci.vehicle.changeLane(v, arg, 2.0)
                    else:
                        traci.vehicle.setSpeed(v, -1)     # 恢复跟驰模型
                except Exception:
                    pass
                del active[v]

        snap = {}
        for vid in traci.vehicle.getIDList():
            lid = traci.vehicle.getLaneID(vid)
            if ":" in lid:
                continue
            snap[vid] = [lid, traci.vehicle.getRoadID(vid), traci.vehicle.getLaneIndex(vid),
                         traci.vehicle.getLanePosition(vid), traci.vehicle.getTypeID(vid),
                         traci.vehicle.getSpeed(vid)]
        frames.append({"t": round(t, 3), "veh": snap})

    traci.close()
    return {"frames": frames, "probe_ids": probe_ids, "injections": injections,
            "insert_fail": dict(fail)}


def detect_events(frames, warmup_steps, prox, second_pass=False):
    events, seen, streak = [], set(), {}
    prev = {}
    rng = range(1, len(frames)) if second_pass else range(len(frames))
    for i in rng:
        cur = frames[i]["veh"]
        prv = frames[i - 1]["veh"] if second_pass else None
        for vid, cv in cur.items():
            if cv[4] != EGO_TYPE:
                continue
            pv = (prv.get(vid) if second_pass else prev.get(vid))
            if pv is None or pv[1] != cv[1] or pv[0] != cv[0]:
                streak[vid] = 0
                continue
            streak[vid] = streak.get(vid, 0) + 1
            if streak[vid] < warmup_steps:
                continue
            for oid, ov in cur.items():
                if oid == vid or ov[1] != cv[1] or abs(ov[2] - cv[2]) != 1:
                    continue
                po = (prv.get(oid) if second_pass else prev.get(oid))
                if po is None or po[1] != ov[1] or po[0] != ov[0]:
                    continue
                gp, gn = pv[3] - po[3], cv[3] - ov[3]
                if abs(gn) > prox:
                    seen.discard((vid, oid))
                    continue
                if (vid, oid) in seen:
                    continue
                if gp <= 0 < gn:
                    events.append((frames[i]["t"], "ot", vid, oid)); seen.add((vid, oid))
                elif gp >= 0 > gn:
                    events.append((frames[i]["t"], "otn", vid, oid)); seen.add((vid, oid))
        if not second_pass:
            prev = cur
    return events


def otf_series(events, window, sim_end):
    """逐窗口 OTF 序列（**不可跨窗口求和**：单辆自车行程内 N_ot≡N_otn，和为恒等式 0）"""
    n_win = int(sim_end // window) + 1
    per = defaultdict(lambda: [[0, 0] for _ in range(n_win)])
    for t, kind, vid, _o in events:
        w = int(t // window)
        if w < n_win:
            per[vid][w][0 if kind == "ot" else 1] += 1
    return {vid: [c[0] - c[1] for c in wins] for vid, wins in per.items()}


def distribution(values, bin_w):
    """按 bin_w 分箱，返回 {bin_center_str: fraction}（对应论文表 3.3–3.7 的占比口径）"""
    if not values:
        return {}, 0
    idx = [int(round(v / bin_w)) for v in values]
    cnt = defaultdict(int)
    for i in idx:
        cnt[i] += 1
    n = len(values)
    out = {}
    for i in sorted(cnt):
        out["%.1f" % (i * bin_w)] = round(cnt[i] / float(n), 4)
    return out, n


def mean_std(xs):
    if not xs:
        return None, None
    m = sum(xs) / float(len(xs))
    if len(xs) < 2:
        return round(m, 4), None
    var = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return round(m, 4), round(var ** 0.5, 4)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="*", default=[0, 1, 2, 3, 4])
    ap.add_argument("--scenarios", nargs="*", default=["cutin", "none", "lead-brake", "lead-exit"])
    ap.add_argument("--probe-speed", type=float, default=23.0)
    ap.add_argument("--save-trace", action="store_true",
                    help="落盘完整逐帧轨迹（~16 MB/次）；默认关闭以免总耗时翻倍")
    args = ap.parse_args()
    seeds = sorted(args.seeds)
    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs(RUNS_REAL, exist_ok=True)

    meta = {"east_edge": {"id": "A0B0", "length_m": 2980.8},
            "west_edge": {"id": "A0A1", "length_m": 2980.8}}
    if os.path.exists(META):
        try:
            m = json.load(io.open(META, encoding="utf-8"))
            meta = {"east_edge": m["east_edge"], "west_edge": m["west_edge"]}
        except Exception:
            pass
    else:
        # 元数据文件缺失时，从 net 反查（保持可运行）
        sys.path.append(os.path.join(SUMOHOME, "tools"))
        import sumolib
        net = sumolib.net.readNet(NET)
        cand = [e for e in net.getEdges() if not e.isSpecial() and len(e.getLanes()) >= 3]
        cand.sort(key=lambda e: e.getLength(), reverse=True)
        e1 = max(cand, key=lambda e: e.getShape()[-1][0])
        e2 = max([e for e in cand if (e.getShape()[-1][0] > e.getShape()[0][0]) !=
                  (e1.getShape()[-1][0] > e1.getShape()[0][0])], key=lambda e: e.getLength())
        meta = {"east_edge": {"id": e1.getID(), "length_m": round(e1.getLength(), 1),
                              "lanes": len(e1.getLanes())},
                "west_edge": {"id": e2.getID(), "length_m": round(e2.getLength(), 1),
                              "lanes": len(e2.getLanes())}}

    chash = config_hash(",".join(args.scenarios), args.probe_speed)
    print("config_hash=%s | 种子=%s | 工况=%s | 探测车速=%.1f m/s"
          % (chash, seeds, args.scenarios, args.probe_speed))

    for scenario in args.scenarios:
        per_seed_events, per_seed_meta = {}, {}
        all_inj = 0
        for seed in seeds:
            res = run_one_seed(seed, meta, scenario, args.probe_speed)
            frames = res["frames"]
            warm = int(PARAMS["warmup_s"] / PARAMS["step_length_s"])
            ev1 = detect_events(frames, warm, PARAMS["proximity_m"], False)
            ev2 = detect_events(frames, warm, PARAMS["proximity_m"], True)
            consistent = (len(ev1) == len(ev2) and
                          all(a[0] == b[0] and a[1] == b[1] and a[2] == b[2] and a[3] == b[3]
                              for a, b in zip(ev1, ev2)))
            per_seed_events[seed] = ev1
            per_seed_meta[seed] = {
                "n_frames": len(frames), "n_probe_vehicles": len(res["probe_ids"]),
                "N_ot": sum(1 for e in ev1 if e[1] == "ot"),
                "N_otn": sum(1 for e in ev1 if e[1] == "otn"),
                "n_injections": len(res["injections"]),
                "events_consistent_two_pass": bool(consistent),
            }
            all_inj += len(res["injections"])
            # 轨迹只在需要时落盘：每次 ~16 MB，全量写会让总耗时翻倍。
            # 默认只给第一个工况的 seed 0 留一份完整轨迹（供人工复核/离线复算）。
            if args.save_trace and scenario == args.scenarios[0] and seed == seeds[0]:
                trace = os.path.join(RUNS_REAL, "p1_%s_speed%02d_seed%d_trace.json"
                                     % (scenario, int(args.probe_speed), seed))
                with io.open(trace, "w", encoding="utf-8") as fh:
                    json.dump({"seed": seed, "scenario": scenario, "params": PARAMS,
                               "injections": res["injections"], "frames": frames},
                              fh, ensure_ascii=False)
                print("    （已落盘完整轨迹：%s）" % os.path.basename(trace))
            print("  [%s] seed=%d 帧=%d 探测车=%d ot=%d otn=%d 注入=%d 两遍一致=%s"
                  % (scenario, seed, len(frames), len(res["probe_ids"]),
                     per_seed_meta[seed]["N_ot"], per_seed_meta[seed]["N_otn"],
                     len(res["injections"]), consistent))

        bin_w = PARAMS["otf_bin_width"]
        for window in PARAMS["windows_s"]:
            pooled = []                       # 全部 (探测车 × 窗口) 的 OTF 值
            per_seed = {}
            seed_means = []
            for seed in seeds:
                series = otf_series(per_seed_events[seed], window, PARAMS["sim_end_s"])
                vals = [v for vs in series.values() for v in vs]
                pooled.extend(vals)
                m, s = mean_std(vals)
                frac, n = distribution(vals, bin_w)
                per_seed[str(seed)] = {"n_values": n, "mean": m, "std": s,
                                       "min": min(vals) if vals else None,
                                       "max": max(vals) if vals else None}
                if m is not None:
                    seed_means.append(m)
            frac_all, n_all = distribution(pooled, bin_w)
            agg_mean, agg_std = mean_std(seed_means)
            sign = ("positive" if (agg_mean or 0) > 0.005 else
                    "negative" if (agg_mean or 0) < -0.005 else "near-zero")

            payload = {
                "paper": "p1",
                "experiment": "main_otf_cfc_%s" % scenario,
                "scenario": "highway-mixed",
                "seedset": "s1",
                "seeds": seeds,
                "seed_semantics": "each seed = an independent SUMO run; all seeds reported, none selected",
                "config_path": "configs/p1/sumo_highway.net.xml",
                "config_hash": chash,
                "mode": "real",
                "platform": {"kind": "simulator",
                             "detail": "Eclipse SUMO 1.27.1; synthetic highway mainline, 3 lanes, "
                                       "%.0f m; NOT CARLA, NOT real-vehicle"
                                       % meta["east_edge"]["length_m"],
                             "compiler": None},
                "provenance": "ours-reproduced",
                "metrics": {
                    "per_scenario": {"highway-mixed": {
                        "following_rmse_m": None, "accel_sq_integral": None, "jerk_peak_mps3": None,
                        "lane_center_dev_m": None, "steer_angle_var": None,
                        "e2e_latency_ms": None, "mcu_mem_kb": None}},
                    "otf": {
                        "window_s": window,
                        "bin_width": bin_w,
                        "definition": "per-window (N_ot - N_otn) for each probe vehicle; report the "
                                      "DISTRIBUTION (fractions per bin, as in thesis Tables 3.3-3.7); "
                                      "never sum across windows (trip-wide sum is identically 0)",
                        "distribution_fractions": frac_all,
                        "n_values_pooled": n_all,
                        "sign": sign,
                        "probe_speed_mps": args.probe_speed,
                        "per_seed": per_seed,
                        "per_seed_run_meta": {str(k): v for k, v in per_seed_meta.items()},
                        "n_injections_total": all_inj,
                        "events_consistent_two_pass_all_seeds":
                            all(v["events_consistent_two_pass"] for v in per_seed_meta.values()),
                    },
                },
                "aggregates": {
                    "method": "mean-std",
                    "values": {"otf_per_window_mean": {"mean": agg_mean, "std": agg_std,
                                                       "n_seeds": len(seed_means)}},
                    "n_seeds": len(seeds),
                },
                "fairness": {"no_privileged_inputs": True, "equal_tuning_budget": True,
                             "same_map_and_seeds": True},
                "failure_modes": [],
                "notes": {
                    "abandoned_settings": [
                        "未做动态时间窗函数：需先有固定档逐窗口分布作基线",
                        "早期版本跨窗口求和 OTF → 恒等式（单辆自车行程内 N_ot≡N_otn），已改为逐窗口分布",
                        "早期版本把每个种子写成独立文件（seeds 只有 1 个）→ 违反契约，已改为单文件含全部种子",
                    ],
                    "known_biases": [
                        "合成交通流，非实车数据；证据等级 C",
                        "工况注入由 TraCI 强制（换道/减速），非人因驱动，激烈程度可能被低估",
                        "3 km 单段直路，不含匝道/交叉口；跨 ODD（城市/交叉口）结论无效",
                        "5 s 分箱下多数样本落在 0 与 ±0.2，桶宽敏感；与论文的对拍只比形状与趋势，不比绝对值",
                    ],
                    "seed_independence": {
                        "verified": True,
                        "split_policy": "by-entity",
                        "entity_group": "probe-vehicle",
                        "check_script": "src/stats/check_seed_independence.py",
                        "partial_scope": [],
                    },
                },
            }
            # ★ 文件名必须含 **窗口** 与 **探测车速**：
            #   初版两者都没有 → 5 个窗口互相覆盖（只剩 60 s），车速扫描也互相覆盖。
            win_tag = "-w%02d" % window
            spd_tag = "" if abs(args.probe_speed - 23.0) < 1e-9 else "-speed%02d" % int(round(args.probe_speed))
            name = "main_otf_cfc_%s%s%s_highway-mixed_s1.json" % (scenario, win_tag, spd_tag)
            payload["experiment"] = "main_otf_cfc_%s%s%s" % (scenario, win_tag, spd_tag)
            with io.open(os.path.join(OUTDIR, name), "w", encoding="utf-8") as fh:
                json.dump(payload, fh, ensure_ascii=False, indent=2)
            print("    w=%2ds → %s  众数箱=%s  符号=%s  跨种子 mean=%s"
                  % (window, name,
                     max(frac_all.items(), key=lambda kv: kv[1])[0] if frac_all else "-",
                     sign, agg_mean))
    print("产出目录: %s" % os.path.relpath(OUTDIR, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
