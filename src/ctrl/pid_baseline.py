#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PID 跟驰基线：给 A1 提供一个**外部参照控制器**（本仓库此前完全没有）。

为什么需要它
------------
现稿只比较"OTF 开 / OTF 关"两条臂。两只臂**同一个控制器、只差一个输入**，
所以"Δcost = +0.26"到底算好还是坏，缺少外部标尺。审稿人第一个问题就是：
    "你们的复合代价 30.5 是好还是坏？跟一个朴素 PID 比呢？"
本模块提供一个**参数冻结、可解释、零训练**的 PID 跟驰控制器，用同一环境、同一指标、
同一 20 局协议跑一次，作为外部参照（**不是**要证明 PID 更优）。

控制律（单参数含义清晰）
------------------------
    d_des = s0 + h * v_ego                  # 期望车距（恒定车头时距）
    v_ref = v_ego + kp * (gap - d_des) + kd * rel_speed
    v_cmd = clip(v_ref, 0, v_max)
环境接口 `env.step_speed(target_speed_mps=...)` 接收的正是目标速度，与本输出一致。

诚实边界
--------
· 参数**未在闭环里调优**（写成常量，见下方 DEFAULT）。若审稿人要求"公平基线"，
  应另做一次参数扫描并**同时报告扫描过程**，不能只报最好的那组。
· 它是**几何跟驰**基准，不含换道、不含 OTF，因此不能用来论证 OTF 的优劣；
  它只回答"这个代价量级是否合理"。

自检（无需 CARLA）：
    py -3.12 src/ctrl/pid_baseline.py
"""
from __future__ import annotations

DEFAULT = dict(kp=0.35, kd=0.90, headway_s=1.4, s0_m=5.0, v_max_mps=33.3)


class GapPID:
    """恒定车头时距 + 速度偏差反馈的跟驰基准。"""

    def __init__(self, kp: float = DEFAULT["kp"], kd: float = DEFAULT["kd"],
                 headway_s: float = DEFAULT["headway_s"], s0_m: float = DEFAULT["s0_m"],
                 v_max_mps: float = DEFAULT["v_max_mps"]):
        self.kp, self.kd = float(kp), float(kd)
        self.headway_s, self.s0_m = float(headway_s), float(s0_m)
        self.v_max_mps = float(v_max_mps)

    def n_params(self) -> int:
        """与 CfC 策略对齐的"参数量"口径：4 个标量。"""
        return 4

    def desired_gap(self, v_ego: float) -> float:
        return self.s0_m + self.headway_s * max(0.0, v_ego)

    def target_speed(self, gap_m: float, rel_speed_mps: float, v_ego_mps: float) -> float:
        d_des = self.desired_gap(v_ego_mps)
        v_ref = v_ego_mps + self.kp * (gap_m - d_des) + self.kd * rel_speed_mps
        return float(min(self.v_max_mps, max(0.0, v_ref)))

    def act(self, obs) -> float:
        """与 `controller_obs` 对齐：obs = [gap, rel_speed, v_ego] 或 [gap, rel_speed, v_ego, phi]。"""
        return self.target_speed(float(obs[0]), float(obs[1]), float(obs[2]))


def _selftest() -> int:
    pid = GapPID()
    ok = True
    cases = [
        # (gap, rel, v_ego, 期望方向, 说明)
        (60.0, 0.0, 25.0, "高", "车距远大于期望 → 目标速度应接近/达到上限"),
        (10.0, 0.0, 25.0, "低", "车距远小于期望 → 目标速度应低于自车速度"),
        (40.0, 5.0, 25.0, "偏高", "前车更快 → 比同样车距但 rel=0 时更高"),
    ]
    base = pid.target_speed(40.0, 0.0, 25.0)
    got = [pid.target_speed(g, r, v) for g, r, v, _, _ in cases]
    print("  用例：", [(c[4], round(v, 2)) for c, v in zip(cases, got)])
    if not (got[0] > 30.0):
        print("  ✗ 车距大时目标速度不够高"); ok = False
    if not (got[1] < 25.0):
        print("  ✗ 车距小时目标速度未降低"); ok = False
    if not (got[2] > base):
        print("  ✗ 前车更快时目标速度未提高"); ok = False
    if not all(0.0 <= x <= pid.v_max_mps for x in got):
        print("  ✗ 输出越界"); ok = False
    if pid.n_params() != 4:
        print("  ✗ 参数量口径不一致"); ok = False
    print("  自检：", "全部通过" if ok else "有失败")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(_selftest())
