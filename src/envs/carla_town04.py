#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CARLA Town04 高速公路混行环境（闭环 A1 用）——**只提供观测与场景注入，不含控制器**。

用法（必须 Python 3.12，carla wheel 只有 cp312）：
    py -3.12 -c "from carla_town04 import Town04Env; ..."
    py -3.12 src/envs/carla_town04.py --selftest

设计边界
--------
- **本文件不做控制**：`step()` 接收外部给的目标加速度（由控制器决定）。这样两臂
  （OTF 开/关）共用完全相同的环境与场景，差异只可能来自控制器输入。
- **观测接口固定**（对应 `configs/p1/ablation_a1_closedloop.yaml` 的两臂输入集）：
    a1_otf_off: lead_gap_m, rel_speed_mps, ego_speed_mps
    a1_otf_on : 上式 + phi_otf
  观测里多给的字段（加速度、横向偏差、前车加速度）**只用于算指标与安全层**，
  不得喂给控制器——否则两臂信息集就不对等了（AGENTS.md §3 公平性）。
- ODD：高速公路主线 / 多车道 / 人工与自动混行 / 晴天（AGENTS.md §5）。
  CARLA 的天气在本文件里固定为 ClearNoon，保证两臂环境一致。
- 术语：OTF 是**结构先验**，不称 physics-informed（AGENTS.md §1）。

已知限制（写在此处而非事后补）
-----------------------------
1. **控制频率**：CARLA 在 Python 侧的推进速度实测远达不到 100 Hz（见 --selftest 输出）。
   因此本环境用"仿真步长 + 控制抽取"实现阶梯频率：仿真以 fixed_delta 推进，
   控制器以 control_hz 决策、其余帧零阶保持。**这是对协议 100 Hz 的偏离，必须记录。**
2. **场景注入**用 CARLA 原生 API 直接操纵 Traffic Manager 车辆，不是脚本化场景引擎；
   注入强度需要实测标定（参考项目在 SUMO 里踩过"注入强度不足"的坑）。
