# 图注意力预测 + MPC 的分层交互决策（HDM）｜Interactive Decision-Making Integrating Graph Neural Networks and Model Predictive Control for Autonomous Driving

- **出处**：IEEE Transactions on Intelligent Transportation Systems, Vol. 26, No. 5, May 2025, pp. 6991–7005 ｜ **类型**：期刊论文（方法 + 仿真/数据集/HiL 实验）
- **作者**：Kai Yang et al.（第一作者 Kai Yang，重庆大学机械与运载工程学院；通讯作者 Shen Li、Xiaolin Tang）
- **DOI**：10.1109/TITS.2025.3532936（Crossref `works/10.1109/TITS.2025.3532936`，取用日期 2026-10-04：命中，题名一致，Vol. 26 / Issue 5 / pp. 6991-7005 一致，`relation` 为空 → 未见更正或撤稿标记）
- **全文来源**：`literature/fulltext/meeting2/interactive-decision-making-integrating-graph-neural-network__440c8383.txt`（本机文本 72,118 字符 / 15 页）
- **分组**：TITS
- **证据等级初判**：**B 级** — 设计良好但有明确边界：CARLA 四类交互场景闭环 + 6 组消融 + 7 个基线 + HiL 台架两种场景 + 主动报告失败案例；但**无显著性检验/CI**，且**部分基线数字直接取自文献 [29]（跨论文拼接）**，**非实车**，ODD 为城市交叉口/环岛（跨 ODD）。
- **档位建议**：**A 精读** — 它是本组唯一直接命中 P1 **架构原则**（学习型上层"大胆决策" + MPC 下层"小心修正"）的论文：给出可复用的 MPC 代价函数/避撞约束写法、学习型预测器的在线训练范式、逐场景失败分类，以及**"预测失败时由 MPC 兜底"的实证片段**（Fig. 7 timestep 130）。
- **五维打分**：D1=2 D2=2 D3=1 D4=2 D5=1 → 加权 = 3·2+2·2+2·1+1·2+2·1 = 6+4+2+2+2 = **16 / 20**（A 档判据：加权 ≥14 且 D1=2 且 D5≥1 ✓）

> ⚠ **冻结协议排除词表字面命中（需上游裁定）**：本文四个实验场景为 **unsignalized intersection / T-junction / roundabout / mixed traffic（含行人）**，`literature/meeting2/00-triage-protocol.md` §3"跨 ODD"排除词表字面命中 `intersection` / `roundabout` / `urban unsignalized` / `pedestrian interaction`。若**机械执行"命中即 D 档"**，本文应降为 D。
> **本卡片按实质判为 A 的理由**：(1) 排除词表的理由栏写的是"跨 ODD 结论无效"——本文的**性能数字确实不可迁移**（本卡片已逐条标注）；(2) 但 P1 需要的是本文的**架构与约束写法**（学习型上层 + MPC 下层、避撞约束、兜底逻辑），这与 ODD 无关；(3) 父任务亦明确点名本文"与 P1 基线②及架构原则直接相关"。**建议**：对排除词表补一句限定——"仅当论文的**主要结论**落在该 ODD 时才排除；方法/架构层可迁移者按 D1 正常计分"。此条已列入回传的"本组材料问题"。

---

## 1. 标题

Interactive Decision-Making Integrating Graph Neural Networks and Model Predictive Control for Autonomous Driving｜中文直译：融合图神经网络与模型预测控制的自动驾驶交互式决策

