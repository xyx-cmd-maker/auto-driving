# 停走波对学习型跟驰控制训练的影响｜Implications of Stop-and-Go Traffic on Training Learning-Based Car-Following Control

- **出处**：**本次精读材料 = ISTTT 25 会议版**：25th International Symposium on Transportation and Traffic Theory (ISTTT 25), 15–17 July 2024, Ann Arbor, Michigan, United States（**首页逐字**，见下 §"材料版本判定"），33 页，**会议版文件内无 DOI** ｜ **对应的期刊版**：*Transportation Research Part C: Emerging Technologies*, 2024, **168: 104578**，DOI **10.1016/j.trc.2024.104578**（2024-11）｜ **类型**：**会议论文（ISTTT 25）**；同名期刊版**已存在**，**本次未取得期刊版全文**
- **作者**：Zhou A, Peeta S, Zhou H, et al.（n=**6**；全文署名逐字：Anye Zhou^a, Srinivas Peeta^b,*, Hao Zhou^b, Jorge Laval^b, Zejiang Wang^a, Adian Cook^a —— ^a Oak Ridge National Laboratory，^b Georgia Institute of Technology。**Crossref 期刊版作者序一致**：Zhou, Peeta, Zhou, Laval, Wang, Cook。通讯作者逐字：peeta@gatech.edu）
- **DOI**：**本次材料（会议版）无 DOI**；**对应期刊版 DOI：10.1016/j.trc.2024.104578**（逐字，Crossref 返回）
- **全文来源**：`literature/fulltext/fresh2024/trc2024-stopandgo-learning-cf__b0668d39.txt`（PAGES=33, CHARS=90,755）｜ **材料版本**：见下方"★★ 材料版本判定（逐字证据）"
- **分组**：2024+ 增量
- **证据等级初判**：**C 级** — 理论部分是定理/引理级（数学证明，A 级成分）；实验部分是**纯数值仿真**（无实车、无实测数据），但**有 20 次重复训练并报告了方差与 95% CI**（就重复性而言**强于**项目既有 #43 Stern 2018 的单次运行），关键结论（DRL 跨数据集"无显著差异"）**只由图给出、未印出任何统计量**，且用"95% CI 重叠"当作"无显著差异"，**未做等价/非劣检验**
- **档位建议**：**B** — 理论框架（PE 阶 ↔ 训练数据集设计）与"BC 需要含停走波的全面数据集、DRL 用自由流即可泛化"这一结论对 P1 的**训练数据设计与基线论证**有直接价值（D1=1，属相邻环节），仿真 + 单受控车 + 单向耦合限制了迁移上界
- **五维打分（各维 0–2，满分 20）**：D1=1 D2=1 D3=1 D4=2 D5=1 → 加权 = **13**

  | 维度 | 分 | 依据 |
  |---|---|---|
  | D1 问题吻合 | 1 | 给的是 P1 **相邻环节**——学习型跟驰控制器的**训练数据集/环境设计**（BC 与 DRL 两条路线的泛化性），并含 P1 需要回应的 TD3/DRL 基线论证；**不是** P1 的控制器本体，也不是同 ODD 闭环评价协议 |
  | D2 设计强度 | 1 | 定理引理齐全 + **20 次重复训练**（PPO/SAC）+ NGSIM 1341 条轨迹测试 + 95% CI；但**全部为仿真**（无实车），**单受控车、单向耦合**（前车轨迹外生）→ "仿真/单组"= 1 |
  | D3 可迁移性 | 1 | PE 阶 → 训练数据充分性的**分析框架**可迁移（P1 可直接借来论证训练集设计）；但训练数据是**自行合成的正弦叠加**，无数据集发布、**无代码可用性声明** |
  | D4 时效性 | 2 | 2024 年，检索上界 2026-10-04，≤5 年 |
  | D5 完整性 | 1 | 超参表（Table 2/3/4）、图注、物理方程均给出；但**无代码/数据/环境开源**，且**多处关键结果只有图、无统计量**（含 DRL 四数据集对比的 95% CI 数值） |

  **加权核算**：3×1 + 2×1 + 2×1 + 1×2 + 2×1 = 3+2+2+2+2 = **13**（→ 协议 §5 档位：加权 9–13 且 D1=1 → **B 略读**；A 档要求 D1=2，本篇不满足）

- **★ 正式版核验**
  - **核验方式与日期**：Crossref `https://api.crossref.org/works?query.bibliographic=Implications%20of%20Stop-and-Go%20Traffic%20on%20Training%20Learning-Based%20Car-Following%20Control&rows=3`（**2026-10-04**）。
  - **返回（首条即命中，逐字段）**：
    - title：`Implications of stop-and-go traffic on training learning-based car-following control`
    - container：`Transportation Research Part C: Emerging Technologies`
    - type：`journal-article`；DOI：**`10.1016/j.trc.2024.104578`**
    - issued：**2024-11**；volume：**168**；issue：空；page：**104578**；article-number：**104578**
    - authors：**Zhou, Peeta, Zhou, Laval, Wang, Cook**（6 人，与本次会议的 6 人**逐一对应、序相同**）
  - **结论**：**该工作已有正式版（期刊版）**。→ 按 `00-scope.md` §2.2"若存在正式版：以正式版为准"，**P1 引用须用 TR-C 168:104578 版**；本次精读的 ISTTT 会议版作**内容补充**（会议论文集通常为 6–12 页，但不适用本文——本文 33 页，见下）。
  - ⚠ **两点须下游注意**：① 会议版**无 DOI**，且**我未从本次材料中取得任何 DOI 字样**；② **会议版与期刊版的数值是否完全一致，未核**（未取期刊版 PDF）——**不得假定逐字相同**。

