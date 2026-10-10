# 精读笔记 #43：Dissipation of stop-and-go waves via control of autonomous vehicles: Field experiments

- **文献**：Stern RE, Cui S, Delle Monache ML, Bhadani R, Bunting M, Churchill M, Hamilton N, Haulcy R, Pohlmann H, Wu F, Piccoli B, Seibold J, Sprinkle J, Work DB. "Dissipation of stop-and-go waves via control of autonomous vehicles: Field experiments." *Transportation Research Part C: Emerging Technologies* 2018;89:205–221. DOI 10.1016/j.trc.2018.02.005
- **精读日期**：2026-10-02 ｜ **全文来源**：已获全文（纯文本，`literature/fulltext/p43-dissipation-trc2018.txt`，72,719 字节 / 1,301 行）
- **抓取来源**：`https://arxiv.org/html/1705.01693`（arXiv HTML 版，FETCH_DATE 2026-10-02）。**并未获取 TRC 正式版 PDF** → 凡"arXiv 版与正式版可能存在的差异"一律标 `[待核实]`（见 §九 限制 1）。
- **技能**：`deep-paper-reader`（v1.0）｜**产物类型**：逐节精读台账，供审稿人/下游技能直接使用

---

## 作用域

**场景①：项目内文献工作**（`deep-paper-reader` §1 前置条件二）。

- **项目**：`D:\Deepseek Harness\auto-driving`（自动驾驶 OTF 论文集群，主课题"自动驾驶"下的独立项目）。
- **项目不变量文件**：`D:\Deepseek Harness\auto-driving\AGENTS.md`。本笔记全部结论受其 §1「主张上限」硬约束。
- **本次精读服务的主张**：论文 1（P1，代号 **OTF-CfC**）「基于超车频次势场与液态神经网络的高速主线编队连续时间控制」。
- **P1 主张上限（项目 `AGENTS.md` §1 逐条显式引用，本笔记不得越界）**：
  1. **不得预先声称"OTF 势场带来 X% 性能提升"**。学位论文报告的分类器准确率增益 **+1.0 ~ +5.5 个百分点**（SVM +2.23~+3.60／LSTM +2.23~+5.46／Bi-LSTM +1.00~+1.73；**分类器准确率，论文报告值，未经我们复现**），在 LNN 控制范式下**未经本项目实测即属 C/D 级证据**。
  2. **不得把仿真/回放写成实车验证**：CARLA（Town04）与实车数据回放都是仿真或开环证据；未做真车闭环前措辞上限是"在 CARLA 与真实数据回放中"。
  3. **不得直接搬用他人论文数字**：未同协议复现的对比必须标注"**文献报告值，协议不同，不可直接比较**"。
- **本笔记对 P1 的作用**：P1「少量自动车即可消散拥堵波」这一**场景动机**的最强实证来源。因此本笔记在 §二/§四/§五 之外，单列 **§十**，把"能否引 / 引用时必须带什么限定语 / 它没证明什么"写成 P1 可直接落笔的三条结论。
- **本文对该主张的证据地位（在 P1 稿件中的定位）**：**文献报告值，协议不同，不可直接比较**。本文是**封闭环形试验场真车实验**（field experiment，非仿真），其"真车"地位成立；但其道路类型（单车道环形）、车队规模（21–22 辆）、控制律（FollowerStopper / PI-with-saturation）与 P1 的 ODD（高速公路主线、多车道、混行）**均不同**，故 P1 只能引其**方向性结论**，**不得**把其百分比搬到 P1 的性能表格里做横向对比。

> 本笔记不评价该工作的**重要性**与**新颖性**（该视角属 `cross-paper-synthesizer` / `research-gap-hunter`）。

---

## 一、作者主张

作者主张：在一条单车道环形赛道上（车道中心半径 41.4 m、周长 260 m），用 21–22 辆乘用车、由经过安全驾驶培训但无特殊驾驶训练的大学雇员驾驶、按"跟紧前车"的指令行驶时，**拥堵波（stop-and-go waves）会在没有任何几何瓶颈、车道变换或匝道触发的情况下自发出现**（Appendix 5.2 用"瞬时速度标准差 > 2.5 m/s"作为波判据）；而只要把车队中**唯一一辆**可自动控制纵向速度的车辆（University of Arizona CAT Vehicle，方向盘始终由受训驾驶员握持）切换为波消散控制器，波就能被显著削弱，并伴随速度标准差、过量制动事件率与油耗的下降，吞吐量在部分实验中上升。作者给出的三种波浪消散实现分别是：(A) FollowerStopper——在 Δx–Δv 相平面上按抛物线边界分区、需外部给定期望速度 U 的控制器；(B) 由受训人类驾驶员手工复现同一"维持平均速度"策略；(C) PI with saturation——**完全自动、不需要任何外部输入**，用车辆自身过去 38 s（约一圈）速度的滑动平均来在线估计期望速度 U，并在小间距与车间距过大两侧做饱和的控制器。作者据此主张：交通流控制可以通过**极稀疏的"拉格朗日执行器"（Lagrangian actuators）**实现，摘要中进一步外推为"**less than 5%** 的移动执行器即可实现流量控制，远早于多数车辆具备自动驾驶能力"，并把该结果定位为相对于匝道控制（ramp metering）与可变限速（VSL）等固定位置/集中式控制的**范式转变**。作者自认的边界是：环形实验只代表单车道路段，多车道干道的效益"还需未来的多车道实验才能完整量化"。

---

## 二、主张—证据台账

**双口径评级**（`deep-paper-reader` §3.1.1）：`内部等级` = 仅凭本文内部证据（无 CI、无重复运行、无预注册者，**最高 B_int**）；`外部复现` = 本次**未做任何外部检索**，故**一律填"未检"**——"未检"是信息缺失，**不等于**"无外部证据"，也不得据此把本文说成"仅一次性证据"。

