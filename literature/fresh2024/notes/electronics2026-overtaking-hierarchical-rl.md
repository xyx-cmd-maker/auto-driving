# 高速公路超车的分层强化学习决策与控制（PPO 1 Hz ＋ TD3-LSTM 10 Hz）｜Large Autonomous Driving Overtaking Decision and Control System Based on Hierarchical Reinforcement Learning

- **出处**：Electronics **2026, 15(8):1711**（MDPI；Received 8 March 2026 / Revised 14 April 2026 / Accepted 14 April 2026 / Published 17 April 2026）｜ **类型**：期刊论文（Article，MDPI 开放同行评议；正文自述 "in accordance with the reviewers' comments"）
- **作者**：Chen-Ning Wang, Xiuhui Tang（**n=2**；School of Electrical and Information Engineering, Wuhan Institute of Technology）
- **DOI**：10.3390/electronics15081711（逐字；每页页脚复现）
- **全文来源**：`literature/fulltext/fresh2024/electronics2026-overtaking-hrl__53508599.txt`（PAGES=22, CHARS=68,789 为题面给定值；**本机实测**：总字符 70,329（含 CRLF）／去换行 67,441，LINES=1,444，PAGE 分隔符 22 个）｜ **材料版本**：**出版社正式版（VoR）**。逐字证据：① "Copyright: © 2026 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license."；② 每页页脚逐字 "Electronics 2026, 15, 1711" + "N of 22" + "https://doi.org/10.3390/electronics15081711"；③ 无 "Accepted Manuscript"／"author's version"／"preprint" 字样。【确定】
- **分组**：2024+ 增量
- **证据等级初判**：**C 级** — 纯软件在环（SIL）仿真闭环 + 5 条基线对照 + 5 个随机种子 + 报 mean±SD，但**无显著性检验、无置信区间、无效应量、无代码/数据**，且 Abstract 的四个标志性数字（98.3%／0.6%／0.2 m／5 m）**在全文任何表格与正文中均查不到**（见 §8 与 ⚠内部不一致 1）。按铁律 1，"有统计检验与效应量"未达成，"内部独立重复"未达成 → 不能进 B。**【确定】**
- **档位建议**：**B（略读）** — 加权 14 恰好触及 A 档门槛（≥14 且 D1=2 且 D5≥1），但建议按 B 记录：① 母协议 §4 的 A 档预算（5 篇）已满；② 与 P1 的可对标性集中在"分层频率解耦 + 闭环评价协议"两点，本卡已把这两点抽干；③ 其内部数字冲突使其**不适合作为任何定量引用来源**。**【判断，非协议机械结论】**
- **五维打分（各维 0–2，满分 20）**：D1=2 D2=1 D3=1 D4=2 D5=1 → 加权 = 3·2+2·1+2·1+1·2+2·1 = 6+2+2+2+2 = **14**
  - D1=2：**同 ODD（高速公路、多车道、人工与自动混行）**，且直接给出 P1 相邻的"超车决策"环节与**可复用的闭环评价协议**（1000 场景蒙特卡洛 + 成功率/碰撞率/超时率三分量）。不给编队跟车控制，故不构成对 P1 RQ 的直接回答，但按母协议 §5 的 D1=2 定义（同 ODD 下的闭环控制评价协议、数字或协议可被 A1–A5 消融对标或复用）判 2。
  - D2=1：有对照（5 条基线）与多场景闭环，但**无任何假设检验**（只有 mean±SD）；且纯 SIL，无实车。**与 `meeting2/notes/scirebotics2023-chahine-lnn-flight.md` 给 D2=2 的口径差异是刻意的**：那一篇有真机闭环，本篇只有仿真。
  - D3=1：超参数表（Table 1）、奖励权重、场景配置、基线定义全部印在文中，仿真平台 highway-env 开源 → 协议可部分迁移；但**无代码、无数据、无种子清单**。
  - D4=2：2026 年发表，≤5 年。
  - D5=1：全文 22 页 + 结果数字齐全（Table 2/3），但无效应量、无 CI、无检验、无可复现材料，且摘要数字不可追溯。**D4 一律指时效性。**

## 1. 标题

原文标题（逐字）：**Large Autonomous Driving Overtaking Decision and Control System Based on Hierarchical Reinforcement Learning** ｜ 中文直译：**基于分层强化学习的大型自动驾驶超车决策与控制系统**

## 2. 摘要（≤400 字）

作者用**异构频率双层架构**解耦超车：**上层 PPO 以 1 Hz 输出 5 个离散动作**，**下层 TD3+LSTM 以 10 Hz 出连续转向与加速度**，上层意图作下层条件输入。状态只保留"关键交互车"（同车道前车、左目标车道前车与后车），每车编码 Δx、Δy、Δvx、Δvy 与**倒数碰撞时间 TTC⁻¹**。奖励为安全/效率/舒适加权和加稀疏任务奖励，权重按超车三阶段调度（0.6/0.1/0.3；0.5/0.4/0.1；0.4/0.1/0.5），用贝叶斯优化与课程学习整定。平台为 highway-env 二次开发加四轮动力学，NPC 纵向 IDM、横向 MOBIL，密度 15–20 veh/km，另加低附着（μ 1.0→0.4–0.6）、噪声与幽灵刹车。1000 次随机场景（5 种子）：成功率 **96.5±0.6%**、碰撞率 **1.2±0.3%**、超时率 **2.3±0.4%**，优于五条基线；去掉 LSTM 使 Jerk 惩罚近三倍，动态奖励换静态使碰撞率升到 5.8%。全部为纯仿真。

