# Q-优势引导的人机协同安全 RL｜Q-Advantage Integrated Human-Guided Reinforcement Learning for Safe End-to-End Autonomous Driving

- **出处**：IEEE Transactions on Intelligent Transportation Systems, Vol. 27, No. 3, March 2026, pp. 2957–2969（起始页 2957；全文 13 页）｜ **类型**：期刊论文
- **作者**：Yong Wang（University of Hong Kong）et al.（Pei Wang, Seres Automobile；Hongwen He（通讯）, Jingda Wu, Yingjuan Tang, Zirui Kuang, Beijing Institute of Technology）
- **DOI**：10.1109/TITS.2026.3656268
- **全文来源**：`literature/fulltext/meeting2/q-advantage-integrated-human-guided-reinforcement-learning-f__cb4bb9d0.txt`
- **分组**：决策基线 / TITS
- **证据等级初判**：B 级 — 3 个安全攸关任务的闭环对照（7 类基线 + 3 种 QIHG 变体）+ 集成规模消融 + 每法 50 次测试 + 实车 5 次试验，设计与对照充分；边界是**仿真为主、实车仅 5 次试验且无实车侧基线对照、四张表表体在可得全文中缺失、未报随机种子/CI/显著性检验**（等级判据：平台边界写进理由，不因"仿真"二字单独降级）
- **档位建议**：B 略读 — 加权 13 落在 B 档（9–13），且 D1 = 1（相邻环节：安全 RL / 人机引导的**训练范式**，不是 P1 的控制器，也不提供 P1 可复用的评价协议），不满足 A 档"D1 = 2"的硬条件
- **五维打分**：D1=1 D2=2 D3=1 D4=2 D5=1 → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = 3+4+2+2+2 = **13**

## 1. 标题
Q-Advantage Integrated Human-Guided Reinforcement Learning for Safe End-to-End Autonomous Driving｜Q-优势集成的人机引导强化学习，用于安全端到端自动驾驶

## 2. 摘要（≤400 字中文，保留关键数字与结论成立条件）

端到端自动驾驶用 RL 的主要障碍是**样本效率低**与**对奖励设计敏感**。本文提出 **QIHG-RL**（Q-advantage Integrated Human-Guided RL）框架，把机器学习与人类经验结合，含两项设计：① **集成 Q-优势函数**——聚合多个价值网络以增强价值估计；② **集成机制**——把 Q-优势同时嵌入 actor-critic 网络与优先经验回放（PER）。其效果是让智能体利用**稀疏且次优的人类示教**：早期加速策略学习，随训练推进逐步增强自主探索。Q-优势定义为同一状态下**人类动作 Q 值与 RL 动作 Q 值之差**（式 15），集成版取 N 个 critic 的最小值（式 16），再经 `Qclip = max(exp(QEadv), 1) − 1`（式 17）截断：负优势→0（丢弃），正优势→指数放大（加权）。动态权重 ωt 分两段：episode < K 时用常数 κ 强制行为克隆，之后换成 Qclip(t)（式 20）。评估跨**三个安全攸关驾驶任务**（AEB 紧急制动；静态与动态 LCO 换道超车），在 CARLA 中完成，人类被试通过键盘介入。**作者报告的关键数字：相比标准 RL 样本效率提升 167%（QIHG 变体 150 episode 达到传统 RL 400 episode 的水平）；相比当前最优人机引导 RL 基线（Hug-TD3）性能提升 14%**（摘要措辞）。最后用**域随机化 + 语义去噪重映射**的 Sim2Real 流水线部署到真实自动驾驶车辆（Apollo D-KIT Standard S，5 次 LCO 试验全部无碰撞、无压线）。结论成立条件：CARLA 仿真 + 单维动作（刹车开度或转向角）+ 少量实车初步验证；作者明确指出"试验次数有限，不能宣称完全可部署"。

## 3. 结论（≤350 字中文：作者结论节要点 + 关键数字 + 作者自承的局限）

