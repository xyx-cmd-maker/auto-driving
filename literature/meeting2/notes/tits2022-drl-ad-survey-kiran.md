# DRL 自动驾驶综述（IEEE 正式版）｜Deep Reinforcement Learning for Autonomous Driving: A Survey

- **出处**：IEEE Transactions on Intelligent Transportation Systems, vol. 23, no. 6, June 2022, pp. 4909–4926 ｜ **类型**：综述
- **作者**：B Ravi Kiran et al.（Kiran, Sobh, Talpaert, Mannion, Al Sallab, Yogamani, Pérez）
- **DOI**：10.1109/TITS.2021.3054625
- **全文来源**：`literature/fulltext/meeting2/deep-reinforcement-learning-for-autonomous-driving-a-survey__db81b4cc.txt`（**IEEE 正式版**；arXiv 预印本 `...__c542597e.txt` 不用，符合"以正式版为准"）
- **分组**：TITS
- **证据等级初判**：D 级 — 非系统检索：无检索式（仅在 Fig. 2 借用 Dimensions 平台的出版物趋势图）、无纳入/排除标准、无筛选流程；四张表全部为图像，文本层未提取。按本卡规则作"观点/汇编"处理。
- **档位建议**：B 略读 — 与 P1 的 DRL 基线族相邻，其**RL 算法族谱 + LfD/IRL 边界 + 部署挑战（验证、sim2real、样本效率、安全）**四块可直接用于 P1 的 Related Work 与 Limitations；但**场景重心在城市/混合 ODD**，不提供 P1 可对标的闭环协议。
- **五维打分**：D1=1 D2=1 D3=2 D4=2 D5=2 → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = 13

## 1. 标题
Deep Reinforcement Learning for Autonomous Driving: A Survey｜自动驾驶的深度强化学习：综述

## 2. 摘要（中文）
随着深度表示学习的发展，强化学习（RL）已成为能在高维环境中学习复杂策略的学习框架。本综述总结 DRL 算法，并给出**自动驾驶任务的分类学**（哪些任务已采用 (D)RL），同时讨论真实世界部署中的关键计算挑战。文章还划出**相邻但非经典 RL** 的领域——行为克隆（BC）、模仿学习（IL）、逆向强化学习（IRL）。此外讨论了仿真器在训练智能体中的作用、验证/测试方法、以及使现有 RL 方案更鲁棒的手段。摘要未给出任何性能数字，也未给出检索协议。

## 3. 结论（中文）
作者结论（§VII）：RL 在真实自动驾驶中仍是**新兴**领域，**文献很少、缺大规模公开数据集**。自动驾驶需协商与动态决策，故适配 RL；但成熟仍有诸多挑战（§VI）：**验证、仿真—现实差距、样本效率、奖励函数设计、把安全纳入决策型 RL**。作者强调"RL 结果通常难以复现，且对超参数高度敏感，而这些超参数往往未被详细报告"，故用 Table III 汇总开源框架。最后指出**显式 MARL 是重要但关注不足的方向**。

**自承未解问题**：超参数各异致解读不一致（引 [115]）；sim2real 三路线覆盖不足；**Chauffeurnet [134]：3000 万条状态—动作样本仍不足以学到 BEV→控制最优策略**；安全（Safe DAgger、约束 MDP、SORL）。

## 4. 方法一句话
RL 算法族谱 → 任务分类学（Table I）→ 工具链与仿真器清单 → 部署挑战缺口清单。

