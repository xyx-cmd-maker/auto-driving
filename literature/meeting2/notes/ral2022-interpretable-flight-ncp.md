# 可解释自主飞行（紧凑可可视化神经回路策略）｜Interpretable Autonomous Flight Via Compact Visualizable Neural Circuit Policies

- **出处**：IEEE Robotics and Automation Letters, vol. 7, no. 2, April 2022, pp. 3265–3272 ｜ **类型**：期刊论文（Letter）
- **作者**：Paul Tylkin et al.（Tylkin P, Wang T-H, Palko K, Allen R, Siu HC, Wrafter D, Seyde T, Amini A, Rus D；MIT CSAIL / USAF AI Accelerator / MIT Lincoln Laboratory）
- **DOI**：10.1109/LRA.2022.3146555（PDF 第 1 页印出；Crossref 核验 2026-10-03 通过：RA-L 7(2):3265–3272，2022-04，被引 16）
- **全文来源**：`literature/fulltext/meeting2/interpretable-autonomous-flight-via-compact-visualizable-neu__ba0519f5.txt`（PAGES=8, CHARS=42,279）
- **分组**：连续时间 / 流体神经网络
- **证据等级初判**：B 级 — 顶刊正式版全文可得；**有真实硬件（Raspberry Pi Zero / Jetson Nano / DJI Tello / NXP RRDRONE-FMUK66）上的实时推理实测**，这是本组五篇中唯一同时具备"同源 LNN 家族 + 实机 + 内存/帧率数字"的一篇；但性能对比只有图（无数字、无统计检验），且**未报告参数量**、**Table I–III 的正文在本 .txt 中缺失**。**【确定】**
- **档位建议**：A 精读 — P1 可解释性论证与"参数量可上 MCU / 端到端延迟可测"两条主张的**唯一直接证据来源**（NCP 与 CfC/LTC 同出 Rus 组，且本文把模型压到 200 KB 级并跑在 <10 g 的单板机上）。**【确定】**
- **五维打分**：D1=5 D2=3 D3=5 D4=3 D5=4 → 加权 = 3·5+2·3+2·5+1·3+2·4 = 15+6+10+3+8 = **42**

## 1. 标题
Interpretable Autonomous Flight Via Compact Visualizable Neural Circuit Policies｜通过紧凑可可视化神经回路策略实现可解释自主飞行

## 2. 摘要（≤400 字中文）
作者用 **NCP（Neural Circuit Policy，源自线虫 C. elegans 的四层稀疏网络：感觉—中间—指令—运动神经元）** 学习端到端可解释控制器，完成两个飞行域任务：**Canyon Run**（固定翼穿越未知峡谷、命中随机高度的航路点、避免撞地与飞出峡谷）与 **Drone Dodgeball**（四旋翼在 100 m × 30 m × 100 m 边界内保持站位、同时躲避对手连续发射的球）。NCP 的神经元数极少（**9 至 24 个**），因此可**在神经元层面直接解读**：作者通过固定输入、扫掠关键环境变量，把归一化激活映射成热图（Fig. 6/7），再蒸馏成**人类可读决策树**（Fig. 5），从而在部署前就能审问策略"为什么这样决策"。控制器：**PPO** 训练，每个域训练 **1,200 万时间步**，每个模型在测试时评估 **100 个 episode**；作者称在更复杂的 Canyon Run 中 NCP 相对同类前馈/递归网络表现更好，在较简单的 Drone Dodgeball 中性能**相当**。硬件迁移：把仿真训练的策略导出为 **TensorFlow Lite（约 170 KB）+ 观测预处理器（约 10 KB）**，在**电池供电的 Raspberry Pi Zero** 上实时推理、控制 **DJI Tello**；早期飞行测试 **10 FPS**，后续飞行软件改进后 **>30 FPS**；另一套更大平台（**NXP RRDRONE-FMUK66 + PX4 + Jetson Nano + Intel RealSense d435i**）因电池与机动性限制，**全部低速、地面系留**测试。作者自承：NCP 与"可解释设计"是否真比黑箱做出更好决策仍是开放问题。