结论节（§IV）要点：QIHG-RL 通过集成 Q-优势函数与 Q-优势集成机制，识别并优先使用高质量人类示教，显著提升数据利用效率、加速策略收敛；在静态/动态 LCO 与 AEB 场景中一致优于基线 HGRL 与标准 RL；**"在两项 LCO 任务上分别取得 19.6% 与 16.1% 的学习效率提升，以及 14.9% 与 15.9% 的驾驶性能增益"**；并学到更平滑、更鲁棒的驾驶策略；真实车辆上验证了物理可行、可泛化的驾驶策略。

补充关键数字（正文 §III）：静态 LCO 中 QIHG-TD3 的回合平均奖励比 HPM 高 **21.2%**、比最强基线 Hug-TD3 高 **14.9%**；动态 LCO 中分别为 **14.8%** 与 **15.9%**；训练期对比 Hug-TD3 的"最优平均奖励"提升为 **19.6%（静态）/16.1%（动态）**；相比传统 RL 的收敛优势写成"**167% 的训练效率提升**"（150 episode vs 400 episode）。安全率：AEB 达 **100%**；静态 LCO 在 6/8/10 m/s 下三种 QIHG 变体均 **100%**，15 m/s 下仍 >70%，而同条件下 HPM 与传统 HGRL **低于 50%**、纯 RL 基线**低于 20%**；动态场景 QIHG-TD3 在 25 m/s 下 **75%**。集成规模消融（Table III 正文摘数）：**N = 3 最优（奖励 0.529、干预率 0.131），N = 4 各项指标退化**。

**作者自承的局限**：① 真实世界场景复杂多变，可能超出当前策略的泛化能力；② 实车**仅 5 次 LCO 试验**，作者原文写"While the limited number of trials prevents definitive claims of full deployability"；③ 未来工作需加入**安全监督层**与**持续学习**、以及预测建模与选择性人类引导；④ 整个控制架构仍为 human-in-the-loop（边缘情形由人接管）。

## 4. 方法一句话（≤60 字）

45×80 单通道语义分割图（+人类引导指示 G(t)）→ 集成 Q-优势调制的 QIHG-TD3（多 critic 取 min，改写 actor-critic 损失与 PER 优先级）→ 单维连续动作（AEB 刹车开度 / LCO 转向角）。