## 5. 图表清单（占位符）
全文共 **4 个 Figure + 4 个 Table**（合计 8 个，全部收录）。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-KIRAN-1} | Fig. 1 | Standard components in a modern autonomous driving systems pipeline listing the various tasks. The key problems addressed by these modules are Scene Understanding, Decision and Planning. | 从传感器流到控制执行的完整流水线；本文用"Scene Understanding / Decision / Planning"三词概括关键问题。P1 声明模块边界时可引此图。 |
| {FIG-KIRAN-2} | Fig. 2 | Trend of publications for keywords 1. "reinforcement learning", 2. "deep reinforcement", and 3. "reinforcement learning" AND ("autonomous cars" OR "autonomous vehicles" OR "self driving") for academic publication trends from this [13]. | **本文唯一的"检索式"痕迹**：三条关键词组合 + Dimensions 平台（引 [13]）的出版物趋势。**无命中数、无筛选流程图**；引用"趋势"陈述时须以此为界。 |
| {FIG-KIRAN-3} | Fig. 3 | A graphical decomposition of the different components of an RL algorithm. It also demonstrates the different challenges encountered while training a D(RL) algorithm. | RL 组件的图形化分解 + 训练中遇到的挑战；与 MDP 五元组 <S, A, T, R> 及式 (1)(2) 配套。 |
| {FIG-KIRAN-4} | Fig. 4 | Bird Eye View (BEV) 2D representation of a driving scene. Left demonstrates an occupancy grid. Right shows the combination of semantic information (traffic lights) with past (red) and projected (green) trajectories. The ego car is represented by a green rectangle in both images. | BEV 中层表示：占用栅格 vs 语义 + 过去/预测轨迹；作者主张 BEV "sensor agnostic 但保留道路空间布局"，而图表示做不到。 |
| {TAB-KIRAN-1} | TABLE I | LIST OF AD TASKS THAT REQUIRE D(RL) TO LEARN A POLICY OR BEHAVIOR | **本文对 P1 最有价值的表**（任务级分类学）。⚠ **表体在 PDF 中为图像，文本层未提取到任何行内容**。可由 §V 正文推得的任务族（**非表中原样行标题，须补取后方可逐字引用**）：controller optimization；path planning and trajectory optimization；motion planning and dynamic path planning；high-level driving policies for complex navigation tasks；scenario-based policy learning for highways, intersections, merges and splits；reward learning with IRL from expert data for intent prediction；safety-ensuring policies and risk estimation。 |
| {TAB-KIRAN-2} | TABLE II | SIMULATORS FOR RL APPLICATIONS IN ADVANCED DRIVING ASSISTANCE SYSTEMS (ADAS) AND AUTONOMOUS DRIVING | **P1 选平台时最该先看的表**（高保真感知仿真器，具备相机/LiDAR/雷达模拟能力）。⚠ **表体为图像，未提取**。正文可确证在表中的条目（†=从 §V-C 与参考文献表交叉确证）：CARLA [94]†、Flow [103]†、TORCS [96]†、AirSim [97]†、Gazebo/ROS [98]†、SUMO [99]†、Unity [148]、Deepdrive [100]、NVIDIA Drive Constellation [101]、MADRaS（基于 TORCS 的多智能体仿真器）[102]、MIT-DeepTraffic [110]、CARLA Challenge [107]；另有泛化引用 [105]（感知系统与仿真器系统综述）。**行名与列名须按 §7 动作 1 补取后核对。** |
| {TAB-KIRAN-3} | TABLE III | OPEN-SOURCE FRAMEWORKS AND PACKAGES FOR STATE OF THE ART RL/DRL ALGORITHMS AND EVALUATION | **P1 复现纪律的直接工具**（作者用它回应"RL 结果难复现、超参数常不报告"）。⚠ 表体为图像，未提取。正文可确证的条目：OpenAI Baselines [147]、TF-Agents [149]、rlpyt [150]、Behaviour Suite for RL [151]、Unity [148]。 |
| {TAB-KIRAN-4} | TABLE IV | ACRONYMS RELATED TO REINFORCEMENT LEARNING (RL) | 附录缩写表；首页脚注 1 明确"本文主要缩写见附录（Table IV）"。⚠ 表体为图像，未提取。 |

### 5.1 分类学表格行标题（额外要求：必须完整收录）
本文的**任务分类学表 = TABLE I**。⚠ 其**表体在 PDF 中被渲染为图像，本机 .txt 文本层未提取到任何一行**；上表 {TAB-KIRAN-1} 行中给出的任务族是**从 §V 正文首段回推**，原文为：

> "Autonomous driving tasks where RL could be applied include: controller optimization, path planning and trajectory optimization, motion planning and dynamic path planning, development of high-level driving policies for complex navigation tasks, scenario-based policy learning for highways, intersections, merges and splits, reward learning with inverse reinforcement learning from expert data for intent prediction for traffic actors such as pedestrian, vehicles and finally learning of policies that ensures safety and perform risk estimation."

**结论：TABLE I 的行标题未从全文取得，本卡不伪造。** 须按 §7 动作 1 从 PDF 提取后方可逐字使用。同理，TABLE II（仿真器）与 TABLE III（框架）的行标题亦须补取。

## 6. 对 P1 的用处

- **与 P1 的关系**：**相邻问题**。同属 DRL 决策/控制族（覆盖 P1 基线③ TD3 直控的方法族），但其 ODD 重心是**城市道路 + 交叉口 + 混合场景**，且明言"自动驾驶任务分类学"，不针对高速主线编队。

