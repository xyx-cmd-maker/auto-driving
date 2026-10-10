# DeepONet 算子学习｜Learning nonlinear operators via DeepONet based on the universal approximation theorem of operators

- **出处**：Nature Machine Intelligence, vol. 3, no. 3, 2021, pp. 218–229（正式版，见下条版本警示）｜ **类型**：期刊论文
- **作者**：Lu Lu et al.（第一作者 Lu Lu；正式版作者 **Lu L, Jin P, Pang G, Zhang Z, Karniadakis GE** 共 5 人；**本地 .txt 内印出的作者只有 3 人**：Lu Lu, Pengzhan Jin, George Em Karniadakis）
- **DOI**：10.1038/s42256-021-00302-5（**PDF 内未见**；由 Crossref 核验 2026-10-03 得到：NMI 3(3):218–229，2021-03-18 在线）
- **全文来源**：`literature/fulltext/meeting2/learning-nonlinear-operators-via-deeponet-based-on-the-unive__330d80e4.txt`（PAGES=22, CHARS=57,787）
- **分组**：连续时间 / 流体神经网络
- **★ 版本警示（贯穿全卡）**：本地 .txt 第 1 页明确印有 "**arXiv:1910.03193v3 [cs.LG] 15 Apr 2020**"，且全文**无 Nature Machine Intelligence 刊头、无 DOI、无期刊卷期页码**，页脚为 arXiv 页码 1–22，第 16 章的致谢日期与参考文献格式均为 arXiv 风格。→ **本卡的全部图号、表号、数值来自 arXiv v3 预印本，不是 NMI 2021 正式版**；正式版章节结构、图号与数值可能不同。**引用前必须取 NMI 正式版逐条复核**（`citation-and-relate-work` 动作）。
- **证据等级初判**：C 级 — 材料为预印本（**非**正式版），全部证据为**数值仿真**（参考解由 Runge-Kutta (4,5) / 二阶有限差分生成，无实验数据、无真实系统），且**无参数量、无硬件、无不确定度（仅个别图有 ±1 SD 阴影）**。**【确定】**
- **档位建议**：C 仅引用 — DeepONet 的"branch/trunk 双网 + 归纳偏置"思想对 P1 的 OTF 势场作为**函数条件模态**有方法论启发，但本文的四个问题全是低维 ODE/PDE 基准，与车辆控制、编队、混行交通无一相同；且材料为预印本，**不建议占用 A 档精读预算**。**【确定】**
- **五维打分**：D1=2 D2=3 D3=3 D4=1 D5=3 → 加权 = 3·2+2·3+2·3+1·1+2·3 = 6+6+6+1+6 = **25**

## 1. 标题
Learning nonlinear operators via DeepONet based on the universal approximation theorem of operators｜基于算子通用逼近定理、用 DeepONet 学习非线性算子
（⚠ 本地 .txt 第 1 页的标题为 "**DeepONet: Learning nonlinear operators for identifying differential equations based on the universal approximation theorem of operators**"，与正式版标题不同；本卡标题栏采用正式版标题，正文引用时须对应版本。）

## 2. 摘要（≤400 字中文）
神经网络是连续函数的通用逼近器，但**更少被注意、可能更强的结果**是：**单隐层网络可精确逼近任意非线性连续算子**（Chen & Chen, 1995）。该定理只保证"网络足够大时逼近误差小"，**不涉及优化误差与泛化误差**——而后者在实践中常占主导。为把定理落地，作者提出 **DeepONet**：两个子网络，**branch net** 在固定的 m 个传感器位置 x₁…x_m 上编码输入函数 u，**trunk net** 编码输出函数的求值位置 y，两者内积得 G(u)(y) ≈ Σ b_k t_k（可加偏置 b₀）。训练数据只需**传感器位置对所有输入函数一致**（不要求网格），**输出位置 y 任意**。作者对**动态系统（ODE）与偏微分方程（PDE）两类算子**做系统仿真，证明 DeepONet 相比全连接网络**显著降低泛化误差**，并从理论上推导了**逼近误差对传感器数 m 与输入函数类型的依赖**（Theorem 2），用计算实验验证；更重要的是观察到**高阶误差收敛**：对训练数据量呈**多项式率（半阶到四阶）甚至指数收敛**。在**最简线性问题**上即可看出机制：DeepONet 的泛化误差可忽略，而 FNN 即便网格搜索（深度 2–4、宽度 10–2560、学习率 1e-4–1e-2）最优测试 MSE 也只有 ∼10⁻⁴。结论成立条件是：**算子连续、输入函数空间紧（GRF/RBF 或 Chebyshev 多项式）、传感器数 m 足够大**。

