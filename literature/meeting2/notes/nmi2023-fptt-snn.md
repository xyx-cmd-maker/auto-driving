# FPTT 在线训练脉冲网络｜Accurate online training of dynamical spiking neural networks through Forward Propagation Through Time

- **出处**：Nature Machine Intelligence, vol. 5, no. 5, May 2023, pp. 518–527 ｜ **类型**：期刊论文（Article）
- **作者**：Bojian Yin et al.（Yin B, Corradi F, Bohté SM；CWI Amsterdam / TU Eindhoven / IMEC Netherlands / Univ. Amsterdam / Rijksuniversiteit Groningen）
- **DOI**：10.1038/s42256-023-00650-4（PDF 内印出；Crossref 核验 2026-10-03 通过：NMI 5(5):518–527，2023-05-08 online，被引 70）
- **全文来源**：`literature/fulltext/meeting2/accurate-online-training-of-dynamical-spiking-neural-network__2ac5058b.txt`（PAGES=12, CHARS=58,285）
- **分组**：连续时间 / 流体神经网络
- **证据等级初判**：B 级 — 顶刊正式版全文可得、表 1/表 2 与 Fig. 1–3 齐备，主要基准（Table 2）为**跨论文拼接的 SOTA 对比**（"This work" 一列自跑，Online/Offline baseline 两列取自他文）且无种子/无 CI；硬件只有训练 GPU（RTX3090）与显存，**无嵌入式/MCU/神经形态实测**。**【确定】**
- **档位建议**：A 精读 — 本组唯一直接给出「**在线训练**的内存复杂度与**在线学习**精度优势」的论文，且 LTC-SN 与 CfC 同源（LTC 血统），直接对标 P1「在线/增量适应」与「MCU 内存占用」两项指标的论证方式。**【确定】**
- **五维打分**：D1=4 D2=5 D3=4 D4=2 D5=5 → 加权 = 3·4+2·5+2·4+1·2+2·5 = 12+10+8+2+10 = **42**

> 打分口径（本组统一）：**D1** 与 P1 工程命题（100 Hz 连续控制 / 参数量可上 MCU / 端到端延迟可测）的直接相关度；**D2** 实验设计与报告质量（对照、重复、不确定度、可复现信号）；**D3** 方法/协议/数字的可迁移性；**D4** 与 P1 七项指标的可对齐度；**D5** 材料完整度（0–5，讲稿类材料上限 1）。权重 3/2/2/1/2。

## 1. 标题
Accurate online training of dynamical spiking neural networks through Forward Propagation Through Time｜通过时间前向传播实现动态脉冲神经网络的高精度在线训练

## 2. 摘要（≤400 字中文）
脉冲神经元递归网络虽已接近普通 RNN 的性能，但现有算法受限于小规模简单脉冲神经元与较短序列：内存需求高、难以训练复杂神经元模型、**与在线学习不兼容**。本文把 FPTT（Forward-Propagation Through Time，把沿时间的学**看作各时间步更新之间的"共识"问题**，只用空间梯度 + 动态正则项，不做 BPTT 的连乘链）与新提出的 **LTC-SN（liquid time-constant spiking neuron，膜时间常数 τm 与适应时间常数 τadp 是输入与状态的**可学习动态函数**）**结合，实现超长序列的在线学习：在时序分类任务上超过现有在线方法、逼近或超过离线方法（Table 2：R-MNIST 98.63% 为脉冲网络在线 SOTA，MNIST 99.62%、Fashion-MNIST 93.58% 逼近离线 BPTT；S-/PS-MNIST 与 DVS-GESTURE 接近离线）。代价是 FPTT 每样本**梯度计算 Ω(c(1)T)、参数更新 Ω(T)、内存 Ω(1)**（Table 1），而 BPTT 内存为 Ω(T)。该效率使端到端训练大规模 YOLOv4 式脉冲检测器 **SPYv4**（21 层、约 620 万脉冲神经元、**1400 万参数**）成为可能：PASCAL VOC07 上 mAP **51.38%（4 次读入）/ 53.25%（8 次读入）**，单时间步训练 < 14 GB 显存，直接相机输入时约 **60 时间步/秒（RTX3090）**，每个时间步约 10% 神经元激活；作者称其在性能、稀疏度与延迟上均超过 Spiking-YOLO（mAP 51.83% 但需 8,000 仿真时间步）。结论成立条件是：**任务为时序分类/检测、网络为 LTC-SN 或 LTC-SCNN、损失允许每步瞬时损失（分类任务需辅助散度项）**。

