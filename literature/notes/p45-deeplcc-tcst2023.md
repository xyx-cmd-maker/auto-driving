# 精读笔记 #45：DeeP-LCC: Data-EnablEd Predictive Leading Cruise Control in Mixed Traffic Flow

- **文献（以抓取全文 byline 为准）**：Jiawei Wang, Yang Zheng, Keqiang Li, Qing Xu. *DeeP-LCC: Data-EnablEd Predictive Leading Cruise Control in Mixed Traffic Flow*. IEEE Transactions on Control Systems Technology, 2023, 31(6): 2760–2776. DOI 10.1109/TCST.2023.3288636.
- **全文来源**：已获全文（arXiv HTML 纯文本，`https://arxiv.org/html/2203.10639`，97,265 字符 / 1,383 行，抓取日期 2026-10-02）。**未**获 IEEE 正式排版版、补充材料、代码仓库快照。
- **精读日期**：2026-10-02
- **本笔记的技能依据**：`deep-paper-reader`（六件套 + 双口径评级 + 数字口径对照表 + 机器可读限定语）

---

## 作用域

**场景①：项目内文献工作。**

- **项目**：`D:\Deepseek Harness\auto-driving`（自动驾驶 OTF 论文集群）。
- **项目不变量文件**：`D:\Deepseek Harness\auto-driving\AGENTS.md`。
- **本次精读服务的主张**：论文 1（P1，代号 **OTF-CfC**）「基于超车频次势场与液态神经网络的高速主线编队连续时间控制」。
- **P1 的主张上限（本项目 `AGENTS.md` §1，逐条原样引用，本笔记不得越过）**：
  1. **「不得预先声称"OTF 势场带来 X% 性能提升"」**——学位论文报告的分类器准确率增益（SVM +2.23~+3.60／LSTM +2.23~+5.46／Bi-LSTM +1.00~+1.73 个百分点）是**论文报告值、未经本项目复现**，在 LNN 控制范式下未经本项目实测即属 **C/D 级证据**；A1 消融须诚实报告。
  2. **「不得把仿真/回放写成实车验证」**——未做真车闭环前，措辞上限是"在 CARLA 与真实数据回放中"。
  3. **「不得直接搬用他人论文数字」**——与外部方法对比若未同协议复现，必须标注"文献报告值，协议不同，不可直接比较"。
- **本笔记的用途边界**：本笔记中来自 DeeP-LCC 的**任何**数字（24.69%／9.05%／43.82%／4.8%／28.07 ms 等）均为**文献报告值，协议不同，不可直接比较**；不得写入 P1 稿件的性能对比句，只能出现在 Related Work 的方法差异陈述中，且必须携带 §七 的 `citation_qualifier` 单行限定语。
- **元数据旗标（本次精读发现，需 `citation-and-related-work` 层 1/2 修正）**：任务给定作者串为 "Wang J, Sun Y, Bian Y, Zhu Y, Ozbay K, Li SE, Wang X, Yan F, Li K"，与 DOI 10.1109/TCST.2023.3288636 对应的真实作者串 **不符**。本项目自身经 Crossref 核验的记录（`literature/final_list.jsonl` 第 45 行，`n=45`）与抓取全文 byline 一致，均为 **4 位作者：Jiawei Wang; Yang Zheng; Keqiang Li; Qing Xu**。判定：任务给定作者串**错误**（其中 K. Ozbay、S. E. Li 出现在本文**参考文献** [21][22] 与 [2][3] 中，疑为串行）。本笔记内容分析以抓取全文为准。

---

## 一、作者主张

> 以下为转述，不含评价。凡引号内为英文原句。

作者主张分四层。

**第一层（可行性基础）**：现有的 CAV 控制多为 model-based，需要显式已知 HDV 的跟驰动力学，而这"are non-trivial to identify accurately"（Abstract）。作者因此提出**非参数的、数据驱动的**策略 DeeP-LCC。其可行性建立在三项系统论性质之上：线性化混行系统在 $1\notin S$ 时**不可控但可镇定、可观测**（Theorem 1、Theorem 2）；引入头车速度误差 $\epsilon(t)$ 作为**外部输入**后，重构系统 (24) 变为**完全可控且可观测**（Corollary 1）——作者称这是"the foundations of our adaptation of DeePC [26] for mixed traffic control"；由此可套用 **Willems' fundamental lemma**（Lemma 3）做非参数行为表征（Proposition 2）。

**第二层（方法）**：DeeP-LCC = 离线数据采集（构造 Hankel 矩阵 $U_{\mathrm p},E_{\mathrm p},Y_{\mathrm p},U_{\mathrm f},E_{\mathrm f},Y_{\mathrm f}$）+ 在线滚动时域求解一个 QP（式 (37)）。目标函数 $J(y,u)=\sum(\lVert y\rVert_Q^2+\lVert u\rVert_R^2)$ 惩罚**全交通流**的输出偏差与控制能量（继承 LCC 的 system-level 视角）；约束含 CAV 间距上下界（$\tilde s_{\min}\le \tilde s_i\le\tilde s_{\max}$）与加速度饱和。因真实系统非线性且含噪，等式约束用松弛变量 $\sigma_y$ 加 $g$、$\sigma_y$ 的二范数正则化处理。作者主张该式 (37)"is applicable to nonlinear and non-deterministic mixed traffic systems"。

**第三层（性能）**：作者主张 DeeP-LCC **不需要任何 HDV 模型知识**，却能达到与"基于精确线性化模型的 standard MPC"**可比**的性能（Experiment A 损失 4.8% 最优性）；在 NEDC 驱动的城市/高速工况与紧急制动工况下，DeeP-LCC 带来**燃油经济性、交通平滑性与安全性**的改进（Abstract、§I-B、§VII）。

**第四层（边界自认）**：作者自认数据在**单一平衡点** $15\,\mathrm{m/s}$ 采集，而仿真中平衡点时变，故"we assume that the HDVs have a similar behavior around different equilibrium states"且"This assumption indeed may not hold"（Remark 6、Appendix C）；DeeP-LCC 的**递归可行性**"we leave ... for future work"（§V-D）；针对未知外部输入的**鲁棒 DeePC**"is beyond the scope of this work"（Remark 4）。

---

## 二、主张—证据台账

> **内部等级** `A_int–D_int` 仅凭本文内部证据；**外部复现**一律为 `未检`（本技能只记录状态，不做外部检索）。**判据**：凡证据为仿真者，内部等级最高 `C_int`；纯假设/设计意图为 `D_int`；有完整证明的理论结论最高 `B_int`（A_int 需预注册 + 独立重复，单篇精读无法满足）。

