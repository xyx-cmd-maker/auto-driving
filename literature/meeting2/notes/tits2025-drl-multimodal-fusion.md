# 预定义多模态输入 + 共享特征提取的端到端 DRL 决策｜A Deep Reinforcement Learning Method for Autonomous Driving Integrating Multi-Modal Fusion

- **出处**：IEEE Transactions on Intelligent Transportation Systems, Vol. 26, No. 8, August 2025, pp. 11850–11863 ｜ **类型**：期刊论文（方法 + CARLA 实验）
- **作者**：Chengcheng Xu et al.（第一作者 Chengcheng Xu，吉林大学通信工程学院；通讯作者 Haiyan Zhao）
- **DOI**：10.1109/TITS.2025.3573781（Crossref `works/10.1109/TITS.2025.3573781`，取用日期 2026-10-04：命中，题名一致，Vol. 26 / Issue 8 / pp. 11850-11863 一致，`relation` 为空 → 未见更正或撤稿标记）
- **全文来源**：`literature/fulltext/meeting2/a-deep-reinforcement-learning-method-for-autonomous-driving-__7c59240b.txt`（本机文本 82,761 字符 / 14 页）
- **分组**：TITS
- **证据等级初判**：**C 级** — 纯 CARLA 仿真闭环（Town04 训练与测试、Town05 泛化），有同类方法基线对照与 5 次重复，但**无显著性检验、无置信区间、无实车**；且本机全文文本**完全不含任何表格数值**（见 §5 与 §7），主结果在本机不可核。
- **档位建议**：**B 略读** — 与 P1 同属"车辆决策/控制"，但其为端到端图像 DRL、ODD 为 CARLA 地图导航任务，只提供**指标定义、消融骨架与"先验结构化输入"的同类论证**，不直接测 P1 的 RQ；主结果数字本机不可核，不能作为基线数字来源。
- **五维打分**：D1=1 D2=1 D3=1 D4=2 D5=1 → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = 3+2+2+2+2 = **11 / 20**（按 `literature/meeting2/00-triage-protocol.md` §5 记分；D1 定义见该协议）

> ⚠ **冻结协议排除词表字面接近**：本文输入构造依赖**语义分割图**与 **BEV**（`00-triage-protocol.md` §3"感知层专用"含 `semantic segmentation` / `BEV perception`）。但本文的贡献点是**决策框架**（共享特征提取 + 多模态输入设计），不做感知方法本身。→ 若严格按字面命中执行，需人工裁定是否降 D 档；本卡片按"贡献层为决策"记为 B。

---

## 1. 标题

A Deep Reinforcement Learning Method for Autonomous Driving Integrating Multi-Modal Fusion｜中文直译：一种融合多模态的自动驾驶深度强化学习方法

## 2. 摘要（≤400 字中文，保留关键数字与结论成立条件）
端到端自动驾驶输入维度高，特征提取网络若在线从零训练会导致学习与决策困难。本文提出预定义多模态图像方法与共享框架：输入不是传感器原始数据，而是鸟瞰图（BEV）、自车状态、前视图（语义分割后去噪并嵌入轨迹、禁行线、风险分割等预定义内容）三类观测，按人类先验滤除照明、树木、山体等无效特征；并提出共享特征提取模块，使其独立于 DRL 网络、只算一次并把隐特征序列共享给各网络，与 actor、critic、Q 三路损失加权联合更新（权重按余弦退火调整），避免嵌入式框架的重复计算。实验在 CARLA 上构建交互环境：地图上 110 辆随机车辆，时间步长 0.1 s；训练与测试在 Town04，泛化测试在 Town05；动作空间为 [-1.0, 1.0]²，加速度缩放至 [-0.6, 0.6]、转向缩放至 [-0.1, 0.1]。结果：共享模式在三模态下比嵌入式快 3.14 倍；作者结论是多模态融合输入优于传统方法并可缩短训练周期。但成功率、碰撞率等主结果数值只存在于本机文本缺失的表格内。

