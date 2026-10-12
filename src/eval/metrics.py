#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""闭环 A1 的指标计算（纯函数，不依赖 CARLA / 不依赖仿真器）。

用法（可单独自检，不需要 CARLA）：
    python src/eval/metrics.py --selftest

为什么单独一个文件
------------------
`configs/p1/ablation_a1_closedloop.yaml` 冻结了 primary / secondary 指标清单。指标算法
必须**与仿真解耦**，否则"两臂指标是不是同一套算法"就无法独立验证。

指标（对应协议 §metrics）
------------------------
primary   : following_rmse_m, accel_sq_integral_mps3
secondary : jerk_peak_mps3, lane_center_dev_m, steer_angle_var, collision_count, min_ttc_s

术语与口径纪律
-------------
- 跟车误差 RMSE：对"有前车"的采样点算 (gap − 期望间距) 的均方根。期望间距用**恒定车头时距**
  `d_des = v·τ + d0`（τ=1.5 s, d0=5 m）——这是显式假设，写进结果文件，不得事后改。
- 加速度平方积分与 Jerk 峰值按**时间积分/差分**算，因此依赖采样间隔，必须传 dt。
- `min_ttc_s`：TTC = gap / max(−Δv, ε)，只统计 Δv<0（接近）的样本；无接近样本时返回 None，
  **不得**填成 0 或 ∞ 蒙混。