| # | 作者主张（英文原句） | 支撑证据（图/表/统计量） | 内部等级 | 外部复现 | 是否被结果支撑 | 缺口 |
|---|---|---|---|---|---|---|
| 1 | "the general mixed traffic system consisting of multiple CAVs and HDVs is not controllable (but stabilizable) unless the vehicle immediately behind the head vehicle is a CAV." | Theorem 1（含 Appendix A 完整证明，用 Lemma 4 可控性不变性 + 虚拟输入 $\bar u$）；条件 (16) $\alpha_1-\alpha_2\alpha_3+\alpha_3^2\neq 0$；Lemma 1/2 引自 [11] | `B_int` | 未检 | 是（在 (16) 成立且线性化模型精确的前提下） | 仅线性化 LTI 结论；Lemma 1/2 为转引 [11]，本文未重证；条件 (16) 退化（$=0$）情形未讨论；无非线性系统的对应结论 |
| 2 | "The general mixed traffic system given by (15), where there exist $m$ $(m\geq 1)$ CAVs, is observable when (16) holds." | Theorem 2；正文注明"By adapting [11, Theorem 4]"；无独立证明；无数值秩检验 | `B_int` | 未检 | 部分（陈述被接受，但证据是转引而非本文证明） | 证明依赖 [11]；未给出可观测性矩阵条件数或数值验证；未讨论近奇异/病态情形 |
| 3 | "system (24) is controllable and observable if (16) holds." → 使 Willems 引理可用 | Corollary 1；"The proof is similar to that of ... [11, Corollary 1]; we refer the interested reader to [11]"（未展开）；Assumption 1（离散化保持可控可观） | `B_int` | 未检 | 部分（证明被委派给 [11]；Assumption 1 为充分条件假设） | 证明未写出；Assumption 1 是充分条件而非充要，采样周期 $\Delta t=0.05\,\mathrm{s}$ 是否满足未被逐一验算 |
| 4 | 混行中领航车控制（LCC）在**未知 HDV 模型**下可行："DeeP-LCC directly relies on the trajectory data of the HDVs, bypassing a parametric HDV model, to design the CAVs' control input." | Proposition 2（行为表征，需 (16) + Assumption 1 + Assumption 2）；式 (29)/(37)；Fig. 3(c) 单条轨迹下的波衰减 | `B_int`（LTI 情形）/ `C_int`（非线性情形） | 未检 | 是（线性化情形有证明；非线性情形仅仿真） | 非线性"可行"只有 3 个仿真场景支撑；持续激励（Assumption 2）**未被实际校验**——作者只说"One could verify the full rank condition by Definition 1 before applying the pre-collected data set" |
| 5 | 相对 **人类驾驶（all-HDV, OVM）** 基线的改进量："DeeP-LCC reduces up to $24.69\%$ fuel consumption with safety guarantees in the braking scenario at a CAV penetration rate of $25\%$ compared with the case of all HDVs." | §VI-C 正文（DeeP-LCC $24.69\%$，MPC $25.12\%$）；Fig. 7(a)(b) 速度曲线；Fig. 7(c)(d) 间距曲线 | `C_int` | 未检 | 是（方向一致），但口径受限 | 单次仿真；无种子、无重复、无 CI、无显著性检验；"up to"为选取值；**渗透率分母歧义**（$2/8=25\%$，含头车则 $2/9=22.2\%$，见 §四口径表）；无碰撞/TTC 计数支撑"driving safety" |
| 6 | 相对 **MPC** 基线："DeeP-LCC achieves comparable performance in nonlinear and non-deterministic cases with respect to a standard MPC based on an accurate linearized model." | Fig. 4（100 次实验）：MPC 均值 $2.91\times10^{4}$，SD $0.003\times10^{4}$；DeeP-LCC 均值 $3.05\times10^{4}$，SD $0.077\times10^{4}$；§VI-A 文字"losing only $4.8\%$ optimality" | `C_int` | 未检 | 部分：均值差可核（本文 $4.8\%$；本次复算 $4.81\%$，见 §四），但"comparable"**未做等价检验**，且 **DeeP-LCC 在全部设置中均未优于 MPC** | 两控制器 SD 相差约 $25.7$ 倍（$30$ vs $770$）；未报检验统计量；100 次实验是否独立同分布未说明；Experiment B/C 中 **MPC 被刻意失配**（用 nominal 参数 vs Table I 异质 HDV），故"可比"是失配 MPC 与 DeeP-LCC 的对比 |
| 7 | 相对 **ACC / CACC** 基线：**未报告**（全文无任何 ACC/CACC/CCC/LCC 控制器被实现为基线） | 无对应图表；CACC/CCC/LCC 仅出现在 §I 引言叙述与参考文献 [2]–[4][10][11] | `D_int`（缺证据） | 未检 | 不适用（无主张—无证据） | P1 若需与 ACC/CACC 对齐，本文**不能**提供任何可比数字；这是本文基线集的明确空缺 |
| 8 | 数据需求（多少轨迹、多长时间）："the length for the pre-collected trajectory is chosen as $T=800$ with a sampling interval $\Delta t=0.05\,\mathrm{s}$"；"The theoretical lower bound on the input length $T$ is $(m+1)(T_{\mathrm{ini}}+N+2n)-1$ ... which is of value $257$ ... and we choose $T=800$ for redundancy considerations."；"we collect $100$ trajectories of the same length $T=800$" | §VI 离线数据采集条目；Appendix B（含 $T\ge257$ 的下界推导）；Fig. 8（预采集轨迹示意）；式 (27) | `B_int` | 未检 | 是 | 换算：$T=800\times0.05\,\mathrm{s}=\mathbf{40\,s}$ 单条轨迹；理论下界 $257\times0.05\,\mathrm{s}=\mathbf{12.85\,s}$【计算值】。**关键缺口：论文中的 800 点轨迹是仿真生成的**（CAV 预设计控制器 = OVM + $\delta_u\sim\mathbb{U}[-1,1]\,\mathrm{m/s^2}$；头车 $\epsilon\sim\mathbb{U}[-1,1]\,\mathrm{m/s}$，每 $0.5\,\mathrm{s}$ 变一次），**不是实地采集的混行轨迹** |
| 9 | 数据来源可取自真实历史轨迹："These pre-collected data samples could be generated offline, or collected from the historical trajectories of those involved vehicles." | 仅为可能性陈述；无任何真实轨迹采集实验、无数据集名称、无数据来源说明 | `D_int` | 未检 | 不适用（设计意图，非结论） | 全文**没有任何真实交通数据**；"historical trajectories" 路线**未被演示**；故不能据此声称该方法已在真实数据上被验证 |
| 10 | 对模型失配的鲁棒性："we introduce a slack variable $\sigma_y$ ... to ensure the feasibility of the equality constraint"；"This formulation (37) is applicable to nonlinear and non-deterministic mixed traffic systems." | 式 (37) 正则化（$\lambda_g\lVert g\rVert_2^2+\lambda_y\lVert\sigma_y\rVert_2^2$）；HDV 加速度加 $\mathbb{U}[-0.1,0.1]\,\mathrm{m/s^2}$ 噪声；Experiment B/C 用 Table I 异质参数；Remark 3 | `C_int` | 未检 | 部分（经验上可行；无形式化保证） | **明确未做鲁棒性分析**：Remark 4"robust DeePC for mixed traffic ... is beyond the scope of this work"；Appendix C"it is also an interesting future direction to investigate the robustness performance of DeeP-LCC ... in the case of behavior mismatch"。无失配扫描、无性能衰减曲线、无 $\sigma_y$ 有界性验证 |
| 11 | 安全性 / 无碰撞保证："input/output constraints are incorporated for collision-free guarantees"；"provides safety guarantees for CAVs when feasible" | 式 (32)(33)(34)(35)：$\tilde s_{\min}\le\tilde s_i\le\tilde s_{\max}$（$s_{\min}=5\,\mathrm{m},s_{\max}=40\,\mathrm{m}$）；$a_{\min}=-5,a_{\max}=2\,\mathrm{m/s^2}$ | `C_int` | 未检 | 部分（约束被正确编码，但保证是**条件性**的） | 作者自认"Due to the page limit, we leave the recursive feasibility of DeeP-LCC for future work"——**递归可行性未证**，故"collision-free"在最坏情形无保证；且**未报告任何安全事件统计量**（最小间距、TTC、约束触发次数、碰撞次数） |
| 12 | **弦稳定性**结论：**未报告** | 全文无弦稳定性判据、无传递函数/放大率指标、无闭环稳定性定理；"stability"仅出现于 (a) 开环子系统"is not controllable but is stable"（Lemma 2），(b) 转引他人结果"exponential stability ... rigorously proved in [46, 45]"（非本文系统），(c) 参考文献 [11] 标题中的 "string stability" | `D_int`（缺证据） | 未检 | 不适用（无主张—无证据） | 本文只提供 **controllability / stabilizability / observability**，**没有** closed-loop string stability 结论；因此"improving traffic efficiency / traffic smoothness"缺少形式化稳定性支撑，只有 Fig. 3、Fig. 6(b)、Fig. 7 的曲线与百分比 |
| 13 | **仿真 vs 实验**：全文**仅仿真**。"This section presents three nonlinear and non-deterministic traffic simulations to validate the performance of DeeP-LCC in mixed traffic." | §VI（Experiment A/B/C）；"The algorithm and simulation scripts are available at https://github.com/soc-ucsd/DeeP-LCC" | 不适用（作用域事实） | 未检 | 是（文中从未声称实车） | 本文**无**任何真车、台架或微型车队实验。Remark 3 提及的"our follow-up real-world miniature experiments in **[47]**"（J. Wang et al., arXiv:2204.03747）**是另一篇文献**，本文未报告其实验细节或数据。按 P1 项目红线，引用本文结果时**不得**表述为实车验证 |
| 14 | 工况真实性："we design both an urban driving trajectory and a highway driving trajectory for the head vehicle motivated by ECE-15 and Extra-Urban Driving Cycle (EUDC) from the New European Driving Cycle (NEDC)" | §VI-B；Fig. 5(a)(b) all-HDV / (c)(d) DeeP-LCC；Fig. 6 分 Phase 的降幅柱状图 | `C_int` | 未检 | 是（工况被实现） | 仅**头车**轨迹取自 NEDC；HDV 仍是 OVM 合成体，非实测车流；**无换道、无横向动力学、无多车道**（唯一涉及相邻车道之处是 §V-C 对"vehicles from adjacent lanes to cut in"的定性讨论，无建模） |
| 15 | 时变平衡点下的可迁移性（作者自认的边界）："we assume that the HDVs have a similar behavior around different equilibrium states ... This assumption indeed may not hold, and thus the performance of DeeP-LCC might be compromised in this simulation." | Remark 6；Appendix C（式 (42) 用过去 $T_{\mathrm{ini}}$ 内头车平均速度估 $v^*$） | `D_int` | 未检 | 不适用（自认假设） | 该假设**未被量化**：作者未测量 $v^*$ 偏离 $15\,\mathrm{m/s}$ 时性能衰减多少；未做多平衡点数据采集对照 |
| 16 | 在线可计算性："its mean computation time during this experiment is $28.07\,\mathrm{ms}$ in a laptop computer equipped with Intel Core i7-11800H CPU and 32 G RAM"；Remark 5"about $28.07\,\mathrm{ms}$" | §VI-B 正文；Remark 5（决策变量数 $2mn+2n+Nm$；与 MPC 的比较） | `C_int` | 未检 | 是（数字被报告），但不可核验 | 未给求解器名称/版本/容差、未给计时样本数与统计量（均值？中位数？worst case？）、未说明是否含 Hankel 矩阵构造与初始状态估计；**换算：$28.07\,\mathrm{ms}/50\,\mathrm{ms}=56.1\%$ 的采样预算**【计算值】 |

