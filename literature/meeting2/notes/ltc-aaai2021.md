# 液态时间常数网络（LTC）｜Liquid Time-Constant Networks

- **出处**：Proceedings of the AAAI Conference on Artificial Intelligence 35(9):7657–7666, 2021 ｜ **类型**：会议论文
- **作者**：Hasani R, Lechner M, Amini A, Rus D, Grosu R（MIT / IST Austria / TU Wien）
- **DOI**：10.1609/aaai.v35i9.16936 —— **PDF 内未见 DOI 字样**（两版 grep `doi` 均为 0 命中）；由项目既有核验取得，见 `literature/dois_appendix_checked.json`（n=102），并于 **2026-10-04** 用 Crossref `api.crossref.org/works/10.1609/aaai.v35i9.16936` 直查复核：volume 35 / issue 9 / page 7657-7666 / published 2021-05-18，`update-to`、`updated-by`、`relation` 均为空 → **Crossref 无撤稿/更正登记**。
- **全文来源**：
  - **主用 = 正式版（VoR）**：`literature/fulltext/meeting2/ltc-aaai2021-VoR__0f06995f.txt`（PAGES=10，UTF-8 字符 48,669，MD5 `0f06995fba06dbcfa7ed965fc66027ff`，来源 `https://ojs.aaai.org/index.php/AAAI/article/download/16936/16743`）
  - **对照 = arXiv 版**：`literature/fulltext/meeting2/ltc-aaai2021__5ea4332a.txt`（PAGES=25，MD5 `5ea4332ad26a85c0de9767fab95aa365`，内含 arXiv:2006.04439v4 版本戳；任务给定 CHARS=92,938，**实测 UTF-8 字符 96,695**，按 CRLF→LF 归一为 93,053 —— 见文末「材料问题」）