## 3. 结论（≤350 字中文）
作者结论节称：本文探索了多模态状态对 DRL 训练的影响，基于人类先验融合可降低无效特征影响，单独设计状态特征提取以加速融合，并基于 CARLA 建立实时交互环境。结论句为多模态融合输入优于传统方法、可让智能体更快学会规则并在相同条件下缩短整个训练周期，同时需平衡各状态相互影响、防止网络因状态频繁变化陷入局部涡旋。关键数字：BFS 下共享模式比嵌入式快 3.14 倍（Table V 与正文，5 次重复均值）；BFS 单次实验计算时间 8.31 s，复算每样本梯度更新约 2.6 ms（式 (23)）。作者自承局限：受算力限制地图上只设 110 辆随机车辆；结论建立在训练 episode 数受限的设定上，称若继续训练碰撞率会下降、速度会上升，即把当前碰撞率偏高归因于训练阶段；承认多模态融合存在大量重复表征片段会干扰训练，留待未来研究。全文未见代码或数据可用性声明。

## 4. 方法一句话（≤60 字）

BEV + 前视图（语义分割去噪 + 预定义内容）+ 自车状态 → 独立共享 CNN 特征提取 + SAC → 油门/转向连续动作。

## 5. 图表清单（占位符）

> 全文共 **9 个 Figure + 7 个 Table = 16 项**，超过 12；下表覆盖**按出现顺序的前 12 项**，剩余 4 项见紧随其后的补充表。
> ⚠ **本机文本的一个重要事实**：该 .txt 抽取结果**只保留图/表题注，不含任何表格单元格数值**（对全文 grep `%`、多位小数并列模式均无命中）。因此"读图要点"只能写正文中对图表的文字描述，**不得视为已读到表内数值**。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-MMF-1} | Fig. 1 | Predefined multi-modal end-to-end autonomous driving. | 全文方法总示意；§I 末段引用它提出"预定义多模态融合 + 特征提取在线从零训练"。图内细节在本机文本不可见 |
| {FIG-MMF-2} | Fig. 2 | The algorithm framework. | 算法框架总览（§III 开头："overview of our proposed approach is presented in Fig. 2"）。图内细节不可见 |
| {FIG-MMF-3} | Fig. 3 | Comparison of two different input data. | 对照"原始未处理数据 vs 感知处理后统一样式数据"（§III-A）；用于论证原始数据含大量噪声 |
| {FIG-MMF-4} | Fig. 4 | The denoised and predefined BEV. | BEV 的坐标变换与预定义内容（式 (9) 的传感器→BEV 投影）；只把对训练有用的感知数据投到 BEV |
| {FIG-MMF-5} | Fig. 5 | The denoised and predefined front view. | 前视图四态：(a) 原始 →(b) 语义分割去动态噪声 →(c) 式 (10) 去静态噪声（天空/树/山置黑）→(d) 嵌入轨迹/禁行线/风险分割 |
| {TAB-MMF-1} | TABLE I | THE STATE SPACE OF THE EGO VEHICLE Vself | 自车观测 **7 个参数**（含相对前向角 a_r、相对位置 x_sr / y_sr、one-hot 道路 id L_s/L_l/L_r）；**表体数值在本机文本缺失** |
| {TAB-MMF-2} | TABLE II | THE STATE SPACE OF THE SURROUNDING VEHICLES Vothers | 周车观测为**固定 40×6 矩阵**（最多 40 辆最近车，每步全零初始化，存位置/速度/车道 id/车辆形状）；来自 CARLA 直接读取；**表体缺失** |
| {FIG-MMF-6} | Fig. 6 | Comparison of two different framework design methods. | 嵌入式（a）vs 共享式（b）特征提取对照；正文用式 (11)(12) 论证嵌入式数据量为共享式 3 倍、GPU 累积重复计算 |
| {TAB-MMF-3} | TABLE III | PARAMETERS OF EACH MODULE (K: KERNEL SIZE, C: OUTPUT CHANNELS, S: STRIDE, P: PADDING) | 三个特征提取子网（BEV/前视图、V_others、融合）的层参数；隐特征序列统一压到 **1×128**，环境表征再压到 **1×7** 后与 V_self 拼接；SAC：critic/Q 输入 1×16 输出 1，actor 输入 1×14 输出 2；**表体缺失** |
| {FIG-MMF-7} | Fig. 7 | Separate display different random noise interference. | 四类后加噪声（区域模糊、雨雪背景、区域遮挡、运动模糊）的独立概率 0.1/0.2/0.1/0.5；面积最大 50%，运动模糊需车速 >15 km/h |
| {TAB-MMF-4} | TABLE IV | HYPER-PARAMETERS | 全部实验共用同一套超参（"for fairness and rigor… same parameter settings"）；距离 m、速度 m/s；**表体数值在本机文本缺失** |
| {TAB-MMF-5} | TABLE V | THE AVERAGE TIME (SECOND) OF DIFFERENT TYPES | **主结果表之一（计算成本对照）**；正文给出唯二可引用数字：BFS 共享模式比嵌入式**快 3.14 倍**、BFS 单次实验 **8.31 s**；batch=64、梯度更新 50 次、5 次重复均值；**表体缺失** |

