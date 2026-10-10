# 知识引导自学习混行编队控制（带时延）｜Knowledge-guided self-learning control strategy for mixed vehicle platoons with delays

- **出处**：Nature Communications 16(1):7705, 2025 ｜ **类型**：期刊论文
- **作者**：Jingyao Wang, Huinian Wang, Jian Song, et al.（n=8；余为 Xingyu Chen, Jinghua Guo, Keqiang Li, Xunrui Li, Bowen Huang）
- **DOI**：10.1038/s41467-025-62597-x
- **全文来源**：`literature/fulltext/fresh2024/natcommun2025-platoon__a7709772.txt`（PAGES=18, CHARS=90,038；MD5=a770977246fba63e9354b02c8aa12cd1）｜ **材料版本**：**VoR（出版社最终版）** — 逐字证据：首页 "Article / https://doi.org/10.1038/s41467-025-62597-x"、"Received: 16 July 2024 / Accepted: 24 July 2025"；末页 "© The Author(s) 2025"、"Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License"、"Peer review information Nature Communications thanks Daliang Shen, Zhengwu Wang and the other anonymous reviewer(s) for their contribution to the peer review of this work."
- **版本/更正核查（T5，动作已执行）**：Crossref `works/10.1038/s41467-025-62597-x`（2026-10-06 取用）HTTP 200，`update-to` 与 `updated-by` 均为 `null` → **未发现撤稿或更正**；同一端点 `is-referenced-by-count = 58`（Crossref 端点，非 OpenAlex）。
- **分组**：2024+ 增量
- **证据等级初判**：**B 级** — 同行评议期刊 + 4 条对照基线 + 5 类场景闭环仿真 + 代码与数据在 CodeOcean 可复现，但**全部为数值仿真、无实车、无不确定度/CI/种子，且基线由作者自行改写**；未达 A（A 需预注册 + 效应量与 CI + 内部独立重复）。
- **档位建议**：A 精读 / B 略读 / C 仅引用 / D 排除 — **A 精读**。理由：唯一一篇在同一 ODD 族（高速公路主线、人工与自动混行的**编队纵向控制**）下同时给出**控制器**与**可直接复用的闭环评价协议**的 2024+ 论文；其 "knowledge-guided" 正是 P1"先验注入"路线最接近的可比对象（且**不是势场**，是宏观交通流先验），P1 的 Related Work 与 A1（OTF 开/关）消融都必须回应它。
- **五维打分（母协议 §5，各维 0–2，满分 20）**：D1=2 D2=2 D3=2 D4=2 D5=2 → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = **20**
  ⚠ **必须 0–2 制**；D4 一律指**时效性**（2024+ 基本应为 2）。
  - D1=2 依据：给出混行编队纵向**控制器**，且其四指标协议（式 1–6）+ 鲁棒性矩阵可被 P1 的 A1–A5 消融直接对标或复用。
  - D2=2 依据：4 条对照 + 5 类场景闭环 + 20 组数据/100 次实验的描述统计；**但按本项目 `AGENTS.md` §4 的门槛（种子 ≥5、mean±std 或 95% CI）严格判则 D2=1**。
  - D3=2 依据：代码与数据在 CodeOcean（DOI 10.24433/CO.4294963.v1）+ Source Data；NGSIM I-80 轨迹可直接作为 P1 的第二条真实领头车数据流。
  - D5=2 依据：全文 + PIP 效应量 + 可复现材料（代码/数据 DOI）。
  - **敏感性（写下来供复核）**：若按"单车道 + 显式忽略侧向"的 ODD 严格判，D1=1 → **17**；若按统计门槛严格判，D2=1 → **18**。**两种严格读法都仍在 A 档（≥14），档位结论不随读法变化。** ⚠ 20/20 是"按母协议字面"的上界分，**不等于该文证据无瑕**——其统计与基线改写问题见 §6「不可迁移 / 陷阱」与 §7。

## 1. 标题
Knowledge-guided self-learning control strategy for mixed vehicle platoons with delays ｜ 中文直译：面向带时延混行车辆编队的知识引导自学习控制策略

## 2. 摘要（≤400 字中文，保留关键数字与结论成立条件）

