# 精读笔记（P1 文献 #7）：Physics-Informed Neural Nets for Control of Dynamical Systems

- **文献**：Antonelo, E. A., Camponogara, E., Seman, L. O., Jordanou, J. P., de Souza, E. R., & Hübner, J. F. (2024). *Physics-informed neural nets for control of dynamical systems.* **Neurocomputing, 579, 127419.** DOI: 10.1016/j.neucom.2024.127419
  - 【已核验】Crossref 元数据（2026-10-02 查询 `api.crossref.org/works/10.1016/j.neucom.2024.127419`）：标题、卷 579、文章号 127419、published-print 2024-04、ISSN 0925-2312、PII S0925231224001905、references-count = **57**、is-referenced-by-count = 149（索引日 2026-09-30）。
  - 【勘误，供 `citation-and-related-work` 使用】任务简报中的作者串 "de Souza EN … Jordanou JP" 与 Crossref/arXiv 不一致：正确为 **de Souza, Eduardo Rehbein（E. R.，不是 E. N.）**，且 Crossref 与 arXiv 的作者顺序均为 `Antonelo → Camponogara → Seman → de Souza → Jordanou → Hübner`（简报把 Jordanou 与 de Souza 次序对调）。
- **精读日期**：2026-10-02 ｜ **全文来源**：**已获全文**（纯文本 `literature/fulltext/p07-pinn-ctrl-neucom2024.txt`，约 80.7 k 字符 / 1421 行，`SOURCE_URL: https://arxiv.org/html/2104.02556`，`FETCH_DATE: 2026-10-02`）。
- **⚠️ 版本口径（本笔记的首要限定）**：本笔记逐字精读的是 **arXiv 2104.02556 的 HTML 版**（下文所有页码/表号/数字均指该版）。Crossref 显示**正式发表版（VoR）有 57 条参考文献，而 arXiv HTML 只有 48 条**；VoR 多出的条目中包含 **Optuna（Akiba et al., 2019，超参数优化框架）**、**Nicodemus et al. 2022（PINN-based MPC for multi-link manipulators）**、**Xiang et al. 2022（self-adaptive loss balanced PINN）**、Li et al. 2020（FNO）、Dwivedi et al. 2020（PIELM）等，而这几条在 arXiv HTML 中**完全不存在**（已 grep 确认无 "Optuna/Nicodemus/Xiang/Dwivedi/Fourier neural operator" 等字样）。这强烈提示 **VoR 的"超参数搜索"与"损失加权"两节可能与本笔记所见版本实质不同**——见 §三 与 §九。

---

## 作用域

**场景①：项目内文献工作。**

- **项目**：`D:\Deepseek Harness\auto-driving`（自动驾驶 OTF 论文集群）。
- **项目不变量文件**：`D:\Deepseek Harness\auto-driving\AGENTS.md`。
- **本次精读服务的主张**：论文 1（P1，代号 **OTF-CfC**）「基于超车频次势场与液态神经网络的高速主线编队连续时间控制」。
- **P1 主张上限（`AGENTS.md` §1 原文，逐条引用，本笔记不得越界）**：
  1. > **P1 红线**：不得预先声称"OTF 势场带来 X% 性能提升"。……在 LNN 控制范式下**未经本项目实测即属 C/D 级证据**。A1 消融须诚实报告；若不显著，卖点改为"**可解释性 + 零额外传感器成本**"。
  2. > **不得把仿真/回放写成实车验证**：CARLA（Town04）与实车数据回放都是仿真或开环证据。未做真车闭环前，措辞上限是"在 CARLA 与真实数据回放中"。
  3. > **不得直接搬用他人论文数字**：与 DriveDreamer 等对比若未同协议复现，必须标注"文献报告值，协议不同，不可直接比较"。
- **本笔记对本项目的直接约束**：本笔记所抄录的一切数值均为 **文献报告值，协议不同，不可直接比较**；不得作为 P1"OTF 势场带来 X% 提升"的任何形式证据；本笔记不评价该工作的**重要性**与**新颖性**（见 §九 视角限制）。

---

## 一、作者主张

作者主张：经典 PINN（Raissi et al., 2017/2019）把连续时间 $t$ 作为唯一输入、输出 ODE/PDE 的解，物理以**损失项**形式进入学习；但原始 PINN **不接受控制输入**，也**无法在训练时固定之外的时间区间上长时间仿真而不严重退化**（Abstract："In their original form, PINNs do not allow control inputs, neither can they simulate for variable long-range intervals without serious degradation in their predictions."）。为此，本文提出 **PINC（Physics-Informed Neural Nets for Control）**：把网络条件化在**初始状态 $\mathbf{y}(0)$ 与控制输入 $\mathbf{u}$** 上，即 $\mathbf{y}(t)=f_{\mathbf{w}}(t,\mathbf{y}(0),\mathbf{u}),\,t\in[0,T]$；以**自环（self-loop）链式**方式（把上一段末状态当作下一段初状态）实现**任意长、且不必预先固定**的时间仿真；由于 $T$ 取为采样周期 $T_s$，网络退化为一个**离散控制接口** $\mathbf{y}[k]=\widehat{f}_{\mathbf{w}}(\mathbf{y}[k-1],\mathbf{u}[k])$，可直接替换 NMPC 中的状态方程（Eq. 5b）构成 "Multiple Shooting-inspired" 的 NMPC（Eq. 12），并可由自动微分提供 Jacobian 给求解器。作者据此提出四条贡献（Intro (i)–(iv)）：(i) 输入增广；(ii) 长时程仿真能力；(iii) **"第一个"让连续时间物理信息网络可用于 MPC 的工作**；(iv) 推理式仿真比数值积分更满足实时要求。**注意作者并未把 PINC 当作控制器**——控制器始终是 NMPC，PINC 只是其中的**预测模型**。实验对象是 **Van der Pol 振子**（2 状态、1 输入）与**四水箱（four-tank）系统**（4 状态、2 输入，取 Johansson 2000 的非最小相位参数组），基线是**用被控对象自身的精确 ODE + 四阶 Runge–Kutta（RK4）作预测模型的 NMPC**（一个"神谕"基线）。指标为 $\mathrm{MSE}_{gen}$（自环模式、对照 RK 真值，Eq. 13）、控制性能 $\mathrm{IAE}$（Eq. 14）与 $\mathrm{RMSE}$（Eq. 15）、以及桌面机上的墙钟时间。作者的结论是：PINC 在 RMSE/IAE 上"实际上与 ODE/RK 达到同一结果"、在四水箱上快 23.3%，并（在只喂初值、不含任何实测数据的训练集下）成功实现了带约束的参考跟踪；鲁棒性用 $\pm 5\%$ 的参数/初值扰动（各 151 次仿真）以直方图展示。作者自认：**该框架本身没有处理建模误差与完全抑制扰动的机制，无积分作用因而存在稳态误差，这些留作未来工作**。

---

## 二、主张—证据台账

> **评级口径说明（务必与下游同步）**：依 `deep-paper-reader` §3.1 规则"若一条主张的证据是仿真，等级最高 C"，而本文的**全部经验证据都是低维 ODE 的数值仿真**，故本表经验性主张的**内部等级上限被规则压到 `C_int`**——这是**评级规则的后果，不是本文独有的缺陷**。`D_int` 用于**无实验支撑的推断/预测/文献优先级主张**。若某条主张被本文自己的数字否定，仍按证据类型给级，并在"是否被结果支撑"列写"否/部分"。`外部复现` 列依任务要求**一律填"未检"**；按技能 §3.1.1，"未检"是**信息缺失**，**不等于**"已检：无独立复现"。

