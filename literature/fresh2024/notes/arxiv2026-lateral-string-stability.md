# 横向弦稳定性（弧长视角）｜Lateral String Stability for Vehicle Platoons: Formulation, Definition, and Analysis

- **出处**：**版本 A（精读对象）** arXiv:2605.01731v1 [cs.RO]，提交日期 2026-05-03（逐字页脚："arXiv:2605.01731v1 [cs.RO] 3 May 2026"），24 页，**`journal_ref` 为空（截至 2026-10-04）**；**版本 B（同行评议正式版，见下方 ★ 正式版核验节）** —— 逐字 `journal_ref`：`2026 American Control Conference (ACC), New Orleans, LA, USA, 2026, pp. 3444-3449`，arXiv ID **2606.29677v1**，提交日期 2026-06-29 ｜ **类型**：版本 A = 预印本；版本 B = **会议论文（ACC 2026 正式版，有页码）**
- **作者**：Sixu Li, Swaroop Darbha, Yang Zhou（n=3；Texas A&M University，Zachry 土木与环境工程系 + J. Mike Walker '66 机械工程系）
- **DOI**：**无**（arXiv API 返回 `doi` 为空；ACC 版亦未在 arXiv 记录中给出 DOI）
- **全文来源**：`literature/fulltext/fresh2024/arxiv2026-lateral-string-stability__9c8a2cbd.txt`（PAGES=24, CHARS=76,635）｜ **材料版本**：逐字——`SOURCE_PDF: arxiv2026-lateral-string-stability.pdf` / `MD5: 9c8a2cbd422af2c9b001426ea5e5dbc5` / `PAGES: 24`，页脚逐字 `Sixu Li et al.: Preprint submitted to Elsevier`（**Elsevier 投稿模板**，与最终落在 ACC 不一致，见 §7 缺失信息）；**本次仅取得版本 A 全文，未取得 ACC 版 PDF**
- **分组**：2024+ 增量
- **证据等级初判**：**C 级** — 定理与命题是数学证明（A 级成分），但**全部"验证"仅为单次仿真（6 车 / 12 车），无实车、无重复、无 CI、无 seed，且 L2 范数只有图、没有任何印出的数值**；作者自述 "The theoretical results are validated via simulation."（Abstract 逐字）
- **档位建议**：**B** — 判据/定义可直接服务 P1 的横向指标口径（D1=2），但仿真单次、无 CI、全文无数值、且唯一可达弦稳定的配置**要求 V2V**，与 P1"零额外传感器成本"路线正面冲突；即便按 ACC 正式版调整后加权达 14（A 档阀值），我仍建议**先按 B 档使用**（理由见下方"D5 口径取舍"）
- **五维打分（各维 0–2，满分 20）**：D1=2 D2=1 D3=1 D4=2 D5=1 → 加权 = **14**

  | 维度 | 分 | 依据 |
  |---|---|---|
  | D1 问题吻合 | 2 | 直接给出 P1 **纵向 + 横向**指标中"横向"一侧的**弦稳定性定义与判据**，其 §5 验证协议（按车辆序号的误差范数曲线）可被 P1 直接复用为横向指标的更强口径 |
  | D2 设计强度 | 1 | 定理级证明 + **单次仿真**；无实车、无多场景、无重复、无 CI、无 seed。按协议 §5"相关/仿真/单组"= 1（不得给 2） |
  | D3 可迁移性 | 1 | 定义/判据公式与设计步骤（Remark 4）可迁移；**无数据、无代码**，车辆参数转引自 Liu et al. 2020a，赛道不可得 |
  | D4 时效性 | 2 | 预印本 2026-05-03，ACC 2026；检索上界 2026-10-04，≤5 年 |
  | D5 完整性 | 1 | 全文在（24 页）+ 定理证明完整，但**关键验证结果只有图、无任何数值**，无代码/数据可用性声明，无置信区间 |

  **加权核算**：3×2 + 2×1 + 2×1 + 1×2 + 2×1 = 6+2+2+2+2 = **14**

  **★ 版本 B（ACC 2026）落地后对 D4/D5 的处置（必读）**
  - **D4 不变（2）**：两版均在 5 年内。
  - **D5 我仍给 1，不给 2**：理由有三。① **ACC 版是 6 页（pp. 3444–3449）**，容量上不可能容纳本长版的全部定理与证明；② 两版 **Abstract 逐字比对**显示差异明确——长版含 "Both strategies are analyzed for lateral string stability with respect to **two error measures: tracking error vector and lateral (cross-track) error**." 与 "The analysis further identifies **structural controller requirements, showing that nonzero feedback on specific measurements is essential for guaranteeing stability**."，而 **ACC 版 Abstract 中这两句均不存在**；③ 我自己没有 ACC 版全文，不能假定其含完整证明链。→ **在拿到 ACC 版 PDF 之前，D5 以我实际读到的材料（长版）为准；而这正是本卡片的重要局限。**
  - **若 ACC 版确认含完整 Definition 1 + Theorem 1 及其证明**：D5 应升至 2，加权 → **16**，则档位建议可上调为 **A**。
  - ⚠ **本卡片的 D5 与档位属于"未取 ACC 版全文"条件下的判定**；下游若据此分配 A 档预算，须先用一次取用补齐 ACC 版。