### ★★ 材料版本判定（逐字证据）：本次手上是 **ISTTT 25 会议版**，不是 TR-C 期刊版

| 判据 | 逐字证据（本次材料） | 指向 |
|---|---|---|
| 页眉 / 首页标识 | 第 9 行逐字：`25th International Symposium on Transportation and Traffic Theory, ISTTT 25, 15-17 July 2024`；第 10 行：`Ann Arbor, Michigan, United States` | **会议版**（会议名、届数、日期、地点齐全） |
| 期刊版式特征 | 全文**无** TR-C 页眉/页脚、**无** "Transportation Research Part C" 字样出现在版式区（仅在参考文献中作为被引期刊名出现）、**无** Elsevier 的 article-number / "Contents lists available at ScienceDirect"、**无** DOI 行 | **非期刊版** |
| 页数 | `PAGES: 33`，页脚为 `===== PAGE n =====` 至 33；正文行号在每页**重新编号**（1,2,3…），是投稿/会议模板特征 | **会议版**（TR-C 期刊版不会 33 页且行号逐页重置） |
| 资助声明特征 | 第 2465–2484 行逐字：`This manuscript has been authored in part by UT-Battelle, LLC, under contract DE-AC05-00OR22725 with the US Department of Energy (DOE)...` 与 DOE Public Access Plan 链接（`http://energy.gov/downloads/doe-public-access-plan`） | **实验室稿件（manuscript）用语**，与"已被期刊接受、走 DOE 公共获取通道"相容，但**该段本身不标明期刊名** |
| 版本对应关系 | 题名 `Implications of Stop-and-Go Traffic on Training Learning-Based Car-Following Control` ↔ Crossref 期刊版 `Implications of stop-and-go traffic on training learning-based car-following control`：**仅大小写与连字符差异**（"Car-Following" ↔ "car-following"）；作者 6 人同序；DOI `10.1016/j.trc.2024.104578`、卷 168、页/文章号 104578、2024-11 **逐项对应** | **同一工作的会议版 ↔ 期刊版** |

→ **判定结论**：**手中这份是 ISTTT 25 会议版**（arXiv/期刊版的对应关系已由 Crossref 字段逐项确认）。**引用时以 TR-C 168:104578 为准；本卡片的一切内容取自会议版，若期刊版有数值修订则本卡片需回改。**

---

## 1. 标题 / 2. 摘要（≤400 字） / 3. 结论（≤350 字） / 4. 方法一句话（≤60 字）

**1. 标题（逐字）**：`Implications of Stop-and-Go Traffic on Training Learning-Based Car-Following Control`（PDF 提取时题名跨行断词为 "Car-" + "Following"，本卡片按原文还原为 "Car-Following"）

**2. 摘要（≤400 字，中文）**

学习型跟驰控制（LCC）的无模型架构有潜力超过基于模型的跟驰模型，但其**在与训练环境/数据集不同的交通条件下的泛化性仍不清楚**。本文探究**训练数据集中的停走交通**对 LCC 泛化性的影响：用**前车轨迹特征**刻画停走交通，把系统辨识的**可辨识性理论**与**行为克隆（BC）**和**深度强化学习（DRL）**的泛化性联系起来。理论证明：(i) 停走交通**能实现可辨识性并提升 BC 型 LCC 的性能**；(ii) 停走交通**对 DRL 泛化并非必需**；(iii) **仅用匀速轨迹训练的 DRL 仍可泛化**；(iv) 停走交通**增大训练集方差**，改善参数估计收敛，却**对 DRL 收敛到最优策略有负面影响**。数值实验验证：BC 需全面的训练数据集才能泛化，DRL 用简单自由流环境即可泛化。作者据此建议 DRL 是更具成本效益的 LCC 路线。

**3. 结论（≤350 字，中文）**

- **主线**：把"训练数据够不够"归为**持续激励（PE）阶**。辨识**二阶**线性跟驰模型需 **PE 阶 ≥ 4**；**停走交通含 ≥2 个振荡频率即可满足**；波动越大 → **方差越大**。
- **BC 侧**：停走波方差在权重更新上**起正则化作用**，提升泛化性。
- **DRL 侧**：高方差经奖励传入 Q 值与策略梯度，形成**方差递增回路致训练失败**；其探索本身提供任意阶 PE。
- **实验**：排序 **拥堵(6, 43.69) > 梯形(4, 34.98) > 线性(1, 27.32) > 匀速(0, 0)**；BC 的 MSE 在匀速集**最大**、拥堵集**最小**；DRL 各训练 **20 次**。
- **立场**：BC 需含停走波的全面数据集，**DRL 用自由流环境即可泛化**。

**4. 方法一句话（≤60 字）**：用 PE 阶把前车轨迹特征换算成训练数据充分性，在 BC 与 DRL 两侧推导并仿真验证。

---

## 5. 图表清单（占位符）

> **会议版编号，期刊版可能不一致**（未比对）。全文 **10 幅图 + 4 张表**。