**>12 的剩余 4 项（按出现顺序）**

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {TAB-MMF-6} | TABLE VI | THE TEST RESULTS UNDER DIFFERENT SCENARIOS | ★**主结果表（对比实验）**：对比对象为 raw image benchmark（文献 [41]）、BEVFusion [43]、PGM（Chen et al. [47]）与本文方法；指标为 SR 成功率 / CR 碰撞率 / AS 平均速度 / AD 平均偏差；同参数、测试 **100 次**取均值。**表体全部数值在本机文本中缺失** → 不得据本机文本写任何"提升 X%"；P1 选基线前须回原 PDF 抄表 |
| {FIG-MMF-8} | Fig. 8 | The average reward, speed, angle, and deviation of different fusions. | 四种融合（S / FS / BS / BFS）逐 episode 的平均奖励(a)、速度(b)、角度(c)、偏差(d)；误差带来自 **5 次重复**；正文称 BFS 平均奖励"基本最优"，FS 早期弱于 BS |
| {FIG-MMF-9} | Fig. 9 | Different moments while the agent was driving normally. | 智能体正常行驶的若干时刻截图；用于定性展示轨迹跟随（正文：高速下仍严格跟随轨迹点） |
| {TAB-MMF-7} | TABLE VII | THE RESULTS WITH DIFFERENT FUSIONS IN DIFFERENT STAGES | Fig. 8 数据按**四个训练阶段**分段求均值；正文结论："横向比较 BFS 在获取奖励上最优；FS 起始奖励低、下一阶段逐渐追平 BS"；**表体缺失** |

## 6. 对 P1 的用处

- **与 P1 的关系**：**相邻问题**。同属"车辆决策/控制"，且其方法类（端到端 DRL 直控）正是 P1 基线③（学位论文 TD3 直控）的同一族；但本文是**图像→低层控制的端到端 SAC**，P1 是**连续时间控制器 + 编队跟车**，ODD 为其 CARLA 地图上的"到达目的地"驾驶任务，**不是高速公路主线多车道编队**。
- **可迁移**：
  1. **评价指标定义**：`Succ.(%) 成功到达 / Coll.(%) 碰撞 / TO.(%) 超时 / Pass Time` 与本文的 `AS 平均速度 / AD 平均偏差`——其中 **AD（平均偏差）与 P1 的"车道居中偏差"同构**，可用于 P1 的场景级报告表；`TO./Pass Time` 可对应 P1 的"效率"维度。
  2. **消融骨架（"逐模态加一"）**：`S`（仅状态）→`FS`（前视+状态）→`BS`（BEV+状态）→`BFS`（三模态）。这是**一次只改一个因素**的干净设计，可直接借为 P1 的 A1（OTF 开/关）之外的输入模态消融模板；其"误差带来自 5 次重复"的写法也可对齐 P1 `AGENTS.md` §4（种子 ≥5）。
  3. **"先验结构化输入"的同类论证**：本文的核心动机是"按人类先验滤掉对任务无效的特征，并把任务信息预定义进输入"，与 P1 把 OTF 势场当作 **inductive bias / prior-informed** 结构条件的论证同构——可作为 P1 Introduction 里"注入先验结构"这一论证线的**他领域支撑**（注意 P1 术语红线：**不称 physics-informed**）。
  4. **参数共享/去重复计算**：共享特征提取模块（一个模块算一次、被多个网络共用、损失加权联合更新）与 P1 "OTF 势场模块在 MPC 与 LNN 两条路径间复用"的工程动机同构，可作为"共享中间表征以省算力"的引用支点。