## 3. 结论（≤350 字中文）
作者结论：本文把算子学习问题放在更一般的设定下（传感器只需固定、不需等距网格；输出位置无约束），提出 DeepONet 用两个子网络分别编码输入函数与位置变量，再合并输出；在**四个 ODE/PDE 问题**上验证，DeepONet 依靠这一**归纳偏置**取得更小的泛化误差。作者系统研究了传感器数、最大预测时长、输入函数空间复杂度、训练数据量、网络规模对测试误差的影响，观察到**多项式与指数级误差收敛**，并称"**据我们所知，这是深度学习里首次观察到指数收敛**"。**作者自承的局限（结论节逐字）**：① "**尚无算子逼近的网络规模理论结果**"（类比函数逼近的宽度/深度界）；② "**理论上仍不理解 DeepONet 为何能产生小泛化误差**"；③ 本文两个子网络都用**全连接网络**，卷积或注意力机制"可能进一步提升精度"但未做；④ §4.2.2 明确写 m、T、l 的精确依赖"难以量化"，Theorem 2 中的 Te^{cT} 界"相对计算结果**是松的**"（loose）；⑤ §4.3 承认对拟合出的 ln(x) / e^{−x} 收敛形式"**目前无法完全解释**，需更多理论与计算研究。

## 4. 方法一句话
输入函数 u 在 m 个固定传感器上的采样 + 输出位置 y → branch net 与 trunk net 双网内积（显式归纳偏置）→ G(u)(y) 标量输出，逐点拼出输出函数。

