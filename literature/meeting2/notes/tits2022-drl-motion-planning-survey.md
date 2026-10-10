# DRL 运动规划综述｜Survey of Deep Reinforcement Learning for Motion Planning of Autonomous Vehicles

- **出处**：IEEE Transactions on Intelligent Transportation Systems, vol. 23, no. 2, February 2022, pp. 740–759 ｜ **类型**：综述
- **作者**：Szilárd Aradi（单作者）
- **DOI**：10.1109/TITS.2020.3024655
- **全文来源**：`literature/fulltext/meeting2/survey-of-deep-reinforcement-learning-for-motion-planning-of__c4772609.txt`
- **分组**：TITS
- **证据等级初判**：D 级 — 非系统检索：**有**一份可核验的检索式（Fig. 1 的 Web of Science 主题检索 "Deep Reinforcement Learning" AND "Autonomous vehicles"，检索日期 2020.01.17），但**无纳入/排除标准、无筛选流程图、无文献计数**；两张分类学大表（Table III/IV）在 PDF 中为图像，文本层未提取。按本卡规则作"观点/汇编"处理。
- **档位建议**：B 略读 — 与 P1 的 TD3 直控基线同族（DRL 决策），其"单智能体/多智能体 × 场景"分类框架可直接用于组织 P1 的相关工作与基线定位；但无闭环协议、无代码，不构成 A 档精读。**若按冻结的 `00-triage-protocol.md` 严格执行，本卡加权 9 分落在 B 档下沿（见 §6 说明）。**
- **五维打分**：D1=1 D2=0 D3=1 D4=2 D5=1 → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = 9

## 1. 标题
Survey of Deep Reinforcement Learning for Motion Planning of Autonomous Vehicles｜自动驾驶车辆运动规划的深度强化学习综述

## 2. 摘要（中文）
本文综述 DRL 在自动驾驶运动规划中的应用，覆盖传感器、V2X、安全、决策、控制乃至法规标准化等议题。核心内容是给出**分层运动规划问题**的视角（至少四层：路径规划、行为层、运动规划层、局部反馈控制层）并介绍 DRL 基础；随后逐项讨论系统设计要素：环境建模、建模抽象层级（运动学单车模型 → 3 自由度动力学自行车模型 → 四轮 9 自由度模型）、状态与感知模型描述、恰当的奖励设计、以及底层神经网络的实现。文章还介绍车辆模型、仿真平台（SUMO/VISSIM/TORCS/CarSIM/CarMaker/AirSim/Udacity Gazebo-ROS/CARLA）与**计算量量级**，并按自动驾驶的不同任务与层级系统化梳理现有方案：跟车、车道保持、轨迹跟随、汇入、稠密车流中行驶。最后讨论开放问题与未来挑战。摘要未给出任何性能提升数字。

## 3. 结论（中文）
作者结论（§IV 与收束句）：DRL 能用于运动规划**各层级**，但许多问题未解。① 复杂场景训练**可达百万级步数**，一组超参数或奖励假设实验可持续数小时至数天。② 因此**多数论文只处理细小任务，最复杂场景（如城市交通导航）在文献中找不到**。③ ISO 26262 与 Automotive SPICE **尚未对深度学习给出专门条款**，"复杂场景下无法保证完整的功能安全覆盖"。④ **所评估工作全部在仿真中训练，仅一处例外**（[123] 真车车道跟随）。⑤ "**强化学习本身不足以作为汽车运动规划的工具**"，需结合其它方法。

**自承未解问题**：episode 终止条件；奖励整形缺乏原则；训练/验证环境同源；域随机化维度与保守化；corner case 难选。

## 4. 方法一句话
Web of Science 检索式（2020-01-17）→ 四层级 × 单/多智能体分类 → 缺口清单。

