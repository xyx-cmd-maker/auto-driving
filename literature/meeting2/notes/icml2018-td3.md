# TD3 原文：Actor-Critic 中的函数逼近误差｜Addressing Function Approximation Error in Actor-Critic Methods

- **出处**：Proceedings of the 35th International Conference on Machine Learning（ICML 2018），Stockholm, Sweden，PMLR v80, 2018，全文 10 页（PDF 内未见正式起止页码）｜ **类型**：会议论文
- **作者**：Scott Fujimoto（McGill University, Montreal, Canada）et al.（Herke van Hoof, University of Amsterdam；David Meger, McGill University）
- **DOI**：PDF 内未见；ICML 2018 PMLR v80
- **全文来源**：`literature/fulltext/meeting2/addressing-function-approximation-error-in-actor-critic-meth__cd715fc9.txt`
- **分组**：决策基线（RL / 安全 RL 组）；非 TITS
- **证据等级初判**：B 级 — 7 个 MuJoCo 连续控制环境 × 6 个基线对照 + 每个组件单因素消融 + 10 个随机种子并报 ±1 SD，设计属"良好但有边界"；边界是**全部为 MuJoCo 仿真、非 P1 的 ODD、无实车、无 CI、无显著性检验**（等级判据：平台边界写进理由，不因"仿真"二字单独降级；只有单例/无对照的仿真才判 C）
- **档位建议**：A 精读 — 它是 P1 基线③（黄梦圆学位论文 TD3 直控）的算法原始出处，且是本组唯一直接给出基线算法、超参与全部对比表的文献；加权 19 ≥ 14、D1 = 2、D5 = 2，同时满足 A 档三条判据
- **五维打分**：D1=2 D2=2 D3=2 D4=1 D5=2 → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = 6+4+4+1+4 = **19**

## 1. 标题
Addressing Function Approximation Error in Actor-Critic Methods｜在 Actor-Critic 方法中处理函数逼近误差

## 2. 摘要（≤400 字中文，保留关键数字与结论成立条件）

在基于值的方法（如 deep Q-learning）中，函数逼近误差会导致值高估与次优策略。本文证明**该问题在 actor-critic 设定下同样存在**，并提出机制同时减轻其对 actor 与 critic 的影响。算法建立在 Double Q-learning 之上：**取一对 critic 的最小值**以限制高估（Clipped Double Q-learning，CDQ）；作者进一步建立**目标网络与高估偏差之间的联系**，并建议**延迟策略更新**以减少每次更新的误差。评估在 OpenAI Gym 的 7 个连续控制任务（MuJoCo，`HalfCheetah-v1`/`Hopper-v1`/`Walker2d-v1`/`Ant-v1`/`Reacher-v1`/`InvertedPendulum-v1`/`InvertedDoublePendulum-v1`）上进行，每个任务 100 万时间步、10 个随机种子、每 5000 步评估一次（每次评估 = 无探索噪声下 10 个 episode 的平均回报），与 DDPG、作者重调的 DDPG、PPO、TRPO、ACKTR、SAC 对比，Table 1 报"10 次试验的最大平均回报"，Table 2 报"最后 10 次评估的平均回报"。摘要断言"在测试的**每一个**环境中都优于当前最优"。作者自承的实验边界：**全部为 MuJoCo 仿真**，未做真车/真实系统验证；策略延迟更新之所以取 d = 2 而非更大值，是"为了公平比较、避免 actor 训练过少而损害学习"这一**权衡下的选择**，不是最优性结论。

## 3. 结论（≤350 字中文：作者结论节要点 + 关键数字 + 作者自承的局限）

结论节主张三点：(1) 高估偏差在 actor-critic 方法中同样是问题，而离散动作下常用的解法（Double DQN 式）在 actor-critic 中**无效**，作者提出的 Double Q-learning 变体限制了可能的高估；(2) 由于噪声与高估相关，作者考察了时序差分学习中误差累积，并说明**目标网络**在限制误差累积中的作用；(3) 提出 SARSA 式正则化（target policy smoothing），修改 TD 目标以对相近状态-动作对做自举。三者合起来构成 TD3，作者称其"大幅提升 DDPG 的学习速度与性能"，且"修改易于实现，可加到任何其他 actor-critic 算法上"。