---

## 三、方法可复现性清单

| 项 | 论文是否给出 | 具体位置 | 缺失影响 |
|---|---|---|---|
| 1. 数据来源与版本 | **部分给出**。仿真生成：HDV = OVM (2) + $\mathbb{U}[-0.1,0.1]\,\mathrm{m/s^2}$ 噪声；离线数据 = OVM 预设计 CAV 控制器 (40) + $\delta_u\in[-1,1]\,\mathrm{m/s^2}$ + 头车 $\epsilon$ 式 (41)。**无真实数据集、无版本号**。代码链接 `https://github.com/soc-ucsd/DeeP-LCC` 未给 commit/快照日期 | §VI 开头；§VI 离线数据采集条目；Appendix B（式 40、41）；§VI 脚注 4 | 无法确认"预采集轨迹"作为混行数据代理的有效性；无 commit 则无法冻结复现基线；真实数据路线完全没法评估 |
| 2. 预处理与划分方式 | **未给出**（无训练/验证/测试划分概念）；仅有"选一条轨迹构造 Hankel 矩阵"的做法。图 3(c) 用的是**哪一条**轨迹、如何选取，**未说明** | §VI-A"using one single pre-collected trajectory"；§VI-B"the same pre-collected data set"；Appendix B"we present one pre-collected trajectory in Fig. 8 ... which is also utilized in Experiments B and C" | 无法复现 Fig. 3(c) 的单条轨迹结果；无法判断性能对"选哪条轨迹"的敏感性（作者只说"Different pre-collected trajectories might influence the performance"） |
| 3. 模型/实验装置规格 | **给出**：$n=8$（头车后 8 辆），$m=2$（CAV），$S=\{3,6\}$，$\Delta t=0.05\,\mathrm{s}$；车辆为**质点跟驰模型**（无车辆动力学、无执行器一阶/二阶滞后、无传感噪声） | §VI 第 2 段；式 (2)(9)(14)(25) | 无执行器动力学与感知噪声 → "acceptable for real-time implementation" 的外推受限；横向/转向完全不在模型内 |
| 4. 超参数与搜索空间 | **给出最终值，未给搜索过程**：$N=50$，$T_{\mathrm{ini}}=20$，$w_v=1$，$w_s=0.5$，$w_u=0.1$，$\lambda_g=10$，$\lambda_y=10000$，$s_{\min}=5\,\mathrm{m}$，$s_{\max}=40\,\mathrm{m}$，$a_{\min}=-5$，$a_{\max}=2\,\mathrm{m/s^2}$；OVM nominal $\alpha=0.6,\beta=0.9,v_{\max}=30,s_{\mathrm{st}}=5,s_{\mathrm{go}}=35,v^*=15$ | §VI 在线控制条目；§VI-A | **无消融、无敏感性分析**：无法判断结果对 $\lambda_g,\lambda_y$（两个正则权重相差 3 个数量级）的依赖；无法判断 $N,T_{\mathrm{ini}}$ 的选择依据 |
| 5. 随机种子 / 重复次数 | **未给出**。Experiment A 说"100 trajectories ... carry out the same experiment"，但**无种子、无独立重复次数**；Experiment B/C **未说明重复次数**（从 Fig. 5/7 看为单次） | §VI-A；Fig. 4 图注 | 无法复现 Fig. 4 的 mean/SD；无法判断 Experiment B/C 的单次结果是否落在随机波动内 |
| 6. 评价指标定义（含边界情况） | **部分给出**：$J(y,u)$ 式 (31)；燃油率 $f_i$（瞬时模型，引自 [51]）；MSVE 公式。**但 MSVE 的车辆索引口径自相矛盾**：正文"we consider the fuel consumption and velocity errors for the vehicles indexed from $3$ to $8$"，而公式求和为 $\sum_{i=1}^{n}$。另"up to X%"的最大值选取规则**未定义** | §VI-B（燃油模型、MSVE 定义）；Fig. 6 图注 | MSVE 口径二义导致降幅不可复算（含不可控的前 2 辆 HDV 会稀释降幅）；"up to"的选取空间未声明 → Fig. 6 的百分比无法独立重算 |
| 7. 基线实现来源 | **部分给出**：基线 ① all-HDV（OVM，参数在 §VI-A 与 Table I）；基线 ② 本文自实现的 output-feedback MPC（式 (23)，用精确线性化模型 (25) 或 nominal 参数）。**未给** MPC 的求解器、终端代价、状态估计器实现、调参预算。**ACC/CACC 基线未实现** | 式 (23)；§VI-A"the other parameters ... remain the same between MPC and DeeP-LCC"；§VI-B"MPC controller still utilizes the nominal parameter setup" | 无法判断"MPC 与 DeeP-LCC 同等调参预算"是否真成立（只有一句声明，无预算清单）；Experiment B/C 中 MPC 被输出侧失配，公平性只能部分成立 |
| 8. 显著性检验方法 | **未给出**（全文无任何检验、无 p 值、无 CI） | 全文；Fig. 4 图注仅给 mean 与 SD | 所有"comparable / improvement / up to"结论均为**描述性**，不可推断 |
| 9. 代码/数据可用性声明 | **有代码链接**：`https://github.com/soc-ucsd/DeeP-LCC`（§VI 脚注 4）。**无数据可用性声明、无 commit/版本、无许可证说明**。本笔记**未联网核验**该仓库状态 | §VI 脚注 4 | 需固定 commit 才能复现；仓库可用性未核验 → 引用时须标注"代码链接由作者提供，本笔记未核验" |