## 5. 图表清单（占位符）
全文共 **10 个 Figure + 3 个 Table**（合计 13 个，全部收录）。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-DON-1} | Figure 1 | Illustrations of the problem setup and architectures of DeepONets. (A) The network to learn an operator G : u 7→ G(u) takes two inputs [u(x1), u(x2), . . . , u(xm)] and y. | (A) 问题设定（函数进、函数出）；(B) 训练数据要求——**输入函数必须在同一组传感器上取值，输出位置完全不限**（这是本文相对 CNN 类图像法的核心自由度）；(C) stacked DeepONet（p 个并行 branch 网）；(D) unstacked DeepONet（1 个 branch 网输出 p 向量）——**本文后续全部使用 unstacked + bias**。 |
| {TAB-DON-1} | Table 1 | Default parameters for each problem, unless otherwise stated. We note that one data point is a triplet (u, y, G(u)(y)), and thus one specific input u may generate multiple data points with different values of y. | 四问题的 u 空间（全部 GRF, l=0.2）、传感器数 m=100、训练/测试点数（4.1.1: 10k/100k；4.1.2: 10k/100k；4.2: 10k/100k，k=1,T=1；4.3: 1,000,000/500,000）、迭代次数。**"一个 u 生成多个数据点"这一口径决定了下文所有"数据集大小"的含义。** |
| {TAB-DON-2} | Table 2 | DeepONet size for each problem, unless otherwise stated. | Trunk 深 3 宽 40（4.3 为 100）；Branch 深 2 宽 40（4.3 为 100）。**只有层宽/深度，无参数量、无 FLOPs。** |
| {FIG-DON-2} | Figure 2 | Errors of FNNs trained to learn the antiderivative operator (linear case). (A and B) Learning rate 0.01. (C and D) Learning rate 0.001. (E and F) Learning rate 0.0001. … The shaded regions in (D) are the one-standard-derivation from 10 runs with different training/test data and network initialization. | **FNN 基线的网格搜索结果**：最小测试误差 ∼10⁻⁴（depth 2, width 2560, lr 0.001）。作者的关键观察：网络小时训练误差大而泛化误差小，网络大时训练误差降但泛化误差升；**FNN 始终未进入过拟合区**。**10 次运行的 ±1 SD 只画在 (D) 一处。** |
| {FIG-DON-3} | Figure 3 | Errors of DeepONets trained to learn the antiderivative operator (linear case). (A) The training trajectory of an unstacked DeepONet with bias. (B) The training/test error for stacked/unstacked DeepONets with/without bias compared to the best error of FNNs. The error bars are the one-standard-derivation from 10 runs with different training/test data and network initialization. | **本文的核心机制图**：加 bias 同时降低训练与测试误差、并**降低随机初始化下的方差**；unstacked 训练误差更大但测试误差更小（泛化误差更小）→ 选 unstacked + bias。**±1 SD 来自 10 次运行（不同训练/测试数据 + 初始化）**。 |
| {FIG-DON-4} | Figure 4 | Nonlinear ODE: unstacked DeepONets have smaller generalization error and smaller test MSE than stacked DeepONets. (A) The correlation between the training MSE and the test MSE of one stacked/unstacked DeepONet during the training process. | 非线性 ODE（g = −s² + u）下训练/测试 MSE 的相关性；**(B) 10 次随机运行下 unstacked 的拟合直线**：`MSE_test ≈ 10 × MSE_train − 10⁻⁴`；(C) 均值 ±1 SD。⚠ 4.1.2 明写测试 MSE **剔除了最差的 1‰ 预测**——这是一个容易漏掉的口径。 |
| {FIG-DON-5} | Figure 5 | Nonlinear ODE: predictions of a trained unstacked DeepONet on three out-of-distribution input signals. The blue and red lines represent the reference solution and the prediction of a DeepONet. | 三个**分布外**输入（u=x、sin(πx)、sin(2πx)）上的预测 vs 参考解；**"OOD 也能用"是本文少见的泛化主张，但仅 3 个例子、无误差数字**。 |
| {FIG-DON-6} | Figure 6 | Gravity pendulum: required number of sensors for different T, k and l. (A) Training MSE (square symbols) and test MSE (circle symbols) decrease as the number of sensors increases in the case k = 1, T = 1 and l = 0.2. | (A) 传感器数小时的**指数衰减 MSE ∝ 4.6⁻#sensors**，转折点在 **∼10 个传感器**（图中箭头）；(B) 预测越长需要越多传感器（T=5 需 ∼25 个）；(C) u 越不平滑（l 越小）需要越多；(D) 对 k 不敏感。**注意图注明写"For clarity, the SD is not shown"——本图无不确定度。** |
| {FIG-DON-7} | Figure 7 | Gravity pendulum: error tendency and convergence. (A) Both training error (blue) and test error (red) increase fast for long-time prediction if we keep the network size fixed at width 40 and the training data size fixed at 10000 points. | (A) **MSE ∝ 8^T**（预测时长指数放大误差，且是 [0,T] 上的平均误差而非 T 点误差）；(B) 存在**最优网络宽度**（宽 100 附近，超过后误差回升，作者归因于优化误差）；(C)(D) 数据量收敛律：小数据集 `MSE_test ∝ e^{−x/2000}`，大数据集 `∝ x^{−0.5}`；泛化误差 `∝ x^{−1}`（**优于经典学习理论的 x^{−0.5}**）。 |
| {FIG-DON-8} | Figure 8 | Gravity pendulum: errors for different input function spaces. Training error (solid line) and test error (dash line) for (A) GRF function space with different length scale l. (B) Chebyshev polynomials for different number of basis functions. | 存在**临界长度尺度**与**临界基函数数**，越过即误差骤变；拟合关系 **l ∝ m⁻¹**、**#Bases ∝ √m**。→ P1 若把 OTF 势场参数化为函数空间，**必须做同类的"函数空间复杂度 vs 采样数"扫描**，否则无法界定适用域。 |
| {FIG-DON-9} | Figure 9 | Learning a diffusion-reaction system. (A) (left) An example of a random sample of the input function u(x). (middle) The corresponding output function s(x, t) at P different (x, t) locations. (right) Pairing of inputs and outputs at the training data points. | (A) 训练数据构造：对每个 u 只在 100×100 网格中**随机取 P 个 (x,t) 点**；数据点总数 = P × #u；(B) 固定 #u=100 时误差随 P 先降后饱和；(C) 固定 P=100 时随 #u 变化。**"小数据也能学"的具体证据：100 个 u + P=1000 → 测试误差 ∼10⁻⁵（每个位置平均仅 10 个训练点）**。 |
| {FIG-DON-10} | Figure 10 | Error convergence rates for different number of training data points. (A) Convergence of test error with respect to P for different number of u samples. (B) Convergence of test error with respect to the number of u samples for different values of P. | (A) 对 P 的收敛率随 #u 从 **x^{−1.4} 增至 x^{−2.4}**；(B) 对 #u 的收敛率随 P 从 **x^{−2.6} 增至 x^{−3.7}**；(D)(E) 初始段的指数收敛 `e^{−x/k}`，k 随 #u/P 变化（1/k 从 0.04–0.2）；(C)(F) 给出 1/k 与收敛率的经验拟合式。**这些拟合式无置信带、无拟合优度。** |
| {TAB-DON-3} | Table 3 | Notations. | 符号表（X, R^d, K, C(K), V, u(x), s(x), f, G, (TW), σ, {x₁…x_m}, n/p, N, M）。**纯符号定义，无数据。** |

