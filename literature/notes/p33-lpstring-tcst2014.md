# 精读笔记 #33：Lp String Stability of Cascaded Systems: Application to Vehicle Platooning

文献：Ploeg J, van de Wouw N, Nijmeijer H. *Lp String Stability of Cascaded Systems: Application to Vehicle Platooning*. IEEE Transactions on Control Systems Technology, 2014, 22(2): 786–793. DOI: 10.1109/TCST.2013.2258346
全文来源：**已获全文**（TU/e 机构库 accepted manuscript PDF 提取，`fulltext/p33-lpstring-tcst2014.txt`，1351 行 / 49,889 bytes；原始 PDF `fulltext/_raw/p33-lpstring-tcst2014.pdf`，411,291 bytes）
原文版本说明（须随引用带上）：extracted from the **Accepted manuscript including changes made at the peer-review stage**（TU/e pure 页眉），非 publisher final layout；页码以期刊版 786–793 为准。
精读日期：2026-10-02（PDF 下载日期同） ｜ 提取方式：PDF→text，**该文原文即无表格**（已核实：全文 0 个 table，所有参数写在正文与图注中）

---

## 作用域

**场景①：项目内文献工作。**

- 归属项目：`D:\Deepseek Harness\auto-driving`（自动驾驶 OTF 论文集群）。
- 项目不变量文件：`D:\Deepseek Harness\auto-driving\AGENTS.md`（本笔记的全部结论受其约束）。
- 本次精读服务的**主张**：论文 1（P1，代号 **OTF-CfC**）——「基于超车频次势场与液态神经网络的高速主线编队连续时间控制」。
- P1 的**主张上限**（`AGENTS.md` §1，原文引用，本笔记不得越界）：
  - 「**P1 红线**：不得预先声称"OTF 势场带来 X% 性能提升"。」
  - 「**不得把仿真/回放写成实车验证**：CARLA（Town04）与实车数据回放都是仿真或开环证据。未做真车闭环前，措辞上限是"在 CARLA 与真实数据回放中"。」
  - 「**不得直接搬用他人论文数字**：……若未同协议复现，必须标注"文献报告值，协议不同，不可直接比较"。」
  - 本项目 ODD ＝ 高速公路主线、多车道、人工与自动混行（`AGENTS.md` §5）。
  - P1 指标（`AGENTS.md` §3）：跟车误差 RMSE、加速度平方积分（舒适性）、Jerk 峰值、车道居中偏差、前轮转角方差、端到端延迟、MCU 内存占用。
- 本文在 P1 中的**唯一用途**：作为 P1 必须报告的「**弦稳定性（string stability）指标的定义出处**」。评审会问"你的编队是否弦稳定、按哪个定义、在什么范数下"。
- **本笔记的使用边界**：本文的一切数值（h = 0.7 s、0.3 s、15.5 s/8.5 s 等）若进入 P1 稿件，均为「**文献报告值，协议不同（实车六车 CACC、线性时不变控制器、固定时距策略），不可与 P1 的 CARLA / 回放指标直接比较**」。本文的**实验是实车实验，不是仿真**——不得反向写成仿真，也不得据此声称 P1 的 CfC 编队弦稳定。
- 本笔记不评价该工作的**重要性**与**新颖性**（那是主编视角，交给 `cross-paper-synthesizer` / `research-gap-hunter`）。

---

## 一、作者主张

作者的核心主张是：文献中「string stability」一词既被当作**稳定性性质**、又被当作**性能指标**使用，含义已「rather ambiguous」，因此需要一个统一的**定义级**基础。为此作者用输入–输出（Lp）稳定性语言提出 Definition 1（Lp string stability / strict Lp string stability），把**外部扰动**（class K 函数 α）与**初始条件扰动**（class K 函数 β）同时纳入，且要求对**任意车队长度 m ∈ N** 成立（即"scalable"）；作者称该定义对**线性与非线性、同质与异质**车队均适用。作者进一步证明：对**线性单向耦合**系统，该定义可退化为文献中常用的性能型判据（$\sup_\omega|\Gamma_i(j\omega)|\le 1$，即 H∞ 范数条件），并给出对应的两个定理（Theorem 1 对 L2、Theorem 2 对 L∞）；其中 L2 情形在标量输入输出、Γ 与车辆序号 i 无关时，条件**既充分又必要**。在车辆编队的具体算例中，作者用固定时距间距策略 + 前车期望加速度前馈（CACC）推导出 Γ(s) 的解析式，论证：**无通信时延时，系统对任意控制器增益与时距都严格 L2 弦稳定**；**有通信时延时弦稳定性被破坏**，并给出最大可容许时延 $\theta_{max}$ 随时距 h 的曲线；L∞ 判据比 L2 判据更严格。最后，作者用**六辆乘用车的实车车队**（IEEE 802.11p，10 Hz 更新率）做实验验证：在 τ = 0.1 s、φ = 0.2 s、kp = 0.2、kd = 0.7、kdd = 0、θ ≈ 0.15 s 下取 h = 0.7 s「just achieving strict L2 string stability」，并测量 |Γ(jω)|（Welch 平均周期图）与起步速度响应，显示 CACC 弦稳定、ACC 不弦稳定。

---

## 二、主张—证据台账

> 内部等级口径（`deep-paper-reader` §3.1.1）：A_int ＝预注册+对照/识别+足够功效+效应量与 CI+**内部**独立重复；B_int ＝设计良好但有边界；C_int ＝仿真/相关/单例；D_int ＝假设。
> **硬规则**：无 CI、无重复运行者**最高 B_int**；证据为仿真/单例者最高 C_int。外部复现列一律「未检」（本笔记未做任何外部检索，**不等于**"无外部证据"）。