- **★ 正式版核验（含两版关系）**
  - **核验方式与日期**：① Crossref `https://api.crossref.org/works?query.bibliographic=Lateral%20String%20Stability%20for%20Vehicle%20Platoons%3A%20Formulation%2C%20Definition%2C%20and%20Analysis&rows=3`（2026-10-04）；② arXiv API `http://export.arxiv.org/api/query?id_list=2605.01731` 与 `id_list=2606.29677`（2026-10-04）；③ arXiv API `search_query=all:"Lateral String Stability"&max_results=25`（2026-10-04）。
  - **Crossref 查询返回（逐条）**：
    1. `Lateral String Stability in Autonomous & Connected Vehicle Platoons` — 2024 IEEE International Conference on Vehicular Electronics and Safety (ICVES)，DOI **10.1109/icves61986.2024.10927795**，2024-12-17，作者 Somisetty, Darbha。
    2. `String Stability Analysis of Followerstopper for Mixed-Autonomy Vehicle Platoons` — 2026 IEEE Intelligent Vehicles Symposium (IV)，DOI 10.1109/iv66570.2026.11623934。
    3. `String stability margin of cyclic vehicle platoons with variable communication range` — Automatica，DOI 10.1016/j.automatica.2022.110488。
    → **Crossref 中不存在**与本篇题名匹配的正式版记录（ACC 版的 DOI 尚未在 Crossref 建索引，或以会议论文集整体登记）。
  - **arXiv API 返回**：`2605.01731v1`：`journal_ref` **空**、`doi` **空**、primary `cs.RO`、published/updated 均为 `2026-05-03T06:02:28Z`。
  - **★ 版本 B 核验（由上游 agent 提示后，我独立用 arXiv API 复核，2026-10-04）**：
    - 题名：`Lateral String Stability for Vehicle Platoons`
    - arXiv ID：**2606.29677v1**，published/updated 均为 `2026-06-29T00:52:32Z`，primary `cs.RO`
    - `journal_ref` **逐字**：`2026 American Control Conference (ACC), New Orleans, LA, USA, 2026, pp. 3444-3449`
    - `doi`：**空**；作者：Sixu Li, Swaroop Darbha, Yang Zhou（与长版完全一致）
    - **逐字差异（我从两版 Abstract 文本直接比对）**：ACC 版题名去掉副题 "Formulation, Definition, and Analysis"；ACC 版 Abstract 删去"two error measures"与"structural controller requirements"两句，也删去末句 "The theoretical results are validated via simulation."
  - **★ 该引哪一版（我的判定）**：**引用归 ACC 2026 正式版（Li S, Darbha S, Zhou Y. Lateral String Stability for Vehicle Platoons. In: 2026 American Control Conference (ACC), New Orleans, LA, USA, 2026: 3444–3449）**，理由：项目 `AGENTS.md` §6 引用版本纪律"优先引正式发表版"，且 `00-scope.md` §2.2 规定"若存在正式版：以正式版为准，预印本降 C"。
  - **同时必须做的两件事**：① **P1 实际使用的定义式与判据（Definition 1 / Theorem 1 / Theorem 3 与四个 Proposition）取自 24 页长版** → 引用时须写明 "the extended preprint version (arXiv:2605.01731) provides the full formulation and proofs, while the ACC version is the peer-reviewed six-page version"，**不得**只引 ACC 版却照抄长版才有的内容（如两个输出定义的四格结论、Remark 4 的设计步骤）；② **两版在定义与判据上是否一致：未比对（未取得 ACC 版全文），须取 ACC 版核对**。
  - **长版是否因此降 C**：**是（按 `00-scope.md` §2.2 字面规则）**——"预印本若存在正式版则降 C"。**但本卡片的档位/D5 是对整个工作的判定**，故我按"以正式版为准"处理：正式版为 6 页会议论文，材料上限取"会议论文 + 有页码、无代码无数据、验证为单次仿真"，D2/D3/D5 均不变；若严格按 §2.2 把长版单独记为一条，则该条目应记 **C**、仅作引用。**两种口径我都在此保留，由你决定**（这正是 `meeting2/00-triage-protocol.md` §8 的做法）。

---

## 1. 标题 / 2. 摘要（≤400 字） / 3. 结论（≤350 字） / 4. 方法一句话（≤60 字）

**1. 标题（逐字，长版）**：`Lateral String Stability for Vehicle Platoons: Formulation, Definition, and Analysis`（ACC 版逐字题名：`Lateral String Stability for Vehicle Platoons`）

**2. 摘要（≤400 字，中文）**

CAV 编队的安全收益取决于弦稳定性。纵向弦稳定性已充分研究，**横向弦稳定性**——决定路径追踪误差如何传播、进而导致偏离期望路径——仍未被充分探索；随 AV 转向依赖车载感知与无地图导航，编队内传感器遮挡使横向控制更苛刻。本文提出横向弦稳定性框架，**核心是弧长（Eulerian）视角**：道路几何是空间属性，必须在**同一弧长位置**比较各车误差，否则会把控制器性能与几何复杂度混在一起。据此定义 **L₂ 横向弦稳定性**、给出**充要条件**，并分析两种策略：仅用车载感知的反馈–前馈（FF），与利用 V2V 的**学自前车（LFP）**新策略。结果：**仅靠车载感知无法保证路径追踪误差衰减（根本性安全限制），V2V 才可实现真正的误差衰减**；分析还识别出结构性控制器要求（对特定测量的非零反馈是保证稳定性的必要条件）。理论结果经仿真验证。

**3. 结论（≤350 字，中文）**

- **LTI 下，L₂ 横向弦稳定性 ⟺ 传递函数阵 H∞ 范数 < 1**（定理 1，充要）。
- **四种"策略 × 输出定义"组合中只有一种可行**（Table 2）：**仅 LFP + V2V + 输出取标量横向误差 $e^{des}_{lat,i}$ 能实现衰减**；FF 两种输出取法**都不可达**（命题 4、5）；LFP 取完整误差向量亦不可达（命题 6）。
- **$K_{LD}$ 是关键**：LFP 导数学习增益若为零则不可达（命题 8）。
- **横向对时延天然鲁棒**：时延小于 $\Delta l/v_f$ 即无影响。
- **仿真**：6 车（定量扩到 12 车）、10 m/s、赛道含 4 次换道。
- **边界**（逐字）："validated via simulation" —— 无实车、无重复、无 CI。