- **可迁移**：
  1. **受控术语与边界界定（P1 最强的一项可迁移资产）**：本文把 **BC / IL / IRL 明确划为"相邻但非经典 RL"**，并给出可逐字引用的定义句——BC："Behavior Cloning (BC) is applied as a supervised learning that maps states to actions based on demonstrations provided by an expert."；IRL："Inverse Reinforcement Learning (IRL) is about inferring the reward function that justifies demonstrations of the expert."；GAIL："GAIL trains a policy close enough to the expert policy to fool a discriminator."。**P1 若把学位论文的实车数据用于预训练或对照，必须按此三分法声明自己用的是哪一种**，不得混称"模仿学习/RL"。
  2. **P1 可直接引用的"缺口句"出处**：
     - §VI-A Validating RL Systems："implementations often have varying code-bases and different hyper-parameter values, and that unprincipled ways to estimate the top-k rollouts could lead to incoherent interpretations on the performance of the reinforcement learning algorithms, and further more on how well they generalize."（**P1 主张"同等调参预算 + 多种子 + mean±std"的动机句**）
     - §VII Conclusion："Reinforcement learning results are usually difficult to reproduce and are highly sensitive to hyper-parameter choices, which are often not reported in detail."（**同上，更适合放在 Limitations 或 Experiment Setup 开头**）
     - §VI-D Exploration Issues With Imitation："even 30 million state-action samples were insufficient to learn an optimal policy that mapped bird-eye view images (states) to control (action)"（引 Chauffeurnet [134]）——**P1 说明"数据量不等于策略质量"的现成引用**。
     - §VI-G MARL："the continued development of explicitly multi-agent approaches to learning to drive autonomous vehicles is an important future research direction"；"One important area where MARL techniques could be very beneficial is in high-level decision making and coordination between groups of autonomous vehicles, in scenarios such as **overtaking in highway scenarios** [146], or negotiating intersections without signalised control."（**P1 的 OTF 编队协调可直接引这句作为 gap 的前置证据**）
  3. **RL 算法族谱（术语表）**：DQN / Double DQN / Dueling / DRQN(LSTM+DQN) / DDPG / A3C / A2C / SAC / model-based(Dyna-Q, R-max, Dyna-2) / on-off policy。**P1 的 TD3 基线可在"DDPG 系 actor-critic 的确定性策略改进"脉络中定位**（本文述 DDPG："a model-free, off-policy, actor-critic algorithm that can learn policies for continuous action spaces using deep neural net based function approximation"）。注意：**本文未讨论 TD3**，P1 不能引本文作为 TD3 的技术来源。
  4. **两条与 P1 直接相关的设计判据**：
     - **奖励整形有原则与无原则之分**（§IV-A）：无原则整形会让"对增广奖励 R′ 最优的策略未必对原奖励 R 最优"，作者举的经典反例是**自行车智能体为保持直立而原地转圈**；有理论保证的两类是 **difference rewards (D)** 与 **potential-based reward shaping (PBRS)**。⚠ **这条与 P1 的 OTF 势场直接相关**：若 OTF 势场以奖励整形形式注入，**应优先论证它属于 PBRS 形式（势函数差分）**，否则须自认是启发式整形并做 A1 消融。这是一个可在稿件中主动防守的方法论要点。
     - **状态空间设计**（§V-A）：常用状态含自车位置/航向/速度、占用栅格、车道号、路径曲率、过去与未来轨迹、TTC、交通法规与信号位置；并给出"原始传感器数据信息更细但复杂 ↔ 抽象数据复杂度低"的取舍，以及 BEV 作为中层表示。**P1"同等可用信息"的公平性声明可对照此清单逐项核对。**
  5. **仿真器与框架清单**（Table II/III）：为 P1 记录 CARLA 版本与选定基线提供外部参照；Table III 可作为"RL 结果可复现性"的引用出处。
  6. **多保真度 RL（MFRL）**：§V-C 记 [106] 用**逐级提升保真度的仿真器级联**，在**遥控小车**上以更少真实样本找到近最优策略。**P1 若规划 CARLA→实车（或回放）的两段式实验，这是一个可引的方法论模板**。

