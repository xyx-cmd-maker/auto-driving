#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""SUMO → OTF 采集链路：最小可跑冒烟（docs/sumo-basics.md §3 的实现）

做三件事：
  1. netgenerate 造一条 3 车道高速直路（含对向车道，用于验证"对向流不得污染 OTF"）
  2. duarouter 生成车流：本车道自车流 + 邻车道快流 + 邻车道慢流（人为制造速度差，否则 OTF 恒为 0）
  3. TraCI 逐步采集，按学位论文第 3 章的事件学定义统计 N_ot / N_otn / OTF

判定规则（对应论文图 3.1）：
  N_ot  ：窗口内，某邻车 j 使 pos_self 由 <= pos_j 变为 > pos_j（自车超越 j）
  N_otn ：窗口内，某邻车 j 使 pos_j 由 <= pos_self 变为 > pos_self（自车被 j 超越）
  只统计"相邻车道"且"同向"的车辆；换道中的车辆跳过（避免把换道误计为超车）

输出：runs/smoke/otf_smoke_<window>s.json（mode: "smoke"，按 AGENTS.md §2 不可引用）
依赖：SUMO 自带 traci（不发包安装）
"""
import json
import os
import subprocess
import sys
import tempfile
import time

# ---------- 配置 ----------
STEP_LENGTH = 0.5      # s，显式写入结果，不用默认值
SIM_END = 300          # s
WINDOWS = [5, 10, 20, 30, 60]
SEEDS = [0]            # 冒烟只跑 1 个种子；真实算例用 seedset_s1（5 个）
N_LANES = 3            # 单向车道数
SPEED_FAST = 32.0      # m/s 邻车道快流（制造"被超车"）
SPEED_PROBE = 23.0     # m/s 本车道**探测车**速度（OTF 的自车视角）
SPEED_SLOW = 13.0      # m/s 邻车道慢流（制造"超车"）
FLOW_FAST = 600        # veh/h
FLOW_PROBE = 60        # veh/h —— 低密度：OTF 是**自车视角**量，探测车越少越干净
FLOW_SLOW = 900        # veh/h
FLOW_OPP = 300         # 对向流（用于验证污染过滤）
PROXIMITY_M = 80.0     # 只有纵向距离在此范围内的邻车才参与交互判定
WARMUP_S = 10.0        # 预热：出发瞬间的位置交叉不是超车，此前的窗口不计入统计

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
RUNS_SMOKE = os.path.join(ROOT, "runs", "smoke")


def sumo_home():
    home = os.environ.get("SUMO_HOME")
    if home and os.path.isdir(home):
        return home
    # 回退：读注册表（Windows）
    try:
        out = subprocess.check_output(
            ["reg", "query", r"HKCU\Environment", "/v", "SUMO_HOME"],
            stderr=subprocess.DEVNULL, text=True)
        for line in out.splitlines():
            if "SUMO_HOME" in line and "REG_" in line:
                return line.split("REG_")[1].split(None, 1)[1].strip()
    except Exception:
        pass
    return None


def build_network(home, workdir):
    net = os.path.join(workdir, "net.net.xml")
    netgenerate = os.path.join(home, "bin", "netgenerate.exe")
    # 注意：--grid.number 必须 >= 2（netgenerate 报 "number of nodes must be at least 2"）
    proc = subprocess.run([netgenerate, "--grid", "--grid.number=2", "--grid.length=2000",
                           "--default.lanenumber=%d" % N_LANES, "--default.speed=35",
                           "--no-turnarounds", "true", "--output-file", net],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError("netgenerate 失败（exit %d）：\n%s\n%s"
                           % (proc.returncode, proc.stdout[-800:], proc.stderr[-800:]))
    return net


def build_routes(workdir, net):
    """读 net，挑出两条**最长且车道数足够**的平行直边作为东向/西向主干，再手写 flows"""
    home = sumo_home()
    sys.path.append(os.path.join(home, "tools"))
    import sumolib
    parsed = sumolib.net.readNet(net)
    edges = [e for e in parsed.getEdges() if not e.isSpecial() and len(e.getLanes()) >= N_LANES]
    if len(edges) < 2:
        raise RuntimeError("产物里找不到两条 %d 车道边" % N_LANES)

    def length(e):
        return e.getLength()

    def is_straight(e):
        xs = [p[0] for p in e.getShape()]
        ys = [p[1] for p in e.getShape()]
        return (max(xs) - min(xs)) > 10 * max(1.0, max(ys) - min(ys)) or \
               (max(ys) - min(ys)) > 10 * max(1.0, max(xs) - min(xs))

    straight = [e for e in edges if is_straight(e)] or edges
    straight.sort(key=length, reverse=True)
    main_pair = straight[:2]
    # 找该对的反向配对：id 形如 "AB" / "BA"
    ids = {e.getID(): e for e in edges}
    east_edge = max(main_pair, key=lambda e: e.getShape()[-1][0])
    rev_id = east_edge.getID()[::-1]
    west_edge = ids.get(rev_id)
    if west_edge is None:
        # 退路：与 east 形状 x 方向相反的最长边
        def goes_east(e):
            return e.getShape()[-1][0] > e.getShape()[0][0]
        cand = [e for e in edges if goes_east(e) != goes_east(east_edge)]
        west_edge = max(cand, key=length) if cand else main_pair[1]

    def lane_id(edge, idx):
        return "%s_%d" % (edge.getID(), idx)

    rou = os.path.join(workdir, "flows.rou.xml")
    with open(rou, "w", encoding="utf-8") as fh:
        fh.write("<routes>\n")
        for vid, spd in (("fast", SPEED_FAST), ("probe", SPEED_PROBE), ("slow", SPEED_SLOW), ("opp", 25.0)):
            fh.write('  <vType id="%s" accel="2.6" decel="4.5" sigma="0.5" length="5" maxSpeed="%.1f"/>\n' % (vid, spd))
        # 单向三车道：lane0=慢流（被探测车超越）, lane1=探测车（OTF 的自车）, lane2=快流（超越探测车）
        fh.write('  <flow id="slow" type="slow" begin="0" end="%d" vehsPerHour="%d" from="%s" to="%s" departLane="0" departSpeed="max"/>\n'
                 % (SIM_END, FLOW_SLOW, east_edge.getID(), east_edge.getID()))
        fh.write('  <flow id="probe" type="probe" begin="0" end="%d" vehsPerHour="%d" from="%s" to="%s" departLane="1" departSpeed="max"/>\n'
                 % (SIM_END, FLOW_PROBE, east_edge.getID(), east_edge.getID()))
        fh.write('  <flow id="fast" type="fast" begin="0" end="%d" vehsPerHour="%d" from="%s" to="%s" departLane="2" departSpeed="max"/>\n'
                 % (SIM_END, FLOW_FAST, east_edge.getID(), east_edge.getID()))
        fh.write('  <flow id="opp" type="opp" begin="0" end="%d" vehsPerHour="%d" from="%s" to="%s" departSpeed="max"/>\n'
                 % (SIM_END, FLOW_OPP, west_edge.getID(), west_edge.getID()))
        fh.write("</routes>\n")
    return rou, east_edge.getID(), west_edge.getID()


def run_traci(home, net, rou, seed):
    sys.path.append(os.path.join(home, "tools"))
    import traci

    sumo_bin = os.path.join(home, "bin", "sumo.exe")
    cmd = [sumo_bin, "-n", net, "-r", rou, "--seed", str(seed),
           "--step-length", str(STEP_LENGTH), "--end", str(SIM_END),
           "--no-step-log", "true", "--no-warnings", "true",
           "--collision.action", "warn", "--time-to-teleport", "-1"]
    traci.start(cmd)

    # 交互判定：OTF 是**自车视角**量 → 只统计"自车类型为 EGO_TYPE"的超越/被超越事件。
    # 若统计全网所有车对，每对必然同时贡献一次 ot 与一次 otn，净和恒为 0（本脚本初版即踩此坑）。
    EGO_TYPE = "probe"
    events = []            # (t, type, self, other)
    seen_pairs = set()     # 去重：同一对车只记一次，直到间距重新拉开
    prev = {}              # vid -> (lane_id, edge_id, lane_index, x, type_id)
    same_edge_steps = {}   # vid -> 连续处于同一 edge 的步数（兼作预热计数与"非新到达"守卫）

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        t = traci.simulation.getTime()
        if t > SIM_END:
            break

        cur = {}
        for vid in traci.vehicle.getIDList():
            lid = traci.vehicle.getLaneID(vid)
            if ":" in lid:      # 内部车道（路口）跳过
                continue
            cur[vid] = (lid, traci.vehicle.getRoadID(vid), traci.vehicle.getLaneIndex(vid),
                        traci.vehicle.getLanePosition(vid), traci.vehicle.getTypeID(vid))

        for vid, (lid, edge_id, idx, x, typ) in cur.items():
            if typ != EGO_TYPE:
                continue                      # 只以探测车为自车
            p = prev.get(vid)
            if p is None or p[1] != edge_id or p[0] != lid:
                continue                      # 新到达 / 换边 / 换道：本步不参与
            if same_edge_steps.get(vid, 0) < WARMUP_S / STEP_LENGTH:
                continue                      # 预热：出发瞬间的位置交叉不是超车
            for oid, (olid, oedge, oidx, ox, otyp) in cur.items():
                if oid == vid or oedge != edge_id:
                    continue
                if abs(oidx - idx) != 1:      # 必须相邻车道（同向车道索引连续）
                    continue
                po = prev.get(oid)
                if po is None or po[1] != oedge or po[0] != olid:
                    continue                  # 邻车上一步不在同车道 → 换道中，跳过
                gap_prev = p[3] - po[3]
                gap_now = x - ox
                if abs(gap_now) > PROXIMITY_M:
                    seen_pairs.discard((vid, oid))
                    continue
                key = (vid, oid)
                if key in seen_pairs:
                    continue
                if gap_prev <= 0 < gap_now:
                    events.append((round(t, 3), "ot", vid, oid))     # 探测车超越邻车
                    seen_pairs.add(key)
                elif gap_prev >= 0 > gap_now:
                    events.append((round(t, 3), "otn", vid, oid))    # 探测车被邻车超越
                    seen_pairs.add(key)

        # 维护连续同边步数
        for vid, (_l, edge_id, _i, _x, _ty) in cur.items():
            if vid in prev and prev[vid][1] == edge_id:
                same_edge_steps[vid] = same_edge_steps.get(vid, 0) + 1
            else:
                same_edge_steps[vid] = 0
        prev = cur

    try:
        version = traci.getVersion()[1]
    except Exception:
        version = "unknown"
    traci.close()
    return events, version


def aggregate_by_window(events, sim_end, window):
    """按固定窗口聚合：每条事件归属其发生时刻所在窗口（避免跨界重复计数）"""
    n_windows = int(sim_end // window) + 1
    buckets = [{"window_index": i, "t_start": i * window, "t_end": (i + 1) * window,
                "N_ot": 0, "N_otn": 0} for i in range(n_windows)]
    for t, kind, _v, _o in events:
        i = int(t // window)
        if i >= n_windows:
            continue
        if kind == "ot":
            buckets[i]["N_ot"] += 1
        else:
            buckets[i]["N_otn"] += 1
    for b in buckets:
        b["OTF"] = b["N_ot"] - b["N_otn"]
    return buckets


def main():
    home = sumo_home()
    if not home:
        print("SUMO_HOME 取不到：请先设环境变量或确认安装（见 configs/env/local-cpu.lock.yaml）")
        return 2
    os.makedirs(RUNS_SMOKE, exist_ok=True)
    workdir = tempfile.mkdtemp(prefix="otf_smoke_")
    t0 = time.time()

    net = build_network(home, workdir)
    rou, east_edge, west_edge = build_routes(workdir, net)
    all_events = []
    version = None
    for seed in SEEDS:
        ev, version = run_traci(home, net, rou, seed)
        all_events.extend(ev)

    n_ot = sum(1 for e in all_events if e[1] == "ot")
    n_otn = sum(1 for e in all_events if e[1] == "otn")
    n_probes = len({e[2] for e in all_events})
    outputs = []
    for w in WINDOWS:
        buckets = aggregate_by_window(all_events, SIM_END, w)
        otf_vals = [b["OTF"] for b in buckets]
        payload = {
            "mode": "smoke",
            "source": "SUMO 合成交通流（非 CARLA、非实车；AGENTS.md §2 路线 B）",
            "sumo_version": version,
            "step_length_s": STEP_LENGTH,
            "window_s": w,
            "seeds": SEEDS,
            "sim_end_s": SIM_END,
            "warmup_s": WARMUP_S,
            "proximity_m": PROXIMITY_M,
            "ego_type": "probe",
            "ego_view_only": True,
            "network": {"n_lanes_one_way": N_LANES, "east_edge": east_edge, "west_edge": west_edge},
            "flows": {"fast": FLOW_FAST, "probe": FLOW_PROBE, "slow": FLOW_SLOW, "opposite": FLOW_OPP},
            "speeds_mps": {"fast": SPEED_FAST, "probe": SPEED_PROBE, "slow": SPEED_SLOW},
            "event_count": {"N_ot": n_ot, "N_otn": n_otn},
            "probe_vehicles_involved": n_probes,
            "otf_series": otf_vals,
            "otf_nonzero_windows": sum(1 for v in otf_vals if v != 0),
            "windows": buckets,
            "first_events": [{"t": e[0], "type": e[1], "self": e[2], "other": e[3]} for e in all_events[:10]],
            "notes": [
                "冒烟产物：按 AGENTS.md §2 不得进入任何对外文本",
                "只验证链路能否数出超车事件，不构成任何性能主张",
                "OTF 为自车（probe）视角量；事件已排除预热期与换道瞬间",
                "未与论文表 3.3-3.7 对拍（属下一步）",
            ],
        }
        out = os.path.join(RUNS_SMOKE, "otf_smoke_%ds.json" % w)
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        outputs.append((w, out, n_ot, n_otn, otf_vals))

    print("SUMO %s | step=%.2fs | seeds=%s | 自车类型=%s | 用时 %.1fs"
          % (version, STEP_LENGTH, SEEDS, "probe", time.time() - t0))
    print("事件总数（自车视角）：N_ot=%d（超越邻车）  N_otn=%d（被邻车超越）  涉及探测车 %d 辆"
          % (n_ot, n_otn, n_probes))
    for w, out, a, b, vals in outputs:
        nz = sum(1 for v in vals if v != 0)
        print("  window=%2ds  非零窗口 %2d/%2d  OTF 取值范围 [%d, %d]  产出 %s"
              % (w, nz, len(vals), min(vals), max(vals), os.path.relpath(out, ROOT)))
    if n_ot == 0 and n_otn == 0:
        print("[WARN] 事件数为 0：检查速度差是否足够、或判定规则是否被换道/对向流污染")
        return 1


if __name__ == "__main__":
    sys.exit(main())