关键数字（Table 1，Max Average Return over 10 trials of 1 million time steps，仅 TD3 报 ±1 SD）：HalfCheetah **9636.95 ± 859.065**（DDPG 3305.60；SAC 2347.19）、Hopper **3564.07 ± 114.74**（SAC 2996.66；TRPO 2471.30）、Walker2d **4682.82 ± 539.64**（PPO 3317.69；Our DDPG 3098.11）、Ant **4372.44 ± 1000.33**（ACKTR 1821.94）、Reacher **−3.60 ± 0.56**、InvertedPendulum **1000.00 ± 0.00**、InvertedDoublePendulum **9337.47 ± 14.96**（DDPG **9355.52**，高于 TD3）。

**作者自承的局限**：① 未做任何实车/真实系统实验（全文无实车、无硬件、无实时性指标）；② 组件消融"显著性因任务而异"，单个组件在多数情形下提升**不显著**，需组合才显著更好；③ 只在 MuJoCo 连续控制基准上验证，未在驾驶/交通场景验证；④ 论文正文未给出折扣因子 γ、replay buffer 容量、观测归一化等关键复现细节（超参表与收敛性证明放在**补充材料**，本 10 页正文不含）；⑤ 论文脚注提示 SAC 的对比数值存在争议（"See the supplementary material for hyper-parameters and a discussion on the discrepancy in the reported results of SAC"）。

## 4. 方法一句话（≤60 字）

（状态 s 与动作 a）→ 单 actor πφ + 双 critic Qθ1,Qθ2（400-300 ReLU）→ 连续动作 a = πφ(s)，用 y = r + γ·min_{i=1,2}Qθ′i(s′, πφ′(s′)+ε) 更新。

## 5. 图表清单（占位符）

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-TD3-1} | Figure 1 | "Measuring overestimation bias in the value estimates of DDPG and our proposed method, Clipped Double Q-learning (CDQ), on MuJoCo environments over 1 million time steps." | 两个子图 (a) Hopper-v1、(b) Walker2d-v1；纵轴 Average Value（0–400/500），横轴 Time steps (1e6)；四条线 CDQ / DDPG / True CDQ / True DDPG。真值由"replay buffer 采样状态出发、跟随当前策略 1000 个 episode 的平均折扣回报"估计，平均值取 **10000 个状态**。要点：DDPG 的值估计明显高于真值，CDQ 大幅压低高估 |
| {FIG-TD3-2} | Figure 2 | "Measuring overestimation bias in the value estimates of actor critic variants of Double DQN (DDQN-AC) and Double Q-learning (DQ-AC) on MuJoCo environments over 1 million time steps." | 同样 (a) Hopper-v1、(b) Walker2d-v1，1e6 步。要点：DDQN-AC 的高估与 DDPG 类似（说明 Double DQN 式解法在 actor-critic 中无效），DQ-AC 减轻但**未完全消除**高估——这是 CDQ 的必要性证据 |
| {FIG-TD3-3} | Figure 3 | "Average estimated value of a randomly selected state on Hopper-v1 without target networks, (τ = 1), and with slow-updating target networks, (τ = 0.1, 0.01), with a fixed and a learned policy." | (a) Fixed Policy（纵轴 150–350 线性）、(b) Learned Policy（纵轴 10^2–10^4 **对数**）；横轴 Time steps (1e5)。要点：固定策略下三种 τ 收敛行为相近；**策略同时学习时，τ=1（无目标网络）发散**——这是"延迟策略更新"的动机图，也说明该图两子图纵轴刻度不同，不可直接比大小 |
| {FIG-TD3-4} | Figure 4 | "Example MuJoCo environments (a) HalfCheetah-v1, (b) Hopper-v1, (c) Walker2d-v1, (d) Ant-v1." | 四个环境的渲染示意图，无数据；用于说明实验平台（MuJoCo 关节型机器人连续控制） |
| {FIG-TD3-5} | Figure 5 | "Learning curves for the OpenAI gym continuous control tasks. The shaded region represents half a standard deviation of the average evaluation over 10 trials. Some graphs are cropped to display the interesting regions." | 7 个子图 (a)–(g) 对应七个环境；曲线含 TD3、DDPG、our DDPG、PPO、TRPO、ACKTR、SAC；阴影 = **10 次试验平均评估的半标准差**（不是 1 SD，也不是 95% CI）；作者声明"部分图被裁剪以显示有趣区域"→ 纵轴不可直接跨图比较 |
| {TAB-TD3-1} | Table 1 | "Max Average Return over 10 trials of 1 million time steps. Maximum value for each task is bolded. ± corresponds to a single standard deviation over trials." | 7 环境 × 7 方法（TD3/DDPG/Our DDPG/PPO/TRPO/ACKTR/SAC）；**只有 TD3 列有 ± SD**，其余六列无任何不确定度。要点：InvertedDoublePendulum 上 DDPG(9355.52) 高于 TD3(9337.47)，与 Abstract "every environment" 冲突（见文末 ⚠） |
| {TAB-TD3-2} | Table 2 | "Average return over the last 10 evaluations over 10 trials of 1 million time steps, comparing ablation over delayed policy updates (DP), target policy smoothing (TPS), Clipped Double Q-learning (CDQ) and our architecture, hyper-parameters and exploration (AHE). Maximum value for each task is bolded." | 4 环境（HCheetah/Hopper/Walker2d/Ant）× 11 行（TD3、DDPG、AHE、AHE+DP、AHE+TPS、AHE+CDQ、TD3−DP、TD3−TPS、TD3−CDQ、DQ-AC、DDQN-AC）；全部为单值，**无 SD**。要点：单组件（AHE+某一项）多数不如组合；TD3−CDQ 在 Ant 上从 4185.06 崩到 849.75（CDQ 在 Ant 上贡献最大） |