**4. 方法一句话（≤60 字）**：弧长重参数化横向误差动力学，用 LTI 传递函数 H∞ 范数判据判四种组合，仿真验证。

---

## 5. 图表清单（占位符）

> ⚠ **图号可能不与 ACC 版一致**（ACC 版仅 6 页，图表必然压缩/删减）。以下**全部以本次精读的 24 页长版为准**；引用任一图号前须核对 ACC 版 PDF。
> 长版**正式编号的表只有 4 个**（Table 1–4）；文中出现 14 次 "Table" 字样，其余为交叉引用。图 18 幅。**原文表格不是三线表排版，而是嵌入正文的小块（页 9 / 11 / 17 / 18）**。

| 编号 | 图注（逐字） | 页 | P1 用途 |
|---|---|---|---|
| Fig. 1 | Illustration of a sensor-occlusion scenario in a vehicle platoon | 2 | 【占位符】动机图：编队内遮挡 → 后车看不到障碍 |
| Fig. 2 | Lateral error representations | 3 | 【占位符】时间基准 vs 弧长基准对比（(a) time-based / (b) arc-length-based）→ **P1 抄口径的关键图** |
| Fig. 3 | Schematic of the vehicle platoon lateral control problem | 3 | 【占位符】问题设定 |
| Fig. 4 | Heading and position error representation | 4 | 【占位符】$e_{lat}$、$\tilde\theta$ 定义图 |
| Fig. 5 | Projection of $v_x, v_y$ onto the path tangent | 5 | 【占位符】$dl/dt = v_x\cos\tilde\theta - v_y\sin\tilde\theta$ 的几何 |
| Fig. 6 | Information flow under onboard sensing mode | 6 | 【占位符】仅车载感知的信息流 |
| Fig. 7 | Reference error computation under predecessor tracking | 7 | 【占位符】PT（跟"前车走过的路径"） |
| Fig. 8 | Information flow under V2V mode | 7 | 【占位符】V2V 信息流 |
| Fig. 9 | Reference error computation under desired-path tracking | 7 | 【占位符】DT（跟"期望路径"） |
| Fig. 10 | Illustration of spatially induced time gap | 9 | 【占位符】时延天然鲁棒性的几何解释 |
| Fig. 11 | The "virtual" closed-loop system | 15 | 【占位符】为套用 Bode 灵敏度积分而构造的虚拟回路（作者自述"does not have much physical meaning"） |
| Fig. 12 | Test track and desired path | 17 | 【占位符】赛道 + 期望路径（4 次换道，半径 7.4 m 至 2.9×10⁴ m） |
| Fig. 13 | Simulation results for the LFP strategy under V2V mode | 18 | 【占位符】(a) X–Y 轨迹 (b) 横向误差 vs 弧长 (c) 航向误差 vs 弧长 |
| Fig. 14 | Quantitative results for the LFP strategy under V2V mode | 18 | 【占位符】(a) $e^{des}_{lat}$ 的 L₂ 范数 (b) $\mathbf{e}^{des}$ 的 L₂ 范数；12 车 |
| Fig. 15 | Simulation results for the LFP strategy under V2V mode with $K_{LD}=0$ | 19 | 【占位符】消融：去掉导数学习增益 |
| Fig. 16 | Quantitative results for the LFP strategy under V2V mode with $K_{LD}=0$ | 19 | 【占位符】12 车 L₂ 范数：横向误差第 5 车起、误差向量第 4 车起放大 |
| Fig. 17 | Simulation results for the FF strategy under onboard sensing mode | 21 | 【占位符】仅车载感知的放大 |
| Fig. 18 | Quantitative results for the FF strategy under onboard sensing mode | 21 | 【占位符】12 车 L₂ 范数严格逐车递增 |
| Table 1 | Summary of control strategies（FF/LFP；是否需 V2V） | 9 | 【占位符】策略对照 |
| Table 2 | L₂ lateral string stability results under different control strategies and output definitions（FF/LFP × $\mathbf{e}^{des}_i$/$e^{des}_{lat,i}$ 四格 ✓✗） | 11 | 【占位符】**P1 必抄的结论表**（四格中仅 1 ✓） |
| Table 3 | Parameters of the Lincoln MKZ（$m$=1896 kg, $I_z$=3803 kg·m², $C_f$=400000 N/rad, $C_r$=381900 N/rad, $a$=1.2682 m, $b$=1.5818 m） | 17 | 【占位符】模型参数（转引自 Liu et al. 2020a） |
| Table 4 | Numerical values of the controller gains for the designed LFP strategy（$k_{e_{lat}}$=0.06, $k_{\tilde\theta}$=0.96, $k_{\dot e_{lat}}$=0, $k_{\dot{\tilde\theta}}$=0.08, $k_{ff}$=1.59, $K_{LP}$=−0.04, $K_{LD}$=−0.3） | 18 | 【占位符】控制器增益（反馈增益转引自 Liu et al. 2020a） |

---

## 6. 对 P1 的用处（含 **与对应层 3 笔记的关系**）

> **本卡片对应两份层 3 笔记**：`literature/notes/p33-lpstring-tcst2014.md`（**纵向** Lp 弦稳定，Ploeg 等 2014）与 `literature/notes/p43-dissipation-trc2018.md`（停走波消散，Stern 等 2018）。本文与 #33 是**同一判据家族的两个方向**（纵向 vs 横向），与 #43 无方法关系（仅共享"扰动沿车队传播"这一动机）。