| # | 作者主张（英文原句） | 支撑证据（图/表/统计量） | 内部等级 | 外部复现 | 是否被结果支撑 | 缺口 |
|---|---|---|---|---|---|---|
| 1 | "we demonstrate experimentally that intelligent control of an autonomous vehicle is able to dampen stop-and-go waves that can arise even in the absence of geometric or lane changing triggers."（Abstract） | Table 3（A: σ 3.31→0.64 m/s；B: 2.36→1.19；C: 3.85→1.74）；Figure 3(b)/4(b)/5(b) 速度剖面；§2.2 "Traffic waves appear in all experiments" | **B_int** | 未检 | 是（方向） | 3 次实验各 1 次运行、同一场地、同一密度档；"best interval" 事后择优；无 CI。方向在 3 个不同控制器/车队条件下一致，故方向给 B_int，幅度另见 #5–#8 |
| 2 | "our experiments on a circular track with more than 20 vehicles show that traffic waves emerge consistently"（Abstract） | Appendix 5.2 判据：瞬时速度标准差 > 2.5 m/s 记为有波；Figure 6(a)(b)(c)；波起始时刻 A=79 s、B=55 s、C=161 s（§4.2、Table 1/2/4） | **B_int**（限"这 3 次运行"）／**C_int**（若读作"普遍地一致出现"） | 未检 | 部分 | **"consistently" = n=3，全部同一赛道、同一密度（≈81–85 veh/km）、全部由大学雇员驾驶**；无不同密度、不同车队规模、不同场地的重复。另见表注冲突：B 的"Waves start" 区间 σ=2.36 m/s **低于** 2.5 m/s 判据（见 §五 旗标 S6） |
| 3 | "flow control will be possible via a few mobile actuators (less than 5%) long before a majority of vehicles have autonomous capabilities."（Abstract） | 实验事实：A/B 为 21 辆中控制 1 辆 = 4.8%；C 为 22 辆中控制 1 辆 = 4.5%（§2.1、§4.2） | **C_int** | 未检 | 部分 | **只测了 1 个执行器**，未做渗透率扫描（1 辆 / 2 辆 / 3 辆…）；"a few"（复数）"will be possible"（将来时）是从**单个执行器**外推；结论句本身用的是推测语气，不得当作实测结论引用 |
| 4 | "A single autonomous vehicle can control the flow of at least 20 human-controlled vehicles around it, with substantial reductions in velocity standard deviation, excessive braking, and fuel consumption."（§5 Conclusions） | Exp A/B: 21 辆 = 1 AV + 20 人工驾驶；Exp C: 22 辆 = 1 AV + 21 人工驾驶；Table 3 四项指标均改善或基本持平 | **B_int** | 未检 | 是 | 仅在**单车道环道、260 m、≈81–85 veh/km**这一个密度—几何点上验证；"control the flow" 未给出控制性能的稳定性/鲁棒性判据 |
| 5 | "Compared to when waves are present, the Lagrangian control results in up to 40% less fuel consumption"（§1.2） | Table 3：A −42.5%、B −22.1%、C −28.1%（单位 ℓ/100km，区间为 spatio-temporal 平均瞬时油耗率） | **C_int** | 未检 | **与表冲突** | §1.2 写 "up to 40%"，Table 3 的 A 为 42.5% → **正文低估表格值**；本笔记按 `deep-paper-reader` §3.3 硬规则**以表为准**。"up to" = 事后择优区间；无 CI；油耗为 OBD-II 瞬时油耗率，非油量/CO₂ 计量 |
| 6 | "the velocity standard deviation is reduced by 80.8%, the fuel consumption is reduced by 42.5%, and the excessive braking events are reduced from 8.58 events per vehicle per kilometer to 0.12 events per vehicle per kilometer."（§4.2, Experiment A） | Table 1（79 s 区间 vs 292 s 区间）；Table 3 行 A | **C_int** | 未检 | 是（数值可复算） | 3.31→0.64 = −80.7%（报告 −80.8%，舍入内）；24.6→14.1 = **−42.7%**（报告 −42.5%，**用打印值无法精确复算**，未印出未舍入值）；8.58→0.12 = −98.6% ✓；A 的"best interval" 是在 **6 个受控区间中事后挑出**的一个 |
| 7 | "The improvements include a reduction of 42.5%, 22.1%, and 28.1% in Experiments A, B, and C, respectively."（§4.2 小结，油耗） | Table 3 行 A/B/C 的 Fuel consumption 列 | **C_int** | 未检 | 是（B、C 可复算） | B: 21.8→17.0 = −22.0%（报告 −22.1%）✓；C: 29.0→20.9 = −27.9%（报告 −28.1%，且 §4.2 正文 line 604 亦写 **27.9%**）→ **正文与表格在 C 上再冲突**（−27.9% vs −28.1%） |
| 8 | "Velocity standard deviation: The velocity standard deviation is reduced in all experiments, ranging between 49.5% for Experiment B, 54.7% for Experiment C, and a high of 80.8% for Experiment A."（§4.2 小结） | Table 3 行 A/B/C 的 Velocity st. dev. 列 | **B_int**（方向）／**C_int**（幅度） | 未检 | 是（可复算） | 三个方向一致是本条最强之处；但每个实验只跑了 1 次、每个实验只有一个受控车队规模，**幅度**为单次运行的事后最优区间 |
| 9 | "Changes in throughput for each experiment are +14.1% for Experiment A, and +9.8% for Experiment B, with a −2.5% change in Experiment C."（§4.2 小结） | Table 3 行 A/B/C 的 Throughput 列（veh/hr） | **C_int** | 未检 | 是（可复算） | **口径警告**：本文的 throughput 定义为 `q = (n/L)·v̄`（§4.1），即"密度 × 平均速度"的**导出量**，环道上 n/L 恒定 → 吞吐量变化与平均速度变化**在数学上同一件事**，不是独立测量的过车计数。**C 实验吞吐量下降 −2.5% 与"控制有效"并存**，属本文自认的代价（§4.2：该控制器"slightly reduces the average velocity"） |
| 10 | "the excessive braking events are reduced from 8.58 to 9.66 excessive braking events/veh/km down to 2.47 events/veh/km"（§4.2 小结） | Table 3 行 A/B/C 的 Braking 列：8.58/9.50/9.66 → 0.12/2.27/2.47 | **C_int** | 未检 | 是（可复算） | 该句本身表述混乱（把 A、C 的基线并列）。更关键：制动事件阈值 τ 定义为"**未控波期**所有车辆减速度标准差的平均"（§4.1），**τ 是逐实验各算各的** → 三个实验的 events/veh/km **不在同一标尺上**，不可跨实验比较；τ 的数值本身**未印出** |
| 11 | "The PI with saturation controller (Experiment C) is a fully automatic control, while the FollowerStopper (Experiment A) and the human-implemented control (Experiment B) have an external input (dependent on observed traffic conditions)."（§5） | §3.1（FollowerStopper 需给定 U）、§3.2 Eq.(3)(5)（U = 自身速度 38 s 滑动平均；g_l=7 m、g_u=30 m、v_catch=1 m/s、γ=2 m、Δx^s=max(2s·Δv, 4 m)）、§2.2 "For some controllers, a desired average velocity is communicated from an external observer." | **B_int** | 未检 | 是 | 控制律形式与参数给出较完整（见 §三 第 4 项）；但**底层 PID 的增益未给出**（只说"经系统辨识确定"），CAT Vehicle 的**车间距传感器型号未给出** |
| 12 | "these benefits can be achieved via structurally very simple control strategies, based only on the AV's velocity, its spatial gap between the vehicle immediately in front, and some estimate of the average velocity of traffic flow."（§5） | §3 全文；Eq.(1)–(5) | **C_int** | 未检 | 部分 | "some estimate of the average velocity of traffic flow" 在 A、B 中其实是**由外部观察者提供**的（§2.2、§4.2），并非车辆自估计；只有 C 是自估计。"只用车自身可得信息"这一强表述**只对 Experiment C 成立** |
| 13 | "This simple structure implies that a noticeable impact on congested traffic flow can in principle be achieved by means of adaptive cruise control systems that are already in place in certain new vehicles"（§5） | 无实验；仅为论证性推断 | **D_int** | 未检 | 否（无证据） | 未测试任何量产 ACC；未考虑量产 ACC 的感知/执行限制与法规约束。属推测级断言，出现在 Conclusions 中 |
| 14 | "The presented ring experiments represent a stretch of single-lane roadway. However, the theory extends also to multi-lane freeways… To fully quantify the benefits of Lagrangian actuators on urban freeways, future multi-lane experiments are needed."（§5） | 无多车道实验；作者自认 | **D_int** | 未检 | 否（明示为未来工作） | 多车道、换道触发波、匝道、交叉口**一概未测**；P1 的 ODD 恰好落在未测区间 |
| 15 | "The FollowerStopper controller is deactivated after 463 seconds, and the traffic wave reappears."（§4.2）；"Once the CAT Vehicle returns to a typical gap closing behavior …, the traffic wave reappears"（§4.2） | Table 1 行 "Disable Autonomy"（463 s）：σ 1.44 m/s、制动 2.95、油耗 17.4 ℓ/100km、吞吐 **2133 veh/hr**；Table 2 行 "Disable control"（300 s）：σ 2.25 m/s、制动 9.43、吞吐 1908 | **B_int**（作为 on/off 反转的内部对照，是本文设计上最有力的部分） | 未检 | 部分 | **两处内在张力**：① 按 Appendix 5.2 的 2.5 m/s 判据，A 的 463 s 区间（σ=1.44）**并未判定为"有波"**，与正文"wave reappears"措辞不符；B 的 300 s 区间（σ=2.25）同样低于 2.5；② A 的 463 s 区间吞吐量 **2133 veh/hr 是全实验最高**，高于受控最优区间的 2085 → 若以吞吐为唯一判据，"关闭控制"反而更好。该反转在**速度方差与制动率**上支持作者主张，在**吞吐量**上不支持 |
| 16 | 隐含主张：报告的百分比变化是精确点估计（全文未给任何不确定度） | Table 1–4 只有点值；全文无 CI、无 SE、无 p 值、无效应量区间、无等价检验；唯一的离散度指标 σ 是**跨车速度标准差**（交通状态量），**不是效应量的不确定度** | **D_int** | 未检 | 否（无证据） | 见 §五 旗标 S1–S3。任何"X% 提升/降低"的引用都必须自带"单次运行、无 CI"的限定语 |

---

## 三、方法可复现性清单