## 6. 对 P1 的用处

- **与 P1 的关系**：**直接回答**（就"TD3 基线是什么、怎么配、怎么评"而言）。本文是 TD3 的算法原始出处，P1 基线③（学位论文 TD3 直控）在算法层面即本文 Algorithm 1。但本文的**任务与 ODD 与 P1 无关**（MuJoCo 关节机器人连续控制，非高速公路、非混行交通、非编队），因此它**只解决"基线算法与协议"这一层**，不提供任何高速混行场景证据。
- **可迁移**：
  1. **算法与超参**（§9 可整表照用）：双 critic + 单 actor、400-300 ReLU、Adam lr 1e-3、batch 100、target policy smoothing ε~N(0,0.2) clip(−0.5,0.5)、延迟 d=2、τ=0.005、每 5,000 步评估、每次评估 10 episode 无探索噪声。
  2. **消融骨架**：Table 2 的"全量 − 单组件"（TD3−DP / TD3−TPS / TD3−CDQ）+ "AHE + 单组件"双向设计，可直接映射到 P1 的 A1–A5 消融（P1 §4 要求"消融一次只改一个因素"）。注意本文的做法正是**一次只去掉/加上一个因素**。
  3. **报告纪律**：10 个随机种子 + ±1 SD + 明确写出评估频率与评估 episode 数——这是 P1 §4"种子 ≥5，报 mean ± std"可以直接对标的下限；P1 应在此基础上补齐 **CI 与显著性检验**（本文两项都缺）。
  4. **诚实的组件级结论**：作者明说单组件"causes insignificant improvement in most cases"——P1 若发现 OTF 势场增益不显著，这一段可作为"消融不显著也照报"的先例（对应 P1 红线：不显著则卖点改为可解释性 + 零额外传感器成本）。
  5. **措辞范例**：d = 2 的选择被明确写成**公平比较下的权衡**，而不是"最优超参"。P1 给基线调参时同样要写清是"同等预算下的选择"。