### ① 与 #33（Ploeg 2014，纵向 Lp 弦稳定）的逐条关系

| 项 | #33 Ploeg 2014（纵向） | 本文（横向） | 对 P1 的后果 |
|---|---|---|---|
| 范数 | Definition 1 是 **Lp**（p 任意），实验与数值分析走 **L₂**，另有 **L∞** 定理（未被实验验证） | 只做 **L₂**；**全文没有 L∞ 横向判据** | P1 若想用"最大超调/Jerk 峰值"动机的 L∞ 口径，**横向一侧本文给不了**（须回到 #33 的 Theorem 2，而 #33 自己也没实验验证它） |
| 判据 | Theorem 1：$\|\Gamma_i(j\omega)\|_{H_\infty}\le 1$（**≤1**，strict 版含等号；且只给**充分**条件，必要性要 Remark 4 的四个前提） | Theorem 1：$\|\mathbf{H}_i(s)\|_{H_\infty} < 1$（**严格小于 1**，且是**充要**条件，前提是因果稳定 LTI + 零初值） | **阈值口径不同（≤1 vs <1）**；且 #33 的 Lp 定义含初值扰动项 β，本文**明文设零初值**（"with zero initial states"）→ 两者不可混用 |
| 是否对非线性成立 | 定义层对非线性成立；**判据层只对线性单向耦合成立** | **完全相同**：定义层（Definition 1）适用面更广，判据层（Theorem 1）明文要求 LTI | **P1 的 CfC 是非线性学习控制器 → 两份文献的判据都不能直接套用**；#33 笔记 §十.① 给出的三条路线（局部线性化 / 时域 Lp 增益 / 经验弦稳定指标）**对横向同样适用** |
| 时间 vs 空间 | 时间域 | **空间域（弧长 $l_d$）** | **这是本文相对 #33 的唯一不可替代增量**：横向误差必须在同一弧长点比较 |
| 时延 | **时延破坏纵向弦稳定性**（§V，Fig. 3(a)），并给出 $\theta_{max}(h)$ 曲线 | **横向对时延天然鲁棒**：时延 < $\Delta l/v_f$ 则无影响（§2.6） | P1 若同时报纵横向，**必须分开讨论时延敏感性**，不得写成"弦稳定性对时延敏感"一句话 |

### ② 与 #43（Stern 2018，停走波消散）的关系

无方法学交集（#43 是单车道环道真车、单个执行器、波消散；本文是多车横向路径追踪、LTI 判据、纯仿真）。**唯一共同点**是"扰动沿车队传播"的动机。**统计口径上本文比 #43 更差**：#43 至少有 3 次独立实验运行（尽管每条件 n=1），本文**只有 1 次仿真**。→ P1 引用两者时都不能当作"统计证据"。

### ③ 闭环 / 开环、实车 / 仿真、统计（本卡片须明确的四项）

- **闭环？** 横向**闭环**（控制器 $u_i=\delta_{f,i}$ 反馈作用到自行车动力学；Fig. 13/15/17 的轨迹是闭环仿真结果）。但**纵向不是闭环**：纵向速度**恒定为 $v_x=10$ m/s**，前车与后车之间没有纵向动力学耦合（各车按弧长各自的推进推进，互不影响纵向速度）。→ **P1 若做纵横向联合控制，"纵向闭环"这一块本文完全没有覆盖。**
- **实车？** **否，纯仿真（numerical simulation）**。作者逐字："we perform numerical simulation tests using parameters based on real-world data"——"based on real-world data"仅指**车辆参数辨识自 Lincoln MKZ**（转引自 Liu et al. 2020a），不是实车实验。**P1 不得把本文写成"实车验证"。**
- **统计？** **无**。单次仿真；**全文未出现 seed、重复次数、方差、CI、显著性检验**（我已 grep 复核）。"validated via simulation" 的强度是**图示级定性一致**（"providing clear visual confirmation" / "confirming"），不是假设检验。

### ④ ★ P1 报"车道居中偏差 / 前轮转角方差"时，能不能改用"横向弦稳定"这个更强的口径？需要什么条件？

**结论：可以"升级表述"，但不能"直接套用判据"；且升级后 P1 会撞上一个不利结论——必须正面处理。**

**（A）能升级的部分（定义层，不要求 LTI）**
- 若 P1 把"车道居中偏差"从**单一 RMSE 标量**改为**按车辆序号 $i$ 的逐车误差范数曲线**，并声明"要求 $\|y_i\|_{L_2}\le\gamma\|y_{i-1}\|_{L_2}$，$\gamma<1$，$\forall i$"，这就**形式上等价于本文 Definition 1**（式 (16) 逐字：$\|\mathbf{y}_i\|_{\mathcal{L}_2}\le\gamma\|\mathbf{y}_{i-1}\|_{\mathcal{L}_2},\ \forall i=2,\dots,m$，$\gamma\in[0,1)$）。
- **升级的实质收益**：RMSE 是**单车绝对量**，横向弦稳定性是**沿车队的传播性质**——一个"每车 RMSE 都很小"的编队仍可能弦不稳定。这正是 #33 笔记 §十.② 第 2 条对纵向给出的同一条论证，横向完全平行。
- **必须同时改的口径**：① **弧长（Eulerian）重参数化**——误差必须在**同一弧长位置**比较，不能在同一时刻比较（本文 §2.2；Fig. 2 是这一点的图证）；② 误差定义必须写清是相对**期望路径**（DT，$e^{des}_{lat,i}$）还是相对**前车实际走过的路径**（PT，$e^{ref}_{lat,i}$）——**这两者在编队里不相等**，本文正是靠区分它们才拆出 FF 与 LFP 两种模式；③ 若采用弧长口径，须声明**恒定纵向速度 + 小航向误差**假设（本文式 (4)(6)，$dl/dt\approx v_x$、$\ddot{\mathbf e}\approx \mathbf e''v_x^2$）。