| # | 作者主张（英文原句） | 支撑证据（图/表/统计量） | 内部等级 | 外部复现 | 是否被结果支撑 | 缺口 |
|---|---|---|---|---|---|---|
| 1 | "Remarkably, PINC achieves practically the same result as the ODE/RK approach in terms of RMSE and IAE, while being slightly faster on average when executed with 10 repetitions on the same desktop computer."（§4.1.4，针对 Van der Pol） | Table 1：RMSE 0.15 vs 0.15；IAE 123.6 vs 122（+1.31%，本笔记复算）；时间 3.32±0.15 s vs 3.41±0.04 s；Fig. 10 左右两栏曲线叠合 | `C_int` | 未检 | **部分**：RMSE/IAE 在 VdP 上确为同量级；但**"faster"不成立**——$\Delta=0.09$ s **小于** PINC 侧报告的 0.15 s，且无配对检验、无 n 之外的信息 | RMSE/IAE 为**单次仿真**，无重复、无 CI；± 的语义（SD 还是 SE）**全文未定义**；无显著性/非劣检验；"practically the same"是点估计比较而非等价检验 |
| 2 | "Although IAE seems to differ more between PINC and ODE/RK, RMSE errors for both methods are almost equivalent."（§4.2.2，四水箱） | Table 1：RMSE 0.811 vs 0.807（+0.50%，复算）；IAE **876 vs 544（+61.03%，复算）** | `C_int` | 未检 | **部分**：RMSE 近似成立；**IAE 差 61% 与"同一结果"的总体叙事不一致**，且 IAE 恰恰是作者自己在 §4.2.3 选用的鲁棒性主指标 | 未解释 RMSE 与 IAE 的分歧来源（稳态误差？IAE 对长时程漂移的累积敏感性？）；无逐场景/逐时段分解；无 CI |
| 3 | "The average time spent on a desktop computer for the complete control simulation using PINC, repeated 10 times, 10.85s, is 23.3% inferior than using the ODE of the four tanks as a model for MPC (14.15s)"（§4.2.2） | Table 1：10.85±0.14 s vs 14.15±0.13 s（n=10）；本笔记复算 $1-10.85/14.15=23.32\%$ ✓ | `C_int` | 未检 | **是**（数值自洽、量级远大于波动） | 计算平台仅写"a desktop computer"（CPU/GPU/框架版本均未报告）；MPC 求解器名称、容差、迭代次数、每步 NLP 规模**全部未报告**→"同等求解预算"未被证明；未说明计时边界（是否含 NLP 求解与网络推理） |
| 4 | "our proposal, after the network is trained, has shown that it is possible to speed up the runtime of these simulations (**up to 30% on average**)."（§4.3 讨论）＋ Abstract："this long-range time simulation of differential equations is **faster than numerical methods**" | §4.3 无表无图；可对应的只有 Table 1 的两组时间 | `C_int` | 未检 | **否**：Table 1 能算出的加速为 **VdP 2.64%** 与 **四水箱 23.32%**（本笔记复算），**没有任何一组达到 30%**；"on average"的分母也不明 | "30%"的出处不明（是未展示的实验？是 PDE 的"10x"文献值的误植？）；同一"更快"主张存在 **2.64% / 23.3% / 30%** 三个口径 |
| 5 | "Experiments show that the training data size $N_t$ required for learning a certain dynamical behavior is **drastically reduced** due to the a priori information assimilated from $\mathrm{MSE}_{\mathcal{F}}$."（§3.1） | §3.1 为方法节，**未引任何图表**；全文**没有 $\lambda=0$（关闭物理损失）的消融**，也没有与纯数据驱动模型（ESN/LSTM）的同条件对比；唯一相关的是 Fig. 5b（$N_f$ 与 $N_t$ 的联合扫描，5 次随机初始化平均） | `D_int` | 未检 | **否**（无直接证据）：Fig. 5b 至多说明"配置点太少时训练失败"，**无法把数据量下降归因于 $\mathrm{MSE}_{\mathcal{F}}$** | **最小补法**：固定 $N_t$ 网格、令 $\lambda=0$（等效普通 MLP 回归），比较达到同一 $\mathrm{MSE}_{gen}$ 所需的 $N_t$；本文缺的正是这个对照 |
| 6 | "if we assume that the given ODE is an exact representation of the process, it is enough for this dataset to contain only the initial conditions of the modelled ODE."（§3.3.3）；"Practically, this does not require collecting data from ODE simulators." | Eq. (10) 训练对 $(t,\mathbf{y}(0),\mathbf{u})^j$ 全部取 $t=0$ 且目标 = $\mathbf{y}(0)$；$N_t=1{,}000$ 个随机初值/控制对；Fig. 9（VdP 随机 $u$）、Fig. 12（四水箱）预测叠加真值 | `C_int` | 未检 | **是**（在"ODE 精确"这一自设假设下） | 该结论的适用边界被作者自己写死为"ODE 精确已知"；本文**没有任何实测数据**，因此不能推断"稀疏实测数据 + 物理"的表现（作者在 Conclusion 中亦仅为 foresee）；$\lambda$ 未给出→物理项与初值项的权衡不可复现 |
| 7 | "our proposed PINC network can run for **an indefinite time horizon** as long as it is necessary, **without significant deterioration** of network prediction."（Intro (ii)）＋ "conventional PINNs would need to be retrained from scratch if a different initial condition or control input is required."（§4.1.3） | Fig. 6（1 个固定初值、固定 $u=0.54$，PINN 逐个 $T\in\{0.5,1,2,5,10\}$ s 重训 vs 单个 PINC）；Fig. 7（RMSE vs PINN 训练所用 $T$）；§4.1.3 自述 "At $T=10s$, PINN has slightly lower error than PINC"；Fig. 12 显示自环长程偏差 | `C_int` | 未检 | **部分**：长程不退化在给定初值/$u$ 下成立；但**同一句话在 Four tanks 上不被无条件支持**——§4.2.2 承认 "The deviation in prediction at longer ranges … is expected" | 长程对比只用了**单一初值与单一控制输入**；"indefinite"无误差上界/漂移率量化；自环误差累积机制未量化；无重复运行 → 无法区分网络初始化方差与系统性漂移 |
| 8 | "*泛化到未见过工况*"：PINC 对**任意初值与控制输入**成立（Abstract："able to simulate for longer-range time horizons that are not fixed beforehand"；§3.3："operates with variable initial conditions as well as control inputs that can change over the complete simulation"） | Fig. 9 / Fig. 12（随机生成的控制信号、测试数据）；§4.1.2 "The validation dataset is composed of 1810 points obtained using a randomly generated control action $u$"；§4.2.2 测试集为"new randomly generated control actions (not shown)" | `C_int` | 未检 | **部分** | **"泛化"的范围仅限同一条 ODE 的采样区间内**（VdP：$u\in[-1,1]$、$x_{1,2}\in[-3,3]$）：没有跨系统、跨参数区间外推、跨工况（如不同 $\mu$、不同阀门开度 $\gamma$）的测试；四水箱的训练/测试采样区间**根本未给出**；测试集生成协议"not shown" |
| 9 | "The best generalization error ($10^{-2.87}$) is achieved with a deep network of 10 layers with 20 neurons each."（Fig. 5a caption） | Fig. 5a（$\log_{10}\mathrm{MSE}$，对 10 次随机权重初始化取平均）；10 层配置的最佳值仅出现在**图注** | `C_int` | 未检 | **是**（对图内排序而言） | 最终选用的 4 层配置的误差值**从未印出**→无法量化"为了省算力损失了多少精度"；$\mathrm{MSE}$ 的物理单位与状态归一化方式未说明；"training time is fixed to a constant number of iterations"掩盖了不同容量网络的收敛差异（作者自己也说"errors would decrease even further if training had been extended"） |
| 10 | "Clearly, 40 data points are not enough, and the proportion $N_f/N_t$ should be considerably higher than 4"（§4.1.2） | Fig. 5b（$N_f$ vs $N_t$ 热力图，5 次随机初始化平均）；最终配置 $N_t=1{,}000$、$N_f=100{,}000$（比值 100） | `C_int` | 未检 | **部分**（方向可信，幅度不可核） | 热力图的**轴取值与单元格数值均未印出**；"4"这个阈值与"upper-right corner 是最差区"的叙述在文字上互相别扭（看不清到底是哪个角落差）→ **报告口径有歧义**；无 $\lambda=0$ 对照 |
| 11 | "the sensitivity experiments imply that the system does not lose much performance in terms of IAE. In fact, the occurrence of lower IAE simulations is actually higher."（§4.2.3） | Fig. 15（左：$k_1,k_2$ 均匀 $\pm5\%$ 扰动；右：初值 $\pm5\%$ 扰动；**每个直方图 151 次 MPC 仿真**；上排 5 层×20、下排 8 层×20）；Fig. 16（最大扰动下 IAE = 1022，作者自承"in the tail of the histogram"） | `C_int` | 未检 | **部分**（图确实显示分布未崩塌）；**"低 IAE 出现更多"与"不损失性能"缺统计支撑** | 无预定义容差、无均值/标准差/CI、无与未扰动基线的配对比较；"acceptable range"未定义；扰动只有**参数与初值的乘性 ±5%**，**不含未建模动态、测量噪声、执行器饱和、时延** |
| 12 | *方差报告情况（事实性核查）*："averaged over 10 different random initializations of the network weights"（Fig. 5a）；"averaged over 5 different randomly initialized networks"（Fig. 5b）；"151 simulations were carried out"（§4.2.3）；"repeated 10 times"（Table 1 计时） | Fig. 5a、Fig. 5b、Fig. 15、Table 1 | `C_int` | 未检 | **是**（确有部分实验报告重复次数） | **关键控制指标（RMSE、IAE）全部为单次运行**；表 1 的 ± 仅有计时；**无随机种子、无重复次数对性能指标的报告、无任何显著性检验**；作者自承 "the random initialization of the weights of neural networks may cause different results" |
| 13 | "the particular structure of PINC makes physics-informed nets in continuous time amenable to MPC applications, **which is the first work in the literature to tackle this as far as the authors know**."（Intro (iii)） | §2.3 与 Zhai & Sands 2021（"we have not found any physics law that was included in the network training, making their network just an ordinary one"）、Liu & Wang 2021（离散化物理损失）、Gokhale et al. 2022（"they do not show actual control experiments"）、Meng et al. 2020（不可控）的**文献论证**，非实验 | `D_int` | 未检 | **不适用**（优先级主张不可由本文实验支撑） | **可核验的反证线索**：正式发表版（Crossref references）**新增了 Nicodemus et al. 2022 "Physics-informed neural networks-based model predictive control for multi-link manipulators"**，而 arXiv 版既未引用它、也未在"first work"句中提及——**该优先级主张至少被作者后来自己引用的工作侵蚀**（VoR 是否仍保留该句，本笔记无法判定，标 `[需核实]`） |
| 14 | *预测类（非结果）*："we foresee that using additional sparse data will make the training of PINC nets much faster"（Conclusion）；"we envision an even higher gain (e.g., **10x faster as reported in the literature** for simulation of PDEs with PINNs)"（§4.3） | 无实验；后者为**文献报告值** | `D_int` | 未检 | **不适用** | 10x 一句**必须**带"文献报告值，协议不同，不可直接比较"（本项目 `AGENTS.md` §1 第 4 条正对应此类转述）；训练时长本身是作者自认的主要障碍（"One of the main obstacles … is the long training of such networks"） |