---

## 四、关键数字表

> 只抄论文明确印出的数字。单位、样本量与设置跟数字同行。`[计算值]` 为本笔记按论文公式复算所得，**不是**论文印出的数字，不得作为文献报告值引用。`[估读]` 为图内目测（本表未使用估读数字）。

| 指标 | 值 | 不确定度 | 出处（表/图/节） | 备注（哪个实验、哪个设置） |
|---|---|---|---|---|
| MPC 平均真实代价 $\bar J$ | $2.91\times10^{4}$ | SD $0.003\times10^{4}$（$=30$） | Fig. 4 图注；§VI-A | Experiment A，正弦扰动，100 次实验，$n=8,m=2,S=\{3,6\}$，MPC 用**精确线性化模型** |
| DeeP-LCC 平均真实代价 $\bar J$ | $3.05\times10^{4}$ | SD $0.077\times10^{4}$（$=770$） | Fig. 4 图注；§VI-A | 同上；DeeP-LCC 用预采集轨迹数据 |
| 最优性损失（DeeP-LCC vs MPC） | $4.8\%$ | 未报告 | §VI-A 正文 | **本笔记复算**：$(3.05-2.91)/2.91=4.81\%$ → **自洽 ✓**【计算值】 |
| 两控制器 SD 之比 | 未报告 | — | — | **本笔记复算**：$0.077/0.003\approx25.7$ 倍【计算值】 |
| Experiment A 实验次数 | $100$ | 未报告 | §VI-A；Fig. 4 图注 | 100 条 $T=800$ 轨迹各跑一次；无种子 |
| 燃油消耗降幅（DeeP-LCC） | $24.69\%$ | 未报告 | §VI-C；§I-B；Abstract | Experiment C **紧急制动**场景，渗透率 $25\%$，对比 all-HDV |
| 燃油消耗降幅（MPC） | $25.12\%$ | 未报告 | §VI-C | 同一场景；**MPC 略优** |
| 燃油消耗降幅（DeeP-LCC，最大） | $9.05\%$ | 未报告 | §VI-B | Experiment B **城市**工况 **Phase 3**，"up to" |
| MSVE 降幅（DeeP-LCC，最大） | $43.82\%$ | 未报告 | §VI-B | Experiment B **高速**工况 **Phase 1**，"up to" |
| DeeP-LCC 平均计算时间 | $28.07\,\mathrm{ms}$ | 未报告（无样本数/worst case） | §VI-B；Remark 5 | 平台：laptop，Intel Core i7-11800H CPU，32 GB RAM；规模 $n=8,m=2$ |
| 计算时间 / 采样周期 | — | — | — | **本笔记复算**：$28.07/50=56.1\%$ 采样预算【计算值】 |
| 预采集轨迹长度 $T$ | $800$ samples | 未报告 | §VI；Appendix B | $\Delta t=0.05\,\mathrm{s}$ → $40\,\mathrm{s}$ 数据【计算值】 |
| $T$ 的理论下界 | $257$ samples | — | Appendix B；式 (27) | $\lceil(m+1)(T_{\mathrm{ini}}+N+2n)-1\rceil$；**本笔记复算**：$3\times(20+50+16)-1=257$ → **自洽 ✓**【计算值】；$=12.85\,\mathrm{s}$【计算值】 |
| 预测时域 $N$ / 初始时域 $T_{\mathrm{ini}}$ | $50$ / $20$ | — | §VI | 采样步数 |
| 车辆规模 | $n=8$（头车后）、$m=2$ | — | §VI | CAV 位置 $S=\{3,6\}$ |
| CAV 渗透率 | $25\%$ | 未报告 | §VI；§I-B；Abstract | $2/8$（**不含头车**）；含头车则为 $2/9=22.2\%$【计算值】 |
| 代价权重 | $w_v=1$，$w_s=0.5$，$w_u=0.1$ | — | §VI | 式 (31) |
| 正则权重 | $\lambda_g=10$，$\lambda_y=10000$ | — | §VI | 式 (37) |
| 间距约束 | $s_{\min}=5\,\mathrm{m}$，$s_{\max}=40\,\mathrm{m}$ | — | §VI | §V-C 约束（正文以 $\tilde s$ 表达，仿真条目以 $s$ 表达） |
| 加速度约束 | $a_{\min}=-5\,\mathrm{m/s^2}$，$a_{\max}=2\,\mathrm{m/s^2}$ | — | §VI | 对 HDV 亦经饱和施加 |
| HDV 加速度噪声 | $\mathbb{U}[-0.1,0.1]\,\mathrm{m/s^2}$ | — | §VI 开头 | 加到式 (2) |
| 数据采集用 CAV 噪声 | $\delta_u\in[-1,1]\,\mathrm{m/s^2}$ | — | Appendix B 式 (40) | i.i.d. |
| 头车速度扰动（采集期） | $\delta_\epsilon\sim\mathbb{U}[-1,1]\,\mathrm{m/s}$ | — | Appendix B 式 (41) | 每 $10$ 步（$0.5\,\mathrm{s}$）变一次 |
| OVM nominal 参数（Exp A 全体 HDV） | $\alpha=0.6$，$\beta=0.9$，$v_{\max}=30$，$s_{\mathrm{st}}=5$，$s_{\mathrm{go}}=35$，$v^*=15$ | — | §VI-A | 单位：$\alpha$（1/s），$\beta$（无量纲），$s$（m），$v$（m/s） |
| 平衡间距 $s^*$（nominal） | 未印出 | — | — | **本笔记复算**：由 (13) 得 $s^*=20\,\mathrm{m}$；由 (42) 得 $\arccos(1-2\cdot15/30)\cdot30/\pi+5=20\,\mathrm{m}$ → **两途径一致 ✓**【计算值】 |
| 决策变量数（DeeP-LCC） | 下界 $2mn+2n+Nm$ | — | Remark 5 | **本笔记复算**：$=148$；MPC 为 $Nm=100$；增量 $48$ → 相对 MPC $+48\%$，而正文称"slightly larger"【计算值】 |
| 安全/碰撞事件统计 | **未报告** | — | — | 无最小间距时间序列、无 TTC、无碰撞次数、无约束触发次数 |
| 弦稳定性指标 | **未报告** | — | — | 全文无 |

### 数字口径对照表

**触发条件**：同一指标出现 ≥2 个数值（燃油降幅出现在 3 处口径），且 MSVE 与渗透率存在口径二义。

| 指标 | 数值 | 实验/场景 | Phase | 对比基线 | 其他设置 | 出处 |
|---|---|---|---|---|---|---|
| 燃油消耗降幅（DeeP-LCC） | $24.69\%$ | Experiment C：紧急制动 | 未按 Phase 划分 | all-HDV | $25\%$ CAV，$n=8,m=2$，单次仿真 | §VI-C |
| 燃油消耗降幅（MPC） | $25.12\%$ | Experiment C：紧急制动 | 未按 Phase 划分 | all-HDV | 同上，MPC 用 linearized model | §VI-C |
| 燃油消耗降幅（DeeP-LCC，最大） | $9.05\%$ | Experiment B：NEDC 城市 | **Phase 3** | all-HDV | 同上，异质 HDV（Table I）；"up to" 为跨 Phase 取最大 | §VI-B |
| 燃油消耗降幅（DeeP-LCC，最大） | $43.82\%$（**注意：此值为 MSVE 降幅，非燃油**） | Experiment B：NEDC 高速 | **Phase 1** | all-HDV | 同上；"up to" | §VI-B |
| MSVE 降幅（DeeP-LCC） | $43.82\%$ | Experiment B：NEDC 高速 | Phase 1 | all-HDV | **口径二义**：正文限定 vehicles $3$–$8$；公式 (MSVE) 为 $\sum_{i=1}^{n}$。两种口径给出不同的归一化分母与不同的降幅 | §VI-B |
| 真实代价 $\bar J$（MPC） | $2.91\times10^{4}$ | Experiment A | 不适用 | 不适用（自身基准） | 100 次，nominal HDV | Fig. 4 图注 |
| 真实代价 $\bar J$（DeeP-LCC） | $3.05\times10^{4}$ | Experiment A | 不适用 | 不适用 | 100 次，nominal HDV | Fig. 4 图注 |
| CAV 渗透率 | $25\%$ | 全部实验 | — | — | 分母 $=n=8$（不含头车） | §VI |
| CAV 渗透率（另一口径） | $22.2\%$【计算值】 | 全部实验 | — | — | 分母 $=n+1=9$（含头车）→ $2/9$ | 本笔记复算 |