## 3. 结论（≤350 字中文）
作者结论：NCP 能在两个复杂度递增的域中学到可解释控制，**学到的神经元激活直接对应环境关键特征**；与"可解释性与性能二选一"的 DNN 不同，NCP 允许**同时**高性能与可解释。已把 Drone Dodgeball 策略部署到真实飞行硬件上做推理，并认为这类模型将有益于安全 AI 部署与人机协同。关键数字：**200 KB 内存**（Abstract）／**TFLite ≈170 KB + 预处理器 ≈10 KB**（正文 §VII-C）；**10 FPS → >30 FPS**；NCP 神经元规模 **9–24**（正文另称鲁棒性检查覆盖 9–40 个神经元：4/2/3 → 16/12/12）。**作者自承的局限**：① "NCP 与可解释设计是否比黑箱模型做出更好决策，仍是开放问题"；② "把决策树提取算法推广到任意环境"留作未来工作；③ Raspberry Pi Zero 全机载部署（用无人机电池供电、飞行中推理）**尚未完成**，只测了静态位置供电推理；④ 未给出任何性能数值/成功率/接管率；⑤ 更大的 NXP 平台**仅低速地面系留**测试。**⚠** 结论节写"there is a tradeoff between interpretability and performance"不适用于 NCP，与 Results 的"Drone Dodgeball 中 NCP 与其它架构**性能相当（comparable）**"存在措辞张力。

## 4. 方法一句话
射线传感器（21×101 + 19×33 网格）+ 车辆状态向量 → 固定 CNN/MLP 前端 + **9–24 神经元的 NCP（LTC 神经元 ODE）**，PPO 端到端训练 → 多离散动作（每轴 ∈{−1,0,1}），神经元激活可视化/决策树审问。