**表下注**：Crossref 报告该文被引 149 次（索引日 2026-09-30）——这是**计量事实**，**不构成任何方向的外部复现证据**，故"外部复现"列仍一律为"未检"。

---

## 三、方法可复现性清单

| 项 | 论文是否给出 | 具体位置 | 缺失影响 |
|---|---|---|---|
| 数据来源与版本 | **部分给出（且本文不使用任何外部数据集）** | VdP 方程 Eq. (16)，$\mu=1$，$u\in[-1,1]$，$x_{1},x_{2}\in[-3,3]$（§4.1.1）；四水箱方程 Eq. (17)–(18)，**参数"same as the ones stipulated for the non-minimum phase experiment in Johansson [2000]"**（§4.2.1）——**具体数值未印出**；训练数据=随机采样的初值与控制（§3.3.3） | 四水箱的 $A_i,a_i,k_j,\gamma_j,g$ 与采样区间缺失 → **训练集（$N_t=10^3$、$N_f=10^5$）无法重建**；须去翻 Johansson (2000) 并猜采样区间；VdP 采样分布（均匀？）也未明说 |
| 预处理与划分方式 | **基本未给出** | 验证集"1810 points obtained using a randomly generated control action $u$ (e.g., Fig. 9)"（§4.1.2）；测试集"new randomly generated control actions (**not shown**)"（§4.2.2）；无 train/val/test 划分比例或独立性说明；collocation 点区间为 $t\in[0,T]$（§3.3.3） | 训练/验证/测试**同源同分布且时序相关**（同一条随机 $u$ 轨迹）→ $\mathrm{MSE}_{gen}$ 的乐观/悲观方向不可判；无划分脚本 → 复现出来的"泛化误差"不可比 |
| 模型/实验装置规格 | **部分给出** | 最终配置：VdP 4 隐层×20 神经元、四水箱 5 层×20（§4.1.4、§4.2.2）；全连接（Fig. 2 caption）；权重 Xavier normal 初始化（Algorithm 1）；**激活函数未给出**；是否含 skip connection 只作为"preliminary work"提及（§4.3）；**参数量、FLOPs、推理延迟均未报告** | 激活函数是 PINN 精度的关键自由度 → 结构不可精确重建；"更深更好"（Fig. 5a）与选定较浅网络的取舍无法验证；无内存/延迟指标（对照 P1 需报 MCU 内存与端到端延迟的指标集） |
| 超参数与搜索空间 | **部分给出，关键项缺失** | $K_1=500$ epochs（ADAM）+ $K_2=2{,}000$（探索，§4.1.2）/ **$K_2=20{,}000$（最终，§4.1.4、§4.2.2）**；$N_t=1{,}000$、$N_f=100{,}000$；MPC：$N_1=1,\ N_2=5,\ N_u=N_2,\ Q=10\mathbf{I},\ R=\mathbf{I}$；$T=T_s=0.5$ s（VdP）/ $10$ s（四水箱）；"grid search experiments over hyperparameters"（§4.1.2）但**网格取值与结果未列表**；**$\lambda$ 只写"set empirically"（§3.1、§3.3.3），数值未给**；PINC 的 ADAM 学习率未给（只给了对照 PINN 的 0.0035/0.001）；L-BFGS 配置未给 | **$\lambda$ 缺失＝物理约束注入强度不可复现**，而这是全文机制的核心；"grid search"无表格 → 无法判断调参预算、无法判断是否对基线不公平；**VoR 新增 Optuna 参考文献**，提示正式版可能补了搜索方法——须以 VoR 复核 |
| 随机种子 / 重复次数 | **重复次数部分给出，种子一律未给** | 10（Fig. 5a）、5（Fig. 5b）、151（Fig. 15）、10（Table 1 计时）；**无任何 seed 说明** | 无法复现方差、无法判断差异是否超出随机波动；作者自承权重初始化会改变结果，却未固定种子 |
| 评价指标定义（含边界情况） | **给出公式，边界情况未定义** | $\mathrm{MSE}_{gen}$ Eq. (13)（自环模式、对照 RK、与 PINC 用同一 $u[k]$）；$\mathrm{IAE}$ Eq. (14)；$\mathrm{RMSE}$ Eq. (15)；计时="the average time spent … for the complete control simulation" | 指标本身可复算；但**未扰动基线 IAE 的口径随初值变化**（见 §四 口径对照表）；约束满足仅定性（"which were respected"，最大越限量未报告）；稳态误差未量化 |
| 基线实现来源 | **定性给出，无代码/无实现细节** | 基线 = 用**被控对象自身的精确 ODE** 作 MPC 预测模型，数值解用"classic, fourth-order Runge-Kutta method (RK4)"（§4.1.4）；"This ODE/RK-based model is the reference model that represent the plant itself"（§4.2.2） | 基线是**神谕（oracle）**：拥有与受控对象**逐字相同**的模型 → 只能证明"没变差"，不能证明"比任何可实现的替代方案好"；无 PID、无 ESN/LSTM（Jordanou 2021、Terzi 2020 均被引用却未做对比）、无 RL 基线；求解器与容差未给 |
| 显著性检验方法 | **完全没有** | 全文无 p 值、无检验、无 CI、无等价/非劣检验（已逐词 grep 确认） | "practically the same"、"does not lose much performance"、"slightly faster" **全部是无检验的点估计断言**；按本项目 `AGENTS.md` §4 与技能 §3.4，这属**推断错误**（不得由无检验推出"无差异"），也是本笔记给不出 B 级以上等级的直接原因 |
| 代码/数据可用性声明 | **未发现** | 按 `github` / `code (is )?avail` / `data availab` / `supplement` 等关键词在全文 grep **均无命中**，正文与文末亦无此类小节；仅有基金致谢（CNPq 308624/2021-1、FAPESC 2021TR2265） | 复现须全量重实现（含 NMPC 求解器接线）；表 1 与各图数字**不可由第三方独立重算**——这正是本项目"结果唯一来源"纪律要防的情况 |