- **不可迁移 / 陷阱**：
  1. **v1 环境与 MuJoCo 版本**：全部结果基于 `*-v1`（Gym 早期版本）。P1 若在 CARLA/自建高速环境复现 TD3，**不能**说"按 TD3 原文设置"就跑出可比数字；环境版本差异本身足以改变量级（本文 Table 1 中 Ant 的 SD 已达 ±1000.33）。
  2. **正文缺 γ 与 buffer 容量**：直接照正文抄会写不出一份完整配置（详见 §9），必须查补充材料或代码，并注明来源。
  3. **只有 TD3 有 SD**：Table 1 中 DDPG/PPO/TRPO/ACKTR/SAC 全是单值 → **不能**用该表对"TD3 相对某基线的优势"做任何统计推断。
  4. **两个表的指标口径不同**（Table 1 = Max Average Return；Table 2 = 最后 10 次评估的平均回报），同一环境同一算法的数值不同（如 HalfCheetah TD3：9636.95 vs 9532.99）。**跨表取数即口径混用**。
  5. **无实车、无延迟/内存指标**：P1 的"端到端延迟、MCU 内存占用"两项本文完全没有，不能引本文支撑任何实时性主张。
  6. **不得把本文的 MuJoCo 数字搬进 P1**：P1 §1 红线第 4 条。任何对比必须标注"文献报告值，协议（环境、任务、步数、评估口径）不同，不可直接比较"。
- **引用时必须带的限定语**：**"TD3 原文在 7 个 MuJoCo/Gym `*-v1` 连续控制任务（每任务 1e6 步、10 个随机种子、每 5000 步评估 10 个 episode）上报告其优于 DDPG/PPO/TRPO/ACKTR/SAC，且仅对 TD3 报 ±1 SD；该结论的成立范围为仿真关节控制，非道路场景，且正文未给折扣因子与 replay buffer 容量——属文献报告值，与 P1 协议不同，不可直接比较。"**

## 7. 缺失信息（≥3 条，写成可执行动作）

1. **需取回 ICML 2018 补充材料（supplementary material）并抄出完整超参表**：正文只说"see the supplementary material for hyper-parameters"（脚注 1）与"full comparison between our re-tuned version and the baselines DDPG is provided in the supplementary material"；**折扣因子 γ、replay buffer 容量、观测归一化、网络初始化、权重衰减/梯度裁剪**均不在正文。（后果：P1 无法只凭正文写出一份可执行的 TD3 配置，§9 的"未给"项将无法闭合。）
2. **需向作者/代码仓库确认 γ 与 buffer 容量并记录来源**：请以 `https://github.com/sfujim/TD3` 的 `main.py`/`td3.py` 或补充材料为准，把"论文未印出、取自官方实现"逐项标注。（后果：若误把代码默认值写成本文报告值，等于把未印出的数字冒充文献值——违反 P1 §1 第 4 条。）
3. **需索取 10 个随机种子的列表与逐次重复结果**：Table 1 的 ±SD 只覆盖 TD3 一列，Table 2 全无 SD，Figure 5 的阴影是"半标准差"而非 95% CI。无种子列表则方差不可复算，也无法做配对检验。（后果：P1 若与 TD3 做同种子配对比较，缺少基准侧的种子信息。）
4. **需澄清 "Our DDPG" 与 DDPG 的完整差异清单**：正文只说"includes all architecture and hyper-parameter modifications to DDPG without any of our proposed adjustments"，具体改了哪些项只在补充材料。（后果：P1 若把 "Our DDPG" 当作"同等调参预算下的 DDPG"，必须知道差异清单，否则违反 P1 §3 公平性要求。）
5. **需核验 SAC 对比数值的争议**：正文脚注明确提示 SAC 报告结果存在 discrepancy，并把讨论放补充材料。（后果：Table 1 的 SAC 列不可作为"TD3 优于 SAC"的证据。）
6. **需与正式出版版（PMLR v80）逐字比对全文**：本卡片依据 PDF 提取的纯文本（10 页，MD5 `cd715fc9d10492069c85d96978350553`），公式换行与表格排版在纯文本中有损（如 Table 1/2 的行列关系由文字顺序重建）。（后果：Table 1/2 的行列对应关系需人工回原 PDF 复核后再入库。）
7. **需确认本文相对 arXiv 版（1802.09477）是否有改动**，尤其是 Abstract 的 "every environment" 措辞与 Table 1 的 InvDoublePendulum 行。（后果：P1 引用的是 ICML 正式版，若两版措辞不同需按正式版。）

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