| # | 作者主张（英文原句） | 支撑证据（定理/引理编号、图号、仿真设置） | 内部等级(A_int–D_int) | 外部复现 | 是否被结果支撑 | 缺口 |
|---|---|---|---|---|---|---|
| 1 | "a novel definition for string stability of nonlinear cascaded systems is proposed, using input–output properties." | **Definition 1 (Lp string stability)**（§IV-A）：存在 class K 函数 α、β 使 $\|y_i(t)-h(\bar x_0)\|_{L_p}\le\alpha(\|u_r(t)\|_{L_p})+\beta(\|x(0)-\bar x\|)$，$\forall i\in S_m,\forall m\in\mathbb N$；strict 版另加 $\|y_i(t)-h(\bar x_0)\|_{L_p}\le\|y_{i-1}(t)-h(\bar x_0)\|_{L_p}$。仅数学构造，无实验 | **A_int**（定义是约定，不是经验主张；无统计推断成分，故不受"无重复"降级约束） | 未检 | 是（定义自洽，Footnote 1 给出 class K 定义） | 定义本身**可判定**但**不可复现为数值**；未给出 α、β 的具体形式（除线性情形的 (17)/(25)）；未讨论 $u_r\notin L_p$ 时的行为 |
| 2 | "This definition is shown to result in well-known string stability conditions for linear cascaded systems." | **Theorem 1**（§IV-B）+ (16)–(22)：线性单向耦合下 L2 弦稳定 ← (1) $\|P_1(j\omega)\|_{H_\infty}$ 存在；(2) $\|\Gamma_i(j\omega)\|_{H_\infty}\le 1,\forall i\in\mathbb N\backslash\{1\}$；"the system is strictly L2 string stable **if and only if** conditions 1 and 2 hold"（证明用 (20) 分解 + H∞ 范数次可乘性 (21)） | **A_int**（定理级，证明完整给出） | 未检 | 是（证明逐步可查） | 对**非 strict** L2 弦稳定只给**充分**条件（"only yields sufficient conditions … basically due to the submultiplicative property"）；未给非 strict 情形的必要条件 |
| 3 | "Note that this necessity of these conditions only holds in the absence of poles of P1(s) on the imaginary axis…" | **Remark 4**（§IV-B）：标量输入输出、Γ 与 i 无关时 $\|P_i(j\omega)\|_{H_\infty}=\sup_\omega\{|\Gamma(j\omega)|^{i-1}|P_1(j\omega)|\}$（23），故"L2 string stability and strict L2 string stability are equivalent" | **A_int**（定理+注记级） | 未检 | 是 | (23) 带一长串前述前提（标量、Γ 与 i 无关、P1 在虚轴上无被 Γ 零点抵消的极点）；**引用必要条件时必须连前提一起引**，否则会把"必要"过度推广 |
| 4 | "Obviously, the induced L∞ norm can be used instead. In the scope of vehicle following, the motivation for using this norm would be trafﬁc safety, since the L∞ norm is directly related to maximum overshoot." | **Theorem 2**（§IV-B）+ (24)–(25)：L∞ 弦稳定 ← (1) $\|p_1(t)\|_{L_1}$ 存在；(2) $\|\gamma_i(t)\|_{L_1}\le 1$；证明用"Young's inequality for convolutions" | **A_int**（定理级） | 未检 | 是 | 同样只给**充分**条件（"Again, Theorem 2 only provides sufﬁcient conditions for L∞ string stability"）；L∞ 判据**未被实验验证**（见 #13） |
| 5 | "It follows from (30) that without delay (D(s) = 1), $\|\Gamma(j\omega)\|_{H_\infty}$ exists, since $\|\Gamma(j\omega)\|_{H_\infty}=\sup_\omega|H^{-1}(j\omega)|=1$. According to Theorem 1, the system without delay is thus strictly L2 string stable for any choice of controller gains and time headway." | (30) + (31) + 无时延代入 D(s)=1；"provided that h ≥ 0" 的稳定性前提在 (31) 之后的句子中 | **B_int**（推导正确，但覆盖范围有前提） | 未检 | 部分是 | **口径过宽**：该句未带"闭环渐近稳定"前提。§III 结尾的 Routh–Hurwitz 条件为 $h>0$、$k_p,k_d>0$、$k_{dd}>-1$、$(1+k_{dd})k_d>k_p\tau$——超出该集合时"any choice of controller gains"不成立；且 h = 0 的边界情形与"h ≥ 0"表述冲突 |
| 6 | "As a consequence, however, string stability robustness with respect to, e.g., model uncertainties, may be poor in case these uncertainties cause $\|\Gamma(j\omega)\|$ to increase in the lower frequency region." | (32) $\lim_{\omega\to0}|\Gamma(j\omega)|=1\Rightarrow\|\Gamma(j\omega)\|_{H_\infty}\ge1$ + 文字论证 | **D_int**（仅为定性推测，无任何不确定性建模、无 μ/结构化奇异值、无鲁棒裕度数值） | 未检 | 未被检验 | 真空缺：整个"robust string stability"主题在本 brief 中被明确推给未来工作（"will be the subject of further research"）；**P1 若想引用"鲁棒弦稳定"，本文给不了** |
| 7 | "This time delay compromises string stability [32], as illustrated in Fig. 3(a), showing the gain $\|\Gamma(j\omega)\|$ for various values of the time delay $\theta$." | **Fig. 3(a)**：τ = 0.1 s, kp = 0.2, kd = 0.7, kdd = 0, h = 0.5 s；θ = 0（实黑）/0.15（虚黑）/0.3 s（灰）三条 | **C_int**（**数值计算/仿真级**：由线性模型解析求 |Γ(jω)|，非实验；无重复运行概念，无不确定度） | 未检 | 是 | 无实验支撑（该组参数 h = 0.5 s 与实验用的 h = 0.7 s 不同）；曲线读数不可引用（只能定性） |
| 8 | "Fig. 3(b) illustrates the inﬂuence of the time headway on string stability in the presence of a communication delay, showing the maximum communication delay θmax that yields $\|\Gamma(j\omega)\|_{H_\infty}\le 1$, as a function of time headway h." | **Fig. 3(b)** + 算法说明："This result is calculated by taking a ﬁxed value for θ and then searching for the smallest value of h such that $\|\Gamma(j\omega)\|_{H_\infty}=1$." | **C_int**（数值计算级；正文**未印出任何 θmax 数值**） | 未检 | 是（定性趋势可见） | 无法核验数值：图 3(b) 的 θmax(h) **无任何印出的数字**，只能目测读数 → P1 **不得引用具体 θmax 值**；扫描步长、θ 取值集合未报告 |
| 9 | "It appears that $\|\gamma(t)\|_{L_1}$ is an increasing function of θ, the effect of which is illustrated in Fig. 4(b)… Apparently, $\|\gamma(t)\|_{L_1}\le1$ is a more stringent criterion than $\|\Gamma(j\omega)\|_{H_\infty}\le1$, requiring a signiﬁcantly larger time headway. This could be expected since, from linear system theory, $\|\Gamma(j\omega)\|_{H_\infty}\le\|\gamma(t)\|_{L_1}$." | **Fig. 4(a)(b)** + 不等式 $\|\Gamma(j\omega)\|_{H_\infty}\le\|\gamma(t)\|_{L_1}$ | **C_int**（数值计算级，无实验） | 未检 | 是 | γ(t) 由 (30) 的 Γ(jω) 反 Fourier 变换算得（"calculated using the inverse Fourier transform"）；同样**无印出数值**；未给数值精度/截断说明 |
| 10 | "The test vehicle model has been identiﬁed as [27]: $G(s)=\frac{1}{s^2(\tau s+1)}e^{-\phi s}$ with τ = 0.1 s and φ = 0.2 s." | (33) + §VI；系统辨识结果转引自 [27]（Ploeg et al., ITSC 2011），本文**未给辨识实验细节** | **C_int**（单次系统辨识的报告值，本文层面无重复、无拟合优度、无 CI） | 未检 | 是（与实验装置一致） | 辨识数据、拟合误差、车辆类型/载荷/轮胎状态全部未给；**该 G(s) 只对这套六车试验平台成立**，不得搬用到 P1 的车辆模型 |
| 11 | "Considering stability of the dynamics (7), speed of response, and comfort, suitable controller gains were found to be kp = 0.2 and kd = 0.7, with kdd = 0 to avoid feedback of the jerk, which is in practice unfeasible." | §VI 正文；与 Fig. 3/4 所用参数一致（kp = 0.2, kd = 0.7, kdd = 0, τ = 0.1 s） | **C_int**（手工整定，无搜索空间、无目标函数、无交叉验证） | 未检 | 是（与实验一致） | 未给整定流程（"Considering stability…, speed…, comfort"无量化准则）；kdd = 0 是**实践约束**而非由弦稳定性判据导出，引用时须说明 |
| 12 | "Using the analysis presented in Section V, h = 0.7 s is chosen, just achieving strict L2 string stability." | §VI，由 §V 的 $\|\Gamma(j\omega)\|_{H_\infty}\le1$ 判据反解 h；θ ≈ 0.15 s | **C_int**（模型计算结果；**"just achieving"意味着零裕度**） | 未检 | 是 | "just achieving" ＝边际满足，未报告裕度（多少 dB）；无不确定度；P1 若引用该 h 值须注意它是**该平台 + 该判据的边界值**，不是普适设计值 |
| 13 | "The beneﬁt of CACC in view of L2 string stability is clearly illustrated, validating the theoretical analysis in Section IV." | **Fig. 5**：Γ(jω) 幅值，CACC measured / CACC theoretical / ACC measured / ACC theoretical；测量用"Welch's averaged periodogram method [33]"；激励为 prescribed acceleration profile a0(t)（引自 [27]），ur(t) 经 (9) 的动态逆微分算出 | **C_int**（**实车实验，但单次运行**，无重复、无 CI、无方差；估计器参数未报告） | 未检 | 部分是 | ①严格说这只验证了**相邻两车的 |Γ|**，而 Theorem 1 的两条条件中"$\|P_1\|_{H_\infty}$ 存在"未被单独核验；②作者自承"estimation inaccuracy may compromise the second string stability criterion from Theorem 1"→ 在 |Γ| ≈ 1 的低频段，**判据是否真被满足，实验精度不足以判定**；③**单次运行**，无重复，无法排除随机性 |
| 14 | "Therefore, L∞ string stability is not further investigated here." | §VI：因估计误差使脉冲响应函数（由反 Fourier 变换算得）不准确，故不进一步考察 L∞ | **C_int**（=实验**未覆盖**L∞ 判据） | 未检 | **不适用**（作者主动放弃） | **Theorem 2 全文无任何实验验证**。P1 若要用 L∞ 判据（对"最大超调/安全性"更贴切，见 #4），必须知道：本文只给了它的**定理**，没给实验证据 |
| 15 | "Noteworthy is the observation that with ACC, the last vehicle starts to accelerate after 15.5 s, whereas with CACC, this is already after 8.5 s, showing that CACC may also be effective at trafﬁc lights." | **Fig. 6**：(a) ACC、(b) CACC 的实测速度响应（black–light grey: vehicle 1–6），激励为前车的 constant acceleration | **C_int**（实车、单次运行、无重复/CI；15.5 s 与 8.5 s 为**图上读取的"起步时刻"**，正文印出但**读取判据未定义**） | 未检 | 是（趋势与图一致） | "starts to accelerate"无量化阈值（如达到 0.1 m/s 或 5% 目标速度）；未报告 6 辆车各自的完整轨迹；该数字是**实验平台特定值**，P1 引用须带限定语 |
| 16 | "Next, the string stability properties of CACC for vehicle platoons were analyzed, showing that time gaps well below 1 s were admissible." | §VI（h = 0.7 s 实车验证）+ Fig. 3 | **C_int**（结论层：0.7 s 有实验、"well below 1 s"含模型外推成分） | 未检 | 是（0.7 s 由实验支持） | "well below 1 s"的边界由模型给出而非实验；实验只做了 h = 0.7 s **一个**时距 |
| 17 | "…which also indicated that time gaps down to 0.3 s are feasible when minimizing the latency of the wireless link." | **Fig. 3(b)**（模型计算 θmax(h) 曲线）| **C_int**（**纯模型结论，无实验**） | 未检 | 是（作为模型预测） | **P1 的红线提醒**：0.3 s 是**线性模型 + 零不确定度**下的计算值，**未做实验**；若引用必须写"文献报告值（模型预测，非实验），协议不同，不可直接比较" |
| 18 | "Such small time headways, however, will require insight into the string stability margins in the presence of uncertainties or unknown disturbances, which will be the subject of further research." | §VII（结论自承边界） | **A_int**（作者自述的边界声明，非经验主张） | 未检 | 是 | 作者**自己**把"不确定性下的弦稳定裕度"列为未解决问题 → 本文**不能**用来支撑任何"鲁棒弦稳定"断言（与 #6 一致） |
| 19 | "Deﬁnition 1 encompasses those [existing deﬁnitions]" / "the performance-oriented approach … is captured by Deﬁnition 1 as a special case for linear, unidirectionally interconnected systems" | §IV-C Discussion：与 [7]–[10]（Lyapunov 型）、[11]–[16]（无限长/空间频率型）、[17]–[25]（性能型）的关系逐类论证；并承认输出选择上的差异（"the Lyapunov-stability approach focusses on the system states, whereas Deﬁnition 1 regards the outputs"，补救办法是"choosing the output so as to include all states, albeit that the string stability complementary sensitivity can no longer be computed using (19)"） | **B_int**（论述型主张，有逐条对照理由，但无形式化证明"encompasses"） | 未检 | 部分 | "encompasses"是**包含性断言**，本文未给形式化的等价/包含证明；且作者自认：把全部状态纳入输出后 **(19) 不再可用**→ 那时 Theorem 1 的判据失效。P1 引用"该定义覆盖既有定义"时须带此限制 |