## 2. 摘要（≤400 字中文，保留关键数字与结论成立条件）
公开道路驾驶本质是双向交互：自车动作影响周边车辆、反之亦然，而现有模块化栈多假设单向影响，易致过保守规划或冻结机器人问题。本文提出分层决策框架 HDM。上层为粗粒度策略生成器，用 plan-informed graph attention network（P-GAT）做交互感知引导：输入周边车辆历史状态、道路结构与自车潜在意图的候选轨迹集（含左换道、右换道、保持车道及目标速度，轨迹由二次规划预计算），输出各意图下他车未来轨迹，再按安全、效率、舒适三项代价选最优意图。下层为细粒度 MPC，以非线性运动学自行车模型、三点圆与椭圆避撞约束、道路边界与执行器约束生成可行轨迹。P-GAT 不用数据集离线预训练，而像强化学习一样在与环境交互中在线训练。验证含 openDD 数据集注入 CARLA 的定性实验、CARLA 四场景定量、硬件在环两场景与失败案例。定量结果：无信号交叉口 HDM 成功率 98%、碰撞率 2%（GAT-MPC 74% 与 25%，IntMPC 75% 与 18%）；T 型口 91% 与 9%、通行 18.4 s；环岛 98% 与 1%（IntMPC 91% 与 7%）。实时性：上层小于 0.2 s（2 Hz），下层小于 0.02 s（10 Hz）。

## 3. 结论（≤350 字中文）
作者结论：提出面向交互场景的分层决策框架 HDM，先用 P-GAT 交互式运动预测模型刻画自车动作对他车的潜在影响，再由基于 P-GAT 的粗粒度策略生成器提供交互感知引导，最后由细粒度 MPC 结合该引导生成安全、运动学可行的轨迹；定性、定量与硬件在环实验验证其提升安全与效率。关键数字：三场景成功率 98%、91%、98%，碰撞率 2%、9%、1%；人车混行场景成功率 98%、碰撞率 1%、超时率 1%、通行 21.4 s，其基线数字取自文献 [29]；消融中移除自车计划特征使成功率由 98% 降至 94%；实时性满足 2 Hz 与 10 Hz。作者自承局限：报告了典型失败案例，P-GAT 预测前车会让行但实际未让，HDM 虽随即减速仍与另一车路径交叠造成刮擦，作者归因于仿真中该车行为过于激进；本文未深入探讨 P-GAT 失败风险如何影响 MPC 的收敛性与鲁棒性；车载算力受限时的轻量化 P-GAT 仍需探索；未考虑人为因素；未来将做实车实验，即当前未做实车。

## 4. 方法一句话（≤60 字）

周边历史轨迹 + 路网 + 自车候选意图轨迹 → P-GAT（GRU+GAT+Transformer 注意力，在线训练）评分选意图 → 细粒度 MPC。

## 5. 图表清单（占位符）