**引用纪律**：引用上述任一数字，必须连同"实验名 + Phase + 对比基线 + 是否单次 + 渗透率口径"一并给出；`43.82%` 必须写明是 **MSVE（均方速度误差）降幅**，不得写成燃油降幅。

---

## 五、统计与推断旗标

1. **全文无任何显著性检验**。无 p 值、无置信区间、无效应量。唯一的不确定度报告是 Fig. 4 图注的 mean ± SD（$2.91\pm0.003$ 与 $3.05\pm0.077$，单位 $10^4$）。→ 所有"comparable / improvement"结论均为**描述性**。
2. **"无差异"未被检验 → 推断旗标（严重）**。"comparable performance with respect to MPC" 是一个**等价性主张**，但未做等价/非劣检验（TOST 或 bootstrap CI）。按本技能判据：以"未检出差异"推"性能相当"属推断强度不匹配。
3. **方差异质未处理**。MPC SD $=0.003\times10^4$（$=30$）与 DeeP-LCC SD $=0.077\times10^4$（$=770$）相差约 $25.7$ 倍。任何均值比较都应使用 Welch 校正；本文未报检验，故无从判断。均值差 $=0.14\times10^4=1400$，约为 DeeP-LCC 自身 SD 的 $1.8$ 倍——即两控制器分布大幅重叠，"可比"与"略差"在统计上不可分。
4. **多重比较未校正 → 假阳性膨胀风险**。"up to $9.05\%$"与"up to $43.82\%$"是在 Experiment B 的**多个 Phase** 上取最大值（Fig. 6 横轴为 P#），既未校正多重比较，也未声明最大值是在多少个候选口径中选出。→ 这两个数字是**选择性报告的上界**，不是无偏效应量。
5. **Experiment B/C 无重复**。从 Fig. 5、Fig. 7 与正文叙述看为单次仿真；无种子、无独立重复 → 无法判断单次结果是否超出随机波动。
6. **无随机化/无对照分配**。改进了多少，来自同一仿真器上"切换控制器"的反事实对比，不是随机化对照设计；因果措辞（"DeeP-LCC reduces up to $24.69\%$"）强于设计所能支撑的强度。
7. **无敏感性分析**。$\lambda_g,\lambda_y$、$N$、$T_{\mathrm{ini}}$、$w_v,w_s,w_u$ 均只给单点值，无扫描 → 性能对超参的稳健性未知。
8. **等价性定理是转引，非本文结论**。"DeePC is equivalent to sequential system identification and MPC for deterministic LTI systems [26, 28]"引自他人；本文自己的式 (37) 含**外部扰动输入** $\epsilon$，作者明言"we leave its theoretical investigation for future research"（Remark 3）。→ 不得把该等价性读作本文对 DeeP-LCC 的证明。
9. **"safety guarantees"是条件性措辞，易被读成无条件保证**。约束可行性成立时才有保证，且递归可行性被留给 future work。→ 引用时不得写成"保证无碰撞"。
10. **全部证据为仿真**。按本项目 `AGENTS.md` §1 红线，本文结果**不得**表述为实车验证；本文自身也未如此声称（正确）。
11. **统计口径缺失**：$28.07\,\mathrm{ms}$ 未说明是均值/中位数、样本量、是否包含 Hankel 构造与状态估计；无最坏情形。→ "acceptable for real-time implementation"不可核验。
12. **正常性/分布假设未检验**。Fig. 4 有 100 个 cost 样本，但未报分布形状；未做正态性或异常值检查。

---

## 六、缺失信息清单

**A. 未报告**

1. **未报告：随机种子与重复次数**（Experiment A 的 100 条轨迹、Experiment B/C 的运行次数与种子）。
   - 影响：无法复现 Fig. 4 的 mean/SD；无法判断 B/C 的单次结果是否落入随机波动；无法做种子 ≥5 的 mean ± std 报告（与本项目 `AGENTS.md` §4 的要求直接冲突）。
   - 最小补法：向作者索取种子列表或种子生成脚本，并固定 GitHub commit hash。
2. **未报告：Experiment B/C 的仿真时长与 Phase 起止时间**（MSVE 定义含 $t_0,t_f$，但正文只给"Phase"编号）。
   - 影响：MSVE 数值无法归一化复算，Fig. 6(b) 的 $43.82\%$ 不可独立验证。
   - 最小补法：给出每 Phase 的起止时刻表与总仿真时长。
3. **未报告：QP 求解器与计时口径**（求解器名称/版本/容差/最大迭代；$28.07\,\mathrm{ms}$ 的统计量与样本数；是否含 Hankel 构造与初始状态估计）。
   - 影响：无法复核实时性结论；$28.07\,\mathrm{ms}$ 相对 $\Delta t=50\,\mathrm{ms}$ 的 $56.1\%$ 裕度是否在最坏情形下成立，完全不可知。
   - 最小补法：给出求解器与容差、计时脚本、以及 mean/median/p95/worst-case 四个统计量。
4. **未报告：任何安全事件统计量**（最小车间距时间序列、TTC、约束触发次数、碰撞/近碰次数）。
   - 影响："driving safety"与"collision-free guarantees"只有约束式与曲线，无事件计数 → 无法支撑系统级安全结论。
   - 最小补法：逐场景报告最小间距与约束违反次数。
5. **未报告：弦稳定性或闭环稳定性判据**。
   - 影响：CAV 介入后上游车流的扰动是否被放大，缺少形式化判据；"smoothing mixed traffic flow"仅有曲线与百分比支撑。
   - 最小补法：给出闭环传递函数/放大率指标（如 $\lVert H(z)\rVert_\infty\le1$）或引理式证明。
6. **未报告：真实交通数据上的任何验证**，且**未报告** [47] 的微型车队实验细节（本文只在 Remark 3 提及该后续工作存在）。
   - 影响：无法判断从"仿真生成的 40 s 轨迹"到真实混行数据的可迁移性。
   - 最小补法：在本文或后续工作中报告真实/半实物数据的采集协议与性能对照。
7. **未报告：ACC / CACC / CCC / LCC 基线的实现与数字**。
   - 影响：无法把本文结果放入"人类驾驶 → ACC → CACC → LCC → DeeP-LCC"的递进比较框架中。
   - 最小补法：至少补一个 CACC 或 LCC 基线（LCC 有 [11] 可依）。

**B. 报告但不可核验**

8. **报告但不可核验：代码仓库 `https://github.com/soc-ucsd/DeeP-LCC`**（无 commit、无版本、无快照日期；本笔记**未联网核验**其可访问性与内容）。
   - 需要什么才能核验：仓库 URL + commit hash + 许可证；或随论文提供的补充材料归档（如 Zenodo DOI）。
9. **报告但不可核验：Table I 的异质 HDV 参数与 nominal 之间的失配程度未被量化**（只说 MPC 用 nominal、HDV 用 Table I）。
   - 需要什么才能核验：给出 $\alpha_1,\alpha_2,\alpha_3$ 在 Table I 与 nominal 下的相对偏差表，或直接给出 MPC 与 DeeP-LCC 各自的"模型误差"指标。
   - 影响：Experiment B/C 中"MPC 被失配"这一关键公平性问题只能定性判断。
10. **报告但不可核验：$4.8\%$ 最优性损失的统计显著性**（本文未检验；本笔记只能复算其算术值 $4.81\%$）。
    - 需要什么才能核验：100 个样本的原始 cost 序列（或分布图）+ 配对检验/Welch 检验结果。