## 5. 图表清单（占位符）
全文共 **13 个 Figure + 5 个 Table**（合计 18 个，超过 12 → 按规则覆盖前 12 个，并列出全部编号）。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-ARADI-1} | Fig. 1 | Web of science topic search for "Deep Reinforcement Learning" and "Autonomous vehicles (2020.01.17.)". | **本文唯一的检索证据**：给出检索式与日期，但无命中数、无纳入/排除标准。P1 引用本文作"趋势"陈述时须以此图为界（截至 2020-01-17）。 |
| {FIG-ARADI-2} | Fig. 2 | Layers of motion planning. | 四层级分解（route planning / behavioral / motion planning / local feedback control）；本文的组织骨架。 |
| {FIG-ARADI-3} | Fig. 3 | The POMDP model for deep reinforcement learning based autonomous driving. | POMDP 五元组 (S, A, T, R, Ω, O) 在自动驾驶中的对应物；建模清单来源。 |
| {FIG-ARADI-4} | Fig. 4 | Observation for basic vehicle state (source: [3]). | 最简观测 (|e|, v, θe)：车道中心线横向偏差、车速、偏航角。P1 的"车道居中偏差"指标与之同源。 |
| {FIG-ARADI-5} | Fig. 5 | Real images from the driving data and their semantic segmentations (source: [72]). | 640×400 分辨率的真实图像与语义分割；sim2real 的域适配中间层。**注意：本文全部为感知/观测侧内容，P1 不涉及**。 |
| {FIG-ARADI-6} | Fig. 6 | The surrounding from the perspective of the vehicle can be described by a coarse perception map where the target is represented by a red dot (c) (source: [78]). | 栅格图观测 + 自车位置/偏航；静态环境导航。 |
| {FIG-ARADI-7} | Fig. 7 | The visualization of the HDM mapping process (source: [57]). | 等距栅格中以格内数值编码邻车纵向速度；**无法表达横向运动**。 |
| {FIG-ARADI-8} | Fig. 8 | The simulator state (top, zoomed in) gets converted to a 4 x 3 x (2 x FoV + 1) input observation tensor (bottom) (source: [10]). | 四通道张量：在路占用、相对速度、相对横向位移、相对航向。结构化观测的代表。 |
| {FIG-ARADI-9} | Fig. 9 | Environment state on the highway [83]. | 6×(dx, dv) 标量向量 + 自车邻道占用；高速机动的最小观测表示。 |
| {FIG-ARADI-10} | Fig. 10 | Path planning results from [89]. | 经典 Q-learning 以 (v, x, y, θ) 为状态做带 Ackermann 转向的路径规划。 |
| {FIG-ARADI-11} | Fig. 11 | Ramp merge: (a) simulated scenario and (b) real-world location (source: [82]). | 匝道汇入场景的仿真与真实地点对照；**属汇入 ODD，非 P1 的高速主线混行**。 |
| {FIG-ARADI-12} | Fig. 12 | Flow-density relations detected by the virtual loops under different strategies (source: [80]). | 合作 vs 非合作策略下的流量—密度图；合作行为带来更高流量、更低总行程时间。**P1 若做混行编队，这是"社会性收益"类证据的模板**。 |
| {FIG-ARADI-13} | Fig. 13 | Conceptual illustrations of three approaches for sim2real transfer (source: [126]). | 系统辨识 / 域适配 / 域随机化三路线。P1 的 CARLA→真实高速差距说明可引此三分类。 |
| {TAB-ARADI-1} | TABLE I | STATE REPRESENTATION DISCRETIZATION IN [85] | 状态离散化档数 (6, 10, 8, 9) → 配 3 个横向动作得 Q 表 12,960 元素。⚠ 表体为图像；**数值取自 §III 正文**。 |
| {TAB-ARADI-2} | TABLE II | ACTION SPACE IN [65] | 6 个动作（含先减速或先逼近目标间隙的变道）。⚠ 表体为图像，未提取。 |
| {TAB-ARADI-3} | TABLE III | SINGLE AGENT APPROACHES FOR MOTION PLANNING IN DIFFERENT SCENARIOS | **本文对 P1 最有价值的表之一**。⚠ **表体在 PDF 中为图像，文本层未提取到任何行内容**；列标题只能从 §III-E 正文推得，逐字为：scenario / model or simulation environment / observation space / action space / elements in the reward function / type of RL agent / neural network。 |
| {TAB-ARADI-4} | TABLE IV | MULTIAGENT APPROACHES FOR MOTION PLANNING IN DIFFERENT SCENARIOS | MARL 版同表，列为：场景 / 模型或仿真环境 / 观测空间 / 动作空间 / **奖励在智能体间的分配** / RL 智能体类型 / 神经网络。⚠ 表体为图像，未提取。 |
| {TAB-ARADI-5} | TABLE V | PROS AND CONS OF USING SIMULATION FOR TRAINING RL | 仿真训练的利弊对照；**§IV-B 结论"多数研究停留在仿真层，仅少数能提供真实世界应用且都有限制"的依据表**。⚠ 表体为图像，未提取。 |