---

## 四、关键数字表

> 纪律：以下数字**全部**抄自 arXiv 2104.02556 HTML 版**正文/表/图注的印刷值**（不是估读）；单位、样本量、系统名随行。本笔记自己算出的派生量一律标注「**复算**」。**引用任一数字都必须带上 §七 的 `citation_qualifier`。**

| 指标 | 值 | 不确定度 | 出处（表/图/节） | 备注（哪个系统、哪个设置） |
|---|---|---|---|---|
| RMSE（控制） | **0.15** | 未报告 | Table 1 | Van der Pol，60 s 仿真，$T=T_s=0.5$ s，PINC 作 MPC 模型，单次运行 |
| RMSE（控制） | **0.15** | 未报告 | Table 1 | 同上，基线 ODE/RK4 作 MPC 模型 |
| IAE（控制） | **123.6** | 未报告 | Table 1 | Van der Pol，同上 |
| IAE（控制） | **122** | 未报告 | Table 1 | Van der Pol，基线 ODE/RK4 |
| 墙钟时间 | **3.32 ± 0.15 s** | ± 语义未定义（SD/SE 未说明），n=10 | Table 1；§4.1.4 "repeated 10 times on the same desktop computer" | Van der Pol，整段控制仿真；平台仅"a desktop computer" |
| 墙钟时间 | **3.41 ± 0.04 s** | 同上，n=10 | Table 1 | Van der Pol，基线 ODE/RK4 |
| RMSE（控制） | **0.811** | 未报告 | Table 1 | Four tanks，2400 s 仿真，$T=T_s=10$ s，初值 $h_1=h_2=2$ |
| RMSE（控制） | **0.807** | 未报告 | Table 1 | Four tanks，基线 ODE/RK4，同初值 |
| IAE（控制） | **876** | 未报告 | Table 1（口径见 §四 对照表第 1 行） | Four tanks，PINC，初值 $(2,2)$，标称参数 |
| IAE（控制） | **544** | 未报告 | Table 1 | Four tanks，基线 ODE/RK4，初值 $(2,2)$ |
| 墙钟时间 | **10.85 ± 0.14 s** | ± 语义未定义，n=10 | Table 1；§4.2.2 | Four tanks，整段控制仿真 |
| 墙钟时间 | **14.15 ± 0.13 s** | ± 语义未定义，n=10 | Table 1；§4.2.2 | Four tanks，基线 ODE/RK4 |
| IAE（受扰） | **1022** | 未报告 | Fig. 16 caption | Four tanks，$k_1,k_2$ 施加 **5% 最大扰动**，初值 $h_1=h_2=9$；作者注："in the tail of the histogram from Fig. 15(a) left plot" |
| 最佳泛化 MSE | $\log_{10}\mathrm{MSE}=\mathbf{-2.87}$，即 $\approx \mathbf{1.35\times10^{-3}}$（**复算**） | 对 10 次随机权重初始化取平均（未给散布） | Fig. 5a caption | Van der Pol，10 层×20 神经元；训练迭代数固定；仅图注给出该数值 |
| 敏感性运行次数 | **每直方图 151 次** | — | Fig. 15 caption；§4.2.3 | Four tanks；左列 $k_1,k_2\sim U_{5\%}$、右列初值 $\sim U_{5\%}$；上排 5 层、下排 8 层 |
| 训练集规模 | $N_t=\mathbf{1{,}000}$（仅初值/控制对）、$N_f=\mathbf{100{,}000}$（配置点） | — | §4.1.2、§4.1.4、§4.2.2 | 两套系统相同 |
| 训练轮次 | $K_1=\mathbf{500}$ epochs（ADAM）+ $K_2=\mathbf{20{,}000}$（L-BFGS，最终） | — | §4.1.4、§4.2.2（探索期用 $K_2=2{,}000$，§4.1.2） | 从 2,000 增到 20,000 使验证误差改善"at least one order of magnitude"（§4.1.4，**无具体数值**） |
| 控制时域/权重 | $N_1=\mathbf{1},\ N_2=\mathbf{5},\ N_u=N_2,\ Q=10\mathbf{I},\ R=\mathbf{I}$ | — | §4.1.4、§4.2.2；Algorithm 2 | 两套系统**相同**；VdP 预测时域 $5T=2.5$ s，Four tanks $5\times10=50$ s |
| 采样周期 | $T=T_s=\mathbf{0.5}$ s（VdP）／$\mathbf{10}$ s（Four tanks） | — | §4.1.2、§4.2.2 | 网络内区间 $T$ 与 MPC 采样周期被设为相等 |
| 状态约束 | $h_3,h_4\in[\mathbf{0.6,5.5}]$ cm；$h_1,h_2$ 允许区间 $[2,20]$ | 最大越限量未报告 | Fig. 13 caption；§4.2.2 | Four tanks；"which were respected"仅定性 |
| 加速比 | **23.3%**（四水箱）／**2.64%**（VdP，**复算**）／**"up to 30% on average"**（§4.3，无出处） | 未报告 | Table 1 与 §4.3（**互相冲突**） | 见 §四 对照表第 3 行 |
| 文献转述值（**非本文测量**） | "**10x faster** as reported in the literature for simulation of PDEs with PINNs" | — | §4.3 | **文献报告值，协议不同，不可直接比较**；不得作为本文或 P1 的结果 |

### 数字口径对照表

