# 分布外鲁棒飞行导航（液态神经网络）｜Robust flight navigation out of distribution with liquid neural networks

- **出处**：Science Robotics 8(77):eadc8892, 2023 ｜ **类型**：期刊论文（Research Article）
- **作者**：Chahine M, Hasani R, Kao P, Ray A, Shubert R, Lechner M, Amini A, Rus D
- **DOI**：10.1126/scirobotics.adc8892
- **全文来源**：`literature/fulltext/meeting2/chahine2023-scirebotics__fd7513e5.txt`（PAGES=15, CHARS=84426）
- **分组**：连续时间 / 流体神经网络（P1 控制器的方法学底座）
- **★ 版本与材料核验**：

  **① 本 PDF 是哪一版？→ 判定：出版社正式版（Version of Record），非作者接受稿。**
  逐字证据与位置：
  - 卷期页脚（p.1 起每页复现，共 15 处）逐字："Chahine et al., Sci. Robot. 8, eadc8892 (2023)" ｜ "19 April 2023" ｜ "N of 14"（N = 1…14）→ 卷 **8**、文章号 **eadc8892**、出版日 **2023-04-19**、连续印刷页码 **1 of 14 … 14 of 14**。
  - p.1 页眉逐字："SC I EN C E RO B OT ICS | RE SEA RCH A RTIC LE"（正式版栏目标识 SCIENCE ROBOTICS | RESEARCH ARTICLE；字号导致的字符间空格为文本层提取现象）。
  - p.1 版权块逐字："Copyright © 2023 The Authors, some rights reserved; exclusive licensee American Association for the Advancement of Science. No claim to original U.S. Government Works"。
  - p.1–p.15 下载水印逐字（共 15 处）："Downloaded from https://www.science.org at Massachusetts Institute of Technology on April 19, 2023" → 该 PDF 是 MIT 用户于**出版当日**从 science.org 下载的出版社文件。
  - p.14 逐字："Submitted 6 May 2022 ｜ Accepted 22 March 2023 ｜ Published 19 April 2023" 与 "10.1126/scirobotics.adc8892" → 收稿/录用/出版三段日期与 DOI 齐备。
  - p.15（AAAS 引文/版权页）逐字："Sci. Robot., 8 (77), eadc8892." ｜ "DOI: 10.1126/scirobotics.adc8892" ｜ "View the article online https://www.science.org/doi/10.1126/scirobotics.adc8892" ｜ "Science Robotics (ISSN ) is published by the American Association for the Advancement of Science." → **卷期 = 8(77)**，与题面一致。
  - 全文 grep：无 "Accepted Manuscript"、无 "This is the author's version"、无 "preprint"（正文引文除外）；"License" 仅 1 处命中（p.14，且指开放代码/数据的 **Apache 2.0**，非论文文本许可）。
  - 文件头 `SOURCE_PDF` 标注 "(MIT CSAIL author copy)"，托管于 `cap.csail.mit.edu` —— 即**作者自存在 MIT CSAIL 站点的出版社正式版 PDF**；排版、页码、DOI、版权页均为 AAAS 正式版形态。**【确定】**
  - ⚠ `[待核实]`：p.15 的 "Science Robotics (ISSN )" 中 **ISSN 号为空**。疑为文本层提取丢失（ISSN 常以特殊字符呈现），**不得据此断言原文缺 ISSN**。

  **② 是否含补充材料？→ 本 .txt/.pdf 不含补充材料本体，只含清单。**
  p.12 逐字："Supplementary Materials / This PDF file includes: / Materials and Methods / Figs. S1 to S10 / Tables S1 to S7 / References (57–61) / Other Supplementary Material for this manuscript includes the following: / Movies S1 to S4 / MDAR Reproducibility Checklist"。
  本文件共 15 页 = 正文 14 页（"14 of 14"）+ 第 15 页 AAAS 引文页；grep 全文**无任何 Fig. S× 图注、无任何 Table S× 表体**，只有正文对它们的交叉引用。**清单完整性可由正文交叉引用反查**：
  - 补充图：figs. S1–S3（显著性图，p.5、p.8）、figs. S7–S8（扰动与对抗物示例，p.6）、fig. S9（徒步任务布置，p.6）、fig. S10（Grass Pitch 场地，p.7）、fig. S2（系统设计图，p.11）、fig. S3（控制协议图，p.12）。
  - 补充表：table S1（各架构最优超参，p.11）、table S2（微调训练参数，p.11）、**table S3（各架构可训练参数量——P1 最需要的一张，p.11）**、table S4（共享 CNN 架构，p.11）、Table S5（旋转/遮挡结果，p.6）、Table S6（对抗徒步成功率，p.6）、table S7（动目标跟踪，p.7）。
  - 补充算法：Algorithm S1（合成序列生成，p.11）、Algorithm S4（VisualBackProp 流程，p.12）。
  → **对 P1 的直接后果：本文的参数量（table S3）与四类任务（旋转/遮挡、对抗徒步、动目标、超参）的量化结果均不在本材料内。** 【确定】

  **③ 网络架构到底是什么？→ 控制器 = CfC（闭式连续时间液态网络）；对照含 NCP（LTC 细胞，需 ODE 求解器）。**
  逐字：
  - p.2："We compared six different recurrent neural network architectures, namely, long short-term memory (LSTM), gated recurrent unit (GRU)–ordinary differential equation (ODE), ODE–recurrent neural network (RNN), temporal convolutional network (TCN), neural circuit policy (NCP), and closed-form continuous-time (CfC)"。
  - p.2："The CfC model (21) is a sparsely wired **four-layer** architecture built by numerical approximation of the closed-form solution of LTCs and is faster to compute than ODE-based models."
  - p.8："Throughout, liquid (neural) networks refer to the general category of models that are presented either by LTCs or CfCs. **CfCs are closed-form liquid networks, and LTCs are ODE-based liquid networks."
  - p.9 Fig. 5(D) 图注："CfC. A sparse neural circuit with the same architectural motifs as NCPs, this time with CfC neural dynamics."
  - p.11："Each network tested was prefixed by a simple CNN backbone for processing incoming images. The **128-dimensional** CNN features were then fed to the recurrent unit that predicted control outputs."（六种架构**共享同一 CNN 主干**）
  - 控制器动力学：式 (1) 为 LTC 的 ODE，式 (2) 为 CfC 闭式（"Time-continuous gating" × 两个 σ 门控，f/g/h 三头共享 backbone）。
  - **神经元数：正文未报告。** 唯一相近句在 p.9："a sparse network configuration composed of **fewer than two dozen LTC neurons** supplied with convolutional heads showed great promise…"，但该句主语是**前人 NCP 工作（引文 18）**，不是本文的 CfC。
  - **层数：CfC = 稀疏四层电路**（p.2 逐字 "sparsely wired four-layer architecture"）。
  - **参数量：正文未报告**。p.11 逐字："For each chosen hyperparameter configuration, the number of trainable parameters in the corresponding model for every neural architecture is listed in **table S3**." → 在补充材料，本材料未含。**【确定】**

  **④ 硬件平台？→ DJI M300 RTK + DJI Manifold 2（内含 NVIDIA Jetson TX2）+ Zenmuse Z30 云台相机；GPU 上跑 TensorFlow 2.3.x。控制频率、时延、内存、参数量全部未报告。**
  逐字（均在 p.11）：
  - "We evaluated the proposed RNN architectures on a commercially available quadcopter with custom software running onboard. The system featured a forward-facing gimbal-mounted camera and a **GPU to run onboard inference**. We used Robot Operating System (ROS) (55) to handle communication between the RNN inference code and the lower-level drone flight controller."
  - "A **DJI M300 RTK** quadcopter was used for data collection and evaluation of policy performance. … It also interfaces with the **DJI Manifold 2 companion computer**, enabling programmatic control of the drone. The companion computer included an **NVIDIA Jetson TX2**, which has a CPU and GPU. The DJI Onboard SDK and its associated ROS wrapper provided an interface for giving the drone's low-level flight controller **desired linear and angular velocity set points**. The flight controller is a **black box** not modifiable by the end user, but it controls the four-rotor speeds to track the velocities specified by the TX2 computer."
  - "A **Zenmuse Z30** camera and gimbal were mounted on the underside of the drone, pointed forward."
  - "The TX2's **GPU** ran the RNN inference with **GPU-accelerated Tensorflow 2.3.x**."
  - 图像输入尺寸（p.11）逐字："The size of the input images was **144 pixels by 256 pixels**.]"（原文方括号不配对，为原文错误）。
  - **控制频率（Hz）：全文未见**（grep `Hz` / `fps` / `FPS` / `frame rate` **零命中**）。唯一相关句 p.11 逐字："The sequence length was also randomized to be between 120 and 250 frames to encourage robustness to external forces or **varying update frequencies**." → 回环频率**可变且未给数**。
  - **推理时延（ms）：全文未见**（grep `latenc` 零命中）。
  - **内存占用 / 参数量（KB / MB / 个数）：全文未见**（grep `memory` 仅命中 LSTM 记忆单元与生物记忆机制；grep `parameter` 仅命中超参、式 (1) 的 "bias parameter" 与指向 table S3 那一句）。
  - ⚠ **不是 MCU**：Jetson TX2 为嵌入式计算模块/单板计算机。P1 措辞上限仍为"已在**单板机**上实测实时推理"。**【确定】**

  **⑤ 闭环还是开环？→ 真机闭环；训练数据 = 离线人类示范 + 图像裁剪合成序列 + 微调；OOD 通过"换场景 + 任务外推"构造，但任务结构保持不变。**
  逐字：
  - 闭环：p.3 "**Closed-loop (online) testing** / All seven tasks were evaluated in closed loop with environments by **running the neural networks onboard the drone**."；p.3 "We launched the **closed-loop policy** and observed whether the network could successfully guide the drone to the target."
  - 训练数据来源：p.1/2 "We trained neural network agents on **a few runs of data collected by a human pilot** in an **offline supervised learning** setting"；p.3 "The objective was to learn to complete this task **entirely from an offline dataset of expert demonstrations**."
  - Fig. 6 图注（p.10）逐字："(D) The training process started by **hand-collecting human expert trajectories** and recording camera observations and human expert actions. (E) To further convey the task, we then generated **synthetic sequence** by taking images collected during human flights and repeatedly cropping them… (F) The networks were trained **offline** on the collected expert sequences using a **supervised behavior cloning MSE loss**. (G) We then **deployed trained networks on the drone in online testing** and observed task performance under heavy distributional shifts…"
  - **无仿真引擎**：合成数据由**真实飞行图像反复裁剪**生成（p.10/11），非物理仿真；**无在线/增量学习**。
  - OOD 构造（八项任务，p.2 列表 + p.4 展开）：① 四测试环境 Training Woods / Alternative Woods / Urban Lawn / Urban Patio；② 射程外推 10 → 20 → 30 m；③ 离线图像扰动压力测试（噪声/亮度/对比度/饱和度）；④ 目标旋转 90°/180° 与黑帘遮挡；⑤ 对抗物徒步（含不同材质的两把红椅等干扰目标）；⑥ 三角循环（无穷步）；⑦ 动目标跟踪（Urban Lawn 与 Grass Pitch）；⑧ Patio 内布置多把不同颜色（含红色）与尺寸的椅子。
  - ⚠ **关键限定（P1 必须带）**：p.3 逐字 "…to evaluate the networks' performance in OOD settings but **maintained a task structure identical to the one learned from training data**." → 这是**环境/外观分布移动**，不是任务或动力学分布移动。
  - 控制接口：网络输出 **desired linear and angular velocity set points**，交黑箱飞控跟踪（p.11）→ 神经网络是**高层速度指令器**，非底层执行器控制器。**【确定】**

  **⑥ 有无统计？→ 有 N 与成功率（不报总平均、逐环境报）；无 CI、无显著性检验、无随机种子、无独立重复。**
  逐字：
  - Table 1 表注（p.4）："Closed-loop evaluation of the fly-to-target task for the trained policies in four testing environments. Quantitative results are success rates. Higher is better. **(N = 40)**"；正文 p.3："The test was **repeated 40 times for each network and in each environment**."
  - Table 2 表注（p.4）："Range test evaluation of the trained policies in the Training Woods environment. Quantitative results are success rates. Higher is better. **(N = 10)**"；正文 p.4："We ran **10 experiments for each of 10-, 20-, and 30-m distance** from the target."
  - Fig. 2 图注（p.5）："Bars show the **SD across 10 runs**… **(N = 10)**"。
  - p.12 "Statistical analysis" 逐字："The quantitative results of the paper presented in Tables 1 and 2 and table S4 to S7 all supply the number of active tests performed, N, and **report the success rate of models in each scenario in percentages**. On all compartments of Fig. 2, each point represents the **mean across 10 runs**, whereas the vertical bar on each point represents the **SD** corresponding to the data entry."
  - **置信区间：未报告**（grep `confidence` / `interval` 零命中）。
  - **显著性检验：未报告**（grep `p value` / `significan` 仅命中 2 处非检验语境：p.12 "still maintaining enough frames to yield **statistically significant** results"——该句**未做任何检验**；另一处是引文标题中的 "Artificial Intelligence and Statistics"）。
  - **随机种子：未报告**（grep `seed` 仅 1 处命中，p.11 "model-specific hyperparameters such as backbone unit count or **connection seed**"——这是被 TPE 调优的超参，不是可复现性意义上的种子清单）。
  - 超参搜索（p.11 逐字）："we used **tree-structured Parzen estimators (TPEs)** (53, 54) for tuning hyperparameters… The set of parameters leading to the lowest **train + validation loss over the 40 episodes** was selected for the final tested model. … After **three trials**, episodes with a higher median training + validation loss on the **10th epoch** were pruned early… Hyperparameter optimization was implemented using the **Optuna** library."（按 train+validation loss 选优、非按测试集选优——此点对公平性有利）
  - 独立重复：**未见**。致谢中"thank J. Feld, I. Futran, K. Mishra, P. Whartenby, C. Vorbach, T.-H. Wang, and W. Xiao **for testing NCP and CfC models for confirmation of results across other domains**"（p.13）为**组内**交叉确认，非外部独立复现。**【确定】**

