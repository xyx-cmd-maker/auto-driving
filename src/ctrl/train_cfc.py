#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""闭环 A1 执行器：两臂（Φ_OTF 开/关）同种子、同预算、同 rollout 条件。

用法（**必须 Python 3.12**，CARLA wheel 只有 cp312）：
    py -3.12 src/ctrl/train_cfc.py --smoke                      # 冒烟：1 场景 × 1 种子
    py -3.12 src/ctrl/train_cfc.py --scenarios none,cutin --seeds 0,1 --resume
    py -3.12 src/ctrl/train_cfc.py --analyze                    # 只做配对统计，不跑仿真

为什么用"固定协议策略搜索"而不是 PPO/TD3
----------------------------------------
A1 要回答的是"**把 Φ_OTF 加进控制器输入，控制性能是否更好**"，**不是**"哪个 RL 算法更强"。
若用 PPO/TD3 训练，两臂的差异会同时混入"两臂各自训练收敛到不同局部最优"的噪声，
届时无法把结果归因到 OTF。因此本执行器采用**受控的策略搜索**：
  · 策略 = CfCCell 参数（两臂结构完全相同，只差输入维度）
  · 搜索 = 固定候选数 K 的随机搜索 + 精英保留，两臂 **K 相同、随机种子组相同**
  · 每个候选在**同一组**初始条件与同一组交通流种子下评估
  · 最终用**同种子配对比较**（协议 statistics.primary_test）
这样两臂的唯一系统性差异就是输入集本身。搜索规模小、可复现，适合先给出 A1 的诚实答案；
若日后要用 RL 训练，属于另一条实验线（需另立协议），不混入本次对比。

诚实标注（写在此处而非事后补）
-----------------------------
1. **偏离协议的控制频率**：CARLA 在 Python 侧达不到 100 Hz。协议写 100 Hz；本执行器用
   `sim_hz` / `control_hz`（默认 50 / 20 Hz）并**如实记录**（`actual_control_hz`），
   不得对外写成 100 Hz。
2. 混行程度用 Traffic Manager 全局速度差近似，不区分驾驶风格分布。
3. 场景注入用 CARLA 原生 API 直接操纵车辆，不是脚本化场景引擎；注入强度需实测标定。

三条看护（用户要求）
-------------------
  G1 多 episode 连续 reset 稳定性：记录每次 reset 耗时，超阈值或异常即标记
  G2 actor 泄漏：每 episode 记录场上 actor 数，单调增长即报警
  G3 拥塞死锁：统计"长时间零速车辆占比"，超阈值即标记该 episode

★★ 已知阻塞：本执行器目前**还跑不出有效结论**，两个前置必须先在环境侧解决 ★★
--------------------------------------------------------------------------------
阻塞 1：**ego 无法维持速度**（环境缺陷，非控制器问题）
    实测：给 0.2 m/s² 的恒定命令，ego 加速到约 1.7 m/s 后在 40 s 内**停到 0.10 m/s**，
    前车距离从 50.9 m 一路拉到 131 m 直至丢失前车。满油门（诊断脚本）能到 6.33 m/s，
    说明车本身没问题——是 `Town04Env.step()` 的加速度→油门映射不自洽
    （前馈分母 A_MAX 与实际动力学不匹配、且与 `_measured_accel` 的反馈项相互抵消）。
    后果：控制器学不到跟车行为，A1 对比失去意义。
    修法：改为"目标速度 PI + 加速度前馈"，并加一条**速度保持自检**
    （固定命令下速度的标准差应小于某阈值），自检不过不许开跑 A1。