**C. 报告口径有歧义**

11. **报告口径有歧义：MSVE 的车辆索引范围**。正文：燃料与速度误差只统计 vehicles $3$–$8$；公式：$\mathrm{MSVE}=\frac{\Delta t}{n(t_f-t_0)}\sum_{t}\sum_{i=1}^{n}(v_i-v_0)^2$，分母为 $n=8$ 且求和自 $i=1$。
    - 两种解释会导致结论如何不同：若按公式含车辆 1–2（CAV 无法影响的前两辆 HDV），其大偏差会**抬高** MSVE 基数，从而**放大**降幅；若按正文只算 3–8，降幅更保守。故 $43.82\%$ 的符号不变但量级不可比。
    - 最小补法：明示求和与分母口径，并给出两套口径的结果。
12. **报告口径有歧义：CAV 渗透率的分母**。正文以 $m/n=2/8=25\%$；系统实际含头车共 $n+1=9$ 辆。
    - 两种解释会导致结论如何不同：$25\%$ vs $22.2\%$【计算值】。与其他文献的"渗透率"对齐时，若对方含头车，则本文的"25%"实为更低渗透率，即**在更有利的设置下取得**。
    - 最小补法：显式写清分母定义（是否含头车、是否含所有车道车辆）。
13. **报告口径有歧义：$28.07\,\mathrm{ms}$ 的计时边界**（是否含 Hankel 矩阵构造、past-data 更新、QP 预处理）。
    - 两种解释会导致结论如何不同：若不含预处理，实际单步耗时可显著高于 $28.07\,\mathrm{ms}$，$56.1\%$ 的采样预算占比会被低估。

---

## 七、复用价值判断

| 问题 | 结论 |
|---|---|
| 方法可否搬到我的问题？需要改什么？ | **不能直接搬，但可作对照口径**。DeeP-LCC 是**离散时间、非参数、滚动时域 QP** 的 system-level 控制器（$S$ 集合上的全流代价），无任何神经网络/无训练；P1 是**连续时间 LNN（CfC）** + OTF 势场。要搬需替换三处：① 行为表征（Hankel/基本引理 → LNN 隐状态）；② 数据依赖（须预采集轨迹且满足持续激励 → OTF 标量 + 前车扰动模型）；③ 代价口径（$J$ 的加权输出偏差 → P1 的 RMSE/Jerk/横向指标）。 |
| 评价协议可否直接对齐（指标、划分、基线）？ | **可对齐者**：OVM 跟驰模型 + Table I 异质参数、交通场景（正弦扰动／NEDC Phase／急刹）、加速度与间距约束边界、瞬时燃油模型（式在 §VI-B 完整印出，引自 [51]，可直接实现）。**不可对齐者**：本文无 ACC/CACC 基线、无弦稳定性、无横向/换道、无 MCU 资源指标、无端到端延迟口径。 |
| 数据/代码可否直接取用？许可如何？ | 代码链接由作者给出（`https://github.com/soc-ucsd/DeeP-LCC`），**本笔记未核验**其可访问性、内容与许可证。论文未提供数据文件，也未给数据许可声明。→ 复用前须由 `citation-and-related-work` 核验仓库与许可证；未核验前不得写入 P1 稿件。 |
| 若要引用其数字，引用时**必须**带上的限定语是什么？ | 见下方 `citation_qualifier` 单行。核心要素：**单车道纵向纯跟驰、8 车 2 CAV（25% 口径含歧义）、全仿真无实车、数据为仿真生成的 40 s 单轨迹、性能数字为单次/仅均值、无检验无种子、基线仅 all-HDV 与自实现 MPC、"up to"为分 Phase 最大值、无弦稳定性结论**。 |

```
citation_qualifier: OVM single-lane pure-longitudinal mixed traffic, n=8 vehicles behind 1 head vehicle with m=2 CAVs at S={3,6} (=25% CAV penetration using denominator n=8, excluding the head vehicle; 22.2% if the head vehicle is counted), simulation-only with no vehicle/hardware test in this paper (the referenced real-world miniature experiments are a separate follow-up [47]), pre-collected data = 1 simulated trajectory of T=800 samples at dt=0.05 s (=40 s; theoretical lower bound 257 samples = 12.85 s) generated by an OVM pre-designed CAV controller with uniform noise and used for ALL experiments, 100 trajectories used only for the Experiment A cost statistics, single equilibrium v*=15 m/s during data collection whereas the simulated equilibrium is time-varying under the unverified assumption that HDV behaviour is similar across equilibria, performance numbers are single-run or mean-only with NO significance test, NO seeds and NO confidence intervals (only Fig. 4 reports mean +/- SD), the reported SDs differ by ~25.7x between MPC and DeeP-LCC, baselines are all-HDV (OVM) and a self-implemented output-feedback MPC only (no ACC/CACC/CCC/LCC baseline), the 'up to X%' values are per-Phase maxima over the NEDC phases without multiplicity correction, the 'collision-free' claim holds only conditional on constraint feasibility because recursive feasibility is explicitly left to future work, and NO string-stability result is reported.
```

---

## 八、红队三条

**1. 领域最懂的人（LCC / DeePC 方向）会质疑：**
"你宣称'comparable to MPC'，但你的 MPC 只在 Experiment A 里精确匹配；在 Experiment B/C 中 HDV 用 Table I 异质参数、MPC 却用 nominal（§VI-B 明写），MPC 被刻意失配。即便如此，**紧急制动场景里 MPC 仍略优于你（$25.12\%$ vs $24.69\%$）**，Experiment A 里你又损失 $4.8\%$。全文**没有任何一个设置**显示 DeeP-LCC 优于 MPC。那么真正的贡献只是'不需要模型'，不是'更好'——而这一点你自己也承认（'MPC is not easily applicable in practice'）。"
- **需要什么证据才能消解**：① 让 MPC 与 DeeP-LCC **同等失配**（同一模型误差分布）的对照实验；② 模型误差从 0 增大的**扫描曲线**，给出 DeeP-LCC 与 MPC 的交叉点；③ 或一个 MPC 无法建模但 DeeP-LCC 可用的场景（如非线性饱和、时变参数）上的对比。

**2. 方法与统计视角会质疑：**
"你的核心定量证据只有 Fig. 4 的 100 次实验，而且只报 mean ± SD：**没有检验、没有种子、没有 CI**，两控制器 SD 相差约 $25.7$ 倍（$30$ vs $770$），你却用'comparable'这个等价性措辞——等价性必须用 TOST 之类的等价检验来支撑。'up to $9.05\%$'与'up to $43.82\%$'是在 Experiment B 的多个 Phase 上**取最大值**，未做多重比较校正，是选择性报告的上界。更严重的是，你写'collision-free guarantees'，却把 recursive feasibility 明确留给 future work——那么在最坏情形下约束可能不可行，**安全保证不成立**。另外 MSVE 的定义公式（$i=1..n$）与正文口径（vehicles 3–8）自相矛盾，你的降幅到底按哪个算？"
- **需要什么证据才能消解**：① Welch 检验或 bootstrap CI；② 以 TOST 支撑"comparable"；③ Phase 层多重比较校正或直接报全 Phase 表；④ recursive feasibility 的证明，或在 $\sigma_y$ 有界条件下给出可行性充分条件 + 最小间距经验分布；⑤ MSVE 两套口径的结果并列。

**3. 编辑 / 邻域读者会质疑：**
"8 辆车的单车道纯纵向跟驰仿真、**单一 $25\%$ 渗透率**、无换道、无横向动力学、无弦稳定性、无真车、无 ACC/CACC 基线——这能支撑'improving traffic efficiency, driving safety, and fuel economy'这种系统级结论吗？'driving safety'甚至连一个安全事件计数都没有。而且你的'预采集数据'是仿真生成的：把 DOI 拿走，读者会以为你用了真实混行轨迹。"
- **需要什么证据才能消解**：① 渗透率扫描（如 10/25/50%）与更大 $n$ 的规模扫描；② 闭环弦稳定性指标或放大率；③ 至少一个高保真平台（SUMO / VISSIM / CARLA）或微型车队实测；④ 明确写出"预采集数据为仿真生成"于摘要或实验节首句，避免读者误读。

