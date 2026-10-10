#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OTF 计数的真值校验（对应 AGENTS.md §0「反证问」与 docs/sumo-basics.md §6 待办 1）

目的：在链路输出被用于任何论断之前，先**证伪**它。做法有四层：

  1. 独立重算：把逐帧轨迹落盘后，用**独立的第二遍扫描**重新判定事件，与第一遍比较
  2. 逐事件证据：每个事件给出"触发前 10 s / 触发帧 / 触发后 10 s"的原始数值，
     间距应严格从 <=0 变到 >0（或反向），且触发帧就是符号翻转的那一帧
  3. 物理合理性：超越方的车速必须高于被超越方（否则不是超车）
  4. 独立性：抽查的事件必须落在**不同的相遇段**（相邻事件时刻间隔 >= 抽查间隔），
     避免同一个事件被当成两条证据（那是循环论证）

输出（落 runs/smoke/，属冒烟产物，按 AGENTS.md §2 不得引用）：
  otf_truthcheck_trace.json     逐帧轨迹（可人工复核）
  otf_truthcheck_report.json    自检报告 + 抽查事件（含前中后三帧数值）
"""
import io
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter

SUMOHOME = os.environ.get("SUMO_HOME", r"D:\SUMO\sumo-1.27.1")
sys.path.append(os.path.join(SUMOHOME, "tools"))
import traci, sumolib  # noqa: E402

STEP = 0.5
END = 300.0
NLANES = 3
EGO_TYPE = "probe"
SPD = {"slow": 13.0, "probe": 23.0, "fast": 32.0}
FLOW = {"slow": 900, "probe": 60, "fast": 600}
PROX = 80.0
WARMUP = 10.0
SPOT_INTERVAL_S = 15.0      # 抽查事件之间的最小时间间隔（保证是不同相遇段）
SPOT_COUNT = 9              # 抽查事件数（用户要求 5–10）

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUTDIR = os.path.join(ROOT, "runs", "smoke")


def build(home, wd):
    net = os.path.join(wd, "net.net.xml")
    p = subprocess.run([os.path.join(home, "bin", "netgenerate.exe"), "--grid", "--grid.number=2",
                        "--grid.length=2000", "--default.lanenumber=%d" % NLANES,
                        "--default.speed=40", "--no-turnarounds", "true", "--output-file", net],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("netgenerate 失败：\n%s\n%s" % (p.stdout[-500:], p.stderr[-500:]))
    parsed = sumolib.net.readNet(net)
    edges = [e for e in parsed.getEdges() if not e.isSpecial() and len(e.getLanes()) >= NLANES]

    def straight(e):
        xs = [q[0] for q in e.getShape()]
        ys = [q[1] for q in e.getShape()]
        return (max(xs) - min(xs)) > 10 * max(1.0, max(ys) - min(ys))

    st = sorted([e for e in edges if straight(e)] or edges, key=lambda e: e.getLength(), reverse=True)
    east = max(st[:2], key=lambda e: e.getShape()[-1][0])

    rou = os.path.join(wd, "f.rou.xml")
    with io.open(rou, "w", encoding="utf-8") as fh:
        fh.write("<routes>\n")
        for k, v in SPD.items():
            fh.write('  <vType id="%s" accel="2.6" decel="4.5" sigma="0.5" length="5" maxSpeed="%.1f"/>\n' % (k, v))
        for flow, lane in (("slow", 0), ("probe", 1), ("fast", 2)):
            fh.write('  <flow id="%s" type="%s" begin="0" end="%d" vehsPerHour="%d" from="%s" to="%s" departLane="%d" departSpeed="max"/>\n'
                     % (flow, flow, int(END), FLOW[flow], east.getID(), east.getID(), lane))
        fh.write("</routes>\n")
    return net, rou, east.getID()


def main():
    wd = tempfile.mkdtemp(prefix="truthcheck_")
    net, rou, east_id = build(SUMOHOME, wd)
    os.makedirs(OUTDIR, exist_ok=True)

    traci.start([os.path.join(SUMOHOME, "bin", "sumo.exe"), "-n", net, "-r", rou,
                 "--step-length", str(STEP), "--end", str(END), "--no-step-log", "true",
                 "--no-warnings", "true", "--time-to-teleport", "-1"])

    # ---- 第一遍：与 sumo_otf_smoke.py 相同的判定，记录 detected 事件 ----
    frames = []                 # [{"t":..., "veh": {vid: [lane_id, edge, lane_idx, x, type]}}]
    detected = []
    prev, same_edge_steps, seen = {}, {}, set()
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        t = traci.simulation.getTime()
        if t > END:
            break
        cur = {}
        for vid in traci.vehicle.getIDList():
            lid = traci.vehicle.getLaneID(vid)
            if ":" in lid:
                continue
            cur[vid] = [lid, traci.vehicle.getRoadID(vid), traci.vehicle.getLaneIndex(vid),
                        traci.vehicle.getLanePosition(vid), traci.vehicle.getTypeID(vid),
                        traci.vehicle.getSpeed(vid)]
        frames.append({"t": round(t, 3), "veh": {k: v for k, v in cur.items()}})

        for vid, cv in cur.items():
            if cv[4] != EGO_TYPE:
                continue
            pv = prev.get(vid)
            if pv is None or pv[1] != cv[1] or pv[0] != cv[0]:
                continue
            if same_edge_steps.get(vid, 0) < WARMUP / STEP:
                continue
            for oid, ov in cur.items():
                if oid == vid or ov[1] != cv[1] or abs(ov[2] - cv[2]) != 1:
                    continue
                po = prev.get(oid)
                if po is None or po[1] != ov[1] or po[0] != ov[0]:
                    continue
                gp, gn = pv[3] - po[3], cv[3] - ov[3]
                if abs(gn) > PROX:
                    seen.discard((vid, oid))
                    continue
                if (vid, oid) in seen:
                    continue
                if gp <= 0 < gn:
                    detected.append({"t": round(t, 3), "kind": "ot", "self": vid, "other": oid})
                    seen.add((vid, oid))
                elif gp >= 0 > gn:
                    detected.append({"t": round(t, 3), "kind": "otn", "self": vid, "other": oid})
                    seen.add((vid, oid))
        for vid, cv in cur.items():
            same_edge_steps[vid] = (same_edge_steps.get(vid, 0) + 1) if (vid in prev and prev[vid][1] == cv[1]) else 0
        prev = cur
    traci.close()

    # ---- 第二遍（独立重算）：只读落盘轨迹，用相同的符号穿越规则重判 ----
    redo = []
    seen2 = set()
    warm = {}
    for i in range(1, len(frames)):
        t, cur = frames[i]["t"], frames[i]["veh"]
        prv = frames[i - 1]["veh"]
        for vid, cv in cur.items():
            if cv[4] != EGO_TYPE:
                continue
            pv = prv.get(vid)
            if pv is None or pv[1] != cv[1] or pv[0] != cv[0]:
                warm[vid] = 0
                continue
            warm[vid] = warm.get(vid, 0) + 1
            if warm[vid] < WARMUP / STEP:
                continue
            for oid, ov in cur.items():
                if oid == vid or ov[1] != cv[1] or abs(ov[2] - cv[2]) != 1:
                    continue
                po = prv.get(oid)
                if po is None or po[1] != ov[1] or po[0] != ov[0]:
                    continue
                gp, gn = pv[3] - po[3], cv[3] - ov[3]
                if abs(gn) > PROX:
                    seen2.discard((vid, oid))
                    continue
                if (vid, oid) in seen2:
                    continue
                if gp <= 0 < gn:
                    redo.append({"t": t, "kind": "ot", "self": vid, "other": oid})
                    seen2.add((vid, oid))
                elif gp >= 0 > gn:
                    redo.append({"t": t, "kind": "otn", "self": vid, "other": oid})
                    seen2.add((vid, oid))

    match = (len(detected) == len(redo) and
             all(a == b for a, b in zip(detected, redo)))

    # ---- 抽查：取间隔 >= SPOT_INTERVAL_S 的不同相遇段 ----
    picks, last_t = [], -1e9
    for ev in detected:
        if ev["t"] - last_t >= SPOT_INTERVAL_S:
            picks.append(ev)
            last_t = ev["t"]
        if len(picks) >= SPOT_COUNT:
            break

    idx_of_t = {}
    for i, fr in enumerate(frames):
        idx_of_t[fr["t"]] = i

    spot = []
    for ev in picks:
        i_trig = idx_of_t.get(ev["t"])
        if i_trig is None:
            continue
        back = int(round(10.0 / STEP))
        fwd = int(round(10.0 / STEP))
        i_pre = max(0, i_trig - back)
        i_post = min(len(frames) - 1, i_trig + fwd)
        s, o = ev["self"], ev["other"]

        def gap(i):
            a = frames[i]["veh"].get(s)
            b = frames[i]["veh"].get(o)
            if not a or not b:
                return None
            return round(a[3] - b[3], 3)

        def spd(i, who):
            c = frames[i]["veh"].get(who)
            return None if not c else round(c[5], 2)

        gp = gap(i_trig - 1)
        gn = gap(i_trig)
        sign_ok = (gp is not None and gn is not None and
                   ((ev["kind"] == "ot" and gp <= 0 < gn) or (ev["kind"] == "otn" and gp >= 0 > gn)))
        self_faster = (spd(i_trig, s) is not None and spd(i_trig, o) is not None and
                       ((ev["kind"] == "ot" and spd(i_trig, s) > spd(i_trig, o)) or
                        (ev["kind"] == "otn" and spd(i_trig, s) < spd(i_trig, o))))
        spot.append({
            "event": ev,
            "gap_before_10s": gap(i_pre), "gap_at_prev_step": gp,
            "gap_at_trigger": gn, "gap_after_10s": gap(i_post),
            "speed_self": spd(i_trig, s), "speed_other": spd(i_trig, o),
            "sign_crossing_ok": bool(sign_ok),
            "speed_direction_ok": bool(self_faster),
            "frame_matches": {"trigger": frames[i_trig - 1]["t"], "after": frames[i_trig]["t"]},
        })

    report = {
        "mode": "smoke",
        "purpose": "OTF 计数的真值校验（证伪优先）",
        "sumo_version": None,
        "params": {"step": STEP, "end": END, "proximity_m": PROX, "warmup_s": WARMUP,
                   "ego_type": EGO_TYPE, "spot_interval_s": SPOT_INTERVAL_S},
        "pass1_detected": len(detected),
        "pass2_rederived": len(redo),
        "pass1_equals_pass2": bool(match),
        "kind_counts": dict(Counter(e["kind"] for e in detected)),
        "independent_encounters_among_picks": len(picks),
        "spot_checks": spot,
        "spot_all_sign_ok": all(x["sign_crossing_ok"] for x in spot),
        "spot_all_speed_ok": all(x["speed_direction_ok"] for x in spot),
        "notes": [
            "冒烟产物，不得引用（AGENTS.md §2）",
            "第二遍是独立重算，但用的是同一符号穿越规则 → 它证明的是实现一致，不是规则正确",
            "规则正确性由抽查与人工复核承担；未做的是与实车/他人实现的对比",
        ],
    }
    with io.open(os.path.join(OUTDIR, "otf_truthcheck_trace.json"), "w", encoding="utf-8") as fh:
        json.dump({"step": STEP, "frames": frames}, fh, ensure_ascii=False)
    with io.open(os.path.join(OUTDIR, "otf_truthcheck_report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)

    print("第一遍检出=%d  第二遍独立重算=%d  完全一致=%s" % (len(detected), len(redo), match))
    print("事件构成:", report["kind_counts"])
    print("抽查 %d 个事件（间隔 >= %.0f s 的不同相遇段）:" % (len(spot), SPOT_INTERVAL_S))
    print("  %-7s %-6s %-9s %-9s %-9s %-9s %-7s %-7s" % ("t", "kind", "gap@pre", "gap@trig", "gap@post", "v_self", "v_oth", "判定"))
    for x in spot:
        e = x["event"]
        print("  %-7.1f %-6s %-9s %-9s %-9s %-9s %-7s %s" %
              (e["t"], e["kind"], x["gap_at_prev_step"], x["gap_at_trigger"], x["gap_after_10s"],
               x["speed_self"], x["speed_other"],
               "OK" if (x["sign_crossing_ok"] and x["speed_direction_ok"]) else "FAIL"))
    print("抽查全部符号翻转正确: %s | 全部速度方向正确: %s"
          % (report["spot_all_sign_ok"], report["spot_all_speed_ok"]))
    return 0 if (match and report["spot_all_sign_ok"] and report["spot_all_speed_ok"]) else 1


if __name__ == "__main__":
    sys.exit(main())