| 项 | 论文是否给出 | 具体位置 | 缺失影响 |
|---|---|---|---|
| **数据来源与版本** | 部分给出 | §2.1（360° 中心相机视频 + OBD-II 数据记录器）；§4.2 "The full data set and code used to generate the plots can be found in [67]"；[67] = `https://uofi.box.com/v/trajectoryPaperData` (2016)；Movie S1 为 Exp A 视频 | 未给数据集版本号、文件清单、许可条款。→ 无法确认可否再分发或用于 P1 的对比复现；BOX 分享链接的存活状态与正式版 TRC 的数据声明是否相同 **未核** |
| **预处理与划分方式** | 部分给出 | §2.1/§4.2：相机视频经计算机视觉提取每辆车中心 → 平滑 → 轨迹；速度、加速度由位移**离散差分**得到 [61]；与 CAT Vehicle 控制计算机和车载设备交叉验证；区间由 "Notable events" 人工界定 | 未给 CV 跟踪算法与失败帧处理、未给平滑滤波类型与截止频率、未给差分步长、未给区间边界的客观规则（"notable events" 由作者判定）。→ σ、加速度、jerk、制动事件计数对这些选择都敏感，**外部无法独立复算** |
| **模型/实验装置规格** | 给出较多（但有硬缺口） | **赛道**：单车道环形，车道中心半径 41.4 m，周长 260 m，逆时针；沥青路面 + 小锥桶标记，3 cm 橙色内侧指示物，近乎平坦无标线/灯柱/障碍（§2.1）。**车辆数**：Exp A = 21、Exp B = 21、Exp C = 22（§2.1、§4.2）。**车队规格**：Table 5 逐辆给出年份/厂牌/型号/车长/EPA 城市与高速油耗（22 辆；车长 4.44–5.70 m；EPA 城市 6.92–15.67 ℓ/100km，高速 6.37–10.68 ℓ/100km；构成为 Malibu ×9、Grand Caravan ×7、Silverado ×2、Suburban ×2、Impala ×1、Ford Escape Hybrid ×1）。**AV 平台**：University of Arizona "Cognitive and Autonomous Test (CAT) Vehicle"，可在手动与自动速度控制间切换，方向盘**始终**由受训驾驶员握持（§2.1、§3.4）。**采样率**：车间距 30 Hz（§3）、底层控制 20 Hz（§3.3）。**绕圈周期**：≈38 s（§3.2，作为 PI 平均窗长） | **硬缺口**：① 22 辆车中**哪一辆是 CAT Vehicle 未标明**，其年份/厂牌/型号亦未在 Table 5 中指出；② 车间距 Δx 的**传感器类型、量程、精度、安装位置全未给出**（只说"measures … at a sampling rate of 30Hz"）；③ 赛道所在地、试验日期/季节/时段、天气与光照未给；④ 路面摩擦、轮胎状态未给。→ 无法评估感知噪声对控制器的影响，也无法做 sim-to-real 差距分析 |
| **超参数与搜索空间** | 参数值给出，**搜索空间未给出** | **FollowerStopper**（Eq.1–2）：Δx₁⁰=4.5 m、Δx₂⁰=5.25 m、Δx₃⁰=6.0 m；d₁=1.5、d₂=1.0、d₃=0.5 m/s²；Δv₋=min(Δv,0)（§3.1）。**PI with saturation**（Eq.3–5）：U=自身速度 m 点滑动平均，m 对应 **38 s**；g_l=7 m、g_u=30 m、v^catch=1 m/s；γ=2 m；Δx^s = max(2 s × Δv, 4 m)；β=1−α/2（§3.2）。**底层多模态 PID**（§3.3）：切换阈值 v^cmd−v ≤ −0.25 m/s 时用制动模式 h₂，否则 h₁；输出 a ∈ [−100, 100] | 未给超参的目标函数、网格/搜索范围、被淘汰的候选参数，也未给**底层 PID 的具体增益**（只说"经 CAT Vehicle 在实验代表速度下的系统辨识确定"）。→ 无法判断参数是否接近最优、**无法判断换到另一种密度/车队规模是否需要重调** → 直接限制外推 |
| **随机种子 / 重复次数** | **均未报告** | 每个实验各运行 **1 次**：Exp A 567 s、Exp B 409 s、Exp C 413 s（§4.2）；§2.2 "Each experiment lasts between 7–10 minutes"；全文无种子、无重复、无重复次数说明 | 这是本文最重要的缺失。非随机化设计（无种子概念），且**每个条件 n=1**。→ 无法估计 run-to-run 变异；"up to 40%" 的分母是单次运行内的单一时间区间；"wave emerges consistently" 实际是 3 次运行全部出现 |
| **评价指标定义（含边界情况）** | 给出较完整，边界有歧义 | §4.1 全部给出解析定义：空间平均速度 v̄_j = (1/n)Σv^i_j；时空平均 v̄、σ = [ΣΣ(v−v̄)²/(mn−1)]^{1/2}；油耗 c̄（时空平均瞬时油耗率）；吞吐 **q = (n/L)·v̄**，L=260 m；制动事件率 **κ = (1/n)Σ ρ_τ(a)/(x_m−x_1)**，ρ_τ 为减速度峰值计数，**τ = 未控波期所有车辆减速度标准差的平均**。波判据（Appendix 5.2）：瞬时速度标准差 > **2.5 m/s** | ① **τ 的具体数值未印出** → 无法复算 κ；② q 是密度×均速的导出量、非实测计数（见 §二 #9）；③ τ 逐实验各算 → 跨实验制动率不同标尺；④ **判据与表格口径不一致**：波判据用"瞬时 σ > 2.5"，而 Table 1–4 报的是"区间平均 σ"，B 的波起始区间均值 2.36 < 2.5（见 §五 S6） |
| **基线实现来源** | 基线为"同一实验内的未控/波期区间"，**无外部控制器基线** | §4.2 全部比较都是 within-experiment：Exp A 的 79 s（波期）vs 292 s（最优受控区间）；B 的 55 s vs 202 s；C 的 161 s vs 218 s | 没有 PID / MPC / ACC / VSL 等**独立实现的控制器基线**；A/B/C 三者互为参照但**车辆数、控制器结构、是否有人类驾驶员同时变化**，不是受控对比。→ 只能说"该控制律在本条件下相对'无控制'有效"，**不能说**它优于任何其它控制律 |
| **显著性检验方法** | **未报告** | 全文无假设检验、无 p 值、无置信区间、无等价/非劣检验、无效应量区间 | → 所有百分比均为**无不确定度的点估计**；"up to X%" 与 "best interval" 属事后择优（见 §五 S2），乐观偏倚方向已知、幅度未知 |
| **代码/数据可用性声明** | 给出（简略） | §4.2 → [67] `https://uofi.box.com/v/trajectoryPaperData` (2016)；补充材料 Movie S1（Exp A 视频） | 无版本号/无许可声明/无 README 说明；链接为 2016 年 box 分享，**存活与许可未核**。→ 入稿引用前须由 `citation-and-related-work` 复核；在许可明确前**不得**假定可再分发 |

**额外（P1 特别关注）：实验伦理与安全安排——本文报告了什么、没报告什么**

| 项目 | 本文是否报告 | 原文/位置 |
|---|---|---|
| 安全员 / 方向盘值守 | **报告** | "A trained human driver controls the steering wheel of the CAT Vehicle **at all times** during all experiments."（§2.1） |
| 安全员能否越权接管油门/刹车 | **未报告** | 全文未说明自动化纵向控制期间驾驶员是否有 brake/throttle override；仅 §3.4 说明 Exp B 由该驾驶员直接控速 |
| 驾驶人来源与资质 | **报告** | "All other vehicles are driven by University of Arizona employees that have completed **safe driver training** but received no other special driving training."（§2.1）；Exp B 的控制驾驶员"received training from the University of Arizona on safe driving of high-occupancy vehicles, and had **extensive practice**"（§3.4） |
| 知情同意 / IRB / 人体受试者审批 | **未报告** | 全文（含致谢、附录）无 IRB、consent、human-subjects 相关表述 |
| 区域许可 / 试验场授权 / 保险责任 | **未报告** | 全文无 permit / authorization / insurance 表述。可推断为自有封闭试验场（车辆由 University of Arizona Motor Pool 提供，见 Acknowledgements），但**未明示** |
| 里程 / 暴露量 | **未报告** | 全文无里程或暴露量数字。可得的替代口径仅为**时长**：§2.2 "Each experiment lasts between 7–10 minutes to limit driver fatigue"；三次实验实际时长 A 567 s + B 409 s + C 413 s = 1,389 s ≈ **23.2 min**（本笔记由 §4.2 相加，**非论文报告值**） |
| 接管/干预次数与分母 | **未报告** | 全文无 disengagement / intervention / takeover 计数，**无任何分母**（每公里或每次干预机会均无）。仅报告**计划内的模式切换时刻**：A 在 126 s 激活、463 s 停用；B 在 112 s 由驾驶员接管控速、300 s 恢复常规跟车；C 在 218 s 激活（§4.2） |
| 异常/紧急处置协议 | **报告** | "In the event of an unsafe scenario, the drivers are instructed to **steer out of the circle**, at which the experiment coordinator will sound the air horn and the experiment will stop."（§2.2）；并要求 CAT 车后车"drive as if the CAT Vehicle were in the same lane"，CAT 车"will be driving at a **larger radius (1/2 vehicle width)** to facilitate evasive emergency maneuvers"（§2.2） |
| 人员与赛道隔离 | **报告** | 每次实验设 "Evacuation" 阶段："All research team personnel evacuate the track."；"Experiment personnel enter the track after all vehicles have stopped."（§2.2） |
| 疲劳管理 | **报告** | 实验时长限制在 7–10 min（§2.2） |
| 参与者是否被告知 AV 模式 | **报告** | "All drivers are instructed that the CAT Vehicle would be switching back and forth between autonomous and manual mode, and that they should focus on their driving rather than attempting to guess what mode the vehicle is in at any given time."（§2.2） |
| 驾驶员行为指令（防污染） | **报告（且是关键设计）** | 逐字给出指令："Drive as if you were in rush hour traffic. Follow the vehicle ahead without falling behind. Do not pass the car ahead. Do not hit the car ahead. Drive safely at all times. Do not tailgate. But put an emphasis on catching up to the vehicle ahead, if a gap starts opening up."；明示目的是 "to explicitly prevent the human drivers from intentionally smoothing out traffic waves themselves"（§2.2） |
| 随机化 | **无（未报告任何随机化）** | 三次实验的控制器/条件由作者指定；控制器的**开/关顺序固定为"先波后控"**，未随机化开关顺序；未设对照实验（如"受控车保持人类驾驶"的同长运行） |
| 资金 | **报告** | NSF CNS-1446715 (B.P.)、CNS-1446690 (B.S.)、CNS-1446435 (J.S.)、CNS-1446702 (D.W.)；车辆由 University of Arizona Motor Pool 提供 |

---

## 四、关键数字表

> 硬规则（`deep-paper-reader` §3.3）：只抄论文**明确印出**的数字；**Table 1–4 中的 σ 是"跨车速度标准差"这一交通状态量，不是效应量的不确定度**，不得当作误差棒引用。所有效应量百分比**论文均未给任何不确定度**（见 §五 S1）。

