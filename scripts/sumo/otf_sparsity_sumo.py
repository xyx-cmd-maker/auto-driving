#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""SUMO 高速多车道 OTF 稀疏性实验（零门槛：SUMO 已装、无需任何数据审批）。

目的
----
回答一个决定论文论证方式的问题：**在自由流高速上，OTF（车辆跨越 ego 车道的次数）
在长度 W 的滑动窗口内非零的比例是多少？**

为什么必须做
------------
- highD/exiD 需要审批、CitySim 需填表、NGSIM 有 2017 年 TR-B 质量批判 ⇒ **真实数据不可依赖**；
- 但"OTF 稀疏"这个论证**不需要真实数据**：只要有一个自带车辆轨迹与车道号的多车道高速环境，
  用 `src/otf/otf_core.py` 的**同一套定义**就能算出稀疏性曲线；
- SUMO 本机已装（D:\\SUMO\\sumo-1.27.1），**零审批、可复现、可公开** ⇒ 这是最稳的"第二环境"。

产出
----
results/p1/otf_sparsity_sumo_s<seed>.json：
  - 每个窗口长度 W 的 {非零比例, 均值 OTF, 95% 分位, 样本数}
  - 交通参数（车道数、限速、流量、seed）—— 可追溯

用法
----
  py -3.12 scripts/sumo/otf_sparsity_sumo.py --seeds 1,2,3 --minutes 20
"""
import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src", "otf"))
RESULTS = os.path.join(ROOT, "results", "p1")

SUMO_HOME = os.environ.get("SUMO_HOME", r"D:\SUMO\sumo-1.27.1")
SUMO_BIN = os.path.join(SUMO_HOME, "bin", "sumo.exe")


def write_scenario(d: str, seed: int, minutes: float, lanes: int, length_m: float,
                   speed_ms: float, veh_per_hour: int) -> str:
    """写一个单路段多车道高速：nodes + edges + vtypes + flows + config。"""
    nodes = """<?xml version="1.0" encoding="UTF-8"?>
<nodes>
  <node id="n0" x="0" y="0" type="priority"/>
  <node id="n1" x="%.1f" y="0" type="priority"/>
</nodes>
""" % length_m

    edges = """<?xml version="1.0" encoding="UTF-8"?>
<edges>
  <edge id="e0" from="n0" to="n1" numLanes="%d" speed="%.1f" priority="1"/>
</edges>
""" % (lanes, speed_ms)

    # 速度因子异质 ⇒ 产生真实超车（这是 OTF 非零的必要条件）
    routes = """<?xml version="1.0" encoding="UTF-8"?>
<routes>
  <vType id="car" vClass="passenger" length="4.5" minGap="2.5" accel="2.6" decel="4.5"
         sigma="0.5" speedFactor="normc(1.00,0.18,0.60,1.40)" speedDev="0.1"/>
  <vType id="truck" vClass="truck" length="12.0" minGap="3.0" accel="1.2" decel="3.5"
         sigma="0.5" speedFactor="normc(0.80,0.10,0.55,1.00)" speedDev="0.05"/>
  <flow id="f_car" type="car" begin="0" end="%.0f" number="%d" from="e0" to="e0"
        departLane="random" departSpeed="max"/>
  <flow id="f_truck" type="truck" begin="0" end="%.0f" number="%d" from="e0" to="e0"
        departLane="random" departSpeed="max"/>
</routes>
""" % (minutes * 60.0, int(veh_per_hour * 0.85 * minutes / 60.0),
       minutes * 60.0, int(veh_per_hour * 0.15 * minutes / 60.0))

    cfg = """<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <input>
    <net-file value="net.net.xml"/>
    <route-files value="routes.rou.xml"/>
  </input>
  <time>
    <begin value="0"/>
    <end value="%.0f"/>
  </time>
  <processing>
    <time-to-teleport value="-1"/>
  </processing>
  <output>
    <fcd-output value="fcd.xml"/>
    <fcd-output.geo value="false"/>
  </output>
  <random_number>
    <seed value="%d"/>
  </random_number>
  <report>
    <no-step-log value="true"/>
    <no-warnings value="true"/>
  </report>