面向自动驾驶车与传统车将长期共存的混行交通，通信时延会显著劣化网联自动车（CV）编队控制。作者提出"知识引导自学习"混行编队控制策略，两步：① 以**运动波模型 + Newell 跟驰模型**提取传统车连续、聚合行为的关键特征（期望时变车头时距、期望静止间距），用于预测传统车轨迹；② 把**上一拍控制指令**并入软演员-评论家（SAC）的状态表示，并设计**模型切换机制**应对随机时延。仿真中 7 车编队（领头车与第 2、第 6 车为 CV，其余 4 辆为传统车；默认常数时延 **20 ms**）在交通稳定性、乘客舒适、能耗成本、交通振荡抑制四项上均优于 CVDS-IDM／DDPG／AC／PPO 对照；汇入汇出场景碰撞率为零。**结论成立条件**：Methods 明确假设"an infinite single straight highway"且"the lateral motion of the vehicle is ignored"（单车道、无侧向）；传统车由最优速度模型生成；领头车轨迹取自 NGSIM 加州 I-80 项目 16:00–16:15 一段。

## 3. 结论（≤350 字中文：作者结论节要点 + 关键数字 + 作者自承的局限）

Discussion 三点：① 首次把云平台作为控制器，充分利用路侧单元采集的宏观交通信息（交通波速、阻塞密度）；② 把运动波模型与 Newell 跟驰模型嵌入 SAC 作为知识引导模块，估计传统车聚合行为以抑制个体随机性；③ 把时延引起的"历史控制指令"并入状态并设计模型切换机制。**关键数字**：累计阻尼比由 **0.7 降至 0.54**；第 2 车 PIP（对 DDPG／CVDS-IDM／PPO／AC）阻尼比 +1.03／+7.68／+21.10／+13.40%，舒适 +2.06／+14.77／+30.04／+25.01%，能耗 +1.06／+9.14／+15.56／+18.72%，流稳定 +16.22／+19.23／+8.14／+22.27%；第 6 车舒适最高 +53.84%（对 PPO）。渗透率 0→100% 时 g_p 0.7309→0.3862、j_jerk 0.4341→0.1381、e_eco 2.0357→1.3461、f_flow 0.2238→0.2433（Table 1）。**作者自承局限**：全篇为数值仿真，Discussion 末句 "Future research could focus on applying the proposed framework to real-world vehicle platoons" —— **未做任何实车验证**；另自承对照方法"assumptions underlying these methods differ from those of this paper"、因"the limited availability of related research"才选现有方法对照。**本卡核验补充的局限（作者未自承）**：未报告弦稳定性、未报告计算/内存/端到端时延成本、未报告任何统计不确定度。

## 4. 方法一句话（≤60 字，必须含「输入 → 模型 → 输出」三要素）

输入路侧宏观流参数与邻车状态 → 运动波/Newell 先验估期望间距，送入含历史动作的 SAC → 输出 CV 期望加速度。

## 5. 图表清单（占位符）