| 指标 | 值 | 不确定度 | 出处（表/图/节） | 备注（哪个实验、哪个设置） |
|---|---|---|---|---|
| 赛道：车道中心半径 / 周长 | 41.4 m / 260 m | 未报告 | §2.1 | 单车道环形赛道，逆时针，沥青，锥桶标记 |
| 车队规模 | 21 辆（Exp A）、21 辆（Exp B）、22 辆（Exp C） | 未报告 | §2.1、§4.2 | "The experiments … with 21 to 22 vehicles depending on the experiment" |
| 受控车辆数 | **1 辆**（全程只控制 1 辆） | 未报告 | §2.1 "only one vehicle is ever controlled" | AV 方向盘始终由受训驾驶员握持 |
| 自动化比例（渗透率） | 1/21 = **4.8%**（A、B）；1/22 = **4.5%**（C） | 未报告 | 由 §2.1/§4.2 计算 | 本笔记由"1 辆受控 / 21 或 22 辆"直接算得；论文摘要只写 "less than 5%" |
| 平均车辆长度（Table 5） | 5.06 m | 未报告 | 本笔记由 Table 5 计算（**推算值**） | 22 辆样本；车长范围 4.44–5.70 m |
| 均匀排列时的车头间距（推算） | ≈12.4 m（21 辆）/ ≈11.8 m（22 辆） | — | 本笔记推算（**非论文报告值**） | 260 m ÷ 21 或 22；对应车头时距 ≈1.9–2.0 s（@6.3 m/s） |
| **速度标准差 σ（波期基线 → 最优受控）** | A: 3.31 → 0.64 m/s（**−80.8%**）；B: 2.36 → 1.19（**−49.5%**）；C: 3.85 → 1.74（**−54.7%**） | **未报告**（无 CI/SE） | Table 3（WS/CA 列）+ Table 1/2/4 | σ 口径 = 时空平均跨车速度标准差（§4.1） |
| 波期 σ 的增幅（Exp C，无控平稳期 → 波期） | **+37.7%**（论文原文） | 未报告 | §4.2 正文（line 561） | **复算不符**：由 Table 4 的 1.62 → 3.85 得 **+137.7%**。同句的油耗 +63.8% 与吞吐 −18.8% 均由 Table 4 复算通过 → 疑为 "137.7" 漏印首位 "1"（见 §五 S7） |
| **油耗（ℓ/100km，波期 → 最优受控）** | A: 24.6 → 14.1（**−42.5%**，原始精度 14.13）；B: 21.8 → 17.0（**−22.1%**）；C: 29.0 → 20.9（**−28.1%**） | **未报告** | Table 3 + Table 1（A 最优区间 7.50 m/s 行，含 14.13） | 口径 = 全车时空平均**瞬时油耗率**（OBD-II），非总油量 |
| **过量制动事件率（events/veh/km，波期 → 最优受控）** | A: 8.58 → 0.12（**−98.6%**）；B: 9.50 → 2.27（**−76.2%**）；C: 9.66 → 2.47（**−74.4%**） | **未报告** | Table 3 + Table 1/2/4 | 阈值 τ **逐实验不同且数值未印出** → 跨实验不可比 |
| **吞吐量（veh/hr，波期 → 最优受控）** | A: 1827 → 2085（**+14.1%**）；B: 1828 → 2008（**+9.8%**）；C: 1755 → 1711（**−2.5%**） | **未报告** | Table 3 + Table 1/2/4 | q = (n/L)·v̄，L=260 m → 吞吐量与平均速度**同义**，非独立计数 |
| 实验时长 | A 567 s、B 409 s、C 413 s；单次设计 7–10 min | 未报告 | §4.2、§2.2 | 合计 ≈23.2 min（本笔记相加） |
| 波首次出现时刻 | A 79 s、B 55 s、C 161 s | 未报告 | §4.2、Table 1/2/4 | 判据：瞬时速度标准差 > 2.5 m/s（Appendix 5.2）；但 B 的区间均值 2.36 < 2.5（口径冲突，见 §五 S6） |
| 控制激活前波持续时长 | **≥45 s** | 未报告 | §2.2 "the unsteady traffic is allowed to persist for at least 45 seconds before a controller is activated" | 保证基线确为"波期" |
| 波判据阈值 | 瞬时速度标准差 > **2.5 m/s** | 未报告 | Appendix 5.2、Figure 6 | 判据用于"波起始时刻"，与表格的区间平均 σ 口径不同 |
| 车间距采样率 | 30 Hz | 未报告 | §3 | 传感器型号未给 |
| 底层控制更新率 | 20 Hz | 未报告 | §3.3 | 多模态 PID |
| FollowerStopper 参数 | Δx₁⁰=4.5、Δx₂⁰=5.25、Δx₃⁰=6.0 m；d₁=1.5、d₂=1.0、d₃=0.5 m/s² | 未报告 | §3.1 Eq.(1)(2) | 举例：Δv=−3 m/s 时 Δx₁=7.5、Δx₂=9.75、Δx₃=15 m（自洽，本笔记已复核通过） |
| PI-with-saturation 参数 | m ↔ **38 s**（≈绕圈一周）；g_l=7 m；g_u=30 m；v^catch=1 m/s；γ=2 m；Δx^s=max(2 s·Δv, 4 m) | 未报告 | §3.2 Eq.(3)(5) | **无需外部输入**（U 为自身速度滑动平均） |
| 底层控制器阶跃性能 | h₁: 上升时间 ≈1.6 s、超调 5%、调节时间 ≈5.52 s；h₂: 上升时间 ≈0.8 s、超调 11%、调节时间 ≈1.94 s | 未报告 | §3.3 | 阶跃 1 m/s（制动为 −1 m/s）；切换阈值 −0.25 m/s；输出范围 ±100 |
| 试验车队 EPA 油耗范围（Table 5） | 城市 8.71–15.67 ℓ/100km；高速 6.37–10.68 ℓ/100km（Escape Hybrid 最低：6.92/7.84） | 未报告 | Table 5 | 用于说明车队异构性；**不是**实测油耗 |
| 研究资助 | NSF CNS-1446715、CNS-1446690、CNS-1446435、CNS-1446702 | — | Acknowledgements | 车辆由 University of Arizona Motor Pool 提供 |
| 数据与代码 | `https://uofi.box.com/v/trajectoryPaperData`（2016） | — | §4.2 → 参考文献 [67] | 无许可声明；存活状态**未核** |

### 数字口径对照表

> 触发条件（`deep-paper-reader` §3.7）：同一指标在本文出现 ≥2 个数值（不同实验 / 不同区间 / 是否控制激活 / 不同期望速度）。**本表把模板的"数据集划分 / 集成 / checkpoint 平均"三列改写为本文对应的口径维度：实验编号 / 区间口径 / 控制状态**；口径列**无空缺**。引用任意一个数值都必须连同口径一起引。

| 指标 | 数值 | 实验（等价于"数据集/划分"） | 区间口径（起止秒 / 区间长） | 控制状态与设定 | 其他设置 | 出处 |
|---|---|---|---|---|---|---|
| 速度标准差 σ (m/s) | 3.31 | A（21 辆） | 79 s 起，至 126 s（≈47 s） | 未控，波期（WS） | 期望速度 U 未施加 | Table 1 / Table 3 行 A |
| 速度标准差 σ (m/s) | 0.64 | A（21 辆） | 292 s 起，至 347 s（55 s） | FollowerStopper，U=7.50 m/s（**6 个受控区间中事后最优**） | 同上 | Table 1 / Table 3 行 A（CA） |
| 速度标准差 σ (m/s) | 0.67 | A（21 辆） | 222 s 起，至 292 s（70 s） | FollowerStopper，U=7.00 m/s | 同上 | Table 1 |
| 速度标准差 σ (m/s) | 1.56 | A（21 辆） | 347 s 起，至 415 s（68 s） | FollowerStopper，U=8.00 m/s | 正文称该设定"inevitably induces a wave again"，但 σ=1.56 < 2.5 判据 | Table 1 / §4.2 |
| 速度标准差 σ (m/s) | 1.44 | A（21 辆） | 463 s 起，至 567 s（104 s） | **控制已停用** | 正文称"the traffic wave reappears"，但 σ=1.44 < 2.5；且该区间吞吐 2133 veh/hr 为**全实验最高** | Table 1 / §4.2 |
| 速度标准差 σ (m/s) | 2.36 | B（21 辆） | 55 s 起，至 112 s（57 s） | 未控，波期（WS） | **区间均值 2.36 < 2.5 判据**（口径冲突，见 §五 S6） | Table 2 / Table 3 行 B |
| 速度标准差 σ (m/s) | 1.19 | B（21 辆） | 202 s 起，至 300 s（98 s） | 人类驾驶员控速，U=7.15 m/s（**2 个受控区间中事后最优**） | 16 mph | Table 2 / Table 3 行 B（CA） |
| 速度标准差 σ (m/s) | 2.25 | B（21 辆） | 300 s 起，至 409 s（109 s） | 控制停用，恢复常规跟车 | 正文称波重现；σ=2.25 < 2.5 | Table 2 |
| 速度标准差 σ (m/s) | 3.85 | C（22 辆） | 161 s 起，至 218 s（57 s） | 未控，波期（WS） | 密度 22/260 = 84.6 veh/km | Table 4 / Table 3 行 C |
| 速度标准差 σ (m/s) | 1.74 | C（22 辆） | 218 s 起，至 413 s（**195 s**） | PI-with-saturation，全自动（**唯一受控区间，无择优**） | 该 195 s 窗口内**又生成了一次波**（§4.2），故这是"含二次波的平均" | Table 4 / Table 3 行 C（CA） |
| 油耗 (ℓ/100km) | 24.6 → 14.1 | A | 79–126 s → 292–347 s | 波期 → FollowerStopper U=7.50 m/s | 正文另给未舍入值 14.13 | Table 1 / Table 3 行 A |
| 油耗 (ℓ/100km) | 21.8 → 17.0 | B | 55–112 s → 202–300 s | 波期 → 人类控速 U=7.15 m/s | 正文另给中间档 17.9（U=6.26 m/s 区间） | Table 2 / Table 3 行 B |
| 油耗 (ℓ/100km) | 29.0 → 20.9 | C | 161–218 s → 218–413 s | 波期 → PI 全自动 | 百分比正文 −27.9% vs 表格 −28.1% | Table 4 / Table 3 行 C |
| 制动事件率 (events/veh/km) | 8.58 → 0.12 | A | 同上 | 同上 | **τ 逐实验不同，数值未印出** | Table 1 / Table 3 行 A |
| 制动事件率 (events/veh/km) | 9.50 → 2.27 | B | 同上 | 同上 | 同上 | Table 2 / Table 3 行 B |
| 制动事件率 (events/veh/km) | 9.66 → 2.47 | C | 同上 | 同上 | 同上 | Table 4 / Table 3 行 C |
| 吞吐量 (veh/hr) | 1827 → 2085 | A | 同上 | 同上 | q=(n/L)·v̄，n=21，L=260 m | Table 1 / Table 3 行 A |
| 吞吐量 (veh/hr) | 1828 → 2008 | B | 同上 | 同上 | n=21 | Table 2 / Table 3 行 B |
| 吞吐量 (veh/hr) | 1755 → 1711 | C | 同上 | 同上 | n=22 | Table 4 / Table 3 行 C |
| "波期"定义口径 | 瞬时 σ > 2.5 m/s | 全部 | 判据用于确定**起始时刻** | — | 与 Table 1–4 的**区间平均 σ** 不是同一口径 | Appendix 5.2 / Figure 6 |
| "波期"定义口径 | 区间平均 σ（3.31 / 2.36 / 3.85） | A / B / C | 各实验第一段"Waves start"区间 | 未控 | B 的 2.36 不满足 2.5 判据 | Table 1 / 2 / 4 |