### 8.1 协议类数字（正文 §6.1 / §6.2 / 图注）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 网络结构 | actor 与 critic 均为两层前馈，隐层 400、300；层间 ReLU；actor 输出端加 tanh | 未报告 | §6.1 Evaluation |
| critic 输入 | 状态与动作**同时进入第一层**（与原始 DDPG 不同） | 未报告 | §6.1 |
| 优化器 / 学习率 | Adam，学习率 10^−3（两者同） | 未报告 | §6.1 |
| mini-batch 大小 | 100 条 transition，从"包含 agent 全部历史"的 replay buffer 均匀采样 | 未报告 | §6.1 |
| replay buffer 容量 | **未给出数值**（仅"the entire history of the agent"） | — | §6.1 |
| 探索：预热 | 前 10000 步纯探索（HalfCheetah-v1、Ant-v1）；其余环境前 1000 步纯探索 | 未报告 | §6.1 |
| 探索：行为策略噪声 σ | 每个动作加高斯噪声 N(0, **0.1**)；使用**不相关噪声**（不用 Ornstein–Uhlenbeck） | 未报告 | §6.1 |
| target policy smoothing：σ̃ | ε ∼ N(0, **0.2**) | 未报告 | §6.1；式(14)；Algorithm 1 |
| target policy smoothing：裁剪 c | 裁剪到 (**−0.5, 0.5**) | 未报告 | §6.1；式(14)；Algorithm 1 |
| 策略延迟 d | **d = 2**（每 2 次 critic 更新才更新 actor 与目标网络） | 未报告 | §6.1；Algorithm 1 |
| 目标网络更新 τ | **τ = 0.005**（两个目标网络同） | 未报告 | §6.1；Algorithm 1 |
| 折扣因子 γ | **正文未给出数值**（仅在 Background 中定义 γ 为折扣因子） | — | §3 Background（无数值） |
| 每任务总步数 | **1,000,000**（1e6）时间步 | 未报告 | §6.1；Table 1 表注；Table 2 表注 |
| 评估频率 | 每 **5000** 时间步评估一次 | 未报告 | §6.1 |
| 单次评估协议 | 无探索噪声下 **10 个 episode** 的平均回报 | 未报告 | §6.1 |
| 重复次数 / 种子 | **10 个随机种子**（Gym 模拟器与网络初始化） | 10 trials | §6.1；Table 1 表注；Table 2 表注 |
| Figure 5 阴影含义 | "half a standard deviation of the average evaluation over 10 trials" | 半 SD（非 CI） | Figure 5 图注 |
| 估计真值的方法（Fig.1/2） | 从 replay buffer 采样状态出发、跟随当前策略 **1000 个 episode** 的平均折扣回报；值曲线取 **10000 个状态**的平均 | 未报告 | §4.1 |

### 8.2 Table 1（Max Average Return over 10 trials of 1 million time steps；仅 TD3 列有 ±SD）

| Environment | TD3 | DDPG | Our DDPG | PPO | TRPO | ACKTR | SAC |
|---|---|---|---|---|---|---|---|
| HalfCheetah | **9636.95 ± 859.065** | 3305.60 | 8577.29 | 1795.43 | -15.57 | 1450.46 | 2347.19 |
| Hopper | **3564.07 ± 114.74** | 2020.46 | 1860.02 | 2164.70 | 2471.30 | 2428.39 | 2996.66 |
| Walker2d | **4682.82 ± 539.64** | 1843.85 | 3098.11 | 3317.69 | 2321.47 | 1216.70 | 1283.67 |
| Ant | **4372.44 ± 1000.33** | 1005.30 | 888.77 | 1083.20 | -75.85 | 1821.94 | 655.35 |
| Reacher | **-3.60 ± 0.56** | -6.51 | -4.01 | -6.18 | -111.43 | -4.26 | -4.44 |
| InvPendulum | **1000.00 ± 0.00** | 1000.00 | 1000.00 | 1000.00 | 985.40 | 1000.00 | 1000.00 |
| InvDoublePendulum | 9337.47 ± 14.96 | **9355.52** | 8369.95 | 8977.94 | 205.85 | 9081.92 | 8487.15 |

> 注：表注写"Maximum value for each task is bolded"。**InvDoublePendulum 行的最大值按数值应为 DDPG 的 9355.52**（本表按数值标粗，原文粗体排版未能从纯文本读取，需回 PDF 复核）。其余六行按数值最大者为 TD3。