| 编号 | 图注（逐字） | 页（会议版） | P1 用途 |
|---|---|---|---|
| Figure 1 | Comparison between CF parameter estimation and BC-based LCC. | — | 【占位符】把参数估计与 BC 训练并列（论证桥梁） |
| Figure 2 | Loop illustrating training failure. | — | 【占位符】DRL 方差递增回路（奖励→Q 值→策略梯度→更差策略） |
| Figure 3 | Examples of lead vehicle trajectory and power spectrum | 20–21 | 【占位符】4 类前车轨迹 (a)(c)(e)(g) 与对应功率谱 (b)(d)(f)(h) |
| Figure 4 | MSEs of BC-based LCC trained using different datasets. | 22–23 | 【占位符】6 子图：加速度/速度/位置的 MSE × 两种 DNN 结构 |
| Figure 5 | Comparison of DRL training under free-flow and congested traffic. | 25 | 【占位符】(a) PPO (b) SAC；均值曲线 + 方差阴影（**这是本篇唯一给"方差"的图**） |
| Figure 6 | Impact of increased oscillatory magnitude and frequency on DRL training. | 26 | 【占位符】(a) PPO (b) SAC |
| Figure 7 | Impact of exploration on DRL training. | 26 | 【占位符】(a) PPO (b) SAC；无探索 / 正常探索 / 过度探索 |
| Figure 8 | Performance comparison of DRL-LCC trained with different datasets. | 27 | 【占位符】(a) Spacing (b) SS norm (c) TTC (d) Jerk，四张箱线图（**"无显著差异"的依据**） |
| Figure 9 | Performance of PPO trained using constant-speed dataset. | 27–28 | 【占位符】(a) 加速线型 (b) 减速线型 (c) 梯形 (d) 拥堵 (e) 正弦 (f) NGSIM 速度跟随 |
| Figure 10 | Performance comparison of DDPG and EIDM-guided DDPG. | 28 | 【占位符】EIDM 正则化引导的 DDPG vs 无正则化 DDPG |
| Table 1 | PE order and variance of lead vehicle trajectories | 21 | 【占位符】**核心数字表**（Constant 0/0；Linear 1/27.32；Trapezoidal 4/34.98；Congested 6/43.69） |
| Table 2 | Hyperparameters of BC-based LCC | 22 | 【占位符】lr 0.0001；batch 64；epochs 80；线性层维度 32 |
| Table 3 | Hyperparameters of PPO | 24 | 【占位符】actor lr 0.0001；critic lr 0.0002；**Episode 600**；clip 0.2；熵系数 0.05；折扣 0.99；初始策略方差 0.6；方差衰减率 0.05；衰减频率 10000；最小动作标准差 0.01；权重更新频率 500；价值函数系数 0.5；surrogate 系数 1；actor 线性层 64；critic 线性层 32 |
| Table 4 | Hyperparameters of SAC | 24 | 【占位符】actor lr 0.0001；critic lr 0.0002；**Episode 600**；batch 32；回放容量 320000；每步更新 2 次；折扣 0.99；软更新系数 0.95；熵系数 0.15（表中另标 0.05，**原表同时列两处熵系数**）；actor 线性层 64；critic 线性层 32 |

---

## 6. 对 P1 的用处（含 **与对应层 3 笔记的关系**）

> 本卡片主要对应层 3 笔记 `literature/notes/p43-dissipation-trc2018.md`（Stern 等 2018，停走波消散）。另与 `literature/notes/p01-cfc-nmi2022.md`（CfC 原文）间接相关（P1 的控制器训练范式），本卡片不重复其结论。

### ① 停走波数据/场景怎么构造（**仿真？实测？**）——逐字答案：**纯仿真合成，不是实测**

- **构造式（逐字）**：`The lead vehicle in the fourth dataset displays stop-and-go movements that are constructed by summing sinusoidal speed profiles with different magnitudes and phase shifts: v₀ + Σ_{i=1}^{4} aᵢ sin(ωᵢ(t + φ))`。
- **参数网格（逐字）**：速度水平 $v_0\in\{0,10,15,25\}$ m/s；幅值 $a_i\in\{1,2,4,8\}$ m/s；角频率 $\omega_i\in\{0.03,0.05,0.08,0.1\}$ rad/s；相移 $\phi\in\{0,10,30,50\}$ rad。**四类前车轨迹数据集**：
  1. **匀速**：35 个速度档（0 → 34 m/s，步长 1 m/s）；
  2. **线性加减速**：加速度 {0.5, 1, 1.5} m/s²、减速度 {−0.5, −1, −1.5, −2} m/s²，加速初速 {0,5,10,20} m/s、减速初速 {10,15,25,35} m/s；
  3. **梯形速度**（加减速循环）：加速度 {0.5,1,2} m/s²、减速度 {−1,−2,−4} m/s²，初速 {5,10,20} m/s；
  4. **拥堵/停走**：上式正弦叠加。
- **是仿真还是实测**：**全部为合成/仿真轨迹**。全文**无实车、无实测数据采集**；唯一的真实数据是**测试**用的 **NGSIM 处理后数据集（1341 条车辆轨迹，引自 Montanino & Punzo 2015）**，且其作用是"displaying significantly different speed fluctuations compared to the four training datasets"——**只做分布外测试**，不参与训练、也不是本文采集的。
- **仿真环境**：车辆跟驰由**离散二阶 CF 方程**推进（逐字式 (48a–c)）：$\delta p_t=\delta p_{t-1}+\delta v_{t-1}dt+0.5(a^{lead}_t-a_t)dt^2$；$\delta v_t=\delta v_{t-1}+(a^{lead}_t-a_t)dt$；$v_t=v_{t-1}+a_t\,dt$，**采样步长 $dt=0.1$ s**。**未说明仿真平台（无 Simulink/SUMO/CARLA 等字样）**，即"自建离散 CF 环境"。