**（B）不能套用判据的部分（判据层强依赖 LTI）**
- 判据是 $\|\mathbf{H}_i(s)\|_{H_\infty}<1$，其证明链条为"因果稳定 LTI → 诱导 L₂ 范数 = H∞ 范数"（Theorem 1 的 proof 逐字：its induced L₂ norm equals $\|\mathbf{H}_i\|_{\mathcal{H}_\infty}$）。**CfC 闭环不存在传递函数阵 $\mathbf{H}_i(s)$** → 该判据**没有定义**。
- 出路与 #33 笔记 §十.①(4) 的三条路线**逐条同构**：路线 A 局部线性化（分工作点算 $\mathbf{H}_i^{(k)}(j\omega)$ 并报裕度）、路线 B 时域直接估计 L₂ 增益比（不要求 LTI）、路线 C 只报经验曲线并明写"不声称满足 Li et al. 2026 的 Theorem 1"。

**（C）★ 升级后必然遇到的两个"不利结论"（这是本卡片最重要的判断）**
1. **唯一可达弦稳定的配置要求 V2V。** Table 2 的四格中只有 **LFP + V2V + 标量横向误差** 是 ✓；**仅靠车载感知的 FF 策略被证明不可能**（Proposition 4、5）。→ 若 P1 坚持"**零额外传感器成本**"（`AGENTS.md` §1），就必须承认：**在本文口径下，纯车载感知 + 前馈无法实现横向弦稳定性**。P1 只能二选一：(i) 承认并明确 P1 的横向指标**不声称**横向弦稳定性，只报经验曲线（路线 C）；或 (ii) 引入 V2V/车车通信使 LFP 型策略成立——但那已超出"零额外传感器成本"的主张边界，必须写进 Limitations。
2. **"完整误差向量"这一口径被否证。** 若 P1 想让"车道居中偏差 **与** 航向误差同时衰减"，Proposition 6（LFP）与 Proposition 4（FF）都给出不可能 → **P1 不得同时主张"横向误差与航向误差都沿车队衰减"**，只能对标量横向误差主张。

**（D）"前轮转角方差"这一项本文没有覆盖**
- 本文的**控制输入**是前轮转角 $\delta_f$（$u:=\delta_f$，§2.1），但**没有任何把转角本身作为弦稳定输出的分析或结果**。→ "前轮转角方差"**不能**直接改用横向弦稳定口径；若要做，需自建"从转角到横向误差的 Lp 增益"环节（本文不提供）。
- 同理，"跟车误差 RMSE / 加速度平方积分 / Jerk 峰值"属**纵向**，须走 #33（Ploeg 2014）那一套，**与本文判据分开陈述**；P1 不得用本文的横向判据去支撑任何纵向结论。

**（E）最小可执行清单（推荐路线）**
1. **指标口径**：横向一侧把"车道居中偏差"扩为**逐车 $L_2$ 范数曲线**（按弧长重参数化），并声明 $\gamma<1$ 是**经验观测**而非定理保证。
2. **引用定位**：定义引 **Li et al., ACC 2026**（正式版），并注明完整表述与证明见长版 arXiv:2605.01731；判据不适用性写入 Limitations（措辞与 #33 笔记 §十.①(4) 路线 C 一致）。
3. **必须报告的**：对比 Li et al. Table 2 的四格，**明确 P1 的配置落在哪一格**（若 P1 无 V2V → 落在被否证的 FF 格），并说明 P1 用什么额外手段（若有）规避。
4. **禁止**：把本文的 $v_x=10$ m/s、Lincoln MKZ 参数、$K_{LP}=-0.04$/$K_{LD}=-0.3$、赛道半径 7.4 m–2.9×10⁴ m 当作 P1 的设定或基准；P1 的 ODD 是**高速公路主线、多车道、混行**，本文是**单一期望路径上的同质编队**，两者不同。

---

## 7. 缺失信息（≥3 条）

**A. 未报告（缺失影响 + 最小补法）**

1. **未报告：ACC 2026 正式版的全文**（我只有长版）。影响：无法判定两版在**定义与判据**上是否一致，也无法判定 D5=1 还是 2（进而决定档位是 B 还是 A）。**最小补法**：取 ACC 版 PDF（pp. 3444–3449），逐条比对 Definition 1、Theorem 1、Theorem 3、Proposition 4/5/6/8 与 Table 2 是否齐全。
2. **未报告：任何 L₂ 范数的具体数值。** 影响：§5 的全部"定量结果"只有图（Fig. 14/16/18），**没有印出任何一个 $\|e^{des}_{lat,i}\|_{L_2}$ 数值** → P1 **无法引用任何数字**，也无法判断衰减比 $\gamma$ 的实际量级（是 0.9 还是 0.5？）。**最小补法**：向作者索取 Fig. 14/16/18 的逐车范数数据，或按式 (9)(15)(44)(56) 自行复现（公式足够，但需自建赛道）。
3. **未报告：仿真的时间/弧长区间、积分步长、离散求和的近似误差。** 逐字只说 "approximating the continuous-time integrals with discrete-time summations over the simulation horizon"——**horizon 长度、步长、误差界均未给**。影响：L₂ 范数对积分区间高度敏感（尤其末端截断），数值不可比。**最小补法**：索取仿真脚本或报告 $l_d$ 区间与步长。
4. **未报告：随机种子、重复次数、运行间离散度、任何 CI。** 影响：单次仿真的"confirming / validating"无法排除数值偶然性；本卡片台账等级因此锁在"仿真单例"。**最小补法**：要求 **≥5 次**（不同初值/曲率扰动）重复并给 $\gamma$ 的分布；P1 自身按 `AGENTS.md` §4 执行（种子 ≥5 + 95% CI）。
5. **未报告：初值分布。** Definition 1 明文设 **zero initial states**（"with zero initial states"），但仿真是否真的零初值、编队如何初始化（沿赛道等间距？按弧长对齐？）**未说明**。影响：弦稳定性的实证结果对初值极敏感；零初值是**最强的有利假设**之一。**最小补法**：报告初始 $e_{lat,i},\tilde\theta_i$ 与车辆初始弧长位置。
6. **未报告：无代码/数据可用性声明。** 全文无 Data/Code availability 段（仅有 CRediT 作者贡献声明，第 1574 行起）。影响：P1 无法直接复用其仿真环境。**最小补法**：按 Remark 4 的三步 + 式 (9)(15)(44)(56)(58) 自行实现（**这一步本文公式足够，可做**）。
7. **未报告：赛道几何的完整参数。** 只给"半径范围 7.4 m 到 2.9×10⁴ m、全场 4 次换道"，**不给赛道坐标/曲率函数**。影响：无法复现 Fig. 12，也无法把结果对到 P1 的高速直线+缓弯工况。**最小补法**：索取赛道定义文件。