---

## 五、统计与推断旗标

> 本节只做旗标；统计量重算请交 `paper-experiment-analyzer`。**重要区别**：Table 1–4 中的 σ 是**交通状态指标**（跨车速度标准差），**不是**效应量的不确定度。全文**没有任何一处**给出效应量的 CI、SE 或误差棒。

| 编号 | 旗标 | 证据/位置 | 后果 |
|---|---|---|---|
| **S1** | **无不确定度**：效应量全部为无 CI 的点估计 | 全文无 CI、无 SE、无误差棒；Table 1–4 的四列指标均只有点值 | 引用方**不能**说"油耗降低 42.5%"，只能说"在该单次运行中，事后择优区间的平均油耗率由 24.6 降至 14.1 ℓ/100km（−42.5%），论文未报告不确定度" |
| **S2** | **事后择优（post-hoc best-interval selection）**：Table 3 的 CA 列定义即 "the **best** interval when control is active" | Table 3 表注（§4.2）；Exp A 有 6 个受控区间、B 有 2 个、C 有 1 个 → **A、B 的"最优"是 winner's curse** | A 的 −80.8%/−42.5%/−98.6% 是最乐观估计；C 的数值（唯一受控区间、无择优）反而**更接近无偏**，但其窗口含二次波（195 s） |
| **S3** | **用单次实验下结论**：每个条件 n=1，无重复运行、无随机种子 | §4.2 三次实验各 1 次（A 567 s、B 409 s、C 413 s）；§三"随机种子/重复次数"= 未报告 | **"consistently"（n=3 次运行、同一场地、同一密度档）不足以支撑统计意义上的稳健性**；run-to-run 变异完全未知 |
| **S4** | **时间混杂（confounding with time-in-experiment）**：所有对比都是"先波期 → 后受控期"，控制的**开/关顺序从不随机化** | Exp A：126 s 开、463 s 关；Exp B：112 s 开、300 s 关；C：218 s 开。无"先控后波"的反向顺序运行，也无"全程无控制"的同长对照 | 无法排除"驾驶员热身/疲劳漂移/密度自然变化"与"控制效应"的混杂。**部分缓解**：A 与 B 都做了关断反转（波重现）——这是本文设计上最强的内部对照，但它仍只在**同一次运行内**成立（见 §二 #15 的两处张力） |
| **S5** | **多重比较未校正**：Exp A 在 6 个不同期望速度下各算了一套指标，正文各处引用的是各自最好/最差的区间 | Table 1 共 8 个区间；§4.2 逐档讨论 6.50/7.00/7.50/8.00/7.50 m/s | **膨胀的假阳性风险**：在 6 档里挑最好的，报出的"提升"含选择性偏倚；论文未声明任何校正，也未预设主终点 |
| **S6** | **波判据与表格口径不一致**：判据是"瞬时 σ > 2.5 m/s"，但表格报的是"区间平均 σ" | Appendix 5.2 vs Table 1/2/4。B 的 "Waves start" 区间 σ=2.36 < 2.5；A 的多处"wave reappears"区间（σ=1.44、1.56）同样 < 2.5 | 若按论文自己的 2.5 判据，A 的"关闭控制后波重现"与"8.00 m/s 又诱发波"两处**在表格口径下并未成立**。这直接影响"基线确为波期"的可信度 → 建议作者**印出逐时刻 σ 曲线与阈值穿越时刻**（Figure 6 已在，但表格未对齐口径） |
| **S7** | **关键计算复算不符 1 处**：Exp C 波期 σ 增幅 | §4.2 line 561 写 "+37.7% increase in the average velocity standard deviation"；由 Table 4（Exp start 1.62 → Waves start 3.85）复算为 **+137.7%**。同句油耗 +63.8%（17.7→29.0）与吞吐 −18.8%（2160→1755）**均复算通过** → 判为漏印首位 "1" | 引用该句时**必须**用复算值或回避；否则会把 C 的波强度低估近 4 倍 |
| **S8** | **关键计算复算不符 2 处（小）**：Exp A 油耗降幅与 Exp C 油耗降幅 | A：24.6→14.1 = −42.7%，正文/表 3 报 −42.5%（用 14.13 亦为 −42.6%）；C：29.0→20.9 = −27.9%，表 3 报 −28.1%，而同文 line 604 写 27.9% | 差异 ≤0.2 个百分点，**不足以改变结论**，但说明本文百分比不是用打印精度复算得到 → 引用时优先抄**表格原始值**（ℓ/100km、m/s、veh/hr），而非百分比 |
| **S9** | **正文与表格的"up to"冲突** | §1.2 "up to 40% less fuel consumption, and a throughput increase of up to 15%"；Table 3：A 油耗 −42.5%、吞吐 +14.1% | Intro 的 40% **低于**表格 42.5%，15% **高于**表格 14.1% → 两处均为对表格的近似/包络，**不可作为引用值**；以 Table 3 为准（`deep-paper-reader` §3.3 硬规则） |
| **S10** | **指标定义导致的同义化**：throughput ≡ 平均速度 × 常数 | §4.1 `q = (n/L)·v̄`，环道上 n/L 恒定 | "吞吐量提升 14.1%"与"平均速度提升 14.1%"是同一句话；**这不是两个独立证据**。P1 若同时引用两者作为两处证据将构成重复计数 |
| **S11** | **跨实验指标不同标尺**：制动阈值 τ 逐实验各算 | §4.1 "τ is always calculated over the interval when waves are active" | 三个实验的 events/veh/km **不能横向比较**；也不能与其它文献的制动指标对比 |
| **S12** | **无等价/非劣检验**：Experiment C 的吞吐量 −2.5% 未被检验是"无实质差异"还是"确有下降" | Table 3 行 C；§4.2 只说 "slightly reduced" | 按全局 AGENTS.md §1 铁律 2，"无差异"必须用等价/非劣检验 → 本文的 −2.5% **既不能读成"吞吐未降"，也不能读成"显著下降"**；引用时必须写成"报告下降 2.5%，未做检验" |
| **S13** | **相关未被写成因果（合格项）** | §5 用 "can control the flow"、"demonstrate" 等，但结论均限于单车道环道；多车道写成 "the theory extends"（明示为未来工作） | 本文在**因果措辞上是克制的**（有真实的干预：切换控制），这一点优于常见的仿真类文献；**但** §5 的 "implies that a noticeable impact … can in principle be achieved by means of adaptive cruise control systems that are already in place" 属 **D 级推测**，出现在结论段 |
| **S14** | **测量效度未独立验证**：油耗来自 OBD-II 瞬时油耗率，未与油量/CO₂ 计量比对 | §2.1、§4.2；轨迹由相机 CV 得到，仅"validated against the CAT Vehicle control computers and the in-vehicle devices"，**未给误差量级** | 油耗的**绝对水平**（14.1–29.0 ℓ/100km）不宜直接引用为真实道路油耗；相对变化方向比绝对值更可信 |
| **S15** | **样本不独立**：σ、油耗、制动率都是**同一批车、同一段路、同一时段**上的聚合量，且同一实验内的多个区间共享同一批驾驶员 | §4.1 的时空平均定义；Table 1 的 8 个区间来自同一次 567 s 运行 | 各区间不是独立观测 → 不能把 8 个区间当作 n=8；任何区间间的"比较"都是**同一次运行内的描述**，不具备推断性 |

---

## 六、缺失信息清单

**A. 未报告（缺失影响 + 最小补法）**