### ② 训练集里"有无停走波"对控制器的**定量影响**

**⚠ 关键事实：本篇几乎所有影响都是"排序 + 图"，印出的数值很少。** 逐条列印出的与未印出的：

| 项 | 是否有印出数值 | 逐字/具体内容 |
|---|---|---|
| PE 阶与方差（Table 1） | **有** | Constant：PE order **0**，Variance **0**；Linear：**1**，**27.32**；Trapezoidal：**4**，**34.98**；Congested：**6**，**43.69** |
| BC 训练/验证损失 | **有（仅一个阈值）** | 四类数据集下 "both the training loss and validation loss ... decay to values smaller than **0.001 m/s²**" |
| BC 的测试 MSE（加速度/速度/位置） | **无**（只有图） | 逐字排序：匀速 **最大** > 线性 > 梯形 > **拥堵最小**；两种 DNN 结构结论一致，DNN 结构 2（含 tanh）使线性与梯形的差距"略微缩小" |
| DRL 训练收敛 | **无**（只有图） | 自由流的 episode reward 收敛到**更大的值**且**方差显著更小**；拥堵训练"**diverges and fails to reach the optimal control policy**" |
| 波动幅值/频率增大的影响 | **无**（只有图，Figure 6） | "leads to **reduced episode reward with increased variance**" |
| 探索的影响 | **无**（只有图，Figure 7） | 无探索 → 困在低奖励、无法改善；**过度探索**（熵系数×10、探索噪声方差×2）→ 奖励降低、方差增大 |
| 四数据集 DRL 的四项指标（spacing、SS、jerk、TTC） | **无**（只有箱线图） | 逐字："display **no significant differences** (i.e., large overlapping regions of 95% confidence interval)"；并称 "The results demonstrate that DRL-based LCC trained using constant-speed lead vehicle trajectories can generalize to traffic congestion" |
| 安全性 | **有（定性）** | "**no collisions or reverse movements occur** during testing" |

- **⚠统计读法警告（P1 不得照抄其措辞）**：作者用"**95% CI 重叠**"直接推出"**no significant differences**"。按项目 `AGENTS.md` §4 与全局铁律，"**无差异**必须用等价/非劣检验"，"CI 重叠 ≠ 无显著差异"更是经典的推断错误（重叠的 CI 仍可能对应显著的组间差）。→ P1 若引用"四种训练集的 DRL 表现无差异"，**必须**写成"该文报告四项指标的 95% CI 大幅重叠，据此认为无显著差异（**未做等价/非劣检验**）"，并且**不得**把它当作"停走波对 DRL 无影响"的阳性证据。
- **可直接用的定量结论（须带限定语）**：**PE 阶与轨迹方差同向**（Table 1：0/0 → 1/27.32 → 4/34.98 → 6/43.69）；**BC 的测试 MSE 排序与 PE 阶反向**（PE 越高、MSE 越小）。这两条是 P1 能引的**唯一带数字的结论**，且都是**仿真内**的。

### ③ 与项目已有 #43（Stern 等 2018 停走波消散）的关系——**是补上了统计缺口，还是又一个单例？**

**结论：补上了一部分，但补的不是同一件事；两者不能互相替代。**

| 对比项 | #43 Stern 2018（层 3 笔记 `p43-dissipation-trc2018.md`） | 本篇 Zhou et al. 2024 | 判定 |
|---|---|---|---|
| 性质 | **真车闭环现场实验**（21–22 辆、单车道环道、260 m） | **纯数值仿真**（1 个受控车 vs 1 条合成前车轨迹） | 证据类型不同，**不可互相替代** |
| 重复 | **每条件 1 次运行，无重复、无种子、无 CI、事后择优区间** | DRL 训练 **20 次**（PPO/SAC），报均值+方差与 95% CI 箱线图；BC 部分**未报重复次数** | **本篇补上了 DRL 训练的重复性缺口**；但**没有补**"停走波真车实验"的重复性缺口 |
| 停走波来源 | **人工驾驶员自发产生**（被指令"跟紧前车"），有 2.5 m/s 瞬时速度标准差判据 | **合成正弦叠加**（作者指定幅值/频率/相移） | 一个是"真实涌现"，一个是"参数化构造" |
| 与 P1 的关系 | P1 的**场景动机**实证源（少量自动车可压制波） | P1 的**训练数据设计**依据（训练集该不该含停走波） | 互补，不重叠 |
| 对 P1 的可引强度 | 方向性结论可引（B 级方向 / C 级幅度），真车 | 训练数据设计结论可引，**仿真**且部分结论**只有图** | 两者都**不能**作为 P1 的性能基线数字来源 |

→ **给 P1 的落笔建议**：把 #43 放"**动机**"（真实交通中波确实自发且稀疏执行器可压制），把本篇放"**方法/训练协议**"（训练集是否必须含停走波；BC 与 DRL 的差异）。**不得**把两者写成一个证据链去支撑"OTF 势场有效"——两篇都**没有**任何 OTF 类信号（本篇尤其：状态仅为 $(\delta p_t,\delta v_t,v_t,a^{lead}_t)$，**无任何社会压力/超车频次项**）。

### ④ 受控车数、编队规模、是否闭环（本卡片须明确的四项）