## 5. 图表清单（占位符）
全文共 **10 个 Figure + 3 个 Table**（合计 13 个，全部收录）。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-NCPFLY-1} | Fig. 1 | Neural Circuit Policies allow for end-to-end learning (from perception to control) with a small number of neurons, which leads to policies that can be interpreted at the neuron level and safely deployed on real hardware. | 全文总纲图：感知→NCP→控制；**"safely deployed on real hardware" 是本文相对 CfC 的增量**（CfC 只有建议句）。 |
| {FIG-NCPFLY-2} | Fig. 2 | The two environments, Canyon Run and Drone Dodgeball, for which we study learning interpretable policies are depicted above. … The NCPs have three layers of neurons: inter, command, and motor neurons, and output actions. | 两个任务的奖励结构与 NCP 三层结构（inter/command/motor）；注意图注写"three layers"，而正文 §III-A 写 NCP 是**四层**（含 sensory）——图注把 sensory 视作输入前端。 |
| {FIG-NCPFLY-3} | Fig. 3 | The agent receives visual input from two depth sensors along with vector-valued state information. The inputs are processed by Convolutional Neural Networks (CNNs) and a Multi-layer Perceptron (MLP), respectively. The resulting latent features are passed to the behavioral model, represented here as a Neural Circuit Policy (NCP) … | 完整数据流；**P1 若要申报"参数量是否含感知头"，本图界定了"感知头 = 两个 CNN + 一个 MLP，单独存在、单独计参"**。 |
| {TAB-NCPFLY-1} | Table I | 未见图注 | ⚠ **表正文与图注在本 .txt 中均缺失**（PDF 文本层只提取到标题"NEURAL NETWORKS FOR EACH ENVIRONMENT"）。从正文推断为 4 种网络（NCP / small LSTM / large LSTM / large MLP）× 2 环境的配置。**在取得表正文前，不得引用其中任何行。** |
| {TAB-NCPFLY-2} | Table II | 未见图注 | ⚠ 同上（标题"TRAINING SETTINGS"）。正文提到"4 网络 × 2 环境 × 3 控制自由度"共 24 组设置，推断本表给训练超参。**不得引用其中任何行。** |
| {FIG-NCPFLY-4} | Fig. 4 | Training and test results, comparing NCPs, small LSTMs, large LSTMs, and large MLPs. All of the models were trained for 12 million time steps. The average episode length in Canyon Run is much longer than in Drone Dodgeball … we truncated episodes in that environment at 5,000 time steps during testing, so reward in a given episode could never exceed 25 in 1 DoF and 2 DoF (throttle fixed at 50%), and 36 in Full DoF … | **本文唯一的性能对比图，全部以曲线/柱形给出，正文未印任何数值**。测试上限（25/36 奖励）说明 Canyon Run 的奖励被截断，跨环境比较不可行；**P1 无法从本文取任何控制器性能数字**。 |
| {FIG-NCPFLY-5} | Fig. 5 | Neuron activations and example decision trees for 9-neuron NCP models trained in 1 DoF variants of Canyon Run (left) and Drone Dodgeball (right). Individual neurons have learned to respond to key features in the environments such as the direction to the next waypoint (left) and presence of obstacles (right). … | **P1 可解释性论证的核心图**：单神经元激活 → 决策树 → 自然语言解释。9 神经元是全文最小配置。 |
| {FIG-NCPFLY-6} | Fig. 6 | Heat maps of neuron activations in the 14-neuron NCP model trained in the 2 DoF variant of Drone Dodgeball. Heat maps are generated for each neuron by placing waypoints (stimulus) at different locations on a 2D grid and recording the induced activation (left box). … Starting from nondescript activity patterns in the untrained NCP model (middle), we observe consistent specialization of individual neurons to specific half-spaces in the trained NCP model (right). | 14 神经元模型：C1/C2 指令神经元对应航路点 X/Y，M0/M1/M3/M5 运动神经元分工；**"训练前无结构 → 训练后半空间特化"的对照是本文最像"可解释性证据"的部分**。 |
| {FIG-NCPFLY-7} | Fig. 7 | Neuron activations in the 24-neuron NCP models in Full DoF Drone Dodgeball. Top row: example neural responses of two command neurons to varying the waypoint position across a 3D grid. Bottom row: corresponding neuron activations along a trajectory approaching a waypoint located at the origin (red star). | 24 神经元、Full DoF、3D 网格；指令神经元 #0 对正 x 半空间特化、#2 互补。**规模谱系 9 / 14 / 24 三档在此补齐**。 |
| {TAB-NCPFLY-3} | Table III | 未见图注 | ⚠ **表正文与图注在本 .txt 中均缺失**（标题"DRONE HARDWARE SETTINGS"）。正文称其给出 Raspberry Pi Zero + DJI Tello 与 NXP + Jetson Nano + RealSense 两套平台配置。**表内平台细节（CPU 型号、主频、内存容量）在取得前不得引用。** |
| {FIG-NCPFLY-8} | Fig. 8 | Normalized neuron activations for simulated (dashed) and real-world (solid) 1 DoF Drone Dodgeball as a function of perceived ball radius in pixel space. The neurons exhibit similar patterns of activation, consistent with the expected dodging behavior in response to an oncoming obstacle. | **唯一的仿真—实机一致性证据**：除 M2 神经元外全部随感知球半径增大而激活增强；峰值由仿真的 ~9 px 移到实机的 ~7 px（作者归因于深度尺度转换与视场差异 90°×90° vs 86°×57°）。 |
| {FIG-NCPFLY-9} | Fig. 9 | The larger drone hardware setup for deploying the NCP policies from the Drone Dodgeball simulation environment on physical flight hardware. The quadcopter, which uses an Intel RealSense camera for visual input and a Jetson Nano for processing and inference, is shown on the left. … The middle image shows the model staying at the waypoint when no obstacle is in view. The right image shows the model lowering its thrust in response to an oncoming obstacle. | 大平台实机；**注意：该平台全部测试为低速、地面系留**，且图中"彩色数字代表 NCP 动作输出"——这是把网络输出直接印在感知图上的可解释性展示方式，P1 可直接借鉴为答辩/论文插图。 |
| {FIG-NCPFLY-10} | Fig. 10 | The DJI Tello drone experimental setup for deploying the NCP policies from the Drone Dodgeball simulation environment on physical flight hardware. Inference is done on a battery-powered Raspberry Pi Zero (not shown). The left image shows the experimental setup, in which a ball is moved into the visual field of the drone … | 小平台实机；**推理在 Pi Zero 上、相机图像经颜色掩膜/缩放/灰度化后送入 NCP**——注意这套预处理（颜色掩膜）是**任务特定的手工流水线**，P1 不能假设可迁移。 |