**（无 >13 项的情形；全文 10 图 3 表已全部覆盖。）**

## 6. 对 P1 的用处

- **与 P1 的关系**：**不同问题（远邻方法学）**。DeepONet 解决的是"**学一个从函数空间到函数空间的映射**"；P1 的 OTF 势场若被视为"由交通流状态场决定边界条件的 ODE 右端"，二者在**形式**上有交集（都是"输入是场/函数、输出是场/轨迹"），但本文的四个问题（一维反导数、一维非线性 ODE、重力摆、扩散-反应方程）与车辆动力学、编队、混行交通**没有一个相同**，也**完全没有控制回路**。

- **可迁移**：
  1. **"双网分解 + 显式归纳偏置"这一设计原则可迁移到 P1 的 OTF 条件化**：作者逐字写 —— "*Embodying some prior knowledge into neural network architectures usually induces good generalization. This inductive bias has been reflected in many networks … The success of DeepONet even using FNN as its sub-networks is also due to its **strong inductive bias**. The output G(u)(y) has two independent inputs u and y, and thus using the trunk and branch networks explicitly is consistent with this prior knowledge.*"（§2.1）。→ **P1 若把 OTF 势场作为条件模态，正确的写法是"OTF 是 inductive bias / structure prior"，而不是"physics-informed"**——本句可作为"**用架构而非损失项注入先验**"的已发表支撑，且与 `AGENTS.md` §1 的术语口径（structure-informed / prior-informed / boundary-conditioned）**完全一致**。
  2. **传感器数 vs 输入函数空间复杂度的定量关系（可直接引用的扫描范式）**：`m ∝ √T`、`m ∝ l⁻¹`、`l ∝ m⁻¹`、`#Bases ∝ √m`，以及"转折点 ∼10 个传感器"（Fig. 6）。→ P1 若要论证"OTF 势场需要多少个采样点/多少阶离散化才够"，**这是可照抄的实验设计模板**（扫 m × 扫函数空间复杂度 × 报告误差转折点）。
  3. **"评价协议三分解"的报告纪律**：本文把总误差拆成 **approximation / optimization / generalization** 三类并分别讨论（§1 引言，引 Bottou & Bousquet 等）。→ P1 报告 OTF-CfC 的跟踪误差时，可用同一框架区分"**模型容量不足**（逼近）/**训练不充分**（优化）/**泛化**"，避免把所有误差混成一个 RMSE。
  4. **小数据学习的具体量级参照**：扩散-反应问题上 **100 个输入函数 + P=1000 个位置点 → 测试误差 ∼10⁻⁵，平均每个位置仅 10 个训练点**。→ P1 若受限于实车数据量（学位论文数据集规模 `[待确认]`），这是"**输入函数的多样性比每个函数上的采样密度更重要**"（Fig. 9B vs 9C 的饱和行为）的已发表证据，可支撑 P1 的数据采集优先级（多场景、少重复 vs 少场景、多重复）。
  5. **误差随时长指数放大（MSE ∝ 8^T）可作 P1 长时域预测的风险锚点**：→ P1 若让模型做多步预测（而非单步控制），**必须报告预测时长 T 与误差的关系曲线**，否则"长时域"结论无效。