> 图注逐字取自全文 txt，按 ≤100 字符截断；原提取文本含 ﬁ/ﬂ 连字，此处已还原为 fi/fl，其余逐字未改。**正文共 11 个 Figure + 1 个 Table（合计 12，已全覆盖）**；另有 Supplementary Fig. 1–2、Supplementary Table 2、Supplementary Algorithm 1（**本次全文 txt 未含补充材料，未见图注**）。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-nc-platoon-1} | Fig. 1 | An overview of the mixed platoon composed of autonomous vehicles and human-driven vehicles. a Comparisons between autonomous vehicles and human-driven vehicles (HV). b The NGSIM data shows… | (b) 用 NGSIM 真实数据展示 HV 急刹/急加速引发后继 HV 的振荡——全文的问题动机与"真实数据当领头车"的依据；(c) 一般混行编队分解为 "CV-HVs-CV" 子编队。 |
| {FIG-nc-platoon-2} | Fig. 2 | The proposed knowledge-guided self-learning mixed platoon control framework. CV = connected vehicle. HV = human-driven vehicle. V2X = vehicle-to-everything. Here, CV 0 is designated… | 三层架构：路侧单元采宏观流信息 → 云控自学习控制器（知识引导 + 数据驱动 + 模型切换 + 多模型存储）→ V2X 下发指令、执行器执行；注意"Delayed control command"这一时延路径。 |
| {FIG-nc-platoon-3} | Fig. 3 | The velocity, acceleration and position curves of a mixed platoon under different control strategies. CV = connected vehicle. HV = human-driven vehicle. a A schematic diagram… | 7 车编队示意 + 5 种策略的速度/加速度/位置曲线。**读图关键：图注 e=PPO、f=本文 SAC，与正文引用不一致（见文末 ⚠）**；碰撞只能靠位置曲线交叉目视判断。 |
| {FIG-nc-platoon-4} | Fig. 4 | Performance comparison among AC, PPO, CVDS-IDM, DDPG and the proposed knowledge-guided self-learning SAC strategies. PPO = proximal policy optimization. DDPG = deep deterministic policy… | 四指标逐车对比（按时间步平均）。要点：传统车（3–5 号）放大干扰、CV（2、6 号）抑制干扰——这是全文最有价值的**逐车传播**结论；(a) 累计阻尼比 0.7→0.54。 |
| {FIG-nc-platoon-5} | Fig. 5 | The superiority percentage of the proposed strategy compared with existing methods for CVs in mixed platoon. a Following CV 2. b Following CV 6. PPO = proximal policy optimization… | PIP 条形图（式 6 的可视化）。**唯一给出效应量的图**，但无误差棒/CI，故不能判"显著"。 |
| {FIG-nc-platoon-6} | Fig. 6 | The velocity, acceleration and spacing curves of CVs in a mixed platoon under different communication delays. a–c Following CV 2. d–f Following CV 6. Source data are provided as a… | 时延 {0.2, 0.5, 1.0, 2.0}ΔT（ΔT=0.1 s）下的速度/加速度/间距。要点：约 12 s 处第 2 车加速度幅值近 1.5，且跨时延几乎一致——作者据此声称对硬制动场景鲁棒。 |
| {FIG-nc-platoon-7} | Fig. 7 | The velocity and acceleration heat map based on the position trajectories for the mixed platoon with different penetration rates. Source data are provided as a Source Data file. | CV 渗透率热图。要点：0% 时后随车减速至 0 m/s（拥堵/振荡），100% 时编队"gradually stabilizes"。 |
| {FIG-nc-platoon-8} | Fig. 8 | Average dampening ratio, driver comfort cost, energy consumption cost and flow stability of six vehicles for random delays. Center blue lines of the boxes represent the median. Vehicle 1… | **随机时延 100 次实验**的箱线图（4 指标 × 6 车）。要点：中位数被明确标注，但**无四分位数值、无 CI**；第 6 车中位数优于前方传统车（3–5 号）。 |
| {FIG-nc-platoon-9} | Fig. 9 | Averaged performance indicators for different platoons with different number of vehicles. The oscillation dampening, driving comfort cost, energy consumption and flow stability with the… | 编队规模扫描（混行 vs 全 HV 对照）。要点：随车数增加，能耗/舒适/阻尼比"先缓升后降"；同规模下含 CV 者更优——**规模可扩展性**的唯一证据。 |
| {FIG-nc-platoon-10} | Fig. 10 | Position profiles of a mixed platoon in the presence of lane changing behavior of an HV (in red) under CVDS-IDM, DDPG, PPO and the proposed SAC strategy. CV = connected vehicle… | 换道扰动算例（6 车 = 3 CV + 3 HV，红色 HV 于 4 s 汇入、40 s 驶离）。要点：曲线交叉=碰撞。**图注 g–i=PPO、j–l=本文 SAC，与正文引用不一致（见文末 ⚠）**。 |
| {FIG-nc-platoon-11} | Fig. 11 | The algorithm procedure of knowledge-guided self-learning mixed platoon control framework. CV = connected vehicle. HV = human-driven vehicle. SAC = soft actor-critic. | **本卡最重要的一张图**：左侧"知识引导"支路显式写出 d_{i−1,i−n}=H·v+L 与 L=w_v·H 的估计流程、标出 "k HVs (0≤k≤m, k=n-1)"；右侧为 SAC 网络与状态构成（空间偏差、相对速度、上一拍指令、随机时延）。 |
| {TAB-nc-platoon-1} | Table 1 | Performance comparison under different permeability | 渗透率 0/20/40/60/80/100% × 四指标（g_p、j_jerk、e_eco、f_flow）的六行数值表。**全文唯一的表**，也是"CV 渗透率↑→指标单调改善"的唯一定量依据。 |

## 6. 对 P1 的用处