**（无 >13 项的情形；全文 10 图 3 表已全部覆盖，其中 3 张表正文缺失已逐条标注。）**

## 6. 对 P1 的用处

- **与 P1 的关系**：**直接回答（可解释性 + 可上车）**，但**不同 ODD、不同任务**。本文给出的是"**同源 LNN 家族（NCP/LTC）在真实硬件上以 KB 级内存实时推理**"的唯一实证；对 P1 的价值集中在两条主张上——① 可解释性论证的**已发表模板**；② "参数量可上 MCU / 端到端延迟可测"的**对照基准与报告口径**。它不提供任何车辆、编队、跟驰或 ODD 相关内容。

- **可迁移**：
  1. **★ P1 可直接引用的"LNN 家族上真实硬件"唯一硬数字**：Abstract 逐字 —— "*deploying a small NCP (**200 KB of memory**) capable of real-time inference on a **Raspberry Pi Zero** controlling a **DJI Tello** drone*"；正文 §VII-C 逐字 —— "*built a TensorFlow Lite model (**∼170 KB**) and associated observation preprocessor (**∼10 KB**) for deployment*"。→ **这是本项目"<500 KB"红线之外的合法替代锚点**：① 200 KB 是**整模型部署产物**（TFLite 序列化）而非 fp32 参数字节数，口径与 CfC 的 230,828 参数**不可直接换算**；② 170 + 10 = 180 KB ≠ 200 KB，**作者未解释差额**（可能含 TFLite 运行时/量化误差/四舍五入）。引用时须写"**论文报告值，口径为 TFLite 模型文件大小**"。
  2. **"参数量 vs 内存占用量纲"的第二个参照系**：本文正文 §II 写 NCP "requiring **tens or hundreds of parameters** and **kilobytes or megabytes of memory**"，而 CfC 的 RNN 分量是 4,184 参数。两者相差 1–2 个数量级 → **P1 在写"可上 MCU"时必须写明是"参数量"还是"部署产物字节数"**，本文正是把两者混用（200 KB 是字节数，不是参数数）的典型例子，可作为反面教材引用。
  3. **神经元级可解释性的可复现做法（P1 的可解释性论证可直接照搬结构）**：① 固定输入、**扫掠单一环境变量**（航路点位置 / 障碍物半径），记录**每个神经元的归一化激活**（Fig. 6/7 的热图）；② 与**未训练网络**的激活剖面对照（Fig. 6 中列 vs 右列）；③ 把激活模式**蒸馏成决策树 + 自然语言说明**（Fig. 5）；④ **不需跑真实轨迹**即可完成上述三步（正文："even without needing to evaluate the network over a real trajectory"）。→ P1 的 OTF 势场恰好是一个可扫掠的标量，**这套"扫掠标量 → 单神经元激活热图 → 决策树"的流水线可几乎原样移植**，且天然回避 CARLA 闭环算力成本。
  4. **仿真—实机一致性的报告方式（Fig. 8）**：把"仿真激活曲线"与"实机激活曲线"叠在同一坐标轴上，并**主动解释两者峰位差异的物理原因**（深度尺度 Unity vs 米、视场 90°×90° vs 86°×57°）。→ P1 若做 CARLA 与实车数据回放的 sim-to-real 对比（`AGENTS.md` §5 要求"须量化或至少定性说明"），这是可直接照抄的图表范式。
  5. **实时性的报告口径**：同时给"早期 10 FPS → 改进后 >30 FPS"的**版本化帧率**，并说明改进来自**飞行软件的视频流处理**而非模型。→ P1 的"端到端延迟"指标应同样区分**模型推理延迟**与**系统/管线延迟**，并记录改进来源（本文是反面提醒：10→30 FPS 的 3 倍提升与模型无关）。
  6. **可引用的负面对照（对 P1 的公平性论证有用）**：作者做鲁棒性检查时"**把网络加深、放大到 10 倍，未发现显著性能差异**"（Results），且"评估 5 种不同深度的 CNN 配置，未发现显著差异"（脚注 3）。→ 支持 P1 的 A2 消融**按参数量对齐**而非按"越大越好"设计，并可作为"小模型不吃亏"的旁证（**注意：作者写的是 "no significant difference"，未做任何检验，"significant" 是口语用法**）。