## 3. 结论（≤350 字中文）
作者结论：FPTT 可直接在 SNN 计算图上实现（Fig. 1a），**与 BPTT 相比兼容在线训练、内存恒定、能学更长序列**；FPTT 优于 OSTL、e-prop 等 BPTT 在线近似，并在大卷积 LTC-SNN 上逼近或超过对应的离线 BPTT 解。关键条件是 **FPTT 需要 LTC-SN 这种带门控结构的神经元**：FPTT 直接用于 ASRNN 或不带门控的 vanilla RNN **无法收敛**（正文自述亦在非脉冲 RNN 上观察到），而 LTC-SNN 用 BPTT 训练会因梯度爆炸**发散（loss 在 2,000 迭代后变 NaN）**。数字（Table 2，This work 一列）：R-MNIST **98.63%**、MNIST 99.62%、Fashion-MNIST 93.58%、DVS-GESTURE 97.22%、S-MNIST 97.37%、PS-MNIST 93.23%、DVS-CIFAR10 73.2%。**作者自承的局限**：① "最优的网络递归程度仍待确定"（optimal degree of network recurrency remains to be determined）；② LTC-SN 增加神经元状态计算量，在神经形态实现中"可能需要多房室神经元或全新的脉冲神经元模型实现"；③ 作为生物可行学习规则，FPTT 中的**空间误差反向传播需替换为局部空间信用分配**才可能在神经形态硬件上高效实现；④ LTC-SNN 无递归连接时可解较短序列但不能解较长序列（Supplementary Fig. 4）。

## 4. 方法一句话
输入脉冲序列 x_t → FPTT（瞬时风险 + 动态正则项，仅空间梯度）训练的 LTC-SNN（时间常数为输入/状态的可学习函数） → 每步输出脉冲/预测。