- **分组**：连续时间 / 流体神经网络（P1 控制器的方法学底座；P1 消融 A2 中 LTC 一臂的定义来源）
- **★ 版本与材料核验**：

  **Q1 两份材料的版本判定（逐条证据）**
  | 材料 | 判定 | 逐字证据（位置） |
  |---|---|---|
  | `ltc-aaai2021-VoR__0f06995f.txt`（10 页） | **AAAI-21 正式版（Version of Record）** | ① 页眉逐字：「The Thirty-Fifth AAAI Conference on Artificial Intelligence (AAAI-21)」（提取文本中该页眉只出现在第 1 页 = txt 第 111 行，其余 9 页仅提取到页码）；② 页脚逐页递增页码 **7657–7666**（txt 第 112/239/384/479/641/919/1084/1202/1321/1402 行，10 页 10 个号）；③ 版权行逐字：「Copyright c⃝2021, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.」（第 1 页）；④ **无 `arXiv:` 版本戳**：全文 `arXiv` 共 **24 次**、分布在 **19 行**内，**全部落在第 9–10 页的参考文献段**（首次出现位置已在 References 标题之后），无一处是版本戳（如 "arXiv preprint arXiv:1606.01540 ."）；⑤ `AAAI` 在 PDF 内容中仅 **3 次**：第 1 页页眉「…(AAAI-21)」（2 次）+ 版权行「www.aaai.org」（1 次）；⑥ 无 `Supplementary`/`Appendix` **正文段**（仅正文 8 处引用，见下 Q2）。 |
  | `ltc-aaai2021__5ea4332a.txt`（25 页） | **arXiv:2006.04439v4 的 PDF（作者排版版，带 AAAI-21 版权行）**，**含完整补充材料** | ① 第 1 页逐字版本戳：「arXiv:2006.04439v4 [cs.LG] 14 Dec 2020」（txt 第 110 行）；② 第 1 页同一版权行（「Copyright © 2021, Association for the Advancement of Artificial Intelligence…」）；③ **无 AAAI 页眉与 7657–7666 页码**（`7657`/`7666` 均 0 命中），正文未编号卷期；④ 第 10 页起逐字「Supplementary Materials」（txt 第 1433 行）至第 25 页末。 |
  | **哪份是哪版** | VoR = AAAI 正式版 10 页（= 印刷页 7657–7666）；arXiv 版 = 同一稿的**作者版 + 完整补充材料**（25 页）。 | 两版**数值完全一致**（见 Q8），差异在**体量与措辞**，不在结果。 |
  | arXiv 版附加核验（2026-10-04，arXiv API `export.arxiv.org/api/query?id_list=2006.04439`） | 该条目**最新版即 v4**（无 v5），首次提交 2020-06-08，v4 更新 2020-12-14 —— 与 PDF 内版本戳一致。 | 路径 `http://arxiv.org/abs/2006.04439v4`。 |

  **Q2 图号与表号全集**
  - **正式版（VoR）：4 个 Figure + 6 个 Table = 10 项**。Figure 1–4（p.7660 / 7661 / 7662 / 7664）；Table 1–6（p.7659 / 7660 / 7663 / 7663 / 7663 / 7664）。式号 **(1)–(9)**。
  - **arXiv 版补充材料：Table S1–S2、Figure S1**（无 S3 及以后的图表），章节 **S1–S9**，公式 **(S1)–(S120)**，位于第 10–25 页（Table S1/S2 在第 24 页，Figure S1 在第 25 页）。
  - ⚠ **正式版不含 Appendix**：VoR 正文 **8 处**引用它 —— **p.7659 ×2**：「The proof is provided in Appendix.」（Theorem 1 后）、「The proof is given in Appendix.」（Theorem 2 后）；**p.7662 ×3**：「The proof is provided in Appendix. It follows similar…」（Theorem 4 后）、「The proof is provided in Appendix. A rough outline…」（Theorem 5 后）、Fig. 3 图注「(More results in the supplements)」；**p.7663 ×3**：「The experimental setup are provided in Appendix.」、「(details in Appendix)」、「(See supplements)」。**但 10 页 VoR 到 7666 页即为参考文献末页，无任何附录**。故**证明、实验设置、超参表（S1）、参数量表（S2）、Figure S1 在正式版中缺席，只在 arXiv 版可得**。

  **Q3 LTC 的动力学定义式（正式版）与时间常数项**
  - **式 (1)**（正式版第 1 页；VoR txt 第 73–81 行）逐字：
    > dx(t)/dt = −[1/τ + f(x(t), I(t), t, θ)] x(t) + f(x(t), I(t), t, θ) A.  (1)
  - 构造过程逐字（同页）：「let the hidden state flow of a network be declared by a system of linear ODEs of the form: dx(t)/dt = −x(t)/τ + S(t), and let S(t) ∈ R^M represent the following nonlinearity determined by S(t) = f(x(t), I(t), t, θ)(A − x(t)), with parameters θ and A.」
  - **时间常数项 τ_sys**（同页 "Liquid Time-Constant" 段）逐字：
    > "A neural network f not only determines the derivative of the hidden state x(t), but also serves as an input-dependent varying time-constant (τsys = τ / (1+τf(x(t),I(t),t,θ))) for the learning system (Time constant is a parameter characterizing the speed and the coupling sensitivity of an ODE)."
  - **状态依赖的写法 = A − x(t)**（上式的乘子），即 f 同时进入"变时间常数"与"对偏置向量 A 的状态依赖驱动"两项。
  - 有界性：Theorem 1 式 (4)「τi/(1 + τiWi) ≤ τsys_i ≤ τi」（p.7659）；Theorem 2 式 (5)「min(0, A^min_i) ≤ xi(t) ≤ max(0, A^max_i)」（p.7659）。证明建立在「a bounded, monotonically increasing sigmoidal nonlinearity for neural network f」之上 —— 即**有界性结论只对 sigmoid 类激活成立**（Table 2 显示 ReLU/Hard-tanh 下 LTC 的计算深度高达 56.9 / 81.01）。

  **Q4 是否需要 ODE 求解器？求解器 / 步长 / 训练方法（逐字）**
  - **需要，且是本文的核心工程贡献之一。** Abstract 逐字（p.7657）：「…with outputs being computed by **numerical differential equation solvers**.」
  - 不可解析：p.7658 逐字「**Solving Eq. 1 analytically, is non-trivial** due to the nonlinearity of the LTC semantics.」
  - **求解器 = 自研 "Fused" 固定步长求解器（显式 + 隐式 Euler 融合）**。p.7658 逐字：「LTCs' ODE realizes a system of **stiff** equations (Press et al. 2007). This type of ODE requires an exponential number of discretization steps when simulated with a Runge-Kutta (RK) based integrator. Consequently, ODE solvers based on RK, such as Dormand–Prince (default in torchdiffeq (Chen et al. 2018)), are **not suitable for LTCs**. Therefore, we design a new ODE solver that **fuses the explicit and implicit Euler methods**.」
  - 更新式：式 (2)「x(ti+1) = x(ti) + ∆t f(x(ti), x(ti+1))」；式 (3)「x(t + ∆t) = [x(t) + ∆t f(x(t),I(t),t,θ) A] / [1 + ∆t(1/τ + f(x(t),I(t),t,θ))]」（p.7658）；伪码 **Algorithm 1**（同页，参数含 `L = Number of unfolding steps`、`∆t = step size`）。
  - **步长策略 = 固定步长**。第 1 页逐字：「In Section 2, we introduce a practical **fixed-step** ODE solver that simultaneously enjoys the stability of the implicit Euler and the efficiency of the explicit Euler methods.」→ 具体数值**只在 arXiv 版**：S5 逐字「All ODE solvers were **fixed-step** solvers. The time-step is set to **1/6 of the input sampling frequency, i.e., each RNN step consists of 6 ODE solver steps**.」（arXiv p.22）**正式版未印此设置**。
  - **训练 = vanilla BPTT（直接反传），明确不用伴随法**。第 1 页逐字：「We settle to trade memory for numerical precision during a backward-pass by using a **vanilla backpropagation through-time algorithm** to optimize LTCs **instead of an adjoint-based optimization method** (Pontryagin 2018).」；p.7658–7659 逐字：「The adjoint method, however, comes with numerical errors when running in reverse mode…」；**Algorithm 2**；**Table 1**（p.7659）逐字：Vanilla BPTT「Time O(L × T × 2) / Memory O(L × T) / Depth O(L) / FWD acc High / BWD acc High」vs Adjoint「Time O((Lf + Lb) × T) / Memory O(1) / Depth O(Lb) / FWD acc High / BWD acc Low」；同页结论逐字「…with similar computational complexity, **at large memory costs**.」；优化器 = Adam（p.7659「such as Adam (Kingma and Ba 2014), which we use in our experiments」）。

  **Q5 是否已提出 NCP？是否出现 CfC 的闭式解？（划界）**
  - **NCP：正式版未提出。** 两版 grep `NCP` **均 0 命中**；`neural circuit` 两版**各 2 次且全部是参考文献语境**（其中一次即 NCP 那篇的题名「Neural circuit policies enabling auditable autonomy」，另一次是文献里 "learning with ordinary neural circuits" 之类的一般说法），**无一处是本文自提的概念**。NCP 以**参考文献条目**出现在 VoR 第 10 页文献表，逐字：「Lechner, M.; Hasani, R.; Amini, A.; Henzinger, T. A.; Rus, D.; and Grosu, R. 2020a. **Neural circuit policies enabling auditable autonomy**. Nature Machine Intelligence 2(10): 642–652.」并在结论"未来方向"句被引一次（p.7664）。→ **NCP 是 LTC 的下游应用/平行工作（NMI 2020），不是本文贡献**；本文贡献是 LTC 这一**神经元动力学**。
  - **CfC 的闭式解：两版均 0 命中**（grep `closed-form`、`closed form`、`CfC` 全部 0）。**核实结论：不出现。** 本文立场恰与 CfC 相反——逐字「Solving Eq. 1 analytically, is non-trivial」（p.7658），并因此**必须数值求解**；CfC（NMI 2022）所做的正是补上这个闭式近似并取消求解器。**这是 LTC→CfC 最硬的方法学分界。**
  - 附：本文把 CT-RNN 与 ODE-RNN 画等号，逐字（p.7663）：「the CT-RNN architecture is equivalent to the ODE-RNN described in (Rubanova, Chen, and Duvenaud 2019), with the difference of having a state damping factor τ.」→ **对 P1 的 A2（LNN vs CfC vs 普通 ODE-RNN）直接有用：CT-RNN ≡ ODE-RNN + 阻尼 τ。**

  **Q6 是否报告参数量？**
  - **正式版：全文未见任何参数量。** VoR grep `parameter` 命中处全部是「time-constant 参数」「参数空间 θ」「parameter efficiency」（Related Works 的一般说法）等，**无一处给出模型规模**。
  - **arXiv 版：只给"公式"，不给任何具体模型的实际参数数。** Table S2（arXiv p.24）表头逐字：「Number of parameters of various RNN model in relation to the RNN width k, the number of hidden layers n, and the number of decay slots m.」表内逐字：CT-RNN `O(nk²)` / `nk² + 2nk`；ODE-RNN `O(nk²)` / `nk² + nk`；LSTM `O(nk²)` / `4nk² + 4nk`；CT-GRU `O(mk²)` / `2mk² + 2mk + k² + k`；**LTC `O(nk²)` / `4nk² + 3nk`**。
  - 实验规模逐字（arXiv Table S1 与 S5）：「Number of hidden units 32」；「Each RNN consists of 32 hidden units.」→ **代入 n=1、k=32 复算（本卡算术，非论文印出值）**：LTC = 4·32² + 3·32 = **4,192**；ODE-RNN = 1,056；LSTM = 4,224；CT-RNN = 1,088。

  **Q7 是否报告任何硬件 / 时延 / 内存？**
  - **两版均"全文未见"。** grep `GPU`/`CPU`/`NVIDIA`/`Titan`/`Jetson`/`MCU`/`microcontroller`/`embedded`/`latency`/`runtime`/`FLOP`/`KB`/`MB`/`footprint` = **0 命中**；**无单步时延、无内存占用、无功耗、无精度档位（fp32/fp16）、无计时协议、无 batch-size-for-timing**。
  - 唯一平台字样只在 arXiv 版 S5（p.22）逐字：「We implemented all RNN models in **TensorFlow1.14**.」**正式版连这句都没有。**
  - 与"资源"相关的**唯一**表述是定性自承，p.7664 逐字：「Our proposed model, in their current format, significantly enhances the expressive power of TC models at the expense of **elevated time and memory complexity which must be investigated in the future**.」（VoR 与 arXiv 同句。）
  - **代码/数据可用性：正式版已删除该声明。** arXiv 版第 1 页脚注逐字「1Code and data are available at: https://github.com/raminmh/liquid time constant networks」、S9 逐字「All code and data are publicly accessible at: https://github.com/raminmh/liquid time constant networks.」，但**VoR grep `github` = 0 命中**。（本卡**未克隆该仓库**，未核验其与论文表格一致。）

  **Q8 正式版与 arXiv 版的结果数值是否一致？（逐表比对）**
  - **数值完全一致。** 机器比对（归一化后取多重集）：全部 **65 行 `mean ± SD` 数值行**（Table 2、3、4、5、6）两版**完全相同、无一行差异**；Figure 2 的 **36 个 `l(N-ODE)/l(CT-RNN)/l(LTC) = …` 轨迹长度值**两版**完全相同**（如 `l(LTC) = 266.2873` / `527.0816` / `53858.6441` / `17707.2484`）。
  - **arXiv 有而正式版"省略"的表**：**Table S1**（Hyperparameters）、**Table S2**（参数量公式）、**Figure S1**（Additional trajectory length results）—— 以及承载它们的整个 S1–S9 附录（全部定理证明、实验设置、代码可用性声明）。**正式版省略（且正文仍引用）。**
  - 两版**措辞层面**的差异（不影响数字，但影响逐字引用）：① 标题 **VoR「Liquid Time-Constant Networks」** vs arXiv「Liquid Time-constant Networks」；② VoR「We refer to these models as liquid time-constant **networks** (LTCs)」vs arXiv「…liquid time-constant **recurrent neural networks** (LTCs)」；③ VoR「We extend these criteria to **the CT family**.」vs arXiv「…to the family of continuous-time recurrent models.」；④ VoR「…variants of continuous-time (CT) models **that show great expressivity**」vs arXiv「…that **are loosely inspired by biology**, show great expressivity」；⑤ VoR 增补参考文献 (Sarma et al. 2018; Gleeson et al. 2018)；⑥ Intro 提问句 VoR 止于「…enable better representation learning?」vs arXiv「…richer representation learning and expressiveness?」；⑦ 结论首句 VoR「**We introduced liquid time-constant networks.**」vs arXiv「We investigated the use of a novel class of time-continuous neural network models…」；⑧ **VoR 的小节标题为 AAAI 式无编号 Title Case**（"Experimental Evaluation"、"Conclusions, Scope and Limitations" 等），arXiv 版为 1–8 编号；⑨ **⚠ 正式版 Figure 2 图注把 D/E 面板定义互换**：VoR「D) as a function of width (Hard-tanh), and E)in network layers with logistic-sigmoid activations.」vs arXiv「D) in network layers with logistic-sigmoid activations and E) as a function of width (Hard-tanh).」，正文交叉引用随之整体互换（VoR「(Fig. 2A, 2C and 2D)」/「(Fig. 2B to 2D)」/「(Fig. 2E)」 vs arXiv「2A, 2C and 2E」/「2B to 2E」/「(Fig. 2D)」）——**两版必有一版的面板标签与图内实际曲线不符，本卡无法从纯文本判定哪版正确**；⑩ VoR 在 Experimental Evaluation 前新增一句「In this section, we evaluate the performance of the LTCs compared to the state-of-the-art RNN models in a series of time-series benchmarks.」