**台账小结（供下游直接取用）**：19 条中，**A_int 5 条**（#1–#4、#18：定义与两个定理、以及作者自承边界），**B_int 2 条**（#5、#19），**C_int 11 条**（#7–#17，即全部数值/实验/整定类主张），**D_int 1 条**（#6 鲁棒性推测）。**没有任何一条达到 A_int 的经验级**——这是理论 brief 的正常形态，不是缺陷；但意味着 **P1 引用本文的数值（h = 0.7 s、0.3 s、15.5/8.5 s）时，证据等级按 C_int 处理**。

---

## 三、方法可复现性清单

> 说明：本文是**理论 + 实车验证**型 brief。九项中数项按理论文章性质写 N/A 或"未给出"，每项均给缺失影响。

| 项 | 论文是否给出 | 具体位置 | 缺失影响 |
|---|---|---|---|
| 数据来源与版本 | **N/A（理论文章）**。本文的"数据"是**解析推导的传递函数 + 一次实车实验的测量信号**，不存在数据集与版本概念。实验数据未公开、未附 | §IV–§V（解析）、§VI（实验） | 无原始数据 → 无法复算 |Γ(jω)|、无法验 Welch 估计的偏差与方差；只能做自洽性检查（本笔记已做，见 §五） |
| 预处理与划分方式 | **部分给出**：|Γ(jω)| 用 "Welch's averaged periodogram method [33]" 估计；γ(t) 与 impulse response 用 inverse Fourier transform 算得。**无训练/测试划分概念（N/A）** | §VI | **窗长、段数、重叠率、采样率（除 10 Hz 通信更新率外）、频率分辨率、抗混叠处理全部未给** → 无法复现 |Γ| 的谱估计误差，也就无法判断 |Γ| 与 1 的差距是否只是噪声 |
| 模型/实验装置规格 | **给出到可算的程度**：车辆模型 (4)/(26)/(33)（τ = 0.1 s、φ = 0.2 s）；控制器 (5)–(6)（kp = 0.2、kd = 0.7、kdd = 0）；通信 D(s) = e^{−θs}（θ ≈ 0.15 s）；IEEE 802.11p、10 Hz；虚拟参考车模型 (9) | §III、§V、§VI、Fig. 2 | **车辆品牌/型号、质量、是否同一车型、执行器（油门/制动）接口、传感器（radar/lidar 型号）、路面与试验场地均未给** → P1 无法把该平台参数迁移到 CARLA；也无法评估 φ = 0.2 s 是否具有代表性 |
| 超参数与搜索空间 | **给出取值，未给搜索空间**：kp = 0.2、kd = 0.7、kdd = 0（"to avoid feedback of the jerk, which is in practice unfeasible"）、h = 0.7 s（"just achieving strict L2 string stability"）、τ = 0.1 s、τ = 0.1 s（Fig. 3/4 同）、h = 0.5 s（Fig. 3/4 用） | §VI、Fig. 3/4 正文 | 未给整定准则的量化形式（stability/speed/comfort 三者的权衡未参数化）→ **P1 无法复现"如何选到 h"这一步**，也就无法判断该 h 是否为该平台的最优或保守值 |
| 随机种子 / 重复次数 | **均未给出**；实际为**单次运行** | §VI 通篇无重复次数、无 seed（实车实验无 seed 概念，但**应有重复试验**） | **无法给出方差或 CI** → 无法判断 |Γ| 曲线与 15.5 s / 8.5 s 差异是否超出运行间波动；**P1 不得把这两个数字当作稳定可比的定量结论** |
| 评价指标定义（含边界情况） | **给出**：Lp 弦稳定（Definition 1，(1)）；Γ(s) 定义 (19)(30)；$\|p_i(t)\|_{L_1}$ 与输入输出 L∞ 增益关系 (24) | §IV-A、§IV-B、§V | 边界情况未讨论：$u_r\notin L_p$ 时、$x(0)$ 使 $\|x(0)-\bar x\|$ 不存在时（作者只承认"only initial condition perturbations are considered for which the norm … exists"）；**未给"实测 |Γ| 在低频贴近 1 时如何判定通过/不通过"的操作性规则** |
| 基线实现来源 | **给出**：ACC 基线 = 同一控制器但令 $u_{i-1}=0$（"with the communicated desired acceleration $u_{i-1}$ of the preceding vehicle and without (i.e., $u_{i-1}=0$), referred to as CACC and ACC"）；理论曲线由 (30) 直接画出 | §VI、Fig. 5 | 这是**消融**（去掉前馈），不是外部 SOTA 基线；无其他基线（如仅雷达 ACC、变时距策略）→ 无法回答"该 CACC 相对其他弦稳定设计好多少" |
| 显著性检验方法 | **N/A（理论文章）**；实验部分**未做任何统计检验** | §VI | 结论是**定理级**（数学证明）与**定性图示级**（Fig. 5/6），不存在统计推断；**P1 引用其"验证了理论"时不得读成"统计显著"** |
| 代码/数据可用性声明 | **未给出**（全文无 code/data availability 声明；TU/e pure 页只给版权与再利用条款 "You may download and print one copy … for private study or research"） | 页 1 版权页 | P1 **不能假设可得其仿真/实验代码**；若 P1 要复现 Fig. 3(b) 的 θmax(h)，须依据 (30) 自行实现（本文已给足公式，**这一步是可做的**，见 §七） |