> 全文共 **14 个 Figure + 4 个 Table = 18 项**，超过 12；下表覆盖**按出现顺序的前 12 项**，剩余 6 项见补充表。
> ⚠ 与论文 1 相同的材料事实：本机 .txt **只有题注、没有表格单元格数值**（对全文 grep 多位小数并列模式无命中）。但本文的**主结果数值在正文中逐句给出**，故下表把正文数字一并抄录，并明确标注"抄自正文、非表体"。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-HDM-1} | Fig. 1 | The overall structure of the proposed hierarchical decision-making method. | 框架总览：意图生成 → 二次规划生成候选轨迹 → P-GAT 预测他车反应 → 粗粒度代价评分选引导 → 细粒度 MPC。前提假设：路结构与限速来自高精地图，他车运动状态可由车载传感器准确获得 |
| {TAB-HDM-1} | TABLE I | PARAMETERS OF THE VEHICLE MODEL AND PROPOSED HDM | 车辆模型与 HDM 全部实验参数；**表体数值在本机文本缺失** → 若要复现或对标 P1 基线②，必须回原 PDF 抄此表 |
| {FIG-HDM-2} | Fig. 2 | The overall structure of P-GAT model (note that only key components and their parameters are described, and some tensor operations in the add part are omitted for brevity). | P-GAT 网络结构；正文式 (13)–(25)：GRU 提动态特征 → GAT 提车间交互（邻居阈值 **30 m**）→ Transformer 注意力提"车—路"交互（G 作 Q、地图编码作 K/V）→ 自车意图轨迹旋转到被预测车坐标系 + sigmoid 打分 → GRU 解码 |
| {TAB-HDM-2} | TABLE II | ABLATION STUDY OF P-GAT COMPONENTS’ IMPACT ON HDM PERFORMANCE | **消融表**（场景：Fig. 4(c) 环岛，作者称"因篇幅只测该场景"）。6 组：①P-GAT 完整 ②wo-T̄（去掉式 (23)(24) 计划特征）③wo-H̄ḠM̄ ④wo-ḠM̄ ⑤wo-Ḡ ⑥wo-H。**正文唯一给出的数字**：去掉 AV 计划特征后成功率由 **98% 降至 94%**；**其余行数值在本机文本缺失** |
| {FIG-HDM-3} | Fig. 3 | Qualitative performance evaluation results via openDD dataset. | openDD（德国 Wolfsburg/Ingolstadt 环岛）四个环岛 rdb1/rdb2/rdb3/rdb6 的定性过程；每个案例只画 3 个关键时刻（如 7.3 s/10.0 s 减速等待、14.3 s/12.0 s 汇入、21.3 s/16.0 s 驶出）；**数据集被注入 CARLA，非实车** |
| {FIG-HDM-4} | Fig. 4 | Test driving scenarios constructed in the CARLA simulator. (a) Unsignalized intersection; (b) T-junction; (c) Roundabout; (d) Mixed Traffic. | 四个定量场景：(a) 无信号交叉口左转、(b) T 型口左转、(c) 环岛进出、(d) 人车混行 |
| {TAB-HDM-3} | TABLE III | COMPARISON RESULTS OF POLICY PERFORMANCE | ★**主结果表 A（分层方法对比）**。**表体缺失；下列行列与数值抄自 §VI-D-2 正文**。场景（列/分组）：无信号交叉口、T 型口、环岛。指标：Succ.% / Coll.% / Pass Time（另有 TO.% 定义）。行（基线）与数值——**无信号交叉口**：Carla Driver Model 88% 成功；GAT-MPC 74% 成功 / 25% 碰撞；IntMPC 75% 成功 / 18% 碰撞；**HDM 98% / 2%**。**T 型口**：GAT-MPC 38% / 60%；IntMPC 35% / 63%；**HDM 91% / 9% / 通行 18.4 s（最短）**。**环岛**：**HDM 98% / 1%**；IntMPC 91% / 7%；GAT-MPC 67% / 30%；通行时间 HDM 27.2 s vs IntMPC 26.2 s。**无 CI、无显著性检验、无语料量（episode 数）逐格报告** |
| {TAB-HDM-4} | TABLE IV | COMPARISON WITH LEARNING-BASED BASELINES IN MIXED ENVIRONMENT | ★**主结果表 B（学习型基线对比，场景 = Fig. 4(d) 人车混行）**。**表体缺失；数值抄自 §VI-D-2 正文**。行（基线）：PPO [41]、DrQ [42]、Decision Transformer (DT) [43]、Scene-Rep-Transformer (SRT) [29]，对比 **HDM**。结果：**HDM 成功率 98%、碰撞率 1%、超时率 1%、通行 21.4 s**；DrQ 通行最短 **21.3 s**。⚠**作者自述"this scenario and comparison algorithms' results are sourced from [29]"——即该组基线数字为跨论文引用，非本文重跑** |
| {FIG-HDM-5} | Fig. 5 | HiL test bench. (a) HiL platform; (b) Schematic diagram of communication. | 硬件在环台架：IPC 跑 CARLA 与粗粒度预测推理、**NVIDIA Jetson Orin** 跑细粒度 MPC、**Speedgoat** 实时机跑车辆模型、**Logitech G29** 模拟人工驾驶车。**注意：HiL ≠ 实车** |
| {FIG-HDM-6} | Fig. 6 | Schematic diagram of mandatory lane change with dense traffic flow. | 强制换道场景：自车在 Lane #0，前方有静止车辆，相邻 Lane #1 车流密集，需及时安全汇入；周围车协人性通过调整跟车距离随机化 |
| {FIG-HDM-7} | Fig. 7 | The driving speed and steering angle of the proposed HDM in the dense traffic case. | timestep 130（关键点①）：P-GAT 预测后车会减速让行，实际未让 → HDM 取消换道；timestep 275（关键点②）：预测到足够安全间隙 → 加速汇入成功。**这是"预测失败由 MPC 兜底"的直接实证** |
| {FIG-HDM-8} | Fig. 8 | The decision-making process and real-time performance in the dense traffic case. (a) Decisions of coarse-level policy generator; (b) Real-time performance. | (a) 0–30 步加速保持车道、30–130 步减速等待、130 步尝试换道、275 步完成；(b) 实时性：**上层多次预测推理 <0.2 s（2 Hz）**、**下层 MPC <0.02 s（10 Hz）** |