**（全文实为 13 图 5 表；上表覆盖前 12 项并列出其余编号，符合" >12 个覆盖前 12 个"的规则。）**

### 5.1 分类学表格行标题（额外要求：必须完整收录）
两张分类学表（Table III / IV）**表体在 PDF 中为图像，本机 .txt 文本层未提取到任何行或列内容**。以下为从 `§III-E Literature Summary` 正文逐字回推的两表**列标题（即"行标题"意义上的分类维度）**，并注明来源：

**Table III（单智能体）列维度**，出自 §III-E：
> "The summarization of the single-agent approaches are given in table III, providing information on the **scenario**, the utilized **model or simulation environment**, the **observation** and **action spaces**, the elements considered in the **reward function**, and also the **type of RL agent**, and the **neural network**."

**Table IV（多智能体）列维度**，出自 §III-E：
> "Table IV presents the researches with multiagent (MARL) approaches, with similar columns, except for **rewarding**, where the **distribution of the reward among agents** is outlined."

**表注中的符号释义（逐字，出自 §III-E 的表注 [a]–[d]）**：
- **[a] 观测空间元素**："(x, y) are longitudinal and lateral position. (dgoal, dhead, dgap) are distances to goal, leading vehicle, and the target gap, respectively. (T, TTC, TTP) are Elapsed time, Time-to-collision and Time-to-position. (vx, vdes, dv) are for longitudinal speed, desired speed, and speed difference.  denote the heading of the vehicle. (id, w, c, geo) are for lane id, width, curvature, and geometry."
- **[b] 动作空间元素**："a-acceleration, th-throttle, st-steering, st′-steering speed, ayaw-yaw rate, br-brake, hb-handbrake… LCy and Dir are lateral, steps are longitudinal discrete steps, Tn is action for turning in intersection. {N} shows the size of the discrete action set, if known. For strategic decisions: (WAIT, GO)… ACC-acceleration, ACCSP-ACC setpoint, DEC-deceleration, (LLC, RLC)-Lane change left or right, NA-No action (keep state), FOL-stay in lane and use car following rules."
- **[c] 单智能体奖励项**："spe-speed, lc-lane chage (penalty), q-traffic flow, coll-collision, clo-unsafe distance (closing), time-time elapsed (step cost), succ-success/failure, lane-lane choice, acc-acceleration, trav-distance traveled, head-heading, lat-lateral distance, kright-keep right, sty-style, ayaw-yaw rate, jerk-jerk, over-overtaking."
- **[d] 多智能体奖励分配**："Centralized rewards are given, when there is one centralized controller for the multiagent task. 'Joined' means that the agent receives the reward based on the performance of every agent, while 'Individual' means the agent receives reward only for its performance."

⚠ **不得伪造 Table III/IV 的行条目（具体论文编号 × 场景的单元格）**：本机文本无法取得，须按 §7 动作 1 补取。

## 6. 对 P1 的用处

- **与 P1 的关系**：**相邻问题**。同属"决策/控制"层，且直接覆盖 P1 基线③（黄梦圆学位论文的 **TD3 直控**）所属的方法族（actor-critic / DDPG 系）。但本文的场景主体是跟车、车道保持、匝道汇入、稠密车流，**没有"多车道主线 + 人工与自动混行编队"的闭环协议**，也没有队列稳定性（string stability）议题。