- **证据等级初判**：**B 级** —— 六架构 × 四环境 × N=40 的真机闭环对照 + 多任务外推 + 全部代码/数据开放（Apache 2.0），其设计强度高于本批已读的两张同族卡（RA-L 2022 NCP：性能只有图、无数字；CfC NMI 2022：真车实验零量化指标）；但**无 CI、无显著性检验、无种子清单、无外部独立重复、无预注册**，主要结论建立在 N=40（射程/压力测试为 N=10）的二项成功率之上而无不确定度。按铁律 1，A 级要求的"效应量与 CI + 内部独立重复"未达成。
- **档位建议**：**A 精读** —— 满足协议 §5 的 A 档判据（加权 18 ≥ 14、D1 = 2、D5 = 2），是"LNN 家族在真实硬件上闭环控制且能分布外泛化"这一命题的**最强已发表证据**，且公平性协议（共享 CNN 主干 + 逐架构超参搜索 + 逐环境报 N）可被 P1 直接照搬。⚠ 但须提请注意：协议 §4 的 A 档预算为 **5 篇**，本卡为新加入第 5 组（连续时间/流体神经网络）的**第 6 篇**，是否占用/挤占 A 档名额需按 §8.4 破平或由用户裁定。
- **五维打分（按 `00-triage-protocol.md` §5，各维 0–2，满分 20）**：D1=2 D2=2 D3=1 D4=2 D5=2 → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = 6+4+2+2+4 = **18**
  - D1=2：给出 P1 拟采用的**控制器架构本身（CfC）**在真机闭环下的跨架构对照与 OOD 评价协议。与 §8.2 中 RA-L 2022 NCP 卡给 D1=2 的口径保持一致。
  - D2=2：六架构同主干对照 + 四环境真机闭环 + 多任务外推 + N 与 SD 报告（**但无检验**，已在卡中记明）。
  - D3=1：**代码与协议部分可迁移**（Apache 2.0、共享主干与超参搜索协议、离线压力测试范式），**数据与场景不可迁移**（无人机自采图像）。
  - D4=2：2023 年发表，距今 ≤5 年。
  - D5=2：正式版全文 14 页 ✓ + 效应量（Tables 1–2 印出成功率与 N；Fig. 2 印出 mean ± SD）✓ + 可复现材料（Zenodo 代码 DOI + 全部数据集含文件名与体积 + MDAR 清单 + Movies S1–S4）✓。⚠ 本地副本缺补充材料 PDF（见「缺失信息」第 1 条），引用 table S1–S7 / figs. S1–S10 的数字前必须先取回。
  ⚠ 本卡**严格使用 0–2 制**；D4 一律指**时效性**。

