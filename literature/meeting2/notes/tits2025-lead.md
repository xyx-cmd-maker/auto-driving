# 学习增强的自适应行为决策（LEAD，非合作博弈 + 最大熵 IRL）｜LEAD: Learning-Enhanced Adaptive Decision-Making for Autonomous Driving in Dynamic Environments

- **出处**：IEEE Transactions on Intelligent Transportation Systems, Vol. 26, No. 5, May 2025, pp. 6142–6156 ｜ **类型**：期刊论文（方法 + 自然驾驶数据集 + 实车平台数据验证）
- **作者**：Heye Huang et al.（第一作者 Heye Huang，清华大学车辆与运载学院；通讯作者 Boqi Li、Jianqiang Wang）
- **DOI**：10.1109/TITS.2025.3531293（Crossref `works/10.1109/TITS.2025.3531293`，取用日期 2026-10-04：命中，题名一致，Vol. 26 / Issue 5 / pp. 6142-6156 一致，`relation` 为空 → 未见更正或撤稿标记）
- **全文来源**：`literature/fulltext/meeting2/lead-learning-enhanced-adaptive-decision-making-for-autonomo__100aeee1.txt`（本机文本 72,742 字符 / 15 页）
- **分组**：TITS
- **证据等级初判**：**B 级** — 设计良好但有明确边界：highD/exiD 两个德国高速自然驾驶数据集（1,738 序列 / 1,550 训练 + 188 测试）+ 三车实车平台 13 组可用换道数据，指标逐项给出；但**无置信区间、无显著性检验**、无代码、**实车部分是数据采集 + 离线一致性比对而非闭环控车**，且只有 25→13 个小样本。
- **档位建议**：**B 略读** — 与 P1 的关系在**决策层与论证层**而非控制器层：① 它给出**高速（含匝道合流）ODD 下人类似度评价协议**与实车数据采集流程；② 它的 Related Work **对"势场类方法"给出本组唯一一条正面批评**（参数多、参数选取与优化困难、难以适应动态交通），P1 的 Introduction/风险登记表**必须回应**这条；③ 它指出博弈类方法"未考虑人类驾驶中的隐性社会影响、目标函数缺乏人类似度"——**可反过来支撑 P1 以 OTF 作为"交通社会压力"标量的动机**。
- **五维打分**：D1=1 D2=2 D3=1 D4=2 D5=1 → 加权 = 3·1+2·2+2·1+1·2+2·1 = 3+4+2+2+2 = **13 / 20**（B 档区间 9–13 的上沿；因 D1=1 不能进 A 档）
- **未命中** `00-triage-protocol.md` §3 排除词表（ODD 为高速公路主线 + 匝道合流，非交叉口/环岛/城市无信号/行人/停车）。

---

## 1. 标题

LEAD: Learning-Enhanced Adaptive Decision-Making for Autonomous Driving in Dynamic Environments｜中文直译：LEAD——动态环境下自动驾驶的学习增强自适应决策

## 2. 摘要（≤400 字中文，保留关键数字与结论成立条件）
针对动态合流场景中自车与人工驾驶车的高度交互，本文提出 LEAD 框架。为刻画交互的竞争性与策略性，建立基于非合作博弈的行为模型：行为建模为动态博弈，每辆车用多因素奖励函数独立优化动作，动作空间为让行与不让行，用混合策略求均衡；再用最大熵逆强化学习做特征匹配以标定奖励权重，并用贝叶斯网络建立环境变量到最优权重的映射模型，实现参数在线学习与识别，输出交互行为概率。验证用 highD 与 exiD 自然驾驶数据集（25 Hz、位置误差小于 10 cm）与实车平台数据（三辆车，高速约 80 km/h）。关键数字：188 个测试序列、11,583 个数据点上人类似决策相似率 81.73%（匹配 9,467 点），highD 子集 83.12%；145 个动态交互序列、8,964 点上为 77.12%（匹配 6,913 点）；实车 72.73%，可变交互场景 69.84%，安全违规率 0%。结论成立条件：ODD 限于高速匝道合流与换道、二元让行决策、两车强交互配对建模。