- **不可迁移 / 陷阱**：
  1. **无任何控制性能数字**：Fig. 4 只有曲线；正文未印任何 reward / 成功率 / RMSE / 跟踪误差。唯一印出的数字是**随机动作基线**（Drone Dodgeball 平均奖励 1 DoF 64 / 2 DoF 12 / Full DoF 3；Canyon Run <1）。→ **P1 不能从本文取任何控制器性能对标值。**
  2. **ODD 完全不同**：无人机、峡谷/室内躲避球、无车道、无交通参与者、无编队。本文结论**不可外推到高速公路多车道混行**。
  3. **"实时"的含义与 P1 的 100 Hz 差一个量级**：本文 >30 FPS，P1 目标 100 Hz（10 ms）。**不得把本文的 "real-time inference" 当作 P1 实时性的证据**。
  4. **任务特定的手工感知流水线**：实机部署时用**颜色掩膜（对应障碍物色相）**提取障碍物、再由 altimeter 设定航路点（起飞高度 ~1 m）。这是"被简化到可控"的实机演示，**不是通用感知**；P1 的高速感知不可类比。
  5. **训练规模与预算**：每域 **1,200 万时间步**、PPO、RLLib；本文**未报告任何训练墙钟时间、GPU 型号或能耗**。P1 若引用"训练成本"须自行实测。
  6. **Table I–III 正文缺失** → 本文的"4 种网络配置"、"24 组训练设置"、"两套硬件平台细节"**均不可引用具体数值**。
  7. **"可比/更好"无统计**：Results 只说 NCP 在 Canyon Run "tended to demonstrate relatively higher performance"，Drone Dodgeball "comparable"；**无 p 值、无 CI、无重复运行的方差报告**（每模型 100 episode 但只有"最佳训练运行"，正文："the evaluation of the **best** training run of each model architecture"）。→ 这是**选择性报告**（best run），引用时必须写明。