1. **未报告：IRB / 人体受试者审批与知情同意。** 影响：本文的驾驶员是"University of Arizona employees"，属人类受试者参与实测驾驶；P1 若要以本文为"实车测试规范"的范例，**拿不到伦理合规的可引证据**，写作时不能写"遵循 Stern et al. 的伦理流程"。**最小补法**：向通讯作者索取 IRB 编号与批准日期，或直接改用其它明确报告 IRB 的实车文献作为规范依据（本文只引其技术结论）。
2. **未报告：区域许可 / 试验场授权 / 保险与责任安排。** 影响：无法回答"这类实验需要什么前置审批"，而这恰是 P1 项目 `AGENTS.md` §5「实车测试（若开展）：安全员、区域许可、里程与暴露量」要求的三项之一。**最小补法**：从 Acknowledgements 的"University of Arizona Motor Pool"线索去信确认场地性质（自有封闭场地 / 需州级许可），或按 P1 自建清单报告，**不引本文**。
3. **未报告：里程 / 暴露量。** 影响：无法计算任何"每公里"口径的风险率或接管率，也无法做暴露量归一化的跨研究比较。本文仅可得**时长**（7–10 min 设计；A 567 s、B 409 s、C 413 s ≈23.2 min）。**最小补法**：用 [67] 的轨迹数据自行积分求总里程（数据公开，可行），但须标注"**本笔记据公开数据推算，非论文报告值**"。
4. **未报告：接管 / 干预次数与分母。** 影响：本文只有**计划内**的模式切换时刻（126/463 s、112/300 s、218 s），**没有**任何非计划干预计数，**也没有分母**（每公里或每次干预机会）。P1 若做真车闭环，`AGENTS.md` §5 明确要求"接管率的分母写清"——**本文不满足该项，不能作为模板**。**最小补法**：P1 自行定义"每次干预机会 = 每次控制器输出与前车时距低于阈值的时刻"，并在报告中显式给出分子/分母。
5. **未报告：安全员是否具备油门/刹车越权接管能力。** 影响：本文仅说受训驾驶员"controls the steering wheel … at all times"，纵向控制由软件掌握 → 这是"**方向盘安全员 + 软件纵向控制**"的弱安全安排；P1 若照此设计将无法通过现代功能安全/SOTIF 的思路自检（项目 `AGENTS.md` §4 允许引 ISO 26262 / ISO 21448 的**术语与思路**）。**最小补法**：P1 明确写"安全员具备制动优先权（brake override）"，并报告 override 的触发次数。
6. **未报告：车间距 Δx 的传感器类型、量程、精度与安装位置。** 影响：这是本文控制回路的**唯一在线感知输入**（30 Hz）；未知感知噪声水平 → 无法判断"控制有效"中有多少依赖高精度测距，**直接削弱 P1"零额外传感器成本"论证的可比性**。**最小补法**：查 CAT Vehicle 平台论文（[63] 同团队 IEEE IV 2017）或向作者索取；否则 P1 只能引本文的**结论**、不能引其感知设定。
7. **未报告：底层 PID 增益与控制器参数搜索空间 / 目标函数。** 影响：无法判断参数是否接近最优，**更无法判断换密度、换车队规模是否必须重调** → 外推风险不可量化。**最小补法**：索取代码（[67] 声称含 source code）并复算参数敏感性。
8. **未报告：随机种子 / 重复次数 / run-to-run 变异。** 影响：无法把任何百分比与"运行间波动"对比，**"consistently"（n=3）与"up to X%"都不可做统计解读**。**最小补法**：P1 自身按 `AGENTS.md` §4"种子 ≥5，报 mean ± std 或 95% CI"执行；引用本文时**必须**带上"单次运行、无 CI"。
9. **未报告：实验日期、时段、天气、光照、路面摩擦。** 影响：无法判断结果能否复现于不同环境，也无法做 sim-to-real 的差距归因。**最小补法**：查 [67] 数据集元数据或同团队后续论文（如同一团队的环道实验后续工作），标注 `[待核实]`。

**B. 报告但不可核验**

10. **报告但不可核验：数据与代码链接 `https://uofi.box.com/v/trajectoryPaperData`（[67]，2016）。** 需要什么才能核验：链接存活 + 许可条款 + 文件清单与版本。**在核验前，P1 不得假定可复用、更不得再分发。**
11. **报告但不可核验："the theory extends also to multi-lane freeways"（§5）。** 需要什么才能核验：同团队的多车道实验或稳定性分析结果（[63] 为同团队 IEEE IV 2017 的理论工作，本笔记**未获取该文全文**，标 `[待核实]`）。
12. **报告但不可核验：制动阈值 τ 的定义。** 论文给了算法（未控波期所有车辆减速度标准差的平均）但**未印出数值** → 无法从表格复算 events/veh/km。需要：τ 的逐实验数值，或原始减速度数据。

**C. 报告口径有歧义（两种解释会导致结论如何不同）**

13. **口径有歧义：波判据到底是"瞬时 σ"还是"区间平均 σ"。** 若为**瞬时**（Appendix 5.2 字面）→ 则 Table 1 中 σ=1.44/1.56 的区间**无波**，正文"wave reappears / induces a wave again"两处叙述**不成立**，Exp A 的"关断反转"证据弱化；若为**区间平均** → 则 B 的波起始区间（2.36）**达不到判据**，基线"确有波"不成立，B 的 −49.5% 就失去一个合格的对照基线。**两种解释都要求作者补充逐时刻 σ 与阈值穿越时刻。**
14. **口径有歧义："less than 5%"是"实测渗透率"还是"外推上限"。** 实测只有 1 辆车（4.5–4.8%）；若读作实测 → 可引；若读作"a few actuators 也能做到" → 是**从单执行器外推**，不可引为结论。P1 必须按后一种理解设限。
15. **口径有歧义：Exp C 的 "Autonomy" 区间（218–413 s，195 s）是"控制期平均"还是"控制效果"。** 正文自认该窗口内**又生成了一次波**并被再次消散 → 报告的 −54.7% 是"含二次波的平均"，**低估**了控制生效时的瞬时效果，同时又**高估**了"控制能消除全部波"的能力。引用时必须写明"195 s 长窗口，含二次波"。
16. **口径有歧义：油耗是"瞬时油耗率的时空平均"还是"总油量"。** §4.1 定义明确为时空平均的**瞬时油耗率**（ℓ/100km），非总油量、非加油量 → 不能读成"总共省了多少升"。

---

## 七、复用价值判断

| 问题 | 结论 |
|---|---|
| **方法可否搬到我的问题？需要改什么？** | **部分可搬，且只能搬"思路+指标"，不能搬"控制律"。** 可搬：①"用极少数执行器压制交通波"的问题设定与 on/off 反转式验证设计；②四个指标族（速度标准差、过量制动率、油耗率、吞吐量）。需改：本文控制律（FollowerStopper 的分区抛物线、PI+saturation）是**单车纵向速度控制**，输入是"自车速度 + 前车间距 + 期望速度"，**与 P1 的 OTF 势场（超车频次标量）不是同一类信号**；搬到 P1 的高速主线编队场景需重建为多车协同 + 车道级 ODD。本文**没有任何** OTF 类社会压力项，P1 不能引它支撑"OTF 势场有效"。 |
| **评价协议可否直接对齐（指标、划分、基线）？** | **不能直接对齐，只能借用。** ①指标定义（σ、κ、q、c̄）本文给得清楚，但其 **τ 逐实验不同**、**q 是 v̄ 的线性导出量**，两个都是跨研究不可比的陷阱；②划分方式是"按 notable events 人工切区间 + 事后择优"，**与 P1 项目 `AGENTS.md` §3/§4 要求的"逐场景报告 + 种子 ≥5 + 95% CI"不兼容**；③基线是"同一实验内的未控区间"，**没有独立实现的控制器基线** → P1 的四条基线（PID/MPC/TD3/OTF-CfC）无法与本文对齐。**可用之处**：把本文当作 P1"动机段"的实证引用，而不是"对比表"里的数字来源。 |
| **数据/代码可否直接取用？许可如何？** | **暂不可假定可取用。** [67] 给出 `https://uofi.box.com/v/trajectoryPaperData`（2016），但**无许可条款、无版本号、链接存活状态未核**（见 §六 #10）。→ 在明确许可前：**只引结论，不使用其数据**。若 P1 想用其轨迹做"真实交通波"回放，须先核许可并注明"数据来自 Stern et al. (2018) 公开数据集"，且按 `AGENTS.md` §1 第 2 条**不得写成实车验证**（回放仍是开环/仿真证据）。 |
| **若要引用其数字，引用时必须带上的限定语是什么？** | **必须同时带四项**：①道路 = 单车道环形封闭试验场（车道中心半径 41.4 m、周长 260 m）；②车队 = 21 辆（Exp A/B）或 22 辆（Exp C），≈81–85 veh/km，**仅 1 辆受控**（4.5–4.8%）；③实验次数 = 每条件**单次运行**、无重复、无随机化开关顺序；④报告口径 = **事后择优区间、无 CI/无显著性检验**，且吞吐量是"密度×平均速度"的导出量。另须加一句：**"文献报告值，协议不同，不可直接比较。"**（项目 `AGENTS.md` §1） |

**机器可读单行（下游 `paper-experiment-analyzer` / `citation-and-related-work` 直接消费；缺失则下游应拒绝出具"断言强度校准"并回退补齐）：**

```
citation_qualifier: single-lane closed circular test track (lane-centre radius 41.4 m, 260 m circumference, no lane changes/merges/intersections), 21 vehicles (Exp A, B) or 22 vehicles (Exp C) at ~81-85 veh/km, exactly ONE vehicle under wave-damping control (4.5-4.8% of the fleet; the abstract's "less than 5%" is extrapolated from a single actuator, not a penetration sweep); 3 experiments - A FollowerStopper with an externally supplied set point, B trained human driver reproducing it, C PI-with-saturation fully automatic using a 38 s self-average - ONE RUN EACH, no repetition, no randomisation of control on/off order; no CI/SE/significance test anywhere, Table 3's "control active" values are the post-hoc BEST interval, wave onset uses a 2.5 m/s instantaneous velocity-std-dev threshold while tables report interval-average std dev, braking threshold tau is recomputed per experiment so braking rates are not comparable across experiments, throughput is defined as density times mean speed (not an independent count); drivers were university employees with safe-driver training, a trained driver held the steering wheel at all times, but NO IRB/consent/permit/insurance statement and NO mileage, exposure or takeover/intervention denominator is reported
```