---

## 四、关键数字表

> 本文**原文无表格**（已核实）。以下数字全部来自**正文文字与图注**，出处列写明节号/式号/图号。
> 单位、样本量（车辆数）、设置三件事随数字同行。**"未报告"即为原文未印出**，不得补猜。

| 指标 | 值 | 不确定度 | 出处（节/式/图） | 备注（哪套设置） |
|---|---|---|---|---|
| 车队规模（实验） | **6** 辆乘用车 | 未报告 | Abstract；§VI "a platoon of six passenger vehicles" | 实车实验；另有一个虚拟参考车 i = 0（模型，非实物） |
| 车队规模（理论/数值） | **m 任意**（定义要求 $\forall m\in\mathbb N$）；数值分析取 $m\to\infty$（Remark 3） | N/A | §IV-A Def. 1；Remark 3 | 单向 look-ahead 拓扑下无限长包含所有有限长 |
| 间距策略 | $d_{r,i}(t)=r_i+h\,v_i(t)$（**时距型 + 固定停车间距**，constant time headway + standstill distance） | N/A | (2)，§III | 同质车队（h 对所有 i 相同） |
| 时距 h（实验值） | **0.7 s**（"just achieving strict L2 string stability"） | 未报告（作者称"just"，故裕度≈0 但未量化） | §VI | 实车六车；配 θ ≈ 0.15 s |
| 时距 h（Fig. 3/4 数值分析值） | **0.5 s** | 未报告 | §V "τ = 0.1 s, kp = 0.2, kd = 0.7, kdd = 0, and h = 0.5 s" | 与实验值 0.7 s **不同口径**，引用时必须区分（见 §四末口径表） |
| 停车间距 r_i | 符号给出，**数值未报告** | — | (2)(3)(29) | 误差定义 $e_i=d_i-(r_i+hv_i)$ 依赖它；实验中的取值未印出 |
| 车辆长度 L_i | 符号给出，**数值未报告** | — | (3)(29) | 同上 |
| 驱动系时间常数 τ | **0.1 s** | 未报告 | §V（Fig. 3/4 参数）；§VI（式 (33)） | 同质假设：所有车相同 |
| 执行器/驱动系附加时延 φ | **0.2 s** | 未报告 | §VI，(33) $G(s)=\frac{1}{s^2(\tau s+1)}e^{-\phi s}$ | **仅实验模型含此 φ**；理论分析 (26) 不含 φ |
| 通信时延 θ（实验） | **≈ 0.15 s** | 未报告（"appeared to be"） | §VI | IEEE 802.11p，10 Hz 更新率 |
| 通信时延 θ（数值分析取值） | 0 s / 0.15 s / 0.3 s（三档） | N/A | Fig. 3(a)、Fig. 4(a) 图注 | 用于展示弦稳定性随 θ 退化 |
| 控制器增益 kp | **0.2** | 未报告 | §V、§VI、Fig. 3/4 图注 | 理论与实验同值 |
| 控制器增益 kd | **0.7** | 未报告 | 同上 | 同上 |
| 控制器增益 kdd | **0**（"to avoid feedback of the jerk, which is in practice unfeasible"） | N/A | §VI | 同理沦分析取值 |
| 通信更新率 | **10 Hz** | 未报告 | §VI | IEEE 802.11p |
| 最大通信时延 θmax(h) | **图 3(b) / 图 4(b) 曲线，正文未印任何数值** | 未报告 | Fig. 3(b)、Fig. 4(b) | **不可引用具体数值**；若要数值须自行按 (30) 重算 |
| 可行时距下限（模型结论） | **0.3 s** | 未报告 | §VII "time gaps down to 0.3 s are feasible when minimizing the latency of the wireless link" | **模型预测，无实验**；P1 引用须写"文献报告值（模型预测，非实验），协议不同，不可直接比较" |
| 末端车起步时刻（ACC） | **15.5 s** | 未报告（单次运行） | §VI、Fig. 6(a) | 6 车，前车 constant acceleration 起步工况 |
| 末端车起步时刻（CACC） | **8.5 s** | 未报告（单次运行） | §VI、Fig. 6(b) | 同上；差值 7.0 s（本文未计算此差值，**为本笔记的算术差，非原文数字**） |
| 加速度响应时间窗（Fig. 3/4(a) 横轴） | 0–2 s | N/A | Fig. 3(a)? 见口径歧义 | 图 3(a) 的横轴实为 ω [rad/s] 0.1–10；0–2 s 是 Fig. 4(a) 的 t 轴（**提取文本中两图的轴标签交错，已核实 Fig. 3(a) 为频域、Fig. 4(a) 为时域**） |
| 弦稳定性判据阈值 | $\|\Gamma(j\omega)\|_{H_\infty}\le1$（即 0 dB）；$\|\gamma(t)\|_{L_1}\le1$ | N/A | (1)、Theorem 1 cond. 2、Theorem 2 cond. 2 | 无裕度要求（strict 版含等号，见 (32) 的讨论） |

**§3.7 数字口径对照表（本文同一指标出现多个数值时强制填写）**

| 指标 | 数值 | 数据集/工况 | 是否集成 | 是否重复运行 | 其他设置 | 出处 |
|---|---|---|---|---|---|---|
| 时距 h | 0.5 s | 数值分析（线性模型） | N/A | 单次计算 | θ ∈ {0, 0.15, 0.3} s，τ=0.1, kp=0.2, kd=0.7, kdd=0 | §V / Fig. 3, Fig. 4 |
| 时距 h | 0.7 s | **实车实验（6 车）** | N/A | **单次** | θ ≈ 0.15 s，φ = 0.2 s，τ=0.1, kp=0.2, kd=0.7, kdd=0 | §VI / Fig. 5, Fig. 6 |
| 时距 h | 0.3 s（下限） | 数值分析外推 | N/A | 单次计算 | "minimizing the latency of the wireless link"（具体 θ 未给） | §VII（无对应图号） |
| 控制器增益 (kp, kd, kdd) | (0.2, 0.7, 0) | 数值分析 **与** 实车实验**同一组** | N/A | — | 两处一致，**无第二组增益** | §V / §VI / Fig. 3–6 |
| 触发激励 | prescribed acceleration profile a0(t)（**参数转引 [27]，本文未给数值**） | 实车实验 | N/A | 单次 | 前车加速度曲线，ur(t) 由 (9) 动态逆微分算得 | §VI |
| 触发激励 | constant acceleration of the lead vehicle | 实车实验（起步工况） | N/A | 单次 | 幅值未报告 | §VI / Fig. 6 |

---

## 五、统计与推断旗标

**总旗标：本文的结论是「定理级（theorem-level）」，不是「统计级（statistical）」——两者不可互换。**