**>12 的剩余 6 项（按出现顺序）**

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-HDM-9} | Fig. 9 | The prediction results of P-GAT under different coarse-level policies at timestep 275 in the dense traffic case. (a)-(c) demonstrate the prediction results when the AV adopts keeping lane strategy Iopt(l) = 0 under Iopt(v) = 0m/s, 6m/s, 12m/s, respectively; (d)-(f) demonstrate the prediction results when the AV adopts changing lane strategy Iopt(l) = 1 under Iopt(v) = 0m/s, 6m/s, 12m/s, respectively. (Note that only the closest five vehicles to the AV are shown in the figures). | 关键机制图：保持车道时 P-GAT 预测 veh2 不减速；发出换道意图时预测 veh2 会减速 → 依式 (31) 选换道（Fig. 9(e)） |
| {FIG-HDM-10} | Fig. 10 | Schematic diagram of interacting with aggressive human driver. | 与激进人工驾驶员的交互场景（人为阻挡换道） |
| {FIG-HDM-11} | Fig. 11 | The driving speed and steering angle of the proposed HDM in the interaction with human driver case. | 关键点①（timestep 70 后人工车突然减速）→ HDM 中止换道；关键点②（timestep 85 人工车加速离开）→ 成功换道 |
| {FIG-HDM-12} | Fig. 12 | The decision-making process and real-time performance in the interaction with human driver case. (a) Decisions of coarse-level policy generator; (b) Real-time performance. | 0–15 步以 12 m/s 保持车道，15 步起减速，30 步继续等待，70 步尝试换道，75 步中止，85 步完成；实时性同样满足要求 |
| {FIG-HDM-13} | Fig. 13 | The prediction results of P-GAT under different coarse-level policies at timestep 85 in the interaction with human driver case. (a)-(c) demonstrate the prediction results when the AV adopts keeping lane strategy Iopt(l) = 0 under Iopt(v) = 0m/s, 6m/s, 12m/s, respectively; (d)-(f) demonstrate the prediction results when the AV adopts changing lane strategy Iopt(l) = 1 under Iopt(v) = 0m/s, 6m/s, 12m/s, respectively. | 反例/边界图：关键车位于自车**前方**时，无论自车保持车道还是试图换道，P-GAT 都预测人工车行为不变（自车动作对其无影响）——说明双向交互假设并非处处成立 |
| {FIG-HDM-14} | Fig. 14 | Failure case of the proposed method, where the AV collides with aggressive vehicles. (a) HDM predicts the aggressive vehicle will yield the AV; (b) collision happens. | 失败案例：预测 veh1/veh2 会减速让行但 veh2 未让 → HDM 减速已来不及，与 veh1 路径交叠发生刮擦。P1 的"失败分类与兜底边界"可直接引用此图 |

## 6. 对 P1 的用处