- **受控车数**：**恰好 1 辆**（"ego vehicle"）。BC 的示范者是 CTH-RV 模型（$a_t=k_s(\delta p_t-hv_t)+k_v\delta v_t$），DRL 的学习者是 1 个 agent。
- **编队规模**：**不是编队**，是**两车**（1 前车 + 1 受控车）的跟驰对。全文**无编队/车队规模概念**（未出现 $m$ 辆车、无沿车队的传播分析）。
- **闭环？** → **对 ego 是闭环**（ego 的加速度反馈影响自身状态与下一状态）；**但纵向是单向耦合、开环激励**：前车加速度 $a^{lead}_t$ **外生给定**（由预生成轨迹提供），**不受 ego 影响**。→ 因此**没有真正的交通闭环**，也没有"多车耦合"或"波在车队中传播/被压制"的闭环效应。**P1 的"编队连续时间控制"是闭环多车系统，本篇不覆盖。**
- **实车还是仿真？** **纯仿真**（合成轨迹 + 自建离散 CF 环境 + NGSIM 离线测试）。**无实车、无场地、无驾驶员、无里程/暴露量。**
- **有无 CI / 显著性 / 种子？**
  - **种子**：**未报告**（全文无 seed 字样——我已 grep 复核 `seed|random` 无命中于实验设置处）。
  - **重复次数**：**DRL 训练 20 次**（逐字 "We conduct the DRL training **20 times** for each training dataset"）；**BC 部分未报告重复次数**。
  - **CI**：**有**（Figure 8 箱线图用 **95% confidence interval**），但**未印出数值**。
  - **显著性检验**：**无**（无 p 值、无假设检验、无等价/非劣检验）；"no significant differences" 是**由 CI 重叠目视得出**的。
  - → 与 #43 相比：**在 DRL 部分有了 20 次重复，是净改善**；但**在 BC 部分与"无差异"的推断上仍是弱点**。

### ⑤ 对 P1 的三条具体可用结论

1. **训练集设计**：P1 的 OTF-CfC 如果用行为克隆/模仿学习，本篇给出**可检验的判据**——前车轨迹的 **PE 阶 ≥ 4** 才保证 CF 参数可辨识；停走波（≥2 个振荡频率）恰好满足。→ P1 应在方法节**报告其训练轨迹的 PE 阶**，并把"训练集是否含停走/拥堵轨迹"作为一个**消融因素**（与 P1 的 A1–A5 消融并列）。
2. **DRL 基线的公平性论证**：本篇结论(iii)（匀速轨迹训练的 DRL 可泛化到拥堵）**对 P1 的 TD3 直控基线有直接含义**——P1 若把 TD3 基线训练在简单自由流环境，本篇是**支持该做法的文献依据**；但必须注明该依据是**仿真 + 单受控车 + 单向耦合**，且其"无显著差异"结论**未做等价检验**。同时提示 P1：**训练集方差是 DRL 的超参维度**（高方差训练数据会经奖励函数传导为训练失败），P1 报告 TD3 基线时应**报告训练数据的方差/PE 阶**，否则基线不可比。
3. **术语与机制可借用**：Lemma 5/6 的"奖励方差经 Q 值估计与策略梯度形成方差递增回路"这一机制，可用于 P1 解释"为何在混行高扰动场景下 DRL 基线不稳"；但**必须**标注为"该文在单受控车仿真中的机制分析"，**不得**写成 CARLA/实车观测。

---

## 7. 缺失信息（≥3 条）

**A. 未报告（缺失影响 + 最小补法）**

1. **未报告：仿真/训练平台与代码。** 全文无 Simulink/SUMO/CARLA 等平台字样，也无 code/data availability 段（仅有 DOE 资助声明与 CRediT 式贡献）。影响：**P1 无法复用其 CF 环境与奖励函数实现**，只能按式 (48)(51) 自行重建。**最小补法**：向作者索取 ORNL 的训练脚本；否则按式 (48) 二阶 CF 递推 + 式 (51) 五项奖励自行实现（**公式足够，可做**）。
2. **未报告：随机种子。** DRL 有 20 次重复但**未报种子**，也未说明 20 次之间变的是什么（策略初始化？探索噪声？前车轨迹采样？）。影响：**无法复现其方差**；Figure 5/6/7 的"方差阴影"含义不可核。**最小补法**：报告 20 次的随机化清单与种子；P1 自身按 `AGENTS.md` §4（种子 ≥5 + mean±std 或 95% CI）执行。
3. **未报告：BC 部分的重复次数与方差。** 只有"训练/验证损失 < 0.001 m/s²"与图 4 的 MSE 曲线。影响：BC 的"MSE 排序"可能是单次训练的结果，**无法判断是否超出运行间波动**。**最小补法**：报告 BC 的重复次数与 MSE 的均值±标准差。
4. **未报告：Figure 8 四项指标的 95% CI 数值与样本量。** 只有箱线图。影响：**P1 无法引用任何数字**，也无法自行判断"CI 重叠"是否真能支持"无显著差异"。**最小补法**：索取四项指标的逐数据集均值、CI 上下界与样本量（NGSIM 的 1341 条轨迹如何用于统计？未说明）。
5. **未报告：NGSIM 测试的使用方式与划分细节。** 逐字只说"processed NGSIM trajectory dataset (Montanino and Punzo, 2015) with **1341 vehicle trajectories** is used for testing"。影响：**同一批 1341 条轨迹既用于 BC 测试又用于 DRL 测试**，但**划分、预处理、如何构造 ego 初始状态、是否与训练有重叠**均未说明 → 泛化性结论的可信度不可评。**最小补法**：报告 NGSIM 的处理流程与切分规则。
6. **未报告：车辆动力学/执行器限制。** 只有二阶运动学式 (48a–c)，**无执行器时延、无饱和、无加速度/减速度边界**（除奖励中的 jerk 惩罚与碰撞惩罚）。影响：控制律在真实车辆上的可实现性未知；P1 的 CARLA 车辆动力学与之不可比。**最小补法**：报告加速度/减速度/转向边界与执行时延设定。
7. **未报告：DRL 训练的总步数/墙钟时间/硬件。** 只给 Episode=600。影响：**"DRL 更具成本效益"这一核心主张缺少成本侧证据**（无算力/时间/数据量），而这正是其与 BC 对比的关键卖点。**最小补法**：报告四种训练集的采样的总样本数与训练时长（GPU 型号/小时）。