## 5. 图表清单（占位符）

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-QAHG-1} | Fig. 1 | "The overall framework of the proposed methodology. The QIHG-RL methods built upon the actor-critic architecture were trained in simulation for two autonomous driving tasks, and human participants or HPM can provide intermittent guidance (indicated by the dotted line). Following the training phase, the RL strategy is deployed in real-world scenario." | 全框架三块：HGRL 算法 / 真实部署流水线 / 仿真与真实环境；虚线 = 间歇性人类或 HPM 引导；要点：**训练在仿真、部署在真车**这一两段式结构（P1 措辞上限的直接对照） |
| {FIG-QAHG-2} | Fig. 2 | "Computational flow of the ensemble Q-advantage." | 三步计算流：① 每个 critic 分别算人类动作 QH 与 RL 动作 QRL；② 逐 critic 相减得 Qadv；③ 跨 critic 取 min 得 QEadv。要点：这是式 (15)(16) 的图示，是"集成抑制高估"的直接依据；**与 TD3 的 clipped double-Q 同源（取 min）** |
| {FIG-QAHG-3} | Fig. 3 | "Task environments in CARLA. (a), (b) The AEB scenario. (c) The static LCO scenario. (d) The dynamic LCO scenario." | 四个子图对应三个任务；要点：场景为**单车 + 行人/两辆障碍车**的简化设定，不是多车道混行编队——这是"跨 ODD"判断的图证据 |
| {FIG-QAHG-4} | Fig. 4 | "Training rewards of different RL algorithms in the AEB scenario, evaluated across two stages without HPM involvement." | 五条方法曲线；实线 = 均值、阴影 = 标准差；两阶段 = Stage 1（人引导）/ Stage 2（纯 RL）。要点：Vanilla-TD3 表现最差且方差最大；HG-TD3 在移除人类引导后明显下滑；三种 QIHG 变体在 Stage 2 仍持续改善 |
| {FIG-QAHG-5} | Fig. 5 | "Training rewards of different RL algorithms in LCO scenarios. (a) Training reward curves of QIHG-RL and Vanilla-RL algorithms in the static task. (b) Training reward curves of HGRL algorithms based on TD3 in the static task. (c), (d) Reward curves in the dynamic task. (e), (f) Human intervention rates during training for the static and dynamic tasks, respectively." | 六个子图；LCO 训练分三阶段：Stage 1 人引导 / Stage 2 HPM 引导 / Stage 3 纯 RL；vanilla RL 基线只给 10 episode 的 HPM 初始化。要点：(e)(f) 的**干预率曲线**是"HPM 能否替代人类"的直接证据 |
| {FIG-QAHG-6} | Fig. 6 | "Yaw angle in the dynamic driving task. Error bars indicate standard error." ／ 另在正文流中另有一段疑似同图图注残片（逐字）："Yaw angle comparison of different RL strategies. (a) Average yaw angle in the static driving task. (b) Average"（**原文此行在页/栏间断开，后半句缺失**） | 每 episode 平均偏航角（8 种策略、50 次试验），误差棒 = **标准误**（不是 SD，也不是 CI）。要点：三种 QIHG 变体偏航角最低 → 侧向控制最平滑；⚠ 两段图注残片的关系见文末 |
| {FIG-QAHG-7} | Fig. 7 | "Driving performance of different RL strategies in unseen scenarios. Left and right panels correspond to static and dynamic tasks, respectively. Matrix values indicate safety rates of safe driving; \“+\” denotes relative speed difference in dynamic settings." | 热力矩阵：8 种策略 × 4 档速度 × 静态/动态两panel；**20 个测试 episode** 平均。要点：静态任务 QIHG 在 6/8/10 m/s 达 100%、15 m/s 仍 >70%；动态任务 QIHG-TD3 在 25 m/s 为 75%；这是"跨速度泛化"的核心图 |
| {FIG-QAHG-8} | Fig. 8 | "Evaluation performance of the value network during training. (a) Q-value curves in the static driving task. (b) Q-advantages curves in the static driving task. (c) Q-value curves in the dynamic driving task. (d) Q-advantages curves in the dynamic driving task." | 前 100 个人类引导 episode、共 **15,000 步**；要点：早期价值网络**无判别力**（甚至误判人类动作更差，Q-advantage < 0），因此需要 episode < K 的常数权重 κ——这是"为什么必须有 ωt 两段式"的证据 |
| {FIG-QAHG-9} | Fig. 9 | "Comparative performance of well-trained and under-trained RL. (a) The testing scenario. (b) Turning angle curves of both networks during testing. (c) Q-value curves of both networks during testing." | 训练充分 vs 欠训练网络的转向角与 Q 值对比。要点：成熟价值网络对差动作给低 Q 值，欠训练网络对同一劣质动作反而给更高 Q 值（评价能力失效）→ 作者据此警告"训练早期慎用 Q 值算人类动作优势" |
| {FIG-QAHG-10} | Fig. 10 | "Illustration of the semantic denoised remapping technique. (a) Semantic segmentation output from the CARLA built-in model. (b) Segmentation results from the PIDNet model applied to RGB images." | 左右对比 CARLA 内置分割与 PIDNet 分割；要点：非关键类别被重映射为统一背景类、保留交通要素 → 缩小 Sim2Real 语义鸿沟；PIDNet-S-Simple **7.6M 参数** |
| {FIG-QAHG-11} | Fig. 11 | "Illustration of real-world deployment. (a) Experimental setup based on the Apollo D-KIT Standard S platform for Sim2Real transfer of the QIHG-TD3 policy. (b) Sequential snapshots from a real-world LCO trial, showing raw camera images (top) and corresponding denoised remapped semantic frames (bottom). (c) Trajectory comparison demonstrating the effectiveness of the QIHG-TD3 policy in both CARLA simulation (QIHG-TD3) and real-world deployment (PIDNet+QIHG-TD3)." | 实车部署唯一证据图：平台 = Apollo D-KIT Standard S（含车载计算单元、视觉感知、CAN 线控转向）；两辆静态障碍车交错摆放。要点：(c) 是仿真轨迹与实车轨迹的对比，**MSE = 0.01158**；实车仅 5 次 LCO 试验 |
| {TAB-QAHG-1} | Table I | "NETWORK PARAMETERS FOR THE POLICY NETWORK AND VALUE NETWORK" | 策略网络与价值网络的结构参数（所有 RL 方法共用同一架构，以保公平）。**表体未随全文文本提取**（见 §7 第 1 条），逐项层宽/激活/学习率不可核验 |
| {TAB-QAHG-2} | Table II | "PERFORMANCE COMPARISON OF DIFFERENT STRATEGIES ACROSS THREE DRIVING TASKS. HIGHER VALUES (↑) INDICATE BETTER PERFORMANCE" | 10 种策略 × 3 个任务的测试性能，含安全率、回合平均奖励、距离、平滑度，**以标准差为误差范围**；每法 **50 次测试**。表体缺失（同上） |
| {TAB-QAHG-3} | Table III | "ABLATION STUDY OF THE ENSEMBLE Q-ADVANTAGE FUNCTION USING AVERAGED DATA FROM 100–120 TRAINING EPISODES UNDER LCO CONDITIONS" | 集成规模 N 的消融（正文摘数：N=3 最优，奖励 0.529、干预率 0.131；N=4 全面退化）。表体缺失，仅正文 3 个数字可引 |
| {TAB-QAHG-4} | Table IV | "THE SCOPES OF ENVIRONMENT PARAMETERS DURING TRAINING" | 域随机化的环境参数取值范围（传感器配置与车辆状态）。**表体缺失 → P1 无法复刻域随机化范围** |

