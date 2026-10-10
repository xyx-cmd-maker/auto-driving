# 精读笔记 #15：Human-Like Autonomous Car-Following Model with Deep Reinforcement Learning

**文献**：Zhu M, Wang X, Wang Y. Human-like autonomous car-following model with deep reinforcement learning. *Transportation Research Part C: Emerging Technologies*, 2018, 97: 348–368. DOI: 10.1016/j.trc.2018.10.024
**作者核验**：Crossref（2026-10-02 复查，DOI `10.1016/j.trc.2018.10.024`）确认作者为 **Meixin Zhu, Xuesong Wang, Yinhai Wang**，**共 3 人，无 Pu、无 Li**；题名/期刊/卷 97/页 348–368/2018-12 全部匹配；`update-to` 为空（无更正、无撤稿记录）。
**精读日期**：2026-10-02
**全文来源**：已获全文（34 页 PDF，arXiv:1901.00569v1，`journal_ref` = TRC 2018）。文本经 PyMuPDF 提取（`fulltext/p15-humanlike-cf-trc2018.txt`，2,227 行）；**图 7 数据标签已用原始 PDF 的矢量坐标独立复算验证（见 §四 备注）**。
**版本警示**：arXiv v1 采用 **Transportation Research Record (TRR) 排版模板**（"ABSTRACT / Keywords / 数字编号章节 / TRR 式参考文献"），并在正文留下 **3 处未解析交叉引用 `Error! Reference source not found.`**。本笔记所有数字出自 arXiv v1；**写入稿件前须与 TRC 正式版逐数字核对**（尤其是图 7 与表 4）。

---

## 作用域

**场景①：项目内文献工作。**

- **项目**：`D:\Deepseek Harness\auto-driving`（自动驾驶 OTF 论文集群）。
- **项目不变量文件**：`D:\Deepseek Harness\auto-driving\AGENTS.md`。
- **本次精读服务的主张**：论文 1（P1，代号 OTF-CfC）**「基于超车频次势场与液态神经网络的高速主线编队连续时间控制」**。
- **本文在 P1 中的角色**（引自项目文献池登记）："**与 OTF 势场最接近的替代路线**（用 RL 学"类人跟驰"）；P1 必须显式对比，不能只比 PID/MPC"。

### P1 主张上限（逐字引用 `auto-driving/AGENTS.md` §1，本笔记不得越界）

> **P1 红线**：不得预先声称"OTF 势场带来 X% 性能提升"。学位论文报告的分类器准确率增益为 **+1.0 ~ +5.5 个百分点**（SVM +2.23~+3.60／LSTM +2.23~+5.46／Bi-LSTM +1.00~+1.73；**分类器准确率，论文报告值，未经我们复现**），在 LNN 控制范式下**未经本项目实测即属 C/D 级证据**。A1 消融须诚实报告；若不显著，卖点改为"**可解释性 + 零额外传感器成本**"。
> **不得把仿真/回放写成实车验证**：CARLA（Town04）与实车数据回放都是仿真或开环证据。未做真车闭环前，措辞上限是"在 CARLA 与真实数据回放中"。
> **不得直接搬用他人论文数字**：与 DriveDreamer 等对比若未同协议复现，必须标注"文献报告值，协议不同，不可直接比较"。

**本笔记的三条自我约束**（对应上面的上限）：

1. 本笔记中任何本文数字进入 P1 稿件时，**一律标注"文献报告值，协议不同，不可直接比较"**，并附 `citation_qualifier` 单行。
2. 本文全部结果为 **开环回放 + 运动学仿真（point-mass 模型）**，**不得**被表述为实车验证或闭环驾驶能力；本文作者本人也把实车验证列为 future work。
3. 本笔记**不评价**本文的重要性与新颖性（那是主编视角，交 `cross-paper-synthesizer` / `research-gap-hunter`）。

**外部复现列**：按 `deep-paper-reader` §3.1.1，本笔记只做单篇精读，**未做外部引用检索**，故所有行的"外部复现"列**一律为"未检"**——这是信息缺失，**不等于**"无外部证据"，也**不得**据此把本文结论说成"仅一次性证据"。

---

## 一、作者主张

（一段话转述，不评价。）

作者提出一个"类人自动驾驶跟驰规划"框架：把历史自然驾驶数据喂入一个自建的跟驰**仿真环境**，用深度确定性策略梯度（DDPG）智能体在其中试错，奖励函数度量"仿真行为与实测行为的偏离"，从而学到一个从**（跟驰车速度、前后车相对速度、车间间距）→ 跟驰车加速度**的连续控制策略；该策略可"在更多数据被喂入时持续更新"。作者用 **2015 上海自然驾驶研究（SH-NDS）** 中 **20 名驾驶员 × 100 个跟驰时段 = 2,000 个跟驰时段（合计 827 分钟）**，按 **70/30** 划分标定与验证，逐驾驶员建模，并把所提 3 个 DDPG 变体（DDPGs／DDPGv／DDPGvRT）与 **IDM**、**RNN**、**Loess**、**NNa** 共 7 个模型对比。核心主张是：以**速度偏差为奖励、并考虑 1 s 反应延迟**的 **DDPGvRT** 在**轨迹复现精度**（intra-driver 间距 RMSPE 18.23%、速度 RMSPE 5.67%）与**泛化能力**（inter-driver 21.94% / 6.66%）上优于全部被测模型，并能通过重训**适配不同驾驶员**；作者进而主张强化学习方法"能提供对驾驶员行为的洞见"，并有助于类人自动驾驶算法与交通流模型的发展。作者同时明确声明：本方法**不处理绝对安全问题**，也**不处理历史数据中的人为错误**，这两者需由碰撞避免系统与异常检测另行承担。

---

## 二、主张—证据台账