**B. 报告但不可核验**

8. **报告但不可核验：Table 4（SAC）中"Scaling factor of entropy"出现两个取值（0.15 与 0.05）。** 原表 24 页逐字列出两行同名超参（第一列 `Scaling factor of entropy 0.15`，第二列 `Scaling factor of entropy 0.05`）。需要什么才能核验：作者澄清；或代码。影响：**SAC 的熵系数不可确定**，影响复现。（注：这可能是一处表格排版重复，**我按原样记录，不替作者裁决**。）
9. **报告但不可核验：`Montanino and Punzo, 2015` 的 NGSIM 处理口径。** 需要：该文献原文与处理脚本。影响：1341 条轨迹的筛选标准（车型/车道/时段）未知。

**C. 报告口径有歧义（两种解释导致结论不同）**

10. **口径歧义："no significant differences"是"无差异"还是"未检出差异"。** 作者用 95% CI 重叠支持前者；按 `AGENTS.md` §4，前者需要**等价/非劣检验**。**两种读法对 P1 的后果相反**：读作"无差异"→ 可写成"停走波对 DRL 泛化无影响"（**越界**）；读作"未检出差异"→ 只能写成"未发现显著差异，未做等价检验"（**正确**）。→ **P1 必须按后者写。**
11. **口径歧义："停走交通对 DRL 训练有害"的作用域。** 一是"**作为训练数据**有害（高方差导致训练发散）"，二是"**作为运行条件**有害"。本文证明的是前者（训练侧），而结论(iii)又说 DRL 能泛化到停走运行条件。**两者不矛盾，但极易被混读为"停走波对 DRL 全面有害"**。→ P1 引时必须写明"**训练数据方差**"而非"运行条件"。
12. **口径歧义：PE 阶 = "训练数据充分性"的阈值是理论下界还是工程充分条件。** Proposition 1 给的是**二阶线性 CF 模型**的 PE 阶下界（≥4，由 Theorem 2 的 2n 规则导出）。对**非线性深度网络**（BC 的 DNN）而言，该阈值只是**类比论证**，本文的 Theorem 3 也是"类似正则化"的类比而非等价命题（逐字 "can be described as"）。→ P1 **不得**把"PE 阶 ≥ 4"写成"深度 BC 训练集充分性的充分条件"。
13. **口径歧义：DRL 的 PE 阶来自探索噪声，则"无探索 = 无泛化"是否退化为主张。** Proposition 2/3/4 说探索机制使样本 PE 阶任意。若成立，则"训练数据 PE 阶"对 DRL 几乎不起约束（任何带足够探索的 DRL 都满足），结论(i)/(iii) 的差异主要来自**方差**而非 PE。**本文未把"PE 贡献"与"方差贡献"分离**（无 PE 匹配但方差不同的对照）→ P1 若要引"停走波通过 PE 提升 BC 泛化"，须知道**该机制未与方差机制解耦**。

**D. 该文有、但 P1 需要而本文未提供**

14. **未提供：多车闭环（编队）下的同类分析。** 全文无编队规模概念、无沿车队的误差传播、无弦稳定性度量（除 DRL 指标中的"SS norm"$\|v_t\|_2/\|v^{lead}_t\|_2$，那是**两车**的范数比）。P1 的 ODD（多车道主线编队）**不在其范围内**。
15. **未提供：横向控制。** 状态与动作全为纵向（间距、速度差、速度、前车加速度、加速度指令），**无横向/转向** → 与 P1 的"车道居中偏差、前轮转角方差"两项指标**无接口**。
16. **未提供：人工驾驶车混行。** 前车轨迹为合成或 NGSIM 回放，**无人工驾驶车与自动车的交互模型**，无换道/cut-in 扰动。P1 的"人工与自动混行"场景**不覆盖**。
17. **未提供：实车/硬件在环。** 结论全部止于仿真，作者亦未提任何实车计划。

---

## 8. 关键数字

> 硬规则：只抄原文**明确印出**的数值；**未印出即写"未报告（仅图）"**。本篇**无任何不确定度数值**（除 Figure 5/6/7 的方差阴影与 Figure 8 的 95% CI 图形）。