- **证据等级初判**：**B 级** — 正式版全文可得、含 5 条定理（证明在 arXiv 版附录）、主要结果表（Table 3/4/6）的基线**未见"取自他文"表注**（与 CfC 论文大量跨论文拼接基线形成对比）并报 mean±SD（n=5）；但**全部为离线有监督序列建模，零闭环控制、零实车/硬件、零显著性检验、零 CI、无种子**，且 P1 七项控制指标（跟车 RMSE、加速度平方积分、Jerk、车道居中、前轮转角方差、端到端延迟、MCU 内存）**一项都没有** → 不足以支撑 A 级的"足够功效 + 效应量与 CI"。**【确定】**

- **档位建议**：**A 精读** — D1=2：它是 P1 消融 A2 中 **LTC 一臂的定义来源**，且 Table S2 的参数律（LTC `4nk²+3nk` vs ODE-RNN `nk²+nk`）与"每步 6 个求解步"协议正是 A2 做**等参数/等计算预算公平对照**所必需的两项输入。⚠ **但协议 §4 的 A 档 5 篇预算已满**：LTC 若判 A 需按 §5 破平或占用追加名额（本卡按用户指令做 15 分钟精读，档位仅作记录）。**【确定】**

- **五维打分（按 `00-triage-protocol.md` §5，各维 0–2，满分 20）**：D1=**2** D2=**2** D3=**1** D4=**1** D5=**2** → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = 6+4+2+1+4 = **17**
  - D1=2：给出 P1 所需**控制器方法本体**（LTC 动力学式 (1)）与**可被 A2 直接复用的协议**（参数量律、求解器步数、训练协议）。
  - D2=2：有对照（同宽 32 隐藏单元、多基线、自跑）+ 有统计（n=5，mean±SD）+ 定理证明；**但无实车、无闭环**。
  - D3=1：架构/求解器/训练协议可搬进 A2 的 LTC 臂；**数据（10 项基准）与任务协议与 P1 无关**，代码仅"声明可得"未核验。
  - D4=1：**时效性**。出版 2021-05-18 → 本次核验 2026-10-04 = **5 年 4 个月 16 天**，落入 5–15 年档（非 ≤5 年）。
  - D5=2：全文 + 效应量（全部结果带 mean±SD）+ 复现材料（arXiv 版附录含全部证明、超参表 S1、参数律表 S2，另有代码可得性声明）。
  - **敏感性（口径记录，不改结论）**：D2 若按"必须有实车/闭环"的严口径记 1 → 15；D5 若只认 10 页正式版（无附录、无超参表、无参数量表、无代码声明）记 1 → 15；两者同时取严口径 → **13（B 档）**。三种口径下 D1=2、D5≥1 均成立，主口径 17 落在 **A 档（≥14）**。