- **不可迁移 / 陷阱**：
  1. **★ 材料是预印本，不是正式版**：本 .txt 为 arXiv:1910.03193v3（2020-04-15），**无 NMI 刊头/DOI/卷期**；标题、作者数（3 vs 正式版 5）、图号都可能与 NMI 2021 正式版不同。→ **本卡的任何图号/数值都不得直接写进 P1 稿件**，必须先核正式版。
  2. **无控制、无车辆、无混行**：四个问题全是低维 ODE/PDE 数值基准；**没有任何控制器、反馈回路、稳定性或约束处理**。P1 不能引本文支撑任何控制性能主张。
  3. **参考解由数值求解器生成，不是实验数据**：ODE 用 Runge-Kutta (4,5)，PDE 用二阶有限差分；所有"数据"都是仿真产物。→ 证据级别为**纯数值仿真**，不构成任何工程可行性证据。
  4. **无参数量 / 无 FLOPs / 无硬件 / 无延迟**：Table 2 只给 trunk/branch 的深度与宽度（3×40, 2×40）。全文无 GPU/CPU 型号、无训练时长、无推理时延、无内存。"**未报告硬件**"是本文与 CfC（NMI 2022）共有的缺口。
  5. **不确定度报告极不完整**：只有 Fig. 2D、3B、4C、9B/C 提到 ±1 SD（Fig. 2D 与 Fig. 3B 为 10 次运行）；**Fig. 6/7/8/10 的图注明写不画 SD**。→ 那些"收敛率"数字（x^{−1.4}…x^{−3.7}、e^{−x/23} 等）**没有不确定度**，是曲线拟合值。
  6. **口径陷阱：数据集大小 ≠ 输入函数个数**。正文逐字："*a dataset of size 10000 may only be generated from **100 u trajectories**, and each evaluates G(u)(y) for 100 y locations*"。→ 引用"用 1 万条数据"会**高估**输入多样性 100 倍；P1 引用时必须写"100 个输入函数 × 100 个位置点"。
  7. **"首次观察到指数收敛"是作者主张**：正文写 "*To the best of our knowledge, this is the first time exponential convergence is observed in deep learning.*"——这是**未经检索证明的新颖性断言**，P1 若引用须标注"作者主张，未经本组检索核实"。

- **与 CfC（NMI 2022）的关系**：**互补，不同层面（不构成替代）**。
  - **无引文关系**：CfC（Hasani 等，NMI 2022）的参考文献与本文无交集；本文（arXiv 2020 定稿）也不可能引用 2022 年的 CfC。二者在文献图上**互不引用**。
  - **层面不同**：DeepONet 关心"**学到的是算子**（函数→函数映射）"，求解维度在**空间/参数空间**；CfC 关心"**学到的是时间连续的动力系统**（用闭式门控替代 ODE 求解器）"，求解维度在**时间**。一个是 operator learning，一个是 continuous-depth sequence model。
  - **对 P1 的联合含义**：OTF 势场天然是"**交通状态的函数**"（类 DeepONet 的输入函数）；把 OTF 作为边界条件注入连续时间控制器（类 CfC）在概念上是"**算子学习的条件模态 + 连续时间动力系统**"的组合。→ **但本文与 CfC 都没有做过这个组合，P1 若采用这一表述必须自行实验，不得引用任何一篇暗示该组合已被验证。**
  - **可复用的代码与库**：本文全部实现于 **DeepXDE**（`https://github.com/lululxvi/deepxde`，正文两处给出）。若 P1 需要"用算子学习给 OTF 势场做代理模型"，DeepXDE 是可核验的起点。**本卡未克隆或运行该仓库。**