---

## 八、红队三条

**1｜领域最懂的人会质疑：** "你把 '−42.5% 油耗、+14.1% 吞吐' 记成了这篇论文的结论，但那只是 **Experiment A 的 6 个受控区间里事后挑出的一个 55 秒窗口**；同一实验里'关闭控制'的那个 104 秒区间吞吐量是 **2133 veh/hr，比你说的 2085 还高**。而且 A 用了**外部观察者提供的期望速度**，不是全自动的。"——**需要什么证据才能消解**：① 印出**全部**区间（Table 1 已给，逐区间引用即可）；② 给出"未控基线"的**同长度、同位置**对照区间而不是只在波期取一段；③ 对 A 的 6 档期望速度做**预设主终点 + 多重比较校正**；④ 明确区分"需外部输入的 FollowerStopper"与"完全自动的 PI"的适用条件。**本笔记的处置**：已在 §二 #5–#10、#15 与 §五 S2/S5/S9/S10 落账，并把"引用时不得用 'up to 40%'"写进 §七 限定语。

**2｜方法与统计视角会质疑：** "你给的内部等级是 B_int，但这条主张只有**单次运行、无 CI、无重复、无随机化、事后择优**，凭什么是 B？而且你引用的是**区间平均 σ**，论文自己的波判据是**瞬时 σ > 2.5**，B 实验的基线区间均值 2.36 根本不到阈值——**基线里到底有没有波？**"——**需要什么证据才能消解**：① 逐时刻 σ 时间序列 + 阈值穿越时刻（Figure 6 已有三张图，但表格未与判据对齐）；② 至少 3 次独立重复运行以给出 run-to-run 方差；③ 对"控制开"与"控制关"做**随机化顺序**；④ 给出效应量的 bootstrap CI。**本笔记的处置**：① 方向性主张（波可被消散、σ 下降方向）保留 **B_int**，但**幅度类主张一律降为 C_int**（§二 #5–#10）；② 增设 §五 S6 旗标并把"基线是否有波"列为 §六 #13 的**口径歧义（两种解释都伤结论）**；③ §二 #16 单列"无不确定度"行并给 **D_int**。**红队未推翻方向性结论，但已回改台账等级与数字表**（未只在本节写一句话）。

**3｜编辑 / 邻域读者会质疑：** "缺失信息清单写的是场面话——我读完还是不知道**能不能复现**，也不知道**做同类实车实验要什么手续**。"——**需要什么证据才能消解**（已改写为可执行动作）：① **要复现控制律** → 论文已给足参数（§三 第 4 项），但须向作者索取**底层 PID 增益**与 **[67] 的代码**（缺失后果：无法复现 20 Hz 底层回路，只能复现速度指令层）；② **要复现实验** → 须取得**逐辆车的轨迹数据**与相机标定参数（缺失后果：无法独立重算 σ、κ，因为 τ 未印出）；③ **要办同类实车实验** → **本文帮不上忙**：IRB、许可、保险、里程、接管分母**五项全无**（§六 A1–A4），必须另找规范来源；④ **要判断能否外推** → 论文自己承认多车道"future experiments are needed"（§二 #14），**没有任何**不同密度/不同车队规模的重复（缺失后果：渗透率外推无实测支撑）。

---

## 九、限制

1. **材料限制**：本笔记基于**arXiv HTML 版全文**（`https://arxiv.org/html/1705.01693`，抓取日期 2026-10-02），**未获取 TRC 正式发表版 PDF，也未获取补充材料**（Movie S1 未审；`[67]` 的数据/代码未下载）。因此：§三 中的"数据与代码可用性"、以及"arXiv 版与正式版是否有数值差异"，**均未核验**，一律标 `[待核实]`。正式版可能含 arXiv 版没有的伦理/数据声明 → **入稿前必须用 DOI 核验正式版**。此外，纯文本抓取会丢失图内信息：**Figure 2（FollowerStopper 分区图）、Figure 3/4/5（轨迹与速度剖面）、Figure 6（瞬时 σ 曲线与阈值线）本笔记均未做像素级读数**，因此 §六 #13 关于"阈值穿越时刻"的质疑**只能提出、不能自行裁决**。
2. **复算限制**：所有数字均抄自论文正文与 Table 1–5，**未获原始数据** → 只能做自洽性检查（本笔记已完成：FollowerStopper 的 Δx_k 边界在 Δv=−3 m/s 处自洽 ✓；A/B/C 的 Table 3 百分比 12 项中 11 项可复算 ✓；q=(n/L)·v̄ 与 Table 1–4 的量级自洽 ✓），**无法验证方差、异常值、区间边界选择与统计量**。两处复算不符已记入 §五 S7/S8。
3. **视角限制**：本笔记**不评价**该工作的**重要性**与**新颖性**（属主编视角，交 `cross-paper-synthesizer` 与 `research-gap-hunter`）；也不做**外部复现检索**——台账"外部复现"列**全部为"未检"**，这是**信息缺失状态**，**不得**被下游读成"无外部证据"或"仅一次性证据"（`deep-paper-reader` §3.1.1 硬规则 2）。
4. **口径限制**：本文的四个指标（σ、c̄、κ、q）中，**κ 的阈值 τ 逐实验不同且数值未印出**、**q 是 v̄ 的线性导出量**、**c̄ 是 OBD-II 瞬时油耗率的时空平均**。本笔记已在 §四 数字口径对照表逐行标注，但**无法把三个实验的制动率放到同一标尺上**——这是原文的口径设计问题，不是本笔记可修复的。
5. **时效限制**：精读日期 **2026-10-02**。该文发表于 2018 年，本笔记**未检索其后续更正、勘误或撤稿**，也**未检索引用它的后续工作**（如该团队后续的多车道/渗透率实车实验）。缓解：入稿引用前由 `citation-and-related-work` 复核 DOI 状态与版本；新颖性/奠基定位由 `research-gap-hunter` 另做。

---

## 十、对 P1 的三条具体可用结论

> 本节是 P1（OTF-CfC）专用。**全部引用均受项目 `AGENTS.md` §1 三条红线约束**：① 不得预先声称"OTF 势场带来 X% 性能提升"；② 仿真/回放不得写成实车验证；③ 不得搬用他人论文数字而不标"文献报告值，协议不同，不可直接比较"。

### ① 可直接引用的最强结论句（英文原句 + 成立条件 + P1 必带的限定语）

**首选引用（最强、最可作为动机锚点）——§5 Conclusions 原句：**

> "A single autonomous vehicle can control the flow of at least 20 human-controlled vehicles around it, with substantial reductions in velocity standard deviation, excessive braking, and fuel consumption."
> —— Stern RE, Cui S, Delle Monache ML, et al. *Transportation Research Part C* 2018;89:205–221, §5 Conclusions.

**它成立的条件（缺一不可）**：① 道路 = **单车道封闭环形试验场**（车道中心半径 41.4 m、周长 260 m、无换道/无匝道/无交叉口）；② 车队规模 = **21 辆（Exp A、B）或 22 辆（Exp C）**，密度 ≈ **81–85 veh/km**（接近拥堵密度）；③ **自动化比例 = 恰好 1 辆车受控**（1/21 = 4.8%；1/22 = 4.5%），且该车**方向盘始终由受训驾驶员握持**；④ 波由**被指令"跟紧前车"的人工驾驶员自发产生**（非外部注入）；⑤ **每条件单次运行**，无重复、无随机化、**无 CI/无显著性检验**；⑥ 报告的是 **Table 3 的"事后最优受控区间"**，不是全时段平均。

**P1 引用时必须带的限定语（建议直接落笔的英文句子）：**

> "In a closed single-lane circular-track field experiment with 21–22 vehicles (≈81–85 veh/km) in which exactly one vehicle was under automated velocity control (4.5–4.8% of the fleet) and a trained driver held the steering wheel at all times, Stern et al. (2018) reported that this single vehicle dampened self-generated stop-and-go waves; the reported reductions (velocity standard deviation −49.5% to −80.8%, fuel consumption −22.1% to −42.5%, excessive braking −74.4% to −98.6%, throughput −2.5% to +14.1%) are **literature-reported values obtained under a different protocol (single-lane ring, one run per condition, post-hoc best-interval selection, no confidence intervals), and are therefore not directly comparable to results in this work**."

**P1 绝对不要单独引用的句子（外推型，容易被审稿人抓）：**

> "flow control will be possible via a few mobile actuators (less than 5%) long before a majority of vehicles have autonomous capabilities."（Abstract）

理由：这是**从"1 个执行器"外推到"a few（复数）执行器"** 的将来时推测（`C_int`/推测），本文**未做任何渗透率扫描**。P1 若引，必须写成"该文据此推测（extrapolates）……"，不能写成"该文证明 <5% 即可"。
同一原因，**"up to 40% less fuel consumption"** 也不得引用（§1.2 与 Table 3 的 42.5% 本身冲突，见 §五 S9）；要用就用 Table 3 的区间值。

### ② 它的控制律与观测手段 vs. P1 的"零额外传感器成本 + OTF 标量"路线