### 8.3 Table 2（Average return over the last 10 evaluations over 10 trials of 1 million time steps；**全部无 SD**）

| Method | HCheetah | Hopper | Walker2d | Ant |
|---|---|---|---|---|
| TD3 | **9532.99** | **3304.75** | 4565.24 | **4185.06** |
| DDPG | 3162.50 | 1731.94 | 1520.90 | 816.35 |
| AHE | 8401.02 | 1061.77 | 2362.13 | 564.07 |
| AHE + DP | 7588.64 | 1465.11 | 2459.53 | 896.13 |
| AHE + TPS | 9023.40 | 907.56 | 2961.36 | 872.17 |
| AHE + CDQ | 6470.20 | 1134.14 | 3979.21 | 3818.71 |
| TD3 - DP | 9590.65 | 2407.42 | **4695.50** | 3754.26 |
| TD3 - TPS | 8987.69 | 2392.59 | 4033.67 | 4155.24 |
| TD3 - CDQ | 9792.80 | 1837.32 | 2579.39 | 849.75 |
| DQ-AC | 9433.87 | 1773.71 | 3100.45 | 2445.97 |
| DDQN-AC | 10306.90 | 2155.75 | 3116.81 | 1092.18 |

> 注：粗体为"该列最大值"，本表按数值判定（原文粗体排版未能从纯文本读取，需回 PDF 复核）。**HCheetah 列最大值为 DDQN-AC 10306.90，Walker2d 列为 TD3−DP 4695.50** ——即"完整 TD3"并未在每一列都最大；正文亦只写"outperforms every other combination in **most** tasks"。

### 8.4 正文印出的其它数字

| 指标 | 值 | 不确定度 | 出处 |
|---|---|---|---|
| 评估覆盖的环境数 | 7 个连续控制域（OpenAI Gym / MuJoCo） | — | Abstract；§1；§6.1 |
| 对比算法数 | 6 个（DDPG、Our DDPG、PPO、TRPO、ACKTR、SAC） | — | §6.1；Table 1 |
| 消融变体数 | 11 行（含 DQ-AC / DDQN-AC 两个 Double Q 变体） | — | Table 2 |
| 收敛性/偏差的形式化结果 | CDQ 在有限 MDP 下的收敛性证明 | — | §4.2 正文声明，证明在补充材料（**本正文无**） |
| 代码 | https://github.com/sfujim/TD3（论文正文给出；含学习曲线） | — | §1 |

### 8.5 ⚠ 内部不一致与口径警示

- `⚠内部不一致：` Abstract 声称 "outperforming the state of the art in **every** environment tested"，但 Table 1 的 InvDoublePendulum 行中 DDPG = 9355.52 **高于** TD3 = 9337.47（且 SD 仅 14.96，两者差距 18.05 已超出 1 SD）；§6.1 的措辞较软（"TD3 **matches or** outperforms all other algorithms"）。→ 引用时用 §6.1 的"match or outperform"，不要用 Abstract 的"every environment"。
- `⚠口径警示（非矛盾）：` Table 1（Max Average Return）与 Table 2（Average return over the last 10 evaluations）**指标不同**，同一算法同一环境的数值不同（HalfCheetah TD3：9636.95 vs 9532.99；Hopper：3564.07 vs 3304.75）。→ 跨表取数即口径混用。
- `⚠口径警示：` Figure 5 的阴影是"**half** a standard deviation"，Table 1 的 ± 是"**a single** standard deviation over trials"；同一论文两种不确定度口径，引用时不得互称。
- `⚠外部争议（论文自承）：` SAC 一列的数值存在"discrepancy"，作者把讨论放补充材料，本正文未解决。

---

## 9. TD3 复现清单（给 P1 用）

> **口径声明（P1 §1 红线第 3 条）**：本清单数字**全部来自 TD3 原文正文 §6.1、Algorithm 1、Table 1/2 图注**，凡"未给"处一律标出，**不得**用官方代码默认值冒充实文报告值。P1 引用 TD3 基线时**必须二选一并写明**：①「按论文/学位论文实现原样引用（文献报告值）」或②「我们复现（附本清单 + 差异清单）」。**在 P1 未重训之前，只能写"文献报告值"**；即使重训，也必须写清与原文的差异（尤其 γ、buffer 容量、观测归一化、评估口径）。