---

## 1. 标题

**Liquid Time-Constant Networks**（正式版 VoR 第 1 页逐字；arXiv 版作 *Liquid Time-constant Networks*）｜中文直译：**液态时间常数网络**

## 2. 摘要（≤400 字中文）

作者提出液态时间常数网络（LTC）：把连续时间 RNN 的隐藏状态写成"线性一阶动力学 + 由神经网络 f 调制的非线性门"，即式 (1) `dx/dt = −[1/τ + f(x,I,t,θ)]x + f(x,I,t,θ)A`，使网络**时间常数随输入变化**（τ_sys = τ/(1+τf)），并证明 τ_sys 与状态均有界（Theorem 1/2，式 (4)(5)），输入无界增长时输出不爆炸。该式**无法解析求解**：作者指出 LTC 是刚性 ODE，RK 类求解器（含 torchdiffeq 默认的 Dormand–Prince）不适用，故自研**融合显式与隐式 Euler 的固定步长 Fused 求解器**（式 (2)(3)、Algorithm 1），并用 **vanilla BPTT 而非伴随法**训练（Table 1：BPTT 内存 O(L×T)、反向精度 High；伴随法内存 O(1)、反向精度 Low）。表达能力用"轨迹长度"度量，证明 LTC 下界随深度×求解步数 L 指数增长（Theorem 5，式 (9)），并在 10 项时间序列任务上与 LSTM、CT-RNN（≡ODE-RNN+阻尼 τ）、Neural ODE、CT-GRU 对比（n=5，mean±SD）：7 项中 4 项更优、3 项相当，作者称"提升 5%–70%"。**全部结果均为离线有监督序列建模，无闭环控制、无硬件、无时延与内存数据。**

## 3. 结论（≤350 字中文）

作者结论：LTC 可由任意变步长/固定步长 ODE 求解器实现、可用 BPTT 训练，并展示了有界稳定动力学、更强的表达能力与在有监督时间序列任务上超过标准与现代深度模型的性能。关键数字：Person Activity 第二设定 **0.882 ± 0.005**（最强基线 Latent ODE(C enc.) 0.846 ± 0.013，且带 ∗ 的基线值**直接取自 Rubanova et al. 2019**）；Half-Cheetah MSE **2.308 ± 0.015**（LSTM 2.500 ± 0.140、Neural ODE 3.805 ± 0.313）；Person Activity 第一设定 **85.48% ± 0.40**（CT-GRU 85.27% ± 0.39）。**作者自承的局限**：① 与多数连续时间模型一样存在梯度消失，**不是**学习长期依赖的显然选择；② 性能强烈依赖数值实现——换成现成的显式 Euler 会显著退化；③ 表达能力提升**以更高的时间与内存复杂度为代价**，须留待未来研究；④ 因果性只是未来方向。⑤ 正文称"a series of eleven time-series prediction experiments"，而全部结果表只支持 10 项。

## 4. 方法一句话

多维序列 I(t) → 状态依赖时间常数的 LTC 微分方程（式 1），Fused 固定步长求解器展开、BPTT 训练 → 预测/分类输出。

## 5. 图表清单（占位符）