| # | 作者主张（英文原句） | 支撑证据（图/表/统计量） | 内部等级 | 外部复现 | 是否被结果支撑 | 缺口 |
|---|---|---|---|---|---|---|
| 1 | "the DDPGvRT model has a spacing validation error of 18% and speed validation error of 5%, which are less than those of other models, including the intelligent driver model, models based on locally weighted regression, and conventional neural network-based models." （Abstract） | 图 7(a)(b) 数据标签；n = 20 驾驶员 × 30 个验证时段/驾驶员；DDPGvRT **18.23% / 5.67%** vs IDM **21.88% / 8.97%**、Loess **30.67% / 10.66%**、NNa **36.18% / 14.24%**（intra-driver） | **B_int**（带乐观偏置旗标） | 未检 | **是**（数值方向成立） | 摘要的 "validation error" **未说明是 intra- 还是 inter-driver**；所引 18%/5% 仅对应 intra-driver，inter-driver 为 21.94%/6.66%（差 3.71 / 0.99 个百分点）。且最佳 agent 由"训练+测试误差之和最小"选出（§5.4），**模型选择用了测试集**→ 该数字为乐观估计。**无 CI、无显著性检验、无独立重复运行。** |
| 2 | "The DDPGvRT model outperformed all the investigated models, as evidenced by its having the lowest mean and standard deviation on spacing and speed." （§6.1） | 图 7(a)(b)：误差棒 = "standard deviation (verticals above the bars)"，**只画不标数字** | **C_int**（部分不成立） | 未检 | **部分**：均值最低成立；**"standard deviation 也最低"在 spacing 上不成立**——用 PDF 矢量坐标反算误差棒长度（标定误差 < 0.05 个百分点，见 §四）：**spacing intra** DDPGvRT ≈ 5.2 vs **DDPGv 3.1、RNN 3.4**；**spacing inter** DDPGvRT ≈ 14.1 vs **RNN 2.5、DDPGs 7.8、DDPGv 8.2、IDM 9.8**。仅 speed 两个层级 DDPGvRT 的 SD 最低（≈1.7 / 1.6） | 图 7 **未印出任何 SD 数值**，该断言在当前公开材料下**不可核验**；须作者提供 mean±SD 表。误差棒未说明是 SD 还是 SE、是单侧还是双侧 |
| 3 | "the DDPGvRT model … outperforms the tested traditional and recent data-driven car-following models in terms of trajectory-reproducing accuracy and generalization capability" （§7） | 图 7 + 图 9（20×20 驾驶员间误差矩阵，仅图形无数值）+ 表 4 | **B_int** | 未检 | **是**（点估计方向） | **与经典跟驰模型的对比只有 IDM 一个**：Gipps（安全距离类）、GHR、OVM、Wiedemann、Helly 在 §2.1 被综述，**未被实现、未被对比**；§2.1 选择 IDM 的理由本身指向一处**失效引用**（"the IDM has been found to have the best performance … (Error! Reference source not found.)"，arXiv v1 交叉引用未解析）。7 模型 × 2 指标 × 2 层级 = 28 个比较**无多重比较校正** |
| 4 | "This study used the reward function to facilitate human-like driving by minimizing the disparity between the values of simulated and observed behavior. As results could differ depending on the type of reward function, both spacing and speed (velocity) were tested" （§4.2） | 式 (7) r_t = log(\|S_sim − S_obs\| / S_obs)；式 (8) r_t = log(\|V_sim − V_obs\| / V_obs)；图 6 奖励曲线；图 7（DDPGs vs DDPGv：spacing 22.52% vs 18.67%、speed 11.46% vs 7.48%，同为无 RT 的干净对比） | **C_int**（奖励类型比较）／**D_int**（公式本身） | 未检 | **部分** | **式 (7)(8) 与图 6 不自洽**：式 (7)(8) 在相对偏差 < 100% 时恒 ≤ 0，**最大化**累积奖励会把策略推向**更大**偏差，与"minimizing the disparity"的表述相反；而图 6 "Reward on Training Data" 纵轴 −5000~10000、曲线稳定在 **+5000~+9000** 并随误差下降上升 → 实际实现必为反号（或按负代价累计）。**两种解释必须以作者代码/正式版勘误消解**。另：奖励需要**真值轨迹**才能计算，因此"在线持续更新"不等于可在线计算奖励 |
| 5 | "The DDPGvRT demonstrates good capability of generalization to various driving situations and can adapt to different drivers by continuously learning." （Abstract） | §6.2 图 9（20×20 矩阵）+ 表 4；§6.3 图 10（3 名驾驶员重训曲线） | **B_int**（跨驾驶员泛化）／**C_int**（自适应） | 未检 | **是**（方向），**但"未训练驾驶风格"未被真正留出** | 表 4 只给 **2×2 均值**（A→A 0.1984、A→C 0.2398、C→A 0.2705、C→C 0.2259），**未报告每格驾驶员数**、未报告逐驾驶员误差；风格只由 **k-means k=2** 划出（无轮廓系数/有效性指标/k 的敏感性）；**没有任何"训练时完全排除某一风格"的留出实验**。§6.3 自适应仅有 **n = 3** 名随机驾驶员且图 10 **无数值**，"errors started to converge after approximately 8 episodes" 为定性描述 |
| 6 | "The training was repeated for 60 episodes for each driver, and the RL agent that generated the smallest sum of training and test errors was selected." （§5.4） | 图 6（奖励/误差曲线）；作者未报告任何跨运行统计量 | **D_int**（就"方差"这一主张而言为"未报告"） | 未检 | **不适用／未报告** | **全文 0 处出现 seed / random seed / confidence interval / p-value / significance test / standard error**（已逐词 grep 核实）。图 7 的 "standard deviation" 是**跨跟驰时段（跨驾驶员）的离散度**，**不是**多次独立训练的**运行间方差**。"60 episodes" 是**单次训练内的回合数**，不是 60 次独立重复。→ **无法判断 18.23% vs 18.67% 等差异是否超出随机波动** |
| 7 | "Although the network structure utilized in our study with only one hidden layer cannot be regarded as a truly 'deep' neural network, it fully exploits the main idea of deep reinforcement learning methods and can be easily extended once more input variables are provided." （§7） | 图 4（actor/critic 各 1 个隐藏层、30 神经元；RT 模型 100）；NNa 基线**采用与 DDPGv actor 完全相同的结构** | **B_int** | 未检 | **是**（自我声明） | 作者自承网络非"真 deep"；而 NNa 是同构**监督**基线且在 spacing 上最差（36.18%）→ 说明**性能差主要来自"监督加速度拟合 vs 累积回报优化"的目标差异**，而非网络容量。但该推断**未被消融验证**（无同结构、同目标的对照） |
| 8 | "the performance of the DDPGs model starts to converge when the training episode reaches 20." （§5.4） | 图 6（DDPGs，随机 1 名驾驶员） | **C_int** | 未检 | **是**（单例、图形证据） | **单例、单模型、任选驾驶员**；无跨驾驶员的收敛回合分布；"converge" 无判据（无阈值、无置信带） |
| 9 | "the DDPGvRT model can adapt to different drivers when new data are fed." （§6.3） | 图 10(a)(b)，重训曲线 | **C_int** | 未检 | **是**（定性） | **n = 3** 名随机驾驶员；图 10 **无任何印出数字**；"The final errors were smaller than those in the initial models" 无差值量；重训后**又用测试集选模型**的偏置同样存在；清除 replay buffer 后是否保留原驾驶员能力（**灾难性遗忘**）**完全未测** |
| 10 | "It is worth noting that the proposed DDPG model is intended to reproduce human-like driving behavior … absolute safety issues, as well as the handling of human error in historical driving data, are not addressed in this approach." （§7） | 无（作者主动划定边界） | **D_int**（对该边界为明示声明，非实验结果） | 未检 | **是**（诚实声明） | 这条对 P1 **极有价值**：本文作者**自认**所提"类人"模型**不含安全保证**，需外挂碰撞避免系统。任何把本文当作"类人即安全"的引用都属**越界** |
| 11 | "human-like autonomous car-following planning"（题名）/"can reproduce human-like car-following behavior with higher accuracy than traditional and recent data-driven car-following models"（Abstract） | 图 7（轨迹 RMSPE）+ 图 8（**仅 2 个**跟驰时段：1 stable + 1 dynamic 的轨迹对比） | **C_int** | 未检 | **部分** | **"类人"被完全操作化为"轨迹 RMSPE 更低"**：无任何行为真实性检验——无加速度分布对比、无车头时距分布对比、无 Turing/图灵式判别、无人类观察者评分、无**闭环**交互、无**弦稳定性**（string stability）。且图 8 **图题与正文不一致**：图题为 "generated by the IDM, RNN, and **DDPGv** model"，正文为 "replicated by the **DDPGvRT**, IDM, and RNN" 且 "the DDPGvRT model (in red)" → **图中红曲线究竟是哪个模型无法确定** |
| 12 | "the model only needs a few seconds to converge for data collected on trajectories lasting many seconds … that policy is responsible for real-time referenced acceleration generation, which is feasible because it is just a forward pass on the policy network" （§7） | 无（无计时测量、无硬件说明、无延迟数据） | **D_int** | 未检 | **否**（无测量支撑） | **全文无任何训练耗时、推理延迟、算力平台、MCU/GPU 信息**；"a few seconds" 与 "real-time" 均为未量化的可行性断言。对 P1 的"端到端延迟 / MCU 内存占用"指标**不可引用** |
| 13 | "the current study is the first to use a deep reinforcement learning to model car-following behavior."（§2.2） | 无（新颖性断言） | **D_int** | 未检 | **未检**（本笔记不做外部检索，无法判定） | 属**新颖性断言**，本笔记按纪律不下判断；若 P1 需要引用该定位，须由 `paper-consensus` / `citation-and-related-work` 另行核验（2018 年后该领域文献量很大） |
| 14 | "DDPGsRT and NNaRT are not reported in the table because they performed worse than the corresponding models that did not consider reaction time delay" （§5.2） | 无数字（仅一句话） | **D_int** | 未检 | **未报告** | **选择性报告**：两个被否决的模型**只给结论不给数字**。后果：**无法把"反应延迟 1 s"的增益与"奖励函数类型"的增益分离**——DDPGvRT（速度奖励+RT）优于 DDPGs（间距奖励、无 RT），其中 RT 的独立贡献**从未被干净地隔离**（因为 DDPGsRT 被隐去） |