- **可迁移**：
  1. **P1 基线定位与分类框架**：本文的"单智能体 vs 多智能体"两分法与四层级分解，可直接用于 P1 的 Related Work 组织结构，并用于说明 TD3 直控基线在文献中的位置（行为层/控制层的连续动作 actor-critic）。**P1 可直接引用的缺口句出处**：
     - §IV（Future Challenges 收束）："reinforcement learning is not a sufficient tool for automotive motion planning in itself. Still, it can be very efficient in solving complex optimization tasks by combining with other methods."（**P1 用"MPC+LNN 混合、大胆决策小心修正"架构时的最强外部支撑句**）
     - §IV-A Safety：ISO 26262 / Automotive SPICE "are still far from addressing deep learning with dedicated statements, since verification and validation is not a solved issue in this domain"；"full functional safety coverage can not be guaranteed in complex scenarios this way."（**P1 讨论安全叙事与不得声称合规时的引用锚点**）
     - §IV-B Sim2Real："Validation of these agents is usually made in the same environment setup, which contradicts the basic techniques of machine learning, where the training and validation scenarios should differ in some aspects."（**P1 主张"同一 CARLA 地图 + 同一组交通流种子"之外还须留出验证场景的动机句**）
     - §IV-B："Among the research evaluated in this review, all problems were trained in a simulated environment. There exists only one exception in [123], where the authors taught the agent for lane following on a real vehicle…"（**P1 不得把 CARLA/回放写成实车验证的领域惯例证据**）
  2. **奖励设计清单**：§II-D 给出奖励时机的三档（episode 末折扣回传 / 每步即时 / 预定周期或里程）及其代价，并列出最常用的舒适性量化量为**纵向加速度、横向加速度、jerk**（引 [60]、[61]、[62]、[10]、[63]）。**P1 的"加速度平方积分（舒适性）"与"Jerk 峰值"两个指标可据此声明与 DRL 文献惯例同源**。
  3. **模型保真度—算力量级（P1 可用硬数字）**：§II-A 给出相对计算时间——以运动学单车模型为基准，**3 自由度模型计算量高 10…50 倍，带非线性轮胎模型的 9 自由度精确计算高 100…300 倍**；并给出适用边界：运动学自行车模型在**横向加速度约 0.5g 或以下**且**干路面**假设下结果合适，超过此限模型无法处理动力学。这一条**直接约束 P1 的基线公平性声明**：MPC 基线与神经网络控制器若使用不同保真度的车辆模型，必须说明。
  4. **离散化—平顺性权衡**：§II-C——多数论文把转向与加速度离散为**每通道 3–9 个取值**，取值过少导致"uncontrollable slips, massive jerk, and yaw-rate"，取值过多则 POMDP 结果空间指数增长拖慢学习。P1 报 Jerk 峰值时可引此权衡。
  5. **观测表示维度**（§II-E）：(a) 自车状态 (|e|, v, θe)；(b) 汇入场景最小表示 2×(dx, dv)；(c) 高速机动 6×(dx, dv)（三车道前后车）；(d) 扩展到 6×(dx, dy, dvx, dvy)；另有轨迹数量扩至 9 个目标。**这些维度可作为 P1"同等可用信息"的对照清单**——用来证明 OTF-CfC 未获得超出基线的特权输入。
  6. **社会性收益的证据模板**：Fig. 12 + §III-D 的 [80] 用虚拟线圈采集流量，画出流量—密度图，证明合作行为带来更高流量与更低总行程时间。P1 若想在"混行编队"上报交通级效益，这是可对标（但不可直接搬数字）的呈现方式。