## 1. 标题
原文标题（逐字）：**Robust flight navigation out of distribution with liquid neural networks**（p.1 标题栏；p.15 引文页复现）｜中文直译：**用液态神经网络实现分布外鲁棒飞行导航**

## 2. 摘要（≤400 字中文，保留关键数字与结论成立条件）
作者提出基于液态神经网络（LNN）的模仿学习框架，在**单一环境（Training Woods）的离线人类示范**上训练四旋翼端到端视觉导航策略，再**零样本**部署到场景剧变的 OOD 环境。任务为 fly-to-target：仅用机载 RGB 图像，把无人机从约 10 m 外引导到距目标 2 m 内并使目标居中 10 s。对比 6 种架构（LSTM、GRU-ODE、ODE-RNN、TCN、NCP、CfC），全部**共享同一 CNN 主干**（128 维特征），逐架构做 TPE 超参搜索。四环境成功率（N=40/网络/环境）：Training Woods 上 NCP 100%、CfC 85%、LSTM 82.5%；Urban Lawn 上 CfC 90%、LSTM 62.5%、GRU-ODE 32.5%、ODE-RNN 17.5%、TCN 0%；Urban Patio（含同类干扰目标）上 CfC 67.5%、NCP 52.5%、LSTM 27.5%、ODE-RNN 25%、GRU-ODE 17.5%、TCN 0%。射程测试把起点从 10 m 外推到 20/30 m：CfC 得 90%/20%，LSTM 为 0%/0%，ODE-RNN 为 10%/0%，GRU-ODE 为 0%/0%，非液态网络基本全败。另有旋转/遮挡、对抗物徒步、三角循环、动目标跟踪与离线图像扰动压力测试，CfC 总体占优（旋转仅降 10%、遮挡降约 30%、对抗徒步 20 次完成 14 次、动目标平均 8.8 个检查点 vs LSTM 5.8）。**成立条件**：OOD 仅指环境/外观与起点距离的移动，**任务结构与训练时完全相同**。

## 3. 结论（≤350 字中文：作者结论节要点 + 关键数字 + 作者自承的局限）
作者结论：**模型选择对 OOD 泛化是决定性的**；液态网络（LTC 的 ODE 表示与 CfC 的闭式表示）在全部射程测试、旋转/遮挡、对抗徒步与动目标任务上总体优于非液态对手。关键数字：CfC 在 2×/3× 训练距离上 90%/20%；旋转使 CfC 仅降 10%（成功率 >80%），遮挡降约 30%（60%）；对抗徒步 20 次完成 14 次（70%），为最强非液态对手的两倍以上（LSTM 30%）；动目标平均 8.8 个检查点，比 LSTM 的 5.8 长约 50%。作者把泛化归因于两点：液态网络在端到端训练中对 CNN 头部施加归纳偏置（显著性图为证），且 LTC 在细胞层面是动态因果模型（DCM）——**后者是引 Vorbach 等的理论证明，非本文实验**。作者**无独立 Limitations 小节**；自承局限散见三处：数据增广**不能**使控制任务在换环境后稳健执行（p.8）；因果建模框架无法用于本文这种高维、任务结构未知的设定（p.8）；离线压力测试只喂前 40% 帧，因固定输入帧无法建模视角变化（p.12）。另需指出：作者**未自承**缺少参数量/时延/内存报告。

## 4. 方法一句话
机载 RGB 图像序列 → 共享 CNN 主干（128 维特征）+ 稀疏四层 CfC 循环控制器 → 期望线速度与角速度设定点，经 ROS 交 DJI 黑箱飞控跟踪。