## 3. 结论（≤350 字中文）
作者结论：以匝道合流这一不确定且复杂的交互为案例，提出 LEAD，用非合作博弈把交互建模为动态博弈、用最大熵逆强化学习优化行为模型参数，并建立环境变量到模型参数的映射以适应实时交通。基于 highD、exiD 与实车试验验证：静态测试场景平均人类似决策相似率 81.73%、动态交互场景 77.12%、实车 72.73% 且无安全违规。作者自承局限：高速匝道合流场景在真实高速上难以复现，外部车辆会破坏试验条件、真实驾驶员的固有协调也约束验证；实车 25 个换道样本中仅 13 个完整可用；方法在数学上只建模两车强交互，多车需拆成配对再扩展交互对象矩阵，未做实验；验证场景主要限于合流，T 型口与路口左转仅为理论上的可迁移，只给示意图；未来工作含扩展到骑行者与行人。

## 4. 方法一句话（≤60 字）

环境变量（Δd_x, Δd_y, Δv_x, ΔD_a）→ 非合作博弈 + 最大熵 IRL 标定权重 + 贝叶斯网络映射在线匹配 → 让行/不让行概率。

## 5. 图表清单（占位符）

> 全文共 **16 个 Figure + 2 个 Table = 18 项**（另有 Algorithm 1"Model Parameters Optimization Method"，非图非表，不计入），超过 12；下表覆盖**按出现顺序的前 12 项**，剩余 6 项见补充表。
> ⚠ 与前两篇相同的材料事实：本机 .txt **只有题注、没有表格单元格数值**；但本文**主结果数值在正文逐句给出**，下表已抄录并标注出处为正文。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-LEAD-1} | Fig. 1 | Example of a dynamic interactive process in merging scenario. | 动机图：周边车辆运动状态不确定、交互行为随机时，AV 更难实现避撞与合理驾驶；用于引出"合流场景既高交互又常见"的选题 |
| {FIG-LEAD-2} | Fig. 2 | Overview of the proposed learning-enhanced adaptive decision-making (LEAD) framework for AVs. Here, “env” represents environmental input, qt 0 denotes the final decision behavior, λt 0 and λt 1 are the optimal weight factors for vehicles P0 and P1 in the reward functions. | 五步总览：① 从数据集抽 vehicle ID/位置/速度 → ② 交互行为标定 → ③ 非合作博弈行为模型 → ④ 最大熵 IRL 参数优化 → ⑤ 离线+在线自适应决策机制 |
| {FIG-LEAD-3} | Fig. 3 | Illustration of basic model elements of vehicle dynamic interaction. | 模型四要素：参与者 P={P₀,P₁}、动作空间 Q={Yield, NYield}、奖励函数 U、混合策略解 σ |
| {FIG-LEAD-4} | Fig. 4 | Illustration of vehicle interaction and reward function design process. | P₀ 与匝道车 P₁ 在"直行交互阶段"的中等冲突；对应式 (1)(2) 的奖励项与归一化因子（t_N 5–10 s、v_N 高速 100–120 km/h、D_N 50–150 m） |
| {FIG-LEAD-5} | Fig. 5 | Vehicle adaptive behavior decision-making process based on offline and online learning. | 离线：权重因子学习（特征匹配）+ 最大熵 IRL；在线：以实时环境数据 Eᵗ 查询映射模型 Mλ 取最优权重 → 求解行为模型 → 输出 σ₀ᵗ 并取最大似然动作 |
| {FIG-LEAD-6} | Fig. 6 | The structure of mapping model based on Bayesian network. | 隐变量 H₁/H₂ = 权重因子 λ₀/λ₁；M₁/M₂ = 混合高斯参数；可观测变量 {O₁,O₂,O₃} = {Δd_y, Δv_x} / {Δd_x} / {ΔD_a, Δv_x¹} |
| {FIG-LEAD-7} | Fig. 7 | Dataset Preparation. (a) dataset collection, (b) highD dataset and (c) exiD dataset. | 数据来源与预处理：**25 Hz（每 40 ms）**、无人机 HD 相机航拍、位置测量误差 **<10 cm** |
| {FIG-LEAD-8} | Fig. 8 | The state evolution of the traffic environment with vehicle ID 782. | 典型算例：匝道车 ID 782 的状态演化；其驾驶意图由既有模型分析 |
| {FIG-LEAD-9} | Fig. 9 | Interaction behavior calibration of vehicle ID 782. (a) Interaction time calibration. (b) Acceleration and calibration results and (c) jerk description. (d) Parameter learning results of vehicle P1 and (e) learning results of vehicle P0. | 标定规则：纵向加速度 a_x < 0 → 让行；a_x > 0 时看 jerk ẋ_a——正 jerk = 不让行、负 jerk = 让行。结果：**P1 收敛到不让行（概率 = 1），P0 收敛到让行（概率 = 1）**，与标定一致 |
| {FIG-LEAD-10} | Fig. 10 | The state evolution of the traffic environment with vehicle ID 278 (blue) approaching the interactive vehicle in the merging zone. | 第二个算例：ID 278 在合流区的状态演化；该阶段结束后 P1 在 P0 前方完成换道 |
| {FIG-LEAD-11} | Fig. 11 | Interaction behavior calibration of vehicle ID 278. (a) Interaction time calibration. (b) Acceleration and calibration results and (c) jerk description. (d) Parameter learning results of vehicle P1 and (e) learning results of vehicle P0. | 自适应决策算例：环境变量逐时刻输入映射模型 → 取自适应参数 → 生成自车与交互车行为概率；正文称其与标定结果"高度相似" |
| {TAB-LEAD-1} | TABLE I | MODEL PERFORMANCE IN DIFFERENT SCENARIOS | ★**主结果表 A（数据集上的性能）**。**表体数值在本机文本缺失；下列数值抄自 §V-C-2 正文**。测试集：**188 个测试序列 / 11,583 个数据点**；其中 **145 个序列具有交互动态 / 8,964 个数据点**。**本文方法：人类似决策相似率 81.73%（9,467 个匹配点）**；**highD 子集 83.12%（2,316 点，1,925 匹配）**；**动态波动交互场景 77.12%（6,913 匹配点）**。指标定义：① human-like decision similarity；② adaptive similarity in varied interaction scenarios。**无 CI、无显著性检验** |