## 6. 对 P1 的用处

- **与 P1 的关系**：**相邻问题**。同为"高速/安全攸关场景下的 DRL 决策 + TD3 骨干"，但① ODD 不同（CARLA 的 AEB 行人横穿 + 两车静态/动态 LCO，不是高速主线多车道混行编队）；② 任务是单维动作的端到端视觉控制，不是纵横向编队控制；③ 核心贡献是**训练范式**（人引导数据的筛选与加权），不是控制器结构，也没有 OTF 势场或连续时间网络。它**不回答** P1 的 RQ。
- **可迁移**：
  1. **Q-优势 + 集成取 min 的形式**（式 15–17）与 TD3 的 clipped double-Q 同源。P1 若要把 OTF 势场先验转成"建议动作"，可直接借用该形式（把"人类动作"换成"OTF 势场建议动作"），并保留"负优势→0、正优势→指数放大"的截断设计。**这是纯方法层面的启发，不得据此声称任何性能增益**（P1 §1 红线第 1 条）。
  2. **两段式动态权重 ωt**（episode < K 用常数 κ，其后用 Qclip）与 P1 §6 的架构原则"大胆决策，小心修正"（MPC + LNN 混合）在结构上对应，可作为 P1 混合闭环的**调度器设计参照**。
  3. **评价协议模板**：三任务 × 多基线 × 50 次测试 × 跨速度泛化矩阵（Fig. 7）× 集成规模/组件消融（Table III）——可整表借为 P1 的场景库与消融表骨架（P1 §5 要求逐场景报告，本文是逐场景 + 逐速度报告的正例）。
  4. **实车措辞范例**：作者写了"5 次试验全部成功，无碰撞、无压线"同时写"试验次数有限，不能宣称完全可部署"。这正是 P1 若做实车/回放时必须采用的**证据与措辞分离**写法。
  5. **Sim2Real 的两个具体技巧**可作 P1 的候选（若 P1 走 CARLA→真实数据回放）：域随机化（Table IV 参数范围）+ **语义去噪重映射**（把非关键类别并入背景类，PIDNet-S-Simple 7.6M 参数）。
  6. **负结果的价值**：Fig. 8/9 显示训练早期价值网络无判别力、甚至给人类动作更低的 Q 值——P1 若用价值函数做任何"OTF 先验置信度"估计，必须先报告同样的早期失效现象。