**等级分布**：B_int × 4（#1、#3、#5 泛化部分、#7）、C_int × 5（#2、#4 奖励比较、#5 自适应、#8、#9、#11）、D_int × 5（#4 公式、#6、#10、#12、#13、#14）。**无 A_int**（无预注册、无 CI、无独立重复）。摘要/结论中的 C/D 级断言已在上表逐条标出：**#2（SD 最低）、#6（方差）、#12（实时性）为最需警惕的三条**。

---

## 三、方法可复现性清单

| 项 | 论文是否给出 | 具体位置 | 缺失影响 |
|---|---|---|---|
| **数据来源与版本** | **部分给出** | §3.1 SH-NDS：Tongji + GM + VTTI 联合，**5 辆车**，**60 名中国驾驶员**，**总里程 161,055 km**，采集期 2012-12 至 2015-12；§3.2 SHRP2 NextGen DAS，**10–50 Hz**（GPS、纵/横向加速度、CAN 转向与油门、雷达相对距离与速度、4 路同步摄像头） | **数据不可获得**：SH-NDS 为机构联合数据，论文**未说明任何申请入口、许可条款或再分发条件**。→ **本文结果在外部完全不可复现**（这是最致命的一项） |
| **预处理与划分方式** | **给出**（较完整） | §3.3 跟驰时段自动提取 4 条判据：①雷达目标 ID 恒定 ②纵向距离 **<120 m** ③横向距离 **<2.5 m** ④时长 **>15 s**；视频人工确认；**仅保留 limited access expressways and freeways**；§3.3 从 60 名中随机取 **20 名**，每人随机 **100 段**，每人 **70 标定 / 30 验证**，共 **2,000 段 = 827 min** | 随机抽样**未给随机种子**；"随机取 20 名"与"每人随机 100 段"的具体实现不可复现 → 他人无法构造等价子集。**未报告被筛掉的时段数与筛除理由分布** |
| **模型/实验装置规格** | **给出**（仿真侧）；**未给**（硬件侧） | §4.1 "A simple car-following simulation environment was implemented"：前车轨迹**外部输入**、跟驰车状态用**运动学质点模型**（式 3）更新，ΔT = **0.1 s**；§4.3 actor/critic 各 3 层（1 隐藏层 **30** 神经元；RT 模型 **100**），隐藏层 ReLU（原文误写 "RLU"）、actor 输出层 tanh；动作 = 纵向加速度，限 **−3 ~ 3 m/s²** | 仿真环境为**自建质点模型**，非经过验证的交通仿真器 → **无车辆动力学、无执行器延迟、无传感器噪声**；**无硬件/算力平台信息** → 训练与推理成本不可评估。**开环**：前车轨迹由数据驱动，跟驰车动作**不影响**前车 → **无闭环交互、无弦稳定性** |
| **超参数与搜索空间** | **给出**（表 2） | 表 2：学习率 **0.0005**（Adam）、折扣因子 γ = **0.9**、minibatch **256**、replay start size **7000**、replay memory **10000**、软目标更新 τ = **0.01**；§4.5 OU 探索噪声 θ = **0.15**、σ = **0.2**；§5.4 训练 **60 episodes**；§4.3 反应延迟 **1 s**（依 Zhou et al. (32)） | **无超参数搜索空间与选优协议**：表 2 只说 "determined by testing a randomly sampled training dataset" ——**"randomly sampled training dataset" 未定义**（抽了哪些驾驶员？抽了几次？按什么指标选？）→ 若该抽样子集与最终 70/30 划分有重叠，则**存在额外泄漏，且不可判定** |
| **随机种子 / 重复次数** | **未给出** | 全文无 seed（已 grep 核实）；§5.4 "repeated for 60 episodes" 是单次训练内的回合数 | **无法复现方差，无法判断任何模型间差异是否超出随机波动**；配合"以测试误差选最优 agent"，本文所有 DDPG 数字均为**乐观点估计** |
| **评价指标定义（含边界情况）** | **给出**（式 5、6），但**命名与实现不一致、聚合口径有歧义** | 式 (5)：RMSPE of spacing = **sqrt( Σ(S_sim − S_obs)² / Σ(S_obs)² )**；式 (6) 同构（速度）。§4.2 引 Punzo & Montanino (37) 作为依据 | ① 该式是**全数据池化的归一化 RMSE（NRMSE，L2 归一）**，**不是**通常意义上的 RMSPE（逐点百分比误差的均方根）→ **命名不精确**；② **N 的口径未定义**：是"所有时段所有时间步池化"还是"每段先算再聚合"？若池化，**大步距样本主导指标**，而安全关键的**小步距区间权重极低**；③ **无任何安全类指标**（无 TTC、无最小间距、无碰撞率）、**无舒适性指标**（无 jerk、无加速度平方积分） |
| **基线实现来源** | **部分给出** | IDM：式 (1)(2)，MATLAB® **Genetic Algorithm Toolbox** 标定，最大代数 300 / stall 300… （原文："maximum number of generations at 300, number of stall generations at 100, and population size at 300"），**每驾驶员 12 次运行取误差最小者**；RNN 复现自 Zhou et al. (32)（隐藏单元 **60**）；Loess 复现自 Papathanasopoulou & Antoniou (28)（span = **0.4**、tri-cube 权重）；NNa = 与 DDPGv actor **同构**的前馈网络，**以最小化加速度预测误差训练** | **基线目标函数与 DDPG 不同源**（NNa 监督拟合加速度，DDPG 优化累积回报），但**评估指标是轨迹 RMSPE**（误差会累积）→ **对比不完全公平**，作者未讨论此不对称。**IDM 的 12 次 GA 运行取最小者** = winner's curse，**未报告 12 次运行的分布**；**未说明"最小误差"是在标定集还是验证集上取的** → 若在验证集上取，则 IDM 也被乐观偏置（方向对 DDPG 不利），若在标定集上取，则 DDPG 与 IDM 的选优协议**不对等**（方向对 DDPG 有利）。**两种可能都无法从论文排除** |
| **显著性检验方法** | **未给出** | 全文 **0 处** p 值 / 置信区间 / 效应量 / 标准误 / 检验名（已 grep 核实） | 所有"优于/最低"均是**点估计排序**，**无统计推断**；28 个模型×指标×层级比较**无多重比较校正** → **膨胀的假阳性风险** |
| **代码/数据可用性声明** | **未给出** | 全文无代码仓库、无数据申请入口、无补充材料说明；仅致谢列基金（NSFC 51522810、51878498；上海市科委 18DZ1200200；111 项目 B17032） | **无任何可复现路径**。→ 本文属"**结论可读、过程不可复现**"类型；P1 若需以本文为基线，**只能引用其报告值**（并标"文献报告值，协议不同，不可直接比较"），**不能声称复现** |

---

## 四、关键数字表

> **单位、样本量、数据集名称三件事必须跟数字同行。** 本节所有数字均抄自 arXiv v1 印出的表格/图内数据标签；**误差棒长度（SD）为 PDF 矢量坐标反算值，标 `[矢量重建]`**（非论文印出数字，**不得进入对外文本**）。

### 4.1 主结果：图 7 —— 7 个模型的 intra-/inter-driver 验证误差（RMSPE，%）