## 3. 结论（≤350 字）

作者结论：异构频率分层架构打破单层 RL 瓶颈，**收敛步数降到 60 k、训练 3.2 h、样本效率最高提升 54.5%**；阶段自适应奖励使**平均超车时间 6.4 s、平均车速 15.6 m/s**；相对单层基线**成功率 96.5%、碰撞率 2.0%、平均 Jerk 1.82 m/s³（较最好基线降 44.0%）**。自承局限：**全部验证为软件在环（SIL）仿真**；因高速超车安全风险高且受法规限制，**尚未在全尺寸实车做道路测试**；后续计划域随机化、HIL、1/10 比例车与封闭场地实车，并扩展到 MARL/MAPPO 与 V2V/V2X。**⚠ 结论三个数字与正文冲突**：碰撞率 2.0% vs 1.2±0.3%；Jerk 1.82 vs 0.82±0.06；收敛 60 k vs 约 6×10⁵ 步。§4.6 还把下层写成 SAC。

## 4. 方法一句话（≤60 字）

KIV 状态（Δx,Δy,Δvx,Δvy,TTC⁻¹）→ 1 Hz PPO 出 5 离散意图 → 10 Hz TD3+LSTM 出转向与加速度。

## 5. 图表清单（占位符，覆盖全部图表）

全文共 **10 个 Figure + 3 个 Table**（合计 13 个，全部收录）。图注为逐字（截断到约 100 字符）。

| 占位符 | 图/表号 | 原文图注（逐字） | 读图要点 |
|---|---|---|---|
| {FIG-HRLOT-1} | Figure 1 | Hierarchical Reinforcement Learning: High-Level Strategic Planning and Low-Level Overtaking Control. | 全文总纲：上层 PPO（Strategic Actor/Critic）+ 下层 TD3（Trajectory Actor + **两个** Trajectory Critic，双 Q 抑制高估）+ LSTM Temporal Encoder；图上标注 5 个离散动作全名与"Global Experience Buffer"。**注意图中把 LSTM 编码器写作 "Temporal LSTM Encoad"（原文拼写错误）**。 |
| {FIG-HRLOT-2} | Figure 2 | Schematic of the autonomous overtaking scenario in the simulation environment. | 场景拓扑：RV（后车）、HV1/HV3、FV（前车）、自车（红）、目标点、参考距离 v×1 s、车头间距 d_h 与相对位置 X/Y。**P1 若画 ODD 示意图可复用此结构**。 |
| {TAB-HRLOT-1} | Table 1 | Core network architecture and training hyperparameter settings of HRL-PPO-TD3. | **最可迁移的一张表**：上下层隐藏层均为 [256,256]、ReLU；TD3 Actor 输出层 Tanh；batch 256；TD3 replay buffer 1×10⁶；学习率 PPO 3×10⁻⁴／TD3 Actor 1×10⁻⁴／TD3 Critic 3×10⁻⁴；γ=0.99；τ=0.005；PPO 熵系数 0.01；TD3 探索噪声 N(0,0.1)。⚠ **表内没有列出 PPO 的 clip 系数、GAE λ、TD3 的 policy delay 与 target noise**，不是完整超参表。 |
| {FIG-HRLOT-3} | Figure 3 | Topology Diagram of Highway Overtaking Simulation Scenario and Key Interacting Vehicles. | 三车道俯视图：自车（红）居中车道，NPC 同车道前车（深蓝）、NPC 左后（浅紫）、NPC 左前（浅蓝）；横轴为相对纵向位置 0–50 m，纵轴为横向位置 −4~12 m。对应正文"中高密度 15–20 veh/km"。 |
| {FIG-HRLOT-4} | Figure 4 | Comparison of Average Episode Cumulative Reward Convergence Curves During Training Across Different Algorithms. | 训练收敛曲线（横轴 0.0M–2.0M 步，纵轴平均回合奖励 0–100），4 条：Rule-based（IDM+MOBIL）、Flat-TD3、Flat-PPO、Ours。**注意正文 §4.1 另讨论了图中未出现的 Flat-SAC 与 HRL-PPO-PPO** → 图与正文的算法集合不一致（见 ⚠内部不一致 4）。 |
| {TAB-HRLOT-2} | Table 2 | Performance test comparison of different algorithms in 1000 random overtaking scenarios. | **本卡最重要的数字表**：6 种算法的超车成功率/碰撞率/超时失败率（%），mean±SD（5 种子）。⚠ **表题写 "1000 random overtaking scenarios"，但正文未说明 1000 是"每种算法×每种子各 1000 次"还是"合计 1000 次"**。 |
| {FIG-HRLOT-5} | Figure 5 | Performance Comparison of Different Algorithm Models. | Table 2 的柱状图版（Success/Collision/Timeout Rate 三分量）。**只有 Figure 5 与 Table 2 互为佐证，无其他数值来源。** |
| {TAB-HRLOT-3} | Table 3 | Performance Comparison under Diverse Extreme Scenarios. | 极端场景表：Standard/Rainy(低附着)/Foggy(高噪声)/Road Anomaly(急刹) × {Ours, Flat-PPO, Rule-based}，列为 SR(%)、CR(%)、Comfort(Low/Medium/High/Very High)。**注意**：① 只有 Ours 跑满四行，Flat-PPO 缺 Standard 与 Road Anomaly 行，Rule-based 只有 Road Anomaly 行；② "Comfort" 是**有序标签而非数值**，无法与 P1 的 Jerk 峰值或加速度平方积分对齐；③ 括号内 ↓ 值（如 92.1 (↓4.4)）未说明是相对下降还是百分点下降。 |
| {FIG-HRLOT-6} | Figure 6 | Macro & micro integration of a typical 3-lane overtaking trajectory (0–8 s). | **全文唯一的分层逻辑可视化**：横轴 0–8 s，三行面板分别给 High-Level Decision (1 Hz)、Low-Level Steering (rad)、Low-Level Accel (m/s²)、Ego Velocity (m/s)，每列附自然语言解释（"Safe to follow; Keep current lane"/"Left window detected; Issue Overtake cmd"/"Safe distance reached; Issue Return cmd"）。**P1 的可解释性论证可直接照搬这种"决策—控制—自然语言"三行时间对齐图**。 |
| {FIG-HRLOT-7} | Figure 7 | Impact of the Stage-Adaptive Continuous Reward and LSTM Temporal Memory Module on safety and control smoothness. | 消融图（6 子图）：(a)(b)(c) 为 Full / No LSTM / No SACR 的 Episode–Reward，(d)(e)(f) 为同三者的 Episode–Jerk。**只有曲线，正文给出的两个数字（Jerk 近三倍、碰撞率 1.2%→5.8%）无表格支撑**。 |
| {FIG-HRLOT-8} | Figure 8 | Training performance and test results of the high-level PPO module under different learning rates. | 上层 PPO 学习率敏感性：LR = 1×10⁻⁴、3×10⁻⁴（基线）、5×10⁻⁴、1×10⁻³。正文称 ±50% 内成功率波动 ≤3%，1×10⁻³ 时训练早期剧烈震荡。 |
| {FIG-HRLOT-9} | Figure 9 | Effect of temporal memory length (T) in the low-level TD3-LSTM module on control smoothness and sample training efficiency. | 双纵轴图：左轴 Average Jerk (m/s³)（0–20）、右轴 Convergence Steps (×10³)（80–160），横轴 T = 1/3/5/10。**这是全文最接近 P1 指标体系的图（Jerk + 收敛步数），但横轴是记忆长度而非 OTF 强度。** |
| {FIG-HRLOT-10} | Figure 10 | Visualization of the hierarchical decision and control process during an overtaking maneuver. | 三面板可解释性图：(A) 上层观测（相对距离 Δd 与相对速度 Δv，标 "Safety Threshold (20 m)" 与 "Trigger t1 = 3s"）、(B) 上层离散语义动作 Keep(0)/Overtake(1)、(C) 下层连续转向（rad）。**"20 m 安全阈值"与"3 s 触发"只出现在本图的坐标轴标注里，正文从未定义这两个数**（见 §7 缺失信息 3）。 |