- **与 CfC（NMI 2022）的关系**：**同源、互补，且本文补上了 CfC 最缺的那块证据。**
  - 同源：作者明确致谢 —— "*we would like to thank **R. Hasani** for an introduction and initial discussions about Neural Circuit Policies*"；引用 [1] Lechner/Hasani 的 NCP（NMI 2020）、[2] Hasani 的 ordinary neural circuits（ICML 2020）、[3] **Hasani 等 *Liquid time-constant networks*（AAAI 2021）**——即 CfC（NMI 2022）的理论前身。神经元动力学："*Each neuron has state dynamics governed by an **ODE** [3] … referred to as **Liquid Time Constant (LTC)** neurons*"，并用 "[3, Algorithm 1] 的欧拉法变体"求解。
  - 互补方向（**本组最重要的对照**）：
    | 维度 | CfC (NMI 2022) | 本文 (RA-L 2022) |
    |---|---|---|
    | 参数量 | 有（RNN 分量 4,184；全模型 230,828） | **无**（只有 200 KB 部署产物） |
    | 硬件 | **无任何硬件报告**，"可上 MCU"只是建议句 | **有**：Pi Zero 实时推理、Jetson Nano 30 Hz、两套实机平台 |
    | 内存 | 无（"<500 KB"是外部推算） | **200 KB**（TFLite ≈170 KB + 预处理器 ≈10 KB） |
    | 延迟 | 无 | **10 FPS → >30 FPS** |
    | 实车/实机闭环 | 有真车但**零量化指标** | 有实机但**零量化指标**（同样只有定性"成功躲开"） |
    | 可解释性 | 注意力剖面可视化（Fig. 5） | **神经元级激活 + 决策树 + 仿真/实机激活一致**（Fig. 5–8） |
  - 对 P1 的直接含义：**若 P1 要写"该家族可在 <500 KB 内实时运行"，正确的引用组合是"本文（200 KB / Pi Zero / >30 FPS 实测）+ CfC（4,184 递归参数）"，而不是单独引 CfC。** 同时必须写明：本文的任务是无人机躲避球、控制频率 >30 FPS、且**未报告参数量**。
  - **替代关系**：本文**不替代** CfC——本文用的是 **LTC（需 ODE 求解器，欧拉法变体）**，CfC 是去掉求解器的闭式版；若 P1 的卖点是"无求解器的连续时间控制"，本文不能作为该卖点的证据（它反而证明了 LTC 在 200 KB 内也能跑）。

- **引用时必须带的限定语**：
  "在 Tylkin 等关于 **NCP 可解释飞行控制**的工作中（IEEE RA-L 2022;7(2):3265–3272），结论限定于**两个仿真飞行域**（固定翼 Canyon Run、四旋翼 Drone Dodgeball）与**神经元数 9–24 的稀疏 NCP（LTC 神经元、PPO、每域 1,200 万时间步）**：其 **200 KB 内存**为 **TensorFlow Lite 部署产物大小**（≈170 KB 模型 + ≈10 KB 预处理器），**不能换算为参数量**（本文未报告任何参数量）；实时性为 **Raspberry Pi Zero 上 10 FPS、改进后 >30 FPS**（Jetson Nano 平台 30 Hz），全部条件为**低速无人机**，大平台测试**全程地面系留**；性能对比仅有图（**无任何数值、无统计检验、且只取最佳训练运行**），**无 MCU 实测**（Pi Zero/Jetson Nano 属单板机而非车规 MCU），并**不覆盖任何道路/编队/混行场景**。"

- **P1 落地三问**：
  1. **是否有硬件实测？** **有，且是本组唯一有真机实时推理实测的论文。** 具体：① **Raspberry Pi Zero**（电池供电，<10 g）运行 TFLite 模型控制 **DJI Tello**，**早期 10 FPS、后续飞行测试 >30 FPS**（改进来自飞行软件视频流处理）；② **NXP RRDRONE-FMUK66 + PX4 + NVIDIA Jetson Nano + Intel RealSense d435i**，**Jetson Nano 上 30 Hz 推理**，全部飞行测试**低速、地面系留**。**但**：无 MCU（两款都是单板计算机，非车规 MCU）、无功耗/能耗报告、无单步推理时延（ms）、无内存占用实测值（只有文件大小）、无编译器/量化档位说明（只说"built a TensorFlow Lite model"，**未说明是否 int8 量化**）。
  2. **是否报告参数量？** **无。** 全文没有任何参数计数。只有：神经元数 **9–24**（鲁棒性检查覆盖 9–40；正文 §II 的泛化表述是 "tens or hundreds of parameters"），以及 §VII-C 的字节数 **≈170 KB（TFLite 模型）+ ≈10 KB（预处理器）**。**是否含感知头：本地无法确定** —— 200 KB 是"the trained model"的 TFLite 产物，而 Fig. 3 显示流水线是 CNN+MLP 前端 → NCP；模型文件是否已把 CNN/MLP 权重固化为常量、还是只含 NCP 部分，**本文未说明**（`[待核实]`，需向作者确认）。因此 **P1 不得用本文的 200 KB 去推断"含感知头的控制器可 <500 KB"**。
  3. **训练是在线还是离线？** **离线。** 全部在 Unity + ML-Architecture（ML-Agents）仿真中以 PPO 离线训练 **1,200 万时间步**，再导出权重到硬件推理；**无任何在线/增量学习**。**内存/时间开销**：训练侧完全未报告（无 GPU 型号、无墙钟、无显存）。