**B. 报告但不可核验（转引）**

8. **转引不可核验：Lincoln MKZ 参数（Table 3）与反馈增益（Table 4 的 $k_{e_{lat}}$=0.06, $k_{\tilde\theta}$=0.96, $k_{\dot e_{lat}}$=0, $k_{\dot{\tilde\theta}}$=0.08）** 均转引自 **Liu et al. 2020a（IEEE T-IV 6:406–418）**，本文未复做辨识。需要什么才能核验：Liu et al. 2020a 原文 + 其辨识实验数据。（**本次未取该文，标 `[待核实]`。**）
9. **转引不可核验：$k_{ff}$ 的解析式** 转引自 Rajamani 2011（*Vehicle Dynamics and Control*），本文只给闭合表达式，未给推导与适用条件。
10. **⚠内部不一致（引用层）：参考文献条目与在版编年不符。** 本文参考文献第 1649 行逐字：`Swaroop, D., Hedrick, J.K., 2002. String stability of interconnected systems. IEEE transactions on automatic control 41, 349–357.` ——**卷号 41、页码 349–357 对应的是 1996 年 3 月出版的 IEEE TAC 41(3)**（我 2026-10-04 用 Crossref 查询 `String stability of interconnected systems Swaroop Hedrick` 返回：DOI **10.1109/9.486636**，*IEEE Transactions on Automatic Control*，**1996-03**，vol **41**，issue **3**，pp. **349–357**，作者 Swaroop, Hedrick）。→ **本文把 1996 写成了 2002**（正文三处引用该文，均写 "Swaroop and Hedrick 2002"）。**后果**：P1 若从本文转抄该条参考文献，会把年份写错。**处置**：P1 引用纵向弦稳定奠基文献时，**以 Crossref 的 1996 / 41(3):349–357 / DOI 10.1109/9.486636 为准**。
    - 与项目既有记录的关系（须与上游对齐）：`literature/文献需求-50篇顶刊.md` 附录 A5 记录的是"**Darbha & Hedrick 1996**，常被误引为 Swaroop & Hedrick"。**我本次核验的结果指向另一条**：Crossref 的 **1996** 记录作者是 **Swaroop & Hedrick**（无 Darbha）。→ **两说的分歧我无法用本次工具裁决**（Crossref 的作者字段与项目附录 A5 不一致），**标 `[待核实]`**，建议由 `citation-and-related-work` 单独核一次（需同时核 Swaroop 1994 博士论文与 Darbha & Hedrick 的 1996 会议/期刊条目是否存在）。

**C. 报告口径有歧义（两种解释导致结论不同）**

11. **口径歧义：Theorem 1 的阈值是严格小于 1，但物理上低频必然贴边。** 本文用 $<1$（充要），而 #33/Ploeg 2014 的纵向定理用 $\le 1$（且指出 $\lim_{\omega\to0}|\Gamma(j\omega)|=1$ 是结构性的、裕度为 0）。**两种读法对 P1 后果不同**：若按 $<1$ 严格判据，则**任何数值/估计误差都可能使结论翻转**（#33 笔记 §五.4 记录的同一问题：作者自承谱估计误差可能破坏判据）；若按 $\le1$，则"贴边即通过"但无物理意义。**本文未讨论实测中 |H| 贴近 1 时如何判定通过**（无任何裕度要求或鲁棒性分析）→ P1 若采用该判据，**必须自带裕度声明**。
12. **口径歧义："onboard sensing alone cannot guarantee attenuation"的强度。** 一种读法：**FF 策略这一类**被否证（本文命题仅针对其给出的 FF 结构）；另一种读法：**任何**纯车载感知方案都不可能。**本文支持的是前者**（否证针对式 (10) 的 PD+前馈结构），但摘要措辞容易被读成后者。→ P1 引用时**不得**写成"纯车载感知在物理上不可能实现横向弦稳定"。
13. **口径歧义：Proposition 8 的前提"$H(s)$ 无右半平面零点"是否对所有实用参数成立。** 作者逐字：该假设 "is typically satisfied and can be verified numerically for practical parameters"——**本文未对 Table 3/4 的参数验证它**。若该前提不成立，则"$K_{LD}=0 \Rightarrow$ 不可达"的结论失效。→ P1 若要引用这条设计规则，须自行数值验证该前提。

**D. 该文有、但 P1 需要而本文未提供**