| 指标 | 值 | 不确定度 | 出处 | 备注（数据集 / 设置） |
|---|---|---|---|---|
| **DDPGvRT intra-driver spacing RMSPE** | **18.23** | 未报告 CI；SD **≈5.2** `[矢量重建]` | 图 7(a) 数据标签 | SH-NDS，20 名驾驶员 × 30 个验证时段/人；速度奖励 + 1 s 反应延迟；**该值即摘要中的"18%"** |
| **DDPGvRT inter-driver spacing RMSPE** | **21.94** | 未报告 CI；SD **≈14.1** `[矢量重建]` | 图 7(a) | 同上；标定驾驶员 → 其余 19 名，20×20 矩阵 |
| **DDPGvRT intra-driver speed RMSPE** | **5.67** | 未报告 CI；SD **≈1.7** `[矢量重建]` | 图 7(b) | 同上；**该值即摘要中的"5%"**；本模型 SD 确为 7 个模型中最低 |
| **DDPGvRT inter-driver speed RMSPE** | **6.66** | 未报告 CI；SD **≈1.6** `[矢量重建]` | 图 7(b) | 同上；SD 亦为最低 |
| DDPGv intra / inter spacing | 18.67 / 28.69 | SD ≈3.1 / 8.2 `[矢量重建]` | 图 7(a) | 速度奖励、**无**反应延迟 |
| DDPGv intra / inter speed | 7.48 / 7.89 | SD ≈3.4 / 2.6 `[矢量重建]` | 图 7(b) | 同上 |
| DDPGs intra / inter spacing | 22.52 / 31.13 | SD ≈4.7 / 7.8 `[矢量重建]` | 图 7(a) | **间距**奖励、无反应延迟 |
| DDPGs intra / inter speed | 11.46 / 13.03 | SD ≈7.5 / 7.3 `[矢量重建]` | 图 7(b) | 同上 |
| **IDM** intra / inter spacing | **21.88 / 27.46** | SD ≈8.6 / 9.8 `[矢量重建]` | 图 7(a) | GA 标定（300 代 / stall 100 / 种群 300，**12 次运行取最优**） |
| **IDM** intra / inter speed | **8.97 / 10.44** | SD ≈7.7 / 6.9 `[矢量重建]` | 图 7(b) | 同上 |
| RNN intra / inter spacing | 23.75 / 24.31 | SD ≈3.4 / **2.5** `[矢量重建]` | 图 7(a) | 复现 Zhou et al. (32)，隐藏单元 60 |
| RNN intra / inter speed | 8.47 / 7.98 | SD ≈7.8 / 3.7 `[矢量重建]` | 图 7(b) | 同上 |
| Loess intra / inter spacing | 30.67 / 31.24 | SD ≈15.3 / 15.4 `[矢量重建]` | 图 7(a) | span 0.4，tri-cube 权重 |
| Loess intra / inter speed | 10.66 / 12.25 | SD ≈8.5 / 8.3 `[矢量重建]` | 图 7(b) | 同上 |
| NNa intra / inter spacing | 36.18 / 44.26 | SD ≈14.9 / 18.1 `[矢量重建]` | 图 7(a) | 前馈网络，与 DDPGv actor 同构，**以加速度误差为损失** |
| NNa intra / inter speed | 14.24 / 14.46 | SD ≈14.2 / 9.4 `[矢量重建]` | 图 7(b) | 同上 |

**矢量复算验证记录（本节最关键的方法学动作）**：图 7 的两个面板用 PDF 绘图指令反解 y 轴标定——面板 (a) **y=0 @ 313.2 pt，y=70 @ 87.5 pt**（3.2243 pt/单位）；面板 (b) **y=0 @ 593.3 pt，y=30 @ 378.1 pt**（7.1733 pt/单位）。用该标定反算 14 根柱的柱顶，**逐一复现出论文印出的全部 28 个数据标签**（偏差 < 0.02 个百分点），据此确认**数据标签提取无误、误差棒为"自柱顶向上的单侧 SD"**。误差棒本身**无数字标签**，故上表 SD 全部为反算值。

### 4.2 逐驾驶员/逐风格：表 4（DDPGvRT，inter-driver spacing）

| 指标 | 值 | 不确定度 | 出处 | 备注 |
|---|---|---|---|---|
| 激进标定 → 激进验证（A→A） | 0.1984 | 未报告；**每格 n 未报告** | 表 4 | **无单位行**；与图 7 的百分数口径**相差 100 倍**（应读作 19.84%） |
| 激进标定 → 保守验证（A→C） | 0.2398 | 未报告 | 表 4 | 跨风格泛化，比 A→A 差 4.14 个百分点 |
| 保守标定 → 激进验证（C→A） | 0.2705 | 未报告 | 表 4 | **全表最差**；保守型模型对激进驾驶员的泛化最弱 |
| 保守标定 → 保守验证（C→C） | 0.2259 | 未报告 | 表 4 | 同风格泛化优于跨风格 |

### 4.3 数据规模与描述统计

| 指标 | 值 | 不确定度 | 出处 | 备注 |
|---|---|---|---|---|
| SH-NDS 总规模 | 5 辆车 / 60 名驾驶员 / 161,055 km | 未报告 | §3.1 | 采集期 2012-12 ~ 2015-12 |
| **本文实际使用** | **20 名驾驶员 / 每人 100 段 / 共 2,000 段 / 827 min** | 未报告 | §3.3 | 占总规模驾驶员的 1/3；**未报告被排除的 40 名驾驶员特征** → 选择偏置不可评估 |
| 平均时段长度（派生） | ≈24.8 s | — | **本笔记计算值**（827×60/2000） | 由论文数字派生，非论文印出 |
| 划分 | 70 标定 / 30 验证（每人） | 未报告 | §3.3、§5.1 | 两级验证：intra-driver 与 inter-driver（20×20 全对） |
| 表 1 激进型 | 间距均值 **15.90 m**、速度 **10.50 m/s**、\|Δv\| **0.76 m/s**、时距 **1.73 s**、\|a\| **0.35 m/s²**（min −3.65 / max 2.37）、停车时间占比 **1.39%** | 未报告 SD/CI | 表 1 | **列名 "Absolute Relative Speed" / "Absolute Acceleration" 与负的 Min 值不自洽** |
| 表 1 保守型 | **20.10 m**、**9.20 m/s**、**0.81 m/s**、**2.28 s**、**0.31 m/s²**（min −2.94 / max 2.03）、**1.38%** | 未报告 SD/CI | 表 1 | 同上 |
| 表 1 全体 | **17.53 m**、**9.99 m/s**、**0.78 m/s**、**1.94 s**、**0.34 m/s²**（min −3.65 / max 2.37）、**1.38%** | 未报告 SD/CI | 表 1 | 同上 |

### 4.4 训练设置（表 2、§4.3、§4.5）

| 指标 | 值 | 出处 |
|---|---|---|
| 学习率（Adam） | 0.0005 | 表 2 |
| 折扣因子 γ | 0.9 | 表 2 |
| Minibatch size | 256 | 表 2 |
| Replay start size / Replay memory | 7000 / 10000 | 表 2 |
| 软目标更新 τ | 0.01 | 表 2 |
| OU 探索噪声 θ / σ | 0.15 / 0.2 | §4.5 |
| 仿真步长 ΔT | 0.1 s | §2.3 |
| 动作范围（纵向加速度） | −3 ~ +3 m/s² | §2.3 |
| 隐藏层神经元 | 30（非 RT 模型）/ 100（RT 模型） | §4.3 |
| 输入维数 | 30 或 40（RT 模型，取时序窗） | §4.3 |
| 反应延迟 RT | 1 s（依 Zhou et al. (32)） | §4.3 |
| 训练回合数 | 60 episodes/驾驶员 | §5.4 |
| 收敛回合（DDPGs，单例） | ≈20 | §5.4、图 6 |
| 重训收敛回合（n=3） | ≈8 episodes | §6.3、图 10 |

### 数字口径对照表