1. **结论的性质**：核心结论（Definition 1、Theorem 1、Theorem 2、Remark 4）是**数学命题与其证明**（§IV-B 中 Theorem 1 的 proof 完整给出；Theorem 2 的证明"similar to that of Theorem 1"，用 Young 不等式）。这些结论的成立**不依赖样本、不依赖随机性、不需要显著性检验**。把"定理成立"读成"在数据上显著"是范畴错误。
2. **仿真/实验部分只有单次运行**：§VI 报告一次实车试验（一次 prescribed a0(t) 激励 + 一次 constant-acceleration 起步）。**全文未出现重复次数、未出现方差/SD/SE/CI、未出现任何显著性检验、未出现 any seed（实车无 seed 概念，但应有重复试验）**。因此 Fig. 5 的 |Γ| 曲线与 Fig. 6 的 15.5 s / 8.5 s 都**没有不确定度**。
3. **"验证"的强度**：作者的措辞是"validating the theoretical analysis in Section IV"（Fig. 5）与"in accordance with the theoretical analysis"（§VII）。这是**定性一致性论证**，不是假设检验。P1 引用时**不得**升级为"实验证明弦稳定判据成立"。
4. **作者自承的推断弱点（须原样保留）**："string stability may not always be easy to assess in practice, since $|\Gamma(j\omega)|$ will be close to 1 for low frequencies, see (32), as a result of which **estimation inaccuracy may compromise the second string stability criterion from Theorem 1**." → 在判据阈值附近（0 dB），**谱估计误差与判据裕度同量级**；作者据此**放弃**了 L∞ 的实验考察。这是本文对自身证据边界最诚实的一段，P1 应引用它来论证"实测弦稳定性需要报告估计不确定度"。
5. **多重比较**：N/A（无统计检验，不存在多重比较问题）。
6. **等价/非劣检验**：N/A。本文没有把"p > 0.05"当作"无差异"的推断错误（因为根本没用检验）。P1 若想把"CACC 与 ACC 无差异"写成结论，须自行做等价检验——**本文帮不上**。
7. **不确定性是否被处理**：仅在 #6 的定性推测中被提及，且作者在 §VII 明确把它列为 future research。**没有任何不确定度量化**。
8. **数值自洽性检查（本笔记所做）**：由 (10) 的 $A_r$ 与 (12) 的块结构，可算得 $A_r$ 的特征多项式为 $\tau h s^4+(\tau+h)s^3+s^2+k_d s+k_p$，其 Routh–Hurwitz 条件恰为 §III 结尾列出的 $h>0$、$k_p,k_d>0$、$k_{dd}>-1$、$(1+k_{dd})k_d>k_p\tau$——**与原文一致，未见矛盾**。（另：由 (9) 第三行 $\dot a_0=-\frac1\tau a_0+\frac1\tau u_0$ 与第四行 $h\dot u_0=-u_0+\xi_0$ 可复核 $P_1(s)$ 的低频性质与 (32) 的 $\lim_{\omega\to0}|\Gamma(j\omega)|=1$，亦一致。此项为自洽性检查，**不是**对原文的复算证明。）

---

## 六、缺失信息清单

分类给出，每条写成可执行动作。

**A. 未报告（影响 + 最小补法）**

1. **未报告：实车实验的重复次数与运行间离散度。** 影响：无法判断 Fig. 5 的 |Γ| 曲线与 Fig. 6 的 15.5 s / 8.5 s 是否超出运行间波动；无法给出任何 CI，台账中所有实验类主张的上限被锁死在 C_int。最小补法：向作者索取同一 h、同一 a0(t) 的 **≥5 次重复试验**数据，或索取 |Γ(jω)| 的逐次估计曲线。（可执行：邮件请求 + 在 P1 中改为自建 benchmark 复现）
2. **未报告：Welch 平均周期图的参数（窗长、段数、重叠、频率分辨率）与测量的 SNR。** 影响：恰在判据阈值 |Γ| ≈ 1 附近，这些参数直接决定"是否满足 $\|\Gamma\|_{H_\infty}\le1$"的结论；作者本人承认估计不准可能破坏该判据。最小补法：索取谱估计脚本或原始时域记录，按同一参数重估并**报告 |Γ| 的置信带**。
3. **未报告：Fig. 3(b)/4(b) 的 θmax(h) 数值与扫描步长。** 影响：§VII 的"0.3 s"和"well below 1 s"**无法核到任何印出的数字**，只能目测读图 → 该结论在 P1 中不可作为定量引用。最小补法：按 (30) 自行实现 Γ(jω) 并在给定 θ 下二分搜索最小 h（**这一步本文公式足够，可自行复现**，见 §七）。
4. **未报告：间距策略中的 $r_i$（standstill distance）与 $L_i$（车长）数值。** 影响：误差 $e_i=d_i-(r_i+hv_i)$ 的绝对水平无法还原；P1 无法把"跟车误差 RMSE"与本文的 $e_i$ 做数值对齐。最小补法：索取车辆参数表，或在 P1 中**自行定义并报告** $r_i, L_i$。
5. **未报告：车辆平台规格（车型、质量、执行器接口、传感器型号、试验场地与路面条件）。** 影响：φ = 0.2 s、θ ≈ 0.15 s 的外推性未知；P1 无法判断这些参数是否代表高速公路主线工况。最小补法：索取试验报告或引用 [27] 的完整版本核对。
6. **未报告：初值条件。** 影响：Definition 1 明确含 $x(0)$ 扰动项（class K 函数 β），但 §VI 未说明实验是否从平衡态出发、编队初始化误差是多少。最小补法：索取实验初始时刻的 $e_i, v_i, a_i, u_i$ 记录。

**B. 报告但不可核验**

7. **报告但不可核验：$G(s)$ 的辨识结果（τ = 0.1 s、φ = 0.2 s）转引自 [27]，本文无辨识实验细节。** 需要什么才能核验：Ploeg et al., ITSC 2011 的辨识章节 + 原始频率响应数据。
8. **报告但不可核验：激励 $a_0(t)$ 的具体形状（"as described in [27]"）。** 需要什么才能核验：[27] 原文（本文未复制该曲线，也未给幅值/带宽/时长）。

**C. 报告口径有歧义（两种解释导致结论如何不同）**

9. **口径歧义："for any choice of controller gains and time headway"（§V，无时延时严格 L2 弦稳定的那句话）。** 解释一（宽）：只要 $h\ge0$ 就成立 → 可推出"弦稳定性对增益不敏感"。解释二（窄，本笔记认为正确）：该句只在 §III 的 Routh–Hurwitz 集合内（$h>0$、$k_p,k_d>0$、$k_{dd}>-1$、$(1+k_{dd})k_d>k_p\tau$）有意义，因为超出该集合时**闭环本身不是渐近稳定的车辆跟随系统**，"string stability"无从谈起。**两种解释对 P1 的后果完全不同**：宽解释会诱使 P1 写"弦稳定性不依赖控制器"，而这在 P1 的非线性控制器上不成立。→ 引用时必须带上车辆跟随的稳定性前提。
10. **口径歧义："h = 0.7 s … just achieving strict L2 string stability"。** "just" 是指（a）恰好满足 $\|\Gamma\|_{H_\infty}=1$（零裕度），还是（b）在可选时距里最小可行值？按 §V 的算法（"searching for the smallest value of h such that $\|\Gamma(j\omega)\|_{H_\infty}=1$"）应为 (a)。两种读法对 P1 的影响：若为 (a)，则**任何模型/估计误差都可能使实测系统越过边界**——这正是 #4 旗标所指；若为 (b)，则可声称该 h 对参数不敏感（本文不支持此读法）。
11. **口径歧义：Fig. 3(b) 与 Fig. 4(b) 图注完全相同（"maximum delay θmax as a function of headway h"），但一个对应 $\|\Gamma(j\omega)\|_{H_\infty}\le1$、另一个对应 $\|\gamma(t)\|_{L_1}\le1$。** 提取文本中两图注逐字相同 → 若从 PDF 目测读数，**极易把 L∞ 的 θmax 误当成 L2 的 θmax**。两种读法给出的结论不同（作者称 L∞ 判据"requiring a signiﬁcantly larger time headway"；由 Fig. 4(b) 的轴标签 θmax 上限 ≈0.25 s 与 Fig. 3(b) 的 ≈1.5 s 相比，约差 2.5 倍 [估读：轴标签值，非数据点]）。→ P1 若要引用 θmax，必须回到 PDF 逐图像核对轴与曲线归属。

**D. 该文有、但 P1 需要而本文未提供的**

12. **本文未提供：非线性控制器的弦稳定判据。** Definition 1 适用于非线性系统，但**可操作的判据（Theorem 1/2）只对线性单向耦合系统成立**，且核心工具（传递函数 $P_i(s)$、$\Gamma_i(s)$、H∞ 范数、次可乘性）本质上是 LTI 的。→ P1 的 CfC 是**非线性学习控制器**，**不能直接套用** Theorem 1；缺的是"如何为 CfC 闭环建立 Lp 增益"这一环（详见 §十.①）。
13. **本文未提供：多前车/双向拓扑下的判据。** Remark 1 只说定义"could be further generalized … so as to include multiple-vehicle look-ahead or bidirectional interconnections"，**未展开**。→ 若 P1 的 OTF 势场用到邻车（多车）信息，Theorem 1 的 look-ahead 单向假设不成立，需要另行论证（Remark 3 的"无限长包含有限长"论证也只在单向时成立）。

---

## 七、复用价值判断

