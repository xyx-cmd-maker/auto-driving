#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成高速主线场景（ODD 贴合）——AGENTS.md §5 的 ODD：高速公路主线 / 多车道 / 混行

产物（落 configs/p1/）：
  sumo_highway.net.xml    单向 3 车道、双向、单段长直路（与 toy 网格区分）
  sumo_highway.meta.json  几何与参数的机器可读记录（供结果 JSON 的 config_hash 用）

设计取舍（写清楚，避免以后被当"随便做做"）：
  - 用 netgenerate 的单段直路而非手写 net：可复现、无魔法数字
  - 保留对向边：用于验证"对向流不得污染 OTF"（docs/sumo-basics.md §4 坑 4）
  - 不做匝道/合流：本阶段只做"高速主线 + 邻车插入"，扩到四类工况时再说
"""
import io
import json
import os
import subprocess
import sys

SUMOHOME = os.environ.get("SUMO_HOME", r"D:\SUMO\sumo-1.27.1")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUTDIR = os.path.join(ROOT, "configs", "p1")

N_LANES = 3
EDGE_LENGTH = 3000.0      # m，单段主线
SPEED_LIMIT = 30.0        # m/s ≈ 108 km/h
STEP_LENGTH = 0.5         # s


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    net = os.path.join(OUTDIR, "sumo_highway.net.xml")
    meta_path = os.path.join(OUTDIR, "sumo_highway.meta.json")

    args = [os.path.join(SUMOHOME, "bin", "netgenerate.exe"),
            "--grid", "--grid.number=2", "--grid.length=%d" % int(EDGE_LENGTH),
            "--default.lanenumber=%d" % N_LANES, "--default.speed=%.0f" % SPEED_LIMIT,
            "--no-turnarounds", "true", "--output-file", net]
    proc = subprocess.run(args, capture_output=True, text=True)
    if proc.returncode != 0:
        print("netgenerate 失败：\n%s\n%s" % (proc.stdout[-800:], proc.stderr[-800:]))
        return 2

    # 读回几何，确认车道数与长度，并找出两条对向主干边
    sys.path.append(os.path.join(SUMOHOME, "tools"))
    import sumolib
    parsed = sumolib.net.readNet(net)
    edges = [e for e in parsed.getEdges() if not e.isSpecial()]

    def straight(e):
        xs = [p[0] for p in e.getShape()]
        ys = [p[1] for p in e.getShape()]
        return (max(xs) - min(xs)) > 10 * max(1.0, max(ys) - min(ys))

    st = sorted([e for e in edges if straight(e) and len(e.getLanes()) >= N_LANES],
                key=lambda e: e.getLength(), reverse=True)
    if len(st) < 2:
        print("找不到两条 3 车道直边，实际边数=%d" % len(edges))
        return 1
    east = max(st, key=lambda e: e.getShape()[-1][0])   # 形状 x 递增的那条 = 东向主干

    # 找对向主干边：几何方向与 east 相反、且车道数够的最长边
    # （不要用 ID 反转：A0B0 反转后还是 A0B0，会把自己当成对向边——本脚本初版即踩此坑）
    def goes_east(e):
        sh = e.getShape()
        return sh[-1][0] > sh[0][0]

    east_goes = goes_east(east)
    cands = [e for e in edges if len(e.getLanes()) >= N_LANES and goes_east(e) != east_goes]
    west = max(cands, key=lambda e: e.getLength()) if cands else None
    if west is None:
        print("找不到与 %s 对向的主干边（候选 0 条），无法建立双向场景" % east.getID())
        return 1

    meta = {
        "generator": "netgenerate (grid, 2 nodes, single straight segment)",
        "n_lanes_one_way": N_LANES,
        "design_edge_length_m": EDGE_LENGTH,
        "speed_limit_mps": SPEED_LIMIT,
        "step_length_s": STEP_LENGTH,
        "east_edge": {"id": east.getID(), "length_m": round(east.getLength(), 1),
                      "lanes": len(east.getLanes())},
        "west_edge": {"id": west.getID(), "length_m": round(west.getLength(), 1),
                      "lanes": len(west.getLanes())},
        "all_edges": sorted(e.getID() for e in edges),
        "odd_note": "高速公路主线 / 多车道 / 混行；晴天；不含匝道与交叉口（AGENTS.md §5）",
        "source_script": os.path.relpath(os.path.abspath(__file__), ROOT).replace("\\", "/"),
    }
    with io.open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)

    print("路网: %s" % os.path.relpath(net, ROOT))
    print("  %s: %d 车道, %.1f m" % (east.getID(), len(east.getLanes()), east.getLength()))
    print("  %s: %d 车道, %.1f m" % (west.getID(), len(west.getLanes()), west.getLength()))
    print("边清单: %s" % ", ".join(meta["all_edges"]))
    print("元数据: %s" % os.path.relpath(meta_path, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