- **与 P1 的关系**：**直接回答**（同一个 ODD 族：高速公路、人工与自动混行的**编队纵向控制**，且给出可复用的闭环评价协议）。**但范式不同**：它是离散时间 SAC + 云控 + 路侧宏观信息，不是连续时间（液态）神经网络；且**完全没有 OTF**。
- **可迁移**：
  1. **四指标评价协议可直接复用**：振荡阻尼比 g_p（式 1）、舒适成本 j_jerk（式 2）、能耗 e_eco（式 3–4）、交通流稳定性 f_flow（式 5），外加上报口径 PIP（式 6）。P1 现有七指标（跟车误差 RMSE、∫a²、jerk 峰值、车道居中偏差、前轮转角方差、端到端时延、MCU 内存）**不含** g_p 与 f_flow —— 这两个恰好是"混行编队振荡抑制"的直接度量，可作为 P1 的补充指标，A1（OTF 开/关）消融可直接在此对标。
  2. **鲁棒性测试矩阵可照搬**：时延 {0.2, 0.5, 1.0, 2.0}ΔT（ΔT=0.1 s）；CV 渗透率 0→100% 每 20%；编队规模扫描 + **全 HV 对照编队**（分离"CV 的贡献"与"规模的贡献"）；人工车参数随机化（白噪声 |w_{i−j}|<1 加在 λ_{i−j}、δ_{i−j} 上）；换道扰动（HV 于 4 s 汇入、40 s 驶离）。这套矩阵与 P1 的长尾清单（前车急刹、cut-in、编队单车退出、激进车流扰动）高度互补。
  3. **真实领头车数据流**：用 NGSIM I-80（16:00–16:15）真实轨迹替代"固定确定性前车"作为领头车——与 P1 用黄梦圆学位论文实车数据回放做扰动源的做法**同构**，可作为 P1 的第二条真实数据流（须遵守 NGSIM 使用条款；注意其"低通滤波重建轨迹"的预处理会改变高频成分，P1 引用时须说明）。
  4. **代码与数据可得**：CodeOcean capsule 7637528（DOI 10.24433/CO.4294963.v1）+ Source Data → 可用于复算其统计口径、抽取其四指标实现作为 P1 的对照实现。
  5. **作为 Related Work 里"先验注入"的对照项**：其 knowledge 是**宏观交通流守恒关系**，与 P1 的启发式 OTF 势场形成"有可判真伪残差的先验 vs 无可判真伪残差的先验"这一对照——**这正好是 P1 论证"不宜自称 physics-informed"的现成反例素材**（见下文 ★③）。
- **不可迁移 / 陷阱**：
  1. **不是势场，也不是连续时间控制器**：它的 "knowledge" 只生成**期望间距参考 d\***，注入点在**参考生成**（式 21–24 + 式 33–34 的数据融合），不在 ODE 边界条件、也不在损失项。→ P1 若把 OTF 势场作为 ODE 边界条件，与它是**两种不同的注入点**，**不得写成"同类做法"或"与本文类似"**。
  2. **ODD 窄于 P1**：Methods 逐字 "an infinite single straight highway is considered, and the lateral motion of the vehicle is ignored"。**单车道、无侧向**。P1 的"多车道 + 车道居中偏差 + 前轮转角方差"三项它一项都不覆盖；换道只作为**外生扰动**（HV 汇入/驶离），不是被控对象。
  3. **不是实车**：全篇数值仿真；NGSIM 仅用作领头车轨迹输入（"Instead of a fixed deterministic leader, NGSIM data is utilized to represent the leader's behavior"）。P1 引用其任何数字必须写"**文献报告值，仿真协议，未经我们复现**"（`AGENTS.md` §1 第 4 条）。
  4. **基线被作者改写**：逐字 "we have extended PPO37, DDPG40, AC44, and CVDS-IDM strategies48 to fit the proposed framework and have made appropriate modifications to them"。→ 其 PIP 的 20 个百分点级优势**不是**原论文实现的成绩，**不可**作为"某算法在混行编队上的公开性能"引用；P1 若拿 TD3 直控与它对比，属于**跨协议拼接**。
  5. **无统计不确定度**：20 组数据平均 + 100 次随机时延实验 + 箱线图中位数，**无种子、无重复次数、无 CI、无检验**。因此 PIP 中 1.03%（对 DDPG，第 2 车阻尼比）、1.06%（对 DDPG，能耗）、2.55%（对 AC，第 6 车流稳定）这类**个位数百分比在无不确定度下不能声称差异**；原文写 "significantly outperforms"，但**没有显著性检验支撑**。按全局 `AGENTS.md` §1 铁律 2（措辞强度不得超过证据等级），P1 引用时只能写"作者报告其 SAC 在多数指标上更优"。
  6. **碰撞证据是目视的**：Abstract 的 "zero collision rate" 在正文只能追到 Fig. 10 的 "no instances of curve intersections"；**无碰撞判据、无分母**（每公里 / 每次汇入机会）。不得转写成 P1 可比的碰撞率。
  7. **与 P1 的资源指标无对标接口**：它**未报告**端到端时延与内存/参数量；其"云平台"假设（高性能计算 + 弹性存储）与 P1 的车载/CfC 定位相反。→ 不得从它推断任何 CfC 侧的资源优势。
  8. **它是集中式云控**：控制指令由云生成再经 V2X 下发（式 14 的 u_i(t−ε)）。P1 若主张"零额外传感器成本 / 车载可部署"，与它的架构前提不同，**不是同一个部署约束下的比较**。