## 5. 图表清单（占位符）
全文共 **3 个 Figure + 2 个 Table**（合计 5 个，全部收录；正文另引用 Supplementary Fig. 1–6 与 Supplementary Table 1–5，**不在本 .txt 内**）。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-FPTT-1} | Fig. 1 | FPTT and LTC spiking neurons. a, Roll-out of the computational graph of a spiking neuron as used for BPTT (left) and FPTT (right). | (a) BPTT 沿时间连乘 vs FPTT 只走空间梯度——**在线学习的内存论证核心图**；(b) LIF vs LTC 脉冲神经元结构（LTC 多出 Wτ 与 σ 支路）；(c) LTC 神经元的 F–I 曲线随 Wτ 组合变化；(d) 动态输入电流下的响应放电率（可出现"电流更大、放电率更低"的反直觉区间）。 |
| {FIG-FPTT-2} | Fig. 2 | Performance evaluation of SNNs. a, Example loss-curves for networks trained on the Add-task with sequence length T = 1000 for BPTT, Truncated-BPTT for truncation length 1 (TBPTT-1, equivalent to BP at each time step) and FPTT. | (a) **BPTT 训练 LTC-SNN 的 loss 在 2,000 迭代后变 NaN**，FPTT 收敛；(b) 末 100 次迭代平均 loss ± s.d.（5 次运行）——**本文唯一给出重复次数的图**；(c) DVS-GESTURE 上随帧长 20→1000 的测试精度（3 次运行均值 ± s.d.，插入个体数据点）；(d)(e) DVS-GESTURE / R-MNIST 训练显存随序列长度——R-MNIST 上 FPTT **显存恒定**而 BPTT 线性增长。⚠ (d) 的上升被作者归因于**数据集本身膨胀**（20 帧 7.4 GB → 1,000 帧 368.1 GB），不是模型显存。 |
| {FIG-FPTT-3} | Fig. 3 | Spiking-YOLO-v4 (SPYv4). a, The mAP and components for classification and recognition of 20 different kinds of objects in SPYv4 on the PASCAL VOC07 dataset. | (a) 20 类 AP 条形图，含 mAP；Car 0.77 / Person 0.71 / Train 0.70 … 到 Boat 0.23；(b) 作者在鹿特丹用手机拍的序列图上的检测示例（**作者自采图像，非数据集内**）；(c) 摄像头在"播放作者视频的显示器"与"办公室环境"间移动时，浅层与深层各 100 个随机抽取脉冲神经元的 raster 图——浅层持续激活、深层对无关刺激静默（稀疏性证据）。 |
| {TAB-FPTT-1} | Table 1 | Computational complexity of gradients, parameter updates and memory storage per sample | BPTT Ω(c(T)T) / Ω(1) / **Ω(T)**；RTRL Ω(c(T)T²) / Ω(T) / Ω(T)；e-prop/OSTL Ω(c(1)T) / Ω(T) / Ω(1)；**FPTT Ω(c(1)T) / Ω(T) / Ω(1)**。P1 要论证"在线训练可行"时，**本表是可逐字引用的复杂度口径来源**；注意其内存列是**每样本**，不含优化器状态与激活缓存口径。 |
| {TAB-FPTT-2} | Table 2 | Test accuracy of deep SRNNs/SCNNs on various tasks | 三列 = Online baseline / This work / Offline state of the art。**只有中间一列是本文自跑**：其余两列取自 refs 1/12/16/46–49。R-MNIST 行是本文唯一"在线优于离线 SOTA"的证据（98.63% vs 97.72%）。⚠ 表内**无参数量、无方差、无重复次数、无硬件**。 |

**（无 >5 项的情形；全文 3 图 2 表已全部覆盖。）**

## 6. 对 P1 的用处

- **与 P1 的关系**：**相邻问题（方法学底座）**。本文不是控制器、不是车辆、不含任何动力学/编队/ODD 概念；但它正面回答 P1 需要论证的一条工程命题——**"连续时间模型能不能在线学、代价多少"**，并给出可引用的复杂度表与 GPU 显存曲线。

- **可迁移**：
  1. **可逐字引用的复杂度口径（Table 1）**：FPTT 每样本内存 **Ω(1)**、梯度计算 Ω(c(1)T)、参数更新 Ω(T)，对比 BPTT 内存 **Ω(T)**。P1 若做"在线/增量微调"或"回放-在线混合"，这是**唯一**在顶刊正式版中印出的 LNN 家族在线训练复杂度表。
  2. **"FPTT 需要门控结构"这一消融结论**：FPTT 直接用于 ASRNN 与 vanilla RNN 不收敛，**只有带可学习动态时间常数的 LTC-SN 才收敛**。→ 直接支撑 P1 的 **A2 消融设计（LNN vs CfC vs 普通 ODE-RNN）**：它给出了"为什么不能只把求解器换成便宜的一阶方法、而必须保留输入依赖的时间常数"的**已发表对照**。
  3. **"复杂神经元 + BPTT = 发散"的负面结果**：LTC-SNN 用 BPTT 训练在 2,000 迭代后 loss 变 NaN，TBPTT-1 不发散也不收敛。→ P1 若计划对 ODE-RNN 基线用 BPTT，**必须报告是否出现同类发散**，否则基线不可信（本项目 `AGENTS.md` §3 要求"同等调参预算"）。
  4. **显存 vs 序列长度的报告范式（Fig. 2d/e）**：把"模型显存"与"数据膨胀"分开归因（R-MNIST 用同一图像重复 20 帧来分离两者）。→ P1 报告"MCU 内存占用"时应采用同样的**口径分离**（模型权重 / 激活 / 输入缓冲），并写明采集平台与档位（`AGENTS.md` §3 已要求）。
  5. **LTC-SN 与 CfC 的对照价值**：本文把 LTC 的"输入依赖时间常数"搬到脉冲神经元上并**把 τ 的取值域用 sigmoid 限制到 (0,1] 的 α=exp(−dt/τm)**（式 8a/8b）。→ P1 若在 CfC 上做数值稳定化（防止 α 越界导致积分发散），这是可直接抄的实现细节。