**>12 的剩余 6 项（按出现顺序）**

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-LEAD-12} | Fig. 12 | Results of vehicle interaction behavioral model under the first/second fixed parameters. (a) (d) Behavioral decision-making results of P1 and (b) (e) behavior prediction results of P0. (c) Acceleration and calibration results of vehicle 429 (P1) and (f) parameter learning results for vehicle P1. | **对照设置**：固定参数 `[0.8, 0.2, 0.8, 0.2]` 与 `[0.2, 0.8, 0.2, 0.8]` 作为基准；算例车 ID 429。正文称本文方法"closely resembles the calibrated interaction behavior outcomes" |
| {FIG-LEAD-13} | Fig. 13 | Real-vehicle test platform and road section overview. | 实车平台与路段：**三辆车 Toyota Prius / Buick GL8 / BMW i3**；硬件含 R60S-U 接收机、双卫星天线、D20 组网模块；路段为与 highD 场景接近的高速公路 |
| {FIG-LEAD-14} | Fig. 14 | Illustration of the interaction process in real-vehicle test. (a) (b) Real-vehicle field test process. (c) (d) Interaction process description. (e) The spatiotemporal distribution for the three vehicles. (f) Interaction moment determination. | 实车验证三阶段：由换道意图识别概率 >50% 判定交互终止帧 → 对目标车道冲突车标定不让行概率 → 输出行为决策并与人工标定对比 |
| {FIG-LEAD-15} | Fig. 15 | Results of vehicle non-yielding interaction behavior probability under three fixed parameters. (a) The calibration process of non-yielding behavior probability of interactive vehicle. Non-yielding behavior probability: (b) (d) interaction vehicle P1, (c) (e) ego vehicle P0. | 实车情形下的固定参数对照；正文称本文方法输出"closer and similar to the calibration behavior of human drivers"。⚠ 题注写 **three** fixed parameters，正文只给出 **two** 组（见下方 ⚠） |
| {TAB-LEAD-2} | TABLE II | MODEL PERFORMANCE IN REAL VEHICLE EXPERIMENTS | ★**主结果表 B（实车平台）**。**表体缺失；数值抄自 §V-D-2 正文**：**人类似决策相似率 72.73%（测试场景）/ 69.84%（可变交互场景）**；**安全违规率（safety violation rate）= 0**。样本：25 个换道数据 → **13 个完整可用**；车速约 **80 km/h**；三车由**有经验驾驶员**驾驶 |
| {FIG-LEAD-16} | Fig. 16 | The detailed interaction process for different driving cases. (a) Case 1 (b) Case 2. (c) Case 3. (d) Case 4. | 未来工作示意图：T 型口、路口左转、多智能体交互等**理论上可迁移**的场景（**仅示意，无实验数据**） |