- **不可迁移 / 陷阱**：
  1. **ODD 差异**：本文场景清单以**匝道汇入、交叉口（含无信号交叉口）、环岛、赛车（TORCS）**为多。§III-C 明言"on-ramp merging and some intersection passing problems have a lot in common"。P1 的 ODD 是**高速主线多车道混行编队**，**不能**引用其交叉口/环岛/赛车结论。
  2. **"多智能体 = 合作"不成立**：§III-E 明确"all research deals with cooperative problem setups"（唯一例外是赛车）；且"agents don't establish or develop communication to form joined strategies"。P1 的"人工与自动混行"含**非合作/激进**对手，本文没有对应证据。
  3. **单智能体训练在多智能体环境中会失效**：§III-E 记 [103] "the vehicle trained in a single agent approach fails, when placed in a multiagent environment and must deal with agents with the same policy as itself"。**P1 若把 TD3 基线与 OTF-CfC 都放在同一混行车流中评测，必须报告对手策略组成**，否则结论不可比。
  4. **多数工作用全真值观测、无传感器噪声**：§IV-B 指出"most researches ignore complex sensor models… use 'ground truth' environment representations or 'ideal' sensor models, and only a few articles utilize sensor noise"。P1 若以"零额外传感器成本"为卖点，须同时说明观测假设（是否真值），否则卖点与证据不匹配。
  5. **Table III/IV 的单元格内容缺失**：不得凭印象写出"某某论文用了 DDPG + 3 层网络"这类条目——**本机文本层取不到**。
  6. **档位与协议的张力（须显式报告）**：按冻结的 `literature/meeting2/00-triage-protocol.md`，本卡 D1=1（相邻）、D2=0（观点/无对照）→ 加权 9，落在 **B 档（略读，9–13）下沿**，未达 A 档（需 ≥14 且 D1=2 且 D5≥1）。本卡已按 B 档下限完成（覆盖全部图表编号、收录分类学表维度）。**若要将本文升为 A 档精读，属用户对冻结协议的显式覆盖，需另行确认，不由本卡自行升级。**

- **引用时必须带的限定语**：
  "在 Aradi 对 DRL 运动规划的综述（检索截至 2020-01-17，场景以跟车、车道保持、匝道汇入、稠密车流为主，且作者指出**所评估的全部工作均在仿真中训练、仅一例在真车上做车道跟随**）中，作者明确判断**强化学习本身不足以作为汽车运动规划工具**，需与其它方法结合；该结论**不覆盖多车道主线的人工—自动混行编队**场景。"

## 7. 缺失信息（可执行动作）
1. **补 Table III/IV 表体（最高优先）**：当前 .txt 中两表仅存图注，无任何单元格。→ 动作：定位原始 PDF（`SOURCE_PDF: 决策基线：强化学习与安全强化学习/Survey_of_Deep_Reinforcement_Learning_for_Motion_Planning_of_Autonomous_Vehicles.pdf`），用表格提取或 OCR 取出 7 列 × N 行的全部条目，落盘为 `literature/notes/aradi-tableIII-IV.tsv`；**在取得前，P1 稿件不得引用任何单元格内容**。
2. **补 Table I / II / V 表体**：同上路径。Table V（仿真训练利弊）对 P1 的 Limitations 直接可用。
3. **核验 [65] 与 [57] 的原文归属**：§III-D 记 [65] 用 6 动作（table II），§III-E 记 [65] 的网络为"two convolutional and one dense layer"，而 §III-D 记 [57] 用 Dueling DQN + 优先经验回放与栅格观测。→ 动作：按参考文献表取出 [57]、[65]、[83] 的完整条目，确认"网络结构/观测/动作"三者的对应关系，避免张冠李戴。
4. **核验"3–9 个离散取值"与"300,000 episodes"的原始出处链**：→ 动作：追溯 §II-C 与 §III-D 的引文编号，确认这两个数字来自哪些原始论文、其 ODD 与协议是否与 P1 可比；P1 若引用须标注为"文献报告值，协议不同，不可直接比较"。
5. **核验 ISO 26262 / Automotive SPICE 相关表述的时效性（T2 取代检查）**：本文成稿于 2020（收稿 2020-01-28，见首页），其对标准覆盖度的判断可能已被后续标准活动改变。→ 动作：查 ISO 26262 与 ASPICE 是否有针对 ML/DL 的新增条款或补充指南，记录检索通道 + 日期；在核验前，P1 只能引本文判断为"2020 年时的判断"。
6. **核验 [123]（真车 DDPG 车道跟随）的正式发表版本与 ODD**：本文称其为"唯一例外"。→ 动作：Crossref/OpenAlex 查该条，确认是否真车闭环、场景是否含高速主线；P1 若用它作为"DRL 已上真车"的依据必须核验。
7. **本文与同组第 3 篇（Kiran 等 T-ITS 23(6)）的去重关系**：两篇均为 DRL+AD 综述。→ 动作：在 P1 的 Related Work 中明确二选一或分工（本文=运动规划层级与 RL 设计要素；Kiran=DRL 算法族、LfD/IRL 与部署挑战），避免同源错误复现两次（见 `AGENTS.md` §8 末条）。