- **引用时必须带的限定语**：
  "在 Lu 等关于 **DeepONet 算子学习**的工作中（Nature Machine Intelligence 2021;3(3):218–229，DOI 10.1038/s42256-021-00302-5），全部证据为**四个低维 ODE/PDE 数值基准**（一维反导数、一维非线性 ODE g=−s²+u、重力摆、扩散-反应方程），参考解由 **Runge-Kutta (4,5) 与二阶有限差分**生成而**非实验数据**；输入函数限于 **GRF(RBF 核，l=0.2) 与 Chebyshev 多项式**两个紧函数空间，传感器数 m=100；**无控制器、无闭环、无硬件、无参数量/FLOPs/延迟报告**；误差的 ±1 SD 仅在 Fig. 2D/3B/4C/9 给出（10 次不同训练/测试数据与初始化），**收敛率拟合（x^{−0.5}…x^{−3.7}、e^{−x/k}）均无不确定度**；非线性 ODE 的测试 MSE **剔除了最差 1‰ 预测**；**本组所核验的文本为 arXiv:1910.03193v3（2020-04-15）预印本，未与 NMI 2021 正式版逐条比对**。（另：预印本作者为 3 人，正式版为 5 人，含 Pang G 与 Zhang Z。）"

- **P1 落地三问**：
  1. **是否有硬件实测？** **无。** 全文无 GPU/CPU 型号、无训练时长、无推理时延、无内存占用、无任何嵌入式/实时性内容（对本地 .txt grep `MCU|microcontroller|Jetson|Raspberry|FPGA|latency|real-time` **零命中**）。唯一与"计算"有关的信息是 Table 2 的层宽/深度与 Table 1 的迭代次数（50,000 / 100,000 次）。
  2. **是否报告参数量？** **无。** 只有 Table 2 的 **trunk depth 3 / width 40（问题 4.3 为 100）、branch depth 2 / width 40（4.3 为 100）**，以及 §2.1 的原则性说明"**p 至少是 10 的量级**"（"in practice, p is at least of the order of 10"）。→ 无法估算任何参数预算；**无"是否含感知头"的问题**（本文无感知模块）。
  3. **训练是在线还是离线？** **离线。** 全部为批量训练（Adam，学习率 0.001，"迭代次数取到训练收敛为止"），数据集预先由数值求解器生成（10,000 至 1,000,000 个训练点）。**无任何在线/增量学习内容**；**训练内存与时间完全未报告**。