> 触发条件成立（同一指标在本文出现 ≥2 个数值）。**口径列不得为空**；引用任一数值必须连同口径一起引。

| 指标 | 数值 | 系统 / 初值口径 | 参数口径 | 训练口径 | 其他设置 | 出处 |
|---|---|---|---|---|---|---|
| IAE | **876** | Four tanks，初值 $h_1=h_2=\mathbf{2}$（"the minimum of the allowed interval"） | 标称 $k_1,k_2$（无扰动） | $K_2=20{,}000$，5 层×20 | PINC 作 MPC 模型，2400 s | Table 1 / §4.2.2 |
| IAE | **544** | Four tanks，初值 $(2,2)$ | 标称 | 不适用（无训练） | 基线 ODE/RK4 作 MPC 模型 | Table 1 |
| IAE | **1022** | Four tanks，初值 $h_1=h_2=\mathbf{9}$（"middle point"） | $k_1,k_2$ **最大 +5% 扰动** | 同上 | PINC，作者称位于 Fig. 15(a) 左图分布尾部 | Fig. 16 caption |
| IAE | **未印出具体数值** | Four tanks，初值 $h_1=h_2=9$ | **未扰动** | 同上 | 仅称直方图峰值与它"approximately coincides" | Fig. 15 caption + §4.2.3 |
| 加速幅度 | **2.64%**（复算） | Van der Pol，60 s | — | 4 层×20 | $\Delta=0.09$ s < 0.15 s（PINC 侧报告散布）→ 不可宣称更快 | Table 1 |
| 加速幅度 | **23.32%**（论文写 23.3%，复算一致） | Four tanks，2400 s | — | 5 层×20 | 单机、单框架、求解器未报告 | Table 1 / §4.2.2 |
| 加速幅度 | **"up to 30% on average"** | **未指明系统** | — | — | 与上两行冲突 | §4.3 |
| 验证集规模 | **1810 点 = 905 s** | Van der Pol，$T_s=0.5$ s | — | — | §4.1.2 正文 | §4.1.2 |
| 验证集规模 | **1810 点 = 90 s** | 同上 | — | — | **Fig. 8 图注；与上一行差 10 倍** | Fig. 8 caption |
| 精度改善（延长训练） | **"at least one order of magnitude"** | Van der Pol | — | $K_2$ 从 2,000 → 20,000 | **无具体数值**（对照 Fig. 5a/5b 的 4 层配置误差从未印出） | §4.1.4 |

**本笔记的自洽性复算（仅用论文印刷值，非重算原始数据）**：$3.32/3.41\Rightarrow2.64\%$；$10.85/14.15\Rightarrow23.32\%$（论文 23.3% ✓）；$876/544\Rightarrow+61.03\%$；$123.6/122\Rightarrow+1.31\%$；$0.811/0.807\Rightarrow+0.50\%$；$1810\times0.5=905$ s（正文 ✓ / 图注 ✗）；$10^{-2.87}=1.35\times10^{-3}$。

---

## 五、统计与推断旗标

1. **"无差异"没有等价检验（推断错误）**。§4.1.4 的 "practically the same result … in terms of RMSE and IAE"、§4.2.3 的 "does not lose much performance"、以及 "slightly faster" 全部建立**点估计比较**之上，全文**无 p 值、无检验、无 CI、无非劣/等价检验**（已逐词 grep 确认）。按 `AGENTS.md` §4 与技能 §3.4，这不构成"性能相当"的证据。
2. **± 语义未定义**。Table 1 的 `3.32±0.15`、`10.85±0.14` 等未说明是 SD 还是 SE。若是 SE，则 VdP 的 SD 约为 0.47 s（远大于 0.09 s 的差值），结论方向不变但**波动尺度完全不同**；若是 SD，VdP 的"更快"就已落在噪声内。
3. **VdP 的"更快"不成立**：$\Delta = 3.41-3.32 = 0.09$ s < PINC 侧散布 0.15 s，且无配对检验、无重复实验的分布说明 → 该子主张**不应被引用**。
4. **RMSE 与 IAE 给出相反画面，且未调和**。四水箱上 RMSE 差 0.5%、IAE 差 61%；作者只写 "IAE seems to differ more"，没有解释。**更关键的是作者随后用 IAE 作为鲁棒性主指标（Fig. 15）**——在最不利指标上做鲁棒性叙事，存在**选择性指标使用**的风险。
5. **鲁棒性分析无推断框架**。151 次运行只以直方图呈现：无均值/标准差/分位区间、无"可接受范围"的先验定义、无与未扰动基线的配对检验；"the occurrence of lower IAE simulations is actually higher" 是**对图的定性读数**，无计数、无检验。Fig. 16 的 IAE=1022 被作者自己定位为分布尾部 → 与"不损失性能"的总结存在张力。
6. **无多重比较讨论**；超参数扫描（网络深度/宽度、$N_f$、$N_t$）的选择过程未列表，**选择效应**无法评估（选中 4 层而非 10 层，其误差未印出）。
7. **效应量与不确定度普遍缺失**；唯一带"±"的指标是墙钟时间；作者自承权重初始化会引起不同结果，却未固定种子。
8. **图-only 报告**。Fig. 5a/5b/7/15 的数值只以（对数/热力图/直方图）图形给出，正文无对应表格 → 第三方只能**估读**（本笔记拒绝给出任何估读值）；这使所有基于这些图的结论**不可定量复核**。
9. **约束满足为定性声明**。"The control was successful in spite of the constrains imposed on $h_3$ and $h_4$ (which were respected)"，但**最大越限量、越限次数、越限时长均未报告**。
10. **"无稳态误差"未量化**：§4.2.2 承认 "some minor error in steady regime"，§4.2.3 解释 "Since the PINC control strategy has no integrators, a small steady state error that depends on model match is expected"（无积分作用）——这部分误差**没有数值**，却恰好是 IAE 差异（876 vs 544）最可能的来源。
11. **外部有效性无统计表述**：全部结论来自两套**低维、精确已知**的 ODE 仿真；无测量噪声、无未建模动态、无时延、无实时硬件约束；作者自述 "does not have an inherent method to deal with modeling errors and completely reject disturbances"。
12. **一处算术/口径冲突需作者澄清**（非统计但影响可核验性）：验证集 905 s（§4.1.2）vs 90 s（Fig. 8 caption）。

---

## 六、缺失信息清单

**A. 未报告（可直接补，影响最大）**