- **不可迁移 / 陷阱**：
  1. **不是控制器**：全文无控制代价、无状态反馈结构、无稳定性/约束处理，**无任何闭环控制实验**。P1 不能引本文支撑任何控制性能主张。
  2. **无嵌入式/MCU/神经形态实测**：全文硬件只有 **NVIDIA RTX3090 工作站**（推理计时）与 **24 GB GPU 显存**（训练）。"extremely low latency" 指 60 时间步/秒的 GPU 推理；"可在神经形态硬件上高效实现"是**推测句（can also likely be implemented）**，无实验。
  3. **Table 2 的两列基线不是本文跑的**：Online baseline 与 Offline SOTA 取自 refs 1/12/16/46–49（表注仅说"网络结构与 ref. 16 匹配"）。跨论文拼接 → 引用时须写"文献报告值，协议不同"。**这与 P1 `AGENTS.md` §1 第 3 条红线同类**。
  4. **"online" 的语义与 P1 不同**：本文的 online = **每个时间步更新一次权重**（单遍流式学习），不是 P1 语境里的"车上在线学习/在线适应"。引用时必须限定为"逐时间步流式训练（single-pass streaming）"。
  5. **参数量口径只覆盖 SPYv4**：14 M 参数 + 620 万神经元是 **21 层 YOLOv4 检测器**的规模，与 P1 的控制器规模差 3 个数量级，**不可用作 P1 的参数预算参照**；Table 2 的 7 个分类基准网络**完全没有参数量报告**。
  6. **脉冲网络的能量论证未被本文量化**：本文只报 GPU 显存与时间步/秒，**无能耗、无焦耳/推理、无芯片面积**。P1 若要写"能效"，本文不构成证据。

- **与 CfC（NMI 2022）的关系**：**同源、互补，不是替代**。
  - 同源：本文的 LTC-SN 直接**"Taking inspiration from the concept of liquid time-constants (LTCs) [14]"**，ref. 14 即 Hasani 等 *Liquid time-constant networks*（AAAI 2021），也就是 CfC（NMI 2022）的理论前身。CfC 论文的引文表里亦无本文（CfC 2022-11 见刊，本文 2023-05 见刊，时间上互不引用）。
  - 互补方向：CfC 解决的是 **LTC 积分无闭式解 → 用闭式近似去掉 ODE 求解器**（推理成本问题）；本文解决的是 **训练不能在线上做 + 长序列显存爆炸 → 用 FPTT 去掉时间反向传播**（训练成本问题）。二者可以叠加：理论上可以用 FPTT 训练 CfC 式无求解器的连续时间网络——**但本文没有做这个实验，也没有做任何"FPTT vs BPTT 训练 CfC"的对照**。
  - 对 P1 的直接含义：P1 的 A2 消融若包含"在线训练"这一因素，**目前文献里没有现成的「CfC + FPTT」结果可直接引用**，只能自己跑；反过来，引用本文时必须写明它测的是 **LTC-SN（脉冲版 LTC）**，不是 CfC。