> **触发条件满足**：同一指标（"spacing/speed validation error"、"RMSPE"）在本文出现 ≥2 个数值，且存在"摘要 vs 图"、"intra vs inter"、"图 vs 表"、"分数 vs 百分数"四类口径差。**每个数值一行，口径列不得为空；引用任一数值都必须连同口径一起引。**

| 指标 | 数值 | 数据集/划分 | 验证层级 | 单位口径 | 其他设置 | 出处 |
|---|---|---|---|---|---|---|
| spacing validation error | **18%** | SH-NDS 20 驾驶员 | **未说明**（实为 intra-driver） | 摘要用整数百分数 | DDPGvRT | Abstract |
| spacing validation error | **18.23** | SH-NDS，20 驾驶员 × 30 验证段 | **intra**-driver | **百分数**（纵轴 "RMSPE (100%)"） | DDPGvRT，速度奖励 + 1 s RT | 图 7(a) 数据标签 |
| spacing validation error | **21.94** | SH-NDS，标定驾驶员 → 其余 19 人（20×20） | **inter**-driver | **百分数** | DDPGvRT | 图 7(a) 数据标签 |
| spacing validation error | **0.1984**（A→A 子集） | SH-NDS，激进标定 → 激进验证 | inter-driver 子集 | **分数**（无单位行，= 19.84%） | DDPGvRT | 表 4 |
| speed validation error | **5%** | SH-NDS 20 驾驶员 | **未说明**（实为 intra-driver） | 摘要用整数百分数 | DDPGvRT | Abstract |
| speed validation error | **5.67** | SH-NDS，20 驾驶员 × 30 验证段 | **intra**-driver | **百分数** | DDPGvRT | 图 7(b) 数据标签 |
| speed validation error | **6.66** | SH-NDS，标定驾驶员 → 其余 19 人 | **inter**-driver | **百分数** | DDPGvRT | 图 7(b) 数据标签 |
| RMSPE of spacing | **≈0.2 ~ 0.5**（收敛后） | SH-NDS，**训练/测试过程曲线** | 训练过程（非最终验证） | **分数**（纵轴 0–4 / 0–8） | **DDPGs**，随机 1 名驾驶员 | 图 6（[估读]，轴刻度分辨率约 0.5） |
| RMSPE of spacing | **22.52** | SH-NDS，20 驾驶员 × 30 验证段 | intra-driver（**最终验证**） | **百分数** | **DDPGs** | 图 7(a) 数据标签 |

**口径自洽性交叉检查（通过）**：图 6（分数，DDPGs 收敛后 ≈0.2–0.5）×100 = 20–50%，与图 7(a) 中 DDPGs 的 intra-driver 22.52% **同量级**——这独立支持"图 6 用分数、图 7 用百分数"的读法，也支持"表 4 的 0.1984 应读作 19.84%"。

**引用纪律**：以后引用本文任何一个准确度数字，**必须**同时带上下面的 `citation_qualifier`，并显式指明"intra-driver 还是 inter-driver"、"百分数还是分数"。**只写"18%"而不指明 intra-driver，属口径失实。**

---

## 五、统计与推断旗标

| # | 旗标 | 具体证据 | 后果 |
|---|---|---|---|
| S1 | **零统计推断** | 全文 grep：`significan` 仅 3 处且均非统计语境；`p <` / `p-value` / `confidence interval` / `effect size` / `standard error` / `t-test` / `ANOVA` / `Wilcoxon` **各 0 处** | 所有"outperformed / lowest"均为**点估计排序**，**不构成统计结论**；措辞强度（"outperformed all"）**超过**证据允许强度 |
| S2 | **模型选择使用测试集（信息泄漏）** | §5.4 "the RL agent that generated the **smallest sum of training and test errors** was selected" | DDPG 的 intra-driver 数字（18.23% / 5.67%）为**乐观偏置估计**；这是本文**最严重的方法学缺陷**，直接命中主张 #1 |
| S3 | **基线选优协议与主方法不对等（且方向不可判定）** | §5.3 IDM："**Twelve runs** were conducted for each driver, and the set of parameters with the **minimum error (RMSPE)** was chosen"；**未说明该 RMSPE 取自标定集还是验证集** | 若取自标定集：IDM 未获同等"测试集选优"待遇 → **对 DDPG 有利的不对等**；若取自验证集：IDM 也被乐观偏置。**两种可能都无法从论文排除** → IDM 对比的公平性**不可核验** |
| S4 | **选择性报告被否决模型** | §5.2 "DDPGsRT and NNaRT are **not reported** … because they performed worse" | 只给结论不给数字 → **无法分离 RT 的独立增益与奖励函数的增益**；也无法判断"worse"是否超出运行间波动 |
| S5 | **方差口径混淆（最易被误引）** | 图 7 图题 "Mean and **standard deviation** (verticals above the bars) of intra- and inter-driver validation errors" | 该 SD 是**跨验证时段/跨驾驶员的离散度**，**不是**训练运行间（种子）方差。任何把它读作"运行稳定性"的引用都是**错误引用** |
| S6 | **误差棒语义未定义** | 图 7 未标注误差棒是 SD 还是 SE，未说明单侧或双侧 | 若实为 SE，则 SD = SE×√n（n=30 时段 → ×5.48），图 7 的"低离散度"结论会**完全反转**；须作者澄清 |
| S7 | **多重比较未校正** | 7 模型 × 2 指标 × 2 层级 = **28 个比较**，无任何校正 | **膨胀的假阳性风险**；尤其 #2 这类"SD 也最低"的边缘断言在无校正下更不可靠 |
| S8 | **每格样本量缺失** | 表 4 的 2×2 只给均值，**未给每格驾驶员数** | 无法判断 0.1984 vs 0.2398 的差值精度；若某格 n 很小，该差值可能完全由个别驾驶员驱动 |
| S9 | **无功效分析 / 样本量由算力而非功效决定** | §3.3 "Considering that training DDPG and the comparison models requires substantial time and computing resources, study data was further limited to the car-following periods of **20 drivers**" | 20 名驾驶员是**算力妥协**，不是功效设计；无最小可检测效应量 |
| S10 | **"类人"无独立判据（操作化缺口）** | 题名与摘要主张 "human-like"，但唯一判据是轨迹 RMSPE（图 7）+ 2 个样本的轨迹目视对比（图 8） | **循环论证风险**：以"复现人类轨迹的误差"定义"类人"，再用"类人"解释"误差小" |
| S11 | **未做等价检验（但未犯"p>0.05 当无差异"的错）** | 全文无"无差异"类断言 | **未见该典型推断错误**（记录为"未发现"，以示区分） |
| S12 | **相关/因果未误用** | 全文为模型拟合优度比较，无因果主张 | **未发现因果误用** |
| S13 | **分布假设未检验，但也未使用参数检验** | 无正态性检验、无方差齐性检验，同时无参数检验 | 属"**未做检验**"而非"**做错检验**"；但反过来也意味着**没有任何推断基础** |

---

## 六、缺失信息清单

（每条给出可执行动作与缺失后果。）

1. **未报告：DDPG 训练的随机种子与独立重复次数。**
   - **影响**：无法判断 18.23%（DDPGvRT）vs 18.67%（DDPGv）vs 21.88%（IDM）之间的差异是否超出运行间波动；也无法复核 #2 那条"SD 最低"的断言。
   - **可执行动作**：向作者索取种子列表，并要求以 ≥5 次独立重训报告 mean ± std 或 95% CI。

2. **未报告：图 7 误差棒的具体数值。**
   - **影响**：无法复核"having the lowest … standard deviation on spacing and speed"；本笔记只能用矢量坐标反算（`[矢量重建]`），属**重建而非引用**。
   - **可执行动作**：索取"每模型 × 每验证层级 × 每指标"的 mean±SD 明细表（含 n）。

