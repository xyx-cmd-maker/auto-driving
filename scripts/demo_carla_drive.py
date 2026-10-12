#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""闭环 A1 的**目视确认**演示：把相机挂到 ego 后方，边开边打印状态。

★ 可以从任意目录运行（脚本内部把路径解析成绝对路径）。
  实测踩过：用户在 `C:\WINDOWS\system32` 下敲 `py -3.12 scripts/demo_carla_drive.py`，
  相对路径解析成 `C:\WINDOWS\system32\scripts\...` → `No such file or directory`。
  因此本脚本**不依赖 cwd**；更省事的入口是同目录下的 `run_carla_demo.cmd`（会顺带启动服务端）。

用法（先启动 CARLA 服务端；或用 run_carla_demo.cmd 一步到位）：
    py -3.12 "<项目绝对路径>\scripts\demo_carla_drive.py" --seconds 30
    py -3.12 scripts/demo_carla_drive.py --seconds 60 --scenario cutin --traffic 30

看什么：CarlaUE4 窗口里应能**看到自车在动**（相机跟在车后上方约 9 m）。
为什么需要它：CARLA 的 spectator 默认是自由相机、不跟随任何车辆，
实测 ego 走 82.5 m 而相机纹丝不动、二者相距 763 m——所以默认窗口里
看到的是地图别处的静止场景，容易误判成"车没动"。
"""
from __future__ import annotations

import argparse
import os
import sys

# 用 __file__ 解析绝对路径（脚本不依赖 cwd）
_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC_ENVS = os.path.abspath(os.path.join(_HERE, "..", "src", "envs"))
if _SRC_ENVS not in sys.path:
    sys.path.insert(0, _SRC_ENVS)

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    from carla_town04 import Town04Env  # noqa: E402
except ModuleNotFoundError as exc:
    print("导入失败：%s" % exc)
    print("  期望的模块目录：%s （存在=%s）" % (_SRC_ENVS, os.path.isdir(_SRC_ENVS)))
    print("  提示：请用 Python 3.12（CARLA wheel 只有 cp312）：py -3.12 <本脚本绝对路径>")
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=float, default=30.0)
    ap.add_argument("--target-speed", type=float, default=12.0, help="目标速度 m/s")
    ap.add_argument("--scenario", default="none",
                    choices=["none", "cutin", "lead-brake", "lead-exit"])
    ap.add_argument("--traffic", type=int, default=30)
    ap.add_argument("--no-follow", action="store_true", help="不跟随相机（对照用）")
    a = ap.parse_args()

    env = Town04Env(n_traffic=a.traffic, max_episode_s=a.seconds + 10.0)
    if not a.no_follow:
        env.follow_ego(True)
    st = env.reset(scenario=a.scenario, seed=0)
    print("场景=%s ｜ 目标速度 %.1f m/s ｜ 混行车 %d 辆 ｜ 相机跟随=%s"
          % (a.scenario, a.target_speed, a.traffic, not a.no_follow))
    print("→ 请看 CarlaUE4 窗口：应当能看到自车在前景中行驶")
    print("")
    n = int(a.seconds / (env.dt * env.ctrl_every))
    p0 = env.ego.get_transform().location
    for i in range(n):
        st = env.step_speed(target_speed_mps=a.target_speed)
        if i % max(1, int(3 / (env.dt * env.ctrl_every))) == 0:
            p = env.ego.get_transform().location
            d = ((p.x - p0.x) ** 2 + (p.y - p0.y) ** 2) ** 0.5
            spec = env.world.get_spectator().get_transform().location
            dcam = ((spec.x - p.x) ** 2 + (spec.y - p.y) ** 2) ** 0.5
            print("  t=%5.1fs  v=%5.2f m/s ｜ 已行驶 %6.1f m ｜ 前车距 %s ｜ 相机距车 %4.1f m"
                  % (st.t, st.ego_speed_mps, d,
                     ("%.1f m" % st.lead_gap_m) if st.lead_gap_m else "无", dcam))
    env.close()
    print("")
    print("结束。若窗口里车一直在动、相机跟着它 → 目视确认通过。")


if __name__ == "__main__":
    sys.exit(main())