## 6. 对 P1 的用处

- **与 P1 的关系**：**相邻（同 ODD 的"超车决策"环节，但不同控制器范式、不同被控对象）**。P1 的控制对象是**编队跟车**、核心自变量是 **OTF（超车频次）**、控制器是**连续时间网络（CfC）**；本文的控制对象是**单车超车机动的转向/加速度**、自变量是**交通密度与车辆行为风格**、控制器是**离散决策 PPO + 连续控制 TD3-LSTM**。**Jerk 与横向偏差两项有弱重叠，跟车误差 RMSE／前轮转角方差／端到端延迟／MCU 内存四项完全没有。**

### 6.1 特别要求逐条回答（任务 §3 第 1 篇的 ①②③④⑤）

**① 分层结构（上层/下层各做什么、频率多少）** —— 逐字：
- 上层："the high-level strategic decision-maker, acting as the **'brain'** of the system, **operates at a frequency of 1 Hz** and employs the **PPO** algorithm. It takes the macroscopic environmental state as input and outputs **five discrete strategic actions**: lane keeping, preparing to overtake, executing overtaking, returning to the lane, and emergency braking."（§2.1）
- 下层："the low-level trajectory executor, acting as the **'cerebellum'** of the system, **operates at a frequency of 10 Hz**. It receives the strategic action intention issued by the high level **as conditional input**, combined with the ego vehicle's microscopic kinematic state and historical time-series information… adopts an architecture combining the **TD3** algorithm with **LSTM**"（§2.1）
- 形式化："decomposing the global MDP into a high-level **Semi-Markov Decision Process (Semi-MDP)** and a low-level standard **MDP**"（§2.1）。
- **网络**：上下层全部为 MLP，隐藏层统一 **[256, 256]**、ReLU；上层 Actor 输出层 **Softmax**（离散），下层 Actor 输出层 **Tanh**（连续归一化）；下层 TD3 含 **两个独立 Critic**。训练硬件 **NVIDIA RTX 4090**，PyTorch 2.1（§3.2 + Table 1）。