3. **未报告：DDPGsRT 与 NNaRT 的数值结果。**
   - **影响**：使"1 s 反应延迟"的独立贡献**永远无法从已发表材料中分离**——这是 P1 若想引用"考虑反应延迟带来改善"时的主要障碍。
   - **可执行动作**：索取这两个模型在图 7 口径下的 RMSPE 全表。

4. **未报告：表 4 每格的驾驶员人数与逐驾驶员误差。**
   - **影响**：0.1984/0.2398/0.2705/0.2259 的精度未知；也无法判断"保守型模型对激进驾驶员泛化最差"（C→A = 0.2705）是否由少数驾驶员驱动。
   - **可执行动作**：索取 k-means 分组的**驾驶员名单**与分组 n。

5. **报告但不可核验：奖励函数式 (7)(8) 的符号方向与图 6 的 "Reward" 量纲不自洽。**
   - **需要什么才能核验**：作者代码，或正式版勘误说明。
   - **两种解释的后果**：若实际实现为 `−log|·|`（或按负代价累计）→ §4.2 的公式排版有误，**"奖励函数设计"一节的表述需重写**（但不影响 RMSPE 结果）；若确按印出公式实现 → 则优化方向与"minimizing the disparity"矛盾，**其结果的可解释性论证崩塌**。二者对 P1 的含义完全不同。

6. **报告口径有歧义：摘要 "spacing validation error of 18% and speed validation error of 5%" 未指明验证层级。**
   - **两种解释**：intra-driver（18.23% / 5.67%）或 inter-driver（21.94% / 6.66%）。
   - **后果**：把 18% 当作"泛化误差"引用会**低估 3.71 个百分点**；反之把 21.94% 当作"精度"会低估模型在同驾驶员上的表现。→ **引用时必须显式标注层级**。

7. **报告口径有歧义：表 1 列名 "Absolute Relative Speed (m/s)" 与 "Absolute Acceleration (m/s²)" 的 Min 为负值（−4.90 / −3.65）。**
   - **两种解释**：① 列名中的 "Absolute" 是术语性误用，统计量实为**带符号**量；② 均值列（0.76 / 0.35）是绝对值统计、Min/Max 列是带符号统计（**列内口径混合**）。
   - **后果**：若为 ②，则"激进型 |Δv| 均值 0.76 < 保守型 0.81"这类比较不可直接解释（需知道各列口径）。

8. **报告口径有歧义：表 4 无单位行，0.1984 与图 7 的 21.94% 相差 100 倍。**
   - **两种解释**：分数（0.1984 = 19.84%，**与图 7 自洽，本笔记采纳**）或其它。
   - **后果**：若误读为百分数，会把本文最好的泛化结果误报为"0.2%"，属**数量级错误**。

9. **未报告（且可能不可得）：代码与数据可用性。**
   - **影响**：SH-NDS 为 Tongji/GM/VTTI 联合数据，**无申请入口、无许可说明**；无代码、无权重、无补充材料。
   - **可执行动作**：直接联系通讯作者（Xuesong Wang，同济大学）询问数据申请通道与代码释放可能；**在得到答复前，P1 不得计划"复现本文基线"**。

10. **未报告：训练与推理的计算成本。**
    - **影响**：§7 的 "only needs a few seconds to converge" 与 "feasible … just a forward pass" 无任何计时/平台信息支撑；P1 的"端到端延迟 / MCU 内存占用"指标**不可引用本文任何数字**。
    - **可执行动作**：索取训练平台、单驾驶员训练耗时、推理单步延迟。

11. **报告但不可核验：图 8 红曲线归属（图题 vs 正文不一致）。**
    - **图题**："FIGURE 8 Car-following trajectories generated by the IDM, RNN, and **DDPGv** model."
    - **正文**："replicated by the **DDPGvRT**, IDM, and RNN" + "the **DDPGvRT** model (in red)"
    - **需要什么才能核验**：作者确认；或正式版图题修正。
    - **后果**：图 8 究竟支持 DDPGv 还是 DDPGvRT 的定性展示主张，**当前无法确定**。

12. **未报告：k-means 风格聚类的效度依据。**
    - **影响**：k=2 无轮廓系数/有效性指标/k 的敏感性分析；而全文的"跨风格泛化"结论（表 4、§7 的"driver archetypes"建议）**完全建立在这个二分类上**。
    - **可执行动作**：索取 k 的选择依据与不同 k 下的分组稳定性。

---

## 七、复用价值判断

| 问题 | 结论 |
|---|---|
| **方法可否搬到我的问题？需要改什么？** | **不能直接搬**。本文是**单车、单车道、单前车、纵向加速度**的开环跟驰策略，状态仅 3 维（v, Δv, S）。搬到 P1 需要：① 状态扩到多车/多车道（本文的"社会压力"完全隐式、无结构）；② 加入闭环（本文前车轨迹外部注入，跟驰车动作不影响前车）；③ 加入车队/编队耦合与弦稳定性；④ 重新定义奖励（本文奖励需要真值轨迹，部署时不可计算）。**唯一可直接借用的是它的"两级验证"设计（intra-driver + inter-driver 20×20 矩阵）**——这是一个干净、可移植的泛化评估模板。 |
| **评价协议可否直接对齐（指标、划分、基线）？** | **划分可对齐、指标只能部分对齐、基线部分可对齐**。划分：70/30 + 两级验证 ✅ 可移植（且比 P1 现有协议更严格）。指标：其 RMSPE（式 5/6）是**池化归一化 RMSE**，与 P1 的"跟车误差 RMSE"**同族但不同口径**；**P1 的其余 5 项指标（加速度平方积分、Jerk 峰值、车道居中偏差、前轮转角方差、延迟/内存）本文全部没有**。基线：IDM ✅（P1 也可用）、RNN/Loess/NNa ✅ 可作为数据驱动类基线、**Gipps ❌（本文未实现）**。 |
| **数据/代码可否直接取用？许可如何？** | **都不可取用**。无代码、无权重、无数据申请入口；SH-NDS 为机构联合自然驾驶数据，论文**未给出任何许可或再分发条款**。→ **P1 不得计划复现本文**；只能引用其报告值。 |
| **若要引用其数字，引用时必须带上的限定语是什么？** | 见下 `citation_qualifier` 单行；核心三点：① **intra- 还是 inter-driver**；② **百分数还是分数**；③ **单一训练运行、无种子、无显著性检验、且最佳 agent 由测试误差选出**。且 P1 稿件中**必须**加"文献报告值，协议不同，不可直接比较"。 |

```
citation_qualifier: SH-NDS（2015 上海自然驾驶研究，限速封闭快速路/高速、单车道跟驰、纵向动力学）20 名驾驶员 × 100 个跟驰时段 = 2,000 段 / 827 min，逐驾驶员标定、70/30 划分、两级验证（intra-driver 与 inter-driver 20×20）；最高结果 DDPGvRT 的 18%/5% 指 intra-driver 验证 RMSPE（inter-driver 为 21.94%/6.66%，表 4 的 0.1984 为同指标分数口径 = 19.84%）；单一训练运行、未报告随机种子与运行间方差、无任何显著性检验或置信区间，且最佳 agent 以"训练+测试误差之和最小"选出（含测试集信息）；结果为开环回放 + 运动学质点模型仿真，非实车、非闭环
```

（**单行，机器可读**；下游 `paper-experiment-analyzer` 的"断言强度校准"与 `citation-and-related-work` 的层 3 核验**必须**以本行为限定语基准，不得自行改写。）

---

## 八、红队三条

### 1. 领域最懂的人会质疑
**质疑**："你把'18%'当成这个模型的泛化精度记住了，但它其实是 **intra-driver**（同一驾驶员的留出时段）；真正对应'跨驾驶员/跨风格泛化'的是 **21.94%**，而且在 C→A 那个格子里是 **0.2705（27.05%）**——比 IDM 的平均 27.46% 只差 0.4 个百分点。你还把'最低 SD'记成了结论，但 spacing 上 DDPGvRT 的误差棒根本不是最短的。"