阻塞 2：**Φ_OTF 在闭环中恒为 0**（实测 1500 个采样点全为 0）
    OTF 的触发条件是"相邻车道发生超车/被超车事件"（5 秒时间窗）。混行流用 Traffic Manager
    自动生成、各车速度相近，60–120 秒内不发生超车事件。**两个后果**：
      · a1_otf_on 的第 4 个输入恒为 0 ⇒ 它的策略退化为等价于 a1_otf_off 的策略
        （同 seed 下 4 维策略的前 3 维贡献与 3 维策略**逐位相同**），
        因此两臂轨迹与指标**逐位相同、Δ 恒等于 0**——这是"无 OTF 信号"的如实反映，
        **不是**"OTF 无用"的证据。**不得据此写任何结论。**
    修法（任一）：① 交通流改成"有明确速度差 + 换道意图"的混行（让超车事件真的发生）；
    ② 把 OTF 的判定改成不依赖超车事件（如邻车道相对速度累积量），并同步改信息量版口径；
    ③ 场景注入主动制造超车（cutin/lead-exit 已具备该能力，需延长局时并提高注入密度）。
    在此之前，A1 闭环**不得开跑全量**，更不得报告结果。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import sys
import time

# ★ BLAS / OpenMP 线程数上限（2026-10-17 修复）。
# 触发条件：本机 15.7 GB 内存，CARLA 的 Shipping 进程独占约 6.8 GB，
# 剩余不足 1 GB 时 OpenBLAS 报 "Memory allocation still failed after 10 retries"。
# OpenBLAS 默认按核数（24 线程）各分配工作缓冲，峰值内存被放大数倍。
# 本项目**只用 numpy 做小数组统计**（几十个标量），单线程完全够用，因此强制 1。
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np
import torch

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, os.path.abspath(os.path.join(_HERE, "..", "envs")),
           os.path.abspath(os.path.join(_HERE, "..", "eval")),
           os.path.abspath(os.path.join(_HERE, "..", "otf"))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from cfc import CfCCell, count_params          # noqa: E402
from metrics import Trace, summarize           # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
RESULTS = os.path.join(ROOT, "results", "p1")
# ★ 运行产物默认写在**仓库内** `runs/p1`（2026-10-17 改）。
# 早期默认 `F:\p1_runs`（移动 SSD），理由是想让"会增长的产物"远离仓库；但实测 F: 会掉线，
# 2026-10-13 的 4 局 A1 结果因此在盘符消失后**不可访问**（教训见 AGENTS-LESSONS.md P9 同类）。
# 而本项目单局结果只有 ~3 KB，放进仓库毫无压力；且项目铁律要求"结果唯一来源 = results/ 下可追溯"。
# 因此：**结果一律进仓库**；只有真正的大文件（checkpoint、原始轨迹）才用 P1_RUNS_DIR 外置。
RUNS = os.environ.get("P1_RUNS_DIR", os.path.join(ROOT, "runs", "p1"))

ARMS = ("a1_otf_off", "a1_otf_on")
USE_OTF = {"a1_otf_off": False, "a1_otf_on": True}
SEARCH_K = 12          # 每臂候选策略数（两臂必须相同）
ELITE = 3              # 精英保留数
EPISODE_S = 60.0       # 每个候选的 rollout 时长


# --------------------------------------------------------------- 策略
class CFCPolicy(torch.nn.Module):
    """CfC 控制器：观测 → 目标加速度（**直接通路 + CfC 记忆**）。

    为什么必须有直接通路（三轮调试的结论）
    ------------------------------------
    CfC 的隐状态是**慢变量**：h ← f·g·dt + h·(1−f·g)，在 dt=0.05 时每个控制步只更新很小
    一部分，隐状态实际上是一个低通滤波器。若动作只从隐状态读出，策略对**当前**观测几乎
    无响应（实测极差 0.0009 m/s²），无法驱动被控对象——12 个候选退化成同一个常数控制器。
    因此这里加一条 `act` 直接通路（当前观测线性映射），CfC 隐状态提供记忆/平滑项。
    这仍是一个 CfC 控制器（记忆由 CfC 承担），但动作对当前状态可响应。

    参数初始化尺度同样经过实测标定：
      · 单元内部 U(±0.1/√fan_in)：太大（±1/√fan_in）会让门控 sigmoid 饱和、隐状态冻结
      · 输出层 U(±1)：CfC 隐状态数值接近 0.5，权重太小则输出只有 O(0.05) m/s²
    """

    def __init__(self, obs_dim: int, hidden: int = 24, out_scale: float = 3.0):
        super().__init__()
        self.cell = CfCCell(input_dim=obs_dim, hidden_dim=hidden)
        self.act = torch.nn.Linear(obs_dim, 1)        # 直接通路：对当前观测即时响应
        self.head = torch.nn.Linear(hidden, 1)        # 记忆通路：CfC 隐状态
        torch.nn.init.uniform_(self.act.weight, -2.0, 2.0)
        torch.nn.init.zeros_(self.act.bias)
        torch.nn.init.uniform_(self.head.weight, -1.0, 1.0)
        torch.nn.init.zeros_(self.head.bias)
        self.hidden = hidden
        self.out_scale = out_scale

    def forward(self, obs_seq: torch.Tensor) -> torch.Tensor:
        h = torch.zeros(1, self.hidden)
        outs = []
        for t in range(obs_seq.shape[0]):
            x = obs_seq[t:t + 1]
            h = self.cell(x, h, 0.05)
            outs.append(torch.tanh(self.act(x) + self.head(h)) * self.out_scale)
        return torch.cat(outs)

    def n_params(self) -> int:
        return count_params(self)