**② 状态与动作空间** —— 逐字：St = [s_ego, ⋃_{i∈KIVs}{Δx_i, Δy_i, Δv_x,i, Δv_y,i, TTC⁻¹_i}]（式 2）。
- **KIV 只取三辆车**："namely, the preceding vehicle in the same lane, the preceding vehicle in the left target lane, and the following vehicle in the left target lane"（§2.2）。
- **动作**：上层 5 离散（LK/PT/OT/RL/EB）；下层连续（转向 + 加速度；论文只说"outputting specific continuous control commands"，**未给出动作的数值范围与量纲**）。
- ⚠ **s_ego 的分量本文从未逐一列出**（只说"the microscopic kinematic state of the ego vehicle itself"），动作边界也未给 → **本卡不能用于对齐 P1 的状态/动作定义**。

**③ 超车的判据是什么（TTC？间隙？）** —— **本文没有显式的超车判据**。逐条依据：
- **TTC⁻¹ 只是状态特征，不是判据**：TTC⁻¹_i = max(0, v_ego − v_x,i)/Δx_i（式 1），"introduced the reciprocal of the Time-to-Collision (TTC) as the core representation of safety risk"，取倒数只为避免相对速度为 0 时出现奇异值。
- **实际的安全边界是"学习出来的 + 奖励里的硬约束"**："Once the relative distance between the ego vehicle and surrounding interacting vehicles is less than the **set dynamic safety boundary**, the system will trigger a massive negative reward… the closer the distance and the higher the collision urgency, the non-linearly greater the penalty value"（§2.3）。**该"动态安全边界"的数值全文未给。**
- 文中唯一带 TTC 阈值的角色是**基线**："Rule-based (IDM + MOBIL), a traditional traffic flow model that performs lane-changing decisions based on **preset TTC thresholds**"（§3.4）——**阈值数值未给**。
- Figure 10 坐标轴出现 "Safety Threshold (20 m)" 与 "Trigger t1 = 3s"，但**这两个数从未在正文定义或引用**。
→ **结论：P1 若需要一个可读、可审计的显式超车判据（如"TTC > τ 且目标车道间隙 > g"），本文提供不了；它反而是一个"判据被隐式学进策略里"的例子，可作为 P1 主张"OTF 势场提供可解释判据"时的对照反例。**

**④ 与 P1 OTF 的接口：这篇有没有类似的"拥堵/交互强度"量？** —— **没有 OTF，也没有可替代 OTF 的聚合交互强度标量。** 核验方式与结果：
- 全文检索 `frequency` 的 **14 处命中全部是"控制频率"（1 Hz/10 Hz/异构频率/同频）**，无一处指超车频次；检索 `overtaking frequency` **零命中**。
- 与"交互强度"沾边的只有两个量，**都不是 OTF 的等价物**：
  1. **交通密度 15–20 vehicles/km**（§3.3，称为 "medium-high traffic density"）——它是**环境生成参数**，不是策略输入，也不是随仿真推进变化的观测量；且 Abstract 里的 "medium-density"（98.3%）与 "high-density"（>95%）**在正文没有任何定义或分档**。
  2. **TTC⁻¹（逐车、瞬时、局部）**——它是**局部风险密度**，不是**行为频次**；作者自己把它定位为 "a **minimalist extraction of a 'local risk potential'** tailored to specific game-theoretic objectives"（§2.2）。
- **★ 对 P1 最有价值的一条（可作为 Introduction 必须回应的对立面）**：本文**明确地、有理由地拒绝了全局势场路线**。逐字："Diverging from approaches that address lateral motion uncertainties via refined two-dimensional fuzzy logic models, or those that conduct **macroscopic, fine-grained risk modeling of global traffic flow using continuous potential fields**, the method proposed in this paper essentially represents a minimalist extraction of a 'local risk potential'… Considering the transient nature of microscopic interactions in overtaking scenarios and the **sensitivity of reinforcement learning algorithms to state-space dimensionality**, the proposed system **intentionally bypasses** complex lateral uncertainty reasoning and **global field computations**."（§2.2）
  → P1 的 OTF 势场正是"global field computation"一类构造。**这篇 2026 年论文给出了"为什么不做全局势场"的完整论证（RL 状态空间维度敏感 + 超车交互瞬态）**，P1 的 Related Work／Discussion 必须正面回应：① 若 P1 的 OTF 势场只作为 **ODE 边界条件 / inductive bias**（而非直接拼进 RL 状态向量），维度代价与"全局场计算"不同，这个反驳不直接命中；② 但若 P1 把 OTF 势场作为策略输入特征，本文的反驳成立，P1 需要给出维度/样本效率的实测对照。**这是本卡对 P1 的最高价值点。**
- 次要接口：本文引用的 [35] "Perceived Risk Field Model (PRFM)"（"constructs a continuous safety potential field"）是势场路线的代表，可进 P1 的势场相关工作；⚠ 但**该条引用的编号与参考文献表不符**，见 ⚠内部不一致 5。

**⑤ 仿真还是实车、闭环与否、有无 CI/种子** ——
- **纯仿真**：`highway-env` 二次开发（"conducts secondary development based on highway-env, an open-source traffic flow simulation platform"），自车用"四轮车辆动力学模型"。**无实车**；作者逐字自承："All current validations are based purely on **Software-in-the-Loop (SIL) simulations**… this paper has **not yet conducted road test validations on full-scale real vehicles**."（§5）
- **闭环**：是。RL 训练本身即闭环；评价为 1000 次随机场景的闭环蒙特卡洛 rollout（"we conducted 1000 Monte Carlo tests in randomly generated traffic flows"）。
- **种子**：**有 5 个**——"we conducted independent training using **5 different random seeds**"（§4.1）；"incorporating model validation across **5 different random seeds**"（§4.2.1）。
- **CI**：**无**。全文无 confidence interval / 95% / Wilson / Clopper-Pearson（grep 零命中）。
- **统计检验**：**无**。只有 mean ± SD；无 p 值、无效应量、无多重比较校正。**"significantly" 一词在 §2.2 用于描述 SOTA 差异，但本文自己的结果从未做检验。**
- **代码/数据**：**无**。Data Availability Statement 逐字："The original contributions presented in the study are included in the article. Further inquiries can be directed to the corresponding author."