- **不可迁移 / 陷阱**：
  1. **ODD 完全不同**：CARLA 地图 route-following、110 辆随机车流，无高速公路主线、无编队、无 cut-in/驶离工况分类 → 其成功率数字**不可迁移**到 P1 的 ODD（`AGENTS.md` §5）。
  2. **无一项 P1 核心指标**：全文没有跟车误差 RMSE、加速度平方积分、Jerk 峰值、车道居中偏差（只有"平均偏差"的粗指标）、前轮转角方差、端到端延迟、MCU 内存占用。
  3. **无实车**：纯 CARLA，属"仿真"档；不得表述为实车验证。
  4. **基线不完全同条件**：BEVFusion 基线"use the checkpoints trained by the authors on public datasets, and then connect it with RL networks through the shared framework"——即**用作者在公开数据集上的预训练权重**，而本文方法的特征提取是**在线从零训练**。这意味着两边的**可用信息与训练预算不对等**，与 P1 `AGENTS.md` §3"同等可用信息、同等调参预算"直接冲突；P1 若引用该对比须写明这一点。
  5. **训练预算受限的对照**：作者自承只训练了"相同 episode 数"，并称不同方法的**总时间步数会不同**（"the total number of time steps carried out by different methods will be different at same number of episodes"）→ 不是等步数对照。
- **引用时必须带的限定语**：**"该文为 CARLA（Town04 训练/测试、Town05 泛化）仿真闭环下的端到端 SAC 决策研究，指标为成功率/碰撞率/平均速度/平均偏差，地图上仅 110 辆随机车辆；其 BEVFusion 基线使用原作者在公开数据集上的预训练权重，与本方法在线从零训练并非同等可用信息；其对比数值取自原 PDF 表格（本机文本抽取未含表格数值），引用前须逐格核对。"**

## 7. 缺失信息（可执行动作）

1. **需回原 PDF 抄录 Table VI（主结果表）全部单元格**：列名（SR/CR/AS/AD 及场景维度）、行名（raw image benchmark / BEVFusion / PGM / 本文方法）、每格数值与单位。（后果：本机文本**一个对比数字都没有**，P1 无法据此选基线，也无法评估"多模态融合带来多少提升"。**这是本卡片最重的一条**。）
2. **需抄录 Table V（平均时间）与 Table VII（分阶段结果）的表体**，并确认 3.14× 与 8.31 s 对应的具体行（BFS 行）与单位。（后果：无法判断"3.14 倍"是相对哪一种融合、也无法验证是否与正文"应大于 3 倍"的推导一致。）
3. **需索取 5 次重复的随机种子列表与逐次结果**，并说明"5 repeated tests"（Table V）、"testing 100 times"（Table VI）、"five repetitions"（Fig. 8 误差带）三者是否是同一套种子。（后果：无种子则方差不可复算；`AGENTS.md` §4 要求"种子 ≥5，报 mean ± std 或 95% CI"，本文只有均值。）
4. **需索取对比实验的等预算证明**：BEVFusion 的预训练权重来自哪些公开数据集、是否冻结；三种方法的 episode 数、总时间步数、调参预算各是多少。（后果：决定该对比能否作为"方法更优"的证据，也决定 P1 引用时是否必须写"协议不同、不可直接比较"。）
5. **需索取推理侧指标**：单步推理时延、模型参数量/内存占用、控制频率。（后果：P1 需要端到端延迟与 MCU 内存占用两项资源指标做对照，本文只有训练侧时间。）
6. **需确认是否存在代码/数据可用性声明**：全文（含致谢）未出现任何仓库或数据公开说明（对全文 grep `github` / `available at` / `open-source code` 仅命中 CARLA 本身的引用）。（后果：本机判定"无复现材料"，若需复现须联系作者。）