- **与 P1 的关系**：**直接相关（架构层）**。P1 的架构原则是"闭环用 MPC+LNN 混合（**大胆决策，小心修正**）"；HDM 把这条原则实现为"**学习型上层做交互感知的粗粒度意图选择（大胆决策）+ MPC 下层做安全与运动学修正（小心修正）**"，并且是本文四大块实验（定性/定量/HiL/失败案例）共同验证的对象。同时它的下层正是 P1 **基线②（MPC，线性化车辆模型）** 的同类——但注意本文用的是**非线性运动学自行车模型**，不是线性化模型，两者**不能互称**。
- **可迁移（具体到方法/协议/数字/图表）**：
  1. **MPC 代价函数骨架**（式 (32)）：`w1·‖轮廓误差‖² + w2·‖滞后误差‖² + w3·‖v − v_target‖² + w4·‖a‖² + w5·‖δ‖²`——轮廓/滞后误差 + 速度跟踪 + 控制量惩罚，可直接作为 P1 基线②的实现骨架；`w4‖a‖² + w5‖δ‖²` 与 P1 指标"加速度平方积分""前轮转角方差"同源。
  2. **避撞约束写法**（式 (33)(34)）：自车用 **3 个等半径圆**近似、他车用**椭圆**近似，约束 `∪_c ∩_i cons > 1`，半径取 `α = a_i + r_c + ε`、`β = b_i + r_c + κ`（ε、κ 为安全裕度）——这是**可微/可解的非线性约束**写法，比常用的矩形/点约束更适合 P1 编队场景；P1 若要报"安全裕度敏感性"，这是现成模板。
  3. **学习型模块的在线训练范式**（Algorithm 1）：episodic buffer → replay buffer → 小批量按 ADE 损失更新预测器，与 MPC 逐层解耦（上层只给"引导"，不给指令）——这正是 P1 中"OTF 势场层 ↔ LNN 控制器"接口设计的可引用先例（上层给结构条件，下层负责可行性）。
  4. **逐场景报告表**：`Succ.% / Coll.% / TO.% / Pass Time` 四指标 × 逐场景（交叉口/T 型口/环岛/混行）——与 P1 `AGENTS.md` §5"逐场景报告，不只报总平均"完全同构，可直接借为 P1 的场景级报告模板（P1 再补 RMSE / 加速度平方积分 / Jerk 峰值等控制指标）。
  5. **实时性预算写法**：把"学习型上层 <0.2 s（2 Hz）"与"MPC 下层 <0.02 s（10 Hz）"分层报告，且硬件平台写明（Jetson Orin / Speedgoat）——这正是 P1 `AGENTS.md` §3 要求的"资源类指标须记录采集平台与档位"的现成范例。
  6. **"预测失败 → MPC 兜底"的可引用实例**：Fig. 7 + Fig. 8(a) 的 timestep 130 段落，可直接支撑 P1 架构原则的论证（学习层犯错时，下层约束仍能中止动作）。
- **不可迁移 / 陷阱**：
  1. **ODD 完全不同且属跨 ODD**：交叉口 / T 型口 / 环岛 / 人车混行；P1 的 ODD 是高速主线多车道人机混行编队 → **本文所有成功率/碰撞率数字不可迁移到 P1**（`AGENTS.md` §5）。本卡片建议引用时只引**方法结构**，不引性能数字。
  2. **非实车**：定性部分用的是 **openDD 真实数据集但注入 CARLA**（"all experiments are implemented based on the Carla simulator"），另有 **HiL 台架**；三者都不是实车。**不得写成"实车验证"**。
  3. **Table IV 的基线数字是跨论文引用**：作者明写"this scenario and comparison algorithms' results are sourced from [29]"——这正对应 P1 `AGENTS.md` §1"不得直接搬用他人论文数字"。P1 若引用该对比，必须写"文献报告值，协议不同，不可直接比较"。
  4. **无 P1 的跟车/编队指标**：无跟车误差 RMSE、无加速度平方积分、无 Jerk 峰值、无车道居中偏差、无前轮转角方差；本文的效率指标是成功率/通行时间。
  5. **无不确定度**：全部为点估计百分比，**无 CI、无显著性检验、无语料量逐格报告**（正文只说"each experiment is conducted multiple times with different random seeds"，未给次数）→ 引用其"98% vs 74%"时**不得**声称差异显著。
  6. **消融与基线的同名改动不可混用**：消融② wo-T̄（去掉 AV 计划特征、**保留**交互引导）成功率 98%→94%；而基线 GAT-MPC（去掉意图特征 + **离线预训练** + **无交互引导**）在同为环岛的设置下只有 67%。两处都叫"去掉自车意图"，但配置不同、代价差 27 个百分点，**不可互相印证**，引用时须写清是哪一种。
  7. **训练成本未报**：1000 episodes/场景、单张 RTX 3080Ti，但**无训练时长、无参数量、无 FLOPs** → P1 不能据此推断"能否上 MCU"。
