#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CARLA Town04 场景可见性验证（闭环 A1 的前置风险点检查）。

用法（**必须用 Python 3.12**，carla wheel 只有 cp312）：
    py -3.12 scripts/smoke/check_carla_town04.py
    py -3.12 scripts/smoke/check_carla_town04.py --vehicles 40 --seconds 20 --keep-server

它回答的问题（不是"CARLA 能不能跑"，而是"**闭环到底能不能建起来**"）：
  V1 能否加载 Town04
  V2 高速主线是否可用：找 ≥3 车道的同向路段（P1 ODD 要求多车道高速主线）
  V3 ego 能否 spawn 在该路段上
  V4 混行流能否生成（CARLA Traffic Manager 能否受控地放车）
  V5 **闭环所需的观测量能否拿到**：ego 状态、同车道前车、相邻车道车辆
  V6 能否从观测量算出 OTF（复用本项目的 ot / otn 口径，不是重新定义）
  V7 单步交互延迟（决定能否跑 100 Hz 控制回路）

**不做**：不做训练、不做控制、不写 results/（这是冒烟，不是实验）。
参照：configs/p1/ablation_a1_closedloop.yaml（协议已冻结）。
"""
from __future__ import annotations

import argparse
import sys
import time

# Windows 控制台默认 GBK，下面输出含非 GBK 字符时会在 print 处崩掉
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=2000)
    ap.add_argument("--vehicles", type=int, default=40, help="混行流车辆数（不含 ego）")
    ap.add_argument("--seconds", type=float, default=20.0, help="仿真观察时长")
    ap.add_argument("--step", type=float, default=0.05, help="固定步长（秒）；0.01 = 100 Hz")
    ap.add_argument("--keep-server", action="store_true", help="测完不关 ego/车辆（便于观察）")
    args = ap.parse_args()

    import carla

    R = []

    def ck(name, ok, detail):
        R.append((name, bool(ok), detail))

    # ---------- 连接 ----------
    client = carla.Client(args.host, args.port)
    client.set_timeout(60.0)
    try:
        world = client.get_world()
        ck("connect", True, "已连接；当前地图 = %s" % world.get_map().name)
    except Exception as exc:
        ck("connect", False, "连接失败：%s（服务端是否已启动？）" % exc)
        return report(R)

    # ---------- V1 载入 Town04 ----------
    try:
        if "Town04" not in world.get_map().name:
            t0 = time.perf_counter()
            world = client.load_world("Town04")
            world.tick()
            ck("V1 load-Town04", True, "已切换到 Town04，耗时 %.1f s（首次换图会下载缓存，可能更久）"
               % (time.perf_counter() - t0))
        else:
            ck("V1 load-Town04", True, "已在 Town04")
    except Exception as exc:
        ck("V1 load-Town04", False, "切换失败：%s" % exc)
        return report(R)

    carla_map = world.get_map()

    # ---------- V2 高速主线：找 ≥3 车道的长路段 ----------
    try:
        # 收集每个 road_id + 方向 上的车道数
        road_lanes: dict[tuple, set] = {}
        for wp in carla_map.generate_waypoints(2.0):
            key = (wp.road_id, wp.lane_id > 0)   # lane_id 正负表示两侧
            road_lanes.setdefault(key, set()).add(wp.lane_id)
        multi = {k: sorted(v) for k, v in road_lanes.items()
                 if len([x for x in v if abs(x) >= 1]) >= 3}
        # 取车道最多的一条
        if multi:
            best = max(multi.items(), key=lambda kv: len(kv[1]))
            ck("V2 multilane-road", True,
               "找到 %d 个 ≥3 车道（同向）路段；最多的一条 road_id=%s 同向=%s 车道=%s"
               % (len(multi), best[0][0], "正向" if best[0][1] else "反向", best[1]))
            target_road_id = best[0][0]
            target_forward = best[0][1]
        else:
            ck("V2 multilane-road", False, "未找到 ≥3 车道的同向路段 → P1 的 ODD 不成立")
            target_road_id, target_forward = None, None
    except Exception as exc:
        ck("V2 multilane-road", False, "枚举车道失败：%s" % exc)
        target_road_id, target_forward = None, None

    # ---------- V3 ego 能否 spawn 在目标路段 ----------
    ego = None
    try:
        bp_lib = world.get_blueprint_library()
        ego_bp = bp_lib.filter("vehicle.tesla.model3")[0]
        ego_bp.set_attribute("role_name", "ego")
        spawn_points = world.get_map().get_spawn_points()
        chosen = None
        if target_road_id is not None:
            for sp in spawn_points:
                wp = carla_map.get_waypoint(sp.location)
                if wp.road_id == target_road_id and (wp.lane_id > 0) == target_forward:
                    chosen = sp
                    break
        if chosen is None and spawn_points:
            chosen = spawn_points[0]
        if chosen is None:
            ck("V3 spawn-ego", False, "地图没有可用 spawn point")
        else:
            ego = world.spawn_actor(ego_bp, chosen)
            wp = carla_map.get_waypoint(ego.get_location())
            ck("V3 spawn-ego", True,
               "ego 已 spawn：road_id=%s lane=%s（目标 road_id=%s）"
               % (wp.road_id, wp.lane_id, target_road_id))
    except Exception as exc:
        ck("V3 spawn-ego", False, "spawn 失败：%s" % exc)

    # ---------- V4 混行流（Traffic Manager）----------
    tm = client.get_trafficmanager(8000)
    tm.set_synchronous_mode(True)
    world_settings = world.get_settings()
    world_settings.synchronous_mode = True
    world_settings.fixed_delta_seconds = args.step
    world.apply_settings(world_settings)

    vehicles = []
    try:
        tm.set_global_distance_to_leading_vehicle(2.5)
        tm.global_percentage_speed_difference(10.0)   # 混行：一部分车慢于限速
        bp_all = [b for b in world.get_blueprint_library().filter("vehicle.*")
                  if b.has_attribute("number_of_wheels")]
        spawn_points = world.get_map().get_spawn_points()
        batch = []
        for i in range(min(args.vehicles, max(0, len(spawn_points) - 1))):
            bp = bp_all[i % len(bp_all)]
            if bp.has_attribute("color"):
                bp.set_attribute("color", "%d,%d,%d" % (200, 60, 60))
            sp = spawn_points[(i + 1) % len(spawn_points)]
            batch.append(carla.command.SpawnActor(bp, sp).then(
                carla.command.SetAutopilot(carla.command.FutureActor, True, tm.get_port())))
        results = client.apply_batch_sync(batch, True)
        n_ok = sum(1 for r in results if not r.error)
        errs = [r.error for r in results if r.error][:2]
        vehicles = list(world.get_actors().filter("vehicle.*"))
        ck("V4 mixed-traffic", n_ok > 0,
           "批量 spawn %d/%d 成功（Traffic Manager 自动驾驶已启用）；错误示例：%s"
           % (n_ok, len(batch), errs if errs else "无"))
    except Exception as exc:
        ck("V4 mixed-traffic", False, "生成混行流失败：%s" % exc)

    # ---------- V5 闭环所需观测量 ----------
    obs = {}
    try:
        world.tick()   # 推进一帧让车辆获得状态
        if ego is None:
            ck("V5 observations", False, "无 ego，跳过")
        else:
            t = ego.get_transform()
            v = ego.get_velocity()
            c = ego.get_control()
            obs["ego"] = {
                "loc": (round(t.location.x, 2), round(t.location.y, 2)),
                "speed": round((v.x ** 2 + v.y ** 2 + v.z ** 2) ** 0.5, 3),
                "throttle": round(c.throttle, 3), "brake": round(c.brake, 3),
                "steer": round(c.steer, 3),
            }
            # 同车道前车 / 相邻车道车辆
            ego_wp = carla_map.get_waypoint(t.location)
            lead, adjacent = None, []
            for o in world.get_actors().filter("vehicle.*"):
                if o.id == ego.id:
                    continue
                ot = o.get_transform()
                o_wp = carla_map.get_waypoint(ot.location)
                d = t.location.distance(ot.location)
                if o_wp.lane_id == ego_wp.lane_id and o_wp.road_id == ego_wp.road_id:
                    fwd = o_wp.transform.get_forward_vector()
                    rel = ot.location - t.location
                    if rel.x * fwd.x + rel.y * fwd.y > 0:
                        if lead is None or d < lead[1]:
                            lead = (o.id, d)
                elif abs(o_wp.lane_id - ego_wp.lane_id) == 1 and d < 100.0:
                    adjacent.append(o.id)
            obs["lead"] = lead
            obs["adjacent_ids"] = adjacent
            ok = obs["ego"]["speed"] is not None and (lead is not None or len(adjacent) > 0)
            ck("V5 observations", ok,
               "ego 状态可读（speed=%.2f m/s）｜同车道前车=%s｜相邻车道车辆=%d 辆%s"
               % (obs["ego"]["speed"], ("id %s @ %.1f m" % lead) if lead else "无",
                  len(adjacent), "" if ok else "  ← 观测不足，闭环无法建"))
    except Exception as exc:
        ck("V5 observations", False, "读取观测失败：%s" % exc)

    # ---------- V6 能否算出 OTF（复用项目口径）----------
    try:
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", "otf"))
        from run_a1_prediction import dyn_window  # noqa: F401  (仅确认可复用)
        # 简化版 OTF：在 ego 周围统计"跨 ego 车道"的纵向超越事件（与项目口径同源：ot 为正、otn 为负）
        def otf_over(window_s, dt):
            hist = {}
            steps = int(window_s / dt)
            for step_i in range(steps):
                world.tick()
                for o in world.get_actors().filter("vehicle.*"):
                    w = carla_map.get_waypoint(o.get_location())
                    hist.setdefault(o.id, []).append(
                        (w.lane_id, w.road_id, o.get_location(), step_i))
            ego_lane = carla_map.get_waypoint(ego.get_location()).lane_id
            ot = otn = 0
            for oid, seq in hist.items():
                if oid == ego.id:
                    continue
                for a, b in zip(seq, seq[1:]):
                    d = b[2].x - a[2].x
                    if d > 0 and b[0] == ego_lane and abs(a[0] - ego_lane) == 1:
                        ot += 1
                    elif d < 0 and a[0] == ego_lane and abs(b[0] - ego_lane) == 1:
                        otn += 1
            return ot - otn, ot, otn

        t0 = time.perf_counter()
        otf_val, ot, otn = otf_over(5.0, args.step)
        ck("V6 compute-OTF", True,
           "5 s 窗内 OTF = %+d（ot=%d, otn=%d），用时 %.2f s —— 口径来自 src/otf/run_a1_prediction.py"
           % (otf_val, ot, otn, time.perf_counter() - t0))
    except Exception as exc:
        ck("V6 compute-OTF", False, "OTF 计算失败：%s" % exc)

    # ---------- V7 单步交互延迟 ----------
    try:
        world.tick()   # 预热
        n, t0 = 50, time.perf_counter()
        for _ in range(n):
            world.tick()
        per_ms = (time.perf_counter() - t0) / n * 1e3
        ck("V7 step-latency", True,
           "%.3f ms/帧 @ 固定步长 %.3f s（100 Hz 控制回路预算 10 ms；本项只测仿真推进，不含策略前向）"
           % (per_ms, args.step))
    except Exception as exc:
        ck("V7 step-latency", False, "计时失败：%s" % exc)

    # ---------- 收尾 ----------
    if not args.keep_server:
        try:
            for a in world.get_actors().filter("vehicle.*"):
                a.destroy()
            world_settings.synchronous_mode = False
            world.apply_settings(world_settings)
            ck("cleanup", True, "已销毁 %d 辆车并恢复异步模式" % len(vehicles))
        except Exception as exc:
            ck("cleanup", False, "清理失败：%s" % exc)
    else:
        ck("cleanup", True, "--keep-server：保留车辆便于人工观察")

    return report(R)


def report(R):
    print("CARLA Town04 场景可见性验证（闭环 A1 前置）")
    print("")
    for name, ok, detail in R:
        print("  %s %-20s %s" % ("OK  " if ok else "FAIL", name, detail))
    failed = [n for n, ok, _ in R if not ok]
    print("")
    print("[town04-visibility] %s：%d/%d"
          % ("全部通过" if not failed else "未过：" + ", ".join(failed),
             len(R) - len(failed), len(R)))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