def sample_policy(obs_dim: int, rng: random.Random, hidden: int = 24) -> CFCPolicy:
    """按给定 rng 采一组策略参数（两臂用**同一组** rng 种子，保证搜索预算相同）。

    初始化尺度必须让策略"使得上劲"：实测 U(-0.1,0.1)+零偏置时输出仅 ±0.04 m/s²，
    等效 1.3% 油门 ⇒ 候选之间无差异。这里把 head 权重放大到 U(±1/√hidden)，
    并对 CfC 单元的 fc 层同样放大，使输出能覆盖 ±3 m/s² 的有效区间。
    """
    torch.manual_seed(rng.randrange(1 << 30))
    p = CFCPolicy(obs_dim, hidden=hidden)
    with torch.no_grad():
        # 单元内部用**小尺度**：U(±0.1/√fan_in)。早期试过 ±1/√fan_in，结果门控 sigmoid
        # 直接饱和（预激活 O(±10)）→ 隐状态被冻结在 0.5、候选之间无差异。
        # 小尺度让门控留在工作区（预激活 O(±1)），策略输出才有随输入变化的自由度。
        for m in p.cell.modules():
            if isinstance(m, torch.nn.Linear):
                k = 0.1 / math.sqrt(m.in_features)
                m.weight.uniform_(-k, k)
                m.bias.uniform_(-0.05, 0.05)      # 小偏置：避免所有单元开局同相
    return p


OBS_NORM = {
    # 观测归一化：把量纲拉到 O(1)，否则 gap（几十到几百米）会主导而未归一化的
    # Φ_OTF（次/秒，O(0.1)）在数值上被淹没——那会让 a1_otf_on 实际上"看不见"OTF，
    # 结论会假阴性。归一化用的常数是**固定的物理参考值**，两臂完全相同。
    "gap": 100.0, "rel_speed": 10.0, "ego_speed": 30.0, "phi_otf": 1.0,
}
OBS_KEYS_ON = ("gap", "rel_speed", "ego_speed", "phi_otf")
OBS_KEYS_OFF = ("gap", "rel_speed", "ego_speed")


def normalize_obs(obs: list, use_otf: bool) -> list:
    keys = OBS_KEYS_ON if use_otf else OBS_KEYS_OFF
    return [obs[i] / OBS_NORM[k] for i, k in enumerate(keys)]