- **引用时必须带的限定语**：**"在单车道、显式忽略侧向运动的数值仿真中，以 NGSIM 加州 I-80（16:00–16:15）真实轨迹为领头车、以最优速度模型生成人工驾驶车、默认 20 ms 常数通信时延、7 车编队（其中 2 辆受控网联自动车），作者报告其知识引导 SAC 控制器在阻尼比、舒适、能耗、流稳定四项上优于其**自行改写**的 CVDS-IDM、DDPG、AC、PPO 对照；全部结果未经我们复现，且未报告种子数、重复次数与任何不确定度，亦无实车验证。"**

### ★ 特别要求逐项（本批次指定）

**① 编队规模 n 与受控车数 m**：子编队结构为 "CV-HVs-CV"，**n+1 辆车 = 1 辆领先 CV（索引 i−n）+ (n−1) 辆人工车 + 1 辆受控跟随 CV（索引 i）**，约束 "1 ≤ n ≤ m"；Fig. 11 标注 "k HVs (0≤k≤m, k=n-1)"。→ **每个子编队只控 1 辆车**。仿真算例为 **7 车**（领头车与第 2、第 6 车为 CV，其余 4 辆为 HV），**受控车 = 2 辆**（"Besides the leading vehicle, all autonomous vehicles are controlled by the proposed strategy"）；扩展算例把 CV 置于"领头 + 第 2 + 最后一辆"；换道算例为 6 车（3 CV + 3 HV）+ 1 辆红色 HV 于 4 s 汇入、40 s 驶离。训练时人工车数在 "0 ≤ n−1 ≤ m−1" 内随机采样（⚠ 与 Fig. 11 的 k≤m 差 1，见文末内部不一致）。

**② 时延的具体数值与来源**：**默认常数 20 ms** —— 逐字 "The communication delay is set to a constant value of 20 ms by default."；鲁棒性扫描取集合 **{0.2ΔT, 0.5ΔT, 1.0ΔT, 2.0ΔT}，ΔT = 0.1 s**（即 0.02 / 0.05 / 0.10 / 0.20 s）。**来源**（Methods "Optimization problem under communication delay"）：总时延按四个分量求和 **ε = ε₁ + ε₂ + ε₃ + ε₄** —— ε₁ 云控器生成控制指令、ε₂ 云服务器→路侧单元、ε₃ 路侧单元→执行器、ε₄ 执行器处理指令；并写成 **ε ∈ [zΔT, (z+1)ΔT)，z 为正整数**，离散域为 x(k+1) = e^Φ x(k) + e^Ψ₁ u(k−z) + e^Ψ₂ u(k−z−1)（式 19）。随机时延的分布见 **Supplementary Fig. 1**（**本次未取得补充材料，分布形式与 z 取值范围未核实**）。应对手段两件：把上一拍控制指令并入 SAC 状态（式 35：s_i = [Δd̃_i, Δṽ_i, u_i(1), …, u_i(z+1)]）+ 按 z 分段的多模型切换机制（云侧存储多个网络模型，用收/发时间戳 T_R − T_T 实时检测时延后选模型）。