- **不可迁移 / 陷阱**：
  1. **ODD 差异（最大陷阱）**：本文任务分类表中的"crossing intersection"、"merging into highways"、"negotiating intersections without signalised control"、城市 BEV 感知表示等，均**不是** P1 的"高速主线多车道人工—自动混行编队"ODD。**不得**用本文的任何交叉口/城市结论支撑 P1。
  2. **本文覆盖的是"任务级"而非"协议级"**：它没有给出任何可对标的闭环评价协议（无场景数、无初始条件分布、无失败分类、无成功率区间）。**P1 不能引本文作为评价协议的来源**。
  3. **四张表全部缺失**：TABLE I–IV 的行内容在本机文本中**完全取不到**。任何"本文列了 N 个任务/本文列出的仿真器有 X"这样的具体断言，**补取前不得写入**。
  4. **未覆盖 TD3、未覆盖编队/队列稳定性**：本文的算法清单止于 SAC、ACER 等；**没有 TD3、没有 string stability、没有 platooning 控制**。P1 的编队稳定性主张必须另找来源（可回到黄梦圆学位论文与 CfC 原文）。
  5. **"安全"只到方法罗列，无合规含义**：本文提到 Safe DAgger、约束 MDP、SORL、安全层（safety layer）等，作者自承"full functional safety coverage can not be guaranteed"。**P1 不得据此声称符合 ISO 26262 / SOTIF**（与 `auto-driving/AGENTS.md` §4 一致）。
  6. **商业应用表述不可外推**：§VII 称"there are a few successful commercial applications"，但**未给任何可核验的案例或数字**——不得引用该判断作为"DRL 已量产"的证据。
  7. **与同组第 2 篇（Aradi, T-ITS 23(2)）高度重叠**：两篇均为 DRL + 自动驾驶综述。**必须分工引用**，否则同一错误可能在 P1 与 P2–P5 中共源复现（见 `auto-driving/AGENTS.md` §8 末条）。建议分工：**Aradi = 运动规划四层级 + RL 设计要素（观测/动作/奖励）+ 计算量量级**；**Kiran = RL/DRL 算法族谱 + LfD/BC/IRL 边界 + 部署挑战（验证/sim2real/样本效率/安全/MARL）+ 工具与仿真器清单**。

- **引用时必须带的限定语**：
  "在 Kiran 等对自动驾驶 DRL 的综述（**IEEE T-ITS 23(6) 2022 正式版**；其分类学覆盖的任务以城市道路与交叉口场景为主，且**未讨论 TD3、未涉及编队队列稳定性**）中，作者指出 RL 结果通常难以复现且对未详细报告的超参数高度敏感，并明确 BC/IL/IRL 属相邻而非经典 RL 算法；该综述**未提供可对标的闭环评价协议**，其结论不覆盖高速公路主线人工—自动混行编队控制。"

## 7. 缺失信息（可执行动作）
1. **补 TABLE I–IV 表体（最高优先）**：当前 .txt 中四表仅存图注。→ 动作：定位原始 PDF（`SOURCE_PDF: TITS (IEEE Transactions on Intelligent Transportation Systems)/Deep_Reinforcement_Learning_for_Autonomous_Driving_A_Survey.pdf`），提取 TABLE I（任务清单）、TABLE II（仿真器，含是否支持相机/LiDAR/雷达/车辆动力学等列）、TABLE III（框架清单）的全部行；落盘 `literature/notes/kiran-tables.tsv`。**取得前禁止引用任何单元格内容。**
2. **核验 Fig. 2 的趋势数据来源与口径**：图中引 [13] = Dimensions 平台（访问日期 2020-10-01）的三条关键词曲线。→ 动作：确认图中是否含纵轴数值/年份范围；若 P1 要写"DRL 在自动驾驶中的研究增长"，须改用本项目自己的一次可核验检索（OpenAlex/Crossref，记录检索式与日期），**不得引用本图作为"最新"证据**（违反 §2.1 T1/T3）。
3. **核验 [90]（全尺寸实车 DDPG 车道跟随）**：§V-B 记"an application of DRL (DDPG) for AD using a full-sized autonomous vehicle… trained in simulation, before being trained in real time using on board computers, and was able to learn to follow a lane, successfully completing a real-world trial on a **250 metre section of road**"。→ 动作：取 [90] 完整条目，确认发表venue、车辆平台、闭环/开环、里程与接管情况。**P1 若要引"DRL 已上真车"必须核验，且须注明 250 m 属极短暴露量。**
4. **核验 Table II 中 CARLA 条目的版本与能力列**：→ 动作：提取表中 CARLA 行，确认其标注的能力（相机/LiDAR/雷达/车辆动力学）与本项目实际使用的 CARLA 版本是否一致；P1 的资源类指标须记录采集平台与档位（`AGENTS.md` §3）。
5. **核验 PBRS / difference rewards 的原始出处**：本文 §IV-A 引 [51]（未被证明？）作为 PBRS 来源。→ 动作：取 [51] 完整条目（作者、venue、年份），并在 Crossref 核验；若 P1 要用"OTF 势场属 PBRS 形式"这一防守论点，**必须以原始 PBRS 定理为准而非本综述的转述**。
6. **核验 arXiv 预印本与 IEEE 正式版的差异（引用版本纪律）**：本卡用正式版 `__db81b4cc.txt`；预印本 `__c542597e.txt` 未读。→ 动作：若 P1 引用本文的具体判断句，**页码一律按 IEEE 正式版（pp. 4909–4926）标注**，不得混用预印本编号。
7. **撤稿/更正检查（T5）**：→ 动作：用 DOI `10.1109/TITS.2021.3054625` 查 Crossref `api.crossref.org/works/10.1109/TITS.2021.3054625` 的 `update-to` 字段，记录返回与日期。（本卡未执行该检查，属未完成项。）

