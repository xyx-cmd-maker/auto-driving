# 精读笔记（`deep-paper-reader`）：Closed-form Continuous-time Neural Networks

> ## ⚠ 更正横幅（2026-10-04 追加，**不改本笔记正文**）
>
> **本笔记依据的是 arXiv HTML 版（2106.13898），其中图表编号与 NMI 2022 正式版大面积错位。**
> 照抄本笔记编号写进稿件会指向**完全不同的内容**，属引用失实。
>
> | 本笔记写的 | 正式版实际应引 |
> |---|---|
> | 参数量见 **Table 3** | **Extended Data Fig. 9**（VoR p.21） |
> | Bit-stream XOR 见 **Table 4** | **Extended Data Fig. 5** |
> | PhysioNet 见 **Table 5** | **Extended Data Fig. 6** |
> | IMDB 见 **Table 6** | **Extended Data Fig. 8** |
> | Walker2D 见 **Table 7** | **Table 3** |
> | 紧致性验证 **Fig. 3** | **Fig. 2** |
> | 注意力剖面 **Fig. 5** | **Extended Data Fig. 10** |
> | 超参 **Tables S1–S4** | 正式版无此物 → **Extended Data Figs. 3 / 4 / 7** |
>
> 另 3 处事实需更正：① 正式版题名为 `Closed-form continuous-time neural **networks**`（不是 "Neural Models"）；② 真车试验路段是**乡村道路**（两版全文 `highway` 0 命中），不是高速公路；③ 本文**确有正式更正**：`Publisher Correction, NMI 4(12):1267, 2022-11-29, DOI 10.1038/s42256-022-00597-y`（Crossref `update-to` 指向正文），更正内容尚未取得。
>
> **以正式版为准的新精读卡**：[`../meeting2/notes/cfc-nmi2022.md`](../meeting2/notes/cfc-nmi2022.md)（含正式版全量编号、`ED Fig. 9` 参数量**读图核验结果**、以及本笔记 → 正式版的完整映射表 Q8）。
> **本笔记其余内容（主张—证据台账、方法可复现性清单、统计旗标、红队三条、限制）继续有效**，但引用任何图表编号前**必须先查上表**。

文献：Hasani R, Lechner M, Amini A, Liebenwein L, Ray A, Tschaikowski M, Teschl G, Rus D. "Closed-form continuous-time neural networks". *Nature Machine Intelligence* 2022;4(11):992–1003. DOI 10.1038/s42256-022-00556-7
被精读全文：`auto-driving/literature/fulltext/p01-cfc-nmi2022.txt`（引文题名 "Closed-form Continuous-time Neural Models"）
全文来源：**已获全文**（纯文本约 6.5 万字符）。抓取来源 `SOURCE_URL: https://arxiv.org/html/2106.13898`，`FETCH_DATE: 2026-10-02`。
精读日期：2026-10-02 ｜ 编号：#1（P1 文献图）｜ 技能：`deep-paper-reader`
**版本警示（贯穿全篇）**：本笔记全部数字与图/表号来自 **arXiv HTML 版（2106.13898）**，**未与 NMI 2022 正式版逐字比对**；正式版的图表编号与数值可能不同。凡本笔记标注"出处"处，均指 arXiv HTML 版的编号。

---

## 作用域

**场景①：项目内文献工作**（`deep-paper-reader` §1 前置条件二）。

- **项目**：`D:\Deepseek Harness\auto-driving`（自动驾驶 OTF 论文集群）。
- **项目不变量文件**：`D:\Deepseek Harness\auto-driving\AGENTS.md`。
- **本次精读服务的主张**：论文 1（P1，代号 **OTF-CfC**）——「基于超车频次势场与液态神经网络的高速主线编队连续时间控制」。
- **P1 的主张上限（`AGENTS.md` §1 原文引用，逐条对本次精读生效）**：
  1. 「**P1 红线**：不得预先声称"OTF 势场带来 X% 性能提升"。」——学位论文报告的分类器准确率增益 +1.0 ~ +5.5 个百分点属"**论文报告值，未经我们复现**"，在 LNN 控制范式下**未经本项目实测即属 C/D 级证据**。
  2. 「**不得把仿真/回放写成实车验证**：CARLA（Town04）与实车数据回放都是仿真或开环证据。未做真车闭环前，措辞上限是"在 CARLA 与真实数据回放中"。」
  3. 「**不得直接搬用他人论文数字**：与 DriveDreamer 等对比若未同协议复现，必须标注"**文献报告值，协议不同，不可直接比较**"。」
- **本笔记的定位**：CfC 是 P1 的**控制器选型**候选；P1 需要证明的命题是「用 CfC 做 **100 Hz 连续控制**、参数量 **< 500 KB**、**可上 MCU**」，且 P1 的**消融 A2 = LNN vs CfC vs 普通 ODE-RNN**。因此本笔记的任务是**准确记录这篇论文的主张在什么条件下成立**，尤其记录它的**硬件条件、闭环条件与参数量口径**。
- **本笔记不做什么**：不评价该工作的重要性与新颖性；不做外部引文检索（§二 外部复现列一律"未检"）；不把本文的序列建模结论升格为控制结论。

---

## 一、作者主张

作者主张：他们为 liquid time-constant networks（LTC）动力学中一个此前无已知闭式解的积分给出了**紧致有界的闭式近似**（Theorem 1 / Lemma 1，式 (2)(8)），其误差以 $|x(0)-A|e^{-w_\tau t}$ 为上界且该界是 sharp 的；据此把该近似"蒸馏"成可规模训练的 **Closed-form Continuous-depth（CfC）** 网络（式 (10)，由共享 backbone 分出 $f$、$g$、$h$ 三个 head，用 $\sigma(-[f]\cdot t)$ 与 $1-\sigma(-[f]\cdot t)$ 做时间连续门控），从而**不再需要 ODE 求解器**；由此作者主张 CfC 在**训练与推理上比基于微分方程的对应模型快一至五个数量级**、在**不规则采样**的时间序列上（bit-stream XOR 事件编码、PhysioNet 2012、MuJoCo Walker2d-v2）**保持或超过**包括 ODE-RNN、ODE-LSTM、CT-RNN、GRU-D、Transformer 在内的先进基线，并在**真实车辆的高速公路/乡村车道保持**任务上以约 4k 的 RNN 参数完成端到端驾驶、且在输入噪声下保持一致的注意力剖面。作者同时给出适用边界：CfC 只近似 ODE，因而**不再保证双射**，不适合依赖可逆性的生成建模；可能出现**梯度消失**，长时程依赖任务建议改用混合记忆版本 CfC-mmRNN；并在讨论中把"闭环性能重要的场合"与"嵌入式应用"列为 CfC 的适用场景（以引文支撑，非本文实验）。

---

## 二、主张—证据台账

内部等级：`A_int`（预注册+对照/识别+足够功效+效应量与 CI+内部独立重复）/ `B_int`（设计良好但有边界）/ `C_int`（相关/仿真/单例）/ `D_int`（假设）。
外部复现：**本次一律"未检"**（未做引文检索）；按 `deep-paper-reader` §3.1.1，"未检"是信息缺失，**不等于"无外部证据"**。