1. **未报告：损失权重 $\lambda$ 的数值（及是否按系统分别调）**。全文只写 "The parameter $\lambda$ is set empirically so that $\mathrm{MSE}_{y}$ and $\mathrm{MSE}_{\mathcal{F}}$ are not in disparate scales"（§4.1.2、§3.3.3）。**影响**：物理约束的注入强度——本文机制的旋钮——不可复现；任何"物理项有用"的判断都无法在其他数据规模下重现。**动作**：向作者索取 $\lambda$（含是否随 $N_t$、$N_f$ 变化），或按 VoR 新增的 Xiang et al. 2022（self-adaptive loss balanced PINN）线索核对正式版是否已给出自适应加权方案。
2. **未报告：Four tanks 的全部模型参数与训练/验证采样区间**（$A_i,a_i,k_j,\gamma_j,g$；$\mathbf{y}(0)$ 与 $\mathbf{u}$ 的采样区间与分布）。文中只给"same as Johansson [2000] 的非最小相位实验"。**影响**：$N_t=10^3$、$N_f=10^5$ 的合成训练集无法重建，四水箱的全部结论不可复现。**动作**：索取采样脚本或参数表；核 VoR 是否补了附录。
3. **未报告：计算平台与软件栈**（"a desktop computer"；"deep learning frameworks **such as** Tensorflow"；**实际使用的 MPC 求解器名称、容差与迭代上限**——文中只泛泛举例 SQP / 内点法及 SNOPT、IPOPT 类求解器的文献）。**影响**：23.3% 与 2.64% 的墙钟加速**不可跨机比较**，且求解容差不一致就足以吞掉这个差距。**动作**：索取 CPU/GPU 型号、框架版本、所用求解器与其容差设置、每步 NLP 的变量数与迭代次数。
4. **未报告：随机种子与训练/验证/测试划分协议**。**影响**：验证误差（1810 点自环）与性能指标方差不可复现；作者既承认初始化影响结果，又不给种子，等于放弃方差可复现性。**动作**：索取种子清单与划分代码。
5. **未报告：物理损失的消融（$\lambda=0$ 等价于普通 MLP 回归）与任何学习型基线（ESN/LSTM）**。**影响**：本文的核心动机句 "These networks … are thus not sample efficient as PINNs"（Intro）与其数据效率主张（§3.1）**没有任何同条件对照**；同样，PID、RL 基线也完全缺席。**动作**：设计 $\lambda=0$ 对照 + 同等容量的 ESN/LSTM 对照，在固定 $\mathrm{MSE}_{gen}$ 门槛下比较所需 $N_t$（**这正是 P1 的 A1 消融应当补上而本文没补的实验**）。

**B. 报告但不可核验**

6. **"up to 30% on average"（§4.3）不可核验**：Table 1 只能支持 2.64% 与 23.32%。**需要什么才能核验**：逐次运行的原始计时记录（10 次重复的每个样本）与"30%"所对应的实验标识。
7. **Fig. 5b 的 $N_f/N_t$ 结论不可核验**：热力图轴取值与单元格误差值未印出，文字叙述（"40 data points are not enough"、"proportion should be considerably higher than 4"、"hence the dark cells in the upper-right corner"）与图形语义不能对齐。**需要什么**：该图对应的数值矩阵。
8. **"延长训练使验证误差改善至少一个数量级"（§4.1.4）不可核验**：只有 Fig. 8 的对数曲线，无数字。**需要什么**：$K_2=2{,}000$ 与 $K_2=20{,}000$ 两个检查点的验证 MSE 数值。
9. **优先级主张 "the first work in the literature"（Intro (iii)）不可由本文核验**，且**作者自己在正式版新增的 Nicodemus et al. 2022（PINN-based MPC for multi-link manipulators）构成侵蚀线索**。**需要什么**：读取 VoR 全文确认该句是否被改写，并做一次针对 "PINN + MPC" 的独立检索（属 `paper-discovery` 职责）。

**C. 报告口径有歧义（两种读法导致结论如何不同）**

10. **验证集长度：905 s（§4.1.2）vs 90 s（Fig. 8 图注）**。两者相差 10 倍。若按 90 s 读，则"验证 MSE 更噪声"（Fig. 8）的解释成立且验证集极小（**泛化误差的置信区间会很宽，"PINC 与真值完全重合"的可信度下降**）；若按 905 s 读，则噪声解释不成立，Fig. 8 的波动需要另找原因。**动作**：以表/图为准并索取原始划分；引用该验证误差时必须同时声明口径。
11. **"时间"的计时边界不明**：是仅网络推理，还是含每步 NLP 求解的整段闭环？若是后者，23.3% 里混入了求解器行为（PINC 提供精确 Jacobian 会改变 NLP 的迭代路径），**不能读成"纯模型仿真更快"**。
12. **Four tanks IAE 的初值口径分裂**：Table 1（876）用初值 $(2,2)$，Fig. 15/16 用初值 $(9,9)$（作者称 9 是允许区间的中点）。**两种读法下"鲁棒性没有明显损失"的参照点完全不同**——因为 876 与直方图峰值**不是同一个工况**，而作者用后者与前者互证。**动作**：索取初值 $(9,9)$、标称参数下的 IAE 数值。

---

## 七、复用价值判断

| 问题 | 结论 |
|---|---|
| 方法可否搬到我的问题？需要改什么？ | **可搬的是"接口"与"消融纪律"，不是"物理注入方式"**。可搬：① 把网络**条件化在 $(\mathbf{y}(0),\mathbf{u})$** 上、以 $T=T_s$ 输出离散一步、自环链式生成预测时域（Eq. 6–8）——这正对应本项目架构原则"闭环用 MPC+LNN 混合（大胆决策，小心修正）"中"LNN 作 MPC 模型"的一支；② MPC 每个控制步把初状态**重置为传感器实测值**（Eq. 9、Fig. 3b），以抑制自环误差累积——P1 的 CARLA 闭环必须照此实现，否则误差累积会被误读成控制器缺陷；③ 提供 Jacobian 给 NLP 求解器（自动微分）——P1 若做 OTF-CfC + MPC，这是效率论证的落点。**必须改**：P1 的 OTF 势场不是精确 ODE（见 §十 ①），若照抄"物理残差=0"的 PINN 语义会构成**过度声称**。 |
| 评价协议可否直接对齐（指标、划分、基线）？ | **部分可对齐，且缺口正好是 P1 的强项**。可对齐：IAE/RMSE + MPC 权重/时域对称（$Q,R,N_1,N_2,N_u$ 两臂相同）+ 逐系统报告。**不可对齐**：本文无 PID、无 TD3/RL、无学习型基线、无种子、无 CI、无逐场景分解；P1 的指标集（跟车误差 RMSE、加速度平方积分、Jerk 峰值、车道居中偏差、前轮转角方差、端到端延迟、MCU 内存）与本文只有 RMSE 一项重合。若 P1 要与本文"对标"，**唯一公平的对标方式是同等信息 + 同等调参预算下的 MPC 两臂对比**，并附种子与 CI——本文两样都没有。 |
| 数据/代码可否直接取用？许可如何？ | **否**。本文**未见**代码与数据可用性声明（关键词 grep 无命中，见 §三）；训练数据是随机合成初值（无外部数据集），复现须自行实现 ODE + 采样 + NMPC 接线；四水箱参数还要回到 Johansson (2000)。版权：© 2024 Elsevier B.V.，VoR 需订阅（Crossref 仅给 TDM 链接）；本笔记所读为 arXiv 版。**不得**把本文任何数字搬进 P1 稿件作对比值。 |
| 若要引用其数字，引用时**必须**带上的限定语是什么？ | ① 全部为**低维 ODE 数值仿真**（Van der Pol 2 状态；Johansson 四水箱 4 状态/2 输入），**无实车、无实装置、无实测数据**；② 受控对象与训练所用物理**同一 ODE**（控制臂的"假想对象"由 RK4 积分同一方程），基线是**神谕** NMPC；③ 性能指标为**单次运行**，无方差、无检验；④ 加速结论只在四水箱（2400 s、单机）上量级可信，VdP 的"更快"落在噪声内，§4.3 的"30%"与 Table 1 冲突；⑤ 数字来自 **arXiv 2104.02556 版**，正式版参考文献多 9 条，表号/数值可能不同。 |

**机器可读字段（下游 `paper-experiment-analyzer` / `citation-and-related-work` 直接引用）**：

```
citation_qualifier: two low-dimensional ODE benchmarks only (Van der Pol oscillator, 2-state; Johansson four-tank, 4-state/2-input, non-minimum-phase parameters), plant simulated by RK4 of the very same ODE used for physics-informed training with zero measured data, PINC used as MPC prediction model vs oracle ODE/RK NMPC with identical Q=10I, R=I, N1=1, N2=5, Nu=N2, RMSE/IAE from a single run per system (no seeds, no variance, no significance or equivalence test), +/- reported only for wall-clock over 10 runs with SD/SE undefined, speed-up 23.3% on four-tank only (2.6% on Van der Pol, within run-to-run scatter) while the discussion's "up to 30%" conflicts with Table 1, all values from the arXiv 2104.02556 HTML version rather than the Neurocomputing 579:127419 VoR
```