> **校准记录（按技能 §8 要求：红队若推翻等级，必须回改台账）**：红队第 2 条直接导致台账中 **#6（vs MPC 可比）** 与 **#11（collision-free guarantees）** 的内部等级维持在 `C_int`（未上调），并新增 §五 旗标 2、3、4、9。台账未做降级（原文已按 `C_int` 记录），故 §二 与 §四 无需回改数值。

---

## 九、限制

1. **材料限制**：仅有 arXiv HTML 抽取的纯文本全文（97,265 字符 / 1,383 行）。**未获** IEEE TCST 正式排版版、补充材料、代码仓库快照、原始数据。后果：§三 清单中第 2 项（预处理与划分）与第 5 项（种子/重复）**无法判定**；Fig. 3/5/7 的曲线数值未提供，cost 与 MSVE **无法从图复算**；Fig. 6 的分相柱高只能靠正文"up to"数字转录。
2. **复算限制**：未获原始数据，只能做**自洽性检查**。本次已做的三项复算均通过：$T$ 下界 $257=3\times86-1$ ✓；$4.8\%\approx(3.05-2.91)/2.91=4.81\%$ ✓；$s^*=20\,\mathrm{m}$ 由式 (13) 与式 (42) 两途径一致 ✓。**无法**验证方差、异常值与任何统计量（论文本身也未报检验）。
3. **视角限制**：本笔记**不评价**该工作的**重要性**与**新颖性**（那是主编视角，交给 `cross-paper-synthesizer` 与 `research-gap-hunter`）。也不做外部复现检索——§二 的"外部复现"列一律为 `未检`，**不等于**"无外部证据"。
4. **转引限制**：对 [11]（LCC）、[26]（DeePC）、[45][46]（递归可行性与稳定性）、[47]（微型车队实测）的内容判断**均以本文转述为准**，未回溯原文核验。
5. **元数据限制**：任务给定作者串与 DOI 真实作者串不符（详见 §作用域）。本笔记未联网核验 DOI 状态、页码与卷期。
6. **时效限制**：精读日期 2026-10-02（抓取日期同为 2026-10-02）；若该文此后有更正、撤稿或重大修订，本笔记未反映。缓解：入稿引用前由 `citation-and-related-work` 复核 DOI 状态与正式版页码。

---

## 十、对 P1 的三条具体可用结论

### ① P1 与 DeeP-LCC 的可检验差异（三个维度：数据 / 假设 / 指标）—— **并核对任务给定说法的原文证据**

**任务给定说法**："它需要事先采集足量混行轨迹做数据驱动预测，P1 只用 OTF 标量 + 前车扰动模型。"

**原文核对结论：该说法"一半站得住、一半站不住"，必须改写后才能进 P1 稿件。**

- **站得住的一半（有原文证据）**：DeeP-LCC 的**唯一**行为表征来源就是预采集轨迹。Proposition 2 与式 (29)/(37) 中，预测完全由 Hankel 矩阵列空间给出；Assumption 2 要求输入序列**持续激励**（order $T_{\mathrm{ini}}+N+2n$）；式 (27) 给出长度下界 $T\ge(m+1)(T_{\mathrm{ini}}+N+2n)-1$，本文取值 $257$（$=12.85\,\mathrm{s}$），实际取 $T=800$（$=40\,\mathrm{s}$）。作者明言"requires no prior knowledge of the system model"。→ **"需要事先给定一段满足持续激励的输入/输出轨迹"**成立。
- **站不住的一半（原文没有证据）**：论文中的这段数据**不是采集来的混行轨迹**，而是**仿真生成**的（Appendix B：CAV 用 OVM 预设计控制器 + $\delta_u\sim\mathbb{U}[-1,1]\,\mathrm{m/s^2}$；头车 $\epsilon\sim\mathbb{U}[-1,1]\,\mathrm{m/s}$，每 $0.5\,\mathrm{s}$ 变一次）。原文对真实数据的表述只是可能性——"could be generated offline, **or** collected from the historical trajectories of those involved vehicles"——**全文没有任何真实轨迹采集实验、数据集名称或数据许可**。→ 因此**不能**写"它需要事先采集**足量混行**轨迹"；应写"它需要事先给定一段（论文中为仿真生成的 $40\,\mathrm{s}$）满足持续激励的轨迹数据，且该数据须来自**单一平衡点**"。

**三条可检验差异（每条都给出可判定的操作化定义）**

| 维度 | DeeP-LCC | P1（OTF-CfC） | 可检验判据 |
|---|---|---|---|
| **D1 数据** | 依赖一段满足 Assumption 2 的预采集轨迹；长度有**硬下界** $T\ge257$ samples（$12.85\,\mathrm{s}$），低于此 Hankel 矩阵非行满秩 | 只依赖 OTF 标量（超车频次势场）与前车扰动模型的解析形式，**无数据长度下界** | 把可用轨迹长度从 $12.85\,\mathrm{s}$ 扫到 $40\,\mathrm{s}$ 再到更长：DeeP-LCC 的 cost/燃油降幅应在下界附近出现**台阶式恶化**；P1 应表现为**与数据长度无关**（唯一随机性来自种子）。若 P1 也随数据长度变化，则 D1 差异不成立 |
| **D2 假设** | 需要"HDV 在不同平衡点附近行为相似"这一**未验证假设**（Remark 6："This assumption indeed may not hold"；Appendix C 明言性能"might be compromised"）；数据在**单一平衡点 $15\,\mathrm{m/s}$** 采集 | OTF 是跨工况定义的交通社会压力标量，**不预设单一平衡点**（须由 P1 自己在稿件中证明这一点，见下"待补"） | 把仿真平衡速度显式设为 $5/15/25\,\mathrm{m/s}$ 三档（数据仍在 $15\,\mathrm{m/s}$ 采集），测两端性能衰减：DeeP-LCC 的衰减量应显著大于 P1。论文**自认会衰减但未量化** → 这正是 P1 可占的可检验空白 |
| **D3 指标** | 报 system-level 的**燃油率**（瞬时模型，引自 [51]）与 **MSVE**（相对头车速度的均方误差）；报加权累积代价 $J$；报计算时间 | 报跟车误差 RMSE、加速度平方积分、Jerk 峰值、车道居中偏差、前轮转角方差、端到端延迟、MCU 内存占用 | DeeP-LCC **未报告** jerk、未报告相对期望间距的 RMSE、未报告内存；P1 **未报告** MSVE/燃油。故 D3 只有"P1 补算 MSVE + 燃油，DeeP-LCC 侧无法补算 jerk/RMSE"这一**单向**可检验差异。燃油模型公式已在 §VI-B 完整印出 → **P1 可直接实现同一燃油模型**，从而使燃油指标**变为可比** |

**待 P1 自己补齐（不在本文证据范围内）**：P1 稿件若要主张"OTF 不预设单一平衡点"，必须给出 OTF 的定义域与跨平衡点验证，本文不能替 P1 提供该证据。

### ② DeeP-LCC 的混合交通设置，P1 能否直接复用为基准

**设置清单（全部来自原文）**