| 问题 | 结论 |
|---|---|
| 方法可否搬到我的问题？需要改什么？ | **可以搬的是"判据的形式"与"验证的协议"，不能搬的是"判据的直接套用"。** 可搬：① Lp 弦稳定的定义与 strict 版不等式（定义层，不依赖 LTI）；② L2 情形的判据结构"$\|\Gamma_i(j\omega)\|_{H_\infty}\le1$ 且 $P_1$ 的 H∞ 范数存在"；③ 验证协议——用**相邻车输出的频响比**（而非仅末端误差）来实证弦稳定性，并用 Welch 类谱估计；④ 用 $L_\infty$ 判据对应"最大超调"这一动机（对 P1 的 Jerk 峰值 / 加速度峰值指标更贴切）。必须改：CfC 非线性 → 需局部线性化或 Lp 增益分析（见 §十.①）；P1 的 OTF 势场可能引入多车耦合 → Remark 1 的拓扑推广未在本文完成 |
| 评价协议可否直接对齐（指标、划分、基线）？ | **部分可对齐。** 指标：本文的 $e_i(t)=d_i(t)-(r_i+hv_i(t))$ 与 P1 的"跟车误差 RMSE"是**同一物理量**（间距误差），但**口径不同**（本文是时距型 $r_i+hv_i$，P1 若用固定间距则不可比）。基线：本文的 ACC 是"同控制器令 $u_{i-1}=0$"的**消融**，不是 P1 的 PID/MPC/TD3 基线。划分/种子：本文无此概念。→ **不可说"按 Ploeg 2014 的协议对齐"**，只能说"沿用其弦稳定性判据与频响比验证思路" |
| 数据/代码可否直接取用？许可如何？ | **数据与代码均不可得**（无 availability 声明）。许可：TU/e pure 页明确 "You may download and print one copy … for private study or research"，"You may not further distribute the material or use it for any proﬁt-making activity or commercial gain" → P1 可引用，**不得再分发** PDF。可自行实现的部分：按 (30) 重算 Γ(s)、按 (2)–(6) 重搭线性编队模型 |
| 若要引用其数字，引用时**必须**带上的限定语是什么？ | 见下方单行字段；另附人读版：**「文献报告值：6 辆乘用车 CACC 实车（IEEE 802.11p, 10 Hz），线性时不变控制器、固定时距间距策略、单向 look-ahead、无不确定性建模，单次运行、未报告方差或 CI；其中 0.3 s 时距为模型预测而非实验；协议与 P1 的 CARLA/回放 + 非线性 CfC 不同，不可直接比较。」** |

```
citation_qualifier: 6-vehicle homogeneous platoon (real passenger cars, CACC over IEEE 802.11p at 10 Hz; linear LTI platoon model with driveline time constant tau=0.1 s, actuator delay phi=0.2 s, communication delay theta~0.15 s, controller kp=0.2/kd=0.7/kdd=0, constant-time-headway spacing policy d_r,i=r_i+h*v_i, one-vehicle look-ahead unidirectional topology, no uncertainty modelling) — NOT simulation; Theorem 1/Theorem 2 conditions apply only to linear unidirectionally interconnected systems, and the h=0.7 s / 0.3 s / 15.5 s / 8.5 s figures come from a SINGLE experimental run with no repetitions, no variance and no confidence intervals reported (0.3 s is a model prediction only, never tested).
```

---

## 八、红队三条

1. **领域最懂的人会质疑**："你引的『h = 0.7 s 达到严格 L2 弦稳定』是**单次实车运行 + 一次谱估计**的结论，而且作者自己说低频段 |Γ| 贴近 1、**估计误差可能破坏 Theorem 1 的第二条判据**——你怎么能把它当'已验证的判据'记？" 需要什么证据才能消解：要求作者给出 (i) **≥5 次重复试验**的 |Γ(jω)| 逐次曲线或置信带，(ii) Welch 估计的参数与频率分辨率，(iii) 在低频段 |Γ| 与 0 dB 的**差值分布**（而非一条曲线）。拿不出 → 该条在 P1 中只能作为"判据的定义出处"引用，**不得**作为"该判据已被实验证实"引用。
2. **方法与统计视角会质疑**："Theorem 1 的必要性你只挑了 Remark 4 的那句，但 Remark 4 有四个前提（标量输入输出、Γ 与 i 无关、$P_1$ 在虚轴上无被 Γ 零点抵消的极点、$P_i$ 方阵非奇异）；另外 §V 那句『for any choice of controller gains and time headway』越过了 §III 的 Routh–Hurwitz 集合（$h>0$、$k_p,k_d>0$、$k_{dd}>-1$、$(1+k_{dd})k_d>k_p\tau$）。你把它读成普适结论了。" 需要什么证据才能消解：回到原文逐条抄前提（本笔记已在台账 #3、#5 与 §六.C.9 中给出），并在引用时**把前提与判据捆绑**；对 P1 而言还需额外声明"该必要性结论对非线性 CfC 不适用"。
3. **编辑 / 邻域读者会质疑**："这篇是**理论 brief**：正文无表、实验只有一个 h 值、没有不确定性、没有重复。你写的缺失信息清单如果只是'未报告参数'这类场面话，读者仍然不知道下一步能不能复现。" 需要什么证据才能消解：把每条缺失改成**可执行动作 + 后果**——本笔记 §六 已如此处理（如 A1 索取 ≥5 次重复、A3 按 (30) 自行重算 θmax(h)、D12 为 CfC 建立局部线性化或 Lp 增益论证）；并接受一个硬事实：**本文能提供的最大值是"定义 + 线性判据 + 验证协议"，不能提供"非线性控制器弦稳定的判据"。**

---

## 九、限制

1. **材料限制**：本笔记基于 TU/e 机构库的 **accepted manuscript**（同行评议后的作者版），**非 publisher final version**；页码与图表编号可能与 IEEE Xplore 正式版 786–793 有差异。此外，本文**原文无表格**（已核实），所有参数取自正文与图注——因此 §四 关键数字表的"出处"列全部指向节号/式号/图号而非表号。**未获取**：补充材料（本文无）、[27]（Ploeg et al., ITSC 2011，G(s) 辨识与 a0(t) 激励的原始出处）、[33]（Welch 方法参考书）。
2. **复算限制**：所有数字均抄自论文文本，**未获原始实验数据** → 无法验证 |Γ(jω)| 的谱估计、无法验证 15.5 s / 8.5 s 的读取判据、无法验证 θmax(h) 的扫描精度。本笔记做过的两处**自洽性检查**（A_r 的特征多项式与 Routh–Hurwitz 条件一致；$P_1$ 的低频性质与 (32) 一致）**不构成**对原文的复算证明。图 3(b)/4(b) 的任何读数都**未**被采用（本笔记一律记"未印出数值"）。
3. **视角限制**：本笔记**不评价**该工作的**重要性**与**新颖性**（主编视角，交给 `cross-paper-synthesizer` / `research-gap-hunter`）；不评估其与同类的 Lp/弦稳定文献的相对贡献。**外部复现列一律"未检"**——本笔记未做任何 OpenAlex/Crossref 引用检索，因此**不得**把"未检"读成"无外部证据"（`deep-paper-reader` §3.1.1 硬规则 2）。若需外部复现状态，须另跑 `paper-discovery` / `paper-consensus`。
4. **时效限制**：精读日期 **2026-10-02**。本文发表于 2014 年，属经典文献；本笔记未检查是否有更正（erratum）或撤稿，也未追踪 2014 年之后对 Definition 1 / Theorem 1 的后续修正或反例。缓解：入稿引用前由 `citation-and-related-work` 复核 DOI `10.1109/TCST.2013.2258346` 的状态与正式版页码。
5. **作用域限制**：本笔记的**全部**结论受 `D:\Deepseek Harness\auto-driving\AGENTS.md` 约束。本文的**实车**结果（6 车、h = 0.7 s）**不是** P1 可用的性能基线，也**不能**倒推 P1 的 CfC 编队弦稳定；P1 的 ODD（高速主线、混行）与本文试验条件（封闭试验、同质车队）不同。

---

## 十、对 P1 的三条具体可用结论

### ① 可直接抄用的判据：Lp 弦稳定的判据表达式、符号含义，及其对"线性/时不变"前提的依赖

**（1）定义层（不依赖 LTI，可直接抄用为 P1 的指标定义）**