14. **未提供：非线性/学习型控制器的横向弦稳定判据。** 与 #33 同一缺口：判据层要求 LTI。CfC 需要"局部线性化 + 分工作点裕度"或"时域 L₂ 增益"这套自建论证。
15. **未提供：多车道 / 换道触发扰动下的横向弦稳定分析。** 本文的"换道"**只出现在期望路径的几何里**（"The desired path consists of four lane changes"），**不是**交通流中的邻车切入/换道扰动。P1 的长尾场景（cut-in 急并入、编队单车退出、激进车流扰动）**本文一概没有**。
16. **未提供：混行（人工+自动）下的横向弦稳定。** 全体车辆同质（同参数、同控制器族），**无人工驾驶车** → 与 P1 的 ODD（人工与自动混行）不符。
17. **未提供：纵向闭环。** 纵向速度恒定，前车不影响后车纵向运动 → 纵横向联合控制（P1 的"编队连续时间控制"）不在本文范围内。

---

## 8. 关键数字

> 硬规则：只抄原文**明确印出**的数值。**§5 的全部"定量结果"只有图、没有印出任何 L₂ 范数数值**，故下表"验证类"一栏只能是**定性描述**。所有数字**无不确定度**（原文无 CI/方差/seed）。

| 指标 | 值 | 不确定度 | 出处（节/式/图/节行） | 备注（哪套设置） |
|---|---|---|---|---|
| 判据阈值（L₂ 横向弦稳定） | $\gamma\in[0,1)$；$\|\mathbf{H}_i(s)\|_{\mathcal{H}_\infty}<1$ | N/A | Definition 1 式 (16)；Theorem 1 式 (18) | 严格小于 1；**充要**（前提：因果稳定 LTI + 零初值） |
| 输出定义（两个） | ① $\mathbf{y}_i=\mathbf{e}^{des}_i=[e^{des}_{lat,i}\ \tilde\theta^{des}_i]^{\mathrm T}$，$\mathbf{C}_{out}=\mathbf{I}_2$；② $\mathbf{y}_i=e^{des}_{lat,i}$，$\mathbf{C}_{out}=[1\ 0]$ | N/A | Remark 2 | ② 的动机为"direct safety relevance" |
| 四种组合的可行性 | FF+①✗、FF+②✗、LFP+①✗、**LFP+②✓** | N/A | Table 2；Proposition 4/5/6 | **唯一 ✓ 是 LFP + V2V + 标量横向误差** |
| LFP 学习增益设计条件 | $K_{LD}<0$ 且 $-2k_{e_{lat}}<K_{LP}<0$ | N/A | Remark 4 步骤 (b)；Proposition 8 | $K_{LD}=0$ 则不可达（Bode 灵敏度积分证明） |
| 仿真编队规模 | **6 辆**（Fig. 13/15/17）；定量部分扩至 **12 辆**（Fig. 14/16/18） | 未报告 | §5 开头；§5.1/5.2/5.3 各节 | 同质编队，同一组增益 |
| 纵向速度 | $v_x=10$ m/s | 未报告 | §5 开头逐字 "at $v_x=10\ m/s$" | 恒定（纵向不闭环） |
| 期望路径几何 | 全场 **4 次换道**；绝对转弯半径 **7.4 m 至 2.9×10⁴ m** | 未报告 | §5 开头逐字 "four lane changes over the course of a full circuit, with absolute turning radii ranging from 7.4 m to 2.9×10⁴ m" | 作者称"capturing road characteristics of both highway and urban scenarios"（**含城市几何，与 P1 的纯高速 ODD 不符**） |
| 车辆模型参数（Lincoln MKZ） | $m$=1896 kg；$I_z$=3803 kg·m²；$C_f$=400000 N/rad；$C_r$=381900 N/rad；$a$=1.2682 m；$b$=1.5818 m | 未报告 | Table 3 | **转引自 Liu et al. 2020a**，本文未复辨识 |
| 控制器增益（LFP） | $k_{e_{lat}}$=0.06；$k_{\tilde\theta}$=0.96；$k_{\dot e_{lat}}$=0；$k_{\dot{\tilde\theta}}$=0.08；$k_{ff}$=1.59；$K_{LP}$=−0.04；$K_{LD}$=−0.3 | 未报告 | Table 4 | 反馈增益转引自 Liu et al. 2020a；学习增益按 Remark 4 选 |
| 充分条件系数（式 (57)(58) 验证） | $a_6=2.91\times10^{22}$；$a_4=4.42\times10^{23}$；$a_2=5.70\times10^{22}$；$a_0=6.07\times10^{20}$（**全部 > 0**） | 未报告 | §5.1 | 即 $|D(j\omega)|^2-|N(j\omega)|^2>0,\forall\omega$ 的充分条件成立 |
| $K_{LD}=0$ 时的放大起点 | 横向误差范数**自第 5 车起**增长；误差向量范数**自第 4 车起**增长 | 未报告 | §5.2（Fig. 16） | 单次仿真，**无对应数值** |
| FF（仅车载感知）时的表现 | "a pronounced amplification of errors along the platoon"；横向误差与误差向量范数**严格逐车递增** | 未报告 | §5.3（Fig. 17/18） | 定性；对应 Proposition 4/5 |
| LFP 下的航向误差 | "Fig. 13(c) reveals **no consistent attenuation pattern** in the heading error" | 未报告 | §5.1 | 即：**即使 LFP 成立，航向误差并不逐车衰减** |
| LFP 下完整误差向量的经验表现 | Proposition 6 说"不保证"，但"it is nevertheless observed to hold empirically in this specific test scenario" | 未报告 | §5.1（Fig. 14(b)） | **命题说不可能、单次仿真说成立** → ⚠内部不一致（见下） |
| 时延鲁棒性条件 | 通信/感知时延 < $\Delta l/v_f$（空间间隔诱导的时间间隙） | N/A | §2.6 | $\Delta l=l_1-l_2$，$v_f$ 为跟驰车纵向速度 |
| 参考文献篇数 | 约 40 余条（Besselink & Johansson 2017 起到 Yu et al. 2019） | — | References | — |