3. 混行程度由 Traffic Manager 的全局速度差参数近似，不区分驾驶风格分布。
"""
from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass, field

# Windows 控制台默认 GBK
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(_HERE, "..", "otf"), os.path.join(_HERE, "..", "eval")):
    _p = os.path.abspath(_p)
    if _p not in sys.path:
        sys.path.insert(0, _p)

from otf_core import otf_from_frames, phi_otf  # noqa: E402

SCENARIOS = ("none", "cutin", "lead-brake", "lead-exit")


@dataclass
class Step:
    """一步的观测与状态。控制器只能读 `controller_obs()` 里的字段。"""
    t: float
    # —— 控制器可用（两臂共用）——
    ego_speed_mps: float
    lead_gap_m: float | None
    rel_speed_mps: float
    # —— 仅 a1_otf_on 可用 ——
    otf: int
    phi_otf: float
    # —— 只用于指标/安全，不得喂控制器 ——
    ego_accel_mps2: float
    lead_accel_mps2: float | None
    lateral_offset_m: float
    steer: float
    collision: bool
    dt_s: float
    meta: dict = field(default_factory=dict)

    def controller_obs(self, use_otf: bool) -> list[float]:
        """按协议给出控制器输入。`use_otf=False` 即 a1_otf_off。"""
        gap = self.lead_gap_m if self.lead_gap_m is not None else 200.0
        v = [gap, self.rel_speed_mps, self.ego_speed_mps]
        if use_otf:
            v.append(self.phi_otf)
        return v


class Town04Env:
    """Town04 高速公路混行环境。`reset()` 开一局，`step(accel)` 推进一步。"""

    def __init__(self, host: str = "127.0.0.1", port: int = 2000,
                 sim_hz: float = 50.0, control_hz: float = 20.0,
                 n_traffic: int = 40, otf_window_s: float = 5.0,
                 town: str = "Town04", traffic_seed: int = 0,
                 max_episode_s: float = 120.0, verbose: bool = True):
        if control_hz > sim_hz:
            raise ValueError("control_hz 不得高于 sim_hz（%s > %s）" % (control_hz, sim_hz))
        self.host, self.port = host, port
        self.sim_hz = float(sim_hz)
        self.dt = 1.0 / self.sim_hz
        self.control_hz = float(control_hz)
        self.ctrl_every = max(1, int(round(self.sim_hz / self.control_hz)))
        self.n_traffic = int(n_traffic)
        self.otf_window_s = float(otf_window_s)
        self.town = town
        self.traffic_seed = int(traffic_seed)
        self.max_episode_s = float(max_episode_s)
        self.verbose = verbose

        self._carla = None
        self.world = None
        self.tm = None
        self.ego = None
        self._frames: list[dict] = []      # OTF 用的最近窗口帧
        self._t = 0.0
        self._prev_speed = 0.0
        self._scenario = "none"
        self._injected: list = []
        self._last_lead_id = None
        self._traffic_ids: set[int] = set()   # 只清理自己 spawn 的车（reset 成本的关键）
        self._last_applied_accel = 0.0         # 上一周期下发的目标加速度（前馈用）

    # ------------------------------------------------------------------ 连接
    def _lazy_init(self):
        if self.world is not None:
            return
        import carla
        self._carla = carla
        client = carla.Client(self.host, self.port)
        client.set_timeout(60.0)
        world = client.get_world()
        if self.town not in world.get_map().name:
            world = client.load_world(self.town)
        self.world = world
        self.client = client
        s = world.get_settings()
        s.synchronous_mode = True
        s.fixed_delta_seconds = self.dt
        world.apply_settings(s)
        # 固定晴天，保证两臂环境一致（AGENTS.md §5 的 ODD 含"晴天"）
        world.set_weather(carla.WeatherParameters.ClearNoon)
        self.tm = client.get_trafficmanager(8000)
        self.tm.set_synchronous_mode(True)
        self.tm.set_random_device_seed(self.traffic_seed)   # 交通流可复现的前提之一

    # ------------------------------------------------------------------ 工具
    def _map(self):
        return self.world.get_map()

    def _find_highway_spawn(self):
        """找一条 ≥3 车道同向路段上的 spawn point（P1 的 ODD 要求多车道高速主线）。"""
        cmap = self._map()
        lanes: dict[tuple, set] = {}
        for wp in cmap.generate_waypoints(2.0):
            lanes.setdefault((wp.road_id, wp.lane_id > 0), set()).add(wp.lane_id)
        multi = {k: v for k, v in lanes.items() if len([x for x in v if abs(x) >= 1]) >= 3}
        if not multi:
            return None, None
        (road_id, forward) = max(multi.items(), key=lambda kv: len(kv[1]))[0]
        for sp in cmap.get_spawn_points():
            wp = cmap.get_waypoint(sp.location)
            if wp.road_id == road_id and (wp.lane_id > 0) == forward:
                return sp, (road_id, forward)
        return None, (road_id, forward)

    def _longitudinal_frame(self):
        """返回 (ego_wp, forward_vec, right_vec)：用于把世界坐标投影到 ego 的车道坐标系。

        为什么不用 road_id/lane_id 相等来判"同一车道"：CARLA 的 `get_waypoint()` 返回**最近**的
        waypoint，在弯道/车身偏离中心时会在相邻车道间跳变，导致前车检测时有时无
        （自检里 `scenario-inject` 采到 0 个样本就是这个原因）。
        **改为纵向/横向投影**：沿 ego 前向的分量 = 前后距离，沿右向的分量 = 横向偏移；
        横向偏移在半车道宽内即视为同一车道。这在弯道上同样成立。
        """
        et = self.ego.get_transform()
        wp = self._map().get_waypoint(et.location)
        fwd = wp.transform.get_forward_vector()
        right = self._carla.Vector3D(x=-fwd.y, y=fwd.x, z=0.0)
        return wp, fwd, right

    @staticmethod
    def _project(rel, fwd, right):
        """把相对位移投影到 (纵向, 横向)。"""
        return (rel.x * fwd.x + rel.y * fwd.y, rel.x * right.x + rel.y * right.y)

    def _lane_half_width(self, wp) -> float:
        try:
            return float(wp.lane_width) * 0.5
        except Exception:
            return 1.8      # 车道宽约 3.6 m 的兜底

    def _lead(self):
        """返回 (车辆, 纵向距离)。

        判定"同一车道"用 **lane_id**，不用欧氏横向偏移：
        早期版本用 ego 的直线坐标投影判横向，但 Town04 的 highway 是**弯道**——实测把
        50–164 m 外的同行车辆投影出来得到 −3.8 → −71.5 m 的"横向偏移"，全部超出半车道宽，
        前车检测因此恒为空。lane_id 才是"是否同车道"的权威判据。
        纵向距离仍在 ego 的直线坐标系里算（50 m 内弯道误差可接受；上报值同此口径）。
        """
        if self.ego is None:
            return None, None
        et = self.ego.get_transform()
        wp, fwd, right = self._longitudinal_frame()
        best, best_along = None, None
        for o in self.world.get_actors().filter("vehicle.*"):
            if o.id == self.ego.id:
                continue
            ot = o.get_transform()
            owp = self._map().get_waypoint(ot.location)
            if owp.lane_id != wp.lane_id:          # 同一车道（lane_id 权威）
                continue
            along, _ = self._project(ot.location - et.location, fwd, right)
            if along <= 0.0 or along > 150.0:
                continue
            if best_along is None or along < best_along:
                best, best_along = o, along
        return best, best_along

    def _observe(self) -> Step:
        c = self._carla
        et = self.ego.get_transform()
        v = self.ego.get_velocity()
        speed = math.sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2)
        accel = (speed - self._prev_speed) / self.dt
        self._prev_speed = speed
        self._measured_accel = accel          # 反馈要用**实测**加速度
        ctrl = self.ego.get_control()

        ewp = self._map().get_waypoint(et.location)
        # 横向偏差：ego 到车道中心线的距离（用车道中心 waypoint 的横向分量）
        center = ewp.transform.location
        fwd = ewp.transform.get_forward_vector()
        rel = et.location - center
        lateral = rel.x * (-fwd.y) + rel.y * fwd.x    # 车道坐标系的横向分量

        lead, gap = self._lead()
        if lead is None:
            lead_gap, rel_speed, lead_acc = None, 0.0, None
        else:
            lt = lead.get_transform()
            lv = lead.get_velocity()
            lsp = math.sqrt(lv.x ** 2 + lv.y ** 2 + lv.z ** 2)
            lead_gap = gap
            rel_speed = lsp - speed
            lead_acc = self.tm.get_vehicle_last_acceleration(lead) if hasattr(
                self.tm, "get_vehicle_last_acceleration") else None

        otf_val = otf_from_frames(self._frames, self.ego.id, ewp.lane_id)

        # 碰撞：由 reset 时挂上的碰撞传感器回调置位（原来这里是空占位，永远 False）
        coll = bool(getattr(self, "_collision_flag", False))
        return Step(
            t=self._t, ego_speed_mps=speed, lead_gap_m=lead_gap, rel_speed_mps=rel_speed,
            otf=otf_val, phi_otf=phi_otf(otf_val, self.otf_window_s),
            ego_accel_mps2=accel, lead_accel_mps2=lead_acc,
            lateral_offset_m=lateral, steer=ctrl.steer, collision=coll, dt_s=self.dt,
            meta={"road_id": ewp.road_id, "lane_id": ewp.lane_id, "lead_id": getattr(lead, "id", None)},
        )

    def _record_frame(self):
        """把当前所有车辆的 (车道号, 纵向位置) 记入 OTF 窗口缓冲。

        纵向位置口径：用 waypoint 的 `s`（沿车道的累计弧长）即可——它是**同一车道内单调**的，
        足够判断"谁超过了谁"。早期版本把它按车道方向再乘 ±1，属于多余且错误的处理
        （方向已由 lane_id 的符号表达），会让跨车道的比较失真。
        """
        cmap = self._map()
        frame = {}
        for o in self.world.get_actors().filter("vehicle.*"):
            wp = cmap.get_waypoint(o.get_location())
            frame[o.id] = {"lane": wp.lane_id, "pos": wp.s}
        self._frames.append(frame)
        keep = int(self.otf_window_s * self.sim_hz) + 2
        if len(self._frames) > keep:
            self._frames = self._frames[-keep:]

    # ------------------------------------------------------------------ 交通
    def _route_ahead_points(self, start_sp, max_dist: float = 420.0, step: float = 10.0):
        """沿 ego 前进方向取一串**路点**（位置 + 朝向 + 沿路距离）。

        为什么不用 spawn point：诊断实测 Town04 的 spawn point 在 ego 前方 400 m 内**只集中在
        头 20 m**（且横向偏移 3.5–32 m，属于别的车道），20 m 之外一个都没有。因此
        "找 spawn point 放车"这条路走不通 —— 必须**沿路线自己算位置**，并用
        `world.try_spawn_actor(blueprint, Transform(...))` 直接放置（车辆可以放在任意路面位置，
        spawn point 只是常用起点，不是硬限制）。

        返回：[(Location, forward_vector, 沿路距离 m), ...]，按距离升序。
        """
        cmap = self._map()
        fwd0 = cmap.get_waypoint(start_sp.location).transform.get_forward_vector()
        out, loc, hd, d = [], start_sp.location, fwd0, 0.0
        seen = set()
        while d < max_dist and len(out) < int(max_dist / step) + 2:
            loc = self._carla.Location(x=loc.x + hd.x * step, y=loc.y + hd.y * step,
                                       z=loc.z)
            wp = cmap.get_waypoint(loc, project_to_road=True)
            if wp is None:
                break
            key = (round(wp.transform.location.x, 1), round(wp.transform.location.y, 1))
            if key in seen:
                break
            seen.add(key)
            d += step
            hd = wp.transform.get_forward_vector()
            out.append((wp.transform.location, hd, d, wp))
            loc = wp.transform.location
        return out

    def _spawn_traffic(self, start_sp):
        """生成混行流：沿 ego 前方的路线，**按车道**放置车辆。

        三轮修正的完整教训（都写在注释里，避免下次再踩）：
          ① 按 spawn_points 顺序均匀撒 → 与 ego 同 road_id 的车 = 0
          ② 按"同 road_id + 在 ego 前方"筛 → 该路段只有 9 个点、前方为 0 个
          ③ 沿路网 BFS 找下游 spawn point → 前方 400 m 内只有头 20 m 有点，仍为 0
        最终：**不看 spawn point，沿路线在各车道上按固定间距直接放车**——这样
        前方一定有车、且车道分布可控，两个要求（前车存在、混行多车道）同时满足。
        """
        c = self._carla
        carla = c
        self.tm.set_global_distance_to_leading_vehicle(2.5)
        self.tm.global_percentage_speed_difference(15.0)   # 混行：部分车慢于限速
        bps = [b for b in self.world.get_blueprint_library().filter("vehicle.*")
               if b.has_attribute("number_of_wheels")]

        route = self._route_ahead_points(start_sp)
        # ⚠️ CARLA 行为：**刚 spawn 的 actor 在 tick 之前 get_transform() 返回 (0,0,0)**。
        # 必须显式用 spawn 点的坐标，不能依赖 actor 查询——否则所有相对 ego 的计算都会
        # 以世界原点为基准（实测：全部车被放到原点、前车检测恒为空）。
        ego_loc = start_sp.location
        ego_wp = self._map().get_waypoint(ego_loc)
        # ego 所在车道 + 两侧相邻车道（P1 的 ODD 是多车道混行）
        lane_ids = [ego_wp.lane_id]
        for off in (-1, 1):
            try:
                nb = (ego_wp.get_left_lane() if off < 0 else ego_wp.get_right_lane())
            except Exception:
                nb = None
            if nb is not None and getattr(nb.lane_type, "name", "") == "Driving":
                lane_ids.append(nb.lane_id)

        spawned, failed = [], 0
        spacing = 45.0
        _dbg = bool(os.environ.get("CARLA_ENV_DEBUG"))
        for loc, fwd, d, ref in route:
            if len(spawned) >= self.n_traffic:
                break
            if d < 15.0 or (d % spacing) > 12.0:
                continue
            # ⚠️ 这里**不能**再对这一 loc 做 get_waypoint(project_to_road=True)：
            # route 的坐标保留了 spawn 点的 z，重新投影会把点吸附到**另一条路**上
            # （实测：全部车道 waypoint 变成 ego 脚下那条 road 47 的同一个点，
            #  26 辆车叠在一处、前车检测恒为空）。路线点本身就是 waypoint，直接用。
            if ref is None:
                continue
            # 用 CARLA 自己的车道对象取同级车道中心 —— 不再用"横向矩形偏移"近似。
            # 早期版本用 right 向量 + 车道索引差算偏移，结果车被放到路肩/对面车道，
            # `_lead()` 永远匹配不到（实测：同路同车道 0 辆）。
            for lane_wp in self._lane_family(ref):
                if len(spawned) >= self.n_traffic:
                    break
                tf = carla.Transform(
                    carla.Location(x=lane_wp.transform.location.x,
                                   y=lane_wp.transform.location.y,
                                   z=lane_wp.transform.location.z + 0.4),
                    lane_wp.transform.rotation)
                actor = None
                last_err = ""
                for k in range(3):      # 撞了就往后挪一点再试
                    tf2 = carla.Transform(
                        carla.Location(x=tf.location.x - fwd.x * (k * 6.0),
                                       y=tf.location.y - fwd.y * (k * 6.0),
                                       z=tf.location.z), tf.rotation)
                    actor = self.world.try_spawn_actor(bps[(len(spawned) + failed) % len(bps)], tf2)
                    if actor is not None:
                        break
                    # try_spawn_actor 失败时只返回 None、不给原因；用 spawn_actor 捕获异常文本
                    # 作为诊断信息（**它不会成功**，所以不会多留车；万一成功立即销毁）。
                    probe = None
                    try:
                        probe = self.world.spawn_actor(
                            bps[(len(spawned) + failed) % len(bps)], tf2)
                        last_err = "spawn_actor 竟然成功（已回滚）"
                    except RuntimeError as exc:
                        last_err = str(exc)
                    if probe is not None:
                        try:
                            probe.destroy()
                        except Exception:
                            pass
                if actor is None:
                    failed += 1
                    if failed <= 6:
                        rel = tf.location - ego_loc
                        print("      [spawn 失败] 纵向 %+.1f m 横向 %+.1f m 原因: %s"
                              % (rel.x * fwd.x + rel.y * fwd.y,
                                 rel.x * (-fwd.y) + rel.y * fwd.x, last_err or "未知"))
                    continue
                actor.set_autopilot(True, self.tm.get_port())
                spawned.append(actor)
                if _dbg and len(spawned) <= 3:
                    self.world.tick()
                    at = actor.get_transform().location
                    el = self.ego.get_transform().location
                    print("    [direct] 第 %d 辆：actor=(%.1f,%.1f) ego=(%.1f,%.1f) "
                          "期望=(%.1f,%.1f)"
                          % (len(spawned), at.x, at.y, el.x, el.y,
                             lane_wp.transform.location.x, lane_wp.transform.location.y))

        self._traffic_ids = {a.id for a in spawned}

        # ⚠️ 关键：CARLA 的 actor 是**异步流式创建的**——try_spawn_actor 返回后，
        # 新 actor 的 transform 可能仍是 (0,0,0)，要等若干 tick 才真正生效。
        # 实测：只 tick 1 次时有 7/10 辆车读到的坐标还是原点，导致所有"相对 ego"的
        # 计算与 _lead() 全部失效（前车检测恒为 None）。
        # 这里等到"所有已 spawn 的车都有非原点坐标"再继续，最多等 max_wait 个 tick。
        self._settle_actors(spawned, max_wait=30)

        if os.environ.get("CARLA_ENV_DEBUG"):
            self._debug_layout(spawned, start_sp)
        return len(spawned), failed, len(self._lane_family(ego_wp)), len(route)

    def _settle_actors(self, actors, max_wait: int = 30):
        """等到所有 actor 的位置真正生效（非原点/非零四元数）。"""
        pending = list(actors)
        for _ in range(max_wait):
            alive = []
            for a in pending:
                try:
                    loc = a.get_transform().location
                    if abs(loc.x) < 1e-3 and abs(loc.y) < 1e-3:
                        alive.append(a)      # 仍是默认值，未生效
                except Exception:
                    pass
            if not alive:
                return True
            pending = alive
            self.world.tick()
            self._record_frame()
        # 仍未生效的从记录里剔除，避免污染后续计算
        unloaded = {a.id for a in pending}
        self._traffic_ids -= unloaded
        if self.verbose and unloaded:
            print("    [env] %d 辆车在 %d 个 tick 内未加载完成，已从统计中剔除"
                  % (len(unloaded), max_wait))
        return False

    def _debug_layout(self, spawned, start_sp):
        """打印布下的车相对 ego 的纵向/横向位置（受 CARLA_ENV_DEBUG 控制）。

        这类几何问题只看代码会一直猜错——实测连续三轮"同路车=0/2"都源自布点几何，
        而日志里看不到车到底落在哪。把诊断做进环境，下次直接开这个开关即可。
        """
        et = self.ego.get_transform()
        wp = self._map().get_waypoint(et.location)
        fwd = wp.transform.get_forward_vector()
        right = self._carla.Vector3D(x=-fwd.y, y=fwd.x, z=0.0)
        half = self._lane_half_width(wp)
        print("    [debug] ego road=%s lane=%s 半车道宽=%.2f 绝对(%.1f,%.1f)"
              % (wp.road_id, wp.lane_id, half, et.location.x, et.location.y))
        rows = []
        for o in spawned:
            ot = o.get_transform()
            owp = self._map().get_waypoint(ot.location)
            rel = ot.location - et.location
            rows.append((rel.x * fwd.x + rel.y * fwd.y, rel.x * right.x + rel.y * right.y,
                         o.id, owp.road_id, owp.lane_id, ot.location.x, ot.location.y))
        rows.sort()
        for along, lat, oid, rid, lid, ax, ay in rows[:12]:
            mark = " ← 可作前车" if (along > 0 and lid == wp.lane_id and along <= 150) else ""
            print("    [debug] id=%-5s 绝对(%8.1f,%8.1f) 纵向 %+8.1f m 直线横向 %+7.1f m "
                  "road=%-5s lane=%-4s%s"
                  % (oid, ax, ay, along, lat, rid, lid, mark))
        n_ok = sum(1 for a, _, _, _, l, _, _ in rows
                   if a > 0 and l == wp.lane_id and a <= 150)
        print("    [debug] 符合 _lead() 判定（同 lane_id、在前、≤150 m）的车 = %d 辆" % n_ok)

    def _lane_family(self, ref_wp):
        """返回 ego 所在车道 + 左右相邻可行驶车道（同一 road 上）。"""
        out = [ref_wp]
        for getter in ("get_left_lane", "get_right_lane"):
            try:
                nb = getattr(ref_wp, getter)()
            except Exception:
                nb = None
            if nb is not None and getattr(nb.lane_type, "name", "") == "Driving" \
                    and nb.road_id == ref_wp.road_id:
                out.append(nb)
        return out

    # ------------------------------------------------------------------ 场景
    def _inject(self, scenario: str, t_since_reset: float):
        """四类工况注入。每次 reset 后按固定节奏触发，保证两臂场景一致。"""
        if scenario == "none" or self.ego is None:
            return
        period = 12.0
        # 在 t = 6, 18, 30, ... 触发
        k = int((t_since_reset - 6.0) / period)
        if t_since_reset < 6.0 or k < 0:
            return
        trigger_id = (scenario, k)
        if trigger_id in getattr(self, "_fired", set()):
            return
        self._fired = getattr(self, "_fired", set())
        self._fired.add(trigger_id)

        lead, gap = self._lead()
        if lead is None:
            return
        try:
            if scenario == "lead-brake":
                # 前车减速（用 TM 强制低速一段时间）
                self.tm.vehicle_percentage_speed_difference(lead, 80.0)
                self._injected.append((lead, t_since_reset + 4.0, "restore_speed"))
            elif scenario == "lead-exit":
                # 前车换到相邻车道（"驶离"）
                wp = self._map().get_waypoint(lead.get_location())
                tgt = wp.get_left_lane() or wp.get_right_lane()
                if tgt is not None and tgt.lane_type.name == "Driving":
                    self.tm.force_lane_change(lead, tgt.lane_id < wp.lane_id)
            elif scenario == "cutin":
                # 让 ego 前方相邻车道的一辆车并入 ego 车道（插入）
                ewp = self._map().get_waypoint(self.ego.get_location())
                best = None
                for o in self.world.get_actors().filter("vehicle.*"):
                    if o.id == self.ego.id:
                        continue
                    owp = self._map().get_waypoint(o.get_location())
                    if owp.road_id != ewp.road_id:
                        continue
                    if abs(owp.lane_id - ewp.lane_id) != 1:
                        continue
                    et = self.ego.get_transform()
                    rel = o.get_transform().location - et.location
                    fwd = ewp.transform.get_forward_vector()
                    along = rel.x * fwd.x + rel.y * fwd.y
                    if 5.0 < along < 40.0:
                        best = o
                        break
                if best is not None:
                    wp = self._map().get_waypoint(best.get_location())
                    self.tm.force_lane_change(best, wp.lane_id > ewp.lane_id)
        except Exception as exc:
            if self.verbose:
                print("    [场景注入失败] %s: %s" % (scenario, exc))

    def _apply_deferred(self, t_since_reset: float):
        keep = []
        for actor, due, kind in getattr(self, "_injected", []):
            if t_since_reset >= due:
                try:
                    if kind == "restore_speed" and actor.is_alive:
                        self.tm.vehicle_percentage_speed_difference(actor, 15.0)
                except Exception:
                    pass
            else:
                keep.append((actor, due, kind))
        self._injected = keep

    # ------------------------------------------------------------------ API
    def reset(self, scenario: str = "none", seed: int = 0) -> Step:
        """开一局：清理上一局、放 ego、放混行流、重置 OTF 缓冲。"""
        self._lazy_init()
        c = self._carla
        self._scenario = scenario
        self._fired = set()
        self._frames = []
        self._injected = []
        self._t = 0.0
        self._prev_speed = 0.0
        self._collision_flag = False
        # 释放上一次的碰撞传感器（不释放会报 "sensor object went out of scope but still alive"）
        for attr in ("_collision_sensor",):
            s = getattr(self, attr, None)
            if s is not None:
                try:
                    s.stop()
                    s.destroy()
                except Exception:
                    pass
                setattr(self, attr, None)

        # 清理**只清自己 spawn 的**车：全场 destroy 会连带清掉别的东西并触发重载，
        # 实测是全流程最慢的一步（reset 53.7 s）。只清自己的车 → reset 应降到秒级。
        killed = 0
        for a in self.world.get_actors().filter("vehicle.*"):
            if a.id in self._traffic_ids or (self.ego is not None and a.id == self.ego.id):
                try:
                    a.destroy()
                    killed += 1
                except Exception:
                    pass
        self._traffic_ids = set()
        self.ego = None
        self.world.tick()

        sp, road = self._find_highway_spawn()
        sps = self._map().get_spawn_points()
        if sp is None:
            sp = sps[0] if sps else None
        if sp is None:
            raise RuntimeError("地图没有可用 spawn point")

        # 清空目标点附近的车：可能来自本环境上一局（已按 id 清过）或**别的脚本**留下的车。
        # 不做这一步时，spawn 会以 "collision at spawn position" 失败（实测遇到）。
        for o in self.world.get_actors().filter("vehicle.*"):
            try:
                if o.get_location().distance(sp.location) < 12.0:
                    o.destroy()
            except Exception:
                pass
        self.world.tick()

        bp = self.world.get_blueprint_library().filter("vehicle.tesla.model3")[0]
        bp.set_attribute("role_name", "ego")
        try:
            self.ego = self.world.spawn_actor(bp, sp)
        except RuntimeError as exc:            # 依次尝试同道路上的其它点，最后退化到任意点
            alt = [p for p in sps if self._map().get_waypoint(p.location).road_id == sp.location and False]
            alt = [p for p in sps
                   if self._map().get_waypoint(p.location).road_id
                   == self._map().get_waypoint(sp.location).road_id]
            self.ego = None
            for p in alt[1:6] + sps[:5]:
                try:
                    for o in self.world.get_actors().filter("vehicle.*"):
                        if o.get_location().distance(p.location) < 12.0:
                            o.destroy()
                    self.world.tick()
                    self.ego = self.world.spawn_actor(bp, p)
                    sp = p
                    break
                except RuntimeError:
                    continue
            if self.ego is None:
                raise RuntimeError("ego spawn 失败：候选点均被占用（%s）" % exc)

        # ⚠️ 关键：CARLA 里**刚 spawn 的 actor 在 tick 之前 get_transform() 全是 (0,0,0)**。
        # 因此必须 tick 一次，并断言位置确实生效——否则后续所有"相对 ego"的计算都会以
        # 世界原点为基准（实测：26 辆车被放到原点、前车检测恒为空、油门推进无效）。
        self.world.tick()
        ego_loc = self.ego.get_transform().location
        if abs(ego_loc.x) < 1e-6 and abs(ego_loc.y) < 1e-6 and abs(sp.location.x) > 1.0:
            raise RuntimeError("ego 位置在 tick 后仍为原点（spawn 点应为 (%.1f, %.1f)）——"
                               "CARLA 未按预期初始化 actor" % (sp.location.x, sp.location.y))
        self.ego.set_autopilot(False)
        # 挂碰撞传感器：CARLA 里碰撞只有订阅了才拿得到（原来我用空占位，collision 恒为 False）
        self._collision_flag = False
        try:
            cb = self.world.get_blueprint_library().find("sensor.other.collision")
            self._collision_sensor = self.world.spawn_actor(cb, self._carla.Transform(),
                                                            attach_to=self.ego)

            def _on_collision(_event, _self=self):
                _self._collision_flag = True

            self._collision_sensor.listen(_on_collision)
        except Exception as exc:
            self._collision_sensor = None
            if self.verbose:
                print("  [env] 碰撞传感器未挂上：%s（collision 指标将不可用）" % exc)
        self._record_frame()

        n_ok, errs, n_same, pool_same = self._spawn_traffic(sp)
        for _ in range(2):          # 让 TM 把车开动起来（2 帧足够；5 帧是 reset 的另一处浪费）
            self.world.tick()
            self._record_frame()
        self._t = 0.0
        # 关键：把 _prev_speed 设成**当前真实速度**，否则第一步会算出巨大的假加速度
        # （实测出现过 24.3 m/s² 这种非物理值，会污染 accel_sq_integral 与 jerk 指标）。
        v0 = self.ego.get_velocity()
        self._prev_speed = math.sqrt(v0.x ** 2 + v0.y ** 2 + v0.z ** 2)
        self._last_applied_accel = 0.0
        self._measured_accel = 0.0
        if self.verbose:
            lead, gap = self._lead()
            print("  [env] scenario=%s seed=%s｜ego road_id=%s｜混行车 %d 辆（同路 %d 辆，"
                  "同路候选点 %d）%s｜前车 %s"
                  % (scenario, seed, road[0] if road else "?", n_ok, n_same,
                     pool_same, ("（部分失败：%s）" % errs) if errs else "",
                     ("id=%s @ %.1f m" % (lead.id, gap)) if lead else "无"))
        return self._observe()

    def step(self, accel_mps2: float) -> Step:
        """给目标加速度（m/s²），推进一个**控制周期**（含 control 抽取）。

        纵向控制用**前馈 + 反馈**，而不是纯反馈：
          纯反馈在低速时会被滚动阻力吃掉（实测命令 0.5 m/s² 只有约 20% 油门 → 车不动）。
          前馈按"节气门 ∝ 目标加速度 / 最大加速度"，反馈补实测误差；再从静止起步时给最小油门。
        """
        c = self._carla
        A_MAX, A_BRAKE = 3.0, 6.0     # 近似量程：满油门约 3 m/s²，满刹车约 6 m/s²
        MIN_THROTTLE = 0.35           # 从静止起步的最小油门（否则克服不了静摩擦/滚阻）
        for i in range(self.ctrl_every):
            cur_v = math.sqrt(sum(x ** 2 for x in
                                  (self.ego.get_velocity().x, self.ego.get_velocity().y,
                                   self.ego.get_velocity().z)))
            target = float(accel_mps2)
            # 反馈必须用**实测**加速度。早期版本错用了"上一次下发的目标值"，
            # 于是 err 恒为 0、只剩纯前馈 → 17% 油门推不动静止的车（诊断实测确认）。
            err = target - getattr(self, "_measured_accel", 0.0)

            throttle = brake = 0.0
            if target >= 0:
                throttle = target / A_MAX + max(0.0, err) / A_MAX      # 前馈 + 正误差补偿
            else:
                brake = -target / A_BRAKE + max(0.0, -err) / A_BRAKE
            if cur_v < 0.5 and target > 0.1:
                throttle = max(throttle, MIN_THROTTLE)                 # 起步辅助
            ctrl = c.VehicleControl()
            ctrl.throttle = max(0.0, min(1.0, throttle))
            ctrl.brake = max(0.0, min(1.0, brake))
            self.ego.apply_control(ctrl)

            self.world.tick()
            self._t += self.dt
            self._record_frame()
            self._inject(self._scenario, self._t)
            self._apply_deferred(self._t)
        st = self._observe()
        done = (self._t >= self.max_episode_s)
        st.meta["done"] = done
        return st

    def close(self):
        try:
            for a in self.world.get_actors().filter("vehicle.*"):
                a.destroy()
            s = self.world.get_settings()
            s.synchronous_mode = False
            self.world.apply_settings(s)
        except Exception:
            pass


# ---------------------------------------------------------------------- 自检
def _selftest():
    import time as _time
    R = []

    def ck(n, ok, d):
        R.append((n, bool(ok), d))

    env = Town04Env(n_traffic=30, sim_hz=50.0, control_hz=20.0, max_episode_s=30.0)
    t0 = _time.perf_counter()
    st = env.reset(scenario="none", seed=0)
    ck("reset", True, "reset 用时 %.1f s；ego %.2f m/s；前车距 %s"
       % (_time.perf_counter() - t0, st.ego_speed_mps,
          ("%.1f m" % st.lead_gap_m) if st.lead_gap_m else "无"))

    # 观测契约
    off = st.controller_obs(use_otf=False)
    on = st.controller_obs(use_otf=True)
    ck("obs-arm-off", len(off) == 3, "a1_otf_off 输入维度 = %d（协议要求 3）" % len(off))
    ck("obs-arm-on", len(on) == 4, "a1_otf_on 输入维度 = %d（协议要求 4）" % len(on))
    ck("obs-phi", abs(on[3] - st.phi_otf) < 1e-9,
       "Φ_OTF = %.4f（次/秒，窗 %.1f s，窗口 OTF=%d）" % (st.phi_otf, env.otf_window_s, st.otf))

    # 推进 + 计时
    t0 = _time.perf_counter()
    n = 20
    for _ in range(n):
        st = env.step(accel_mps2=0.5)
    wall = (_time.perf_counter() - t0) / n
    ck("step", True, "%.4f s/控制周期（墙钟）｜仿真推进 %.3f s/周期｜实时倍率 %.3fx"
       % (wall, env.dt * env.ctrl_every, (env.dt * env.ctrl_every) / wall))
    ck("speed-moved", st.ego_speed_mps > 0.1, "ego 速度 = %.2f m/s" % st.ego_speed_mps)
    ck("metrics-available", st.ego_accel_mps2 is not None,
       "加速度 %.3f m/s²｜横向偏差 %.3f m｜前车加速度 %s"
       % (st.ego_accel_mps2, st.lateral_offset_m,
          ("%.2f" % st.lead_accel_mps2) if st.lead_accel_mps2 is not None else "不可得"))

    # 场景注入是否真的改变了前车行为
    st2 = env.reset(scenario="lead-brake", seed=0)
    gaps = []
    for _ in range(int(20 / (env.dt * env.ctrl_every))):
        st2 = env.step(accel_mps2=0.0)
        if st2.lead_gap_m:
            gaps.append(st2.lead_gap_m)
    ck("scenario-inject", len(gaps) > 0,
       "lead-brake：采到 %d 个间距样本，范围 %.1f–%.1f m（注入是否生效需看是否收窄）"
       % (len(gaps), min(gaps) if gaps else -1, max(gaps) if gaps else -1))

    env.close()
    print("CARLA Town04 环境自检")
    print("")
    for n_, ok, d in R:
        print("  %s %-16s %s" % ("OK  " if ok else "FAIL", n_, d))
    bad = [n_ for n_, ok, _ in R if not ok]
    print("")
    print("[carla-town04] %s：%d/%d" % ("全部通过" if not bad else "未过：" + ", ".join(bad),
                                        len(R) - len(bad), len(R)))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(_selftest())