</configuration>
""" % (minutes * 60.0, seed)

    for name, body in (("nodes.nod.xml", nodes), ("edges.edg.xml", edges),
                       ("routes.rou.xml", routes), ("run.sumocfg", cfg)):
        with io.open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(body)
    return os.path.join(d, "run.sumocfg")


def build_net(d: str) -> None:
    """netconvert 把 nodes+edges 转成 net.net.xml。"""
    netconvert = os.path.join(SUMO_HOME, "bin", "netconvert.exe")
    cmd = [netconvert, "-n", os.path.join(d, "nodes.nod.xml"),
           "-e", os.path.join(d, "edges.edg.xml"),
           "-o", os.path.join(d, "net.net.xml"),
           "--no-turnarounds", "true"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("netconvert 失败: %s\n%s" % (r.returncode, (r.stderr or "")[-800:]))


def run_sumo(cfg: str, d: str) -> None:
    r = subprocess.run([SUMO_BIN, "-c", cfg], cwd=d, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("sumo 失败: %s\n%s" % (r.returncode, (r.stderr or "")[-800:]))


def parse_fcd(path: str):
    """返回 {veh_id: [(t, lane_id, s)]}（按时间升序）。"""
    tracks = {}
    for _ev, el in ET.iterparse(path, events=("end",)):
        if el.tag != "timestep":
            continue
        t = float(el.get("time"))
        for v in el.findall("vehicle"):
            vid = v.get("id")
            tracks.setdefault(vid, []).append((t, v.get("lane"), float(v.get("pos"))))
        el.clear()
    for k in tracks:
        tracks[k].sort(key=lambda x: x[0])
    return tracks


def lane_index(lane: str):
    """'e0_0' → 0；无法解析返回 None。"""
    m = re.search(r"_(\d+)$", lane or "")
    return int(m.group(1)) if m else None


def crossed(prev_lane, cur_lane, prev_s, cur_s, ego_lane):
    """与 src/otf/otf_core.py 的 `_crossed` **同一套定义**：

    只有"车辆跨越 ego 所在车道"才计数（对应真实换道/超车事件）。
    """
    d = cur_s - prev_s
    if abs(d) < 1e-9:
        return 0
    passer = cur_lane if d > 0 else prev_lane
    other = prev_lane if d > 0 else cur_lane
    if passer == ego_lane and abs(other - ego_lane) == 1:
        return 1 if d > 0 else -1
    return 0


def otf_series(tracks, ego_id, window_s: float, dt: float):
    """按窗口游标统计 ego 的 OTF 序列（每 dt 秒一个值）。"""
    ego = tracks[ego_id]
    ego_lanes = [lane_index(l) for _, l, _ in ego]
    # 预计算所有车辆的跨车道事件（时间戳 + 方向）
    events = []
    for vid, tr in tracks.items():
        if vid == ego_id:
            continue
        for i in range(1, len(tr)):
            t0, l0, s0 = tr[i - 1]
            t1, l1, s1 = tr[i]
            li0, li1 = lane_index(l0), lane_index(l1)
            if li0 is None or li1 is None or li0 == li1:
                continue          # 没换道
            for k in range(len(ego)):
                if ego[k][0] >= t1:
                    el = lane_index(ego[k][1])
                    if el is None:
                        break
                    d = crossed(li0, li1, s0, s1, el)
                    if d:
                        events.append((t1, d))
                    break
    events.sort()
    if not ego:
        return []
    t_end = ego[-1][0]
    out = []
    t = max(e[0] for e in events) if events else 0.0
    t = ego[0][0] + window_s
    while t <= t_end:
        lo, hi = t - window_s, t
        n = 0
        for (te, d) in events:
            if lo <= te < hi:
                n += 1
        out.append((t, n))
        t += dt
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="1,2,3")
    ap.add_argument("--minutes", type=float, default=20.0)
    ap.add_argument("--lanes", type=int, default=3)
    ap.add_argument("--length-m", type=float, default=1200.0)
    ap.add_argument("--speed-ms", type=float, default=33.3)   # 120 km/h
    ap.add_argument("--veh-per-hour", type=int, default=3600)
    ap.add_argument("--windows", default="5,10,20,30,60")
    ap.add_argument("--keep", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(SUMO_BIN):
        print("  ✗ 找不到 sumo: %s" % SUMO_BIN)
        return 2

    windows = [float(x) for x in args.windows.split(",")]
    seeds = [int(x) for x in args.seeds.split(",")]
    out_all = {"experiment": "otf_sparsity_sumo", "params": vars(args), "seeds": {}}

    for seed in seeds:
        d = tempfile.mkdtemp(prefix="sumo_otf_%d_" % seed)
        try:
            write_scenario(d, seed, args.minutes, args.lanes, args.length_m,
                           args.speed_ms, args.veh_per_hour)
            build_net(d)
            run_sumo(os.path.join(d, "run.sumocfg"), d)
            tracks = parse_fcd(os.path.join(d, "fcd.xml"))
            if not tracks:
                print("  ✗ seed %d 无轨迹" % seed)
                continue
            # 取轨迹最长的一批车作 ego（取前 40 辆，控制运行时间）
            eids = sorted(tracks, key=lambda k: -len(tracks[k]))[:40]
            res = {}
            for W in windows:
                vals = []
                for eid in eids:
                    s = otf_series(tracks, eid, W, dt=W / 2.0)
                    vals.extend(n for _, n in s)
                if not vals:
                    res["W=%.0f" % W] = {"n": 0}
                    continue
                vals_sorted = sorted(vals)
                nz = sum(1 for v in vals if v > 0)
                res["W=%.0f" % W] = {
                    "samples": len(vals),
                    "nonzero_fraction": round(nz / len(vals), 4),
                    "mean": round(sum(vals) / len(vals), 4),
                    "p95": vals_sorted[int(0.95 * (len(vals_sorted) - 1))],
                    "max": vals_sorted[-1],
                }
            out_all["seeds"]["seed_%d" % seed] = {
                "vehicles": len(tracks), "ego_used": len(eids), "windows": res}
            print("  seed %d：%d 辆车，%d 个 ego" % (seed, len(tracks), len(eids)))
            for k, v in res.items():
                if v.get("samples"):
                    print("    %-6s 非零比例 %.3f ｜ 均值 %.3f ｜ p95 %d ｜ 样本 %d"
                          % (k, v["nonzero_fraction"], v["mean"], v["p95"], v["samples"]))
        finally:
            if not args.keep:
                shutil.rmtree(d, ignore_errors=True)

    os.makedirs(RESULTS, exist_ok=True)
    p = os.path.join(RESULTS, "otf_sparsity_sumo_s%s.json" % args.seeds.replace(",", "-"))
    tmp = p + ".tmp"
    with io.open(tmp, "w", encoding="utf-8") as f:
        json.dump(out_all, f, ensure_ascii=False, indent=2)
    os.replace(tmp, p)
    print("\n  已写 %s" % p)
    print("  用途：作为'OTF 在自由流高速上稀疏'的**第二环境证据**（SUMO 合成流，非真实数据）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