### 6.2 可迁移

1. **异构频率解耦的架构先例（直接对应 P1 架构原则"大胆决策，小心修正"）**：1 Hz 离散意图 + 10 Hz 连续控制 + **意图作为下层条件输入**。P1 的 MPC+LNN 混合若按"决策/修正"分层，本文是 2026 年可引的同构先例（但注意本文两层**都是学习器**，没有 MPC）。
2. **可复用的闭环评价协议**：1000 随机场景 + **三分量结果（成功率/碰撞率/超时失败率）** + 5 种子 mean±SD + **极端条件分层（标准/低附着/高噪声/突发异常）**。P1 的 `AGENTS.md` §5 要求"逐场景报告"与长尾覆盖，本文的"标准—恶劣—异常"三层切法是可直接照搬的**表结构**（不搬数字）。
3. **"失败率分解"的写法**：把 Rule-based 的"零碰撞但 31.5% 超时"作为**保守性代价**显式量化。P1 若基线 MPC 偏保守，这是现成的报告范式。
4. **可解释性的图表范式（Figure 6 / Figure 10）**："宏观决策（语义标签）—微观控制（数值曲线）"按同一时间轴三/四行对齐。P1 若要把 OTF 势场做成可解释卖点，这是社区已接受的表现形式。
5. **消融设计的最小集**：本文做的是"去掉时序记忆（LSTM）"与"去掉动态奖励（换静态）"两个单因素消融 + 两组超参敏感性（学习率、序列长度 T）。这正是 P1 `AGENTS.md` §4"消融一次只改一个因素"所能对齐的结构。
6. **奖励归一化纪律**：加权前把三个子奖励"dynamic clipping and normalization (restricted to the [−1, 1] interval)"，使权重数值真的反映物理重要性。P1 若把 OTF 势场并入奖励，这是可引的工程细节。

### 6.3 陷阱 / 不可迁移

1. **不是编队控制，也不测跟车**：全文无 platoon、无车队、无跟车误差，被控对象是单车超车机动的转向与加速度。**P1 的"跟车误差 RMSE"与"前轮转角方差"在本卡零证据。**
2. **资源类指标全缺**：训练用 RTX 4090，但**无参数量、无模型大小、无单步推理时延、无内存占用、无 MCU/嵌入式部署**（grep `latency`/`inference time`/`model size`/`MCU`/`microcontroller`/`embedded`/`Jetson`/`onboard` 全部零命中）。→ **对 P1 的"端到端延迟"与"MCU 内存占用"两条指标，本文供不了任何数字**，且它连"推理在什么硬件上跑"都没写。
3. **"控制频率"是 RL 训练/决策步频，不是实时推理频率**：1 Hz/10 Hz 只是 MDP 的时间步定义，论文没有任何墙钟时间、单步耗时或实时性证据。**不得把"10 Hz"读成"已实现 10 Hz 实时控制"。**
4. **6.4 s / 15.6 m/s 与场景设定自相矛盾**：§3.3.1 写自车初速 **20 m/s**、目标车道限速 **30 m/s**，而结论说"increases the average vehicle speed to **15.6 m/s**"——低于初速。要么是笔误，要么"平均车速"口径未定义。
5. **Jerk 的量纲不一致**：§4.2.1 说 "reduces the average comfort penalty (Jerk) to the lowest value of **0.82 ± 0.06**"（**无单位**），结论说 "reducing the average Jerk to **1.82 m/s³**"；Figure 9 的纵轴单位是 m/s³ 且量程 0–20。**三个口径互不相同，引用前必须澄清。**
6. **摘要数字不可追溯（最严重）**：Abstract 的 "**98.3%** success rate in medium-density scenarios with a collision rate of only **0.6%**"、"lateral control deviation is strictly limited to within **0.2 m**"、"longitudinal safety distance remains stable above **5 m**"——**这四个数在 Table 2、Table 3、Figure 5、Figure 9 及全部正文中均查不到**（grep 仅命中 Abstract 本身）。**在作者澄清前，这四个数字绝对不可引用。**
7. **奖励权重"是贝叶斯优化搜出来的"但未报告搜索空间与最优值来源**：§2.4.2 只说在"preset parameter space"内搜索，三阶段权重（0.6/0.1/0.3 等）**是否为搜索结果、搜索了多少次、目标函数如何折中成功率与碰撞率，均未报告**；同时 §2.4.2 又称"avoids pure manual tuning"，而权重值恰为一位小数的整齐值。**该过程不可复现。**
8. **§2.4.3 的"敏感性分析"没有任何数据**：三个子奖励的敏感性结论（"exponential increase in collision rates"、"linear sensitivity"、"highly sensitive"）**全部无图无表无数字**，属定性断言，不可引用。
9. **交通参与者行为模型是 IDM+MOBIL 的随机风格参数**，论文只写"randomly assigned different driving styles (ranging from conservative to aggressive)"，**未给分布、未给参数、未给种子** → P1 若要对齐"同一组交通流随机种子"的公平性要求（`AGENTS.md` §3），本文的交通流不可复现。
10. **ODD 细看仍不同**：本文是**三车道、目标车道固定为左侧、只做一次超车机动**；P1 是多车道主线 + 人工/自动混行的**编队跟车**。把本文的"超车成功率"当作 P1 场景的性能证据即属跨 ODD 外推（`AGENTS.md` §5）。