正式版共 **4 Figure + 6 Table = 10 项**；arXiv 版另有补充 **Table S1–S2 + Figure S1 = 3 项**。合计 **13 项，全部收录**（未超 14）。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {TAB-LTC-1} | Table 1（VoR p.7659） | Complexity of the vanilla BPTT compared to the adjoint method, for a single layer neural network f. Note: L = number of discretization steps, Lf = L during forward-pass. Lb = L during backward-pass. | **BPTT vs 伴随法的唯一量化对照**：Memory O(L×T) vs O(1)、BWD acc High vs Low。P1 的 A2 若用 BPTT 训练 LTC 臂，这就是内存代价的出处。⚠ 只有复杂度阶，**无任何实测**。 |
| {TAB-LTC-2} | Table 2（VoR p.7660） | Computational depth of models. Note: # of tries = 100, input samples' ∆t = 0.01, T = 100 sequence length. # of layers = 1, width = 100, σ²w = 2, σ²b = 1. | LTC 的计算深度随激活函数剧烈变化：tanh 9.19 / sigmoid 7.00 / ReLU 56.9 / Hard-tanh 81.01。**求解步数 L 直接乘进计算量与内存** → 选激活函数就是选实时性预算。 |
| {FIG-LTC-1} | Fig. 1（VoR p.7660） | Trajectory's latent space becomes more complex as the input passes through hidden layers. | 轨迹长度度量的示意图（6 层、宽度 100、tanh）。概念图，无可引用数字。 |
| {FIG-LTC-2} | Fig. 2（VoR p.7661） | Trajectory length deformation A) in network layers with Hard-tanh activations, B) as a function of the weight distribution scaling factor, C) as a function of network width (ReLU), D) as a function of width (Hard-tanh), and E)in network layers with logistic-sigmoid activations. | 图内印出 36 个 l(·) 值（如 Width=200 时 l(LTC)=527.0816 vs l(N-ODE)=110.943）；**⚠ 正式版与 arXiv 版的 D/E 面板定义互换，交叉引用亦互换**。 |
| {FIG-LTC-3} | Fig. 3（VoR p.7662） | Dependencies of the trajectory length measure. A) trajectory length vs different solvers (variable-step solvers). RK2(3): Bogacki-Shampine Runge-Kutta (2,3)… D) trajectory length vs layers. (More results in the supplements) | **A) 是"轨迹长度对求解器不敏感"的证据**（RK2(3)/RK4(5)/ABM1(13)/TR-BDF2）；B/C/D 分别对宽度、权重方差、层数。**"对求解器不敏感"≠"对求解步数不敏感"**，引用时勿混。 |
| {TAB-LTC-3} | Table 3（VoR p.7663） | Time series prediction. Mean and standard deviation, n=5 | 7 项任务 × 5 模型。LTC 在 Gesture(69.55%)、Occupancy(94.63%)、Traffic(0.099)、Ozone(0.302) 最优；在 Activity recognition(95.67% < 97.26%)、Sequential MNIST(97.57% < 98.41%)、Power(0.642 > 0.586) **不如基线**。 |
| {TAB-LTC-4} | Table 4（VoR p.7663） | Person activity, 1st setting - n=5 | LTC 85.48%±0.40 最优，但仅领先 CT-GRU 0.21 个百分点，而两者 SD 为 0.40 / 0.39 → **差距远小于噪声，不能称"更优"**。 |
| {TAB-LTC-5} | Table 5（VoR p.7663） | Person activity, 2nd setting, n=5 Note: Accuracy for algorithms indicated by ∗, are taken directly from (Rubanova, Chen, and Duvenaud 2019) with: RNN ∆t = classic RNN + input delays, D-enc. = RNN encoder C-enc = ODE encoder. | LTC 0.882±0.005 vs 最强 ∗ 基线 Latent ODE(C enc.) 0.846±0.013 —— **本文最大的领先幅度**；但该表 **7 个基线行全部带 ∗**（跨论文取自 Rubanova et al. 2019），协议不可比。 |
| {FIG-LTC-4} | Fig. 4（VoR p.7664） | Half-cheetah physics simulation | HalfCheetah-v2 的 17 维观测 / 6 控制输出示意（含 φ = joint angle）。**是离线自回归拟合的对象，不是控制实验**。 |
| {TAB-LTC-6} | Table 6（VoR p.7664） | Sequence modeling. Half-Cheetah dynamics n=5 | LTC 2.308±0.015 最优（LSTM 2.500±0.140）。**这是本文唯一"物理动力学"任务，仍是开环拟合**。 |
| {TAB-LTC-S1} | Table S1（**仅 arXiv p.24**） | Hyperparameters used for the experimental evaluations | 全部训练超参：hidden 32 / minibatch 16 / lr 0.001–0.02 / **ODE-solver step 1/6** / Adam(β1 0.9, β2 0.999, ε 1e-08) / **BPTT length 32** / epochs 200。**正式版省略** —— P1 复现 A2 的 LTC 臂必须引这一张。 |
| {TAB-LTC-S2} | Table S2（**仅 arXiv p.24**） | Number of parameters of various RNN model in relation to the RNN width k, the number of hidden layers n, and the number of decay slots m. | **A2 公平性关键表**：LTC `4nk²+3nk`、ODE-RNN `nk²+nk`、LSTM `4nk²+4nk`、CT-RNN `nk²+2nk`。同宽度下层 LTC 参数量≈ODE-RNN 的 4 倍。**正式版省略**。 |
| {FIG-LTC-S1} | Figure S1（**仅 arXiv p.25**） | Additional trajectory length results. | 补充的轨迹长度扫描（输入步长 0.1–0.001、Hard-tanh、depth 1、width 25）。与 Fig. 3 同族，无可引用数字。 |

## 6. 对 P1 的用处

- **与 P1 的关系**：**相邻问题（任务层）／直接回答（方法学层）**。任务层：本文无控制器、无闭环、无车辆、无编队、无 ODD，**全文没有 P1 七项指标中的任何一项**，唯一两处"control"字样都不构成证据（Half-Cheetah 是离线拟合预训练控制器的轨迹；"control of robots"是结论里的未来方向句）。方法学层：LTC 是 P1 消融 **A2（LNN vs CfC vs 普通 ODE-RNN）中 LTC 一臂的定义来源**，本文的动力学式、求解器、参数律与训练协议可被 A2 直接复用。