## 7. 缺失信息（≥3 条，写成可执行动作）
1. **★ 必须取回 NMI 2021 正式版并逐条复核版本差异**（标题、作者、章节编号、图号、Table 1–3 数值、§4.3 的收敛率）。→ 动作：以 DOI 10.1038/s42256-021-00302-5 取正式版 PDF，比对本地 arXiv v3 的 10 图 3 表与全部数字；**差异表须写入本卡**。**在这之前，本卡的所有图号/数值不得进入 P1 稿件。**
2. **需作者提供参数量 / FLOPs / 训练与推理时间**（每个问题、每个网络规模）。（后果：无法判断 DeepONet 的误差优势是否只是"同误差下参数更多/更少"；P1 也无法据此估算任何资源预算。）
3. **需作者提供各图不确定度的完整口径**：Fig. 6/7/8/10 明确不画 SD，其"收敛率"（x^{−0.5}…x^{−3.7}、e^{−x/23} 等）是**单次曲线拟合**还是多次平均？（后果：这些收敛率是本文最常被引用的数字之一，无不确定度则**不可作为"训练数据量—误差"的定量标定**。）
4. **需作者澄清 Theorem 2 的实用性与"松界"的量化程度**：正文自承 "Te^{cT} in the bound is **loose** compared to the computational results"。（后果：P1 若想用该定理做"传感器数够用"的论证，须知道松多少；目前只有计算实验可作为依据。）
5. **需作者说明 GRF / Chebyshev 两个函数空间与实际工程输入分布的差距**：本文全部结论建立在"输入函数取自均值零 GRF（RBF 核）或 Chebyshev 多项式、且落在紧集内"。（后果：**P1 的 OTF 势场是否属于该类紧函数空间、是否满足 Lipschitz 条件，需自行论证**；不得默认可迁移。）
6. **需核验 DeepXDE 仓库与论文表格的一致性**（本卡未克隆、未运行）：至少复现 Fig. 3B 的"unstacked + bias 优于 stacked"与 Fig. 6A 的"转折点 ∼10 传感器"两处。→ 动作：跑通 `github.com/lululxvi/deepxde` 的对应示例并记录 commit 与日期。
7. **需做 T2 取代检查**：检索 2021 年后 DeepONet 的改进（如 POD-DeepONet、MIONet、DeepONet 的误差理论）是否取代本文的收敛率结论。→ 动作：OpenAlex/Crossref 检索并记录检索式与日期（本卡未做，标 `[待核实]`）。

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| FNN 学习反导数算子的最优测试误差 | **∼10⁻⁴**（depth 2, width 2560, lr 0.001） | 图 2D 给 ±1 SD（10 次运行）；其余 lr 无 | Fig. 2 + §4.1.1 |
| FNN 超参搜索范围 | depth **2–4**；width **10–2560**；lr **0.0001–0.01** | — | §4.1.1 |
| 非线性 ODE 的"训练—测试"经验关系 | `MSE_test ≈ 10 × MSE_train − 10⁻⁴` | 10 次随机运行（Fig. 4B） | Fig. 4B + §4.1.2 |
| 非线性 ODE 测试误差口径 | **剔除最差 1‰ 预测** | — | §4.1.2 |
| 传感器数—误差关系（重力摆，k=1,T=1,l=0.2） | `MSE ∝ 4.6^{−#sensors}` | 图注明写 **SD 未画** | Fig. 6A |
| 传感器数转折点 | **∼10 个传感器**（此后增 m 的收益可忽略） | 无 | Fig. 6A（箭头） |
| 预测时长—传感器数关系 | `m ∝ √T`；T=5 需 **∼25 个传感器**；100 个传感器足够 T=5 | 无 | §4.2.1 + Fig. 6B |
| 长度尺度—传感器数关系 | `m ∝ l⁻¹`（与附录 C 的理论一致） | 无 | §4.2.1 + Fig. 6C + Appendix C |
| 参数 k 的影响 | **对传感器数不敏感** | 无 | Fig. 6D |
| 预测时长—误差关系 | `MSE ∝ 8^T`（且为 [0,T] 上的平均误差，非 T 点误差） | 无（width 40、数据 10000 固定） | Fig. 7A + §4.2.2 |
| 最优网络宽度 | 存在最优宽度（**width 100 附近**），超过后误差回升（作者归因于优化误差） | 无 | Fig. 7B |
| 数据量—测试误差收敛律 | 小数据集 `MSE_test ∝ e^{−x/2000}`；大数据集 `MSE_test ∝ x^{−0.5}` | 无 | Fig. 7C + §4.2.2 |
| 数据量—泛化误差收敛律 | 小数据集 `MSE_gen ∝ e^{−x/2000}`；大数据集 `MSE_gen ∝ x^{−1}`（**优于经典学习理论的 x^{−0.5}**） | 无 | Fig. 7D + §4.2.2 |
| 函数空间临界关系 | `l ∝ m⁻¹`；`#Bases ∝ √m` | 无 | Fig. 8 + §4.2.3 |
| 扩散-反应问题：小数据表现 | **100 个 u 样本（P=1000）→ 测试误差 ∼10⁻⁵**；测试用 10000 个网格点，**平均每位置仅 10 个训练点** | Fig. 9B/C 给 ±1 SD | §4.3 + Fig. 9 |
| 收敛率 vs 位置点数 P | 随 #u 从 **x^{−1.4}**（#u=50）增至 **x^{−2.4}**（#u=200/400） | 无 | Fig. 10A |
| 收敛率 vs 输入函数数 #u | 随 P 从 **x^{−2.6}**（P=50）增至 **x^{−3.7}**（P=400） | 无 | Fig. 10B |
| 初始段指数收敛系数 | 对 P：`e^{−x/23} / e^{−x/13} / e^{−x/10} / e^{−x/7.6}`；对 #u：`e^{−x/16} / e^{−x/10} / e^{−x/9.2} / e^{−x/9.0}` | 无 | Fig. 10D/E |
| 1/k 的经验拟合 | `1/k ≈ 0.04·ln(x) − 0.1`；`1/k ≈ 0.1 − 0.2·e^{−x/37}`（x 为 #u 或 P） | 无 | Fig. 10C/F |
| 默认传感器数 m | **100**（四个问题除特别说明外） | — | Table 1 |
| 训练/测试点数 | 4.1.1 & 4.1.2 & 4.2：**10,000 / 100,000**；4.3：**1,000,000 / 500,000** | — | Table 1 |
| 迭代次数 | 4.1.1 **50,000**；4.1.2 **100,000**；4.2 **100,000**；4.3 未列 | — | Table 1 |
| DeepONet 网络规模 | Trunk depth **3** / width **40**（4.3 为 100）；Branch depth **2** / width **40**（4.3 为 100） | — | Table 2 |
| branch 输出维 p 的量级 | "in practice, p is **at least of the order of 10**" | — | §2.1 |
| 优化器与学习率 | **Adam，lr = 0.001**（全部问题）；迭代数取到训练收敛 | — | §4 首段 |
| 数据生成方式 | u 采样自 **GRF(0, RBF 核，l=0.2)** 或 **Chebyshev 多项式**；ODE 用 **Runge-Kutta (4,5)**，PDE 用**二阶有限差分**求解得到参考解 | — | §2.2 |
| 扩散-反应方程参数 | D = **0.01**（扩散系数），k = **0.01**（反应率）；100 × 100 网格 | — | §4.3 |
| 重力摆参数（主实验） | k = 1，T = 1，l = 0.2 | — | Table 1 + §4.2.1 |
| 代码库 | **DeepXDE**（`https://github.com/lululxvi/deepxde`），Python | — | §2.1 + §4 首段 |