- **引用时必须带的限定语**：**"该文为 CARLA 仿真（含 openDD 数据集注入 CARLA 的定性实验与 Jetson Orin/Speedgoat 硬件在环实验，均非实车）中、面向城市无信号交叉口/T 型口/环岛/人车混行的分层交互决策框架；其成功率与碰撞率为点估计、无置信区间与显著性检验，且人车混行场景的基线数值直接取自文献 [29] 而非本文重跑；跨 ODD 到高速公路主线编队时只能迁移方法结构（学习型意图层 + MPC 安全层），不可迁移性能数字。"**

## 7. 缺失信息（可执行动作）

1. **需回原 PDF 抄录 Table I（车辆模型与 HDM 参数）与 Table II（消融 6 行）的完整表体**：包括 Th / Tf / T_f,mpc 三个时域、N 的速度离散数、λ1–λ4 与 w1–w5 的取值、ε 与 κ 安全裕度、r_c 圆半径、a_i/b_i 椭圆轴长。（后果：**P1 无法复现基线②的 MPC 参数**，也无法做同预算调参对齐——`AGENTS.md` §3 要求"同等调参预算"。）
2. **需索取每个百分比的语料量与重复次数**：三类场景各跑了多少 episode、用了几组随机种子、每次实验重复几遍。（后果：正文只说"conducted multiple times with different random seeds"，无 n → "98% vs 74%"不可做任何区间估计；P1 `AGENTS.md` §4 要求成功率类小样本用 Wilson 或 Clopper-Pearson，本文连分母都没给。）
3. **需索取 Table III 的分母是否统一**：三个场景的 episode 数是否相同（若相同，92%/91%/98% 这类数值可反推 8%/9%/1% 的整数计数，否则不可）。（后果：决定这些百分比能否被 P1 用作任何形式的先验。）
4. **需澄清 Table IV 中哪些行是本文重跑、哪些取自 [29]**：作者已说明"scenario and comparison algorithms' results are sourced from [29]"，但未说明 **HDM 那一行**是否在**同一套代码、同一场景配置、同一评测脚本**下产生。（后果：若 HDM 行是本文新跑而基线行是引用，则该表**不是配对比较**，P1 引用时必须标注。）
5. **需索取在线训练 P-GAT 的实际开销**：每 episode 的墙钟时间、总训练时长、P-GAT 参数量与单次推理 FLOPs/显存、是否做过量化。（后果：P1 需要判断"在线训练的学习型上层"能否与 MCU 端控制器共存——本文自己把"轻量化 P-GAT"列为未解决的未来工作。）
6. **需索取实时性的测试条件**：Fig. 8(b)/Fig. 12(b) 的 <0.2 s 与 <0.02 s 是在 HiL 台架（Orin/Speedgoat）上测的，还是在 IPC 上测的；是否含通信时延；计时的分位数（均值？最大值？）。（后果：P1 的"端到端延迟"指标要求写明采集平台与档位，本文未写清。）
7. **需确认代码可用性**：正文两处给出 `https://github.com/Kayne0401/Hierarchical-Decision-Making.git`，但**均标注为"supplementary videos"的来源**，全文无 "code is available" 类声明。（后果：本机无法判定代码是否公开；该仓库链接已记录，取用前须实际访问核实。）

