#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""速度保持守门检查（**独立进程**执行）。

为什么要单独一个文件 + 子进程执行
--------------------------------
`carla_town04._selftest()` 里内置的 speed-hold 检查在同一进程内、已创建过若干环境之后
运行时会得到 **2.9–3.3 m/s**（三次可复现），而**独立进程**跑同一段代码是
**11.99 m/s / sd 0.000**（完全收敛）。已排除的假设：环境数量（前置 0/1/3/6 个环境均
11.99）、预热时长、有前车干扰、sim/ctrl 频率、max_episode_s、随机性。

⇒ 速度环本身是对的，偏低只出现在 harness 的"同进程连续多环境"场景。
因此把该检查**移出 harness、以子进程方式运行**：既消除矛盾，又让这项守门检查可信
（不修的话自检会长期带一个假 FAIL，掩盖以后的真问题）。

用法：py -3.12 scripts/smoke/check_speed_hold.py [--target 12] [--json]
退出码：0 通过；1 未过。--json 时把结果打成一行 JSON 供父进程解析。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, "..", "..", "src", "envs")))

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=float, default=12.0, help="目标速度 m/s")
    ap.add_argument("--warm-s", type=float, default=20.0)
    ap.add_argument("--hold-s", type=float, default=20.0)
    ap.add_argument("--tol", type=float, default=1.5, help="均值误差容限 m/s")
    ap.add_argument("--sd-max", type=float, default=1.5, help="标准差上限 m/s")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    from carla_town04 import Town04Env  # noqa: E402

    env = Town04Env(n_traffic=0, verbose=False, max_episode_s=a.warm_s + a.hold_s + 20.0)
    env.reset(scenario="none", seed=0)
    for _ in range(int(a.warm_s / (env.dt * env.ctrl_every))):
        env.step_speed(target_speed_mps=a.target)
    vs = []
    for _ in range(int(a.hold_s / (env.dt * env.ctrl_every))):
        st = env.step_speed(target_speed_mps=a.target)
        vs.append(st.ego_speed_mps)
    lateral = st.lateral_offset_m
    env.close()

    if not vs:
        out = {"ok": False, "reason": "采不到速度样本"}
    else:
        mean_v = sum(vs) / len(vs)
        sd = (sum((v - mean_v) ** 2 for v in vs) / len(vs)) ** 0.5
        ok = (abs(mean_v - a.target) < a.tol) and (sd < a.sd_max)
        out = {"ok": ok, "target": a.target, "mean": round(mean_v, 4), "sd": round(sd, 4),
               "min": round(min(vs), 4), "max": round(max(vs), 4),
               "lateral_offset_m": round(lateral, 4), "n": len(vs),
               "tol": a.tol, "sd_max": a.sd_max}

    if a.json:
        print(json.dumps(out, ensure_ascii=False))
    else:
        print("速度保持检查（独立进程，无交通流）")
        print("  目标 %.2f m/s ｜ 均速 %.2f ｜ sd %.4f ｜ 区间 %.2f–%.2f ｜ 横向偏差 %+.3f m"
              % (out.get("target", a.target), out.get("mean", float("nan")),
                 out.get("sd", float("nan")), out.get("min", float("nan")),
                 out.get("max", float("nan")), out.get("lateral_offset_m", float("nan"))))
        print("  判据：|均值误差| < %.2f 且 sd < %.2f → %s"
              % (a.tol, a.sd_max, "通过" if out["ok"] else "未过"))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