- **不可迁移 / 陷阱**：
  1. **输入模态完全不同**：状态是 45×80 语义分割图（端到端视觉）；P1 的 ODD 假设邻车状态可观测（`AGENTS.md` §1 排除词表亦把感知层专用列为 D 档）。把本文的"图像状态 → 控制"搬进 P1 会改变 P1 的问题定义。
  2. **跨 ODD**：AEB（行人横穿）属城市/人车交互场景，按分诊协议"跨 ODD（行人交互）"命中排除词表；LCO 虽含"超车"，但是两辆障碍车的极简设定，**不是多车道混行交通流**。
  3. **动作空间**：单维（刹车开度 ∈[0,1] 或转向角 ∈[−λ, λ]），没有 P1 的纵向加速度 + 横向转角联合控制，也没有编队/跟车目标。
  4. **指标无一重合**：本文用安全率、回合平均奖励、平滑度奖励、平均偏航角、停车距离；P1 的七项（跟车 RMSE、加速度平方积分、Jerk 峰值、车道居中偏差、前轮转角方差、端到端延迟、MCU 内存占用）本文一项都没有。
  5. **数字不可搬**：四张表表体缺失（§7 第 1 条），正文只有百分比；且 167% 是"400/150 − 1"的倒数比口径，不是样本量或墙钟时间的严格测量。任何引用必须标注口径。
  6. **实车不能当性能证据**：5 次试验、无实车侧基线对照、无接管率分母、无里程 → 只能当作"可行性初步证据"，与 P1 §5"实车测试：安全员、区域许可、里程与暴露量"的要求相差很远。
  7. **公平性不可核验**：文中写"所有基线都用 PER 且以 TD 误差为采样指标以确保公平"，但 Table I 的网络参数与各基线调参预算不可见（表体缺失）→ P1 §3"同等调参预算"无法从本文核验。
- **引用时必须带的限定语**：**"在 CARLA 的 AEB 与静态/动态换道超车三个任务上，以单维刹车/转向动作、45×80 语义分割图为状态、TD3/DDPG/SAC 为骨干、每法 50 次仿真测试并另有 5 次实车 LCO 试验的条件下，作者报告 QIHG-TD3 相对 Hug-TD3 的回合平均奖励提升 14.9%（静态）/15.9%（动态），实车 5/5 无碰撞无压线；该结果出自仿真为主、实车样本极小的协议，与 P1 的高速编队控制场景不同，属文献报告值，不可直接比较。"**

## 7. 缺失信息（≥3 条，写成可执行动作）