# --------------------------------------------------------------- rollout
def rollout(env, policy: CFCPolicy, use_otf: bool, scenario: str, seed: int,
            episode_s: float = EPISODE_S):
    """在环境里跑一局；策略只用 controller_obs（两臂输入集只差 Φ_OTF）。"""
    st = env.reset(scenario=scenario, seed=seed)
    tr = Trace()
    tr.push(st)
    # 先把观测收集成序列再前向（CfC 是递归的；这里按步前向即可，序列形式仅便于接口统一）
    obs_dim = len(st.controller_obs(use_otf))
    h_state = torch.zeros(1, policy.hidden)
    guard = {"zero_speed_frames": 0, "n_frames": 0, "actors_max": 0, "ttc_events": 0}
    p_start = env.ego.get_transform().location
    travelled = 0.0
    n = int(episode_s / (env.dt * env.ctrl_every))
    for _ in range(n):
        obs = st.controller_obs(use_otf)
        if len(obs) != obs_dim:
            raise RuntimeError("观测维度在局内变化：%d → %d（会破坏两臂可比性）"
                               % (obs_dim, len(obs)))
        with torch.no_grad():
            x = torch.tensor([normalize_obs(obs, use_otf)], dtype=torch.float32)
            h_state = policy.cell(x, h_state, 0.05)
            accel = float(torch.tanh(policy.act(x) + policy.head(h_state)) * policy.out_scale)
        st = env.step_speed(target_speed_mps=max(0.0, accel))
        tr.push(st)
        guard["n_frames"] += 1
        # ★ 处理变量激活率（AGENTS-LESSONS.md §3 列为"高"优先级强制项）：
        # "无差异"结论只有在**处理变量确实被激活过**时才成立。若 Φ_OTF 全程为 0，
        # 则 a1_otf_on 的第 4 维输入恒为零、策略退化为与 a1_otf_off 逐位等价，
        # Δ=0 只是"没有信号"而非"没有效果"——2026-10-11 已踩过一次，此处强制记录。
        if use_otf:
            guard["phi_nonzero_frames"] = guard.get("phi_nonzero_frames", 0) + (
                1 if abs(st.phi_otf) > 1e-12 else 0)
        if st.ego_speed_mps < 0.1:
            guard["zero_speed_frames"] += 1
        guard["actors_max"] = max(guard["actors_max"],
                                  len(env.world.get_actors().filter("vehicle.*")))
        if st.lead_gap_m is not None and st.rel_speed_mps < -0.1 and st.lead_gap_m > 0:
            guard["ttc_events"] += 1
        if st.meta.get("done"):
            break
    p_end = env.ego.get_transform().location
    travelled = ((p_end.x - p_start.x) ** 2 + (p_end.y - p_start.y) ** 2) ** 0.5

    # ★ 守门 G0：ego 必须真的动起来。
    # 教训（2026-10-13）：a1_otf_on 的某局有 99% 的帧车速为 0（残留车把它卡住），
    # 该局指标毫无意义，却会被当成"这一臂更差"的证据混进结果。宁可丢弃也不能污染。
    guard["travelled_m"] = round(travelled, 3)
    if use_otf:
        nzf = guard.get("phi_nonzero_frames", 0)
        guard["phi_nonzero_ratio"] = round(nzf / max(guard["n_frames"], 1), 6)
    guard["valid"] = bool(travelled > 20.0 or guard["n_frames"] == 0)
    if not guard["valid"]:
        guard["invalid_reason"] = ("ego 仅移动 %.1f m（阈值 20 m）——疑似被残留车辆/几何卡住，"
                                   "该局指标不可用" % travelled)
    if getattr(env, "_residue_warn", None):
        guard["valid"] = False
        guard["invalid_reason"] = ("reset 后场上车辆数 %d 远多于生成数 %d——残留未清"
                                   % env._residue_warn)
    return tr, guard


def cost_from_metrics(m: dict) -> float:
    """候选策略的代价（越小越好）。权重写死在此处，两臂相同。

    ⚠️ 各项必须**量纲可比**。初版直接用原始量纲，结果 accel_sq_integral 达 166、
    jerk 达 1571，把跟车误差（O(10)）完全压住，代价被舒适性项独占、跟车性能失去区分度。
    这里把各项除以其**物理参考量级**（写死的常数，两臂相同），使每项都是 O(1) 量级。
    """
    c = 0.0
    c += 1.0 * (m["following_rmse_m"] if m["following_rmse_m"] is not None else 10.0) / 10.0
    c += 1.0 * (m["accel_sq_integral_mps3"] or 0.0) / 50.0            # 参考量级 50
    c += 0.5 * (m["jerk_peak_mps3"] or 0.0) / 50.0                    # 参考量级 50
    c += 0.5 * (m["lane_center_dev_m"] or 0.0) / 0.5                  # 参考量级 0.5 m
    c += 10.0 * m["collision_count"]                                  # 硬约束
    return c


