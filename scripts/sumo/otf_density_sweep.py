#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OTF 的**密度响应曲线**：非零窗口比例 / 均值 OTF 随交通密度的变化。

为什么做这个（2026-10-18 决策）
------------------------------
先前用 highD 的公开总量（5600 次换道 / 16.5 h）估算"多数 5 s 窗口 OTF 为 0"，
但 SUMO 在 3600 veh/h 下实测 **W=5 s 的非零比例是 0.501**，与估算相反。
⇒ 结论应改为：**OTF 的信息量取决于交通密度**，而不是"自由流必然稀疏"。

这条曲线能回答审稿人最可能问的一句话：
  "你的 OTF 在什么条件下才有信息量？"
并且它**不需要任何需要审批的数据集**（SUMO 已装、可复现、可公开），
是"真实数据拿不到"时最稳的替代证据。

产出
----
results/p1/otf_density_sweep_sumo_s<seeds>.json
  density_veh_per_hour → {W: {nonzero_fraction, mean, p95, samples}}

用法
----
  py -3.12 scripts/sumo/otf_density_sweep.py --seeds 1,2,3 --densities 600,1200,2400,3600,4800
"""
import argparse
import io
import json
import os
import sys
import shutil
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import otf_sparsity_sumo as base  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def run_one(seed: int, density: int, minutes: float, windows, lanes: int,
            length_m: float, speed_ms: float):
    d = tempfile.mkdtemp(prefix="sumo_sweep_%d_%d_" % (seed, density))
    try:
        base.write_scenario(d, seed, minutes, lanes, length_m, speed_ms, density)
        base.build_net(d)
        base.run_sumo(os.path.join(d, "run.sumocfg"), d)
        tracks = base.parse_fcd(os.path.join(d, "fcd.xml"))
        if not tracks:
            return None
        eids = sorted(tracks, key=lambda k: -len(tracks[k]))[:30]
        out = {"vehicles": len(tracks), "ego_used": len(eids), "windows": {}}
        for W in windows:
            vals = []
            for eid in eids:
                for _, n in base.otf_series(tracks, eid, W, dt=max(1.0, W / 2.0)):
                    vals.append(n)
            if not vals:
                continue
            vs = sorted(vals)
            nz = sum(1 for v in vals if v > 0)
            out["windows"]["W=%.0f" % W] = {
                "samples": len(vals),
                "nonzero_fraction": round(nz / len(vals), 4),
                "mean": round(sum(vals) / len(vals), 4),
                "p95": vs[int(0.95 * (len(vs) - 1))],
                "max": vs[-1],
            }
        return out
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="1,2,3")
    ap.add_argument("--densities", default="600,1200,2400,3600,4800")
    ap.add_argument("--minutes", type=float, default=15.0)
    ap.add_argument("--lanes", type=int, default=3)
    ap.add_argument("--length-m", type=float, default=1200.0)
    ap.add_argument("--speed-ms", type=float, default=33.3)
    ap.add_argument("--windows", default="5,10,20")
    args = ap.parse_args()

    seeds = [int(x) for x in args.seeds.split(",")]
    dens = [int(x) for x in args.densities.split(",")]
    windows = [float(x) for x in args.windows.split(",")]

    res = {
        "experiment": "otf_density_sweep_sumo",
        "note": ("同一套 OTF 定义（src/otf/otf_core.py 的 _crossed）；SUMO 合成交通流，非真实数据；"
                 "用途是给出 OTF 的**适用密度范围**"),
        "params": {"lanes": args.lanes, "length_m": args.length_m,
                   "speed_ms": args.speed_ms, "minutes": args.minutes},
        "table": {},
    }

    print("  密度(veh/h) × 窗口 → 非零比例 / 均值 OTF")
    for density in dens:
        per_W = {W: {"nz": [], "mean": []} for W in windows}
        for seed in seeds:
            r = run_one(seed, density, args.minutes, windows,
                        args.lanes, args.length_m, args.speed_ms)
            if not r:
                continue
            for W in windows:
                k = "W=%.0f" % W
                if k in r["windows"]:
                    per_W[W]["nz"].append(r["windows"][k]["nonzero_fraction"])
                    per_W[W]["mean"].append(r["windows"][k]["mean"])
        row = {}
        for W in windows:
            nzs, means = per_W[W]["nz"], per_W[W]["mean"]
            if not nzs:
                continue
            row["W=%.0f" % W] = {
                "nonzero_fraction_mean": round(sum(nzs) / len(nzs), 4),
                "nonzero_fraction_all": nzs,
                "otf_mean": round(sum(means) / len(means), 4),
                "n_seeds": len(nzs),
            }
        res["table"]["%d" % density] = row
        cells = " ｜ ".join("W=%s nz=%.3f" % (
            k.split("=")[1], v["nonzero_fraction_mean"]) for k, v in row.items())
        print("    %5d veh/h → %s" % (density, cells))

    os.makedirs(base.RESULTS, exist_ok=True)
    p = os.path.join(base.RESULTS, "otf_density_sweep_sumo_s%s.json" % args.seeds.replace(",", "-"))
    tmp = p + ".tmp"
    with io.open(tmp, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    os.replace(tmp, p)
    print("\n  已写 %s" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