---

## 八、红队三条

1. **领域最懂的人会质疑**："你把 'PINC 与 MPC 基线性能相当、还快 23%' 记成了这篇的结论，但这个基线用的是**被控对象自己的精确 ODE**——在真实控制问题里这个基线根本不存在；而且四水箱的 IAE 差了 61%，你引用的 'practically the same' 只对 Van der Pol 成立。" **需要什么证据才能消解**：① 引入一个**可实现的**基线段（同容量 ESN/LSTM 模型 + 同权重 MPC；以及 PID），证明 PINC 在同等信息与调参预算下不劣；② 给出 IAE 与 RMSE 分歧的分解（稳态误差 vs 瞬态误差），并说明哪个指标对应任务目标；③ 用 ≥5 个种子给出两臂的 mean±CI。**已落实的处置**：本条已回改 §二 第 1、2 行与 §十 ②，并把"神谕基线"写入 `citation_qualifier`。
2. **方法与统计视角会质疑**："'practically the same'、'does not lose much performance'、'slightly faster' 三条断言都没有检验、没有 CI、没有种子；Table 1 的 ± 连是 SD 还是 SE 都没说；VdP 的 0.09 s 差值小于其自身报告的 0.15 s。你凭什么给这些主张留任何强度？" **需要什么证据才能消解**：≥5 个种子（网络初始化）+ 配对比较（同一控制场景、同一初值条件）+ 预先定义的**非劣界**（例如 IAE 相对增幅 ≤5%）并做非劣检验；计时给出每样本记录与平台规格。**已落实的处置**：§二 全部经验主张压到 `C_int`，§五 第 1–3 条标为推断错误，`citation_qualifier` 明写 "no variance, no significance or equivalence test"。
3. **编辑 / 邻域读者会质疑**："缺失信息清单如果只写'未给种子'这类场面话，读者仍然不知道该不该投入复现。到底能不能复现？" **需要什么证据才能消解**：把每条缺失改成**可执行动作 + 具体后果**（已在 §六 A1–A5 逐条写成"索取 $\lambda$ / 参数表 / 平台与求解器容差 / 种子清单 / $\lambda=0$ 与 ESN 对照"），并明确"缺它则哪一张表不能重算"。**已落实的处置**：§六 三类（未报告 / 不可核验 / 口径歧义）各给出"需要什么才能核验"与"两种读法导致结论如何不同"；§三 每一项"未给出"都填了缺失影响。

---

## 九、限制

1. **材料限制（版本风险，本笔记最硬的限制）**：本笔记精读的是 **arXiv 2104.02556 HTML 版（48 条参考文献）**，而非 Neurocomputing 正式版（Crossref：57 条参考文献，PII S0925231224001905）。VoR 新增的条目中包含 **Optuna（超参数优化）**、**Xiang et al. 2022（自适应损失加权 PINN）**、**Nicodemus et al. 2022（PINN-based MPC for multi-link manipulators）** 等——分别可能补上本文缺失的"超参数搜索空间"、"$\lambda$ 取值/加权方案"，并侵蚀 Intro (iii) 的"first work"主张。因此 §三 的"超参数与搜索空间"一项、§五 第 6 条与 §二 第 13 行**须以 VoR 复核后才可作为最终结论**；表号与数值亦可能与 VoR 不同。**缓解**：入稿引用前由 `citation-and-related-work` 取 VoR 做一次逐表差异核对。
2. **复算限制**：所有数字均抄自论文印刷值，未获原始数据、代码或逐次运行记录 → 无法验证方差、异常值、统计量与图内读数；本笔记只做了**自洽性复算**（§四 末段）。凡图-only 的结论（Fig. 5a/5b/7/15）本笔记**拒绝给出估读值**。
3. **视角限制**：本笔记**不评价**该工作的**重要性**与**新颖性**（属主编视角，交 `cross-paper-synthesizer` 与 `research-gap-hunter`）；`D_int` 等级的优先级主张（§二 第 13 行）仅作为**可核验线索**记录，不作为判断。
4. **外部复现限制**：按任务要求与技能 §3.1.1，`外部复现` 列一律填"未检"，即**未做**引用网络检索。**"未检" ≠ "无独立复现"**；Crossref 的 149 次被引（索引日 2026-09-30）只是计量事实，不指示方向。若 P1 要引用本文，建议由 `paper-consensus` 补一次 `cites:` 展开。
5. **时效限制**：精读日期 **2026-10-02**；若该文已有更正/撤稿或 VoR 修订，本笔记未反映（缓解：引用前复核 DOI 状态与 VoR 版本）。
6. **ODD 迁移限制**：本文 ODD 实为"2 状态振子 + 4 状态水箱实验台"，与 P1 的 ODD（高速公路主线、多车道、人工与自动混行）无任何交集；本笔记对其结论的一切转述都不得越出该 ODD。

---

## 十、对 P1 的三条具体可用结论

### ① 该文的物理约束注入方式：**软损失项 + 输入条件化**，与 P1"把 OTF 势场作为 ODE 边界条件"**不同类**

**这篇怎么注入物理（逐条给出证据）**：

1. **物理进入损失函数，不是结构、也不是边界条件**。定义残差算子 $\mathcal{F}(\mathbf{y}):=\partial_{t}\mathbf{y}+\mathcal{N}[\mathbf{y}]$（Eq. 1–2），总损失为 $\mathrm{MSE}=\mathrm{MSE}_{y}+\lambda\cdot\mathrm{MSE}_{\mathcal{F}}$（§3.3.3），其中 $\mathrm{MSE}_{\mathcal{F}}=\frac{1}{N_y}\sum_i\frac{1}{N_{\mathcal{F}}}\sum_k|\mathcal{F}(y_i(\mathbf{v}^{k}))|^2$（Eq. 11），在**随机采样的配置点（collocation points）**上以**自动微分**计算。原文用词是 "$the\ physical\ structure\ of\ the\ solution\ is\ imposed\ by\ \mathcal{F}(\mathbf{y})\ at\ a\ finite\ set\ of\ randomly\ sampled\ collocation\ points$"（§3.1）——即**软惩罚（soft penalty）**，$\lambda$ 是"screening/rescaling factor so that both terms are approximately in the same scale"。**没有任何硬约束、没有把物理写进网络结构、没有输出变换**。
2. **"初始状态/边界"在这篇里是数据项，不是约束项**。Eq. (10) 的 $\mathrm{MSE}_{y}$ 里所有样本取 $t=0$、且目标值**等于输入初值**（$\widehat{\mathbf{y}}^{j}=\mathbf{y}^{j}(0)$），即让网络学会"在 $t=0$ 复现初值"。原文称之为 "data points that lie on the **boundary of simulations**"（§3.3.3）——指的是**仿真区间的边界（$t=0$）**，**不是 ODE 的边界条件约束**。这一处措辞极易被误读为"边界条件注入"，是本笔记要专门辟清的点。
3. **真正的结构性改动是"接口"，不是物理**：$\mathbf{y}(t)=f_{\mathbf{w}}(t,\mathbf{y}(0),\mathbf{u})$（Eq. 6）＋自环链式 $\mathbf{y}[k]=\widehat{f}_{\mathbf{w}}(\mathbf{y}[k-1],\mathbf{u}[k])$（Eq. 8）＋MPC 每步把初状态重置为实测值（Eq. 9）。控制输入被假设在区间内**恒为常数**（§3.3），物理与控制的耦合点就在这里。
4. **代价与前提**：注入强度 $\lambda$ 未给；且全文以"给定 ODE 是被控对象的精确表示"为前提（"if we assume that the given ODE is an exact representation of the process"，§3.3.3）——即**物理残差为零就是真解**，这是 Raissi 意义下严格的 physics-informed。