## 6. 对 P1 的用处

- **与 P1 的关系**：**相邻问题（决策层 + 论证层）**。P1 是"OTF 势场 + 连续时间神经网络的编队跟车控制"；LEAD 是"非合作博弈 + 最大熵 IRL 的**让行/不让行行为决策**"。两者**不在同一层**：LEAD 输出离散行为标签，P1 输出连续控制量；LEAD 的评价指标是"人类似度"，P1 的指标是控制性能。但 ODD（**高速公路主线 + 匝道合流 + 人机混行**）与 P1 **高度重叠**，且它提供了本组唯一一条对"势场类方法"的正面批评。
- **可迁移（具体到方法/协议/数字/图表）**：
  1. **★ 对 P1 方法类的直接批评（最高价值，必须回应）**：LEAD 的 Related Work 把现有方法分四类——learning-based / probabilistic inference-based / **potential field-based** / game theory-based——并逐字写道："**these models are encumbered by a substantial number of parameters, and the selection and optimization of these parameters present considerable challenges, thereby hindering their adaptation to multiple dynamic traffic**"。P1 的 OTF 势场正属此类。→ **建议动作**：把这条写进 P1 的 Introduction 缺口段与 `audit/第一次组会/03-risk-register.md`（**路径修正**：原文写 `audit/03-风险登记表.md`，该文件实际路径与文件名均不同；2026-10-08 由 SUMO 环境线分支按 `AGENTS.md` §0 路径纪律更正），并显式回应（OTF 是**一阶标量**而非高参数化势场、参数来自学位论文实车数据标定而非人工枚举）。这是 reviewer 最可能提出的质疑之一。
  2. **★ 反向支撑 P1 的 OTF 动机**：LEAD 对博弈类方法的批评是"**Limited consideration of factors like hidden social influences in human driving** and the lack of human-like behavior similarity in objective functions"。OTF（超车频次）正是"交通社会压力"的标量化尝试 → 可作为 P1 立项动机的**他文引用支点**（"现有博弈类方法自承未考虑隐性社会影响"）。
  3. **"参数作为环境条件的函数"这一范式**：LEAD 的 Mλ（环境变量 → 最优权重 λ）与 P1 把 OTF 势场作为**结构条件/归纳偏置**注入控制器，在**方法论形态上同构**（都是"用环境条件调制模型参数"）。可作为 P1 术语选择的旁证（structure-conditioned / prior-informed，而非 physics-informed）。
  4. **人类似度评价协议**：`human-like decision similarity = 匹配实例数 / 总实例数`（本文以数据点计）与 `adaptive similarity in varied interaction scenarios` 两个指标的定义（§V-C-2 逐字给出），若 P1 需要报"类人性"或"是否符合人类驾驶习惯"的辅助指标，可直接引用其定义与量级（81.73% / 77.12% / 72.73%）作为参照带。
  5. **实车数据采集与标定流程**：三车（P0 目标车道 / P1 交互车 / P2 前车）+ 双操作员 + 高速约 80 km/h + 25→13 样本的筛选口径，以及"以换道概率 >50% 判定交互终止帧"的交互切分规则——可作为 P1 未来做实车数据采集时的**流程模板**（并直接看到它的样本量有多小）。
  6. **博弈/IRL 作为基线或对照设计**：若 P1 需要一个"非学习型交互决策"对照，LEAD 给出可复现的建模骨架（二元动作 + 混合策略 + 最大熵 IRL 权重标定 + 固定权重对照 `[0.8, 0.2, 0.8, 0.2]` / `[0.2, 0.8, 0.2, 0.8]`）。