- **引用时必须带的限定语**：
  "在 Yin 等关于 **FPTT 在线训练脉冲网络**的工作中（Nature Machine Intelligence 2023;5(5):518–527），结论限定于**时序分类/检测基准**（Add-task、(P)S-MNIST、R-MNIST、MNIST、Fashion-MNIST、DVS-GESTURE、DVS-CIFAR10、PASCAL VOC07）与**脉冲 LTC-SN/LTC-SCNN 架构**：其内存 Ω(1)、梯度 Ω(c(1)T) 是**每样本复杂度**（Table 1，无实测交叉验证），SPYv4 的 1400 万参数指 **21 层脉冲 YOLOv4 检测器**而非分类基准网络，Table 2 的 Online/Offline 两列基线**取自其他论文而非本文重跑**，全部实验仅运行在 **GPU（RTX3090 / 24 GB 显存）** 上，**无 MCU、嵌入式或神经形态硬件实测**，且 FPTT 需 LTC-SN 的门控结构才能收敛（无重复次数、无随机种子、无置信区间报告）。"

- **P1 落地三问**：
  1. **是否有硬件实测？** **有 GPU 推理计时，无 MCU/嵌入式/实时性实测。** 唯一硬件数字：直接相机输入时**约 60 时间步/秒、对应 7 或 15 张图/秒**，运行在 **NVIDIA RTX3090 工作站**（正文，非表格）；训练单时间步 **< 14 GB 显存**。**无内存占用（KB/MB，模型侧）、无单步时延、无功耗、无目标 MCU、无编译器/量化档位**。文中"neuromorphic hardware"只出现在推测句与参考文献中。
  2. **是否报告参数量？** **部分报告。** 只有 SPYv4：**14 million parameters in total**、19 个脉冲卷积层、约 **6.2 million LTC spiking neurons**（正文 + Supplementary Fig. 2a）。**Table 2 的 7 个分类基准网络（(P)S-MNIST 用 1 层 512 隐神经元 + 10 输出；R-MNIST 用 2×256 + 10 输出；DVS 用 6 卷积 + 512D + 11I 等）只给结构，不给参数量。** 无"是否含感知头"的口径问题（本文是单一端到端网络，无独立感知头）。
  3. **训练是在线还是离线？** **在线（本文的核心卖点）。** FPTT 每个时间步更新一次权重（FPTT-T），变体 FPTT-K 每 K 步更新。**时间开销**：正文只给相对陈述"训练时间仅略长（only slightly longer）"（Supplementary Table 4）；**无绝对秒数、无每 epoch 时间、无墙钟对比表**。**内存开销**：每样本 Ω(1)（Table 1）；实测口径见 Fig. 2d/e——R-MNIST 上 FPTT 训练显存**恒定**，BPTT 线性增长；FPTT 相对 BPTT 的显存优势至多 **5 倍**（正文引 Supplementary Table 3）。**故：在线训练的内存有时间步不变性证据，但时间开销只有定性表述，不可引用为"在线训练几乎不增加时间成本"。**