**与 P1 的同类性判定**：

- **不同类**。PINC 的注入是**损失层面的软约束（残差惩罚 + 配置点采样）**；P1 声称的是**把 OTF 势场作为 ODE 边界条件注入 CfC**，那属于**闭式解/结构层面的硬约束**（先验直接决定 ODE 解的形式与定解条件）。两者的**相同点仅有一层**：都不把先验留给数据去学，而是"先把已知模型放进学习问题"。
- **更重要的语义差别（对写作直接有用）**：PINC 里的 $\mathcal{F}$ 是**第一性原理方程**，"物理"有"残差=0 即真解"的地位；**OTF 势场是建模先验/社会压力启发式场，不存在可判真伪的残差方程**。因此 P1 **不宜**把 OTF 项称为 "physics-informed"（会被审稿人按 Raissi 语义追问"你的物理定律是什么、残差如何定义"）；建议用 **structure-informed / prior-informed / boundary-conditioned** 一类表述，并把 OTF 项定位为**归纳偏置（inductive bias）**而非物理定律。这一条与 `AGENTS.md` §1"若不显著，卖点改为可解释性 + 零额外传感器成本"是一致的措辞出口。
- **可直接搬用的两条**：① **接口设计**（$(\mathbf{y}(0),\mathbf{u})$ 条件化 + $T=T_s$ 一步输出 + 自环生成预测时域 + 每步用实测状态重置）；② **本文缺失、P1 必须补的消融**——PINC 从未做 $\lambda=0$ 对照，因此它那句 "training data size … drastically reduced" 严格来说是**无证据的**（§二 第 5 行，判 `D_int`）。P1 的 A1 消融（OTF 项开/关）恰好就是这个对照，**做出来就是相对本文的净增量**。

### ② 控制基线：**有 MPC（但是"神谕"基线），没有经典 PID；公平性是"控制器参数对称、信息不对称"**

- **有 MPC**：基线为 NMPC，其预测模型是**被控对象自身的精确 ODE**，数值解用 RK4（§4.1.4："the classic, fourth-order Runge-Kutta method (RK4) is employed as a numerical solution method"；§4.2.2："This ODE/RK-based model is the reference model that represent the plant itself"）。作者为选它给的理由是 "practically other approximations to the plant/system are not likely to improve the ODE model itself, thus, justifying our comparison to the baseline NMPC"——**这是"上界基线"逻辑：赢不了神谕是正常的，追平神谕即算成功**。
- **没有经典 PID**：全文只有一处提到 PID，且**不是作为实验基线**——§4.2.1 引 Johansson (2000) 说明四水箱可被调成非最小相位，"which are an additional difficulty for PID controllers"。**因此 P1 不能引用本文支持任何"神经网络控制优于 PID"的说法**；P1 的 PID 基线只能由 P1 自己做（`AGENTS.md` §3 已列）。
- **对比的公平性（逐项）**：
  - **同等控制调参预算：满足**。两臂使用**完全相同**的控制参数 $N_1=1,\ N_2=5,\ N_u=N_2,\ Q=10\mathbf{I},\ R=\mathbf{I}$，且两套系统共用同一组（§4.1.4、§4.2.2）——这一点是可以直接对齐到 P1 的做法的。
  - **同等可用信息：不满足，且方向对 PINC 有利**。基线额外拥有**精确模型**这一特权信息（等价于 P1 里给 MPC 一辆真值车辆模型）。所以"追平神谕"是**有利于 PINC 的结果方向**，但**不能**反过来说"PINC 打败了任何可实现的方法"。
  - **同等求解/计算预算：未证明**。求解器名称、容差、迭代上限、每步 NLP 规模全未报告（§三），而 PINC 的接口能提供解析 Jacobian（$\partial\widehat{f}_{\mathbf{w}}/\partial\mathbf{u}$，§3.3.2）——**计时差异里混着求解器行为**，不能读成纯模型代价。
  - **对照族缺失**：无 PID、无 RL/TD3、也无任何**学习型模型**基线——尽管本文的样本效率动机句正是针对它们（Intro："These networks are trained exclusively on data collected from the process and are thus not sample efficient as PINNs"），而被针对的 ESN（Jordanou et al., 2021/2022）与 LSTM（Terzi et al., 2020）**都只出现在参考文献里**。即：**跨族比较的结论缺同条件实验**。
  - **对象-模型同源**：控制实验的"plant"就是训练 PINC 所依据的同一 ODE（VdP 由 RK 积分产生状态）→ **模型失配 = 0**（仅 ±5% 参数扰动实验例外）。P1 的 CARLA/实车回放里模型失配是主导误差源，**不可照搬这一对比结构**。
- **对 P1 的净结论**：可借鉴的是**两臂对称的 MPC 参数设置**与**"上界基线"式论证框架**；不可借鉴的是"只有神谕基线就足够"这一样本选择——P1 必须补齐 PID 与 TD3（按 `AGENTS.md` §3 的四条基线）并给出种子与 CI，否则 P1 的公平性论证会比本文更弱。

### ③ 仿真 vs 真实系统：**这篇 100% 是低维 ODE 数值仿真，零实装置、零实测数据；比 P1 的 CARLA 更靠前**

- **所谓"plant"就是数值积分器**：VdP——"the role of the plant to be controlled is taken by the Van der Pol oscillator, whose states are obtained by an RK integrator"（§4.1.4）；四水箱——以"the plant reference model"作对照（§4.2.2、Fig. 14）。
- **训练数据里没有任何实测样本**（这是本文的卖点，也同时是它的边界）：$t=0$ 的初值-控制对全部随机合成，"Practically, this does not require collecting data from ODE simulators"（§3.3.3）。**没有传感器噪声、没有采样抖动、没有时延、没有执行器饱和/限幅建模、没有通信或算力约束**。
- **所谓"鲁棒性"是同一 ODE 的 ±5% 乘性参数扰动与 ±5% 初值扰动**（$k_1,k_2\sim U_{5\%}$，151 次/直方图，§4.2.3）——**是参数不确定性，不是未建模动态**；而且作者明确声明该框架**没有**扰动抑制机制（"does not have an inherent method to deal with modeling errors and completely reject disturbances"），并因**无积分作用**而预期存在稳态误差（§4.2.3）。
- **计时是桌面机，不是实时硬件**：Table 1 的"time (s)"是"the complete control simulation"在 "a desktop computer" 上的墙钟（平台未指明）。**没有任何嵌入式/实时性证据**（对照 P1 需报端到端延迟与 MCU 内存占用，`AGENTS.md` §3）。
- **对 P1 的边界含义**：① **不可**用本文支撑"仿真结论可迁移到实车"——本文连高保真仿真都没有，只有 2 状态与 4 状态 ODE；② P1 现有的 CARLA 闭环 + 实车数据回放，在证据阶梯上**高于**本文，但依 `AGENTS.md` §1 第 2 条，其措辞上限仍是"**在 CARLA 与真实数据回放中**"，绝不能写成实车验证；③ 本文的"敏感性分析"是 P1 可以低成本模仿的形式（扰动注入 + 多次运行 + 分布呈现），但必须**先定义可接受容差、报均值与区间、并与未扰动基线配对比较**——本文这三样都缺（§五 第 5 条）。