- **不可迁移 / 陷阱**：
  1. **"实车试验"的实际内容必须写准**：实车平台的三辆车由**有经验驾驶员驾驶**（"Three test vehicles … are operated by experienced drivers"），验证步骤是"预处理运动数据 → 导出轨迹与环境变量作模型输入 → 标定 P1 交互行为 → 生成并比较行为概率"——即**实车数据采集 + 离线一致性比对**，**不是 LEAD 闭环控车**。全文**无接管率、无控制器输出执行记录、无里程/暴露量**。→ P1 引用时**不得**写"LEAD 已实车闭环验证"；也不得把它的 0% 安全违规率当作控制级安全证据。
  2. **ODD 只重叠一半**：LEAD 是**匝道合流**（ramp merging）的二元让行决策；P1 是**主线编队跟车**。合流是横纵向强交互、跟车是纵向弱交互 → 方法不通用。
  3. **只有两车强交互**：作者自承方法"mathematically models the interaction between two strongly interacting agents"，多车需拆成配对（**无实验**）。P1 的"多车道混行编队"通常是 N 车耦合 → 不可直接套用。
  4. **无 P1 的任何控制指标**：无跟车误差 RMSE、无加速度平方积分、无 Jerk 峰值、无车道居中偏差、无前轮转角方差、无端到端延迟、无 MCU 内存占用。
  5. **样本量与统计**：实车只有 25→13 个换道样本，全部指标无 CI、无显著性检验、无种子说明 → 相似率差异（如 83.12% vs 77.12%）**不可声称显著**。
  6. **参数口径依赖大量人工设定**：λ ∈ [0.1, 1.0]、t_N 取 5–10 s"based on naturalistic driving observations"、v_N 取 100–120 km/h、D_N 取 50–150 m —— 这些是**人工给定区间**，不是学出来的。引用其"参数自适应"时须注意自适应的是**权重 λ**，不是这些归一化因子。
- **引用时必须带的限定语**：**"该文为面向高速公路匝道合流的两车强交互让行决策研究，验证基于 highD/exiD 自然驾驶数据集（自车由 LEAD 决策、交互车按数据集概率模型驱动）与三辆实车的数据采集与离线一致性比对（车辆由有经验驾驶员驾驶，非 LEAD 闭环控车），样本为 188/145 个测试序列与实车 13 组可用换道数据，全部指标为点估计、无置信区间与显著性检验，无法迁移至多车道编队跟车控制。"**

## 7. 缺失信息（可执行动作）

1. **需回原 PDF 抄录 Table I 与 Table II 的完整表体**：包括被比较的方法/参数设置行（固定参数两组？）、每行对应的序列数与数据点数、以及"安全违规率"的分子/分母。（后果：本机文本只有汇总百分比，**无法核验任何一行**；P1 若要把 81.73% 当参照带，必须知道它的分母。）
2. **需澄清实车相似率的分母**：`72.73% = 8/11`（精确整数比），而正文说实车有"**13 个完整可用的数据集**"——**13 不能整除出 72.73%**。请作者说明相似率是按**序列数**还是**数据点数**统计、分母到底是 11、13 还是别的数。（后果：Table II 的两个数字目前**不可复算**，属"分母不明"的点估计。）
3. **需澄清 Fig. 15 题注的 "three fixed parameters"**：正文（§V-C-2 与 §V-D-2）只给出两组固定权重 `[0.8, 0.2, 0.8, 0.2]` 与 `[0.2, 0.8, 0.2, 0.8]`，Fig. 12 题注也写 "the first/second fixed parameters"（两组）。（后果：实车对照到底几组不明；若引用"三组固定参数对照"即与正文不一致。）
4. **需索取 maximum entropy IRL 的超参与收敛判据**：迭代步数、学习率 δ、特征向量定义、收敛阈值、是否做了 λ 的初值敏感性分析。（后果：Algorithm 1 只给出 `λ ← λ − δ × g` 的更新式，无法复现"最优匹配参数"。）
5. **需索取贝叶斯映射模型 Mλ 的规格**：网络结构、混合高斯分量数、训练/测试划分是否固定、离散化分箱数、以及 65,198 个训练数据点与 188 个测试序列的**是否有重叠**（同一 interaction 的不同数据点可能跨训练/测试集）。（后果：若同一次交互的时间点同时进训练与测试，81.73% 会**高估泛化**——这是小样本序列任务最常见的泄漏点，必须问清。）
6. **需索取 safety violation rate 的判定规则**：什么算一次"安全违规"（TTC 阈值？最小间距阈值？），以及 0% 是"13 个样本中 0 次"还是"996 个数据点中 0 次"。（后果：P1 未来若报安全性指标需要同类定义；`AGENTS.md` §4 要求小样本用 Wilson/Clopper-Pearson 区间，本文连分子分母都没给。）
7. **需确认数据/代码可用性**：highD/exiD 为公开数据集（须按各自许可申请），但全文**未出现任何代码或本文实车数据的公开声明**（对全文 grep `github` / `available at` / `open-source code` 无命中）。（后果：判定为"无复现材料"；实车数据不可得。）