- 一条曲线都不做插值：缺样本就少算，不猜。
"""
from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass, field

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

TAU_S = 1.5          # 期望车头时距（显式假设）
D0_M = 5.0           # 静止安全间距（显式假设）
EPS = 1e-6


@dataclass
class Trace:
    """一次闭环运行的轨迹记录（每个控制周期一条）。"""
    t: list[float] = field(default_factory=list)
    ego_speed: list[float] = field(default_factory=list)
    ego_accel: list[float] = field(default_factory=list)
    lead_gap: list[float | None] = field(default_factory=list)
    lead_speed: list[float | None] = field(default_factory=list)
    lateral_offset: list[float] = field(default_factory=list)
    steer: list[float] = field(default_factory=list)
    collision: list[bool] = field(default_factory=list)

    def push(self, st):
        """从 `carla_town04.Step` 或任何同名属性的对象追加一条。"""
        self.t.append(float(st.t))
        self.ego_speed.append(float(st.ego_speed_mps))
        self.ego_accel.append(float(st.ego_accel_mps2))
        self.lead_gap.append(None if st.lead_gap_m is None else float(st.lead_gap_m))
        ls = None
        if st.lead_gap_m is not None:
            ls = float(st.ego_speed_mps) + float(st.rel_speed_mps)
        self.lead_speed.append(ls)
        self.lateral_offset.append(float(st.lateral_offset_m))
        self.steer.append(float(st.steer))
        self.collision.append(bool(st.collision))
        return self

    def __len__(self):
        return len(self.t)


def _dt(t: list[float]) -> float:
    if len(t) < 2:
        return 0.0
    d = [b - a for a, b in zip(t, t[1:]) if b > a]
    return sum(d) / len(d) if d else 0.0


def following_rmse(tr: Trace, tau: float = TAU_S, d0: float = D0_M) -> float | None:
    """跟车误差 RMSE（仅在有前车的样本上）。无样本返回 None。"""
    errs = []
    for v, g in zip(tr.ego_speed, tr.lead_gap):
        if g is None:
            continue
        errs.append(g - (v * tau + d0))
    if not errs:
        return None
    return math.sqrt(sum(e * e for e in errs) / len(errs))


def accel_sq_integral(tr: Trace) -> float | None:
    """∫ a² dt（舒适性；越小越平顺）。"""
    dt = _dt(tr.t)
    if dt <= 0 or not tr.ego_accel:
        return None
    return sum(a * a for a in tr.ego_accel) * dt


def jerk_peak(tr: Trace) -> float | None:
    """|da/dt| 的峰值。"""
    dt = _dt(tr.t)
    if dt <= 0 or len(tr.ego_accel) < 2:
        return None
    return max(abs(b - a) / dt for a, b in zip(tr.ego_accel, tr.ego_accel[1:]))


def lane_center_dev(tr: Trace) -> float | None:
    """车道居中偏差：|横向偏差| 的均值（也报 RMS 更稳，但协议只要求偏差）。"""
    if not tr.lateral_offset:
        return None
    return sum(abs(x) for x in tr.lateral_offset) / len(tr.lateral_offset)


def steer_variance(tr: Trace) -> float | None:
    """前轮转角方差（转向抖动）。"""
    if len(tr.steer) < 2:
        return None
    m = sum(tr.steer) / len(tr.steer)
    return sum((s - m) ** 2 for s in tr.steer) / (len(tr.steer) - 1)


def min_ttc(tr: Trace) -> float | None:
    """最小 TTC（只统计接近样本 Δv<0）。无接近样本 → None（**不填 0/∞**）。"""
    vals = []
    for v, g, lv in zip(tr.ego_speed, tr.lead_gap, tr.lead_speed):
        if g is None or lv is None:
            continue
        dv = lv - v
        if dv < -EPS and g > 0:
            vals.append(g / max(-dv, EPS))
    return min(vals) if vals else None


def collision_count(tr: Trace) -> int:
    """碰撞次数（按"碰撞标志由 True→False 的上升沿"计次数，避免同一次碰撞记多帧）。"""
    n, prev = 0, False
    for c in tr.collision:
        if c and not prev:
            n += 1
        prev = c
    return n


def summarize(tr: Trace) -> dict:
    """产出协议要求的全部指标 + 支撑信息（样本量、显式假设）。"""
    return {
        "n_samples": len(tr),
        "mean_dt_s": round(_dt(tr.t), 6),
        "following_rmse_m": _r(following_rmse(tr)),
        "accel_sq_integral_mps3": _r(accel_sq_integral(tr)),
        "jerk_peak_mps3": _r(jerk_peak(tr)),
        "lane_center_dev_m": _r(lane_center_dev(tr)),
        "steer_angle_var": _r(steer_variance(tr)),
        "collision_count": collision_count(tr),
        "min_ttc_s": _r(min_ttc(tr)),
        "assumptions": {"tau_s": TAU_S, "d0_m": D0_M,
                        "note": "期望间距 d_des = v·τ + d0；该假设写死在文件里，不得事后改"},
        "n_lead_present": sum(1 for g in tr.lead_gap if g is not None),
    }


def _r(x, nd=6):
    return None if x is None else round(float(x), nd)


# ------------------------------------------------------------------ 自检
def _selftest():
    R = []

    def ck(n, ok, d):
        R.append((n, bool(ok), d))

    # 构造一条已知答案的轨迹：v=20 m/s 恒定，gap 恒为 35 m（恰好等于 20*1.5+5）
    tr = Trace()

    class S:
        pass

    for i in range(21):
        s = S()
        s.t = i * 0.05
        s.ego_speed_mps = 20.0
        s.ego_accel_mps2 = 0.0
        s.lead_gap_m = 35.0
        s.rel_speed_mps = 0.0
        s.lateral_offset_m = 0.1
        s.steer = 0.0
        s.collision = False
        tr.push(s)
    m = summarize(tr)
    ck("following_rmse_exact", abs(m["following_rmse_m"]) < 1e-9,
       "恒定间距=期望间距时 RMSE = %s（应为 0）" % m["following_rmse_m"])
    ck("accel_integral_zero", m["accel_sq_integral_mps3"] == 0.0, "恒定加速度 0 → 积分 = 0")
    ck("jerk_zero", m["jerk_peak_mps3"] == 0.0, "加速度不变 → jerk = 0")
    ck("no_approach_ttc_none", m["min_ttc_s"] is None, "无接近样本 → min_ttc 为 None（不填 0/∞）")
    ck("dt", abs(m["mean_dt_s"] - 0.05) < 1e-9, "平均 dt = %s" % m["mean_dt_s"])

    # 接近场景：gap 递减，Δv=-5 → TTC 应为 gap/5
    tr2 = Trace()
    for i in range(10):
        s = S(); s.t = i * 0.1
        s.ego_speed_mps = 20.0; s.ego_accel_mps2 = 1.0
        s.lead_gap_m = 50.0 - i * 2.0; s.rel_speed_mps = -5.0
        s.lateral_offset_m = 0.0; s.steer = 0.02; s.collision = False
        tr2.push(s)
    m2 = summarize(tr2)
    expect_ttc = (50.0 - 9 * 2.0) / 5.0       # 最后一个样本 32/5 = 6.4
    ck("ttc_value", abs(m2["min_ttc_s"] - expect_ttc) < 1e-6,
       "接近场景 min_ttc = %s（应为 %.2f）" % (m2["min_ttc_s"], expect_ttc))

    # 碰撞计数：连续 True 只算一次
    tr3 = Trace()
    for i, c in enumerate([False, True, True, True, False, True]):
        s = S(); s.t = i * 0.1
        s.ego_speed_mps = 10.0; s.ego_accel_mps2 = 0.0
        s.lead_gap_m = None; s.rel_speed_mps = 0.0
        s.lateral_offset_m = 0.0; s.steer = 0.0; s.collision = c
        tr3.push(s)
    m3 = summarize(tr3)
    ck("collision_edges", m3["collision_count"] == 2,
       "两次碰撞段（True,True,True 与 True）→ 计 %d 次（应为 2）" % m3["collision_count"])
    ck("no_lead_rmse_none", m3["following_rmse_m"] is None,
       "全程无前车 → 跟车 RMSE 为 None（不填 0 冒充）")

    print("闭环 A1 指标自检（不需要 CARLA）")
    print("")
    for n, ok, d in R:
        print("  %s %-22s %s" % ("OK  " if ok else "FAIL", n, d))
    bad = [n for n, ok, _ in R if not ok]
    print("")
    print("[metrics] %s：%d/%d" % ("全部通过" if not bad else "未过：" + ", ".join(bad),
                                   len(R) - len(bad), len(R)))
    return 0 if not bad else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    sys.exit(_selftest() if a.selftest else 0)