## 5. 图表清单（占位符）
**总数**：正文 Figure 6 个 + 正文 Table 2 个 + 补充 Figs. S1–S10（10）+ 补充 Tables S1–S7（7）= **Figure + Table 合计 25 个**；另有序号被正文引用的 Algorithm S1、S4（2 个）与 Movies S1–S4（4 个），不计入图表总数。**本表按要求覆盖前 14 个**（正文全部 8 个 + 补充 Fig. S1–S6），其余 11 个补充条目列于表后清单。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-CHAHINE-1} | Fig. 1（p.3） | "Sample frames of training and test environments. (A) Third-person view of the quadrotor and one of the targets in the Training Woods where data were collected. (B)…" | 定义"训练分布 vs 四个测试环境"的视觉差距；(C) 训练帧含三种目标（露营椅/储物箱/遥控车）与三个季节（夏/秋/冬）——说明**目标多样性 + 季节多样性在训练集内已有覆盖**，OOD 轴是**背景与光照**而非目标类别。 |
| {TAB-CHAHINE-1} | Table 1（p.4） | "Closed-loop evaluation of the fly-to-target task for the trained policies in four testing environments. Quantitative results are success rates. Higher is better. (N = 40)" | **本卡最重要的数字表**：6 架构 × 4 环境成功率，逐环境报。注意 in-distribution 上 NCP 100% > CfC 85%，CfC 的优势**只在 OOD 成立**（Urban Lawn 90%、Patio 67.5%）。 |
| {TAB-CHAHINE-2} | Table 2（p.4） | "Range test evaluation of the trained policies in the Training Woods environment. Quantitative results are success rates. Higher is better. (N = 10)" | **"外推式 OOD"的最干净证据**：10/20/30 m 三档。CfC 100/90/20%；20 m 上除 CfC（90%）与 NCP（50%）外全部 ≤10%，30 m 上仅 CfC 有 20%。⚠ N=10 → 单次成功即 10 个百分点。 |
| {FIG-CHAHINE-2} | Fig. 2（p.5） | "Noise, brightness, contrast, and saturation stress tests. These experiments run both an original image sequence collected by the drone and a perturbed…" | **唯一印出不确定度的图**（bars = SD across 10 runs）。四条曲线对应四种扰动，横轴为扰动量。**P1 可直接借用的"离线鲁棒性代理"范式**：扰动 → 网络输出速度 → Forward Euler 积分 → 两条轨迹终点距离（越低越好）。 |
| {FIG-CHAHINE-3} | Fig. 3（p.6） | "Evolution of flight-time networks' attention maps. (A) A frame illustration of the attention profile of different networks computed by the VisualBackProp…" | 可解释性核心图：上排原图、下排 VisualBackProp 显著性图（0 黑 → 1 白）。(B)(C) 两个 OOD 失败案例：LSTM **感知到目标却飞离/转向干扰物** → 说明失败点在"卷积头到递归模块的表征错配"，而非感知失败。 |
| {FIG-CHAHINE-4} | Fig. 4（p.7） | "Triangular loop between objects. (A) The triangular infinite loop task setup. (B) Time instances of drone views together with their attention map at steps…" | 三椅构成边长 10 m 等边三角形，检测到检查点后右转 120°；作者称可无限循环，**实际跑 4 圈共 12 个检查点即停**（p.7 正文）——"indefinitely"是设计能力而非实测长度。 |
| {FIG-CHAHINE-5} | Fig. 5（p.9） | "Liquid neural networks. (A) Schematic demonstration of a fully connected LTC layer (35). The dynamics of a single neuron i is given, where xi(t)…" | (A) LTC 全连接层；(B) CfC 闭式结构（两个 σ / 1−σ 门控 + f/g/h 三头）；(C) NCP 四层稀疏电路；(D) **CfC = 与 NCP 同架构基元、但换成 CfC 神经动力学**。⚠ 图注 (C) 把第四层写成 "interneurons"（与第二层重名），见内部不一致清单。 |
| {FIG-CHAHINE-6} | Fig. 6（p.10） | "End-to-end learning setup. (A) Policies were trained to solve the following task: Using only images taken from an onboard camera, navigate the drone…" | 训练管线全图：(D) 人工采集示范 → (E) 单张图反复裁剪合成"接近并居中"序列 → (F) 离线行为克隆 MSE → (G) 机上在线测试。**P1 写训练协议时的对照模板**（无仿真器、纯离线 + 图像级合成增广）。 |
| {FIG-CHAHINE-S1} | Fig. S1（补充材料） | 未见图注 | 显著性图（p.5、p.8 交叉引用："We show more comprehensive saliency maps in different scenarios in figs. S1 to S3"）。**本 .txt 未含，数字/图像均不可引用。** |
| {FIG-CHAHINE-S2} | Fig. S2（补充材料） | 未见图注 | ⚠ **编号冲突**：p.5 将其列为显著性图组之一，p.11 又写 "A depiction of the system design can be found in fig. S2."。**在取得补充材料前不得引用。** |
| {FIG-CHAHINE-S3} | Fig. S3（补充材料） | 未见图注 | ⚠ **编号冲突**：p.5 将其列为显著性图组之一，p.12 又写 "This control protocol (depicted in fig. S3)"。**在取得补充材料前不得引用。** |
| {FIG-CHAHINE-S4} | Fig. S4（补充材料） | 未见图注 | 正文未被交叉引用（不在 p.5/p.6/p.7/p.8/p.11/p.12 的 S 图引用列表中）。内容未知。 |
| {FIG-CHAHINE-S5} | Fig. S5（补充材料） | 未见图注 | 正文未被交叉引用。内容未知。 |
| {FIG-CHAHINE-S6} | Fig. S6（补充材料） | 未见图注 | 正文未被交叉引用。内容未知。 |

**其余 11 个未列表条目（本 .txt 均未含，图注一律"未见图注"）**：
- 补充图：{FIG-CHAHINE-S7} Fig. S7（扰动示例，p.6 引用）、{FIG-CHAHINE-S8} Fig. S8（对抗物示例，p.6 引用）、{FIG-CHAHINE-S9} Fig. S9（徒步任务布置，p.6 引用）、{FIG-CHAHINE-S10} Fig. S10（Grass Pitch 场地，p.7 引用）。
- 补充表：{TAB-CHAHINE-S1} table S1（各架构最优超参，p.11 引用）、{TAB-CHAHINE-S2} table S2（微调训练参数，p.11 引用）、**{TAB-CHAHINE-S3} table S3（各架构可训练参数量——P1 最需要，p.11 引用）**、{TAB-CHAHINE-S4} table S4（共享 CNN 架构，p.11 引用；但 p.12 又把它列为"给出 N 的结果表"，编号冲突）、{TAB-CHAHINE-S5} Table S5（旋转/遮挡结果，p.6 引用）、{TAB-CHAHINE-S6} Table S6（对抗徒步成功率，p.6 引用）、{TAB-CHAHINE-S7} table S7（动目标跟踪，p.7 引用）。

## 6. 对 P1 的用处

- **与 P1 的关系**：**相邻问题（同一方法家族 + 真机闭环 + OOD 泛化协议），但不同 ODD、不同任务、不同指标。** 本文不测 P1 的 RQ（OTF 势场在高速主线编队控制中的作用），但它把"LNN 家族在真实硬件上闭环控制、并在分布外场景大幅优于（成功率口径）LSTM/ODE-RNN/GRU-ODE/TCN"这一命题**做成了有 N、有六架构对照、有四个 OOD 环境的已发表实机证据**——这是 P1 控制器选型论证（A2 消融）能拿到的最强外部支撑。