## 8. 关键数字（只抄论文明确印出的表格/正文，不得目测估读）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 共享模式相对嵌入式模式的加速（BFS 三模态） | **3.14 倍** | **未报告**（正文称"5 次重复测试的平均值"，无 SD/CI） | §IV-E-1 + Table V |
| BFS 单次实验计算时间 | **8.31 s** | 未报告 | Table V（经 §IV-E-1 正文引用） |
| 每样本梯度更新时间 | **≈2.6 ms**（= 8.31 s /(50×64)） | 未报告（由正文公式复算，非论文印出值） | 式 (23) |
| 梯度更新次数 / batch size（计时设定） | n = 50 次 / bs = 64 | — | §IV-E-1 |
| 嵌入式输入数据规模（单模态图像 224×224×3，En=3） | 903,168（原文记作 "bits"） | — | 式 (11) |
| 每 episode GPU 处理数据量 | 2,890,137,600（原文记作 "bits"） | — | 式 (12) |
| 仅状态空间（S）数据规模 | 247（原文记作 "bits"，= 40×6 + 7） | — | §IV-E-1 |
| 周车观测矩阵 | 固定 **40×6**（最多 40 辆最近车） | — | §III-A-3 + Table II |
| 自车观测参数个数 | **7** | — | §III-A-3 + Table I |
| 隐特征序列长度 / 融合后环境表征长度 | **1×128** / **1×7** | — | §III-C + Table III |
| SAC 网络 I/O | critic 与 Q：输入 1×16、输出 1；actor：输入 1×14、输出 2 | — | §III-C |
| CARLA 地图车辆数 | **110 辆**随机车辆（traffic manager 自驾模式） | — | §IV-A |
| 仿真时间步长 | **0.1 s** | — | §IV-D-2 |
| 动作空间 | `[-1.0, 1.0]²`；加速度缩放 `[-0.6, 0.6]`、转向缩放 `[-0.1, 0.1]` | — | §IV-C |
| 碰撞惩罚 / 越界惩罚 | r_col = **−100** / 超出 d_max 时 **−50** | — | §IV-B，式 (18)(19) |
| 测试次数 | Table V：**5 次重复**；Table VI：**测试 100 次**；Fig. 8 误差带：**5 次重复** | 无 CI、无检验 | §IV-E-1 / §IV-E-2 / §IV-E-3 |
| 后加噪声独立概率 | 区域模糊 **0.1**、雨雪背景 **0.2**、区域遮挡 **0.1**、运动模糊 **0.5**；面积上限 **50%**；运动模糊要求车速 > **15 km/h** | — | §IV-D-1 + Fig. 7 |
| 主结果（SR / CR / AS / AD 的逐场景数值） | **本机全文文本中不存在** | — | Table VI（题注在文本中，表体缺失） |
| 复现材料可用性 | 全文**未出现**代码/数据可用性声明 | — | 全文 grep |

⚠**内部不一致 1（量纲）**：式 (11)(12) 把 224×224×3×2×En 的**元素计数**写作 "bits"（903,168 "bits"；2,890,137,600 "bits"），未乘字节宽度；按此单位，2.89 G"bits" ≈ 361 MB，而若按 fp32 元素计则约 11.6 GB——两条口径相差 32 倍，论文未说明。

⚠**内部不一致 2（基线条件）**：§IV-D-1 称"all comparisons were set the same hyper-parameters"，但同段又写明 BEVFusion 使用"checkpoints trained by the authors on public datasets"，而本文特征提取是"online from scratch"——"same hyper-parameters"并不等于"同等可用信息与同等训练预算"。

⚠**内部不一致 3（结论强度 vs 证据）**：§V 结论称多模态融合输入"superior to the traditional methods"并"reduce the entire training cycle"，但全文正文可查证的数字只有"共享 vs 嵌入式 3.14 倍"（这是**框架对照**，不是**方法 vs 基线**的性能对照）；性能对照数值只存在于本机缺失的 Table VI 中。

---

**卡片纪律声明**：本卡片所有图号、表号、题注均逐字取自上述 .txt 全文；所有数值均抄自论文正文明确印出的式子/句子，**没有一处来自对图形或表格图像的目测估读**（本机文本不含表体数值，故主结果数值一律标"缺失"）。DOI 与卷期页经 Crossref 独立核验（2026-10-04）。本卡片不评价该论文的重要性与新颖性。