## 8. 关键数字（只抄论文明确印出的表格/正文，不得目测估读）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 人类似决策相似率（188 个测试序列 / 11,583 数据点） | **81.73%**（匹配 9,467 点） | **未报告**（无 CI、无 n 的重复、无检验） | Table I + §V-C-2（数值抄自正文） |
| highD 子集相似率 | **83.12%**（2,316 点中 1,925 匹配） | 未报告 | Table I + §V-C-2 |
| 动态交互场景相似率（145 序列 / 8,964 数据点） | **77.12%**（匹配 6,913 点） | 未报告 | Table I + §V-C-2 |
| 实车：测试场景相似率 | **72.73%** | 未报告（**分母与"13 个可用数据集"不闭合**，见 §7 第 2 条） | Table II + §V-D-2 |
| 实车：可变交互场景相似率 | **69.84%** | 未报告 | Table II + §V-D-2 |
| 实车：安全违规率 | **0%**（"no safety violations"） | 未报告（无分子/分母、无判定规则） | Table II + §V-D-2 |
| 交互序列总量 | **1,738** 条（预处理后） | — | §V-A |
| 训练/测试划分 | **1,550** 训练（**65,198** 个数据点）/ **188** 测试 | — | §V-A |
| 数据集采样率与精度 | **25 Hz（每 40 ms）**；位置误差 **<10 cm**；无人机 HD 相机航拍 | — | §V-A + Fig. 7 |
| 奖励权重 λ 取值范围 | λ₀¹, λ₀², λ₁¹, λ₁² ∈ **[0.1, 1.0]** | — | §III-B |
| 归一化因子 | t_N = **5–10 s**；v_N = **100–120 km/h**（高速）；D_N = **50–150 m** | 人工给定区间，非学习得到 | §III-B |
| 固定参数对照（基准） | `[0.8, 0.2, 0.8, 0.2]` 与 `[0.2, 0.8, 0.2, 0.8]`（**两组**；Fig. 15 题注写 three） | — | §V-C-2 / §V-D-2 vs Fig. 15 题注 |
| 交互终止判据 | 匝道车**换道概率 > 50%** 且自车未超越它；或发生超越的时刻 | — | §III-A / §V-A |
| 行为标定规则 | a_x < 0 → 让行；a_x > 0 时按 jerk：**正 jerk = 不让行、负 jerk = 让行** | — | §V-A |
| 实车平台与样本 | 三车 **Toyota Prius / Buick GL8 / BMW i3**；**25** 个换道样本 → **13** 个完整可用；车速约 **80 km/h**；每车 2 名技术操作员；有经验驾驶员驾驶 | — | §V-D-1 / §V-D-2 + Fig. 13 |
| 算例车 ID | 782（参数标定）、278（自适应决策）、429（固定参数对照） | — | Fig. 8–Fig. 12 |
| 可迁移性声称 | T 型口、路口左转、多智能体交互（拆成配对）——**仅示意，无实验** | — | §VI 1)–2) + Fig. 16 |

⚠**内部不一致（固定参数个数）**：Fig. 15 题注写 "under **three** fixed parameters"，而正文 §V-C-2、§V-D-2 与 Fig. 12 题注只给出**两组**固定权重（`[0.8,0.2,0.8,0.2]` 与 `[0.2,0.8,0.2,0.8]`）。二者不可同时成立。

⚠**口径不闭合（实车分母）**：§V-D-2 称实车有 **13** 个完整可用数据集，但相似率 **72.73% = 8/11**（精确），13 无法整除出该值；论文未说明相似率按序列数还是数据点数统计 → 该行数字**不可复算**。

---

**卡片纪律声明**：本卡片所有图号、表号、题注均逐字取自上述 .txt 全文；表格数值因本机文本不含表体，**一律标注"抄自正文"并给出节号**，无一处为目测估读。DOI 与卷期页经 Crossref 独立核验（2026-10-04）。本卡片不评价该论文的重要性与新颖性。