| # | 作者主张（原句摘录，英文原句） | 支撑证据（图/表/统计量，写图号表号） | 内部等级 | 外部复现 | 是否被结果支撑 | 缺口 |
|---|---|---|---|---|---|---|
| 1 | "the following expression is an approximation of its closed-form solution … Then, $|x(t)-\tilde{x}(t)|\leq|x(0)-A|e^{-w_{\tau}t}$ for all $t\geq 0$ … The first statement implies in particular that our bound is sharp." (Theorem 1, Lemma 1) | 式 (2)(5)(8)；Lemma 1 的 sup/inf 两条 sharpness 结论；完整证明见 Supplementary Materials "Proof of Lemma 1" | **B_int** | 未检 | 是（演绎） | 证明只覆盖**标量单细胞**情形：`constructed by one cell, receiving a single dimensional time-series input I with no self connections`；不含 CfC（式 10）的多维门控网络。A_int 的"预注册/功效/CI"框架不适用于演绎结论，故不授 A_int，避免下游误读为"已有外部复现" |
| 2 | "we observed that the behavior of the ODE is captured with a **mean-squared error of 0.006** by the closed-form solution. This experiment is an empirical evidence for the tightness results presented in our theory." | Fig. 3 + §Tightness of the Closed-form Solution in Practice；对象 = 训练好的 NCP（19 neurons, 253 synapses），车道保持，真实路测记录 | **C_int** | 未检 | 是（就所报范围） | 单网络、单标量指标、**无单位、无 CI、无重复次数、无时间步数**；只验证 LTC 的闭式替身（Fig. 2c 形式），**不验证式 (10) 的 CfC 架构** |
| 3 | "we obtain models that are **between one and five orders of magnitude faster** in training and inference compared to differential equation-based counterparts." (Abstract) / "CfCs perform computations **at least one order of magnitude** faster training and inference time compared to their ODE-based counterparts, without loss of accuracy." | Abstract；§Explicit Time Dependency（Table 1 复杂度表）；Fig. 3 图注（"at least 100x faster than neural ODEs at both training and inference"）；Table 4 / Table 5 / Table 7 的 "Time Per epoch (min)" 列 | **D_int** | 未检 | **部分**：本全文表格中可追溯的最大加速为 **220×**（Table 5, Latent-ODE-ODE 22.0 min → CfC 0.1 min），最小约 **3×**；**"five orders of magnitude"（10^5×）在本全文任何表/图中找不到对应测量** | "without loss of accuracy" 是等价性断言，**无等价/非劣检验**；速度列为单值，**无方差、无重复次数、无硬件** |
| 4 | "CfCs perform competitively to other baselines while performing **160 times faster training time compared to ODE-RNNs and 220 times compared to continuous latent models**. CfCs are also, **on average, three times faster** than advanced discretized gated recurrent models." | §PhysioNet Challenge；Table 5 的 time per epoch：CfC 0.1；ODE-RNN 16.5；Latent-ODE-RNN 6.7；Latent-ODE-ODE 22.0；离散门控 RNN-Impute 0.5 / RNN-delta-t 0.5 / RNN-Decay 0.7 / GRU-D 0.7 / Phased-LSTM 0.3 | **C_int** | 未检 | **部分**：16.5/0.1 = **165×**（正文写 160×，量级一致，绝对数字对不上）；22.0/0.1 = **220×** ✓；**"three times" 无法从 Table 5 复算**——该组五个离散门控基线与 CfC 的比值区间为 3×–7×，均值比 ≈ 5.4×；"three times" 只等于其中最快基线（Phased-LSTM 0.3）的比值 | 口径不明（是取最小值、均值还是不同基线集合）；速度无方差 |
| 5 | "when considering **accuracy-per-compute time, CfCs exhibit over 150× improvement**." | §CfCs: Flexible Deep Models for Sequential Tasks（单句陈述） | **D_int** | 未检 | **否**：本文**无任何图/表/统计量**支撑该数字；"accuracy-per-compute time" 的定义、聚合方式、覆盖数据集均未给出 | 无证据指针，不可引用 |
| 6 | "CfCs are very parameter efficient. They performed the end-to-end autonomous lane keeping task with **around 4k trainable parameters in their recurrent neural network component**." / "CfC and NCP networks perform lane-keeping in unseen scenarios with a compact representation." | **Table 3**（Lane-keeping models' parameter count）：CfC 总参数 **230,828**、RNN 分量 **4,184**；NCP 233,139 / 6,495；Cf-S 227,728 / 1,084；LSTM 259,733 / 33,089；CfC-mmRNN 235,052 / 8,408；纯 CNN 2,124,901 | **B_int**（确定性计数） | 未检 | 是（4k 对应 RNN 分量 4,184） | **"4k" 只是 RNN 分量**，全模型（CNN head + RNN）为 230,828，是"4k"的 **55 倍**；Table 3 是**全文唯一的参数量表**，且只覆盖车道保持模型——四个基准数据集（XOR / PhysioNet / IMDB / Walker2D）**没有任何参数量或 FLOPs 报告** |
| 7 | "After training, all networks were transferred on-board our full-scale autonomous vehicle (Lexus RX450H …). … we observed that **all trained networks were able to successfully complete the lane-keeping task** at a constant velocity of 30 km/hr." / "CfCs similar to NCPs demonstrate a consistent attention pattern in each subtask, while maintaining their attention profile under heavy noise." | §How well CfCs perform in autonomous driving；Fig. 5(a)(b)(c)，噪声为零均值高斯 $\sigma^{2}=0.35$；Table 3（仅参数量）。设施：30 Hz BlackFly PGE-23S3C RGB、3 小时原始数据 + 特权控制器/视图合成增广、1 km 私有测试路、无标注车道线、人类安全员可接管 | **C_int** | 未检 | **定性/断言级**：**未报告任何量化闭环指标** | 无成功率、无接管率/次数、无每模型试验次数、无转向误差、无里程明细；因此**无法在 CfC / NCP / LSTM / CNN 之间做任何定量比较**（Table 3 只是参数量）。这是本文**唯一**的真车闭环实验，却只产出参数量与注意力可视化 |
| 8 | "However, when the bit-stream samples arrive at non-uniform distances, only architectures that are immune to the vanishing gradient in irregularly sampled data can solve the task. These include GRU-D, ODE-LSTM and CfCs, and CfC-mmRNNs." | **Table 4**（Bit-stream XOR，mean ± SD, n=5）：Event-based（irregular）——CfC **99.42% ± 0.42**、CfC-mmRNN **99.72% ± 0.08**、CfC-noGate 96.29% ± 1.61、Cf-S 85.42% ± 2.84、ODE-LSTM 98.89% ± 0.26、GRU-D 97.90% ± 1.71、ODE-RNN 51.21% ± 0.37、CT-RNN 50.79% ± 0.34、GRU-ODE 52.52% ± 0.35、LTC 49.11% ± 0.00；Equidistant 下多模型 100.00% ± 0.00 | **B_int** | 未检 | 是（方向一致） | 任务为玩具级（bit-stream XOR）；**绝大多数 baseline 数字取自 [9] 而非本文重跑**（表注："The performance values for all baseline models are reproduced from [9]"），且 **baseline 超参数未给出**；无显著性检验 |
| 9 | "**ODE-based RNNs cannot solve the event-based encoding tasks regardless of their choice of solvers**, as they have vanishing/exploding gradient issues [9]." | 同 §Regularly and Irregularly-Sampled Bit-Stream XOR | **D_int** | 未检 | **否（与本文自己的 Table 4 冲突）** | Table 4 中标记为 ODE-based = "Yes" 的 **ODE-LSTM 在 event-based 编码下取得 98.89% ± 0.26**，而同段前一句又写 "These include GRU-D, ODE-LSTM and CfCs" ——**同一段内自相矛盾**；"regardless of their choice of solvers" 亦无法从表中推出（表中未做 solver 消融） |
| 10 | "As shown in Table 7, CfCs outperform the other baselines by a large margin … CfCs even **outperform Transformers by a considerable 18% margin**." | **Table 7**（Walker2D，squared error，mean ± SD, n=5）：CfC-mmRNN **0.617 ± 0.006**、CfC **0.643 ± 0.006**、CfC-noGate 0.650 ± 0.008、LTC 0.662 ± 0.013、Transformer 0.761 ± 0.032、ODE-LSTM 0.883 ± 0.014、Cf-S 0.948 ± 0.009、CT-LSTM 1.014 ± 0.014、ODE-RNN 1.904 ± 0.061、Lipschitz RNN 1.781 ± 0.013、coRNN 3.241 ± 0.215 | **B_int** | 未检 | 是（方向一致，CfC 优于 Transformer） | **"18% margin" 的基数未定义**：若按"Transformer 误差相对 CfC 高多少"= 0.761/0.643 − 1 = **+18.35%**；若按"绝对误差下降"= (0.761−0.643)/0.761 = **15.5%**；若换成 CfC-mmRNN 则为 **+18.9% 绝对 / +23.3% 相对**。速度优势在此任务上仅约 **10×**（ODE-RNN 0.79 → CfC 0.08 min/epoch），远非 100× |
| 11 | "We observe that CfCs perform competitively to other baselines" (PhysioNet) / "at least one order of magnitude faster … without loss of accuracy" | **Table 5**（PhysioNet AUC，mean ± SD, n=5）：CfC-noGate **0.840 ± 0.003**、CfC **0.839 ± 0.002**、CfC-mmRNN 0.834 ± 0.006、Phased-LSTM 0.836 ± 0.003、ODE-RNN 0.833 ± 0.009、Latent-ODE-ODE 0.829 ± 0.004、GRU-D 0.818 ± 0.008、IP-Nets 0.819 ± 0.006、SeFT 0.795 ± 0.015、Cf-S **0.643 ± 0.018**、LTC **0.6477 ± 0.010** | **B_int** | 未检 | 是（数值上不低于最强基线） | CfC 0.839 vs Phased-LSTM 0.836 差 **0.003**，与两者 SD（0.002/0.003）同量级 → **"无损失"是未做等价检验的断言**；标 †/* 的基线取自 [7]/[44]，非本文重跑 |
| 12 | "Table 6 represents how **CfCs equipped with mixed memory instances outperform advanced RNN benchmarks**." | **Table 6**（IMDB test accuracy %，mean ± SD, n=5）：CfC-mmRNN **88.3 ± 0.1**、HiPPO-LagT 88.0 ± 0.2、HiPPO-LegS 88.0 ± 0.2、LMU 87.7 ± 0.1、CfC-noGate 87.5 ± 0.1、LSTM 87.3 ± 0.4、coRNN 86.7 ± 0.3、GRU 86.2 ± n/a、**CfC 85.9 ± 0.9**、expRNN 84.3 ± 0.3、Cf-S 81.7 ± 0.5、Vanilla RNN 67.4 ± 7.7、LTC **61.8 ± 6.1** | **B_int**（仅对 CfC-mmRNN） | 未检 | 是（仅对 mmRNN 变体） | **vanilla CfC（85.9 ± 0.9）低于 LSTM（87.3）、LMU（87.7）、HiPPO（88.0）**；标题句用"CfCs"代表 mmRNN 变体，**口径混淆** —— 下游若引用"CfC 在 IMDB 超过 LSTM"即失实。另：LTC 61.8 ≈ 二分类随机水平（50%），与 Table 5 的 LTC 0.6477 一样异常低，作者未解释 |
| 13 | "For large-scale time-series prediction tasks, and **where closed-loop performance matters [24] CfCs should be the method of choice**." | §Scope, Discussions and Conclusions；唯一支撑是引文 [24]（Vorbach et al., *Causal navigation by continuous-time neural networks*, arXiv:2106.08314） | **D_int** | 未检 | **否**（本文实验不支持） | 本文**没有任何闭环控制性能实验**；同段紧接着写 "implicit ODE-based models can still be significantly beneficial in solving continuously defined physics problems and **control tasks**" —— 对控制任务**内部口径自相矛盾**（一处说闭环选 CfC，一处说控制任务 ODE 模型仍有优势） |
| 14 | "we use CfCs when: … 2) training and inference efficiency of a model is important (e.g., **embedded applications** [69, 70, 71])" | §Scope, Discussions and Conclusions；支撑为引文 [69]（模拟集成电路建模）、[70]（在制品质量预测）、[71]（肌电/脑电监督控制） | **D_int** | 未检 | **否**（本文实验不支持） | 全文**无任何 MCU / 嵌入式 / 实时性实测**：无内存占用（KB）、无单步时延、无功耗、无目标平台、无编译器/量化档位。且全文（grep 全文）**未出现任何硬件字样**（无 GPU/CPU 型号、无精度、无批大小） |

**台账整体判读（仅记录，不评价重要性）**：本文的**可复核量化证据集中在四个开环序列建模基准**（Tables 4–7，n=5，mean ± SD，全部有 SD）；**唯一的真车闭环实验（§autonomous driving + Fig. 5 + Table 3）不产出任何闭环性能数字**；**速度主张（Abstract "one to five orders of magnitude"、§150×）在本文图表中不可追溯**，可追溯区间为 3×–220×；**参数量主张只覆盖车道保持模型**。

---

## 三、方法可复现性清单

| 项 | 论文是否给出 | 具体位置 | 缺失影响 |
|---|---|---|---|
| 数据来源与版本 | **部分给出** | XOR：[9] Lechner & Hasani 2020；PhysioNet：Challenge 2012，8000 ICU 患者、37 特征、入院后前 48 小时（§PhysioNet Challenge）；IMDB：25,000 训练 + 25,000 测试（§Sentiment Analysis）；Walker2D：MuJoCo `Walker2d-v2` OpenAI Gym，四种随机策略（§Physical Dynamics Modeling）；车道保持：30 Hz BlackFly PGE-23S3C 采集的 3 小时自采数据（§autonomous driving） | 四个公开基准**无版本号/下载日期/校验和**；Walker2D 未给轨迹条数与划分；车道保持自采数据**未说明是否公开、无 Datasheet** → 无法判断数据可比性与偏差 |
| 预处理与划分 | **部分给出** | IMDB：word-by-word 分词、20,000 词表、可训练 embedding、随机初始化、无预训练（§Sentiment Analysis）；PhysioNet："We perform the **same test-train split and preprocessing as [7]**"（§PhysioNet Challenge）；XOR/Walker2D：未描述 | PhysioNet 的划分**转引 [7] 而非复述** → 若 [7] 的划分有随机成分，本文结果不可独立重建；XOR/Walker2D 的缺失使"不规则采样"的处理细节（掩码、Δt 输入、缺失值填充）不可复现 |
| 模型规格与参数量 | **部分给出** | 架构：式 (10) + Fig. 4（backbone 分 $f$/$g$/$h$ 三 head）；每数据集每变体的 hidden size / backbone_units / backbone_layers 见 **Table S1–S4**；参数量：**仅 Table 3**（且只覆盖车道保持模型） | **四个基准数据集没有任何参数量/FLOPs 报告** → 无法判断 CfC 的准确率增益是否来自更大模型；Table 3 中 CfC-NoGate 与 CfC 参数量完全相同（230,828 / 4,184），无法从参数角度区分两变体 |
| 超参数与搜索空间 | **部分给出（有值，无协议）** | Table S1（XOR）、S2（PhysioNet）、S3（IMDB）、S4（Walker2D）：clipnorm、optimizer、batch_size、Hidden size、epochs、base_lr、decay_lr、backbone_activation、backbone_dr、backbone_layers、backbone_units、weight_decay、forget_bias、class_weight、init、embed_dim | **只给最终取值，不给搜索空间、搜索算法、选择准则、调参预算**；也未说明是否对 baseline 做了同等预算的调参 → **无法判断公平性**（P1 `AGENTS.md` §3 要求"同等调参预算"） |
| 随机种子 / 重复次数 | **未给出** | Table 4/5/6/7 表注均写 "Numbers present mean ± standard deviations, **n=5**"；**全文（grep）无 "seed" 一词**；车道保持实验**无任何重复次数** | 无种子列表 → 5 次重复不可复现、方差不可复算；**速度列（Time Per epoch）为单值，未说明是否重复** → 加速比没有不确定度；车道保持无试验次数 → 无法判断"all networks completed"是几次尝试的结果 |
| 评价指标定义（含边界情况） | **部分给出** | XOR：accuracy（Table 4）；PhysioNet：AUC on the test set（§PhysioNet Challenge）；IMDB：test accuracy（Table 6）；Walker2D：squared error on the test set（§Physical Dynamics Modeling）；**车道保持：未定义任何指标** | 四个指标的**计算方法、聚合窗口、早停准则均未给**；PhysioNet 类别极不平衡（Table S2 给了 `class_weight` 5.91–18.25）但**未说明 AUC 是否按权重/如何取样**；车道保持无指标定义 → 该实验不可能被复现或比较 |
| 基线实现来源 | **给出，但大多数不是本文实现** | 表注：Table 4 "The performance values for all baseline models are **reproduced from [9]**"；Table 5 "marked by † are reported from **[7]** and the ones with ∗ from **[44]**"；Table 6 "marked by † are reported from **[40]**, and ∗ from **[42]**"；Table 7 "marked by † are reported from **[9]**" | **CfC 与 baseline 的对比大部分是跨论文拼接**：不同代码库、不同划分、不同硬件、不同调参预算 —— 这正是 P1 主张上限第 3 条禁止的"直接搬用他人论文数字"的情形。**Table 4 中 ODE-LSTM 98.89% 与 CfC 99.42% 的差距（0.53 个百分点）是否超出跨论文协议差异，本文未做任何论证** |
| 显著性检验 | **未给出** | 全文无 p 值、无检验名称、无置信区间（grep 全文无 significan/confidence/p-value） | 无法判断 CfC 与最强基线的差距（如 Table 5 的 0.839 vs 0.836）是否超过随机波动；台账第 11 条因此只能给 B_int |
| 代码/数据可用性 | **给出（代码）** | Acknowledgments 段："All data, code, and materials used in the analysis are openly available at **https://github.com/raminmh/CfC** under **Apache 2.0 License**" | 车道保持自采数据（3 小时 + 增广）与真车试验记录**未包含在该声明中**（"All data" 与实际可得的公开基准之间存在落差）→ 真车实验不可复现 |

---

## 四、关键数字表

> 纪律：下列数字**全部抄自论文明确印出的表格/正文**；图 3 的 MSE 为正文印出值；无一处为目测估读。速度列的 "Time per epoch (min)" 为论文印出的单值。

| 指标 | 值 | 不确定度（CI/SD/SE，没有就写"未报告"） | 出处（表/图/节） | 备注（哪个数据集/哪个设置） |
|---|---|---|---|---|
| 闭式近似 vs ODE 神经元轨迹的 MSE | 0.006 | 未报告（无单位、无 n、无 CI） | Fig. 3 + §Tightness of the Closed-form Solution in Practice | 训练好的 NCP（19 neurons, 253 synapses）车道保持网络，真实路测记录 |
| Bit-stream XOR accuracy（equidistant） | CfC 100.00% ± 0.00 | SD = 0.00（n=5） | Table 4 | 规则采样（等距）编码 |
| Bit-stream XOR accuracy（event-based, irregular） | CfC **99.42%** ± 0.42；CfC-mmRNN **99.72%** ± 0.08；CfC-noGate 96.29% ± 1.61；Cf-S 85.42% ± 2.84 | SD 如列（n=5） | Table 4 | 事件式（不规则）编码 |
| Bit-stream XOR accuracy（最强非 CfC 基线） | ODE-LSTM **98.89%** ± 0.26；GRU-D 97.90% ± 1.71 | SD 如列（n=5） | Table 4 | ODE-LSTM 标 ODE-based = Yes |
| Bit-stream XOR accuracy（纯 ODE 基线，≈随机） | ODE-RNN 51.21% ± 0.37；CT-RNN 50.79% ± 0.34；GRU-ODE 52.52% ± 0.35；**LTC 49.11% ± 0.00** | SD 如列（n=5） | Table 4 | 同上 |
| XOR time per epoch | CfC **0.75 min**；CfC-mmRNN 1.26；Cf-S 0.36；CfC-noGate 0.78；ODE-LSTM 1.18；ODE-RNN 4.11；LTC 2.67 | **未报告**（单值） | Table 4 | CPU/GPU 未说明 |
| PhysioNet AUC | CfC-noGate **0.840** ± 0.003；CfC **0.839** ± 0.002；CfC-mmRNN 0.834 ± 0.006 | SD 如列（n=5） | Table 5 | PhysioNet Challenge 2012，8000 ICU 患者，不规则采样（时间与特征双缺失） |
| PhysioNet AUC（基线） | Phased-LSTM 0.836 ± 0.003；ODE-RNN 0.833 ± 0.009；Latent-ODE-ODE 0.829 ± 0.004；GRU-D 0.818 ± 0.008 | SD 如列（n=5） | Table 5 | 同上 |
| PhysioNet AUC（闭式解原始形态 Cf-S / LTC） | Cf-S **0.643** ± 0.018；LTC **0.6477** ± 0.010 | SD 如列（n=5） | Table 5 | 同上；**Cf-S 是式 (9) 的直接实例化，明显劣于所有基线** |
| PhysioNet time per epoch | CfC **0.1 min**；CfC-mmRNN 0.2；Cf-S 0.1；ODE-RNN **16.5**；Latent-ODE-RNN 6.7；Latent-ODE-ODE **22.0**；Phased-LSTM 0.3；GRU-D 0.7 | **未报告**（单值） | Table 5 | 由表可复算：CfC/ODE-RNN = 165×；CfC/Latent-ODE-ODE = 220× |
| IMDB test accuracy | CfC-mmRNN **88.3%** ± 0.1；CfC-noGate 87.5% ± 0.1；**CfC 85.9%** ± 0.9；Cf-S 81.7% ± 0.5；LTC **61.8%** ± 6.1 | SD 如列（n=5） | Table 6 | 25,000/25,000 划分，20k 词表，无预训练 |
| IMDB test accuracy（最强非 CfC 基线） | HiPPO-LagT 88.0% ± 0.2；HiPPO-LegS 88.0% ± 0.2；LMU 87.7% ± 0.1；**LSTM 87.3%** ± 0.4 | SD（LSTM/LMU/HiPPO 为 n=5；GRU "± n/a"） | Table 6 | 标 † 者取自 [40] |
| Walker2D squared error | CfC-mmRNN **0.617** ± 0.006；CfC **0.643** ± 0.006；CfC-noGate 0.650 ± 0.008 | SD 如列（n=5） | Table 7 | MuJoCo Walker2d-v2，四种随机策略，不规则采样 |
| Walker2D squared error（基线） | LTC 0.662 ± 0.013；**Transformer 0.761** ± 0.032；ODE-LSTM 0.883 ± 0.014；Cf-S 0.948 ± 0.009；ODE-RNN 1.904 ± 0.061 | SD 如列（n=5） | Table 7 | 同上；无 pretraining |
| Walker2D time per epoch | CfC **0.08 min**；Cf-S 0.12；CfC-mmRNN 0.34；ODE-RNN **0.79**；Transformer 0.8；LTC 0.78 | **未报告**（单值） | Table 7 | 由表可复算：CfC 相对 ODE-RNN 仅约 **9.9×** |
| 车道保持模型总参数量（CNN head + RNN） | CfC **230,828**；CfC-NoGate 230,828；CfC-mmRNN 235,052；NCP 233,139；Cf-S 227,728；LSTM 259,733；纯 CNN 2,124,901 | 未报告（确定性计数，无需不确定度） | Table 3 | 车道保持任务；CNN head 恒为 226,644（可从表内复算，五组一致） |
| 车道保持模型 RNN 分量参数量 | CfC **4,184**；CfC-NoGate 4,184；CfC-mmRNN 8,408；NCP 6,495；Cf-S 1,084；LSTM 33,089 | 未报告（确定性计数） | Table 3 | 正文"around 4k trainable parameters in their recurrent neural network component"对应此列 |
| 真车车道保持试验规模 | 1 km 私有测试路；30 km/hr 恒速；3 小时原始数据 + 增广；30 Hz 相机 | **未报告**（无试验次数、无接管次数、无成功率、无转向误差） | §How well CfCs perform in autonomous driving | Lexus RX450H，drive-by-wire；安全员在越出车道时接管 |
| 真车试验的输入噪声设置 | 零均值高斯噪声，方差 $\sigma^{2}=0.35$ | 未报告（无重复、无各模型对比数字） | Fig. 5(c) | 仅用于注意力可视化对比 |
| 声称的训练/推理加速区间 | "between one and five orders of magnitude" | **未报告** | Abstract | **本文表格中不可追溯**：可复算区间为约 3×–220× |
| 声称的 accuracy-per-compute time 改进 | "over 150×" | **未报告** | §CfCs: Flexible Deep Models for Sequential Tasks | **无对应图/表** |
| 声称的 vs Transformer 优势 | "18% margin" | 未报告 | §Physical Dynamics Modeling | 基数未定义；复算见 §数字口径对照表 |
| 声称的 PhysioNet 加速 | "160 times"（vs ODE-RNN）、"220 times"（vs continuous latent models）、"on average three times"（vs discretized gated） | 未报告 | §PhysioNet Challenge | 前两者可从 Table 5 复算（165× / 220×）；"three times" 复算不出（见下） |

### 数字口径对照表

> 触发条件满足：同一指标在本文中出现 ≥2 个数值（不同数据集 / 不同编码 / 不同变体 / 不同"参数"定义）。

| 指标 | 数值 | 数据集 / 划分 | 变体 / 任务 | 其他设置 | 出处 |
|---|---|---|---|---|---|
| Bit-stream XOR accuracy | 100.00% ± 0.00 | XOR | CfC，equidistant 编码 | 规则采样 | Table 4 |
| Bit-stream XOR accuracy | 99.42% ± 0.42 | XOR | CfC，event-based 编码 | 不规则采样 | Table 4 |
| Bit-stream XOR accuracy | 99.72% ± 0.08 | XOR | **CfC-mmRNN**，event-based | 不规则采样 | Table 4 |
| 加速比（相对 ODE-RNN） | 165×（正文写 160×） | PhysioNet | CfC | 16.5 / 0.1 min per epoch | Table 5 + §PhysioNet |
| 加速比（相对 ODE-RNN） | ≈9.9× | Walker2D | CfC | 0.79 / 0.08 min per epoch | Table 7 |
| 加速比（相对 ODE-RNN） | ≈5.5× | XOR | CfC | 4.11 / 0.75 min per epoch | Table 4 |
| 加速比（相对 Latent-ODE-ODE） | 220× | PhysioNet | CfC | 22.0 / 0.1 min per epoch | Table 5 |
| 加速比（区间声称） | "one to five orders of magnitude"（10×–10^5×） | 全部 | CfC | **无出处** | Abstract |
| 加速比（单点声称） | "over 150×"（accuracy-per-compute time） | 未指明 | CfC | **无出处、无定义** | §CfCs: Flexible Deep Models |
| 参数量 | **4,184**（"around 4k"） | 车道保持 | CfC，**仅 RNN 分量** | CNN head 另计 226,644 | Table 3 + §autonomous driving |
| 参数量 | **230,828** | 车道保持 | CfC，**CNN head + RNN 全模型** | 同上 | Table 3 |
| vs Transformer 优势 | +18.35%（相对：0.761/0.643−1） | Walker2D | CfC | 作者的"18% margin"最大的可能口径 | 由 Table 7 复算 |
| vs Transformer 优势 | 15.5%（绝对：(0.761−0.643)/0.761） | Walker2D | CfC | 若按"误差下降百分比" | 由 Table 7 复算 |
| vs Transformer 优势 | 18.9% 绝对 / 23.3% 相对 | Walker2D | **CfC-mmRNN**（0.617） | 若"CfCs"指 mmRNN 变体 | 由 Table 7 复算 |
| CfC 在 IMDB 的表现 | 85.9% ± 0.9（**低于 LSTM 87.3%**） | IMDB | **vanilla CfC** | 随机初始化 embedding，无预训练 | Table 6 |
| CfC 在 IMDB 的表现 | 88.3% ± 0.1（**高于所有基线**） | IMDB | **CfC-mmRNN** | 同上 | Table 6 |
| 加速比（vs discretized gated） | "on average three times" | PhysioNet | CfC | **按 Table 5 复算：比值区间 3×–7×，组均值比 ≈5.4×**；"three times" 仅等于最快基线 Phased-LSTM（0.3）的比值 | §PhysioNet Challenge vs Table 5 |

---

## 五、统计与推断旗标

| 检查项 | 判定 | 具体位置与说明 |
|---|---|---|
| 是否做显著性检验 | **否** | 全文（grep 全文）无 p 值、无检验名称、无 CI。Tables 4–7 仅给 mean ± SD。**9 个 CfC 变体 × 约 20 个基线 × 4 个数据集，全部比较均未做检验** |
| 是否报 CI | **否** | 全部为 SD（n=5），无任何 95% CI；**速度列连 SD 都没有（单值）**；Fig. 3 的 MSE 0.006 无任何不确定度 |
| 是否单种子 | **不是单次（精度列）**；**但种子未报告** | Tables 4–7 表注均写 "n=5"；**全文无 "seed" 一词** → 5 次重复的种子、是否共用种子、方差是 run-to-run 还是 seed-to-seed 均不明。**速度列为单值，"n=5" 是否覆盖速度列未说明**。车道保持真车实验**无重复次数报告** → 该实验事实上是单例 |
| 是否多重比较未校正 | **是（未校正）** | 4 个数据集 × 4 个 CfC 变体 × 约 20 个基线 = 数十次两两比较，无任何校正；且**大部分基线数字来自其他论文**，连"同一次实验内的比较"都不成立，校正更无从谈起 → **膨胀的假阳性风险 / 跨协议不可比风险** |
| 是否把"无显著"写成"无差异" | **是（存在等价性断言）** | §Explicit Time Dependency: "at least one order of magnitude faster … **without loss of accuracy**" —— 这是**等价性断言，未做等价/非劣检验**。最尖锐处：Table 5 中 CfC 0.839 ± 0.002 vs Phased-LSTM 0.836 ± 0.003，差值 0.003 与 SD 同量级，既不能证明更优也不能证明等价。**判为推断错误（口径过强）** |
| 是否把相关写成因果 | **部分（有 1 处）** | §Design a Closed-form Continuous-depth Model: "Through the shared backbone a coupling between time-constant of the system and its state nonlinearity get established that **exploits causal representation learning** evident in a liquid neural network [1, 24]" —— 以架构先验声称因果表征学习收益，**无因果识别设计、无干预、无对照**。正面之处：§Scope 对同一话题明确写 "we **speculate** that inferring causality from ODE-based networks might be more straightforward"，该处已恰当标注为推测 |
| 效应量是否存在 | **部分** | 提供了绝对差值（accuracy/AUC/平方误差之差）与相对差（"18% margin"、"165×"），但**无标准化效应量、无 CI**；且**"18% margin" 的基数未定义**（见 §数字口径对照表） |
| 缺数据如何处理 | **部分说明** | PhysioNet 的缺失（时间与特征双缺失）通过"same preprocessing as [7]"转引，本文未复述；Table S2 给了 `class_weight`（5.91–18.25）暗示类别不平衡处理，但**未说明缺失值插补与掩码策略**；**无敏感性分析** |
| 是否满足检验假设 | **不适用/未说明** | 未做检验，故无假设检验前提可谈；但 Table 4/5/6 跨论文拼接基线的做法直接违反"独立性/同协议"这一任何比较的前提 |
| 内部自洽性（复算检查） | **Table 3 自洽；§PhysioNet 有 1 处口径不闭合** | ① Table 3 复算：五组模型的（总参数 − RNN 参数）恒为 **226,644**，CNN-only 行则为 2,124,901 → 表内自洽 ✓。② §PhysioNet 的 "on average three times faster than advanced discretized gated recurrent models"：按 Table 5 该组五个基线（0.5/0.5/0.7/0.7/0.3）与 CfC（0.1）的比值区间为 3×–7×、组均值比 ≈5.4× → **该句不可复算** ✗。③ "160 times" vs 复算 165× → 量级一致、绝对数字不一致 ✗ |

---

## 六、缺失信息清单

> 每条写成**可执行动作**；括号内为该缺失造成的具体后果。

1. **需向作者索取"训练/推理加速"的完整计时协议与硬件规格**：包括每个数据集、每个模型（尤其 ODE-RNN、Latent-ODE-ODE、ODE-LSTM、LTC）的 GPU/CPU 型号、精度（fp32/fp16）、batch size、是否含数据加载与求解器自适应步数的计入方式、计时重复次数与方差。（后果：无法判断 Abstract 的 "one to five orders of magnitude" 与可追溯的 3×–220× 之间的落差来自何处；P1 无法据此推断 MCU 上是否有任何加速。**这是 P1 最需要补齐的一条。**）
2. **需向作者索取 n=5 的随机种子列表与逐次重复结果**（四个数据集 × 四个 CfC 变体），并明确"Time per epoch"列是否为 5 次中的某一次/均值。（后果：无种子则方差不可复算；速度列为单值且无重复说明，加速比没有不确定度，P1 无法判断"快 N 倍"是否超出机器噪声。）
3. **需向作者索取真车车道保持试验的原始记录与统计**：每个模型（CfC / CfC-NoGate / CfC-mmRNN / NCP / LSTM / CNN）的试验次数、每次里程、**接管次数与接管率（每公里 / 每次机会）**、越界次数、转向误差或车道居中偏差、以及"all trained networks were able to successfully complete"所对应的判据。（后果：本文唯一真车闭环实验目前**不可复现、不可比较**；P1 无法据此建立任何控制器基线。）
4. **需作者澄清 "CfCs equipped with mixed memory instances outperform advanced RNN benchmarks" 中 "CfCs" 指哪个变体**：Table 6 显示 vanilla CfC 85.9% 低于 LSTM 87.3%、LMU 87.7%、HiPPO 88.0%，只有 CfC-mmRNN 88.3% 最高。（后果：这一句会被下游误读为"CfC 在 IMDB 超过 LSTM"；P1 的消融 A2（LNN vs CfC vs ODE-RNN）若用 vanilla CfC，引用该结论即失实。）
5. **需作者澄清口径歧义：Walker2D "18% margin over Transformers" 的分母/基数**（相对 CfC 自身误差 +18.35%？绝对降幅 15.5%？还是 CfC-mmRNN 的 18.9%/23.3%？）**以及 Abstract "one to five orders of magnitude" 的取值来源**（是否指训练总时长而非每 epoch？是否包含 CPU 上的 ODE 求解器？）。（后果：两种解释导致**同一个数字相差 4 个数量级 / 数个百分点**，引用时必须二选一。）
6. **需作者提供"数据集 × 变体 × 参数量 / FLOPs / 单步推理时延"表**：目前 Table 3 只覆盖车道保持模型，XOR / PhysioNet / IMDB / Walker2D 上 CfC 与各基线的规模完全未知。（后果：无法判断 CfC 的准确率优势是否只是模型更大；P1 也无法据此估算 <500 KB 的可行性。）
7. **需作者说明哪些 baseline 是本文重跑、哪些是复制**：Tables 4–7 的表注显示绝大多数基线数字来自 [7]/[9]/[40]/[42]/[44]，但**未说明这些数字是否在同一代码库/同一划分/同一硬件上产生**，也未给出基线的超参数。（后果：CfC 与 ODE-LSTM 在 XOR 上 0.53 个百分点的差距是否超出跨协议差异，完全不可判断。）
8. **需与 NMI 2022 正式版逐字比对 Tables 3–7、Fig. 3 图注与 Abstract 措辞**（本笔记依据 arXiv HTML 2106.13898）。（后果：正式版若已修改数字或删除 "one to five orders of magnitude" 等措辞，本笔记的台账条目编号与数值需同步修订；投稿引用前必须核对。）
9. **需向作者索取 Cf-S 与 LTC 在 PhysioNet（0.643 / 0.6477）与 IMDB（81.7 / 61.8）上异常低的原因说明**：Cf-S 是式 (9) 的直接实例化，LTC 是 CfC 的理论来源，二者均接近随机水平，而改进后的 CfC 达到 SOTA 附近。（后果：这提示"理论推导的闭式解本身不可用，实际可用的 CfC 是重新设计的架构"，即 §二 第 1 条的紧致性证明**并不覆盖被基准测试的模型**——此点直接决定 P1 能否把 Theorem 1 当作 CfC 的性能保证。）

---

## 七、复用价值判断

| 问题 | 结论 |
|---|---|
| **方法可否搬到 P1？需要改什么？** | **机理上可搬，但需要自建闭环训练与评价协议。** 可搬的部分：① CfC 不需要 ODE 求解器、时间 $t$ 显式进入门控（式 10），推理成本与离散 RNN 同阶（Table 2：序列 $\mathcal{O}(nk)$、单步 $\mathcal{O}(k)$）——这与 P1 的 **100 Hz 定步长控制回路**在机理上相容；② 对**不规则采样**的鲁棒性有 3 个任务的正面证据（Table 4 event-based、Table 5 PhysioNet、Table 7 Walker2D），若 P1 的实车数据回放存在非均匀时间戳，CfC 是合理选型；③ 参数效率在**同类模型横向比较**下成立（Table 3：CfC 的 RNN 分量 4,184 < NCP 6,495 < LSTM 33,089）。必须改的部分：本文 CfC 是**图像→转向曲率的模仿学习序列模型**（30 Hz，pixel-to-control），**不是控制器**，没有控制代价、没有状态反馈结构、没有稳定性/约束处理；P1 若用它做编队控制，需自行设计输入（OTF 势场 + 编队状态）、损失/训练范式（模仿 vs 闭环 RL/MPC 混合，参照 `AGENTS.md` §6「大胆决策，小心修正」）与评价指标（跟车 RMSE、加速度平方积分、Jerk 峰值、车道居中偏差、前轮转角方差、端到端延迟、MCU 内存占用——**这七项本文一项都没有**）。 |
| **评价协议可否直接对齐？** | **不能。** 本文指标为 accuracy（XOR/IMDB）、AUC（PhysioNet）、squared error（Walker2D）与**未定义的**车道保持表现；P1 指标全是控制类指标。两者**没有一项可共用**。可对齐的只有"报告纪律"层面：本文 Tables 4–7 使用 mean ± SD + n=5 的写法，P1 的 `AGENTS.md` §4 要求"种子 ≥5，报 mean ± std 或 95% CI"——在这一层上可以对齐并可对标（但 P1 必须比它多报**种子、CI 与显著性检验**，因为本文这三项都缺）。另外本文的**混合记忆变体对照**（CfC vs CfC-noGate vs Cf-S vs CfC-mmRNN）是 P1 消融 A2（LNN vs CfC vs ODE-RNN）可以借鉴的实验设计骨架：**一次只改一个因素**，且变体间参数尽量对齐（Table 3 中 CfC 与 CfC-NoGate 参数完全相同）。 |
| **代码/数据可否直接取用？许可如何？** | **代码可取用**：Acknowledgments 段明确 "All data, code, and materials used in the analysis are openly available at **https://github.com/raminmh/CfC** under **Apache 2.0 License**, for purposes of reproducing and extending the analysis"。Apache 2.0 允许商用、修改与再分发，需保留版权与许可声明、标注修改。**数据**：XOR / PhysioNet 2012 / IMDB / Walker2d-v2 均为公开基准（各自许可须另行核验）；**车道保持的 3 小时自采数据与增广数据、真车试验记录未声明公开**，不可获得。**本笔记未克隆或运行该仓库**，未验证其与论文表格的一致性——取用前须先跑通并复现 Table 4/5/6/7 中至少一行。 |
| **若要引用其数字，引用时**必须**带上的限定语** | ① 数据集与设置必须同行（XOR equidistant 还是 event-based；PhysioNet AUC；IMDB test accuracy；Walker2D squared error；车道保持只有参数量）；② 变体必须写全（CfC / CfC-noGate / **Cf-S** / **CfC-mmRNN** 四者结论不同，IMDB 上 vanilla CfC 与 mmRNN 的结论方向相反）；③ 加速比必须注明"**论文报告值，未报告硬件与计时协议，速度列为单次测量**"；④ 参数量必须注明是"**RNN 分量 4,184**"还是"**全模型 230,828**"；⑤ 凡基线数字必须注明"**文献报告值（取自 [7]/[9]/[40]/[42]/[44]），协议不同，不可直接比较**"（直接对应 `AGENTS.md` §1 第 3 条红线）；⑥ 版本必须注明所引为 **arXiv 2106.13898 HTML 版，未核 NMI 2022 正式版**。 |

**复用价值总判**：CfC 作为 **P1 控制器选型的工程组件**可取用（Apache 2.0、机理相容、有代码）；作为**"CfC 比 ODE 更快更准"的论证来源**，只能以"序列建模任务、特定基线、未报告硬件"的强度引用，**不可引申为控制性能**。

citation_qualifier: 5 settings (bit-stream XOR with equidistant+event-based encodings; PhysioNet 2012 8000 ICU patients; IMDB 25k/25k; MuJoCo Walker2d-v2; real-vehicle lane keeping on a Lexus RX450H over 1 km private road at 30 km/hr), accuracy/error as mean ± SD with n=5 but no seeds, no CI and no significance tests, speed as single per-epoch values with no hardware/precision/batch size/repetition reported (only 3x–220x is traceable although the Abstract claims one to five orders of magnitude), most baseline numbers copied from [7]/[9]/[40]/[42]/[44] rather than re-run, parameter counts available only for the lane-keeping model (CfC 4,184 RNN-only vs 230,828 including the CNN head), all figures/tables cited from the arXiv HTML version 2106.13898 and not verified against the published Nature Machine Intelligence 2022 version, and no closed-loop control performance metric is reported for the real-vehicle experiment

---

## 八、红队三条

**1. 领域最懂的人会质疑：** "你把 'CfC 比 ODE 快 100×' 当结论记了，但那个数字只出现在 **Fig. 3 的图注**里，没有硬件、没有精度、没有 batch size、没有重复次数；而你**真正能从表里复算的最大加速是 220×（Table 5，PhysioNet），在 Walker2D 上只有约 9.9×（0.79 → 0.08 min/epoch），在 XOR 上只有约 5.5×**。Abstract 写的 'one and five orders of magnitude'（10^5×）在这份全文的任何表格里都找不到对应测量。更要紧的是，你没有把这句加速结论限制在'序列建模任务、且在作者未说明的机器上'——一旦 P1 拿去暗示 MCU 上的实时性，就是**无出处的强度放大**。"
**需要什么证据才能消解：** 作者提供每个数据集计时脚本的硬件规格（GPU/CPU 型号、精度、batch size）、计时边界（是否含数据加载与求解器自适应步）与重复次数；或 P1 自己在目标 MCU 上重跑 CfC 与 ODE-RNN 的单步时延并报告方差。

**2. 方法与统计视角会质疑：** "Tables 4–7 的 n=5 只覆盖精度/误差列，**速度列是单值**；全篇无 CI、无显著性检验、**无多重比较校正**，而这套实验是 4 数据集 × 4 CfC 变体 × 约 20 基线。**最致命的是**：大多数基线数字标了 †/∗，来自 [7]/[9]/[40]/[42]/[44]——**CfC 与基线的比较是跨论文拼接的**，代码库、数据划分、硬件、调参预算全都不同。所以你记的'CfC 又快又准'里，'准'那半是拼接出来的。还有一处内部矛盾你没记：正文说 'ODE-based RNNs cannot solve the event-based encoding tasks regardless of their choice of solvers'，可本文自己的 Table 4 里 ODE-based = Yes 的 **ODE-LSTM 拿到了 98.89%**，同段下一句又把 ODE-LSTM 列为能解该任务的架构。"
**需要什么证据才能消解：** 作者在统一代码库、统一种子集、统一硬件上**重跑全部基线**并给出配对比较与校正后的显著性；或明确逐行标注'本文重跑 / 直接引用'，并说明跨协议差异的量级。对 ODE-based 那句断言，需给出 solver 消融（同一 ODE-RNN 换 Euler/RK4/dopri5）来支撑 'regardless of their choice of solvers'。

**3. 编辑/邻域读者会质疑：** "这篇论文被引用的核心理由是'CfC 又小又快'，但你这条笔记会让他们发现：**Table 3 是全文唯一的参数量表，且只覆盖车道保持模型**——XOR / PhysioNet / IMDB / Walker2D 上 CfC 与各基线的规模完全没有报告；同时正文说的 'around 4k trainable parameters' 只是 **RNN 分量 4,184**，**全模型是 230,828（含 CNN head）**，两者差 55 倍。如果缺失信息清单只写一句'未报告种子'，读者读完还是不知道这个模型到底多大、能不能放进目标硬件。"
**需要什么证据才能消解：** 作者补一张"数据集 × 变体 × 参数量 / FLOPs / 单步推理时延 / 内存占用"的表，并明确区分 RNN 分量与全模型；把每条缺失信息改写成可执行动作（需索取计时协议、需索取种子列表、需索取真车接管率），并写明缺它的具体后果。

> **校准声明（`deep-paper-reader` §8）**：以上三条红队质疑中，第 1 条已回改 §二 第 3 条（由含糊的"更快"降为 **D_int** 并写明 1–5 个数量级不可追溯）与 §四（加速比按数据集分行）；第 2 条已回改 §二 第 9 条（新增 ODE-based 断言的自相矛盾行，判 **D_int／否**）与 §五（多重比较未校正、等价性断言两行）；第 3 条已回改 §二 第 6 条（参数量口径）与 §六 第 6 条。三处修改均已落到台账与数字表，非仅在本节陈述。

---

## 九、限制

1. **材料限制（最重）**：本笔记依据 **arXiv HTML 版（2106.13898）** 的纯文本，**未获取 NMI 2022 正式版**，也**未获取补充材料之外的任何附件**。因此 §三 中"论文是否给出"的判定只对 arXiv 版成立；正式版若调整了 Tables 3–7 的数值或 Abstract 措辞（尤其是 "one to five orders of magnitude"），本笔记 §二、§四的所有条目需同步修订。**缓解**：引用前由 `citation-and-related-work` 以 DOI 10.1038/s42256-022-00556-7 核对正式版图表。
2. **复算限制**：本笔记**未克隆或运行** https://github.com/raminmh/CfC，**未下载任何数据集**。全部数字抄自论文印出的表格/正文，仅做**自洽性算术检查**（Table 3 的 226,644 恒定、Table 5 的 165×/220×、"three times" 不可复算、Table 7 的 18% 基数歧义）。因此**无法验证方差、异常值、实现细节与真实加速比**；§五 中"速度列为单值"的判定也仅基于文本未给出方差，而非确认作者未做重复测量。
3. **图像限制**：Fig. 3（紧致性）、Fig. 5（注意力剖面）在纯文本中**只保留图注**，图内曲线与显著性无法读取。故 §四 中 Fig. 3 的 MSE 0.006 为正文印出值（非估读），而 Fig. 5 **不产生任何可引用数字**——本文真车实验因此在本笔记中**没有任何性能数字**，这不是笔记的遗漏，而是原文确实未报告。
4. **单一视角限制**：本笔记只做**方法学与证据强度**记录，**不评价**该工作的重要性、新颖性与影响力（那是主编视角，交 `cross-paper-synthesizer` / `research-gap-hunter`）。
5. **外部复现未检**：§二 的"外部复现"列**一律为"未检"**，本次**未做引文检索**（按 `deep-paper-reader` §3.1.1，"未检"是信息缺失，**不得**被下游读成"无外部证据"，也**不得**据此把结论说成"仅一次性证据"）。若需升级等级，须由 `paper-discovery` / `paper-consensus` 走 OpenAlex `cites:<WorkID>` 通道完成。
6. **时效限制**：精读日期 **2026-10-02**。若该文已有更正（correction）或撤稿，本笔记未反映。**缓解**：入稿引用前复核 DOI 状态。
7. **P1 适用性限制**：本文**没有任何闭环控制性能指标**，因此本笔记**不能**为 P1 的控制器性能主张提供任何支撑；本笔记对 P1 的价值限于"控制器组件选型的工程属性（无求解器、参数效率、不规则采样、Apache 2.0 代码）"与"引用纪律（限定语）"，**不构成对 OTF-CfC 任何性能主张的证据**。

---

## 十、对 P1 的三条具体可用结论

### ① CfC 声称的推理速度/参数量优势，是在什么硬件与什么基线下得到的

**硬件：论文全文未报告任何硬件。** 全文（含正文、图注、表注、补充材料）grep 无 `GPU` / `CPU` / `NVIDIA` / `A100` / `Titan` / `Jetson` / 精度（fp32/fp16）/ batch-size-for-timing 的任何字样，也**没有单步时延、内存占用、功耗**。因此：

| 主张 | 原句 | 出处 | 该出处是否给硬件/协议 |
|---|---|---|---|
| 训练+推理快 1–5 个数量级 | "between one and five orders of magnitude faster in training and inference" | **Abstract** | 否（且本文表格不可追溯该区间） |
| 训练+推理快 ≥1 个数量级，"无精度损失" | "at least one order of magnitude faster training and inference time … without loss of accuracy" | §Explicit Time Dependency | 否 |
| 比 neural ODE 快 ≥100× | "at least 100x faster than neural ODEs at both training and inference" | **Fig. 3 图注** | 否（无硬件、无协议、无重复） |
| accuracy-per-compute time 改进 >150× | "over 150× improvement" | §CfCs: Flexible Deep Models | **否，且无任何图/表支撑** |
| PhysioNet：160×（vs ODE-RNN）、220×（vs continuous latent）、平均 3×（vs discretized gated） | 同左 | §PhysioNet Challenge | 否；可复算：165× ✓ / 220× ✓ / **"3×" 复算不出**（Table 5 该组比值 3×–7×，组均值比 ≈5.4×） |

**基线集合**：ODE 类 —— ODE-RNN [7]、Latent-ODE-RNN / Latent-ODE-ODE [7]、CT-RNN [33]、GRU-ODE [7]、LTC [1]、**ODE-LSTM [9]**（含混合记忆的 ODE 模型）；离散类 —— LSTM [20]、GRU [30]、Phased-LSTM [37]、GRU-D [36]、RNN-Decay / RNN-Impute / RNN-delta-t [7]、CT-GRU [34]、CT-LSTM [35]、coRNN [42]、Lipschitz RNN [43]、expRNN [41]、LMU [39]、HiPPO [40]、Transformer [46]。**基准的量化锚点是 Table 4/5/7 的 "Time Per epoch (min)" 列（单值、无方差）**，可复算的最大加速为 **220×**（Table 5）、Walker2D 上仅 **约 9.9×**。

**参数量**：**Table 3 是全文唯一的参数量表，且只对应车道保持模型**。CfC：**全模型（CNN head + RNN）230,828**，**RNN 分量 4,184**；CfC-mmRNN 235,052 / 8,408；NCP 233,139 / 6,495；LSTM 259,733 / 33,089。正文的 "around 4k trainable parameters in their recurrent neural network component" 只指**RNN 分量**。

**对 P1 的直接含义（这是本节最重要的一条）**：P1 声称"参数量 < 500 KB"。若按 **CfC 全模型 230,828 参数**估算：fp32 → 230,828 × 4 B = **923,312 B ≈ 902 KiB（0.881 MiB）> 500 KB**；fp16 → 461,656 B ≈ **451 KiB < 500 KB**。若按 **RNN 分量 4,184**：fp32 → 16,736 B ≈ **16.3 KiB**。**因此 P1 的 <500 KB 只能二选一主张：① 只算 RNN 分量（则需自证感知前端不占预算或另行量化）；② 全模型 + 量化到 fp16/INT8（则需报告量化后的精度损失）。** 且**本文未报告任何硬件与实测时延，"可上 MCU"在本文中没有任何证据**——"embedded applications" 只出现在 §Scope 的"何时用 CfC"建议句中，支撑是引文 [69]（模拟集成电路建模）/[70]（在制品质量预测）/[71]（肌电脑电监督控制），**均非本文实验**。

### ② 论文是否给出控制任务（闭环控制）证据？

**结论：论文有 1 次真实车辆上的闭环实验，但没有任何闭环性能数字；全部可比较的量化证据都在开环序列建模任务上。因此 —— 明确地 —— P1 不能把 CfC 的建模优势直接当成控制优势。**

分三层说明：

- **有闭环动作**：§How well CfCs perform in autonomous driving 报告了一次**真车闭环**：模型被部署到 Lexus RX450H（drive-by-wire），在 **1 km 私有测试路**以 **30 km/hr 恒速**跑完，"If the model exited the bounds of the lane a human safety driver intervened and restarted the model from the center of the road"，并做了有/无输入噪声（$\sigma^2 = 0.35$）两组测试。这**不是**仿真、**不是**回放，是实车闭环。
- **无闭环指标**：该实验的产出只有 ① **Table 3 的参数量**（确定性计数）与 ② **Fig. 5 的 Visual-Backprop 注意力可视化**（定性）。**没有成功率、没有接管次数/接管率、没有每模型试验次数、没有转向误差、没有车道居中偏差、没有时延**。作者的原话是定性断言："we observed that **all trained networks were able to successfully complete the lane-keeping task**"——**所有网络（含纯 CNN、LSTM）都完成了**，因此该句在 CfC 与其他架构之间**不构成任何区分性证据**。
- **所有量化比较都是开环**：Table 4（bit-stream XOR 分类）、Table 5（PhysioNet ICU 死亡率 AUC）、Table 6（IMDB 情感分类）、Table 7（Walker2D 下一步物理状态回归）。**没有一项是控制任务**；Walker2D 是"predict the physics state of the next time step"，属建模而非控制。
- **"闭环"一词在本文只出现在建议句里**：§Scope 写 "where **closed-loop performance matters** [24] CfCs should be the method of choice" —— 该句的支撑是引文 [24]（Vorbach et al., *Causal navigation by continuous-time neural networks*），**不是本文实验**；而且**同一段紧接着写** "implicit ODE-based models can still be significantly beneficial in solving continuously defined physics problems and **control tasks**"，即本文对"控制任务该用 CfC 还是 ODE"**内部口径自相矛盾**。

**对 P1 的操作性结论**：P1 若要用 CfC 做 100 Hz 编队控制器，**必须自建闭环训练与评价协议，并自行报告 P1 `AGENTS.md` §3 的七项指标**（跟车 RMSE、加速度平方积分、Jerk 峰值、车道居中偏差、前轮转角方差、端到端延迟、MCU 内存占用）。引用本文时，只能写"CfC 在**开环序列建模任务**上相对特定 ODE 基线报告了训练/推理加速与相当或更优的精度（文献报告值，协议不同，未报告硬件，不可直接比较）"，**不得**写成"CfC 有更好的控制性能"或"CfC 已被验证可用于闭环控制"。

### ③ 论文报告的局限中，哪一条最可能命中 P1

按"命中概率 × 对 P1 的破坏力"排序：

1. **【最可能命中，且是作者未自承的】** 部署边界完全缺失——**"可上 MCU"在本文没有任何证据**。作者只在 §Scope 把"embedded applications"列为适用场景（引文 [69,70,71]），全文**无任何 MCU/嵌入式/实时性实测**：无内存占用（KB）、无单步时延、无功耗、无目标平台、无编译器与量化档位——而 P1 `AGENTS.md` §3 明确要求"资源类指标须记录采集平台与档位（MCU 型号、编译器与优化选项）"。**若 P1 从本文推导"<500 KB、可上 MCU"，就是把作者的场景建议当成了实测结论。** 需要补的：P1 自己在目标 MCU 上实测 CfC 的内存与单步时延；引用本文时只引"参数量（RNN 分量 4,184 / 全模型 230,828）"，不引任何硬件结论。
2. **【作者自承，命中 P1 的长时程编队控制】** 梯度消失 → 长时程依赖需改用混合记忆。"CfCs might express **vanishing gradient problems**. To avoid this, for tasks that require **long-term dependencies**, it is better to use them together with mixed memory networks [9] (See CfC-mmRNN)."（§Scope）。**代价是速度**：Table 6 中 CfC-mmRNN 在 IMDB 上确实最好（88.3% vs CfC 85.9%），Table 7 中 Walker2D 误差也最低（0.617 vs 0.643），但 **time per epoch 从 0.08 涨到 0.34 min（慢 4.25×）**，PhysioNet 上从 0.1 涨到 0.2（慢 2×）。P1 的编队控制需要在长时程稳定性与 100 Hz 实时性之间取舍，**本文恰好把这两个目标推向相反方向**，且没有给出任何长时程稳定性实验（无 >1 km、无长时间连续运行、无失败分类）。
3. **【作者自承，需 P1 自行评估】** 双射性丧失 → 不适合依赖可逆性的用途。"CfCs **only approximate ODEs** and therefore they **no longer necessarily form a bijection** [65]"（§Scope）。P1 做的是前向控制，直接影响较小；但若 P1 后续要做**轨迹反演、安全验证或生成式场景采样**，CfC 不能替代 ODE 表示。同段还有两条作者自承的推测性局限（因果推断在 ODE 表示下可能更直接；连续流的可验证性在 ODE 与闭式之间孰优待评），**均标注为 speculate / would be beneficial to assess，属 D 级**，P1 不可当结论引用。

**明确不构成 P1 风险的项**：**非均匀采样**——本文在事件式 XOR（Table 4，CfC 99.42% vs ODE-RNN 51.21%）、PhysioNet（Table 5，时间与特征双缺失）、Walker2D（Table 7，不规则间隔）三个任务上都做了测试且表现良好，这是本文对 P1 最正面、也最可用的一条证据；**但注意它支撑的是"建模不规则采样数据"，不是"在不规则控制周期下闭环稳定"。**

---

*本笔记按 `deep-paper-reader` 六件套交付：主张—证据台账（含内部等级与外部复现双列）、方法可复现性清单、关键数字表（含数字口径对照表）、统计与推断旗标、缺失信息清单、复用价值判断（含 `citation_qualifier` 单行）；另附红队三条、限制与 P1 专用结论。*