- **可迁移**：
  1. **★ A2 的 LTC 臂可直接采用本文的默认配置**：式 (1) 动力学 + Fused 求解器式 (3) + **每 RNN 步 6 个求解步**（Δt = 1/6 输入采样周期）+ 32 隐藏单元 + Adam + BPTT length 32 + 200 epochs（超参见 Table S1，**只在 arXiv 版**）。这是本文对 P1 最直接的一份"可照抄的配置清单"。
  2. **★★ A2 公平性的关键数字（本卡最重要的可执行结论）**：Table S2 的精确参数律显示，**同宽度 k、同层数 n 下 LTC 的参数量约为 ODE-RNN 的 4 倍**（`4nk²+3nk` vs `nk²+nk`）。若 A2 按"同 hidden size"对齐 LTC 臂与 ODE-RNN 臂，**LTC 臂的容量天然大 4 倍，A2 的结论会被参数预算混淆**。→ A2 必须改为**等参数量对齐**（或至少同时报告各臂参数量），否则不满足 `AGENTS.md` §3"同等可用信息/同等预算"的公平性要求。
     - 复算（**本卡算术代入，非论文印出值**；k=32, n=1）：LTC **4,192**；ODE-RNN **1,056**；LSTM 4,224；CT-RNN 1,088。
     - **附加发现**：LTC 在该配置下的 4,192 与 CfC（NMI 2022）报告的 **RNN 分量 4,184** 几乎相等（差 8）→ **A2 中 LTC vs CfC 两臂可在近乎相同的递归参数量下比较**，而 ODE-RNN 臂差约 4 倍。这给 A2 提供了一个天然的"等参数双雄"设计。（注意 CfC 的 4,184 来自其车道保持模型，配置口径与本卡代入的 k=32/n=1 未绑定，引用时须说明。）
  3. **"需要 ODE 求解器"对 P1 的 100 Hz 实时回路意味着什么（可量化的判断）**：本文的 LTC 求解器是**固定步长**，实验设置是**每 RNN 步 6 个求解步**（arXiv S5）。→ 100 Hz（10 ms 周期）下 LTC 臂需要 **600 次求解步/秒**，且每一步 `x(t+Δt) = [x(t) + Δt f(·)A] / [1 + Δt(1/τ + f(·))]` **串行依赖前一步**，无法像 CNN 那样并行摊平；单步延迟下限 = 6 ×（一次 f 的前向：`f = tanh(γr x + γI + µ)`，两次 N×N 矩阵乘加）。叠加 Table 2 的结论（Hard-tanh 下 LTC 的计算深度达 **81.01**，是 tanh 的 8.8 倍），**求解步数本身就是实时性旋钮**。→ P1 若把 LTC 作为 A2 的一臂，**必须把"每步求解步数"作为显式控制变量报告**，否则延迟不可比。
  4. **CfC 臂相对 LTC 臂的机理优势（可直接写进 A2 的动机段）**：CfC（NMI 2022）取消求解器、把时间 t 显式放进门控（式 (10) 用 σ(−[f]·t) 与 1−σ(−[f]·t)），推理成本与离散 RNN 同阶；而本文 LTC **必须**数值求解，且作者自承"以更高的时间与内存复杂度为代价，须未来研究"（p.7664 逐字）。**这句话是 P1 论"为什么控制器选 CfC 而不是 LTC"的现成、可引的自承认证。**
  5. **跨论文的张力提示（A2 必须先解决的实现争议）**：CfC 论文（NMI 2022）把 **LTC 当作基线**，其 LTC 在 PhysioNet AUC 0.6477±0.010、IMDB 61.8%±6.1、XOR(event-based) 49.11%±0.00 上**接近随机水平**；而 LTC 原文（本文）报告 LTC 在 Person Activity 第二设定 0.882、Half-Cheetah MSE 2.308 上**均为全场最优**。两套数据集不同、不能直接比较，但**同一模型在两篇论文中的相对位置相反**，且 CfC 论文未说明其 LTC 基线用的是哪种求解器/步数配置。→ P1 的 A2 若 LTC 臂表现差，须区分"模型本身"与"求解器/步数配置"；**本文的 6 步固定步长协议就是控制这个变量的钥匙**。
  6. **可复用的引用限定语**：见下"引用时必须带的限定语"。

- **不可迁移 / 陷阱**：
  1. **无任何控制内容**：无控制器结构、无闭环、无稳定性证明（Theorem 1/2 是**状态有界性**，不是闭环稳定性）、无车辆/编队/ODD。**P1 不能从本文取任何控制器性能对标值。**
  2. **Abstract/结论的"superior expressivity / superseding performance"只对有监督序列预测成立**，不得外推为控制性能（`AGENTS.md` §1 第 3 条红线）。本文对 LTC 相对基线的胜负有**反向证据**：Table 3 的 7 项里 3 项不如基线，Table 4 领先 CT-GRU 仅 0.21 个百分点而两者 SD 为 0.40/0.39。
  3. **无硬件、无时延、无内存**：两版**均全文未见** → P1 无法从本文取任何实时性/资源数字；且作者自承"时间与内存复杂度更高且未量化"，**这对 P1 的资源主张是不利证据而非有利证据**。
  4. **统计薄弱**：n=5 是"5 次不同权重初始化"，**无种子列表、无 CI、无任何显著性检验**；Table 5 的 6 个基线值**直接取自 Rubanova et al. 2019**（跨论文拼接，与 `AGENTS.md` §1 第 3 条同类问题）→ 最"亮眼"的 0.882 vs 0.846 不可作为同协议对比。
  5. **★ 正式版不自足**：AAAI VoR 只有 10 页（7657–7666），**不含 Appendix**，但正文 **8 处**写"provided in Appendix"/"See supplements"。**证明、实验设置、超参表 S1、参数量表 S2、Figure S1 只在 arXiv v4 里**。→ P1 引用 Table S2 的参数量律或 Table S1 的 6 步设置时，**必须注明出处是 arXiv:2006.04439v4 附录，而非 AAAI 正式版**（这是引用准确性问题，不是小事）。
  6. **代码可用性只在 arXiv 版、且正式版已删除该声明**；本卡**未克隆或运行**该仓库，未能验证其与论文表格一致。
  7. **⚠内部不一致（两版共有）**：正文称 "a series of **eleven** time-series prediction experiments"（VoR p.7658），而全部结果表只给出 **10 项**（Table 3 的 7 行 + Table 4 + Table 5 + Table 6）；**未找到第 11 项**。
  8. **⚠版本间不一致**：Figure 2 图注的 D/E 面板定义在正式版与 arXiv 版**互换**，正文交叉引用随之互换 → 引用 Fig. 2 任何单个面板前必须核对图内实际曲线。