- **可迁移**（具体到方法/协议/数字/图表）：
  1. **★ "为什么选 CfC 而不是 LSTM/ODE-RNN"的实机对照数字**：Table 1（p.4，N=40）与 Table 2（p.4，N=10）。最有力的一对是 **Urban Lawn 上 CfC 90% vs LSTM 62.5% vs ODE-RNN 17.5%**，以及 **20 m 射程上 CfC 90% vs LSTM 0% / ODE-RNN 10% / GRU-ODE 0% / TCN 0%**。P1 的 Introduction 与 A2 消融可用它做"范式选择已被独立实机验证"的动机，但**不得**写成"CfC 在跟驰控制上更优"。
  2. **★ 公平性协议可直接照搬**（正对 `AGENTS.md` §3「同等可用信息、同等调参预算」）：p.11 逐字 "Each network tested was prefixed by a **simple CNN backbone**… The **128-dimensional CNN features** were then fed to the recurrent unit"——**六种架构共享同一感知前端**，差异只归因于递归模块；超参用 TPE（Optuna）逐架构搜索，**按 train + validation loss 选优**（非按测试集选优），40 episodes、3 trials 后剪枝。这套"共享前端 + 等预算逐架构调参 + 按验证损失选优"是 P1 对齐 PID/MPC/TD3/OTF-CfC 四条基线时可原样借用的纪律。
  3. **闭环评价协议模板**（正对 `AGENTS.md` §5「逐场景报告」）：成功判据 = 距目标 ≤2 m 且目标在画面中心保持 **10 s**；失败判据 = 目标离开视场且不可恢复，**或 30 s 内未到达**；每网络每环境 **N = 40**；**逐环境报成功率，不报总平均**。P1 的跟车场景库（前方无车/邻车插入/前车减速/前车驶离 + 长尾）可套用同一结构：显式成功判据 + 显式失败分类 + 每场景 N + 逐场景表。
  4. **"外推式 OOD"的轴设计**（Table 2）：本文把训练分布外推的**连续变量**（起始距离 10 → 20 → 30 m）当作 OOD 轴，而不是只换外观。P1 可对应为 **OTF 势场强度 / 交通密度 / 编队规模**的外推档位——比"换天气/换地图"更接近 P1 的场景泛化主张。
  5. **★ 廉价的离线鲁棒性代理（stress test 范式，p.4 + p.12）**：对录制的真实帧施加扰动（高斯噪声、亮度、对比度、饱和度）→ 同一网络对原图与扰动图各出一串速度指令 → **Forward Euler 积分成位置轨迹** → 取两条轨迹终点距离作为鲁棒性指标；只喂前 **40%** 帧（作者理由：固定输入帧无法建模视角变化，序列越长估计越失真）；报 mean ± SD（N=10）。**这套流程不需要闭环即可量化"输入分布移动下的输出漂移"，P1 在 CARLA 或实车回放上做同构实验成本极低**，可作为 OTF 消融的补充证据。
  6. **"LNN 只做高层指令器、底层交既有控制器"的分工已被真机验证**：p.11 逐字 "giving the drone's low-level flight controller **desired linear and angular velocity set points**… The flight controller is a **black box** not modifiable by the end user"。这正是 P1 架构原则「闭环用 MPC+LNN 混合（大胆决策，小心修正）」的**实机存在性证明**——LNN 输出速度/加速度级指令，底层控制器负责跟踪。
  7. **可解释性协议**（Fig. 3 + p.12）：**共享 CNN 头 → VisualBackProp 显著性图 → 用显著性图做成功/失败归因**。作者的诊断很实用：LSTM 的卷积头**看得见目标**却仍飞离（p.8 逐字 "the LSTM's perception module detects the target but still fails to navigate the drone"），说明失败发生在"感知表征 → 递归决策"的转换，液态网络在这两个模块间的表征更一致。P1 的 OTF 可解释性论证可复用"共享感知头 → 显著性/激活 → 成功失败归因"这条链条。
  8. **可核验的复现入口**（p.14）：Zenodo（Apache 2.0）代码 + 四份数据集（原始 33.2 GB「devens snowy」、微调 2.3 GB「devens chair」、合成 14.7 GB「synthetic small4」、合成 4.3 GB「synthetic chair」）。P1 若要复现 CfC 控制器，这是合法且可追溯的代码来源（与 CfC 原文的 `github.com/raminmh/CfC` 互补）。

- **不可迁移 / 陷阱**（含四旋翼 ODD vs 高速公路编队 ODD 的差距）：
  1. **★ ODD 差距（必须写清）**：本文是**单机四旋翼、室外林/草坪/砖地、纯视觉 fly-to-target**；**无车道、无车道线、无他车、无编队、无跟驰、无纵横向车辆动力学、无人机混行、无速度约束、无安全距离约束**。P1 的 ODD 是**高速公路主线、多车道、人工与自动混行下的编队连续时间控制**。两者的状态空间、动作语义、失效后果、安全约束完全不同 → 本文任何成功率**都不得**表述为对 P1 场景的适用性证据（对应 `AGENTS.md` §5「跨 ODD 结论无效」）。
  2. **控制频率完全未报告** → P1 的 **100 Hz（10 ms）**目标在本卡**零证据**。相反，p.11 逐字 "varying update frequencies" 暗示其回环频率本身就是**不固定**的。P1 不得写"本文证明了 LNN 可用于 100 Hz 实时控制"。
  3. **参数量 / 内存 / 时延 / 功耗四项全无** → P1 的**参数量主张**（`<500 KB` 红线）与**端到端延迟主张**均**不能引本文**。本文唯一与"算力"有关的信息是"Jetson TX2 的 **GPU** 上跑 GPU 加速的 TensorFlow 2.3.x"——与 P1 的"MCU 内存占用"指标不同口径。
  4. **"实时"二字本文根本没写过**：全文 grep 无 `real-time` / `fps` / `Hz`。**"已在单板机上实测实时推理"这一措辞在本卡也需要 P1 自己承担解释责任**（本文只证明"机载闭环跑通了"，未给速率）。
  5. **⚠ OOD 的强度弱于 P1 所需**：p.3 逐字 "maintained a task structure identical to the one learned from training data" → 本文是**环境/外观 + 起点距离**的移动，**任务定义与动力学不变**。P1 若要用它支撑"OTF 势场使控制器在 ODD 内场景变化下仍稳健"，必须写明这一限定；否则是把"外观分布移动"偷换成"场景/交互分布移动"。
  6. **无显著性检验、无 CI、无种子** → N=40 下单次成功 = 2.5 个百分点，而本文**未做任何检验**：Urban Lawn 上 CfC 90% vs LSTM 62.5% 是大幅差距，但 Training Woods 上 CfC 85% vs NCP 100%、Alt. Woods 上 CfC 95% vs NCP 95% 这类比较**在本卡无法判定是否超出抽样波动**。P1 若要引用比较结论必须自补区间（`AGENTS.md` §4：小样本成功率用 Wilson 或 Clopper-Pearson，**不得**用正态近似）。
  7. **自比风险**：六种被比较架构中，**NCP 与 CfC 都是作者自己组的方法**（表中标 "NCP (ours)" / "CfC (ours)"），而结论正是这两者胜出。本文没有任何"第三方独立实现 NCP/CfC"的说明，LSTM/ODE-RNN/GRU-ODE/TCN 的实现细节与调参预算（除"40 episodes"外）也未给出 → P1 引用时应写成"**作者自实现的对照**"。
  8. **作者对泛化机制的归因不是本文实证**：DCM/因果性是引 Vorbach 等（引文 21）的**理论**结论（p.8 逐字 "This was theoretically shown in Vorbach et al. (21)"；p.9 另逐字 "Vorbach et al. (21) theoretically showed that the learning system described by an LTC network of Eq. 1 can control internal and external interventions by the network parameters θ and thus reduces to a DCM (43) as long as f is monotonically increasing, bounded, and Lipschitz continuous."）。P1 不得把"液态网络是动态因果模型（因而可解释）"当作本文的实验结论。
  9. **数据不可迁移**：训练数据是无人机自采图像（33.2 GB 等），与 P1 的车辆/交通数据无关。**代码可复用，数据与场景不可**。
  10. **补充材料编号本身有冲突**（fig. S2/S3、table S4 各被两种内容引用）→ 引用任何补充条目之前必须先取回补充 PDF 并核对。