**需要什么证据才能消解**：回到图 7(a)/(b) 与表 4，逐个数字带层级与单位口径引用（本笔记 §四口径对照表已做）；SD 断言须作者给出 mean±SD 明细表。**消解结果**：本笔记已把主张 #2 从"结果支撑"降为"**部分成立**"、等级降为 **C_int**，并把 #1 的限定语写进 `citation_qualifier`。→ §二、§四已同步回改。

### 2. 方法与统计视角会质疑
**质疑**："你给 #1 打了 **B_int**，但这条主张的证据是**单次训练运行 + 无 CI + 无显著性检验 + 且模型是在测试集上选出来的**。按全局 §1 的 A 级定义（预注册 + 对照 + 足够功效 + 效应量与 CI + 内部独立重复），它连 B 的边都不该摸到——'模型选择用了测试集'是**直接的信息泄漏**，不是'边界'。"

**需要什么证据才能消解**：出示**固定选优准则**（例如按训练集误差选、或按独立验证折选）后的重训结果，以及 ≥5 次独立种子的 RMSPE 分布。

**裁定**：**部分接受**。本笔记保留 `B_int` 但**在台账 #1 的"缺口"列显式写明"模型选择使用测试集 → 乐观偏置，严格说该数字不可作为无偏估计；若按'设计良好但有边界'从严，可降为 C_int"**，并把 S2 列为本文最严重的方法学缺陷。**不**把等级单方面下调为 C_int 的理由是：数据是**真实自然驾驶轨迹**（非合成流量），7 个模型共用同一评估协议，且 inter-driver 的 21.94% **不受**该泄漏影响（其评估集与选优集不同）——因此"优于基线"的方向性结论仍有 B 级支撑。**降级决定权留给父代理/项目负责人**，不擅自改强度。

### 3. 编辑 / 邻域读者会质疑
**质疑**："你的缺失信息清单如果只写'未报告种子'，读者仍然不知道该不该用这篇。到底能不能复现？如果只是'未报告'，我去问作者不就行了？"

**需要什么证据才能消解**：把每条缺失改成**可执行动作 + 具体后果**，并明确**是否可能补上**。

**裁定**：已在 §六 全部改造为"未报告 X → 影响 Y → 可执行动作 Z"三段式。其中必须点明一条**不可通过问作者解决**的硬缺口：**SH-NDS 数据无申请入口、无许可条款、无代码与权重释放**（§六 第 9 条）→ **本文在外部不可复现**，这决定了 P1 对它的使用方式只能是"引用报告值 + 标协议不同"，而不能是"复现基线"。

---

## 九、限制

1. **材料限制（版本）**：本笔记基于 **arXiv:1901.00569v1**（TRR 排版模板），**不是** TRC 2018, 97:348–368 的正式排版版。arXiv v1 中留有 **3 处未解析交叉引用 `Error! Reference source not found.`**（含选择 IDM 作为对照的**理由出处**、SH-NDS 数据出处、以及 §2.1 的一处）。因此 §三 复现性清单中"**基线实现来源**"与"**数据来源与版本**"两项的**可判定性下降**；**所有数字在入稿前须与正式版逐条核对**（尤其图 7 与表 4）。
2. **复算限制**：未获原始数据与代码 → **无法验证方差、异常值与统计量**，只能做自洽性检查。本笔记对图 7 的误差棒做了**矢量坐标反算**（`[矢量重建]`），已用论文印出的 28 个数据标签完成标定验证（偏差 < 0.02 个百分点），但**反算值不得进入任何对外文本**；#2 的"SD 非最低"结论属**重建发现**，须作者明细表确认后才可作为正式审稿意见。
3. **外部复现状态限制**：本笔记**未做外部引用检索**，故"外部复现"列**一律为"未检"**。这是**信息缺失**，不等于"无外部证据"，也**不得**据此把本文说成"仅一次性证据"。本文 Crossref 记录显示被引 **504** 次（2026-10-02 查询），独立复现的方向与数量须由 `paper-consensus` / `paper-discovery` 另行核验。
4. **视角限制**：本笔记**不评价**本文的重要性与新颖性（主张 #13 的"first to use DRL for car-following"属新颖性断言，本笔记按纪律**不下判断**）。该判断交 `cross-paper-synthesizer` 与 `research-gap-hunter`。
5. **时效限制**：精读日期 **2026-10-02**；Crossref 复查 `update-to` 为空、无撤稿记录，但若此后出现勘误/更正，本笔记未反映。缓解：入稿引用前由 `citation-and-related-work` 复核 DOI 状态。
6. **ODD 限制（对 P1 最关键的一条）**：本文 ODD 为**限速封闭快速路/高速的单车道纵向跟驰**；**P1 的 ODD 是高速主线多车道、人工与自动混行、含编队**。→ **本文结论对 P1 的跨 ODD 迁移无效**（项目 `AGENTS.md` §5 已明示跨 ODD 结论无效）。本笔记不做任何 ODD 外推。

---

## 十、对 P1 的三条具体可用结论

### ① 数据来源与规模，以及与"高速公路主线"ODD 的匹配度

| 项 | 本文 | 与 P1 ODD（高速主线、多车道、人机混行、编队）的匹配 |
|---|---|---|
| **数据集** | **2015 Shanghai Naturalistic Driving Study (SH-NDS)**；Tongji University + General Motors + Virginia Tech Transportation Institute 联合 | 中国城市自然驾驶数据；**非高速主线专用数据集** |
| **原始规模** | **5 辆车 / 60 名中国驾驶员 / 161,055 km**；采集期 **2012-12 ~ 2015-12**；SHRP2 NextGen DAS，**10–50 Hz** | 规模远大于 P1 现有实车数据，但**不可获得**（无申请入口/许可说明） |
| **本文实际使用** | **20 名驾驶员 × 100 段 = 2,000 个跟驰时段，合计 827 分钟**（≈24.8 s/段，本笔记派生）；70 标定/30 验证 | 名义数据量小（≈13.8 小时），但**逐驾驶员建模**（每人 70 段用于标定） |
| **轨迹条数** | **2,000 条跟驰轨迹**（每条 >15 s） | 条数足够做两级验证，但**每条仅纵向** |
| **道路类型** | "the roadway type was identified during the validation phase so only data from car-following periods on **limited access expressways and freeways** were used"（§3.3） | **部分匹配**：属"限速封闭道路"，与高速主线有交集；但**上海快速路 ≠ 高速主线**（匝道密度、限速、交通构成不同），且论文**未分道路子类报告** |
| **场景维度** | **单车道、单前车、纯纵向**。判据：横向距离 **<2.5 m**（只用于筛"同一车道"）、纵向距离 **<120 m**、时长 **>15 s** | **不匹配**：**无换道、无 cut-in、无多车道交互、无编队/车队耦合**；P1 的四类工况（前方无车、邻车插入、前车减速、前车驶离）中只有"前车减速"被隐式覆盖 |
| **风格维度** | k-means **k=2**：aggressive（间距均值 15.90 m、时距 1.73 s）/ conservative（20.10 m、2.28 s） | 可作 P1"驾驶风格分层"的**方法论参考**（但 k=2 无依据，见 §六 第 12 条） |

**结论**：**ODD 部分重叠、场景严重不匹配。** 本文可支持"在限速封闭快速路上、对单前车、纵向跟驰场景下，DRL 策略能比 IDM 更精确地复现真实驾驶员的轨迹"这一**受限结论**；**不可**支持任何关于多车道交互、邻车插入、编队耦合或高速主线的结论。P1 引用时必须写明"其 ODD 为封闭快速路单车道跟驰，与本文高速主线多车道混行 ODD 不同，结论不可直接迁移"。

### ② 指标定义与 P1 指标集的对齐性