### 6.4 引用限定语（可直接粘贴，写英文稿时用）

> 在 Wang & Tang 关于**分层强化学习超车决策与控制**的工作中（*Electronics* 2026;15(8):1711），结论限定于**highway-env 二次开发的纯软件在环仿真**、**三车道高速公路、单车超车机动**：上层 **PPO 在 1 Hz 输出 5 个离散策略动作**、下层 **TD3+LSTM 在 10 Hz 输出连续转向与加速度**（意图作下层条件输入），状态仅含三辆"关键交互车"的 Δx/Δy/Δvx/Δvy 与 **TTC⁻¹**；结果为 **1000 次随机场景、5 个随机种子的超车成功率 96.5±0.6%、碰撞率 1.2±0.3%**（**均值±标准差，无置信区间、无显著性检验、无效应量**）；该文**未报告参数量、模型大小、推理时延、内存占用或任何嵌入式/MCU 部署**，**未做实车验证**（作者自述全部为 SIL），**未公开代码或数据**，且**其摘要中的 98.3%/0.6%/0.2 m/5 m 四个数字在正文与表格中无法追溯**；该文亦**未定义任何"超车频次"或聚合交互强度指标**，其 TTC⁻¹ 为逐车瞬时局部风险量，作者明确选择**不做全局势场计算**。

## 7. 缺失信息（≥3 条，写成可执行动作）