| 指标 | 值 | 不确定度 | 出处（表/图/节） | 备注 |
|---|---|---|---|---|
| PE 阶 / 轨迹方差（匀速） | **0 / 0** | 未报告 | Table 1 | 不能实现可辨识性 |
| PE 阶 / 轨迹方差（线性） | **1 / 27.32** | 未报告 | Table 1 | 不能实现可辨识性 |
| PE 阶 / 轨迹方差（梯形） | **4 / 34.98** | 未报告 | Table 1 | 达可辨识性下界 |
| PE 阶 / 轨迹方差（拥堵/停走） | **6 / 43.69** | 未报告 | Table 1 | 最高 PE、最大方差 |
| 方差排序（逐字） | Var[Congested] > Var[Trapezoidal] > Var[Linear] > Var[Constant] | 未报告 | §5.1 | 与 PE 阶同序 |
| 可辨识性 PE 阶阈值 | **≥ 4**（前车轨迹 PE 阶不低于 4） | N/A | Proposition 1 | 由二阶线性 CF 模型 + Theorem 2（2n）导出 |
| 停走波满足 PE 的最低条件 | **≥ 2 个振荡频率** | N/A | Lemma 1 | 单正弦 PE 阶=2（E2）；叠加两条即 ≥4（E3） |
| 采样步长 | **dt = 0.1 s** | 未报告 | §5.3.1 奖励项 $r_{jerk}$ 处 | 离散递推式 (48a–c) |
| 最大 jerk 幅值 | **Jerk_max = 60 m/s³** | 未报告 | §5.3.1 | 仅用于奖励归一化 |
| 目标自由流速度 | **v_free = 34 m/s** | 未报告 | §5.3.1 奖励项 $r_{speed}$ | — |
| 奖励的时距分布参数 | 对数正态 $\mu=0.45$，$\sigma=0.25$；车长 $\delta_0=4$ m | 未报告 | §5.3.1 奖励项 $r_{tracking}$ | $h_{ego}=(\delta p_t-\delta_0)/v_t$ |
| 奖励权重 | $a_1=1.5$，$a_2=2$，$a_3=a_4=a_5=1$ | 未报告 | §5.3.1 | 碰撞/倒车惩罚均为 **−10** |
| BC 超参 | lr **0.0001**；batch **64**；epochs **80**；线性层维度 **32**；optimizer **Adam**；50 epoch 后 lr 减半 | 未报告 | Table 2 / §5.2.1 | 两种 DNN 结构：①两层线性 ②三层线性 + tanh |
| BC 收敛水平 | 训练与验证损失均 **< 0.001 m/s²** | 未报告 | §5.2.2 | 四类数据集均达到 |
| BC 测试 MSE 排序 | 匀速 **最大** > 线性 > 梯形 > **拥堵最小** | 未报告（仅图） | Fig. 4 (a)–(f) | 两种 DNN 结构结论一致 |
| DRL 训练次数 | **每个训练数据集 20 次** | 未报告 | §5.3.2 逐字 "We conduct the DRL training 20 times for each training dataset" | **本篇主要的重复性证据** |
| DRL Episode 数 | **600**（PPO 与 SAC 同） | 未报告 | Table 3、Table 4 | — |
| PPO/SAC 学习率 | actor **0.0001**，critic **0.0002** | 未报告 | Table 3、Table 4 | — |
| PPO 其他超参 | clip **0.2**；熵系数 **0.05**；折扣 **0.99**；价值函数系数 **0.5**；初始策略方差 **0.6**；方差衰减率 **0.05**；衰减频率 **10000**；最小动作标准差 **0.01**；权重更新频率 **500**；更新 epoch **32** | 未报告 | Table 3 | actor 线性层 64 / critic 32 |
| SAC 其他超参 | batch **32**；回放容量 **320000**；每步更新 **2** 次；折扣 **0.99**；软更新系数 **0.95**；熵系数 **0.15 与 0.05（表内两处，见 §7 第 8 条）** | 未报告 | Table 4 | actor 线性层 64 / critic 32 |
| DRL 训练收敛（自由流 vs 拥堵） | 自由流收敛到**更大** episode reward 且**方差显著更小**；拥堵"**diverges and fails to reach the optimal control policy**" | 未报告（仅图） | Fig. 5 (a)(b) | PPO 与 SAC 同向 |
| 波动幅值/频率增大的影响 | episode reward **下降**、方差**增大** | 未报告（仅图） | Fig. 6 | 验证 Lemma 5、6 |
| 过度探索的影响 | 熵系数 **×10**、探索噪声方差 **×2** → 奖励降低、方差增大 | 未报告（仅图） | Fig. 7 | 对照：正常探索收敛 |
| 四数据集 DRL 的四项指标 | spacing、SS norm、jerk、TTC **"no significant differences"**（**依据：95% CI 大幅重叠**） | **95% CI（图形，无数值）** | Fig. 8 (a)–(d) | ⚠ **未做等价/非劣检验**；推断写法有误（见 §6②） |
| 测试安全性 | **no collisions or reverse movements occur** | 未报告 | §5.3.2 | 定性；无次数/分母 |
| SS norm 定义 | $\|v_t\|_2/\|v^{lead}_t\|_2$ | N/A | §5.3.2 | **两车**范数比，不是弦稳定判据 |
| 测试数据集 | NGSIM 处理后数据集，**1341 条车辆轨迹**（Montanino & Punzo 2015） | 未报告 | §5.2.1 | 仅测试；与训练分布显著不同 |
| 受控车数 / 前车数 | **1 / 1**（两车跟驰对） | N/A | 全文 | 非编队 |
| 资助 | UT-Battelle LLC 合同 **DE-AC05-00OR22725**（US DOE）；Georgia Tech 追加支持 | — | Acknowledgments | 无基金号之外的资源披露 |

**§3.7 数字口径对照表（同一指标多值/多设置时强制填写）**

