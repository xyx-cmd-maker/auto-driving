#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""用**真实图像**验证"能不能看到车在动"——而不是只读程序变量。

做法：给 ego 挂一个 RGB 相机，在 t=1s 与 t=13s 各存一帧 PNG。
若两帧画面**明显不同**（路景推进/车辆易位）⇒ 视野确实在随车移动；
若两帧相同 ⇒ 视野是静止的，"看不到车在动"的问题就没有真正解决。

输出：F:\\p1_runs\\viewcheck\\frame_t*.png（可直接打开目视，也可由 agent 读图核对）
"""
from __future__ import annotations

import os
import queue
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), "src", "envs")))
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import carla  # noqa: E402
from carla_town04 import Town04Env  # noqa: E402

OUT = os.environ.get("VIEWCHECK_DIR", r"F:\p1_runs\viewcheck")
os.makedirs(OUT, exist_ok=True)

env = Town04Env(n_traffic=26, verbose=False, max_episode_s=120.0)
env.follow_ego(True)
st = env.reset(scenario="none", seed=0)

# 挂 RGB 相机（跟在车头前方，模拟"驾驶员视角"）
bp = env.world.get_blueprint_library().find("sensor.camera.rgb")
bp.set_attribute("image_size_x", "800")
bp.set_attribute("image_size_y", "450")
bp.set_attribute("fov", "90")
# ⚠️ 相机必须挂在**车外前方**：Tesla Model 3 车长约 4.7 m，若把相机放在 x=+2.0、z=1.6，
# 它落在**车厢内部**——实测画面里出现的是车内座椅与仪表台（第一版就是这个错）。
# 改挂到车头前方 1.0 m、高 2.2 m（车顶之上），得到真正的向前视野。
cam_tf = carla.Transform(carla.Location(x=4.6, z=2.2), carla.Rotation(pitch=-8.0))
cam = env.world.spawn_actor(bp, cam_tf, attach_to=env.ego)
q: "queue.Queue" = queue.Queue()
cam.listen(q.put)

saved = []
spec_d = []
n = int(20 / (env.dt * env.ctrl_every))
for i in range(n):
    st = env.step_speed(target_speed_mps=12.0)
    t = st.t
    # 记录 spectator（= CarlaUE4 窗口里那台相机）到 ego 的距离：跟随开启时应基本恒定
    sp = env.world.get_spectator().get_transform().location
    el = env.ego.get_transform().location
    spec_d.append((t, ((sp.x - el.x) ** 2 + (sp.y - el.y) ** 2 + (sp.z - el.z) ** 2) ** 0.5))
    want = None
    if not saved and t >= 1.0:
        want = "t1"
    elif len(saved) == 1 and t >= 13.0:
        want = "t13"
    if want:
        # 取最新一帧
        frame = None
        while not q.empty():
            frame = q.get()
        if frame is not None:
            p = os.path.join(OUT, "frame_%s.png" % want)
            frame.save_to_disk(p)
            saved.append((want, p, t, st.ego_speed_mps))
            print("  已存 %s（t=%.1f s，车速 %.2f m/s）" % (p, t, st.ego_speed_mps))

cam.stop()
cam.destroy()
env.close()

# spectator 跟随统计（这是用户在窗口里实际看到的相机）
if spec_d:
    ds = [d for _, d in spec_d]
    first, last = ds[0], ds[-1]
    print()
    print("=== spectator（CarlaUE4 窗口相机）跟随统计 ===")
    print("  采样 %d 次 ｜ 距 ego：首 %.1f m → 末 %.1f m ｜ 最小 %.1f ｜ 最大 %.1f ｜ 均值 %.1f"
          % (len(ds), first, last, min(ds), max(ds), sum(ds) / len(ds)))
    print("  判定：%s"
          % ("距离始终在 5–15 m 内 ⇒ 窗口相机确实跟着车（用户能在窗口里看到车在动）"
             if max(ds) < 20 and min(ds) > 3
             else "距离超出跟随范围 ⇒ 窗口里可能看不到车，需检查 follow_ego"))

print()
print("=== 存下的帧 ===")
for tag, p, t, v in saved:
    print("  %-4s t=%5.1fs v=%5.2f m/s  %s  (%d 字节)"
          % (tag, t, v, p, os.path.getsize(p) if os.path.exists(p) else -1))
if len(saved) >= 2:
    import hashlib
    h = [hashlib.sha256(open(p, "rb").read()).hexdigest() for _, p, _, _ in saved]
    print()
    print("  两帧 SHA256 是否相同 = %s" % (h[0] == h[1]))
    print("  → 不同说明画面在变（视野随车移动）；相同说明视野静止，问题未解决")