## 7. 缺失信息（≥3 条，写成可执行动作）
1. **需取回 Table I / II / III 的正文**（本 .txt 只有三个表标题："NEURAL NETWORKS FOR EACH ENVIRONMENT" / "TRAINING SETTINGS" / "DRONE HARDWARE SETTINGS"）。→ 动作：从本机/馆藏 RA-L 7(2) 版 PDF 做表格提取。**在取得前，本卡与 P1 稿件不得引用这三张表的任何一行**（尤其"各网络的层宽/神经元数"与"Pi Zero / Jetson Nano 的具体型号与内存"）。
2. **需向作者确认 200 KB 的口径**：是否包含两个 CNN 与 MLP 前端的权重？TFLite 是否 int8 量化？200 KB 与 170+10 KB 的 20 KB 差额来自何处？（后果：这直接决定 P1 能否把本文当作"含感知头的控制器 <500 KB"的支撑。**这是本卡最重要的一条。**）
3. **需向作者索取参数量计数**（NCP 部分 / CNN+MLP 部分 / 合计），与 CfC 的 4,184 / 230,828 口径对齐。（后果：没有参数量就**无法与 P1 的参数量指标做任何比较**，只能并列陈述"200 KB 部署产物"。）
4. **需向作者索取性能数字**：Canyon Run / Drone Dodgeball 各网络在 100 episode 上的**reward 均值 ± 方差、成功率、episode 长度**，以及 **NCP 与 LSTM/MLP 差异的显著性检验**。（后果：目前"NCP 在 Canyon Run 相对更好、Dodgeball 相当"只有图，且只取 **best run**，属于选择性报告，不能支撑任何"更优"表述。）
5. **需向作者索取真机试验的完整记录**：Pi Zero/DJI Tello 的飞行架次、每次时长、**成功躲避次数与失败次数**、是否发生碰撞、是否有安全员与场地许可；以及 NXP 平台系留测试的判据。（后果：本文实机部分目前**不可复现、不可比较**，与 CfC 的真车实验同病。）
6. **需核验 NCP 的 LTC 数值积分实现细节**（"[3, Algorithm 1] 的欧拉法变体"，步长？与推理帧率的关系？）。（后果：P1 若要声称"连续时间 + 定步长 100 Hz"，需要知道 LTC 的求解步长与推理帧率是否解耦；本文未说明。）
7. **需做 T2 取代检查**：检索 2022 年后是否有"LNN/CfC 家族在车规 MCU 上的实测部署"工作。→ 动作：OpenAlex/Crossref 检索并记录检索式与日期（本卡未做，标 `[待核实]`）。**若存在，P1 的"可上 MCU"应改引该文而非本文。**

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| NCP 部署模型内存 | **200 KB of memory** | 未报告 | Abstract |
| TFLite 模型大小 | **∼170 KB** | 未报告（"∼"为原文符号） | §VII-C Deployment on Drone Hardware |
| 观测预处理器大小 | **∼10 KB** | 未报告 | §VII-C |
| 推理帧率（Raspberry Pi Zero + DJI Tello） | 早期 **10 FPS**；后续飞行测试 **>30 FPS** | 未报告 | §VII-C |
| 推理频率（Nvidia Jetson Nano） | **30 Hz** | 未报告 | §II Related Work |
| NCP 神经元数范围 | **9 到 24**（Canyon Run / Drone Dodgeball 各控制模式下） | — | §I Introduction（"ranging in size from 9 to 24 neurons"） |
| NCP 鲁棒性检查的神经元跨度 | **9**（4 inter + 2 command + 3 motor）到 **40**（16 + 12 + 12） | — | §V 脚注 4 |
| 训练步数 | 每域 **12 million time steps** | — | §VII-A；Fig. 4 图注 |
| 测试规模 | 每个模型 **100 episodes** | 未报告（且只评估"best training run"） | §V 脚注 4；Fig. 4 图注 |
| 随机动作基线奖励（Drone Dodgeball） | 1 DoF **64**；2 DoF **12**；Full DoF **3** | 未报告 | §VII-A |
| 随机动作基线奖励（Canyon Run） | **<1**（每个控制模式） | 未报告 | §VII-A |
| Canyon Run 测试截断 | episode 截断于 **5,000 time steps** | — | Fig. 4 图注 |
| Canyon Run 测试奖励上限 | 1 DoF / 2 DoF **25**（throttle 固定 50%）；Full DoF **36**（throttle 可到 100%） | — | Fig. 4 图注 |
| 航路点奖励（Canyon Run） | 每个成功航路点 **0.5** | — | §IV-1 |
| 站位奖励（Drone Dodgeball） | 每步 **max(0, 1/(d + 0.5) − 0.1)**，d 为到航路点的距离 | — | §IV-2 脚注 1 |
| 撞球惩罚 / 越界 / 倾角终止条件 | −1 额外惩罚；越出 **100 m × 30 m × 100 m**；倾角超 **70°** | — | §IV-2 |
| 传感器规模 | 稠密 **21 × 101 = 2121** 射线；稀疏 **19 × 33 = 627** 射线；外加车辆状态向量 | — | §IV（Observations 段） |
| CNN 配置（脚注 3） | 稠密传感 [32, 11, 4]；稀疏传感 [16, 5, 4]（格式 [num_channels, kernel_size, stride]） | — | §V 脚注 3 |
| 动作空间 | 多离散逼近连续控制，每轴输出 ∈ **{−1, 0, 1}** | — | §IV 末段 |
| 仿真—实机激活峰位差 | 仿真峰 **~9 pixels**；实机峰 **~7 pixels**（球半径） | 未报告 | §VII-C + Fig. 8 |
| 视场差异（sim vs real） | 仿真深度传感器 **90°×90°**；RealSense 裁剪后 **86°×57°** | — | §VII-C |
| Raspberry Pi Zero 质量 | **<10 grams** | — | §VIII Future Work |
| 训练算法与框架 | **PPO**（RLLib）；NCP 基于 **keras-ncp**；仿真用 **Unity + ML-Agents** | — | §VI Solution Overview |
| 训练数据性质 | 全部为**仿真**（Unity 物理引擎）；无真实飞行数据训练 | — | §IV 末段 |