⚠内部不一致 1：正文 §5 Conclusion 写 "*We test DeepONets on **four** ordinary/partial differential equation problems*"，与 §4 的四小节（4.1 一维动力系统含 4.1.1 线性 + 4.1.2 非线性两个子例、4.2 重力摆、4.3 扩散-反应）**在计数上口径不一**：若把 4.1.1/4.1.2 视为两个问题则为 4 个，视为一个"一维动力系统"则只有 3 个。引用"四个问题"时须注明该计数方式。

⚠内部不一致 2（版本层面）：本地 PDF 第 1 页标题为 "**DeepONet: Learning nonlinear operators for identifying differential equations based on the universal approximation theorem of operators**" 且作者 **3 人**，而正式版（Crossref 核验）标题为 "**Learning nonlinear operators via DeepONet based on the universal approximation theorem of operators**" 且作者 **5 人**（增 Pang G、Zhang Z）。→ **同一工作两个版本在标题与作者数上均不一致**，属预印本—正式版差异，引用必须锁定版本。

【确定】/【待核实】标注：以上数值均为本地 .txt（arXiv v3）印出值【确定】；正式版一致性 **`[待核实]`**（未取正式版）；"首次观察到指数收敛"为**作者主张**，未经本组检索核实 **`[待核实]`**。