**③ "knowledge-guided" 里的 knowledge 究竟是什么（是不是势场/物理先验？与 P1 的 OTF 势场什么关系）**：
- **它是什么**：**不是势场、不是可微物理残差**。它是**宏观交通流理论先验**：运动波模型 w_v = 1/(h·c_d) 与 c_d = 1/l（式 25–26，w_v 平均运动波速、l 阻塞间距、h 波传播时间、c_d 阻塞密度）+ Newell 跟驰模型，用来把 n−1 辆人工车的**聚合行为**压成两个标量函数：期望时变车头时距 H_{i−1,i−n}(t) = d_{i−1,i−n}(t) / (w_v + v_{i−1}(t))（式 27）与期望静止间距 L_{i−1,i−n}(t) = w_v · H_{i−1,i−n}(t)（式 28），再经式 23–24 求和、式 21 得期望间距 d\* = H·v + L。输入量 w_v（交通波速）与阻塞密度由**路侧单元采集后上云**。
- **与 P1 的 OTF 势场的关系（必须写清，三点）**：
  **(a) 相同点**——都是"**把外部先验注入学习型控制器**"，且该文自述动机与 P1 一致：逐字 "by integrating prior knowledge such as the kinematic wave model and Newell's car-following model into the learning process, we can guide the learning more effectively and improve efficiency"。
  **(b) 不同点 1（数学形态）**——它是**宏观守恒关系**：w_v = 1/(h·c_d)、c_d = 1/l 是**可测量、可判真伪**的交通流量，H = d/(w_v+v) 有明确的量纲与物理含义，可以被实测数据证伪；而 **OTF 势场是启发式社会压力标量，不存在可判真伪的残差**。
  **(c) 不同点 2（注入点）**——它在**参考/目标生成**处注入（先算出 d\* 再喂给 RL），**不在 ODE 边界条件、也不在损失项**；P1 若把 OTF 作为 ODE 边界条件，是**另一种注入机制**。
  **(d) 不同点 3（作用对象）**——它用先验**预测他人**（聚合 HV 的行为）；P1 用 OTF **刻画自身所处的交通社会压力**。前者是"预测模块"，后者是"条件模态/归纳偏置"。
  → **对 P1 的直接后果（两条）**：**(i)** 这篇文章是 `AGENTS.md` §1"不宜自称 physics-informed"的**正面参照**——它的先验挂着交通流守恒方程，比 OTF 势场更接近 "physics-informed"；P1 的 OTF 更应定位为 **structure-informed / prior-informed / boundary-conditioned，并把 OTF 定位为 inductive bias**。**(ii)** 它**从未做"knowledge 开/关"的消融**（全文没有移除运动波模块的对照设置）——这正是 **P1 的 A1 消融（OTF 开/关）相对它的净增量之一**。

**④ 弦稳定性是否报告、用什么判据**：**未报告。全文没有弦稳定性判据。** 核验方式：在该 txt 中 grep `string stab` **只命中参考文献 [25] 的标题**（"Impacts of communication delay on vehicle platoon string stability and its compensation strategy: A review"），**正文零命中**；grep `Lyapunov` 亦零命中。它报告的是**另外两个**指标：振荡阻尼比 g_p（式 1，第 i 车与领头车加速度的 L2 范数比）与交通流稳定性 f_flow（式 5，速度变化量/间距的归一化和，越大越稳）；另有 "local stability" 仅作为优化目标中跟踪误差项的定性描述（"the smaller its value, the stronger the local stability of the system"），**无传递函数、无 ‖H(jω)‖∞、无 Lyapunov 分析、无 head-to-tail 放大率**。

### 闭环 / 实车 / 统计（逐字证据）

- **有没有闭环**：**有，但是仿真闭环**。逐字："During training, the SAC algorithm continuously interacts with the traffic environment, generating actions to apply to the system model." 其"环境"即式 (19) 的离散误差动力学 + 最优速度模型驱动的人工车。**闭环的环境是 ODE 仿真，不是交通仿真器，更不是实车。**
- **有没有实车**：**没有**。全文无 hardware / field test / test vehicle 字样。最接近实车的只有 NGSIM 真实轨迹作为**领头车输入**。作者自承（Discussion 末句）："Future research could focus on applying the proposed framework to real-world vehicle platoons, further enhancing the robustness and adaptability of the control strategy."
- **有没有统计检验 / CI / 种子**：**三者皆无**。逐字证据（全部统计手段仅此两处）：① "We firstly average the six following vehicles' performance indicators in the platoon as a representation of the whole platoon, and then calculate the average results across 20 datasets to ensure statistical robustness."；② "A total of 100 simulation experiments were conducted under random delays, and the experimental results are shown in Fig. 8."，而 Fig. 8 图注为 "Center blue lines of the boxes represent the median."（箱线图，中位数）。**grep `seed` 零命中，无 p 值，无 95% CI，无标准差报告，无重复次数说明。**

## 7. 缺失信息（≥3 条，写成可执行动作）