**它用了什么反馈（原文可核）**：
- **反馈量**：自车速度 `v^AV`（连续跟踪）；与前车的**间距** `Δx`（**30 Hz** 采样，定义为自车前保险杠到前车后保险杠的距离，"suitably smoothed"）；间距微分得 `Δv = d(Δx)/dt`；前车速度由 `v^lead = v^AV + Δv` **在自车在线估计**（§3 开头）。
- **期望速度 U 的来源分两种**：**FollowerStopper（Exp A）需外部给定 U**（§2.2 明说"a desired average velocity is communicated from **an external observer**"）；**PI-with-saturation（Exp C）完全自动**，用自车过去 **38 s（≈绕圈一周）**速度的滑动平均自估计 U（§3.2），并明确"only uses information directly measured by the CAT Vehicle itself, and it does not require any external information"（§4.2）。
- **控制律形态**：FollowerStopper = Δx–Δv 相平面的分区规则，边界为抛物线 `Δx_k = Δx_k⁰ + (Δv₋)²/(2d_k)`，三区（停止 / 适应 / 安全），参数见 §四；PI+saturation = `v^target = U + v^catch·clip((Δx−g_l)/(g_u−g_l), 0, 1)` 后经 `v^cmd_{j+1} = β_j(α_j v^target_j + (1−α_j) v^lead_j) + (1−β_j) v^cmd_j` 平滑，`β = 1 − α/2`、`α = clip((Δx−Δx^s)/γ, 0, 1)`、`Δx^s = max(2 s·Δv, 4 m)`、`γ = 2 m`。
- **底层**：多模态 **PID**（加速模式 h₁ / 制动模式 h₂，按 `v^cmd − v ≤ −0.25 m/s` 切换），输出 ±100 的踏板指令，**20 Hz**。阶跃性能：h₁ 上升 1.6 s / 超调 5% / 调节 5.52 s；h₂ 上升 0.8 s / 超调 11% / 调节 1.94 s。
- **观测手段（用于评测，不用于控制）**：赛道圆心一台 **360° 相机**（CV 提取车辆中心 → 轨迹 → 差分得速度/加速度）；每车一台 **OBD-II** 记录器测瞬时油耗；轨迹与控制计算机交叉验证。

**P1 需要额外说明什么（三条，必须写进 P1 的 Related Work / Method）**：

1. **P1 的"零额外传感器成本"必须先定义"额外"相对于什么。** 本文的在线输入只有**自车速度 + 前车间距**——这两样在量产车上由已有的轮速与**前向雷达/摄像头**提供，**并未新增传感器**，因此本文是 P1"零额外传感器成本"主张的**有利旁证**（本文的 Exp C 甚至不需要任何外部/联网输入）。但**本文没有报告 Δx 用的是哪种传感器、精度多少**（§六 #6）→ P1 只能写"已有 ACC 级前向感知即可（Stern et al., 2018, Exp C）"，**不能**写"精度要求已被验证"。
2. **P1 的 OTF 标量在本文中没有任何对应物，必须显式声明。** 本文的控制律只用 `v^AV`、`Δx`、`Δv`（+ 期望速度），**既没有用到交通流社会压力量，也没有用到超车/换道频次，也没有用到任何邻域车辆的社会交互项**；论文全文**未出现** OTF 类概念。→ P1 引用本文时**只能**说"少量自动车可压制交通波这一**场景动机**有真车实证"，**不得**说"OTF 类信号的效用获得实车支持"。P1 的卖点（若 A1 消融不显著）按 `AGENTS.md` §1 应回退为"**可解释性 + 零额外传感器成本**"——本文恰好为后半句提供了弱旁证，**但不为前半句提供任何证据**。
3. **P1 必须说明"单车间距反馈"与"编队 + 势场"之间的建模落差。** 本文是**单执行器、单车道、无换道、稳态密度恒定**的最小系统；P1 是**多车道主线编队**，存在换道触发波、编队内多车耦合、以及自身 OTF 势场对邻近车的影响。P1 若要用本文论证"少量执行器足够"，必须**同时**承认：本文的密度恒定假设（环道上 n/L 不变）消除了真实高速上最关键的密度—流量耦合，因此"渗透率 <5%"**不能在 P1 的 ODD 下直接继承**。

### ③ 它的实车实验规范细节（P1 若做真车闭环必须照此报告 / 必须补报）

**本文报告了、P1 应当照此报告的（可直接借鉴的模板项）**：
1. **安全员安排**："A trained human driver controls the steering wheel of the CAT Vehicle **at all times** during all experiments."（§2.1）——P1 必须写明安全员的**位置与职责范围**。
2. **驾驶员资质与招募口径**：所有跟驰车驾驶员为"University of Arizona employees that have completed **safe driver training** but received no other special driving training"（§2.1）；Exp B 的控制驾驶员另受"safe driving of high-occupancy vehicles"培训并有"extensive practice"（§3.4）。
3. **驾驶员行为指令（防止结果被人工"洗白"）**：逐字给出指令，并明确目的是"explicitly prevent the human drivers from intentionally smoothing out traffic waves themselves"（§2.2）——**这是本文最值得 P1 照搬的一条**：P1 的编队实验必须同样写死驾驶/后台指令，并声明"防止操作员人为抹平效应"。
4. **参与者知情（对 AV 模式的告知）**：告知所有驾驶员 CAT 车会在自动/手动间切换，且"should focus on their driving rather than attempting to guess what mode the vehicle is in"（§2.2）。
5. **紧急处置协议**：不安全场景下驾驶员"steer out of the circle"，协调员鸣笛（air horn）终止实验（§2.2）。
6. **后车保护性几何安排**：CAT 车后车被告知"drive as if the CAT Vehicle were in the same lane"，且 CAT 车"will be driving at a **larger radius (1/2 vehicle width)** to facilitate evasive emergency maneuvers"（§2.2）。
7. **人员隔离阶段**：每次实验有明确的 "Evacuation" 阶段（全体研究人员撤离赛道）与"全部车辆停稳后人员再入场"（§2.2）。
8. **疲劳管理与单次时长上限**：每次实验 **7–10 min**（§2.2）。
9. **内部对照设计**：控制**开 → 关**的反转（A 在 463 s 关断、B 在 300 s 停止控制），用于展示波的**重现**（§4.2）。
10. **资金与资源披露**：NSF 四项基金编号 + 车辆来源（University of Arizona Motor Pool）（Acknowledgements）。

**本文完全没报告、而 P1 项目 `AGENTS.md` §5 明确要求、因此 P1 必须自己补报的**：
- **IRB / 人体受试者审批 + 知情同意**（本文：**未报告**）；
- **区域许可 / 试验场授权 / 保险与责任**（本文：**未报告**）；
- **里程与暴露量**（本文：**未报告**；仅有 7–10 min 时长口径）；
- **接管率及其分母**（本文：**未报告**；只有计划内模式切换时刻，无干预计数、无每公里/每次干预机会的分母）；
- **安全员是否具备制动/油门越权**（本文：**未报告**，仅说方向盘始终由人握持）。

→ **对 P1 的可执行结论**：本文可作为"**闭环真车实验的力学与协议模板**"（安全员、指令、紧急协议、后车保护、时长上限、开/关反转对照），**但不可作为"实车测试合规与暴露量报告"的模板**。P1 若做真车闭环，须按下表补齐，并把本文在 Related Work 中定位为"**提供了协议要素、未提供合规与暴露量分母**"：

| 报告项 | 本文 | P1 必须 |
|---|---|---|
| 安全员（位置/职责/越权能力） | 报告方向盘值守；越权能力未报告 | 报告位置 + 明确"具备制动优先权" + override 计数 |
| 伦理审批（IRB/编号/日期） | 未报告 | 报告编号与日期 |
| 知情同意 | 未报告 | 报告获取方式 |
| 区域许可 / 场地授权 / 保险 | 未报告 | 报告许可主体与编号 |
| 里程与暴露量 | 未报告（仅 7–10 min 时长） | 报告总里程、总时长、参与车辆数×里程 |
| 接管率（分子/分母） | 未报告 | 明确分母（每公里 / 每次干预机会） |
| 场景数与初始条件分布 | 3 次运行；初始化=均匀分布（按前左轮位置） | 按 `AGENTS.md` §5 逐场景报告 + 初始条件分布 |
| 失败分类 | 未报告 | 按 `AGENTS.md` §5 报告失败分类 |
| 控制开/关反转对照 | **报告**（A 463 s、B 300 s 关断） | **照此做**，并给 CI |
| 驾驶员指令逐字记录 | **报告** | **照此做** |

---

**质量门自查（`deep-paper-reader` §6）**：作用域声明已填（场景①，含项目 `AGENTS.md` 路径与主张上限三条）✓｜台账 16 行，证据列全部指向具体表/图/节，含"内部等级 + 外部复现"两列且外部列一律"未检" ✓｜无 A_int 级断言（本文上限 B_int，已按要求不虚高）✓｜同一指标多值已填数字口径对照表且口径列无空缺 ✓｜所有数字有单位与出处，推算值已标"本笔记推算" ✓｜方法清单 9 项全部填写，"未给出"项均写缺失影响 ✓｜已识别"作者没说的边界"（波判据与表格口径冲突、吞吐量现同义化、τ 跨实验不同标尺、C 的 195 s 窗口含二次波）✓｜缺失信息清单 16 条（可执行）✓｜`citation_qualifier:` 单行已给 ✓｜红队三条齐全且每条给出消解所需证据（并已回改台账等级：方向 B_int / 幅度 C_int）✓｜限制 5 条 ✓。
