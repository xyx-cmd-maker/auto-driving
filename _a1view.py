#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A1 结果速览（用完即弃）。"""
import glob
import io
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

files = sorted(glob.glob(r"F:\p1_runs\cases\case_*.json"))
if not files:
    print("  暂无结果")
    sys.exit(0)

print("已完成 %d 局\n" % len(files))
hdr = "%-18s %9s %11s %12s %8s %14s" % (
    "场景/种子", "dCost", "d跟车RMSE", "d加速度积分", "d碰撞", "无效局off/on")
print(hdr)
print("-" * len(hdr))
rows = []
for f in files:
    d = json.load(io.open(f, encoding="utf-8"))
    p = d["paired"]
    ni = {a: d["arms"][a].get("n_invalid", 0) for a in ("a1_otf_off", "a1_otf_on")}
    tag = "%s/s%d" % (d["scenario"], d["seed"])
    fr = p["delta_following_rmse"]
    ai = p["delta_accel_sq_integral"]
    print("%-18s %+9.4f %11s %12s %+8d  off=%d on=%d"
          % (tag, p["delta_cost"],
             ("%+.3f" % fr) if fr is not None else "n/a",
             ("%+.3f" % ai) if ai is not None else "n/a",
             p["delta_collision"], ni["a1_otf_off"], ni["a1_otf_on"]))
    rows.append((tag, d))

print("\n=== 看护 ===")
for tag, d in rows:
    for arm in ("a1_otf_off", "a1_otf_on"):
        g = d["guards"][arm]
        nf = g.get("n_frames", 0)
        zf = g.get("zero_speed_frames", 0)
        print("  %-16s %-11s 帧=%-5d 零速=%-5d(%3.0f%%) 位移=%7.1fm 车辆=%-4d 有效=%s"
              % (tag, arm, nf, zf, 100.0 * zf / max(nf, 1), g.get("travelled_m", -1),
                 g.get("actors_max", -1), g.get("valid", True)))

print("\n=== 跨局汇总（n=%d）===" % len(rows))
if len(rows) < 5:
    print("  n<5：不做统计推断，只列方向一致性")
for k in ("delta_cost", "delta_following_rmse", "delta_accel_sq_integral", "delta_collision"):
    vals = [d["paired"][k] for _, d in rows if d["paired"].get(k) is not None]
    if not vals:
        continue
    pos = sum(1 for v in vals if v > 0)
    neg = sum(1 for v in vals if v < 0)
    print("  %-26s %-32s OTF更好 %d ｜ 更差 %d ｜ 持平 %d"
          % (k, str([round(v, 3) for v in vals]), neg, pos, len(vals) - pos - neg))