## 7. 缺失信息（≥3 条，写成可执行动作）
1. **需向作者索取 Table 2 逐行的"本文重跑 / 文献引用"标注与基线超参数**（尤其 Online baseline 列的 OSTL+SNU、DECOLLE+SNN、EMSTDP+SNN 三行，与 Offline 列的 BPTT+ASRNN、BPTT+SNU、BPTT+PLIF 三行）。（后果：本文的"优于在线方法"结论目前是**跨论文拼接**，R-MNIST 的 98.63% vs 95.34% 差 3.29 个百分点是否超出协议差异**不可判断**。）
2. **需作者提供各基准网络的参数量表**（(P)S-MNIST 的 512 隐层、R-MNIST 的 2×256、DVS 的 6 卷积 + 512D 架构）。（后果：无法判断 FPTT+LTC 的精度优势是否来自参数更多——这正是 P1 做基线公平性时必须排除的混淆；P1 也**无法**从本文推算任何"可上 MCU"的参数预算。）
3. **需补 Supplementary Table 3/4 的原始数值**（FPTT vs BPTT 的显存比"至多 5 倍"、"训练时间仅略长"）。（后果：`literature/fulltext/meeting2/` 内的 .txt 只到正文与参考文献，**两处关键定量结论都落在补充材料里，本卡无法核验其数字**。）
4. **需作者澄清 Table 1 的复杂度口径**：Ω(1) 内存是否包含优化器状态（Adam/Adamax 的一阶二阶矩）与 LTC-SN 的额外状态（u、b、θ、ρ、α）？（后果：P1 的"MCU 内存占用"是**权重 + 状态 + 缓冲**的总账，而本文的 Ω(1) 若不含优化器状态，直接搬用会低估车载常驻内存。）
5. **需作者提供 DVS-GESTURE 长序列实验的逐项数值**（Fig. 2c 只有图，正文仅给 LSTM 从 88.9%（100 帧）降到 82.5%（500 帧）两点）。（后果：**"FPTT+LTC-SNN 在所有帧长下都最好"这一句在图外不可复核**，P1 不可据此引用任何 LTC-SNN 的具体精度数字。）
6. **需核验 LTC-SN 与 CfC 的可组合性**：本文从未用 FPTT 训练 CfC（亦未讨论），CfC 论文亦未引用本文。→ 动作：若 P1 计划把"在线训练"写进卖点，须**自行设计并报告「CfC + FPTT」的最小实验**，不得引用本文暗示该组合已被验证。
7. **需做 T2 取代检查**：检索 2023 年后是否有更长序列 / 更大规模 / 更低内存的在线 SNN 训练法（如 FPTT 的后续改进）取代本文结论。→ 动作：以 OpenAlex/Crossref 检索，记录检索式与日期（本卡未做，标 `[待核实]`）。

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| FPTT 每样本复杂度 | 梯度 Ω(c(1)T)；参数更新 Ω(T)；内存 **Ω(1)** | 无（符号复杂度） | Table 1 |
| BPTT 每样本复杂度 | 梯度 Ω(c(T)T)；参数更新 Ω(1)；内存 **Ω(T)** | 无 | Table 1 |
| RTRL 每样本复杂度 | 梯度 Ω(c(T)T²)；参数更新 Ω(T)；内存 Ω(T) | 无 | Table 1 |
| e-prop/OSTL 每样本复杂度 | 梯度 Ω(c(1)T)；参数更新 Ω(T)；内存 Ω(1) | 无 | Table 1 |
| R-MNIST 测试精度 | **FPTT+LTC 98.63%**；Online baseline OSTL+SNU 95.34%；Offline BPTT+SNU 97.72% | 未报告 | Table 2 |
| MNIST 测试精度 | FPTT+LTC **99.62%**；Online DECOLLE+SNN 98.0%；Offline BPTT+PLIF 99.72% | 未报告 | Table 2 |
| Fashion-MNIST 测试精度 | FPTT+LTC **93.58%**；Online EMSTDP+SNN 85.3%；Offline BPTT+PLIF 94.38% | 未报告 | Table 2 |
| DVS-GESTURE 测试精度 | FPTT+LTC **97.22%**；Online DECOLLE+SNN 95.54%；Offline BPTT+PLIF 97.57% | 未报告 | Table 2 |
| S-MNIST 测试精度 | FPTT+LTC **97.37%**；Online 列为"—"；Offline BPTT+ASRNN 98.7% | 未报告 | Table 2 |
| PS-MNIST 测试精度 | FPTT+LTC **93.23%**；Online 列为"—"；Offline BPTT+ASRNN 94.3% | 未报告 | Table 2 |
| DVS-CIFAR10 测试精度 | FPTT+LTC **73.2%**；Online 列为"—"；Offline BPTT+PLIF 74.8% | 未报告 | Table 2 |
| Add-task 末 100 迭代平均 loss（T=1000） | 见 Fig. 2b（仅图，正文未印数值） | s.d. 取自 **5 次运行** | Fig. 2b 图注 |
| DVS-GESTURE 浅层 SRNN 精度随帧长 | LSTM：**100 帧 88.9% → 500 帧 82.5%** | 未报告 | 正文 §FPTT allows for longer sequence training |
| DVS-GESTURE BPTT 失败点 | LTC-SNN 在帧长 **200 与 500 时不收敛**（报最佳验证精度）；1,000 帧时 LSTM/ASRNN/LTC-SNN 均**超 24 GB GPU 显存** | 未报告 | 正文 §FPTT allows for longer sequence training |
| BPTT 训练 LTC-SNN 的 Add-task 发散点 | loss 在 **2,000 迭代**后变 NaN（T=1000） | 未报告 | Fig. 2a 图注 + 正文 |
| 数据集体积（DVS-GESTURE 帧编码） | 20 帧 **7.4 GB** → 1,000 帧 **368.1 GB** | 未报告 | 正文 §FPTT requires less memory |
| SPYv4 规模 | **19 个脉冲卷积层；约 620 万 LTC 脉冲神经元；1400 万参数**（正文另有一处写"21 layers"） | 未报告 | 正文 §Large-scale object detection；Supplementary Fig. 2a |
| SPYv4 检测精度 | mAP **51.38%**（4 次读入）；**53.25%**（8 次读入）；IoU 阈值 ϑ=0.5 | 未报告 | 正文 §Large-scale object detection；Fig. 3a |
| SPYv4 训练显存 | 单时间步 **< 14 GB** GPU 显存 | 未报告 | 正文 §Large-scale object detection |
| SPYv4 推理速度 | 直接相机输入约 **60 时间步/秒** = **7 或 15 张图/秒**（RTX3090 工作站） | 未报告 | 正文 §Large-scale object detection |
| 脉冲稀疏度 | 每时间步平均约 **10%** 神经元激活 | 未报告 | 正文 §Large-scale object detection |
| Spiking-YOLO 对照 | mAP **51.83%**，需 **8,000 仿真时间步** | 未报告 | 正文 §Large-scale object detection（引 ref. 18） |
| FPTT vs BPTT 显存优势 | 至多 **5 倍** | 未报告 | 正文引 Supplementary Table 3 |
| FPTT vs BPTT 训练时间 | "only slightly longer"（仅略长） | 未报告 | 正文引 Supplementary Table 4 |
| 训练超参（(P)S-MNIST） | Adam，batch 128，200 epochs，初学习率 3×10⁻³，第 30/80/120 epoch 减半 | — | Methods §Datasets |
| 训练超参（DVS-GESTURE / DVS-CIFAR10） | Adamax，batch 16，初学习率 1×10⁻³，20 个连续帧 | — | Methods §Datasets |
| SPYv4 训练超参 | Adagrad，batch 32，初学习率 1×10⁻³；VOC2007+VOC2012 共 16,551 训练图，VOC2007 验证 4,952 图 | — | Methods §Spiking Tiny YOLOv4 |
| 输出单元泄漏时间常数（训练后） | **87 ms ± 13 ms**（S-MNIST）；**65 ms ± 12 ms**（PS-MNIST） | ± 为 s.d.（重复次数未报告） | Methods §Datasets |
| 硬件 | NVIDIA RTX3090 工作站；训练显存上限 24 GB；GPU 显存由 `nvidia-smi` 采集 | — | 正文 + Methods |

⚠内部不一致：正文写 SPYv4 "uses **21 layers**, 6.2 million LTC spiking neurons and 14 million parameters"（§引言末），但在 §Large-scale object detection 段写 "**19 spiking convolutional layers**, two convolutional output layers and 14 million parameters"。同一网络层数两处不一致（21 vs 19+2），**引用层数时须二选一并注原文**。

【确定】/【推测】标注：以上数字均为 PDF 印出值【确定】；对本组材料问题（Table 2 两列为跨论文引用、无 MCU 实测）的判断来自逐字阅读表注与全文 grep"MCU/microcontroller/Jetson/Raspberry/FPGA"零命中【确定】。