⚠内部不一致 1：正文 §III-A 明写 NCP "consisting of **four layers** of neurons: the sensory neurons, inter-neurons, command neurons, and motor neurons"，而 Fig. 2 图注写 "The NCPs have **three layers** of neurons: inter, command, and motor neurons"——**同一网络层数两处不一致（4 层 vs 3 层）**，差异在于是否把感觉神经元计入。引用时须注明口径。

⚠内部不一致 2：Amini 等的 §IX 结论写 "Unlike other deep neural network architectures, in which **there is a tradeoff** between interpretability and performance, NCPs allow for learning policies that are both highly performant and interpretable"，但 §VII-A 的实测描述是 Canyon Run "**tended to demonstrate relatively higher performance**"、Drone Dodgeball "**comparable to** the performance of the other neural architectures"，且 §VII-A 另写 "comparing the performance across various network depths and larger sizes (**up to 10x larger**), but found **no significant difference** in performance"。→ "不牺牲性能"是**无检验支撑的等价性断言**，且与"放大 10 倍无差异"并置时，"highly performant"缺少可比的量化基线本身。

【确定】/【待核实】标注：以上数字均为 PDF 印出值【确定】；"200 KB 是否含 CNN/MLP 感知头"为 **`[待核实]`**（正文未说明，需向作者确认）；"Table I–III 正文缺失"为对本地 .txt 的直接核验结果【确定】。