| P1 指标 | 本文是否定义/报告 | 可否直接对齐 | 说明 |
|---|---|---|---|
| **跟车误差 RMSE** | ✅ 有，但口径不同 | **只能"概念对齐"，数值不可直接比** | 本文用 **归一化池化 RMSE**：`RMSPE = sqrt( Σ(S_sim−S_obs)² / Σ(S_obs)² )`（式 5），**不是**绝对单位的 RMSE，**也不是**通常的逐点 RMSPE。对齐需三步：① P1 明确是否"池化全部时段"；② 明确分母是 `Σ S_obs²`（L2 归一）而非 `Σ S_obs` 或逐点百分比；③ 注意**该指标对大步距样本敏感、对小步距（安全关键）区间权重极低**。**若 P1 直接引用"18%"作为对照，等于是拿一个不度量小间隙精度的指标去比一个关注安全间距的指标。** |
| **加速度平方积分（舒适性）** | ❌ **无** | **不可对齐** | 表 1 的加速度量（0.35 / 0.31 m/s² 均值、min −3.65 / max 2.37）是**驾驶员数据的描述统计**，**不是模型评价指标**；本文从不评价任何模型输出的加速度质量 |
| **Jerk 峰值** | ❌ **无** | **不可对齐** | 全文无 jerk、无加速度变化率、无平滑性指标 |
| **车道居中偏差** | ❌ **无** | **不可对齐** | 横向距离 2.5 m 仅用于**筛选**跟驰时段，**不是**被评价量；模型输出为**纯纵向加速度**，无横向自由度 |
| **前轮转角方差** | ❌ **无** | **不可对齐** | 动作空间仅纵向加速度（−3 ~ +3 m/s²）；CAN 转向角数据在 §3.2 被提及为**采集项**，但**从未用于建模或评价** |
| **端到端延迟 / MCU 内存占用** | ❌ **无** | **不可对齐** | 无平台、无耗时、无内存（§七 主张 #12 已标 D_int） |
| **安全类指标（TTC / 碰撞 / 最小间距）** | ❌ **无** | **不可对齐**（但**P1 应引为反面论据**） | 作者自认 "absolute safety issues … are not addressed in this approach"（§7）→ **本文的"类人"不含安全保证** |

**结论**：**P1 的 7 项指标中，只有"跟车误差"一项存在概念对应，且必须在口径上重新定义；其余 6 项（含全部舒适性、横向、资源类指标）本文完全未涉及。** → 若在 P1 的 Related Work / 对比表中使用本文，**必须**用"指标集不重叠"分栏呈现，**不得**把本文的 RMSPE 与 P1 的指标集并列比较。

### ③ 可解释性缺口的具体表述（为 P1 的"可解释性 + 零额外传感器成本"卖点提供对手方证据）

**缺口一：奖励本身就是"数据匹配残差"，学到的策略不含任何可解释的中间状态量。**
> "This study used the reward function to facilitate human-like driving by **minimizing the disparity between the values of simulated and observed behavior**."（§4.2）
> 式 (7)(8)：`r_t = log(|S_sim − S_obs| / S_obs)`、`r_t = log(|V_sim − V_obs| / V_obs)`

本文**没有任何**"交通社会压力"式的结构化中间量：状态只有（v, Δv, S），动作是加速度，策略是黑箱 actor 网络。**P1 的对手方证据**：这条路线用"数据驱动的匹配误差"替代了"可解释的物理/社会量"，其"解释"只能是**事后的**（事后敏感度分析），而 OTF 是**事前的第一性标量**。

**缺口二：作者自承网络小，但对已学策略的内部表征零分析。**
> "Although the network structure utilized in our study with only one hidden layer can not be regarded as a truly 'deep' neural network, it fully exploits the main idea of deep reinforcement learning methods and can be easily extended once more input variables are provided."（§7）

全文**无**特征重要性、**无**敏感度分析、**无**策略可视化、**无**对"学到了什么驾驶机制"的任何拆解。**P1 的对手方证据**：即使网络只有 30 个隐藏神经元，作者也**没有**给出任何可读的策略解释——可见"网络小"并不自动带来"可解释"。

**缺口三：作者把"揭示潜在关系"明确列为 future work —— 即当下并未揭示。**
> "By comparing the low-dimension input-based DDPG car-following model, which accepts relative position and speed information, with an image-based end-to-end DDPG model, we may **reveal the latent relationship** between human perception and car-following controlling action."（§7，future work）

**"latent relationship"（潜在关系）** 一词是本文对自己可解释性状态的最诚实描述：**关系是潜在的、尚未被揭示的**。**P1 的对手方证据**：这是"数据驱动路线在 2018 年就自认可解释性未解决"的直接英文原句。

**缺口四：唯一的"可解释性"论证是"假设更一般"，而非"输出可读"。**
> "the model assumes only that drivers select actions to maximize cumulative future rewards, which **agrees with psychological and neuroscientific perspectives** of human behavior"（§7）
> "By adopting reaction time and value function (the expected reward for choosing a certain driving maneuver in current driving condition), the DDPGvRT model considers not only the instantaneous traffic conditions …, but also historical driving behaviors and long-term future rewards"（§7）

即：可解释性论证停留在**建模范式的正当性**（"最大化累积回报"符合心理学），**没有**落到策略输出的可读性。**P1 的对手方证据**：可解释性 ≠ 范式正当性；P1 应把卖点锚在**输出量的可解释性**（OTF 是一个有量纲、可与人因解释对应的标量），而不是"我们的学习范式更符合心理学"。

**缺口五：本文作者主动声明不含安全保证 —— 与"类人"卖点形成张力。**
> "It is worth noting that the proposed DDPG model is intended to reproduce human-like driving behavior …; **absolute safety issues, as well as the handling of human error in historical driving data, are not addressed in this approach.** Safety issues must be addressed within the province of a coupled collision avoidance system, and human errors can then be filtered by an anomaly detection algorithm."（§7）

**对 P1 的双向价值**：一方面这是**对手方证据**（纯数据驱动"类人"路线把安全外包给外挂系统）；另一方面也是**警示**——若 P1 用 OTF 提升"类人性"，**同样不能声称安全性提升**，须与项目 `AGENTS.md` §1 的"不得把仿真写成实车验证"一致。

**关于"零额外传感器成本"的精确结论（P1 可直接引用）**：
本文的**车端**输入只有速度、相对速度、车间间距（雷达 + CAN 即可获得），因此"零额外**车端**传感器成本"在本文成立；**但代价在数据侧**：其奖励函数需要**观测到的真值轨迹**（式 7/8 的 `S_obs`、`V_obs`），故
> "The model can be continuously updated when more data are fed in."（Abstract）／"the policy updating work, however, does not necessarily need to be conducted in real time."（§7）

意味着所谓"持续学习"**只能在离线、有真值标注数据的条件下重训**（每名驾驶员 70 个标注跟驰时段，见 §3.3），**不是**部署后的在线自适应。→ **P1 的差异化表述应写为**：OTF 的输入是"可直接从既有雷达/CAN 实时算出的一阶标量"（无需真值轨迹、无需离线重训），而 DRL 类人路线需要**成对的真值轨迹数据 + 逐驾驶员重训**才能获得同等"个性化"。

---

**交接状态**：本笔记已完成 `deep-paper-reader` §6 全部质量门（作用域已填、台账含内部等级与外部复现两列、外部列一律"未检"、数字口径对照表已填且口径列无空缺、缺失信息 12 条均为可执行动作、`citation_qualifier` 单行已给、红队三条含消解证据、限制 6 条具体）。**下游接口**：`paper-experiment-analyzer`（统计旗标 S1–S13 + 结构化数字 + `citation_qualifier`）、`cross-paper-synthesizer`（台账含 B_int/C_int/D_int 与"未检"）、`citation-and-related-work`（层 3 主张一致性以 `citation_qualifier` 为基准）。