1. **需向作者索取 Abstract 四个数字的出处**：98.3%（中密度成功率）、0.6%（中密度碰撞率）、0.2 m（横向控制偏差）、5 m（纵向安全距离）分别对应哪张表/哪幅图/哪一组实验？（后果：**这四个数是本文被引最多的卖点，却在本材料中完全不可追溯；在澄清前 P1 引用本文任何数字都必须避开 Abstract。这是本卡最重要的一条。**）
2. **需作者澄清三处数字冲突**：碰撞率 **1.2%（Table 2/§4.2.1） vs 2.0%（§5 结论）**；Jerk **0.82±0.06（§4.2.1，无单位） vs 1.82 m/s³（§5 结论）**；收敛步数 **约 6×10⁵（§4.1） vs 60 k（§5 结论）**。另请给出样本效率提升的两种口径 **~30%（Abstract） vs 54.5%（§5）** 的计算方式。（后果：**任何一个数字在被澄清前都不能进 P1 稿件**。）
3. **需作者给出"动态安全边界"与超车启动判据的数值定义**：§2.3 的 "set dynamic safety boundary"、Figure 10 坐标轴上的 "Safety Threshold (20 m)" 与 "Trigger t1 = 3s"、§3.4 规则基线的 "preset TTC thresholds"。（后果：**P1 若要写"本文的超车判据是 TTC 阈值"，目前是错的——本文的判据是隐式学到的；照抄会把错误写进 P1 的 Related Work。**）
4. **需作者补报资源类指标**：模型参数量（上层/下层分开）、序列化模型大小、单步推理时延（ms）、推理硬件与内存占用、是否做过量化。（后果：**P1 的"端到端延迟"与"MCU 内存占用"两项指标无法引本文**。）
5. **需作者澄清统计口径**：① F/χ² 检验在哪里？② 1000 次蒙特卡洛是"每算法每种子 1000 次"还是"合计 1000 次"？③ Table 2 中 Rule-based 的 SD 为 **±0.0**，若真有 5 个随机种子且规则法确定性，请说明随机性来自哪里（场景生成？）。（后果：**Table 2 的 ±SD 目前不可解释；不能据此写"更稳定"。**）
6. **需作者澄清 §4.6 的算法名**："the lower-layer **SAC** algorithm take over" 应为 TD3 还是确实比较了 SAC？（后果：若下层真含 SAC，则与 Table 1、Figure 1 全部冲突。）
7. **需索取训练与仿真的可复现材料**：代码、随机种子清单、IDM/MOBIL 参数分布、场景生成脚本。（后果：`AGENTS.md` §3 的"同一组交通流随机种子"公平性要求在本文无法落实。）
8. **需做 T2 取代检查（本卡未做，标 `[待核实]`）**：检索 2026 年 4 月之后是否有 ① 分层/异构频率 RL 用于**高速公路编队跟车**（而非单车超车）的期刊工作；② 以**超车频次（overtaking frequency）作为显式状态/条件变量**的强化学习控制工作；③ 对本文的复现或反例。动作：OpenAlex `cites:` + Crossref + arXiv，记录检索式与日期。**若 ② 存在，P1 的"OTF 作为结构条件"新颖性论证必须重写。**

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 分层频率 | 上层 PPO **1 Hz**；下层 TD3+LSTM **10 Hz** | — | §2.1 |
| 上层离散动作数 | **5**（LK/PT/OT/RL/EB） | — | §2.1；Figure 1 |
| 网络隐藏层 | 上下层均 **[256, 256]**，ReLU；TD3 Actor 输出 Tanh，PPO Actor 输出 Softmax | — | §3.2；Table 1 |
| Batch size / Replay buffer | **256** / **1×10⁶** | — | Table 1 |
| 学习率 | PPO **3×10⁻⁴**；TD3 Actor **1×10⁻⁴**；TD3 Critic **3×10⁻⁴** | — | Table 1 |
| γ / τ / 熵系数 / 探索噪声 | **0.99** / **0.005** / **0.01** / **N(0, 0.1)** | — | Table 1 |
| KIV 数量与构成 | **3 辆**：同车道前车、左目标车道前车、左目标车道后车 | — | §2.2 |
| 交通密度 | **15–20 vehicles/km**（"medium-high"） | — | §3.3 |
| 自车初速 / 目标车道限速 | **20 m/s** / **30 m/s** | — | §3.3.1 |
| 低附着路面摩擦系数 | μ 由 **1.0** 降到 **0.4–0.6** | — | §3.3.2 |
| 幽灵刹车减速度 / 障碍 | 前车随机触发急刹 **5 m/s²**；另设静态路障 | — | §3.3.3 |
| 超车成功率（Ours，1000 场景，5 种子） | **96.5 ± 0.6 %** | SD（无 CI） | Table 2 |
| 碰撞率（Ours） | **1.2 ± 0.3 %** | SD | Table 2 |
| 超时失败率（Ours） | **2.3 ± 0.4 %** | SD | Table 2 |
| 超车成功率（HRL-PPO-PPO / Flat-SAC / Flat-PPO / Flat-TD3 / Rule-based） | **92.1±1.5 / 88.4±1.9 / 81.3±3.2 / 77.2±4.1 / 68.5±0.0 %** | SD | Table 2 |
| 碰撞率（HRL-PPO-PPO / Flat-SAC / Flat-PPO / Flat-TD3 / Rule-based） | **3.2±0.6 / 4.5±0.8 / 8.4±1.5 / 11.5±1.8 / 0.0±0.0 %** | SD | Table 2 |
| 超时失败率（HRL-PPO-PPO / Flat-SAC / Flat-PPO / Flat-TD3 / Rule-based） | **4.7±0.9 / 7.1±1.2 / 10.3±2.1 / 11.3±2.6 / 31.5±0.0 %** | SD | Table 2 |
| 极端场景成功率（Ours） | Rainy **92.1（↓4.4）**、CR 2.8；Foggy **90.8（↓5.7）**、CR 3.1；Road Anomaly **88.5（↓8.0）**、CR 4.5 | 无（单值） | Table 3 |
| 极端场景成功率（Flat-PPO） | Rainy **70.3（↓11.0）**、CR 15.2；Foggy **65.4（↓15.9）**、CR 18.6 | 无 | Table 3 |
| 极端场景成功率（Rule-based，仅 Road Anomaly 行） | **55.2（↓13.3）**、CR **0.5** | 无 | Table 3 |
| 消融：去掉 LSTM | Jerk 惩罚"**nearly three-fold increase**"（无绝对数） | 未报告 | §4.4 |
| 消融：动态奖励换静态奖励 | 碰撞率 **1.2% → 5.8%** | 未报告 | §4.4 |
| 收敛步数 | 单层 Flat-PPO/Flat-TD3 约 **1.2×10⁶** 步后才缓升；Flat-SAC 约 **9×10⁵**；HRL-PPO-PPO 约 **7.5×10⁵**；Ours 约 **6×10⁵** | 未报告 | §4.1 |
| 最终累计奖励相对提升 | 比 Flat-SAC 高约 **15%**；比 HRL-PPO-PPO 高约 **8%** | 未报告 | §4.1 |
| Abstract 声称的收敛加速 | "improves the training convergence speed by approximately **30% within 500,000 steps**" | 未报告 | Abstract |
| 结论声称的收敛/训练 | 收敛步数降到 **60 k**、训练时间 **3.2 h**、样本效率提升 **up to 54.5%** | 未报告 | §5 |
| 结论声称的超车时间与车速 | 平均超车时间 **6.4 s**；平均车速 **15.6 m/s** | 未报告 | §5 |
| 结论声称的碰撞率与 Jerk | 碰撞率 **2.0%**；平均 Jerk **1.82 m/s³**（较最好基线降 **44.0%**） | 未报告 | §5 |
| 超车轨迹时长（典型样例） | **0–8 s**（Stage 1 0–2 s；Stage 2 2–5 s；Stage 3 5–8 s） | — | §4.3；Figure 6 |
| 超车三阶段奖励权重 (w1,w2,w3) | 阶段 1 **0.6/0.1/0.3**；阶段 2 **0.5/0.4/0.1**；阶段 3 **0.4/0.1/0.5** | — | §2.4.1 |
| LSTM 历史序列长度 T（基线） | **5**（对照 T = 1、3、10；T=10 使收敛样本数增加约 **15%**） | 未报告 | §4.5.2；Figure 9 |
| PPO 学习率敏感性 | ±50%（1×10⁻⁴~5×10⁻⁴）内成功率波动 ≤ **3%**；1×10⁻³ 时早期剧烈震荡 | 未报告 | §4.5.1 |
| 训练硬件 | **NVIDIA RTX 4090**，PyTorch **2.1** | — | §3.2 |
| 参数量 / 模型大小 / 推理时延 / 内存 / MCU | **全文未见**（grep 零命中） | — | 全文 |
| 随机种子数 | **5** | — | §4.1；§4.2.1 |
| 蒙特卡洛测试次数 | **1000**（口径未说明） | — | §4.2.1；Table 2 |
| 代码 / 数据可用性 | **无**（"The original contributions presented in the study are included in the article."） | — | Data Availability Statement |
| 论文时间线 | Received **8 March 2026**；Revised/Accepted **14 April 2026**；Published **17 April 2026** | — | 首页 |
| 资助 | 湖北省科技厅 **2024BAB008**；武汉市科技创新局与武汉 DR Laser **2024010702020023**；中国电科院 **SGDK0000PDMM2502428**；武汉工程大学 **K2023047（23QD14）** | — | Funding |