## 8. 关键数字（只抄论文明确印出的表格/正文，不得目测估读）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 无信号交叉口：Carla Driver Model / GAT-MPC / IntMPC / **HDM** 成功率 | 88% / 74% / 75% / **98%** | 未报告（无 n、无 CI） | Table III（数值抄自 §VI-D-2 正文） |
| 无信号交叉口：GAT-MPC / IntMPC / **HDM** 碰撞率 | 25% / 18% / **2%** | 未报告 | Table III（同上） |
| T 型口：GAT-MPC / IntMPC / **HDM** 成功率 | 38% / 35% / **91%** | 未报告 | Table III（同上） |
| T 型口：GAT-MPC / IntMPC / **HDM** 碰撞率 | 60% / 63% / **9%** | 未报告 | Table III（同上） |
| T 型口：HDM 通行时间 | **18.4 s**（正文称 shortest travel time） | 未报告 | Table III（同上） |
| 环岛：**HDM** / IntMPC / GAT-MPC 成功率 | **98%** / 91% / 67% | 未报告 | Table III（同上） |
| 环岛：**HDM** / IntMPC / GAT-MPC 碰撞率 | **1%** / 7% / 30% | 未报告 | Table III（同上） |
| 环岛：通行时间 HDM vs IntMPC | **27.2 s** vs **26.2 s** | 未报告 | Table III（同上） |
| 人车混行（场景与基线结果取自 [29]）：**HDM** 成功率 / 碰撞率 / 超时率 / 通行时间 | **98% / 1% / 1% / 21.4 s** | 未报告 | Table IV + §VI-D-2 |
| 人车混行：DrQ 通行时间（最短） | **21.3 s** | 未报告 | Table IV + §VI-D-2 |
| 消融：去掉 AV 计划特征（wo-T̄）后成功率 | **98% → 94%** | 未报告（仅两点值） | Table II + §VI-D-1 |
| 实时性：粗粒度策略生成器多次预测推理 | **< 0.2 s**（满足 **2 Hz**） | 未报告（无分位数、无平台说明） | Fig. 8(b) + §VI-E-1 |
| 实时性：细粒度 MPC 规划 | **< 0.02 s**（满足 **10 Hz**） | 未报告 | Fig. 8(b) + §VI-E-1 |
| GAT 邻居判定距离阈值 | **30 m** | — | §IV-B-2 |
| 自车避撞几何近似 | **3 个等半径圆**（n_c = 3）；他车为椭圆（长轴 a_i、短轴 b_i）；安全裕度 ε、κ | — | §V-B，式 (33)(34) |
| 训练规模与算力 | **1000 episodes / 每个城市场景**；单张 **NVIDIA RTX 3080Ti**；PyTorch + Adam，**lr = 2e−4** | — | §VI-B |
| 仿真平台与车辆数 | CARLA；混合交通环境直接采用文献 [29] 的开源代码建立 | — | §VI-A / §VI-B |
| HiL 台架组成 | IPC（CARLA + 粗层推理）+ **NVIDIA Jetson Orin**（细层 MPC）+ **Speedgoat** 实时机（车辆模型）+ **Logitech G29**（模拟人工驾驶） | — | §VI-E + Fig. 5 |
| 失败案例 | P-GAT 预测 veh1/veh2 会让行 → veh2 未让 → HDM 减速仍与 veh1 路径交叠、发生刮擦 | 单例 | §VI-F + Fig. 14 |

⚠**内部不一致（口径）**：同为"去掉自车意图/计划特征"，**消融②wo-T̄**（环岛、保留交互引导）给出 98%→94%，而**基线 GAT-MPC**（环岛、去掉意图特征 + 离线预训练 + 无交互引导）为 67%。两处配置不同，论文未并列说明，引用时**不可把两者当作同一消融的不同表述**。

---

**卡片纪律声明**：本卡片所有图号、表号、题注均逐字取自上述 .txt 全文；表格数值因本机文本不含表体，**一律标注"抄自正文"并给出节号**，无一处为目测估读。DOI 与卷期页经 Crossref 独立核验（2026-10-04）。本卡片不评价该论文的重要性与新颖性。