- **与 CfC（NMI 2022）的关系**：
  | 维度 | LTC（本文，AAAI 2021） | CfC（NMI 2022） |
  |---|---|---|
  | 动力学 | **式 (1)**：`dx/dt = −[1/τ + f(x,I,t,θ)]x + f(x,I,t,θ)A`；τ_sys = τ/(1+τf) | **继承同一 LTC 动力学**（其 Theorem 1 / Lemma 1 的紧致性结果正是针对该式），τ_sys 与 A 的写法一致 |
  | 求解 | **必须数值求解**：「Solving Eq. 1 analytically, is non-trivial」；自研 Fused 固定步长求解器（式 (2)(3)、Algorithm 1），实验每步 6 个求解步 | **取消求解器**：给出闭式近似并把 t 显式放进门控（式 (10)：σ(−[f]·t) 与 1−σ(−[f]·t)）→ 推理成本与离散 RNN 同阶 |
  | 训练 | **vanilla BPTT**，内存 O(L×T)（Table 1），明确不用伴随法 | 无 L 这一维，训练/推理与离散 RNN 同阶 |
  | 结构 | 神经元级动力学，未提出 NCP（NCP 是引文 Lechner et al. 2020a, NMI 2020） | 与 NCP 结合（稀疏接线 + LTC 神经元），报告车道保持模型 |
  | 实验 | 10 项**离线有监督序列基准**；**无真车、无硬件、无时延** | 4 个序列基准 + **1 次真车车道保持**（Lexus RX450H / 1 km / 30 km/hr）——**但真车实验零闭环指标**，只有参数量与注意力可视化 |
  | 参数量 | 只有公式 `4nk²+3nk`（正式版无） | 车道保持模型：RNN 分量 4,184 / 全模型 230,828（含 CNN head） |
  - **继承**：CfC 的出发点就是本文式 (1) 与 τ_sys 定义；CfC 论文把 LTC 列为基线之一。
  - **CfC 改掉了**：① 求解器（本文的最大工程负担）被闭式门控取代；② 训练内存里的 L 维消失；③ 从"仅序列建模"扩展到**一次真车部署**（尽管无量化闭环指标）。
  - **两篇共同缺口（对 P1 最关键）**：**都没有闭环控制评价、都没有硬件时延/内存数字**。→ **P1 的 A2 不能靠这两篇中的任何一篇论证控制性能或实时性**；A2 的结论必须由 P1 自测。

- **引用时必须带的限定语**（一句，含样本/场景/协议边界）：
  > LTC（Hasani et al., AAAI 2021）的全部结论来自 10 项**离线有监督时间序列基准**（32 隐藏单元、n=5 次权重初始化、mean±SD，**未报告种子、无 CI、无显著性检验**，Table 5 的多数基线值跨论文取自 Rubanova et al. 2019），其前向必须经**固定步长 ODE 求解器**（实验设置"每步 6 个求解步"与全部超参**仅见 arXiv:2006.04439v4 附录**，**不在 AAAI 正式版内**），**无闭环控制、无硬件/时延/内存数据，也未报告任何具体模型的参数量**（只有 Table S2 的参数律 `4nk²+3nk`，且该表不在正式版内）。

## 7. 缺失信息（写成可执行动作）

1. **向作者/AAAI 索取正式随附的 Appendix/补充材料**：VoR 正文 **8 处**引用"Appendix"/"supplements"，但 OJS 下载的 10 页 PDF 不含。（后果：**正式版引用了自身不含的材料**；P1 引用 Table S1/S2 时必须改用 arXiv 版出处，或补上正式补充材料的链接与编号。）
2. **向作者索取每个任务、每个模型的实测参数量**：目前只有 Table S2 的参数律，实验网络的层数 n 未与 k=32 绑定。（后果：**A2 无法做等参数对齐**——这是 P1 最需要补齐的一条。）
3. **索取 5 次重复的随机种子列表与逐次结果，并补做配对显著性检验**（本文零检验、零 CI）。（后果：Table 4 中 LTC 85.48%±0.40 vs CT-GRU 85.27%±0.39 的 0.21 个百分点差距**无法判定是否超出噪声**，P1 不能引用为"LTC 更优"。）
4. **索取 BPTT vs 伴随法的实测时间与内存**：Table 1 只给复杂度阶（O(L×T) vs O(1)），作者自承"elevated time and memory complexity"却未量化。（后果：P1 的 MCU 内存指标与训练显存预算无锚点。）
5. **核验代码仓库**：arXiv 版 p.1 脚注与 S9 声明 `https://github.com/raminmh/liquid time constant networks` 公开可得，正式版已删除该声明；本卡未克隆运行。（需确认仓库是否含 Fused 求解器实现、10 项任务的训练脚本与超参；这是 A2 直接复用的前提。）
6. **向作者澄清 "eleven" 与 10 项实验的口径**（或指出漏报的一项）。
7. **核验 Figure 2 的 D/E 面板归属**：以图内实际曲线为准确定正式版还是 arXiv 版正确（两版的图注与正文交叉引用整体互换）。
8. **统一本项目的材料口径**：任务给定 arXiv 版 `CHARS=92,938`，本卡实测 UTF-8 字符 **96,695**（含 3,642 个 CRLF 与 496 个孤立 CR；按 CRLF→LF 归一为 93,053）。（后果：若下游用该字段做文件指纹或去重校验，会误判为"文件已变"。）

## 8. 关键数字（只抄论文明确印出的表格/正文）

> 纪律：下列"值"全部抄自论文/附录**明确印出**的表格与正文；**唯一一处算术代入已显式标注**。无一处为目测估读。页码 = AAAI 正式版印刷页码（arXiv 版页码另注）。