**§3.7 数字口径对照表（同一指标多值/多设置时强制填写）**

| 指标 | 数值 | 车辆数 | 控制策略 | 输出定义 | 是否重复运行 | 出处 |
|---|---|---|---|---|---|---|
| $\|e^{des}_{lat}\|_{L_2}$ 的沿序号趋势 | **递减**（定性） | 6（Fig. 13）/ 12（Fig. 14） | LFP + V2V | ② | **单次**（无 seed） | Fig. 13(b) / Fig. 14(a) |
| $\|\mathbf{e}^{des}\|_{L_2}$ 的沿序号趋势 | **递减**（定性，与 Proposition 6 相反） | 12 | LFP + V2V | ① | **单次** | Fig. 14(b) |
| $\|e^{des}_{lat}\|_{L_2}$ 的沿序号趋势 | 第 5 车起**增长** | 12 | LFP + V2V，**$K_{LD}=0$** | ② | **单次** | Fig. 16(a) |
| $\|\mathbf{e}^{des}\|_{L_2}$ 的沿序号趋势 | 第 4 车起**增长** | 12 | LFP + V2V，**$K_{LD}=0$** | ① | **单次** | Fig. 16(b) |
| $\|e^{des}_{lat}\|_{L_2}$ 与 $\|\mathbf{e}^{des}\|_{L_2}$ | **严格逐车递增** | 12 | **FF（仅车载感知）** | ①② | **单次** | Fig. 18(a)(b) |
| 航向误差 $\tilde\theta^{des}$ vs 弧长 | **无一致衰减模式** | 6 | LFP + V2V | — | **单次** | Fig. 13(c) |

**⚠内部不一致（两处，逐字存证）**

1. **"命题说不可能、仿真说成立"。** Table 2 / Proposition 6 判定 LFP + 输出①（完整误差向量）为 **✗（不可达）**；而 §5.1 逐字写 "even though Proposition 6 states that $\mathcal{L}_2$ lateral string stability with respect to $\mathbf{y}_i=\mathbf{e}^{des}_i$ is not guaranteed in all cases, **it is nevertheless observed to hold empirically in this specific test scenario**." → **不矛盾但极易被误读**：Proposition 6 是"不保证/存在反例"，仿真只测了一个场景。**P1 引用时必须写"命题层面不可保证，该单场景经验上成立"，不得写成"完整误差向量也可弦稳定"。**
2. **参考文献年份与卷页不符**（见 §7 第 10 条）：`Swaroop, D., Hedrick, J.K., 2002 ... IEEE transactions on automatic control 41, 349–357`——卷 41 / 页 349–357 对应 **1996**。

**★ 引用时必须带上的限定语（`citation_qualifier` 单行，供 `citation-and-related-work` 直接消费）**

```
citation_qualifier: LTI-only, arc-length (Eulerian) L2 lateral string stability of a homogeneous vehicle platoon with CONSTANT longitudinal speed vx = 10 m/s (no longitudinal closed loop) — the necessary-and-sufficient condition ||H_i(s)||_Hinf < 1 (Theorem 1) requires causal stable LTI interconnections with ZERO initial states, so it is NOT applicable to nonlinear / learning-based (CfC-style) controllers; among the four strategy x output combinations only the V2V-based learn-from-predecessor strategy with the SCALAR lateral error as output is provably L2 laterally string stable (Table 2), while onboard-sensing-only feedback-feedforward is provably NOT (Propositions 4 and 5); validation is NUMERICAL SIMULATION ONLY (6 vehicles, extended to 12 — NOT field experiments, NOT real vehicles; bicycle-model parameters are identified from a Lincoln MKZ but taken from Liu et al. 2020a), performed ONCE with no repetitions, no random seeds, no variance and no confidence intervals, and NO numerical L2-norm values are printed anywhere (all quantitative claims are figures only); the test track includes four lane changes with turning radii from 7.4 m to 2.9e4 m (mixed highway AND urban geometry), and the vehicles are homogeneous with no human-driven vehicles and no cut-in / lane-change traffic disturbances.
```

---

**材料问题（本卡片层面，5 条以内）**

1. **手上是长版而非 ACC 正式版**：`literature/fulltext/fresh2024/arxiv2026-lateral-string-stability__9c8a2cbd.txt` 实为 arXiv:2605.01731（24 页，Elsevier 模板），**不是** ACC 2026 的 6 页版；两版的图号、表号、证明完整度**均未比对**。
2. **本文档由 PDF 提取，数学符号丢失严重**：`\mathcal{L}_2` 变成全角/私用区字符（原文"L₂"处显示为乱码 `顖?`）、`\mathcal{H}_\infty` 显示为 `H∞`、矩阵与公式大量换行错位。本卡片的公式均按结构与上下文重建，**引用公式全文前须回原始 PDF 逐字核对**。
3. **无任何印出的数值结果**：§5 的"quantitative results"只有图，**P1 无法从本文引用任何数字**。
4. **本卡片未做外部复现检索**（未查 OpenAlex/DataCite 的引用与更正状态），故"该判据是否已被他人复现/反驳"**未检**——"未检"是信息缺失，**不等于**"无外部证据"。
5. **撤稿/更正未查**：本文（两版）均无 DOI，DataCite/Crossref 撤稿检查**无从执行**；ACC 版 DOI 待 Crossref 建索引后补核。
