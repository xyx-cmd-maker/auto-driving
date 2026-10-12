#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OTF 核心：超车频次的窗口计数（**唯一实现**，供信息量版与闭环版共用）。

为什么单独抽出来
----------------
OTF 的定义必须**只有一个实现**。若 CARLA 闭环里另写一套，两处口径就会漂移，
届时"A1 消融用的 OTF"和"信息量版用的 OTF"可能不是同一个量——那是不可接受的。

口径（来自黄梦圆 2023 第 3 章，本项目沿用）：
    在长度为 W 的时间窗内，统计 ego 与**相邻车道**车辆之间发生的纵向超越事件：
      - 邻车相对 ego 前移（且跨越 ego 所在车道）→ 计 +1（ego 被超，`otn` 事件）
      - ego 相对邻车前移 → 计 −1
    窗口 OTF = ot_count − otn_count
    **注意符号约定**：本实现的返回值以"ego 被超越为正"还是"负"必须与
    `src/otf/run_a1_prediction.py` **完全一致**——该脚本里 `ot` 表示"邻车越过 ego"、
    `otn` 表示"ego 越过邻车"，窗口值 = ot − otn。此处照搬该约定，保持一致。

输入是**帧序列**（每帧给出各车的车道号与纵向位置），因此本模块不依赖 CARLA、SUMO 或任何仿真器。
"""
from __future__ import annotations


def _crossed(prev_lane, cur_lane, prev_pos, cur_pos, ego_lane):
    """判定一帧之间是否发生"跨 ego 车道的纵向超越"，返回 +1 / -1 / 0。"""
    d = cur_pos - prev_pos
    if abs(d) < 1e-9:
        return 0
    passer_lane = cur_lane if d > 0 else prev_lane      # 前移的一方
    other_lane = prev_lane if d > 0 else cur_lane
    if passer_lane == ego_lane and abs(other_lane - ego_lane) == 1:
        return 1 if d > 0 else -1
    return 0


def otf_window(frames: list[dict], ego_id, ego_lane: int, pos_key: str = "pos",
               lane_key: str = "lane") -> tuple[int, int]:
    """在给定的帧序列内统计 (ot, otn)。

    frames : 按时间升序的帧列表；每帧是 {vehicle_id: {pos_key: float, lane_key: int}}
    ego_id : 自车 id（在 frames 中出现）
    ego_lane : 自车所在车道（作为"相邻车道"判定的基准）

    返回 (ot, otn)；窗口 OTF = ot - otn。
    """
    ot = otn = 0
    ids = set()
    for f in frames:
        ids.update(f.keys())
    for vid in ids:
        if vid == ego_id:
            continue
        prev = None
        for f in frames:
            cur = f.get(vid)
            if cur is None:
                prev = None
                continue
            if prev is not None:
                c = _crossed(prev[lane_key], cur[lane_key], prev[pos_key], cur[pos_key], ego_lane)
                if c > 0:
                    ot += 1
                elif c < 0:
                    otn += 1
            prev = cur
    return ot, otn


def otf_from_frames(frames: list[dict], ego_id, ego_lane: int, **kw) -> int:
    """窗口 OTF 标量 = ot − otn（与 `src/otf/run_a1_prediction.py` 同号约定）。"""
    ot, otn = otf_window(frames, ego_id, ego_lane, **kw)
    return ot - otn


def phi_otf(otf_value: float, window_s: float, scale: float = 1.0) -> float:
    """把窗口 OTF 变成控制器可用的连续标量 Φ_OTF。

    这里刻意保持**最简**：Φ_OTF = otf / window_s · scale（单位：次/秒）。
    不做势场形状设计、不做饱和——那些属于控制器的输入编码，等 A1 消融跑出结论再调，
    现在加进去只会让"Φ_OTF 是否有用"这个问题变成"Φ_OTF 的编码是否有用"。

    术语纪律（AGENTS.md §1）：这是**结构先验**，**不称 physics-informed**。
    """
    if window_s <= 0:
        raise ValueError("window_s 必须为正，收到 %r" % window_s)
    return float(otf_value) / float(window_s) * float(scale)