1. **取补充材料并回填本卡 §8**：Supplementary Table 2（默认实验参数：z 取值、m 取值、Q/W/C/D 权重、λ/δ 与白噪声幅值）、Supplementary Algorithm 1（SAC 伪代码）、Supplementary Fig. 1（随机时延分布）、Supplementary Fig. 2（低通滤波效果）**均不在本次全文 txt 中**。→ **动作**：从 `https://doi.org/10.1038/s41467-025-62597-x` 下载 Supplementary Information PDF，提取后补入本卡 §8 与 ★② 。
2. **查清"20 datasets"的构造**：正文只给了 NGSIM I-80 的 16:00–16:15 一段，"20 datasets"如何划分、是否重叠、是否固定随机种子**均未说明**，而这直接决定 PIP 的可信度。→ **动作**：拉取 CodeOcean capsule 7637528（DOI 10.24433/CO.4294963.v1）的脚本与数据清单，确认分割逻辑与 seed；若无法确认，P1 引用时写"论文报告值，未给不确定度与样本构造"。
3. **补弦稳定性**：全文无弦稳定性判据（★④）。→ **动作**：以该文式 (18) 的状态空间自行数值计算含时延项 exp(−εs) 的传递函数 ‖H(jω)‖∞，或直接取 CodeOcean 代码中的 Φ、Ψ 计算；结果作为 **P1 自己的计算值**报告，**不得写成"该文报告弦稳定性提升"**。
4. **算清碰撞判据与分母**：Abstract 的 "zero collision rate" 无判据、无分母。→ **动作**：从 Source Data 复算最小车头间距与 TTC 分布，得到可报告的分母（每公里 / 每次汇入机会）；或向通讯作者（Jinghua Guo, guojh@xmu.edu.cn；Keqiang Li, likq@tsinghua.edu.cn）索取碰撞判定阈值。
5. **对齐 m 的口径**：需确认 m 是"最大人工车数"还是"最大编队车数"（正文训练段写 0 ≤ n−1 ≤ m−1，Fig. 11 写 k ≤ m）。→ **动作**：查 Supplementary Table 2 或 CodeOcean 代码中的采样区间；在此之前 **P1 不得引用 m 的任何具体数值**。
6. **补计算/部署成本**：全文未报端到端时延与内存/参数量，故 P1 的"端到端延迟""MCU 内存占用"两项与它**无对标接口**。→ **动作**：若要对比，只能在 P1 自己的平台上实测，并按 `AGENTS.md` §3 记录 MCU 型号、编译器与优化选项；**不得**从该文推断任何资源结论。
7. **核对 VoR 与 Source Data 的数字一致性**：本卡的 Table 1 六行 × 四列与 16 个 PIP 百分比**取自正文文字，未与 Source Data 文件逐格比对**。→ **动作**：下载 Source Data，逐格复核；尤其复核 Fig. 4a 的 "0.7 to 0.54" 是否可从数据复现。
8. **确认图号错位是排版错误而非版本差异**（见文末 ⚠）：→ **动作**：对照 VoR 排版的 Figs. 3 与 10 分栏标注；若 VoR 中确实为 e=PPO / g–i=PPO，则本卡按 VoR 记为"正文引用错误"，P1 引用时**只引图注字母所指的曲线**。

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 默认通信时延（常数） | 20 ms | 未报告 | Results（"Comparison results between different control algorithms"） |
| 时延鲁棒性扫描集合 | {0.2ΔT, 0.5ΔT, 1.0ΔT, 2.0ΔT}，ΔT = 0.1 s（= 0.02/0.05/0.10/0.20 s） | 未报告 | Results（"Robustness validation"） |
| 时延分量构成 | ε = ε₁+ε₂+ε₃+ε₄（云控生成 / 云→路侧 / 路侧→执行器 / 执行器处理） | 未报告 | Methods（"Optimization problem under communication delay"） |
| 仿真算例编队规模 | 7 辆车（CV = 第 1/2/6 辆；其余 4 辆 HV） | — | Results |
| 受控车数（该算例） | 2 辆 | — | Results |
| 训练时人工车数采样范围 | 0 ≤ n−1 ≤ m−1 | — | Methods（"Training procedure"） |
| 换道扰动算例 | 6 车（3 CV + 3 HV）+ 1 辆 HV 于 4 s 汇入、40 s 驶离 | — | Results（"Robustness against the disturbance…"） |
| 全部车辆初始速度 | 11 m/s | — | Results |
| 统计平均的数据集数 | 20 | 未报告 | Results（PIP 段） |
| 随机时延实验次数 | 100 | 未报告 | Results（"The switching DRL-based model mechanism"） |
| Table 1: g_p（0% → 100% 渗透率） | 0.7309 → 0.3862（20%: 0.5974；40%: 0.5228；60%: 0.4510；80%: 0.4115） | 未报告 | Table 1 |
| Table 1: j_jerk（0% → 100%） | 0.4341 → 0.1381（20%: 0.2913；40%: 0.2296；60%: 0.1767；80%: 0.1522） | 未报告 | Table 1 |
| Table 1: e_eco（0% → 100%） | 2.0357 → 1.3461（20%: 1.6581；40%: 1.5196；60%: 1.4049；80%: 1.3603） | 未报告 | Table 1 |
| Table 1: f_flow（0% → 100%） | 0.2238 → 0.2433（20%: 0.2275；40%: 0.2311；60%: 0.2354；80%: 0.2393） | 未报告 | Table 1 |
| 累计阻尼比（本文 SAC） | 由 0.7 降至 0.54 | 未报告 | Results（Fig. 4a 正文） |
| 第 2 车 PIP 阻尼比（对 DDPG/CVDS-IDM/PPO/AC） | +1.03% / +7.68% / +21.10% / +13.40% | 未报告 | Results |
| 第 2 车 PIP 舒适（同上顺序） | +2.06% / +14.77% / +30.04% / +25.01% | 未报告 | Results |
| 第 2 车 PIP 能耗（同上顺序） | +1.06% / +9.14% / +15.56% / +18.72% | 未报告 | Results |
| 第 2 车 PIP 流稳定（同上顺序） | +16.22% / +19.23% / +8.14% / +22.27% | 未报告 | Results |
| 第 6 车 PIP 阻尼比（同上顺序） | +9.47% / +16.15% / +32.06% / +26.44% | 未报告 | Results |
| 第 6 车 PIP 舒适（同上顺序） | +18.05% / +29.70% / +53.84% / +45.89% | 未报告 | Results |
| 第 6 车 PIP 能耗（同上顺序） | +9.05% / +16.54% / +27.54% / +25.94% | 未报告 | Results |
| 第 6 车 PIP 流稳定（同上顺序） | +17.49% / +25.30% / +8.46% / +2.55% | 未报告 | Results |
| 第 2 车最大加速度幅值（约 12 s） | "reaches nearly 1.5"（原文未标单位） | 未报告 | Results（"Robustness validation"） |
| 碰撞率 | "a zero collision rate in vehicle merging and diverging scenarios"（**无判据、无分母**） | 未报告 | Abstract |
| SAC 网络结构 | actor 输入 z+3、两层隐藏层 128/64；critic 输入 z+4 | — | Methods（"Neural network structure"） |
| 数据来源 | NGSIM 加州 I-80 项目，16:00–16:15（低通滤波重建轨迹） | — | Methods（"Data preparation"） |
| 代码/数据 DOI | 10.24433/CO.4294963.v1（CodeOcean capsule 7637528） | — | Code availability |
| 弦稳定性判据 | **全文未见**（grep `string stab` 仅命中参考文献 [25] 标题） | — | 本卡核验 |
| 端到端时延 / MCU 内存 / 参数量 | **全文未见** | — | 本卡核验 |