Definition 1（原文 §IV-A）：对级联系统 (11) $\dot x_0=f_r(x_0,u_r)$，$\dot x_i=f_i(x_i,x_{i-1})$，$y_i=h(x_i)$（$i\in S_m=\{1,\dots,m\}$，$S_m$ 为车队车辆集合，$u_r$ 为外部输入、等价于"虚拟参考车"的输入），设 $\bar x=(\bar x_0^{\mathrm T}\dots\bar x_0^{\mathrm T})^{\mathrm T}$ 为 $u_r=0$ 的常值平衡点：

$$\|y_i(t)-h(\bar x_0)\|_{L_p}\ \le\ \alpha(\|u_r(t)\|_{L_p})+\beta(\|x(0)-\bar x\|),\qquad \forall i\in S_m,\ \forall m\in\mathbb N$$

其中 $\alpha,\beta$ 为 **class K 函数**（连续、严格递增、$\alpha(0)=0$）；$\|\cdot\|_{L_p}$ 为信号 p-范数；$\|\cdot\|$ 为任一向量范数。

**严格（strict）Lp 弦稳定**：在上式之外，当 $x(0)=\bar x$ 时还需

$$\|y_i(t)-h(\bar x_0)\|_{L_p}\ \le\ \|y_{i-1}(t)-h(\bar x_0)\|_{L_p},\qquad \forall i\in S_m\backslash\{1\},\ \forall m\in\mathbb N\backslash\{1\}$$

**判据层（Theorem 1；线性、单向耦合、$\Gamma_i(s)=P_i(s)P_{i-1}^{-1}(s)$ 存在）**——原文条件：

1. $\|P_1(j\omega)\|_{H_\infty}$ **存在**；
2. $\|\Gamma_i(j\omega)\|_{H_\infty}\le1,\ \forall i\in\mathbb N\backslash\{1\}$；其中 $P_i(s)=C_i(sI-A)^{-1}B$，$\Gamma_i(s)=P_i(s)P_{i-1}^{-1}(s)$ 称为 **string stability complementary sensitivity**（弦稳定补灵敏度），且 $\hat y_i(s)=\Gamma_i(s)\hat y_{i-1}(s)$。
   则系统 **L2 弦稳定**；且**严格 L2 弦稳定 ⟺ 条件 1 与 2 同时成立**。

**本文车辆编队的显式形式（P1 可直接抄写并改写）**：取 $y_i=a_i$（加速度）、标量输入输出、$\Gamma$ 与车辆序号无关，则

$$\Gamma(s)=\frac{\hat a_i(s)}{\hat a_{i-1}(s)}=\frac{1}{H(s)}\cdot\frac{K(s)G(s)+D(s)}{1+K(s)G(s)},\qquad H(s)=hs+1,\quad K(s)=k_p+k_ds+k_{dd}s^2,\quad G(s)=\frac{1}{s^2(\tau s+1)}$$

$$\|\Gamma(j\omega)\|_{H_\infty}=\sup_\omega|\Gamma(j\omega)|\le1\ \Longleftrightarrow\ \text{（strict）}L_2\ \text{弦稳定};\qquad \|p_1(t)\|_{L_1}\le1\ \Longleftrightarrow\ \text{（strict）}L_\infty\ \text{弦稳定}$$

其中 $D(s)=e^{-\theta s}$ 为通信时延，$\theta$ 为时延；$h$ 为时距，$\tau$ 为驱动系时间常数，$k_p,k_d,k_{dd}$ 为增益。L∞ 情形的条件 2 为 $\|\gamma_i(t)\|_{L_1}\le1$，$\gamma_i(t)$ 是 $\Gamma_i(s)$ 的脉冲响应。

**（2）对"线性 + 时不变"的依赖——必须写进 P1 的限制段**

- **定义层不依赖 LTI**：Definition 1 明确"obviously applies to both linear and nonlinear systems, and homogeneous as well as heterogeneous strings"，无需传递函数。
- **判据层强依赖 LTI**：Theorem 1 的证明链条是"$P_i(s)$ 分解 (20) → H∞ 范数**次可乘性** (21) → H∞ 范数由 L2 范数**诱导** (16)"。这三步全部只对**线性时不变**系统成立：$P_i(s)$ 的存在要求 LTI；次可乘性 $\|XY\|_{H_\infty}\le\|X\|_{H_\infty}\|Y\|_{H_\infty}$ 是 H∞ 范数作为算子范数的性质，对时变/非线性算子**不成立**；且 Theorem 1 还需 $P_i(s)$ 方阵非奇异、$P_{i-1}^{-1}(s)$ 存在（functional controllability）。原文自身也承认判据的适用范围：Remark 3（单向 look-ahead 拓扑下才有"无限长包含有限长"）、Remark 4（必要性只在标量/同质/无虚轴极点被抵消时成立）。

**（3）为什么不能直接把该判据套到 P1 的 CfC 上**

1. **不存在传递函数**：CfC（closed-form continuous-time 网络）是**非线性、含内部状态**的连续时间控制器；闭环 $\hat a_i(s)/\hat a_{i-1}(s)$ 不是一个 LTI 传递函数 $\Gamma(s)$，因此 $\|\Gamma(j\omega)\|_{H_\infty}$ **没有定义**，条件 2 无法直接计算或测量。
2. **不存在"与车辆序号无关"的 Γ**：Remark 4 的必要性结论要求 $\Gamma_i$ 与 $i$ 无关（同质）。CfC 的响应取决于其内部状态与 OTF 势场输入，**各车的等效响应随位置与邻车状态变化** → 同质性假设失效，只能退回 Theorem 1 的**充分**条件（$\sup_{i\in\mathbb N}\|\Gamma_i\|_{H_\infty}\le1$，需对**所有** i 逐一验证）。
3. **低频 $\lim_{\omega\to0}|\Gamma(j\omega)|=1$ 是结构性的（(32)）**：只要编队收敛到同速平衡（$\lim_{\omega\to0}(\hat v_i-\hat v_{i-1})=0$），就有 $\|\Gamma\|_{H_\infty}\ge1$ —— 也就是说判据的等号是**必然取到**的，裕度为 0。对线性系统这是"已知的边界"；对非线性 CfC，这意味着**任何**局部线性化的低频段都必须贴边，判别"是否弦稳定"完全取决于高频段与转捩区，而那里恰是 CfC 非线性最强的区段。若 P1 要做，必须在**频段上分段声明**，或改用 L∞/时域判据。
4. **信号集合不同**：Definition 1 要求 $u_r\in L_p$ 且 $\|x(0)-\bar x\|$ 存在。P1 的 OTF 势场是**状态依赖的外部激励**（前车行为、cut-in、急刹），不保证属于 $L_2$；对 $L_\infty$（有界峰值）更自然——这正好对应"最大超调 / Jerk 峰值"。

**（4）P1 需要什么额外近似或局部线性化（可执行清单）**

- **路线 A（推荐，成本最低）**：在若干**工作点**（典型速度 $v^\ast$、典型间距、典型 OTF 场强度）对 CfC 闭环做**局部线性化**，得到一族 $\Gamma^{(k)}(j\omega)$，然后**逐工作点**检查 Theorem 1 的条件 2，并**报告每个工作点的裕度**（$1-|\Gamma^{(k)}(j\omega)|$ 的最小值）与工作点覆盖范围。诚实写法：这给出的是**局部（小信号）弦稳定**，不是全局结论。
- **路线 B（更贴定义、更贵）**：放弃传递函数，直接在时域估计 **Lp 增益**：对一族扰动幅值 $\|u_r\|_{L_2}$（或 $L_\infty$），测 $\|y_i\|_{L_p}/\|y_{i-1}\|_{L_p}$，报告"增益 ≤ 1 成立的最大扰动幅值"，即**弦稳定的吸引域**。这条与 Definition 1 的 class K 函数 α、β 直接对应，**不要求 LTI**。
- **路线 C（兜底）**：只报告**经验弦稳定指标**（相邻车加速度/间距误差的范数比随车辆序号的曲线，即 $\|y_i\|/\|y_{i-1}\|$ vs. $i$），并明确声明"**不声称满足 Ploeg 2014 的 Theorem 1 条件**，因为 CfC 非线性、判据前提不成立"。**这是最诚实、且能直接回应评审的写法**：把"定义出处"引 [Ploeg 2014]，把"判据不适用"写在 Limitations。
- 无论哪条路线，P1 必须**同时报告 OTF 势场是否参与弦稳定性论证**——若 OTF 场只影响决策层而不改变底层纵向控制的弦稳定性质，就**不得**把弦稳定性说成 OTF 势场的贡献（这正对应 `AGENTS.md` §1 的 P1 红线：不得预先声称"OTF 势场带来 X% 性能提升"）。