### 9.1 算法结构（Algorithm 1 逐条，原文步骤）

| # | Algorithm 1 步骤（原文表述的忠实转写） | 对应公式/说明 |
|---|---|---|
| 1 | Initialize critic networks Qθ1, Qθ2, and actor network πφ with random parameters θ1, θ2, φ | 单 actor + 双 critic |
| 2 | Initialize target networks θ′1 ← θ1, θ′2 ← θ2, φ′ ← φ | 三个目标网络 |
| 3 | Initialize replay buffer B | 容量未给 |
| 4 | for t = 1 to T do | T = 1e6（§6.1） |
| 5 | Select action with exploration noise a ∼ π(s) + ε, ε ∼ N(0, σ) and observe reward r and new state s′ | 行为策略噪声 σ = **0.1**（§6.1） |
| 6 | Store transition tuple (s, a, r, s′) in B | — |
| 7 | Sample mini-batch of N transitions (s, a, r, s′) from B | N = **100**，均匀采样 |
| 8 | ã ← πφ′(s) + ε, ε ∼ clip(N(0, σ̃), −c, c) | σ̃ = **0.2**，c = **0.5** |
| 9 | y ← r + γ min_{i=1,2} Qθ′i(s′, ã) | γ **正文未给** |
| 10 | Update critics θi ← min_θi N^−1 Σ (y − Qθi(s, a))² | 两个 critic 用**同一个目标 y** |
| 11 | if t mod d then | d = **2** |
| 12 | Update φ by the deterministic policy gradient: ∇φJ(φ) = N^−1 Σ ∇a Qθ1(s,a)|_{a=πφ(s)} ∇φ πφ(s) | **只用 Qθ1** |
| 13 | Update target networks: θ′i ← τθi + (1 − τ)θ′i；φ′ ← τφ + (1 − τ)φ′ | τ = **0.005**，每个时间步更新 |
| 14 | end if / end for | — |

> 补充：Twin critics 的**实现简化**在 §4.2 明确写出——"computational costs can be reduced by using a single actor optimized with respect to Qθ1. We then use the same target y2 = y1 for Qθ2."（即 y2 = y1，不是各自的 min）。这一点常被复现者写错，**必须在差异清单里对齐**。

### 9.2 超参数一览（论文位置逐项标注）

| 项 | 值 | 论文位置 | 备注 |
|---|---|---|---|
| actor 层宽/激活 | 两层前馈 400、300；层间 ReLU；输出 tanh | §6.1（正文） | 与 critic 同 |
| critic 层宽/激活 | 两层前馈 400、300；层间 ReLU；**状态与动作拼在第一层输入** | §6.1（正文） | 与原始 DDPG 不同（原文明确） |
| 优化器 | Adam | §6.1（正文） | — |
| 学习率 | 10^−3（actor 与 critic 同） | §6.1（正文） | 未提学习率衰减 |
| batch size | 100 | §6.1（正文） | — |
| replay buffer 大小 | **未给数值**（"containing the entire history of the agent"） | §6.1（正文） | **复现必补**：官方实现为 1e6，但论文未印出，须标注来源 |
| 探索噪声 σ（行为策略） | 高斯 N(0, 0.1)，逐动作加；不使用 OU 噪声 | §6.1（正文） | 作者称 OU 无收益 |
| 预热（纯探索）步数 | 10000 步（HalfCheetah-v1、Ant-v1）；1000 步（其余 5 个环境） | §6.1（正文） | 环境相关 |
| target policy smoothing σ̃ | N(0, 0.2) | §6.1（正文）+ 式(14) + Alg.1 | — |
| target policy smoothing 裁剪 c | (−0.5, 0.5) | §6.1（正文）+ 式(14) + Alg.1 | — |
| 策略延迟 d | 2 | §6.1（正文）+ Alg.1 | 作者称更大 d 对误差累积更好，但为公平比较取 2 |
| 目标网络 τ | 0.005（θ′1、θ′2、φ′ 同） | §6.1（正文）+ Alg.1 | — |
| 折扣 γ | **未给** | 全文正文无 | **复现必补**（须查补充材料/代码，标注来源） |
| 每环境总步数 | 1e6 | §6.1 + Table 1/2 表注 | — |
| 评估频率 | 每 5000 步 | §6.1（正文） | — |
| 单次评估 | 10 个 episode，无探索噪声 | §6.1（正文） | — |
| 种子数 | 10（Gym 模拟器 + 网络初始化） | §6.1 + 表注 | **未给种子列表** |
| 环境版本 | `HalfCheetah-v1`、`Hopper-v1`、`Walker2d-v1`、`Ant-v1`、`Reacher-v1`、`InvertedPendulum-v1`、`InvertedDoublePendulum-v1` | Fig.4/Fig.5 图注 + §6.1 | "original set of tasks from Brockman et al. (2016) with no modifications to the environment or reward" |
| 参考实现 | https://github.com/sfujim/TD3 | §1（正文） | 许可未在本文说明 |
| 补充材料内容 | 超参表、SAC 差异讨论、收敛性证明、完整 DDPG 对比 | §1 脚注 1、§4.2、§6.1 | **本 10 页正文不含** |