**⚠内部不一致（逐条列出，引用前必须处理）**

- ⚠内部不一致 1（**最严重**）：Abstract 的 **98.3% 中密度成功率、0.6% 中密度碰撞率、"lateral control deviation…within 0.2 m"、"longitudinal safety distance remains stable above 5 m"** 四项**在全文任何表格、图与正文段落中均无对应**（全文 grep 仅命中 Abstract 行本身）。与 Table 2 的 96.5±0.6% / 1.2±0.3% 也不一致。
- ⚠内部不一致 2：**碰撞率** §5 结论 "limits the collision rate to **2.0%**" vs Table 2 / §4.2.1 的 **1.2 ± 0.3%**。
- ⚠内部不一致 3：**Jerk** §4.2.1 "lowest value of **0.82 ± 0.06**"（无单位） vs §5 结论 "average Jerk to **1.82 m/s³**"；Figure 9 纵轴为 m/s³、量程 0–20。
- ⚠内部不一致 4：**训练收敛** Abstract "approximately 30% within 500,000 steps" vs §4.1 "approximately **6 × 10⁵** steps" vs §5 "reducing convergence steps to **60 k**…up to **54.5%**"。同一指标出现 5×10⁵、6×10⁵、6×10⁴ 三个量级与 30%、54.5% 两个比例。
- ⚠内部不一致 5：**§4.6 把下层控制器写成 SAC**："only after this high-level decision is made does the **lower-layer SAC algorithm** take over to handle microscopic vehicle dynamics"。全文其余部分（Abstract、§2.1、§3.2、Table 1、Figure 1、缩写表）均为 **TD3**。
- ⚠内部不一致 6：**平均车速 15.6 m/s（§5）低于自车初速 20 m/s（§3.3.1）**，而正文通篇描述的是"加速超车"。
- ⚠内部不一致 7：**§3.4 首句整段重复一次**（"To highlight the dual advantages … as baselines for comparison:" 紧接 "To highlight the dual advantages … as benchmarks for comparative analysis:"），两句内容相同、措辞不同。
- ⚠内部不一致 8：**Figure 4 只画 4 种算法**（Rule-based、Flat-TD3、Flat-PPO、Ours），而 §4.1 的收敛讨论包含 **Flat-SAC 与 HRL-PPO-PPO**（Table 2 也有）。两条基线的收敛曲线在图与表中无法对应。
- ⚠内部不一致 9：**正文 [34]/[35] 与参考文献表编号错位**：正文 "Xu et al. [34] proposed a two-dimensional SSM based on the fuzzy logic and inverse TTC (FL-iTTC) model" 对应的是参考文献 **35**（Xu, Y.; Ye, W.; Xie, Y.; Wang, C. *Accid. Anal. Prev.* 2024, 199, 107529，题名即 "A two-dimensional surrogate safety measure based on fuzzy logic model"）；而正文 "the perceived risk field model (PRFM) proposed by **Yichang et al. [35]**" **在参考文献表中找不到任何对应条目**（表中 34 为 Liu Q. 等的 graph transformer RL 工作）。**若 P1 要引 PRFM，必须直接从原文重查该文献。**
- ⚠内部不一致 10：**实验设计与统计口径未闭合**：称"5 different random seeds"，但 Table 2 中 Rule-based 的 SD 为 **±0.0**（三列全为 0.0），且未说明 1000 次蒙特卡洛与 5 个种子如何组合（1000×5？1000÷5？）。
- ⚠内部不一致 11：**Figure 1 图内文字 "Temporal LSTM Encoad"** 为原文拼写错误（应为 Encoder），图注本身无此字，属图内文本；引用图内标签时须注意。

**字数实测（口径：该节内去除全部空白与 Markdown 标记 `# * \` | > \ -` 后的字符数，含中英文标点）**：§2 = **400 字**（上限 400）；§3 = **319 字**（上限 350）；§4 = **60 字**（上限 60）。**【确定，本机 PowerShell 脚本实测，测量式：`$s -replace '\s','' -replace '[#*`|>\\-]',''`】**

【确定】/【待核实】标注：以上引文、图注与表格数字均为本机 .txt 直接核验结果【确定】；"1000 次蒙特卡洛的统计单元"、"动态安全边界数值"、"贝叶斯优化的搜索空间与结果"为 **`[待核实]`**（正文未报告，需向作者确认）；本文是否存在正式版勘误（Crossref `update-to`）**本卡未查**，标 `[待核实]`。