# --------------------------------------------------------------- 单 (场景,种子) 一次完整对比
def run_case(scenario: str, seed: int, args) -> dict:
    from carla_town04 import Town04Env

    out = {"scenario": scenario, "seed": seed, "arms": {}, "guards": {}}
    env = Town04Env(n_traffic=args.traffic, sim_hz=args.sim_hz,
                    control_hz=args.control_hz, max_episode_s=args.episode_s,
                    verbose=False)

    # 两臂共用同一组随机种子（协议 fairness.same_map_and_seeds + same_training_episodes）
    master = random.Random(1000 + seed)
    seed_list = [master.randrange(1 << 30) for _ in range(SEARCH_K)]

    for arm in ARMS:
        use_otf = USE_OTF[arm]
        t0 = time.perf_counter()
        trials = []
        for k, s in enumerate(seed_list):
            policy = sample_policy(4 if use_otf else 3, random.Random(s), hidden=args.hidden)
            tr, guard = rollout(env, policy, use_otf, scenario, seed, args.episode_s)
            m = summarize(tr)
            # 无效局（ego 被卡住/有残留）不参与择优——否则会把"环境故障"读成"该臂更差"
            trials.append({"k": k, "seed": s, "cost": cost_from_metrics(m), "metrics": m,
                           "guard": guard, "params": policy.n_params(),
                           "valid": guard.get("valid", True)})
        # ★ 逐候选记录（含有效性掩码）——**必须落盘**。
        # 教训（2026-10-17）：初版只存 all_costs 与 n_invalid，导致无法离线审计
        # "哪些候选无效"。而无效局（车没动）的代价**可能低于**有效局，因为代价里
        # "跟车误差 None → 占位 10.0"、车不动时其余项都很小 ⇒ **绝不能靠代价大小判断有效性**。
        # 因此这里显式保存每个候选的 {k, seed, cost, valid, reason, travelled_m}。
        valid_trials = [t for t in trials if t["valid"]]
        n_valid = len(valid_trials)
        out["arms"][arm] = {
            "n_valid": n_valid,
            "invalid_ratio": round(1.0 - n_valid / max(len(trials), 1), 4),
            "candidates": [{"k": t["k"], "seed": t["seed"], "cost": round(t["cost"], 6),
                            "valid": t["valid"],
                            "travelled_m": t["guard"].get("travelled_m"),
                            "invalid_reason": t["guard"].get("invalid_reason")}
                           for t in sorted(trials, key=lambda x: x["k"])],
            # 处理变量激活率取**各候选的最大值**（不是第一个候选）：
            # 早期版本取 next(...)，若恰好撞上"ego 被卡住"的无效候选就会报 0，
            # 掩盖"其它候选其实激活了"的事实（2026-10-18 修）。
            "phi_nonzero_ratio": (max((t["guard"].get("phi_nonzero_ratio") or 0.0)
                                      for t in trials) if use_otf else None),
        }
        # 择优仅用有效候选；全部无效时保守回退到全部（并在 paired 里标注）
        pool = valid_trials or trials
        pool.sort(key=lambda x: x["cost"])
        best = pool[0]
        out["arms"][arm].update({
            "best_cost": best["cost"], "best_metrics": best["metrics"],
            "best_seed": best["seed"], "params": best["params"],
            "elite_costs": [t["cost"] for t in pool[:ELITE]],
            "all_costs": [t["cost"] for t in trials],
            "n_invalid": sum(1 for t in trials if not t["valid"]),
            "wall_s": round(time.perf_counter() - t0, 1),
            # 最优候选自身的激活率（此时 best 已确定；早期误放在 best 之前，
            # 导致第二臂读到的是上一臂的 guard，值为 None）
            "phi_nonzero_ratio_of_best": (best["guard"].get("phi_nonzero_ratio")
                                          if use_otf else None),
        })
        out["guards"][arm] = best["guard"]
    env.close()

    # ★ 等 K 配对（2026-10-17 新增）：两臂的有效候选数往往不等（实测 on 臂更容易把车开死），
    # 若各取"各自最好的一个"，那么**候选池更大的一方天然占优**——这是选择偏倚，不是算法差异。
    # 因此在 K = min(n_valid_off, n_valid_on) 上另算一套配对结果（取各臂前 K 个有效候选的均值），
    # 与"各取最好"的原始口径**同时报告**，让读者自己看到差异来源。
    def _valid_costs(arm):
        return sorted(c["cost"] for c in out["arms"][arm]["candidates"] if c["valid"])

    off_v, on_v = _valid_costs("a1_otf_off"), _valid_costs("a1_otf_on")
    k_eq = min(len(off_v), len(on_v))
    eq = None
    if k_eq >= 1:
        eq = {
            "k": k_eq,
            "delta_cost": round(sum(on_v[:k_eq]) / k_eq - sum(off_v[:k_eq]) / k_eq, 6),
            "n_valid_off": len(off_v), "n_valid_on": len(on_v),
            "invalid_ratio_off": out["arms"]["a1_otf_off"]["invalid_ratio"],
            "invalid_ratio_on": out["arms"]["a1_otf_on"]["invalid_ratio"],
            "caveat": ("等 K 消除了'候选池大小'带来的选择偏倚，但**不消除**两臂产生有效候选能力的"
                       "真实差异；后者作为'训练难度'证据单独报告，不得隐去"),
        }
    out["paired"] = {
        "delta_following_rmse": _d(out, "following_rmse_m"),
        "delta_accel_sq_integral": _d(out, "accel_sq_integral_mps3"),
        "delta_collision": (out["arms"]["a1_otf_on"]["best_metrics"]["collision_count"]
                            - out["arms"]["a1_otf_off"]["best_metrics"]["collision_count"]),
        "delta_cost": out["arms"]["a1_otf_on"]["best_cost"] - out["arms"]["a1_otf_off"]["best_cost"],
        "mask": "best_cost 口径（各取各自最好有效候选）",
        "equal_k": eq,
    }
    return out