## 8. 关键数字（只抄论文明确印出的表格/正文）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 全尺寸实车 DDPG 车道跟随的实路测试长度 | **250 米**路段 | 单一报告，未给里程/接管/重复次数 | §V-B（引 [90]） |
| 模仿学习所需样本量的反面证据 | **3000 万（30 million）**条状态—动作样本仍不足以学到 BEV→控制的最优策略 | 引 [134] Chauffeurnet，单一来源 | §VI-D |
| 域适配用于抓取的样本效率（域外类比） | 真实世界样本减少 **50 倍**而性能可比 | 引 [117]，属机器人抓取而非驾驶 | §VI-B |
| 分层/模块数（AD 流水线） | 4 个功能块：perception / localization & mapping / planning & driving policy / control | — | §II、Fig. 1 |
| 运动规划四层分解的引用来源 | 引 [3]（Paden 等 T-IV 2016） | — | §III-A 前引 |
| RL 算法族清单（本文覆盖） | DQN, Double DQN, Dueling, DRQN, DDPG, A3C, A2C, SAC, Dyna-Q, R-max, Dyna-2, SARSA, Q-learning, ACER, TRPO, PPO | — | §III–§IV、§VI-C |
| 本文的 MDP/POMDP 形式化 | 单智能体 MDP = <S, A, T, R>；随机博弈 SG = <S, A₁…N, T, R₁…N> | — | §III、§IV-B |
| 参考文献条数 / 页数 / 图数 / 表数 | **151** 条（[1]–[151]）；18 页（pp. 4909–4926）；4 图；4 表 | — | 全篇统计 |
| 检索证据 | **无检索式**；仅 Fig. 2 三条关键词组合的出版物趋势（来源 Dimensions [13]，访问 2020-10-01） | 无命中数、无纳入/排除标准 | Fig. 2 图注、§I |
| 论文成稿时间线 | 收稿 2020-03-24；修回 2020-10-13；录用 2021-01-15；在线 2021-02-09；卷期 2022-05-31 | — | 首页脚注 |

⚠内部不一致（**已核验，须修正引用方式**）：§V-B 以 "Recent work by authors [89] contains real world motions by various traffic actors, observed in diverse interactive driving scenarios." 引 [89]，但参考文献 [89] 实为 **W. Zhan et al., "INTERACTION dataset: An INTERnational, adversarial and cooperative moTION dataset in interactive driving scenarios with semantic maps," 2019, arXiv:1910.03088**（**预印本**数据集论文，非正式发表版），**不是**"某作者团队的实车运动工作"。同段紧接着的 "DRL (DDPG) for AD using a full-sized autonomous vehicle [90]" 对应 **[90] A. Kendall et al., "Learning to drive in a day," in Proc. ICRA, May 2019, pp. 8248–8254**（与 §V-B 所述"仿真训练→车上实时训练→250 m 实路"一致）。→ **本文正文多处"引文编号 ↔ 所述内容"的对应关系需逐条回溯原始文献核验**（见 §7 动作 3）；**引用本文转述的具体论文结论时，不得以本文转述为准**；且 [89] 若要在 P1 中引用，须改用 INTERACTION 数据集正式发表版或标注为预印本。