- **与 RA-L 2022 NCP 飞行（`notes/ral2022-interpretable-flight-ncp.md`）的对照 —— 哪一篇才是 P1 该引的硬件证据？**
  **明确判断：两篇分工引用，任何一篇单独都不够；若只能引一篇讲"LNN 家族真机闭环 + 分布外泛化"，引本文（Science Robotics 2023）。**
  理由与分工：

  | 维度 | RA-L 2022（Tylkin 等，NCP） | **Science Robotics 2023（Chahine 等，CfC）** |
  |---|---|---|
  | 架构 | NCP（**LTC 细胞，需 ODE 求解器**，欧拉法变体） | **CfC（闭式，无求解器）** + 对照含 NCP |
  | 任务 | 仿真训练 → 实机推理（Canyon Run / Drone Dodgeball） | **真机闭环飞行**（正文列出 8 项编号任务，另称 "All seven tasks"，见内部不一致 7） |
  | 性能数字 | **无任何数值**（Fig. 4 只有曲线；无成功率、无检验） | **有**：6 架构 × 4 环境成功率，N=40；射程 10/20/30 m，N=10 |
  | OOD 证据 | 无（域内训练，实机验证行为） | **核心卖点**：跨场景零样本迁移 + 起点外推 + 旋转/遮挡 + 对抗物 |
  | 参数量 | 无 | **无**（指向补充材料 table S3） |
  | 内存 | **200 KB**（TFLite ≈170 KB + 预处理器 ≈10 KB） | 无 |
  | 延迟/频率 | **10 FPS → >30 FPS**（Pi Zero）；Jetson Nano 30 Hz | **无**（仅"TX2 的 GPU 上跑 GPU 加速 TF 2.3.x"） |
  | 硬件 | Raspberry Pi Zero / Jetson Nano / NXP FMUK66（**<10 g 单板机**，部分测试地面系留） | DJI M300 RTK + Manifold 2 + **Jetson TX2**（企业级机载，全部真飞） |
  | 统计 | 无（且只取 best training run） | N 明确、逐环境报、Fig. 2 有 SD；**无检验/无 CI/无种子** |
  | 开放材料 | 无代码/数据声明 | **Zenodo + Apache 2.0 + 四份数据集** |

  → **对 P1 的直接结论**：① **"LNN 家族在真实硬件上闭环控制且能分布外泛化"这句主张，应引本文**（唯一有量化 OOD 闭环结果的实机论文；RA-L 那篇**根本没有性能数字**）；② **"内存占用"这一指标仍只能引 RA-L 2022 的 200 KB**（口径是 TFLite 部署产物大小，不是参数量，且是 NCP/LTC 而非 CfC）；③ **两篇都不能支撑 P1 的"端到端延迟"**（RA-L 给的是帧率 10→>30 FPS，且作者明确归因于飞行软件的视频流处理而非模型；本文一个字都没给）；④ **两篇都不是 MCU**（Pi Zero / Jetson Nano / Jetson TX2 全是单板机）→ P1 的措辞上限仍为"**已在单板机上实测实时推理**"，红线不变。

- **对 P1 三条工程主张（参数量 / 端到端延迟 / 可解释性）各自能供什么**：
  1. **参数量 —— 本文供不了任何数字。** 正文只有定性架构描述（"sparsely wired four-layer"、共享 CNN 主干出 128 维特征），参数量被显式推到补充材料 table S3（p.11 逐字），而本材料未含该表。**动作**：取回补充 PDF 后 table S3 将给出**六种架构在同一起点上的可训练参数量**——这恰好是 P1 A2 消融"按参数量对齐"最需要的横向标尺（若 CfC 的参数量与 LSTM 同量级而 OOD 成功率差 25 个百分点以上，可支撑"优势来自架构而非容量"）。在拿到 table S3 之前，**P1 不得从本文推出任何参数量表述**。
  2. **端到端延迟 —— 本文供不了任何数字，且方法学上有反证价值。** 全文无 Hz / ms / fps / 时延。可用的只有两条**定性**事实：① 推理确实在**机载** GPU 上完成并闭环（p.3 "running the neural networks onboard the drone"）；② 回环频率**可变**（p.11 "varying update frequencies"）。→ P1 若要把"端到端延迟"作为卖点，**必须自测**；可引本文的只是"机载闭环推理可行"这一存在性事实（措辞：**"已在单板机上实测实时推理"，不写 MCU，不写 Hz**）。
  3. **可解释性 —— 本文供一条可复用的协议，但只到"感知层"。** 供的是：共享 CNN 头 → VisualBackProp 显著性图（Fig. 3）→ 用显著性图区分"感知到但决策错"与"根本没感知到"（Fig. 3B/C 的 LSTM 案例）；作者并明确写"数据增广能让**所有**网络得到稳定的显著性图，但**不能**让控制任务在换环境后稳健执行"（p.8）——这是一条**很有用的负面结论**，说明显著性图好看 ≠ 控制稳健，P1 写可解释性时**不能只靠显著性图**。→ **神经元级可解释性（扫掠标量 → 单神经元激活热图 → 决策树）本文没有**，那一块仍须引 RA-L 2022 NCP（Fig. 5–8）。P1 的可解释性论证宜**两篇并用**：神经元级用 RA-L，感知层失败归因用本文。

- **引用时必须带的限定语**（一句，含样本/场景/协议边界）：
  "在 Chahine 等关于**液态神经网络分布外鲁棒飞行导航**的工作中（Science Robotics 2023;8(77):eadc8892），结论限定于**单机四旋翼的纯视觉 fly-to-target 任务**：在**单一环境（Training Woods）的离线人类示范 + 图像裁剪合成序列**上以行为克隆 MSE 离线训练、零样本部署到四个场景剧变的测试环境，**且明确保持任务结构与训练时相同**（N=40/网络/环境；射程外推 20/30 m 为 N=10），六种架构（LSTM、GRU-ODE、ODE-RNN、TCN、NCP、CfC）**共享同一 CNN 主干（128 维特征）**并各自经 TPE 超参搜索；机载平台为 **DJI M300 RTK + Manifold 2 内的 NVIDIA Jetson TX2**（GPU 上跑 TensorFlow 2.3.x，网络只输出**速度设定点**交**黑箱**飞控跟踪），**未报告参数量、控制频率、推理时延、内存占用与功耗**；成功率**未给置信区间、未做显著性检验、未报告随机种子**，且 NCP 与 CfC 均为**作者自实现**；**结论不覆盖任何道路、车道、交通参与者、编队或人机混行场景，也不构成 MCU 部署证据**。"

## 7. 缺失信息（≥3 条，写成可执行动作）
1. **需取回本文的补充材料 PDF**（Science Robotics 正式版附件，DOI 10.1126/scirobotics.adc8892），重点是 **table S3（六种架构的可训练参数量）**、table S1（最优超参）、table S2（微调参数）、table S4（共享 CNN 架构）、Table S5（旋转/遮挡）、Table S6（对抗徒步）、table S7（动目标）与 figs. S1–S10。（后果：**P1 最需要的参数量口径目前为零证据**；本卡 §8 中旋转/遮挡、对抗徒步、动目标三组数字只能引用正文的汇总值，不能引用分架构数值。）
2. **需向作者索取机载实时性实测**：控制回环频率（Hz）、单帧推理时延（ms）、TX2 上的内存占用、模型参数量与数值精度（TensorFlow 2.3.x 是否用 fp16/int8）、以及是否做过任何嵌入式/车规级量化。（后果：P1 的"端到端延迟"与"MCU 内存占用"两条指标**不能引本文**；"LNN 可实时闭环"在本卡只能定性表述。**这是 P1 最需要补齐的一条。**）
3. **需向作者索取统计细节**：Table 1 各成功率的不确定度（Wilson 或 Clopper-Pearson 区间）、是否做过多重比较校正、TPE 搜索的随机种子/试次数，以及六种架构的调参预算是否**等量**。（后果：CfC 90% vs LSTM 62.5% 这类关键差距目前无法判定显著性；P1 若写成"显著更优"即属越界。）
4. **需作者澄清旋转/遮挡"reductions of 70, 60, and 30%"的口径（相对下降还是百分点下降）与该项实验的 N**。（后果：按 Table 1 的 Urban Lawn 基线复算，GRU-ODE 32.5% 只有"相对下降 70%"讲得通（→10%），而 CfC 90% 只有"下降 30 个百分点"讲得通（→60%）；**两种口径互斥，这三个数字在澄清前不可引用**。另：'1 success between both the 90° and 180° tests (2.5%)' 的分母是 40 还是 80 无法确定。）
5. **需作者澄清补充材料编号冲突**：fig. S2 同时被指为"显著性图"（p.5）与"系统设计图"（p.11）；fig. S3 同时被指为"显著性图"（p.5）与"控制协议图"（p.12）；table S4 同时被指为"共享 CNN 架构"（p.11）与"给出 N 的结果表"（p.12）。Algorithm 只出现 S1 与 S4，S2/S3 未被引用。（后果：任何依赖编号的引用都可能指错对象。）
6. **需核实数据可获得性**：p.14 给出的是 **Zenodo badge 链接**（`https://zenodo.org/badge/latestdoi/610810400`、`.../381393816`），**未印出解析后的 DOI**；四份数据集（33.2 GB / 2.3 GB / 14.7 GB / 4.3 GB）托管在**个人 NAS 分享链接**（`http://knightridermit.myqnapcloud.com:8080/share.cgi?...`）而非存档仓库。（后果：P1 若要在论文中写"作者公开了数据"，须先实测链接是否仍可访问并记录访问日期；个人 NAS 链接**不构成长期存档证据**。）
7. **需做 T2 取代检查**（本卡未做，标 `[待核实]`）：检索 2023 年 4 月之后是否有 ① "LNN/CfC 在车规 MCU 或车规 SoC 上的实测部署"、② "LNN/CfC 用于高速公路编队/跟驰控制"、③ 对本文 OOD 结论的独立复现或反例。动作：OpenAlex `cites:<WorkID>` + Crossref + arXiv 检索，记录检索式与日期；若 ① 存在，P1 的"可上 MCU"应改引该文而非本文与 RA-L 2022。
8. **需确认本文 CfC 的具体规模**（神经元数、层宽、是否就是 Fig. 5(D) 所示稀疏电路）：正文只写 "sparsely wired four-layer architecture"（p.2）与共享 CNN 出 128 维特征，"fewer than two dozen LTC neurons"那句指前人 NCP 工作（p.9）。（后果：P1 无法据此建立"OTF-CfC 的规模应取多大"的先验。）

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