def _d(out, key):
    a = out["arms"]["a1_otf_off"]["best_metrics"].get(key)
    b = out["arms"]["a1_otf_on"]["best_metrics"].get(key)
    return None if (a is None or b is None) else round(b - a, 6)


# --------------------------------------------------------------- 落盘 / 续跑
def case_path(scenario, seed):
    return os.path.join(RUNS, "cases", "case_%s_s%d.json" % (scenario, seed))


def save_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, path)          # 原子替换：中断不会留下半个文件


def load_case(scenario, seed):
    p = case_path(scenario, seed)
    if os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            return None
    return None


# --------------------------------------------------------------- 主流程
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenarios", default="none,cutin,lead-brake,lead-exit")
    ap.add_argument("--seeds", default="0,1,2,3,4")
    ap.add_argument("--traffic", type=int, default=30)
    ap.add_argument("--sim-hz", type=float, default=50.0)
    ap.add_argument("--control-hz", type=float, default=20.0)
    ap.add_argument("--episode-s", type=float, default=EPISODE_S)
    ap.add_argument("--hidden", type=int, default=24)
    ap.add_argument("--resume", action="store_true", help="跳过已有结果的 (场景,种子)")
    ap.add_argument("--smoke", action="store_true", help="冒烟：1 场景 × 1 种子")
    ap.add_argument("--analyze", action="store_true", help="只做配对统计")
    args = ap.parse_args()

    if args.smoke:
        args.scenarios, args.seeds, args.episode_s = "none", "0", 30.0
    scenarios = [s.strip() for s in args.scenarios.split(",") if s.strip()]
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]

    os.makedirs(RUNS, exist_ok=True)
    print("闭环 A1 执行器")
    print("  场景 %s ｜ 种子 %s ｜ 候选数/臂 %d ｜ 每局 %.0f s ｜ 控制频率 %.0f Hz（仿真 %.0f Hz）"
          % (scenarios, seeds, SEARCH_K, args.episode_s, args.control_hz, args.sim_hz))
    print("  产物目录 %s（仓库内只留 %s 下的小 JSON）" % (RUNS, os.path.relpath(RESULTS, ROOT)))
    print("  ⚠ 协议写 100 Hz；本机实测无法达到，实际为 %.0f Hz——对外必须按实际值报告"
          % args.control_hz)
    print("")

    if args.analyze:
        return analyze(scenarios, seeds)

    done, skipped, failed = 0, 0, []
    for sc in scenarios:
        for sd in seeds:
            if args.resume and load_case(sc, sd) is not None:
                skipped += 1
                print("  [resume] 跳过已完成 %s/s%d" % (sc, sd))
                continue
            t0 = time.perf_counter()
            try:
                case = run_case(sc, sd, args)
            except Exception as exc:
                failed.append("%s/s%d: %s" % (sc, sd, exc))
                print("  [FAIL] %s/s%d → %s" % (sc, sd, exc))
                continue
            save_json(case_path(sc, sd), case)
            done += 1
            p = case["paired"]
            eq = p.get("equal_k") or {}
            print("  %s/s%d  Δcost(best)=%+.3f ｜ Δcost(等K=%s)=%s ｜ 跟车 Δ=%s ｜ 碰撞 Δ=%+d ｜ %.0f s"
                  % (sc, sd, p["delta_cost"], eq.get("k"),
                     ("%+.3f" % eq["delta_cost"]) if eq.get("delta_cost") is not None else "n/a",
                     ("%+.3f" % p["delta_following_rmse"]) if p["delta_following_rmse"] is not None else "n/a",
                     p["delta_collision"], time.perf_counter() - t0))

    print("")
    print("完成 %d 个 (场景,种子)；跳过 %d；失败 %d" % (done, skipped, len(failed)))
    for f in failed:
        print("  ✗ " + f)

    # 三条看护汇总
    print("")
    print("=== 看护检查 ===")
    g1 = g3 = 0
    bad = 0
    phi_ratios = []
    for sc in scenarios:
        for sd in seeds:
            c = load_case(sc, sd)
            if not c:
                continue
            for arm, g in c["guards"].items():
                if g["n_frames"] == 0:
                    g1 += 1
                if g["zero_speed_frames"] > 0.5 * max(g["n_frames"], 1):
                    g3 += 1
                if not g.get("valid", True):
                    bad += 1
            pr = c["arms"]["a1_otf_on"].get("phi_nonzero_ratio")
            if pr is not None:
                phi_ratios.append(pr)
    print("  G1 空 episode（reset 异常）: %d" % g1)
    print("  G2 actor 泄漏: 见每局 guards.actors_max（应稳定在生成数+ego 附近）")
    print("  G3 疑似拥塞/死锁 episode: %d" % g3)
    print("  G0 无效(被卡住)的择优结果: %d" % bad)
    if phi_ratios:
        print("  ★ 处理变量激活率 Φ_OTF≠0 的帧占比（on 臂，各局）: %s"
              % [round(r, 4) for r in phi_ratios])
        if max(phi_ratios) <= 1e-9:
            print("    ⚠️ **Φ_OTF 全程为 0**：on 臂第 4 维输入恒零、策略与 off 臂逐位等价。")
            print("       因此**任何'无差异'结论都不能成立**——这是'没有信号'，不是'没有效果'。")
    print("")
    print("下一步：py -3.12 src/ctrl/train_cfc.py --analyze")
    # 有失败必须反映到退出码：否则冒烟"看起来通过"而实际什么都没跑（本轮就踩过：
    # CARLA 服务端未启动 → 全部 FAIL，但退出码仍为 0）。
    return 1 if failed else 0