### ② 该文的间距策略是什么，与 P1 跟车误差 RMSE 指标如何对应

**策略**：**时距型（constant time headway）+ 固定停车间距**，即

$$d_{r,i}(t)=r_i+h\,v_i(t),\qquad i\in S_m$$

其中 $d_{r,i}$ 为期望车距（desired distance），$h$ 为 **time headway**（时距），$r_i$ 为 **standstill distance**（停车间距），$S_m$ 为车队集合；同质编队假设 h 对所有 i 相同。**不是**固定间距（$d_r$ = const），也**不是**"时延型"（delay-based）；论文明确说该策略"is known to improve string stability [18], [19] and safety [26]"，即**选时距型正是为了弦稳定性**。

**间距误差定义（P1 的 RMSE 口径必须与之区分）**：

$$e_i(t)=d_i(t)-d_{r,i}(t)=\big(q_{i-1}(t)-q_i(t)-L_i\big)-\big(r_i+h\,v_i(t)\big)$$

$q_i$ 为车辆 i 的后保险杠位置，$L_i$ 为其车长。控制目标为 $\lim_{t\to\infty}e_i(t)=0\ \forall i\in S_m$（车辆跟随目标）。

**与 P1 跟车误差 RMSE 的对应关系（三条，逐条可执行）**：

1. **物理量同名但口径不同**：P1 的"跟车误差"若定义为 $e_i(t)=d_i(t)-d_{r,i}(t)$，则与本文**完全同构**；RMSE 就是 $\sqrt{\frac1T\int_0^T e_i^2(t)\,dt}$（或对时间与车辆序号双重平均）。**但若 P1 采用固定间距（$d_r$ = const，对应 $h=0$）**，则两者的"误差为零"含义不同——固定间距下**弦稳定在本文框架里对任意增益都成立而无时延**（#5），却在有时延时最难满足（Fig. 3(b)：h 越小 θmax 越小）。**这正是评审会打的点**：固定间距 RMSE 可能更小（期望车距小、误差尺度小），但更难弦稳定。→ **P1 必须同时报告 h 的取值与 RMSE 的口径**，否则 RMSE 不可比。
2. **RMSE 与本文判据是两个层级的指标，不可互换**：$e_i\to0$（渐近跟随，由 Routh–Hurwitz 条件保证）是**稳定性/收敛性**；$\|\Gamma(j\omega)\|_{H_\infty}\le1$ 是**沿车队方向的扰动传播**。**RMSE 小 ≠ 弦稳定**：一个 RMSE 很小但弦不稳定的编队，其末端车仍可能出现误差放大。→ P1 报告 RMSE 的同时必须报告**沿序号的误差传播**（逐车的 RMSE/峰值曲线，即 $\mathrm{RMSE}_i$ vs. $i$ 单调不增才算经验弦稳定），这正是本文 Definition 1 的 strict 不等式在时域的直接读法。
3. **本文未报告任何 RMSE 数值，也没有报告 $r_i$、$L_i$**（见 §六.A.4）→ **P1 不能引用本文的任何 RMSE 或间距数值**；能引用的是**定义与判据的形式**，以及"时距型策略有利于弦稳定"这一定性结论（出处 [18][19][26]，**转引**）。引用时必须标注：**文献报告值，协议不同，不可直接比较**。

### ③ 它的仿真/实验设置能否被 P1 直接复用为基准场景

**先纠正一个易犯错误**：本文 §VI **是实车实验，不是仿真**（六辆乘用车、IEEE 802.11p、10 Hz、实测 |Γ(jω)| 与速度响应）。§V 的 Fig. 3/4 则**是**线性模型的数值计算（非仿真平台、非实车）。

**逐项"可否直接复用"判定**：

| 项目 | 本文设置 | P1 可否复用 | 理由与需要的改动 |
|---|---|---|---|
| 车辆数 | 6 辆 + 1 个虚拟参考车 | **可复用（建议）** | 6 车足以显现沿序号的扰动传播，又与 P1 的 CARLA 算力预算相容；但注意 §VI 的 |Γ| 验证实际上只用到**相邻两车**，P1 需做**全串激励**才能得到 6 车的完整传播曲线 |
| 初始条件 | **未报告**（§VI 未说明是否从平衡态起步） | **不可复用，须自行定义** | Definition 1 含 $x(0)$ 扰动项 β，但实验初值未给；P1 必须自报初值分布（`AGENTS.md` §5 要求"报告场景数、初始条件分布、失败分类"） |
| 扰动形式 | ① prescribed acceleration profile $a_0(t)$（引自 [27]，**本文未给数值**）；② 前车 **constant acceleration** 起步 | **形式可复用，参数不可复用** | 两种都是"前车纵向激励"，与 P1 的"前车减速"工况可对齐；但 $a_0(t)$ 的幅值/带宽/时长不明，P1 需自建 profile 并报告；**P1 缺少的工况本文完全没有**：cut-in、急刹、编队单车退出、激进车流扰动（`AGENTS.md` §5 的长尾场景） |
| 间距策略 | 时距型，$r_i+h v_i$，实验 $h=0.7$ s | **可复用为对照之一** | 建议 P1 同时跑"固定间距"与"时距型（$h$ 取 0.7 s 一类值）"两档，并报告各自 RMSE 与弦稳定性——这样才可与本文做**口径对齐**的比较 |
| 控制器 | LTI，$k_p=0.2,k_d=0.7,k_{dd}=0$，前馈 $u_{i-1}$ 经无线通信 | **可作为 P1 的额外基线，但须重实现** | 这是 P1 基线清单（PID/MPC/TD3 直控/OTF-CfC，`AGENTS.md` §3）之外的一个**强基线**——CACC + 前车加速度前馈。若 P1 要用，须**自行实现**（本文无代码），并注意公平性：P1 的 OTF-CfC 不得获得比它更多的特权输入（`AGENTS.md` §3） |
| 通信模型 | 时延 $\theta\approx0.15$ s，10 Hz，IEEE 802.11p | **不可直接复用** | P1 在 CARLA 里无法复现 802.11p 的物理层；只能设一个等效时延参数（如 0.15 s）并**明确声明这是文献参数、非实测** |
| 车辆模型 | $G(s)=\frac{1}{s^2(\tau s+1)}e^{-\phi s}$，$\tau=0.1$ s，$\phi=0.2$ s（辨识自 [27]） | **公式可复用，参数不可复用** | 三阶线性模型是编队控制的标准起点，P1 可用它做**预验证/解析对照**；但 $\tau,\phi$ 是那套试验平台的值，P1 的 CARLA 车辆动力学需另行辨识或直接使用 CARLA 的动力学 |
| 度量 | $|\Gamma(j\omega)|$（Welch 估计）+ 速度响应曲线 | **可复用（推荐）** | 这是本文最有复用价值的协议：**用相邻车输出的频响比来实证弦稳定性**，并报告低频段估计不确定度（本文的教训，见 §五.4） |
| 统计 | **无**（单次运行、无重复、无 CI） | **不可复用 —— 必须加强** | P1 按 `AGENTS.md` §4 要求"种子 ≥5，报 mean ± std 或 95% CI"。**若 P1 沿袭本文的单次运行做法，将被直接判定不合格** |

**结论**：本文的设置**可作为 P1 的一个"文献基准场景"的骨架**（6 车 / 时距型 / 前车加速度激励 / 频响比度量），但**四项必须替换**：初始条件（自报分布）、扰动参数（$a_0(t)$ 自建）、通信时延（自设并声明为文献参数）、统计量（≥5 种子 + CI）。同时**必须补齐本文没有的长尾工况**（cut-in、急刹、编队退出、激进车流）。任何把本文数值（h = 0.7 s、0.3 s、15.5 s/8.5 s）当成 P1 性能基准的写法，都须标注：**文献报告值，协议不同，不可直接比较**。