| 指标 | 值 | 不确定度 | 出处（表/图/节/页码） |
|---|---|---|---|
| Fly-to-target 闭环成功率（LSTM） | Training Woods 82.5%；Alt. Woods 92.5%；Urban Lawn 62.5%；Urban Patio 27.5% | 未报告（N=40；无 CI、无检验） | Table 1，p.4 |
| Fly-to-target 闭环成功率（GRU-ODE） | 50%；17.5%；32.5%；17.5%（环境顺序同上） | 未报告（N=40） | Table 1，p.4 |
| Fly-to-target 闭环成功率（ODE-RNN） | 62.5%；82.5%；17.5%；25% | 未报告（N=40） | Table 1，p.4 |
| Fly-to-target 闭环成功率（TCN） | 7.5%；0%；0%；0% | 未报告（N=40） | Table 1，p.4 |
| Fly-to-target 闭环成功率（NCP，作者自实现） | 100%；95%；57.5%；52.5% | 未报告（N=40） | Table 1，p.4 |
| **Fly-to-target 闭环成功率（CfC，作者自实现）** | **85%；95%；90%；67.5%** | 未报告（N=40） | Table 1，p.4 |
| 射程测试成功率 @ 10 m（Training Woods） | LSTM 100%；GRU-ODE 70%；ODE-RNN 80%；TCN 5%；NCP 100%；CfC 100% | 未报告（N=10 → 单次成功即 10 个百分点） | Table 2，p.4 |
| 射程测试成功率 @ 20 m（2× 训练距离） | LSTM 0%；GRU-ODE 0%；ODE-RNN 10%；TCN 0%；NCP 50%；**CfC 90%** | 未报告（N=10） | Table 2，p.4 |
| 射程测试成功率 @ 30 m（3× 训练距离） | LSTM 0%；GRU-ODE 0%；ODE-RNN 0%；TCN 0%；NCP 10%；**CfC 20%** | 未报告（N=10） | Table 2，p.4 |
| Fly-to-target 任务定义：起始距离 / 成功判据 / 超时判据 | 起始约 **10 m**；成功 = 稳定在目标 **2 m** 半径内且目标保持在画面中心 **10 s**；失败含目标离开视场不可恢复、**或 30 s 内未到达** | — | p.3（Results） |
| 四测试环境 | Training Woods、Alternative Woods、Urban Lawn、Urban Patio | — | p.3–p.4；Fig. 1(D) 图注 p.3 |
| 压力测试扰动类型与 N | 高斯噪声 / 亮度 / 对比度 / 饱和度；每点 = 10 次运行的均值，误差棒 = SD（N=10）；只喂每段前 **40%** 帧 | SD 已给（N=10） | Fig. 2 图注，p.5；Analysis methodology，p.12 |
| 旋转/遮挡（Urban Lawn，10 m 起点） | 90° 旋转：CfC **仅降 10%**（成功率 >80%）；180°：CfC/NCP/ODE-RNN 维持接近直立时的水平；遮挡：**仅 ODE-RNN 与 NCP 维持名义性能**，GRU-ODE / LSTM / CfC 分别下降 70% / 60% / 30%（CfC 成功率 60%） | 未报告（N 未在正文给出；见 Table S5） | p.6（正文）+ Table S5（**本 .txt 未含**） |
| 旋转测试中受损最重的架构 | GRU-ODE "managing only one success between both the 90° and 180° tests (**2.5%**)" | 未报告（分母 40 还是 80 不明） | p.6 |
| 对抗物徒步（zero-shot hiking with adversaries） | CfC **20 次中完成 14 次**（target horizon = 3）；Discussion 另写 CfC 成功率 **70%**、LSTM 仅 **30%**。TCN 与 GRU-ODE 中 <45% 的运行到达第一个检查点、**无一到达第二个**（原文未区分这两者各自的占比） | 未报告（见 Table S6） | p.6（正文）+ p.8（Discussion）+ Table S6（**本 .txt 未含**） |
| 三角循环（无穷步任务） | 三椅构成边长 **10 m** 等边三角形；检测到检查点后右转 **120°**；实际跑到 **4 圈、共 12 个检查点**后停止 | — | p.7；Fig. 4 图注 p.7 |
| 动目标跟踪（figure-of-eight，6 个检查点） | 相邻检查点相距 **5 m**；LSTM 平均 **5.8** 步；CfC 平均 **8.8** 个检查点（"约长 50%"）；Grass Pitch 上仅 LSTM / NCP / CfC 能锁定目标，CfC 锁定频率为 LSTM 与 NCP 的 **两倍以上** | 未报告（见 table S7） | p.7 + p.8 + table S7（**本 .txt 未含**） |
| 训练数据构成（原始 / 微调 / 合成） | 原始 "devens snowy" **33.2 GB**；微调 "devens chair" **2.3 GB**；合成 "synthetic small4" **14.7 GB**；合成 "synthetic chair" **4.3 GB**；每轮训练含 **5 个目标**，被切分为 5 段独立序列 | — | p.10（Data preparation）+ p.14（Data availability） |
| 合成序列生成参数 | 目标初始横向偏移 **10–70 px**、纵向偏移 **5–40 px**；图像尺寸 **144 × 256 px**；序列长度随机 **120–250 帧**；居中后插入指令速度为零的静帧占序列 **20–35%**；偏航指令 = 横向像素差 × **0.01**，油门 = 纵向偏移 × **0.01**；训练集因此扩大 **>2.5×** | — | p.10–p.11（Data augmentation） |
| 图像增广参数 | 亮度偏移 U(0, **0.4×** 最大像素值)；对比度因子 **0.6–1.4**；饱和度乘法 **0.6–1.4**；高斯噪声均值 0、**SD 0.05** | SD 0.05（噪声参数，非结果不确定度） | p.10–p.11（Data augmentation） |
| 超参搜索 | TPE（Optuna）；以 **40 episodes** 内 train + validation loss 最低者为最终模型；**3 次试验后**按第 10 个 epoch 的中位损失剪枝 | — | p.11（Hyperparameter tuning） |
| 共享感知前端输出维度 | **128 维** CNN 特征 | — | p.11 |
| 机载平台 | DJI M300 RTK + DJI Manifold 2 伴飞计算机（内含 **NVIDIA Jetson TX2**，CPU + GPU）；**Zenmuse Z30** 前向云台相机；ROS；TX2 的 GPU 上跑 **GPU 加速 TensorFlow 2.3.x** | — | p.11（Platform setup / Drone hardware / System design） |
| 网络输出与执行接口 | 期望**线速度与角速度设定点** → DJI 飞控（**黑箱、终端用户不可修改**）跟踪 | — | p.11 |
| 控制频率 / 推理时延 / 内存占用 / 参数量 | **全文未见**（无 Hz、无 ms、无 KB/MB、无参数个数） | — | 全文 grep 零命中；参数量指向 table S3（**本 .txt 未含**） |
| 代码与数据可用性 | Zenodo badge 链接 `https://zenodo.org/badge/latestdoi/610810400` 与 `https://zenodo.org/badge/latestdoi/381393816`，**Apache 2.0**；数据集发布于个人 NAS 分享链接（未印解析后 DOI） | — | p.14（Data and materials availability） |
| 论文时间线 / 卷期 | Submitted **6 May 2022**；Accepted **22 March 2023**；Published **19 April 2023**；*Sci. Robot.* **8(77)**:eadc8892 | — | p.14（末页）+ p.15（引文页） |
| 利益冲突披露 | 部分工作已于 **2022-10-12** 申请临时专利（申请号 **63/415,382**）；R.H. 兼 Vanguard Group，R.S. 兼 Altitude AI，P.K. 兼 Wing，D.R. 兼 Mitre | — | p.13–p.14（Competing interests） |
| 资助 | AI2050 / Schmidt Futures（grant **G22-63172**）、USAF Research Laboratory 与 USAF AI Accelerator（Cooperative Agreement **FA8750-19-2-1000**）、**Boeing**；计算资源：IBM Satori 与 MIT/MIT Lincoln Labs Supercloud | — | p.13（Funding）+ p.14（计算集群致谢） |