| 指标 | 数值 | 数据集/设置 | 控制范式 | 是否重复运行 | 测试集 | 出处 |
|---|---|---|---|---|---|---|
| 轨迹方差 | 0 / 27.32 / 34.98 / 43.69 | 匀速 / 线性 / 梯形 / 拥堵 | — | 单次计算 | — | Table 1 |
| PE 阶 | 0 / 1 / 4 / 6 | 同上 | — | 单次计算 | — | Table 1 |
| 测试 MSE（加速度/速度/位置） | **仅排序，无数值** | 同上 | BC（DNN 结构 1 与 2） | **未报告** | NGSIM 1341 条 | Fig. 4 |
| Episode reward | **仅曲线与阴影，无数值** | 自由流 vs 拥堵 | DRL（PPO / SAC） | **20 次** | — | Fig. 5 |
| Episode reward（波动幅值/频率增大） | **仅曲线，无数值** | 拥堵（幅值/频率递增） | DRL | 未报告 | — | Fig. 6 |
| Episode reward（探索设置） | **仅曲线，无数值** | 自由流 | DRL（PPO） | 未报告 | — | Fig. 7 |
| spacing / SS norm / jerk / TTC | **仅箱线图，无数值**；95% CI 大幅重叠 | 四类数据集 | DRL（PPO） | 未报告 | NGSIM | Fig. 8 |
| 速度跟随表现 | **仅曲线，无数值** | 匀速数据集训练 | DRL（PPO） | 未报告 | 6 类速度剖面 + NGSIM | Fig. 9 |
| DDPG 收敛 | **仅曲线，无数值** | 有无 EIDM 正则化 | DRL（DDPG） | 未报告 | — | Fig. 10 |

**⚠内部不一致 / 需注意处（逐字存证）**

1. **"无显著差异"的推断写法**：Fig. 8 处逐字 "display no significant differences (i.e., large overlapping regions of 95% confidence interval)" —— 把 **CI 重叠** 等同于 **无显著差异**，且**未做等价/非劣检验**。按项目 `AGENTS.md` §4，这属于**推断越界**；P1 引用时必须降级表述。
2. **Table 4（SAC）熵系数出现两处不同取值（0.15 / 0.05）**：同一张表内同名超参两行，未说明区别。**我不替作者裁决**，按原样记录。
3. **"Fig. 9" 的图注编号与正文交叉引用**：正文第 2362 行处出现子图标签 `(c) Following a sinusoidal speed` 与 `(d) Following a NGSIM speed`，而图注（第 2364 行）为 `(c) Following a trapezoidal speed (d) Following a congested speed` 之后的续行未在图注内重复 —— 即**罗马数字以外的子图标签在提取文本中有错位**（(c)(d) 出现两次）。**需回原 PDF 核对 Figure 9 的子图归属**；本卡片在图 5 清单中按顺序列出 (a)–(f)，**未采信重复标签**。

**★ 引用时必须带上的限定语（`citation_qualifier` 单行，供 `citation-and-related-work` 直接消费）**

```
citation_qualifier: pure NUMERICAL SIMULATION (no field experiments, no real vehicles, no test track) of a two-vehicle car-following pair with EXACTLY ONE controlled ego vehicle (no platoon, no fleet-size concept) under ONE-WAY longitudinal coupling in which the lead vehicle's acceleration trajectory is EXOGENOUS and unaffected by the ego vehicle (so there is no traffic closed loop); the four lead-vehicle training datasets are SYNTHETIC (constant, linear, trapezoidal, and stop-and-go constructed as a sum of four sinusoids, v0 + sum a_i sin(omega_i (t+phi)), with v0 in {0,10,15,25} m/s, a_i in {1,2,4,8} m/s, omega_i in {0.03,0.05,0.08,0.1} rad/s), and the only real data (processed NGSIM, 1341 trajectories) is used for OUT-OF-DISTRIBUTION TESTING ONLY; DRL training is repeated 20 times per dataset and reports mean-plus-variance curves and 95% CI boxplots, but NO seed is reported, the BC part reports no repetitions, no numerical CI values are printed, and the claim of "no significant differences" across the four datasets rests solely on OVERLAPPING 95% CIs with NO equivalence or non-inferiority test; results come from the ISTTT 25 (2024) conference version while the peer-reviewed version is Transportation Research Part C 168:104578 (2024), whose numerical agreement with this version has NOT been checked.
```

---

**材料问题（本卡片层面，5 条以内）**

1. **手上是 ISTTT 25 会议版（33 页），不是 TR-C 期刊版**：文件首页逐字带 ISTTT 25 会议名/届数/日期/地点，且无 DOI、无 Elsevier 版式；期刊版为 TR-C **168:104578**（DOI 10.1016/j.trc.2024.104578，2024-11）。**两版数值是否一致未核**（未取期刊版 PDF）。
2. **绝大多数"定量影响"没有数字**：Table 1 是全文唯一给出数值的结果表；BC 的 MSE、DRL 的 reward、四项性能指标的 95% CI **全部只有图**，P1 **无法引用任何数字**。
3. **统计推断有一处明确越界**：用 95% CI 重叠推出 "no significant differences"，未做等价/非劣检验（`AGENTS.md` §4 不允许）。
4. **无可复现材料**：无代码/数据可用性声明，无仿真平台说明，**未报告种子**；DRL 的 20 次重复**具体随机化了什么未说明**。
5. **与 P1 ODD 的接口缺失**：无横向控制、无编队、无混行人工车、无换道/cut-in —— P1 的"车道居中偏差 / 前轮转角方差"与"编队闭环"两项在本篇**完全没有对应物**。