1. **需回原始 PDF 取回 Table I–IV 的表体数值**（本文全文文本提取中四张表**只有表题、无表体**：可核对 `TABLE I` 后紧接正文"Figs. 3(a) and (b)…"）。至少需要：Table I 的策略/价值网络层宽与激活、Table II 的 10 策略 × 3 任务逐项均值 ± SD、Table III 的 N=1/2/3/4 全指标、Table IV 的域随机化参数范围。（后果：本卡片 §8 的所有数字只能来自正文行文，**P1 无法核验任何逐项数值**，也无法复刻域随机化区间。）
2. **需向作者索取随机种子与重复次数明细**：文中给"每法 50 次测试""20 个测试 episode""5 次实车试验"，但**未报种子数、无置信区间、无显著性检验**（只写"以标准差为误差范围"）；Fig. 6 用的是**标准误**。（后果：无法判断 14.9%/15.9% 的增益是否超出运行间波动，P1 §4 要求的 CI 无法从本文获得。）
3. **需向作者索取实车试验的完整记录**：5 次 LCO 试验的场地、日期、里程、安全员配置、接管次数与接管率（分母写清：每公里 / 每次干预机会）、逐次轨迹与指标；以及 Fig. 11(c) 中"MSE = 0.01158"的逐点定义、对齐方式与单位。（后果：本文唯一的真车证据目前不可复现、不可比较。）
4. **需澄清 CARLA 版本、地图与交通流种子**：全文只写"CARLA simulator"，未给版本号、Town/地图、SVs 的决策模型与随机种子。（后果：直接冲突 P1 §3"同一 CARLA 地图版本与同一组交通流随机种子"的公平性要求。）
5. **需澄清 "167% 样本效率提升" 的口径与协议**：正文依据是"QIHG 三变体 150 episode 达到传统 RL 400 episode 的水平"，并称"a 167% improvement in training efficiency"；需确认分母（150 还是 400）、是否同种子、是否同一评估窗口。（后果：同一句话可算出 167% 或 62.5% 两个完全不同的数字。）
6. **需澄清 §III-C 与 §IV 对同一组数字（19.6%/16.1%）的标签冲突**：§III-C 写 "improves the optimal average reward by 19.6% … and 16.1%"，结论节写 "19.6% and 16.1% improvements in learning efficiency"（见文末 ⚠）。（后果：P1 若引用该数字，必须二选一并注明是"平均奖励"还是"学习效率"。）
7. **需确认开源仓库的可用性与许可**：正文给出 `https://github.com/wybit0304/QIHG RL`（原文链接中间有一处空格，疑为 `QIHG_RL`），未说明许可证、是否含训练配置与人类示教数据。（后果：P1 §3 若计划把 QIHG 作为对照实现，需先确认可获取性与许可。）
8. **需向作者索取 HPM 与人类干预在训练曲线中的分工说明**：HPM 训练于"100 个人类引导 episode"的数据、每 2–3 个 episode 评估一次激活条件；AEB 只在前 30 个 episode 由人类介入且不使用 HPM。（后果：Fig. 4/5 的"人引导阶段"实际混合了人类与 HPM 两种引导源，二者对最终性能的贡献不可分离。）

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