**⚠ 内部不一致（逐条列出，引用前必须处理）**
- ⚠内部不一致 1：**p.4 写 "Both variants of liquid networks outperformed other models in terms of task completion."，但 Table 1 的 Urban Lawn 上 NCP = 57.5% < LSTM = 62.5%** —— "两种液态网络在所有环境都优于其他模型"不成立；该段紧接着已自行收窄为 "with a sparse liquid **CfC** network having a success rate of 90% in Urban Lawn"。
- ⚠内部不一致 2：**p.8 写 "When all nonliquid networks failed to achieve the task at twice the nominal distance…"，但 p.4 明写 "Only ODE-RNN managed to achieve a single success at 20 m among the nonliquid networks"，Table 2 中 ODE-RNN @20 m = 10%** —— "全部失败"与"有一次成功"直接冲突。
- ⚠内部不一致 3：**p.6 明写遮挡测试中 "only ODE-RNN and NCP managed to maintain their nominal performance"，CfC 反而下降 30%；但 p.7–p.8 概括为液态网络 "largely outperformed all other models on all of the range tests, the rotation and occlusion robustness tests…"** —— 概括句掩盖了遮挡子任务上 CfC 不如 ODE-RNN/NCP 的事实。
- ⚠内部不一致 4：p.6 "GRU-ODE, LSTM, and CfC saw performance reductions of **70, 60, and 30%**" 的**口径不统一**：以 Table 1 的 Urban Lawn 为基线，GRU-ODE（32.5%）只有"相对下降 70%"（→≈10%）讲得通，CfC（90%）只有"下降 30 个百分点"（→60%，与正文 "success rates at 60%" 一致）讲得通；**两种口径在同一句内互斥**。
- ⚠内部不一致 5：**补充材料编号冲突** —— fig. S2 被同时指为显著性图（p.5）与系统设计图（p.11）；fig. S3 被同时指为显著性图（p.5）与控制协议图（p.12）；table S4 被同时指为共享 CNN 架构（p.11）与"给出 N 的结果表"（p.12）。且正文只引用 Algorithm S1 与 S4。另外，补充材料清单把 "Materials and Methods" 列为补充 PDF 内容，而正文 p.8–p.12 已有独立的 MATERIALS AND METHODS 章，**两处口径重叠，本材料无法判断是同一内容还是增补内容**。
- ⚠内部不一致 6：**Fig. 5(C) 图注把第四层神经元写成重复的 "interneurons"** —— 逐字："It is constructed by four sparsely connected LTC layers called sensory neurons, interneurons, command neurons, and **interneurons**."（第四层应为 motor neurons；本文 p.2 与 p.9 正文均称其为四层结构）。
- ⚠内部不一致 7：**任务条数自相矛盾** —— p.2 以 "Our experiments included the following diverse set of tasks:" 引出 **8 个编号条目**（1 Fly-to-target、2 Range test、3 Stress test、4 Attention profile、5 Target rotation and occlusion、6 Hiking with adversaries、7 Triangular loop、8 Dynamic target tracking），而 p.3 写 "**All seven tasks** were evaluated in closed loop with environments…"。**8 项 vs "seven tasks" 的差额未被作者说明**（可能的调和是把"4 Attention profile"视为分析而非独立任务，但原文把它编号列在任务表中）。

**⚠ 本卡复算（非论文印出值，仅供内部判断，不得写入 P1 稿件）**
- Table 1 的 N=40 → 单次成功 = 2.5 个百分点。量级参考：N=40、观察到 36/40（= 90%）时 Wilson 95% 区间约为 **[77%, 96%]**（半宽 ≈ ±9.5 个百分点）→ 表中 Urban Lawn 的 CfC 90% vs LSTM 62.5% 远超此宽度，而 Training Woods 的 CfC 85% vs LSTM 82.5%、Alt. Woods 的 CfC 95% vs NCP 95% 等相邻差距则落在该宽度内。**本文未做任何检验，故以上只是量级参考，不是本文结论。**
- Table 2 的 N=10 → 单次成功 = 10 个百分点，**该表只宜作方向性证据**（作者自己在 p.7 也只写 "strong evidence" 而非显著性）。
- 作者 Discussion 中 "more than twice" 对应 70%/30% = 2.33×（自洽）；"about 50% longer" 对应 8.8/5.8 = 1.517（自洽）；"4 laps × 3 chairs = 12 checkpoints"（自洽）；"14 of 20" = 70%（自洽）。

**字符数自查**（实测，2026-10-04，工具：PowerShell `[\u4e00-\u9fff]` 正则计数）：
- 摘要 = **247** 中文字符（含标点与拉丁/数字的全字符数为 715）；上限 400 → **未超**。
- 结论 = **284** 中文字符（全字符数 503）；上限 350 → **未超**。
- 方法一句话 = **42** 中文字符（全字符数 83）；上限 60 → **未超**。
- 口径对齐说明：同组已有的 `ral2022-interpretable-flight-ncp.md` 实测为 摘要 339 / 结论 276 / 方法 49（中文字符），本卡与该批口径一致。