### 9.3 评估协议（可对齐 P1 §4 的部分）

| 项 | TD3 原文 | P1 要求的差异 |
|---|---|---|
| 重复 | 10 seeds，报 ±1 SD（**仅 TD3 列**） | P1 §4 要求种子 ≥5、mean ± std **或 95% CI**；P1 应补 CI 与显著性检验 |
| 评估口径 | 每 5000 步、10 episode、无探索噪声；Table 1 取"10 次试验的最大平均回报"，Table 2 取"最后 10 次评估的平均回报" | P1 须**先固定口径再报数**，并写明是"最大"还是"最后 N 次" |
| 不确定度 | Table 1 ±1 SD；Figure 5 半 SD；Table 2 无 | P1 须统一为一种口径并注明 |
| 失败/长尾 | 未报成功率、未报失败分类 | P1 §5 要求逐场景报告 + 失败分类；小样本用 Wilson/Clopper-Pearson |
| 资源指标 | 无（无延迟、无内存、无硬件） | P1 的"端到端延迟、MCU 内存占用"必须自采，注明平台与档位 |

### 9.4 P1 引用 TD3 基线的强制标注

- 若**未重训**：写 **「TD3 基线按 Fujimoto et al. (ICML 2018) 的算法与其报告的超参数实现；性能数字为学位论文实现结果 / 文献报告值，未经本项目复现，协议不同，不可直接比较」**。禁止写成"我们复现"。
- 若**重训**：必须附差异清单，至少覆盖：γ 取值与来源、replay buffer 容量与来源、观测/动作归一化、环境与版本（CARLA 版本 vs MuJoCo v1）、每任务步数与评估频率、种子列表、硬件与训练时长。

### 9.5 复现所需但**论文未给**的信息（逐条）

1. **折扣因子 γ 的数值**（正文仅定义符号）。
2. **replay buffer 容量**（只有"entire history"这一描述）。
3. **10 个随机种子的具体取值**与逐次重复的返回值（Table 1 只给 TD3 的 ±SD）。
4. **观测归一化/状态缩放**是否存在（P1 的车辆状态量纲差异极大，这一项影响显著）。
5. **网络初始化方案**（正文只写 "random parameters"）。
6. **权重衰减、梯度裁剪、目标网络的初始同步方式**（正文未提）。
7. **"Our DDPG" 的完整修改清单**（只在补充材料）。
8. **CDQ 收敛性证明的前提与结论**（在补充材料；正文只给直觉）。
9. **各基线的超参数与调参预算**（PPO/TRPO/ACKTR 取自 OpenAI baselines，SAC 取自作者 GitHub，本文未给逐项超参）→ 这正是 P1 §3"同等调参预算"无法从本文核验的原因。
10. **训练硬件与墙钟时间**（全文无硬件）→ P1 无法据此估算基线训练成本。
11. **Table 1/2 的原始行列排版**（纯文本重建，需回 PDF 复核后再入库）。