| 项 | 值 | 出处 |
|---|---|---|
| 拓扑 | **单车道、纯纵向跟驰链**：1 辆头车（index 0）+ 其后 $n=8$ 辆 | §VI；Fig. 1 图注 |
| HDV / CAV 数量 | 6 辆 HDV + 2 辆 CAV（$n=8,m=2$） | §VI |
| CAV 位置 | $S=\{3,6\}$（第 3、第 6 辆） | §VI |
| 渗透率 | $25\%$（$2/8$，**不含头车**；含头车为 $22.2\%$【计算值】） | §VI |
| 跟驰模型 | **OVM**（式 (2)–(4)：$\dot v_i=\alpha(v_{\mathrm{des}}(s_i)-v_i)+\beta\dot s_i$） | §II-A |
| HDV 参数（Exp A） | 全体 nominal：$\alpha=0.6,\beta=0.9,v_{\max}=30,s_{\mathrm{st}}=5,s_{\mathrm{go}}=35,v^*=15$ | §VI-A |
| HDV 参数（Exp B/C） | **异质**，见 Table I | Table I |
| 扰动 | HDV 加速度加 $\mathbb{U}[-0.1,0.1]\,\mathrm{m/s^2}$ 噪声 | §VI |
| 场景 | (A) 头车正弦扰动；(B) NEDC（ECE-15 城市 + EUDC 高速）；(C) 头车紧急制动 | §VI-A/B/C |
| 约束 | $s\in[5,40]\,\mathrm{m}$；$a\in[-5,2]\,\mathrm{m/s^2}$ | §VI |
| 采样 | $\Delta t=0.05\,\mathrm{s}$ | §VI |
| 仿真平台 | **未报告具名平台**。仅给出运行环境：laptop，Intel Core i7-11800H，32 GB RAM；算法与脚本见 GitHub | §VI-B；§VI 脚注 4 |
| 基线 | ① all-HDV（OVM）；② 自实现 output-feedback MPC | §VI-A/B/C |

**Table I 完整转录（Heterogeneous Parameter Setup for HDVs in Experiments B and C）**

| HDV | $\alpha$ | $\beta$ | $s_{\mathrm{go}}$ (m) |
|---|---|---|---|
| HDV 1 | 0.45 | 0.60 | 38 |
| HDV 2 | 0.75 | 0.95 | 31 |
| HDV 3 | 0.70 | 0.95 | 33 |
| HDV 4 | 0.50 | 0.75 | 37 |
| HDV 5 | 0.40 | 0.80 | 39 |
| HDV 6 | 0.80 | 1.00 | 34 |
| **Nominal Setup** | **0.60** | **0.90** | **35** |

表注（原文）："The HDVs are indexed from front to end. For example, HDV 1 and HDV 2 are the two HDVs between the head vehicle and the first CAV." / "The other parameters follow the nominal setup: $s_{\mathrm{st}}=5,v_{\max}=30$."

**P1 能否直接复用为基准？—— 结论：跟驰模型层可直接复用，系统层不能整体复用。**

- **可直接复用（高价值）**：OVM 及其 nominal/异质参数集（Table I 六组值 + nominal）、扰动噪声分布、三个场景定义、间距与加速度边界、$\Delta t$、瞬时燃油模型公式（§VI-B）。这些都是**逐值印出**的，P1 可在 CARLA/Town04 中实现同参数的 OVM HDV 作为基准交通流。
- **不能复用为整体基准（三点硬障碍）**：
  1. **ODD 不匹配**：本文是**单车道纯纵向**，无换道、无横向动力学、无多车道。P1 的 ODD 是"高速公路主线、多车道、人工与自动混行"，且 P1 指标含**车道居中偏差**与**前轮转角方差**——本文对这两项**无任何对应设置**。若把本文场景当作 P1 基准，会失去 P1 的横向维度。
  2. **基线集不匹配**：本文只有 all-HDV 与自实现 MPC；**无 ACC、无 CACC、无 CCC、无 LCC 基线**。而 P1 的基线集是 ① PID ② MPC（线性化车辆模型）③ 学位论文 TD3 直控 ④ OTF-CfC。→ 本文的"MPC"可作 P1 的 MPC 基线参考实现思路，但不能替代 P1 的 PID 与 TD3 基线。
  3. **渗透率口径必须先统一**：本文的 $25\%$ 分母为 $n=8$（不含头车）。P1 若按含头车计（$2/9=22.2\%$）或按车道全部车辆计，会得到不同数字。**未统一口径前不得并排引用。**

### ③ 指标口径：与 P1 指标集的可比性判定

| DeeP-LCC 指标（含口径） | P1 对应指标 | 可比性判定 | 理由与操作建议 |
|---|---|---|---|
| $J(y,u)$ 式 (31)：$\sum(\lVert y\rVert_Q^2+\lVert u\rVert_R^2)$，$Q=\mathrm{diag}(w_v,w_s)$，$R=w_u I$，$w_v=1,w_s=0.5,w_u=0.1$ | 跟车误差 RMSE、加速度平方积分、Jerk 峰值（均为分解指标） | **不可比** | $J$ 是**带自由权重的加权和**，量纲混合（速度误差 m/s 与间距误差 m 同置一个标量）；权重一变数值全变。除非 P1 复现同一组权重并报同一 $J$，否则不可并排 |
| 燃油消耗降幅 $24.69\%$ / $9.05\%$（瞬时燃油模型，引自 [51]，公式在 §VI-B 完整印出） | **P1 指标集中无燃油项** | **潜在可比（需 P1 补算）** | 公式与系数（$0.444$、$0.090R_iv_i$、$[0.054a_i^2v_i]_{a_i>0}$，$R_i=0.333+0.00108v_i^2+1.200a_i$）均已印出 → **可直接实现**，实现后该项变为同协议可比。在此之前只能标"文献报告值，协议不同，不可直接比较" |
| **MSVE**（均方速度误差，相对**头车速度** $v_0$） | 跟车误差 RMSE（相对**期望间距/期望速度**） | **部分可比** | 两者都是"相对参考量的均方误差"，但参考量不同（头车速度 vs 期望间距）。**且 MSVE 自身口径二义**（正文 vehicles 3–8 vs 公式 $i=1..n$）。并对齐前须明示：参考量、求和车辆集合、分母、$\Delta t$ 归一化 |
| 计算时间 $28.07\,\mathrm{ms}$（i7-11800H，32 GB，laptop） | 端到端延迟、MCU 内存占用 | **不可比** | 平台完全不同（桌面 CPU vs 车规 MCU）。P1 按项目 `AGENTS.md` §3 须报 **MCU 型号、编译器与优化选项**；本文无任何 MCU/嵌入式数据。可比的只有"计算时间 / 采样周期"这一**相对比值**（本文 $56.1\%$【计算值】），前提是 P1 报出自己控制周期 |
| 速度/间距/加速度**曲线**（Fig. 3/5/7） | — | **不可比** | 纯视觉证据，无数值导出；不能提取数字用于对比 |
| 间距约束 $s\in[5,40]\,\mathrm{m}$；加速度约束 $a\in[-5,2]\,\mathrm{m/s^2}$ | 加速度平方积分、Jerk 峰值；可派生最小间距/TTC | **可比（作为约束一致性检查）** | 建议 P1 采用同一组边界做约束一致性对照；若 P1 边界不同，须显式说明并给出理由 |
| **弦稳定性** | **未列入本文指标，也未列入 P1 七项指标** | **双方都缺** | 本文只报 controllability/stabilizability/observability，**无闭环弦稳定性结论**；P1 若主张"编队"，则**双方都需要补**，且这不是本文能提供的对比项 |
| 安全事件（最小间距/TTC/碰撞数） | 车道居中偏差（横向安全） | **不可比且双缺** | 本文**未报告**任何安全事件统计量；P1 的横向安全指标在本文无对应物 |

**结论**：P1 的七项指标（跟车误差 RMSE、加速度平方积分、Jerk 峰值、车道居中偏差、前轮转角方差、端到端延迟、MCU 内存占用）中，**只有"跟车误差 RMSE"与 MSVE 部分可比**（需先统一参考量、求和集合与分母），**"加速度/Jerk"与本文的加速度约束边界可比**，**其余五项（车道居中偏差、前轮转角方差、端到端延迟、MCU 内存占用，以及燃油项）在本文中无对应或平台不可比**；其中"燃油"经 P1 补算同一模型后可转为可比。**不得**把本文的 $24.69\%$/$9.05\%$/$43.82\%$ 直接放进 P1 的性能对比句——按项目 `AGENTS.md` §1 红线，只能标"**文献报告值，协议不同，不可直接比较**"。