## 8. 关键数字（只抄论文明确印出的表格/正文）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 计算量：3 自由度动力学模型 vs 运动学模型 | 高 **10…50 倍** | 作者给区间，未给测量平台/基准实现 | §II-A |
| 计算量：9 自由度 + 非线性轮胎模型 vs 运动学模型 | 高 **100…300 倍** | 同上 | §II-A |
| 运动学自行车模型适用上界 | 横向加速度约 **0.5g 或以下**，且假设**干路面** | 引 [38]；未给验证数据 | §II-A |
| Q 表规模示例（[85] 超车） | 状态离散 (6, 10, 8, 9) × 3 个横向动作 = **12,960** 元素 | — | §III、TABLE I |
| 转向/加速度离散档数（多数论文） | 每通道 **3–9** 个取值 | "most papers"，非统计 | §II-C |
| 图像观测下采样分辨率示例 | (1×48×27)（[67]）；(3×84×84)（[68], [69]） | 原出处各异，未统一协议 | §II-E-2 |
| 图像观测所需训练步数示例 | **1.5M 步**（[67]）；**100M 步**（[68]） | 原出处各异 | §II-E-2 |
| 差分图像替代原图带来的训练步数下降 | **约 10 倍更少**训练步达到同等性能（引 [71]） | 单一研究报告，未给区间 | §II-E-2 |
| 语义分割输入分辨率（[72]） | 640 × 400 | — | §II-E-2 |
| 稠密车流中端到端驾驶所需训练 episode | **300,000**（对比简单车道保持仅需"few hundreds"） | 单一来源，未给 seeds/区间 | §III-D |
| 激光雷达式观测示例（[73]） | 150° 视场内 **31 个方向**的距离 | — | §II-E-2 |
| 虚拟光束观测示例（[20]） | **19 个**传感器束，量程 **200 m**，每 **10°** 一条，覆盖车前半球 | — | §II-E-2 |
| 观测张量尺寸（[10]） | 4 × 3 × (2 × FoV + 1) | — | §II-E-2 |
| 高速机动观测向量（[54], [83]） | 6 × (dx, dv)；扩展为 6 × (dx, dy, dvx, dvy)；[55] 跟踪目标数扩至 9 | — | §II-E-2 |
| 汇入场景最小观测（[82]） | 2 × (dx, dv)（目标间隙两侧车） | — | §II-E-2 |
| MIT-DeepTraffic 实验规模（[106]） | 环境内共 20 辆车，允许智能控制至多 11 辆，其余随机行动 | — | §III-D |
| 多智能体训练的三种方案 | centralized controller / concurrent learning / parameter sharing | — | §I-C |
| 检索证据 | Web of Science 主题检索 "Deep Reinforcement Learning" AND "Autonomous vehicles"，日期 **2020.01.17**（Fig. 1）；无命中数、无纳入/排除标准 | — | Fig. 1 图注 |
| 分层数 | 至少 **4** 层（route planning / behavioral / motion planning / local feedback control） | 引 [3] | §I-A、Fig. 2 |
| 参考文献条数 / 页数 / 图数 / 表数 | **131** 条（[1]–[131]，编号连续）；20 页（pp. 740–759）；13 图；5 表 | — | 全篇统计 |

⚠内部不一致（小）：§II-D 述跟车任务时写观测空间为 "(v, dv, ds)" 三元组，§II-E-2 述结构化观测时又给 "(d, v) as in [64] or (d, v, a) as in [81]"（headway distance、speed、acceleration）——**同一"跟车"任务出现两套不完全一致的最小观测定义**，引用时须指明所据小节。
⚠内部不一致（小）：§II-A 声称 9 自由度模型考虑四轮角速度 (ωfl, ωfr, ωrl, ωrr) 与车身俯仰/侧倾 (θ̇, φ̇)，但正文以 ˙ 标记的符号串在 PDF 抽取中有乱码，**具体状态变量书写不可逐字复现**；引用时只用"9 自由度、含车身俯仰侧倾与四轮角速度"这一层级描述。