> **重要限制**：本文四张表（Table I–IV）的表体未随全文文本提取，**下表所有数字均取自正文行文**；凡只能从表中读到的逐项数值一律记为"表体缺失"。

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 样本效率提升（vs 标准 RL） | **167%**（150 episode 达到 vanilla RL 400 episode 水平） | 未报告（正文未给重复次数与区间） | Abstract；§III-C |
| 性能增益（vs 当前最优 HGRL 基线） | **14%** | 未报告 | Abstract |
| 训练期 vs Hug-TD3 的"最优平均奖励"提升 | **19.6%**（静态）／**16.1%**（动态） | 未报告 | §III-C |
| 测试期 QIHG-TD3 vs HPM（回合平均奖励） | **+21.2%**（静态） | 未报告（Table II 表体缺失） | §III-D |
| 测试期 QIHG-TD3 vs Hug-TD3（回合平均奖励） | **+14.9%**（静态）／**+15.9%**（动态） | 未报告（Table II 表体缺失） | §III-D；§IV 结论 |
| 测试期 QIHG-TD3 vs HPM（动态） | **+14.8%** | 未报告 | §III-D |
| AEB 任务成功率 | **100%** | 未报告（Table II 表体缺失） | §III-D |
| 静态 LCO 安全率 | 6 / 8 / 10 m/s 下三种 QIHG 变体均 **100%**；15 m/s 下 **>70%** | 20 个测试 episode 平均；无区间 | §III-D；Fig. 7 |
| 静态 LCO 安全率（对照） | HPM 与传统 HGRL **<50%**；纯 RL 基线 **<20%**（15 m/s 附近） | 同上 | §III-D |
| 动态 LCO 安全率 | QIHG-TD3 在 **25 m/s** 下 **75%** | 同上 | §III-D |
| 集成规模消融 | **N=3**：奖励 **0.529**、干预率 **0.131**（最优）；N=1→3 单调改善；**N=4 全面退化** | 未报告（100–120 训练 episode 平均） | §III-E；Table III |
| 价值网络评估窗口 | 前 **100** 个人类引导 episode、共 **15,000** 步 | 未报告 | §III-E；Fig. 8 |
| 测试规模（Table II） | 每个方法 **50** 次测试运行 | 以标准差为误差范围（表体缺失） | §III-D；Table II 表注 |
| 测试规模（Fig. 7 安全率） | **20** 个测试 episode × 4 档速度 × 2 场景 | 未报告 | §III-D；Fig. 7 |
| 对比策略数 | **10** 种（Table II）／**8** 种（Fig. 6、Fig. 7） | — | §III-D |
| 实车试验 | Apollo D-KIT Standard S；**5** 次 LCO 试验，**5/5** 无碰撞、无压线 | 未报告（无接管率、无里程分母） | §III-F；Fig. 11 |
| 实车与仿真轨迹一致性 | **MSE = 0.01158** | 未报告（无单位、无对齐定义） | §III-F；Fig. 11(c) |
| 感知模型规模 | PIDNet-S-Simple：**7.6 M** 参数 | 未报告 | §III-F |
| 状态空间 | 单通道语义分割图 **45 × 80**，归一化到 [0,1] | — | §II-C |
| 动作空间 | AEB：刹车开度 ∈[0, 1]；LCO：转向角 ∈[−λ, λ] | — | §II-C 式 (8)(9) |
| AEB 场景 | 自车 **60 km/h**，行人以 **1 m/s** 横穿；训练 **200** episode，人类干预前 **30** 个 episode；不使用 HPM | — | §III-B |
| 静态 LCO 场景 | 三车：两辆静止障碍车交错车道、间距 **25 m**；自车初始在首个障碍后 **15–25 m**，恒速 **5 m/s** | — | §III-B |
| 动态 LCO 场景 | 两辆障碍车 **5 m/s**、间距 **25 m**；自车初始在首个障碍后 **35 m**、**10 m/s** | — | §III-B |
| HPM | 在 100 个人类引导 episode 的示教数据上以监督学习训练；每 **2–3** 个 episode 评估一次激活条件 | — | §III-E；§III-B |
| 训练硬件 | Intel Core i9 CPU + NVIDIA RTX 3070 GPU；PyTorch | — | §III-B |
| 训练/测试阶段划分 | AEB：2 阶段（人引导 → 纯 RL）；LCO：3 阶段（人引导 → HPM 引导 → 纯 RL）；vanilla RL 基线仅 **10** episode 的 HPM 初始化 | — | §III-C；Fig. 4、Fig. 5(e) |
| 基金/许可 | 基金：郑州市重大专项 2021KJZX0060-5、NSFC 52502520；代码链接 `https://github.com/wybit0304/QIHG RL`（原文含空格） | — | 首页脚注；§III-B |

### ⚠内部不一致

- `⚠内部不一致：` **摘要写"a 14% performance gain over a state-of-the-art human-guided RL baseline"，而正文与结论写的是 14.9%（静态）/15.9%（动态）**（§III-D、§IV）。同一增益在摘要被压成单值 14%，无法判断摘要指的是哪一个任务或哪一种聚合。
- `⚠内部不一致：` **同一组数字（19.6%、16.1%）在 §III-C 被标为"optimal average reward"（最优平均奖励）的提升，在 §IV 结论被标为"learning efficiency"（学习效率）的提升**。两处标签互斥（一个是性能量、一个是效率量），文中未给出"学习效率"的定义与测量方式。
- `⚠疑似图注错位（提取异常）：` 正文第 8 页正文流中夹有一行图注残片 "Yaw angle comparison of different RL strategies. (a) Average yaw angle in the static driving task. (b) Average"（句中断开、无图号），随后第 9 页又出现 "Fig. 6. Yaw angle in the dynamic driving task. Error bars indicate standard error."。**两段图注都指向偏航角图，其中一段缺图号** → 本卡片的 {FIG-QAHG-6} 同时记录两段原文，引用前需回 PDF 确认图号归属。