---

⚠内部不一致：正文把本文方法的性能归给 "Fig. 3e"（"In contrast, the proposed algorithm demonstrates exceptional performance (Fig. 3e)"），但 Fig. 3 图注为 "e Simulated results using PPO. f Simulated results using the proposed SAC strategy." —— 所指应为 Fig. 3f。

⚠内部不一致：正文写 "Traditional DRL algorithms, such as PPO and AC … As shown by the position curves of Fig. 3c and d, collisions even occur during operation"，但 Fig. 3 图注中 3c = DDPG、3d = AC；被点名的 PPO 在 Fig. 3 里是 3e。方法与图号不符。

⚠内部不一致：正文写 "In Fig. 10g–l, all vehicle trajectories remain stable and gradually increase, maintaining consistent relative positions."（指本文 SAC 无碰撞），但 Fig. 10 图注为 "g–i PPO. j–l The proposed knowledge-guided self-learning SAC strategy." —— g–i 属 PPO，本文 SAC 仅 j–l。

⚠内部不一致：人工车数上界。Methods 训练段写 "the number of human-driven vehicles (0 ≤ n−1 ≤ m−1) is randomly sampled"，而 Fig. 11 标注 "k HVs (0≤k≤m, k=n-1)"；k = n−1 时两式上界相差 1。

⚠内部不一致（术语与出处归属）：正文写 "as specified by the Association of Automotive Engineers standard39,43,44"，但同一篇文章前文把 SAE 展开为 "SAE (Society of Automotive Engineers)"；且所引文献 39 / 43 / 44 分别是 IEEE T-ITS 2023、IET Intell. Transp. Syst. 2024、IEEE Veh. Technol. Mag. 2023 的论文，**均非 SAE 标准**。

---
**字数实测**：§2 摘要 = 253 汉字（含中文标点 289）；§3 结论 = 222 汉字（含中文标点 276）；§4 方法一句话 = 39 汉字（含中文标点 41）。
**取用记录**：Crossref `works/10.1038/s41467-025-62597-x`，取用日 2026-10-06，HTTP 200（更正/撤稿检查，见页首）。