| 指标 | 值 | 不确定度 | 出处（表/图/节/页码） |
|---|---|---|---|
| 时间常数界 | τi/(1 + τiWi) ≤ τsys_i ≤ τi | 无（定理界，证明在 arXiv 附录 S1） | 式 (4)，Theorem 1，VoR p.7659 |
| 状态界 | min(0, A^min_i) ≤ xi(t) ≤ max(0, A^max_i) | 无（定理界，证明在 arXiv 附录 S2） | 式 (5)，Theorem 2，VoR p.7659 |
| 计算深度（tanh） | LTC **9.19** ± 2.92；CT-RNN 4.13 ± 2.19；Neural ODE 0.56 ± 0.016 | SD；# of tries = 100 | Table 2，VoR p.7660 |
| 计算深度（sigmoid） | LTC **7.00** ± 5.36 | SD；100 tries | Table 2，VoR p.7660 |
| 计算深度（ReLU） | LTC **56.9** ± 9.03 | SD；100 tries | Table 2，VoR p.7660 |
| 计算深度（Hard-tanh） | LTC **81.01** ± 10.05 | SD；100 tries | Table 2，VoR p.7660 |
| BPTT vs 伴随法复杂度 | Time O(L×T×2) vs O((Lf+Lb)×T)；Memory **O(L×T)** vs **O(1)**；Depth O(L) vs O(Lb)；BWD acc High vs Low | 无（符号界，**无实测**） | Table 1，VoR p.7659 |
| Gesture accuracy | LTC **69.55%** ± 1.13（最优；CT-GRU 68.31% ± 1.78） | SD，n=5 | Table 3，VoR p.7663 |
| Occupancy accuracy | LTC **94.63%** ± 0.17（最优） | SD，n=5 | Table 3，VoR p.7663 |
| Activity recognition accuracy | LTC 95.67% ± 0.575（**低于** Neural ODE 97.26% ± 0.10） | SD，n=5 | Table 3，VoR p.7663 |
| Sequential MNIST accuracy | LTC 97.57% ± 0.18（**低于** LSTM 98.41% ± 0.12） | SD，n=5 | Table 3，VoR p.7663 |
| Traffic squared error | LTC **0.099** ± 0.0095（最优） | SD，n=5 | Table 3，VoR p.7663 |
| Power squared error | LTC 0.642 ± 0.021（**差于** CT-GRU 0.586 ± 0.003） | SD，n=5 | Table 3，VoR p.7663 |
| Ozone F1-score | LTC **0.302** ± 0.0155（最优） | SD，n=5 | Table 3，VoR p.7663 |
| Person Activity 1st setting accuracy | LTC **85.48%** ± 0.40（CT-GRU 85.27% ± 0.39；差距 0.21 pt < SD） | SD，n=5 | Table 4，VoR p.7663 |
| Person Activity 2nd setting accuracy | LTC **0.882** ± 0.005（最强 ∗ 基线 Latent ODE(C enc.) 0.846 ± 0.013） | SD，n=5；**∗ 基线取自 Rubanova et al. 2019** | Table 5，VoR p.7663 |
| Half-Cheetah MSE | LTC **2.308** ± 0.015（最优；LSTM 2.500 ± 0.140、Neural ODE 3.805 ± 0.313） | SD，n=5 | Table 6，VoR p.7664 |
| 性能提升声称 | "between **5% to 70%** performance improvement … in four out of seven experiments and comparable performance in the other three" | **未报告**（口径未定义） | 正文 §Time Series Predictions，VoR p.7663 |
| 实验网络宽度 | 32 hidden units | 无 | Table S1 与 S5，**仅 arXiv p.22/24**（正式版无） |
| 求解器步长 | 每 RNN 步 **6 个 ODE 求解步**（Δt = 1/6 输入采样频率），全部为固定步长 | 无 | S5，**仅 arXiv p.22**（正式版无） |
| 训练超参 | hidden 32；minibatch 16；lr 0.001–0.02；ODE-solver step 1/6；Adam β1 0.9 / β2 0.999 / ε 1e-08；BPTT length 32；epochs 200 | 无 | Table S1，**仅 arXiv p.24**（正式版无） |
| 参数量（公式，逐字） | LTC `4nk² + 3nk`；ODE-RNN `nk² + nk`；LSTM `4nk² + 4nk`；CT-RNN `nk² + 2nk`；CT-GRU `2mk² + 2mk + k² + k` | 无 | Table S2，**仅 arXiv p.24**（正式版无） |
| 参数量（**本卡算术代入** n=1, k=32） | LTC ≈ **4,192**；ODE-RNN ≈ 1,056；LSTM ≈ 4,224；CT-RNN ≈ 1,088 | 无（非论文印出值，由 Table S2 公式代入） | 由 arXiv Table S2 复算 —— **引用时必须标"本卡复算"** |
| 训练/推理时间、加速比 | **全文未见**（两版均无） | — | 全文 grep（arXiv 版亦无） |
| 硬件（GPU/CPU/MCU 型号）、单步时延、内存占用、功耗 | **全文未见**（两版均无） | — | 全文 grep：`GPU`/`CPU`/`NVIDIA`/`Jetson`/`MCU`/`latency`/`KB`/`MB` 等均 0 命中 |
| 唯一平台字样 | "We implemented all RNN models in TensorFlow1.14." | — | S5，**仅 arXiv p.22**（正式版无） |
| 代码/数据可用性 | arXiv 版：「All code and data are publicly accessible at: https://github.com/raminmh/liquid time constant networks.」（S9）；**正式版已删除全部此类声明**（`github` 0 命中） | — | arXiv p.25；VoR 全文无 |

---

**⚠内部不一致（两版共有）**：正文称 "a series of **eleven** time-series prediction experiments"（VoR p.7658 / arXiv p.2），而结果表只支持 **10 项**（Table 3 的 7 行 + Table 4 + Table 5 + Table 6）；**未找到第 11 项**。

**⚠内部不一致（版本间）**：Figure 2 的 D/E 面板定义与正文交叉引用在 VoR 与 arXiv 版之间**整体互换**（VoR：「D) as a function of width (Hard-tanh), and E)in network layers with logistic-sigmoid activations.」；arXiv：「D) in network layers with logistic-sigmoid activations and E) as a function of width (Hard-tanh).」）。两版必有一版与图内实际曲线不符；本卡无法从纯文本判定。

**字符数自查（实测，脚本按 § 边界截取后计数）**：§2 摘要 —— 汉字 **234** ／汉字+西文词 303 ／非空白字符 563（限 400 字）；§3 结论 —— 汉字 **203** ／汉字+西文词 266 ／非空白字符 504（限 350 字）；§4 方法一句话 —— 汉字 **35** ／汉字+西文词 44 ／非空白字符 **60**（限 60 字）。**口径说明**：题目要求实测"中文字符数"，故以**汉字计数**为准（三项均远低于上限）；同时给出另两种口径供交叉核对——**§4 在最严口径（非空白字符）下恰为 60，未超限**。

**材料问题（≤5 行）**
1. 主用材料已换为 AAAI 正式版（VoR，10 页 / 7657–7666），arXiv 版仅作差异对照；两版**全部数值一致**（65 行 mean±SD + 36 个轨迹长度值逐行比对无差异）。
2. **正式版不自足**：10 页 VoR 无附录，但正文 **8 处**引用 Appendix/supplements；Table S1（超参）、Table S2（参数量律）、Figure S1 与全部定理证明**只在 arXiv v4 可得**——P1 引用这三项时必须改注 arXiv 出处。
3. 正式版把 arXiv 版第 1 页的代码/数据可用性脚注与 S9 声明**一并删除**（VoR 中 `github` 0 命中）。
4. 任务给定 arXiv 版 `CHARS=92,938`，实测 UTF-8 字符 **96,695**（CRLF→LF 归一 93,053），差 3,757 / 115，属口径差异，卡片已双记。
5. **A 档 5 篇预算已满**（协议 §4）；LTC 主口径 17 分判 A，需按 §5 破平或占用追加名额。