def analyze(scenarios, seeds):
    """跨 (场景,种子) 的配对统计：协议要求 primary 指标做配对比较并报 CI。"""
    cases = []
    for sc in scenarios:
        for sd in seeds:
            c = load_case(sc, sd)
            if c:
                cases.append(c)
    if not cases:
        print("没有可分析的结果（先跑训练）")
        return 2
    print("配对分析：%d 个 (场景,种子)" % len(cases))
    if len(cases) < 5:
        print("  ⚠️ n=%d < 5：**不足以做任何统计推断**。下面只列原始差值，"
              "不得报 CI、不得写'显著'或'无差异'（协议要求种子 ≥5）。" % len(cases))
    for key in ("delta_cost", "delta_following_rmse", "delta_accel_sq_integral", "delta_collision"):
        vals = [c["paired"][key] for c in cases if c["paired"].get(key) is not None]
        if not vals:
            print("  %-28s 无有效配对" % key)
            continue
        arr = np.array(vals, dtype=float)
        n = len(arr)
        mean = float(arr.mean())
        if n < 5:
            # n<5 时禁止输出区间：t/正态近似都无意义，且点估计的"区间"会假装成 CI。
            print("  %-28s n=%d ｜ 各值 %s ｜ 均值 %+.4f（**样本不足，不报区间**）"
                  % (key, n, [round(float(v), 4) for v in arr], mean))
            continue
        sd_ = float(arr.std(ddof=1))
        se = sd_ / math.sqrt(n)
        ci = (mean - 1.96 * se, mean + 1.96 * se)
        sign = "OTF 更好" if mean < 0 else ("OTF 更差" if mean > 0 else "无差异")
        print("  %-28s 均值 %+.4f ｜ 95%%CI [%+.4f, %+.4f] ｜ n=%d ｜ %s"
              % (key, mean, ci[0], ci[1], n, sign))
    print("")
    print("判读纪律（AGENTS.md §1 铁律 2）：若区间跨 0，**不得**写成'无差异'，")
    print("  必须用等价/非劣检验；样本量不足时只能写'未检出差异'。")

    # ---- 等 K 配对（消除"候选池大小"带来的选择偏倚）----
    eq_vals = [c["paired"]["equal_k"]["delta_cost"] for c in cases
               if isinstance(c["paired"].get("equal_k"), dict)
               and c["paired"]["equal_k"].get("delta_cost") is not None]
    print("")
    print("=== 等 K 配对（两臂各取相同数量 K 个有效候选的均值差）===")
    if eq_vals:
        ks = [c["paired"]["equal_k"]["k"] for c in cases if c["paired"].get("equal_k")]
        print("  各局 K = %s ｜ Δcost 各值 %s ｜ 均值 %+.4f"
              % (ks, [round(v, 4) for v in eq_vals], sum(eq_vals) / len(eq_vals)))
    else:
        print("  无 equal_k 数据（结果来自旧版本，需重跑）")

    # ---- 处理变量激活率（"无差异"结论的前提）----
    prs = [c["arms"]["a1_otf_on"].get("phi_nonzero_ratio") for c in cases
           if c["arms"]["a1_otf_on"].get("phi_nonzero_ratio") is not None]
    print("")
    print("=== 处理变量激活率（Φ_OTF ≠ 0 的帧占比，on 臂）===")
    if prs:
        print("  各局 %s ｜ 最大 %.4f" % ([round(p, 4) for p in prs], max(prs)))
        if max(prs) <= 1e-9:
            print("  ⚠️ **全程为 0**：on 臂第 4 维输入恒零 ⇒ 与 off 臂逐位等价。")
            print("     **不得**据此写'OTF 无效果'——这是'没有信号'。")
        elif max(prs) < 0.05:
            print("  ⚠️ 激活率 <5%：信号稀疏，效应量估计不稳定，需在 Limitations 声明。")
        else:
            print("  信号已激活，'有/无差异'的判定具备前提。")
    else:
        print("  无数据（旧版本结果或未跑 on 臂）")

    # ---- 两臂无效比例（训练难度证据，不隐去）----
    print("")
    print("=== 无效候选比例（作为'训练难度'证据，**不得隐去**）===")
    for c in cases:
        off = c["arms"]["a1_otf_off"]
        on = c["arms"]["a1_otf_on"]
        print("  %-16s off 无效 %.0f%%（%d/%d）｜ on 无效 %.0f%%（%d/%d）"
              % (c["scenario"] + "/s%d" % c["seed"],
                 100 * off.get("invalid_ratio", 0), off.get("n_invalid", 0), len(off["all_costs"]),
                 100 * on.get("invalid_ratio", 0), on.get("n_invalid", 0), len(on["all_costs"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
