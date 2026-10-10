# 多车道编队重构的 GRDF 决策框架（含驾驶风险势场）｜Towards Emergency Scenarios: An Integrated Decision-making Framework of Multi-lane Platoon Reorganization

- **出处**：arXiv:2506.16311v1，2025-06-19（`arXiv:2506.16311v1 [cs.MA] 19 Jun 2025`，本机 arXiv API 核验：最新版仍为 **v1**）｜ **类型**：预印本（**但已有正式版**，见下 ★ 行：IEEE Transactions on Consumer Electronics, vol. 71, no. 4, pp. 11719–11733, Nov 2025）
- **作者**：Aijing Kong, Chengkai Xu, Xian Wu, et al.（n=5；全序：Aijing Kong, Chengkai Xu, Xian Wu, Xinbo Chen, Peng Hang；同济大学；通讯作者 Xian Wu、Peng Hang）
- **DOI**：**10.1109/TCE.2025.3612821**（正式版，Crossref 逐字）。arXiv 预印本本身**无 arXiv DOI**：`api.crossref.org` 未收录，arXiv API 返回的 `arxiv:doi` 字段为 **null**，故本卡不写 `10.48550/arXiv.2506.16311`
- **全文来源**：`literature/fulltext/fresh2024/arxiv2025-platoon-risk-potential-field__d4004eeb.txt`（PAGES=15；任务书标 CHARS=66,569，**本机实测 68,530 字符 / 69,147 字节**，含 4 行提取头；MD5=`d4004eeb47318ff7e0d7a7b56dce3138`）
- **分组**：2024+ 增量
- **★ 正式版核验**（执行日 **2026-10-06**，晚于 `00-scope.md` §2.1 声明的检索上界 2026-10-04；原始返回已存档）
  1. **Crossref 题名匹配**（模板指定的一次查询）：`https://api.crossref.org/works?query.bibliographic=Towards%20Emergency%20Scenarios%3A%20An%20Integrated%20Decision-making%20Framework%20of%20Multi-lane%20Platoon%20Reorganization&rows=3` → **HTTP 200**，**第 1 条即命中**：`10.1109/tce.2025.3612821`，题名逐字 `Towards Emergency Scenarios: An Integrated Decision-Making Framework of Multi-Lane Platoon Reorganization`（与预印本仅 `Decision-making`→`Decision-Making`、`Multi-lane`→`Multi-Lane` 的大小写差异），`container-title` = `IEEE Transactions on Consumer Electronics`，`type` = `journal-article`，`issued` = `{"date-parts":[[2025,11]]}`。第 2、3 条为不相关记录（NIOSH 报告、1991 年书章）——Crossref 该端点为 **OR 语义**，命中需人工判读。
  2. **DOI 记录反查**：`https://api.crossref.org/works/10.1109/tce.2025.3612821` → **HTTP 200**，`vol 71 / issue 4 / page 11719-11733`，作者逐字 `Aijing Kong ; Chengkai Xu ; Xian Wu ; Xinbo Chen ; Peng Hang`（**与预印本同序 5 人**），`reference-count` 45，`is-referenced-by-count` 1。
  3. **T5 更正/撤稿检查**：同记录 `update-to` = **null**、`updated-by` = **null**、`relation` = `{}` → **Crossref 无更正或撤稿记录**（截至 2026-10-06）。
  4. **arXiv 回填检查**：`http://export.arxiv.org/api/query?id_list=2506.16311` → **HTTP 200**，`<id>http://arxiv.org/abs/2506.16311v1</id>`（最新版 = v1），`arxiv:comment`、`arxiv:journal_ref`、`arxiv:doi` **三字段全空** → **作者未把 IEEE TCE 正式版回填 arXiv**。
  5. **正式版可得性**：Unpaywall（`api.unpaywall.org/v2/10.1109/tce.2025.3612821`，2026-10-06，HTTP 200）→ `is_oa: false`、`oa_status: "closed"`、`has_repository_copy: false`、`oa_locations: []`，`published_date: 2025-09-22` → **正式版无任何 OA 副本，本机取不到全文**。
  6. **代码材料核查**：正文给的 `https://github.com/KongAAAAAAJ/GRDF` —— GitHub REST API（2026-10-06，HTTP 200）显示仓库**只有 1 个 `README.md`（765 字节）**，仓库 `size` = 6 KB，`language` = null，**无 LICENSE、无任何代码**。原文措辞亦仅为 `Relevant video materials can be found on the website`。
  - **原始返回存档**：`literature/fresh2024/verify_two_cards.json`、`verify_two_cards_round2.json`、`verify_two_cards_round3.json`；脚本 `literature/scripts/verify_two_cards.mjs`、`verify_two_cards_round2.mjs`、`verify_two_cards_round3.mjs`
  - **→ 按 `00-scope.md` §2.2 处置**：**存在正式版** → 「以正式版为准，**预印本降 C**」。引用一律写 IEEE TCE 正式版；本卡的全部数值出自 arXiv v1 预印本，**未与正式版逐格比对**，故只能作 C 档证据使用。
- **证据等级初判**：**C** — 纯仿真（OpenAI Gym，运动学模型 + PID 闭环）、单一实验台、无随机种子、无置信区间、无统计检验、无代码、风险场参数（`GRM`/`k1`/`k2`）全部转引且未给值；虽有 100 次重复与多基线对照，但"A 优于 B"的效应量不可复算，且我们持的是预印本。
- **档位建议**：**C（仅引用）** — 按 §2.2「存在正式版 → 预印本降 C」的硬口径；**降档的唯一原因是材料**（正式版 closed、无 OA 副本、未取得全文），不是质量。按母协议 §5 打分该工作本身具备 A 档资质（见下）。**升级条件**：取得 IEEE TCE pp. 11719–11733 全文并逐格比对式 12 与 TABLE I/II/III 后，按正式版重判（届时 D5 可升 2）。
- **五维打分（各维 0–2，满分 20）**：D1=**2** D2=**1** D3=**1** D4=**2** D5=**1** → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = 6+2+2+2+2 = **14/20**（按 §5 本应 A 档：≥14 且 D1=2 且 D5≥1 ✓；被 §2.2 压至 C，见上）
  - D1=2：取「**同 ODD 下的闭环控制评价协议可复用**」这一支 —— 三车道高速公路、人工自动混行、随机交通流下重复 100 次的闭环仿真，配编队级指标（碰撞率 / 最小 TTC / 重构成功率 / 重构时间 / 平均车间距）+ 盒图/小提琴图逐场景呈现，这套协议骨架 P1 的「种子 ≥5 + 逐场景报告 + 分工况」可直接沿用。**弱在哪**：它给的是**决策框架不是控制器**，且七项指标与 P1 的七项**无一重叠**（无跟车误差 RMSE、无端侧延迟、无 MCU 内存）。**若把 D1 第二分句读成"数字须可对标"→ D1=1、加权 11（B 档）**；本卡取"协议可复用"支，并在此显式声明该判断。
  - D2=1：有对照（SiPLC / SuPLC / RRL 三类基线）+ 多场景（横向、纵向两个高风险场景）+ 100 次重复；但**无统计检验、无 CI、无 std、无种子**，且为纯仿真 → 「对照 + 闭环 + 有统计」三条不同时成立。
  - D3=1：**协议部分可迁移，代码/数据不可迁移**（GitHub 仓库实为空壳，仅 README；数据自建仿真环境，无公开数据集）。
  - D4=2：2025 年，≤5 年。
  - D5=1：有全文与全部结果表，但**效应量缺失**（无任何不确定度）且**可复现材料缺失**（无代码、无种子、无超参之外的配置）。
  - ⚠ 本卡严格遵守 0–2 制；**D4 一律指时效性**，未改写为其他含义。

---

## 1. 标题

`Towards Emergency Scenarios: An Integrated Decision-making Framework of Multi-lane Platoon Reorganization`（预印本第 1 页逐字）｜中文直译：**面向紧急场景：多车道编队重构的集成决策框架**

> 正式版题名逐字为 `Towards Emergency Scenarios: An Integrated Decision-Making Framework of Multi-Lane Platoon Reorganization`（Crossref，仅大小写差异）。**引用须用正式版题名。**

---

## 2. 摘要（≤400 字；实测 **328 字**＝去空白字符数，脚本 `literature/scripts/count_card_sections.mjs`）

为提升编队应对紧急场景的能力，提出编队分布重构决策框架，含**编队分布层、车辆协同决策层、车辆规划控制层**。首先给出基于强化学习的编队分布模型：**建立风险势场定量评估行车风险**，并构造面向编队重构过程的奖励函数。随后提出基于**联盟博弈**的车辆协同决策模型，通过划分联盟建模车辆间协作关系并为每车生成最优决策。此外，把基于图论的新指标 **PDI（Platoon Disposition Index）** 并入博弈奖励函数，度量重构过程中的编队分布状态以加速重构。最后在两个高风险场景、随机交通流下验证：相比基线模型，所提方法可显著降低碰撞率、提升行驶效率；带 PDI 的模型能显著缩短编队重构时间、提升重构效率。**摘要内无任何具体数值、无硬件、无频率。**

---

## 3. 结论（≤350 字；实测 **348 字**）

作者总结（§VII）：框架分上层**编队级分布层**与下层**车辆级协同决策层**；上层用 RL 决策构型，以**风险势场建立显式风险指标**并设计重构奖励引导探索；下层用**联盟博弈**建模协作，提出 **PDI** 加速重构。按风险源方向设计横向与纵向两个高风险场景，在随机交通流中测试。**关键数字**：碰撞率由 0.884 与 0.965 降至 0.021（但三数出自 **TABLE II 即横向场景**，见 ⚠1）；平均车速由 24.08 与 24.47 m/s 升至 25.42 m/s；重构时间由 6.45 与 6.16 min 降至 4.56 min。

**本卡核验发现的局限（非作者自承**，原文无局限段）：① 风险场参数转引 `[30]` 且未给值；② 全文无控制/决策频率；③ 无耗时、无种子、无 CI；④ 仅仿真；⑤ 代码仓库仅 README。

---

## 4. 方法一句话（≤60 字；实测 **58 字**）

三层：分布层=集中式 PPO 出构型；决策层=联盟博弈（MIP）出每车决策；执行层=lattice+LQR/PID 闭环。

---

## 5. 图表清单（占位符，覆盖全部图表）

> 全文共 **13 张 Figure + 3 张 TABLE = 16 个**（>12，按模板列前 12 个 + 总数，剩余 4 个列于表后）。图注逐字，截断至 100 字符（截断处加 `…`）。表体在本 .txt 中**可读**（TABLE I/II/III 的数值均已进入文本层，见 §8）。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-GRDF-1} | Fig. 1 | `Fig. 1. The communication topology of vehicle platoon` | 编队通信拓扑（LLPF：Leader-Leader-Predecessor-Follower）。P1 若声明"同等可用信息"，可据此界定编队内共享的状态量 `F = {l_target,i, x_i, y_i, v_x,i, v_y,i, a_x,i, a_y,i}`。 |
| {FIG-GRDF-2} | Fig. 2 | `Fig. 2. The overall structure of GRDF framwork` | **全文总框架图**（注：原文拼写 `framwork`）。三层数据流：Around Vehicle states + PDI → 分布层（Actor/Critic）→ 构型动作 → 博弈（Payoff/Equilibrium/MIP）→ δ_f,i 与 a_i。是 P1 画"势场→决策→控制"分层图时可对照的版式。 |
| {FIG-GRDF-3} | Fig. 3 | `Fig. 3. The platoon configuration actions` | 以 3 车编队为例的构型动作（Action 1–4，Sub-leader/Follower 划分）。构型空间规模 m = C¹_{n−1}+…+C^{n−1}_{n−1}+1。 |
| {FIG-GRDF-4} | Fig. 4 | `Fig. 4. The risk field distribution` | **风险场分布图（本卡最关心的图）**。四幅子图，X Position 刻度 60–220、Y Position 刻度 −5…5；**色标刻度（文本层可读）为 181608 / 191274 / 200939 / 210604 / 220270 / 229935 / 239601 / 249266 / 258931 / 268597** —— 场的取值量级为 10⁵，但原文**未说明这些刻度对应什么量、也未给场的函数**（见 §7-2）。 |
| {FIG-GRDF-5} | Fig. 5 | `Fig. 5. Diagram of road node division` | 路段离散为节点图（HDV / CAV / 预测位置 / 检测区）。PDI 的图论载体。 |
| {FIG-GRDF-6} | Fig. 6 | `Fig. 6. PDI calculation process` | PDI = 从编队首车节点到末车节点的**最短路等价长度**（Edge = 等价距离 ED，式 27）。Step 0/1/2 三步示意。 |
| {FIG-GRDF-7} | Fig. 7 | `Fig. 7. The scenario slice diagram of SiPLC and SuPLC` | 两个基线的场景切片：SiPLC（整体换道，t=7.5 min 被 cut-in 后追尾）、SuPLC（蛇形连续换道，t=7.2 min 换道中碰撞）。**P1 报告失败分类时的呈现版式可借鉴。** |
| {FIG-GRDF-8} | Fig. 8 | `Fig. 8. The scenario slice diagram of GRDF` | 本文方法的场景切片（t=1…42.7 min，10 帧）：t=3 min 被 cut-in，t=5 min 第二车左换道避让，t=10–16 min 其余车依次换道恢复原编队。 |
| {FIG-GRDF-9} | Fig. 9 | `Fig. 9. The box plot of average speed` | Case 1 平均车速分布（Ours / SiPLC / SuPLC）。⚠ 正文用 `Ours`，TABLE II 用 `GRDF`。 |
| {FIG-GRDF-10} | Fig. 10 | `Fig. 10. The box plot of minimum TTC` | Case 1 最小 TTC 分布，纵轴单位标 `(s)`。 |
| {FIG-GRDF-11} | Fig. 11 | `Fig. 11. The box plot of average speed and minimum TTC` | **⚠ 此图组名为 `GRDF-PDI`，而正文与 Fig. 12/13 用 `GRDF-GT`**（见 ⚠3）；且下半幅标注 `Minimum TTC` 的坐标轴单位被印成 `Value (m)`（应为 s，见 ⚠6）。 |
| {FIG-GRDF-12} | Fig. 12 | `Fig. 12. The violin plot of average distance` | Case 2 平均车间距分布（GRDF / GRDF-GT / RRL），RRL 近似 7–18 m 均匀分布。 |

> **★ 总数：13 图 + 3 表 = 16 个**（>12，按模板**只列前 12 个**）。**第 13–16 个逐字补录如下，全部图表已覆盖，无遗漏**：
> - `{FIG-GRDF-13}` = **Fig. 13**：`Fig. 13. The violin plot of formation time` —— Case 2 重构时间分布；RRL 大量数据落在 t ≈ 25 min 处（即未在 15 min 内完成重构）。
> - `{TAB-GRDF-1}` = **TABLE I**：`TABLE I HYPERPARAMETERS OF DPL MODEL` —— ⚠ 表题写 **DPL**，而全文框架名为 **GRDF**（见 ⚠3）。9 项 PPO 超参，数值见 §8.2。
> - `{TAB-GRDF-2}` = **TABLE II**：`TABLE II PERFORMANCE EVALUATION OF CASE 1` —— Case 1（横向）四指标 × 三方法，数值见 §8.3。**本卡 §3/§6 引用的 0.884/0.965/0.021 出自此表。**
> - `{TAB-GRDF-3}` = **TABLE III**：`TABLE III PERFORMANCE EVALUATION OF CASE 2` —— Case 2（纵向）六指标 × 三方法，数值见 §8.4。

---

## 6. 对 P1 的用处

### 与 P1 的关系：**相邻**（同 ODD、同"势场 × 编队"结构，最像的公开工作；但势场用法与 P1 本质不同，且不提供任何可对标数字）

ODD 对齐度高：**三车道高速公路 + 编队（CAV）+ 背景人工车（HDV，IDM/MOBIL）+ 随机交通流**，正是 P1 的「高速主线、多车道、人工与自动混行」。但它是**决策层框架**（RL + 联盟博弈 + lattice + LQR/PID），**不含任何连续时间神经网络**，也不含 OTF 概念。

### (a) risk potential field 的定义式（逐字，含歧义声明）

原文式 (12) 在提取文本中的**逐字形态**（含换行，`PAGE 6`）：

```
rris = max
i∈[1,n](GRM
dk1
i
)k2vi/(GRM
dk1
min
)k2vmax
(12)
```

**⚠ 提取限制声明**：纯文本提取丢失了 PDF 的二维排版（分式上下标、上下限），上式为**唯一可核验的文本层形态**，不得据此宣称逐字复原了公式。最可能的 LaTeX 重构（**本卡的重构，非逐字**）：

```
r_ris = max_{i∈[1,n]} ( GRM / d_i^{k1} )^{k2·v_i}  /  ( GRM / d_min^{k1} )^{k2·v_max}
```

- **自变量**：`d_i`（自车与第 i 个被观测对象的**间距**）与 `v_i`（该对象**速度**）。**不是 TTC**：TTC（记作 `τ`）在本文中是**另外两处**用的量 —— 进**观测空间** `O = {x, y, v_x, v_y, a_x, a_y, j_x, j_y, τ}`（式 8，逐字 `τ means the TTC between ego vehicle and observed objects`）与进**重构激励奖励** `r_rc = kt × τ⁰_min/τ⁰ + kv × Σ v_i/v_max`（式 17，`τ⁰_min is the critical value of TTC, set as 2.5 s`）。
- **值域**：**原文未声明**。由归一化结构（分子分母同构，分母取 `d_min` 与 `v_max`）可**推**为 (0, 1]，但**这是我的推断、不是论文的报告值**；FIG-GRDF-4 的色标刻度却落在 1.8×10⁵–2.7×10⁵，与"≤1"不符 → 两处**口径不自洽**（见 ⚠2 附注）。
- **怎么标定参数**：**本文没有标定**。逐字：`The risk reward rris is characterized by the field intensity of the driving risk field, determined in Equation 12. The detailed construction of the risk field refers to work [30], the scenario risk distribution is shown in Figure 4.` 而 `GRM`、`k1`、`k2` 三个符号**全文只出现在式 (12) 本身，一次都没有给过定义或取值**（`k1`/`k2`/`GRM` 的字面检索命中全部在式 12 行内）。`[30]` 逐字为：`Jian-qiang Wang, Jian Wu, and Yang Li. "Concept, principle and modeling of driving risk field based on driver-vehicle-road interaction". In: China Journal of Highway and Transport 29.1 (2016), pp. 105–114.`
  → **结论：该势场在本卡中不可复现、不可引用其任何具体函数形式。** 本机用 Crossref `query.bibliographic` 查该题名（2026-10-06，HTTP 200）**未定位到这条 2016 年中文期刊记录**（返回的是 2024 年 SSRN 的 "Driving Risk Entropy" 等不相关条目；该端点为 OR 语义）。

### (b) 与经典人工势场（APF）、social force 的关系；**有没有处理局部极小**

- **字面事实**：全文 `artificial potential field` / `APF` / `social force` / `repulsive` / `attractive` / `minima` / `local minimum` / `gradient`（除 policy gradient 语境）**全部 0 命中**。它既没引 APF，也没引 social force，更没有讨论局部极小。
- **血统**：它属于中文「**行车风险场**（driving risk field）」一脉（`[30]`，中国公路学报 2016），**不是** APF 一脉。
- **与 APF 的关系：同族（都把环境映射为标量场），但用法完全不同。** APF 取场的**负梯度**生成虚拟引力/斥力，用于**在线运动规划**，因此会遇到局部极小；本文只取场的**强度标量**作为 **RL 奖励函数的加项**（式 9–12），**不取梯度、不生成虚拟力、不做在线规划**。→ 局部极小问题在本文的形式下**不出现，也就没有被处理**。
- **与 social force 的关系：零引用、零讨论。** 本文对人工车（HDV）的行为建模用的是 **IDM（纵向）+ MOBIL（横向）**，不是 social force。
- **→ 对 P1 的直接后果（必答题）**：**这篇不能作为"P1 已处理局部极小"的任何证据，也不能作为势场局部极小的反例。** P1 的局部极小论证必须另找出处；项目已有的可用锚点是 `meeting2/notes/tits2020-highway-motion-planning-review.md` 记录的 Claussmann et al. (T-ITS 2020) §III-B-3：势场族两条公认缺陷 = **障碍附近振荡** 与 **局部极小**，且给出反向观点 `local minima might be necessary in highway planning to keep the ego vehicle safe from inopportune lane changes`（引 [99]）。**P1 应引 Claussmann 而非本文来解决这一条。**

### (c) 三层框架各自的方法与频率

| 层（原文名） | 方法（逐字要点） | 输出 | **频率** |
|---|---|---|---|
| **Platoon Distribution Layer**（编队级/上层） | **集中式 PPO**（actor-critic；`Multi-layer Perception (MLP) as the encoder and decoder, which contains one hidden layer and two fully connected (FC) layers. The size of hidden and FC layers is 256`）；由领航车集中决策；建模为 POMDP `(S, A, P, R, γ, O, Z)` | 理想编队构型（式 7 的构型动作） | **原文未给** |
| **Vehicle Decision Layer**（车辆级/下层） | **联盟博弈（coalition game）**：采用**可转移效用（TU）**合作博弈（Def. 3，式 19）；特征函数 `v_p(S)`（式 21–22）；**解算为 MIP（混合整数优化）** + 剪枝策略剔除不可行/不安全动作 | 每车横向决策 `α, β ∈ {left lane change, right lane change, keep the lane}` | **原文未给** |
| **Vehicle Execution Model**（执行层） | **lattice 法**运动规划（多项式生成轨迹簇 + 动力学稳定性检查 + 综合代价函数选优，考虑效率/安全/舒适）；跟踪与转向用 **LQR + PID** | `δ_f,i`（前轮转角）与 `a_i`（加速度） | **原文未给** |

- **★ 频率是本卡的硬缺口**：全文 `Hz` **0 命中**，没有任何控制周期、决策周期或规划周期。仅有的时标是 §VI 场景切片里以 **min** 计的时刻（t = 1.2 / 7.5 / 16.2 / 42.7 min 等）。
  → **P1 的「端到端延迟」指标无法与本文对齐；本文也不能用来论证任何实时性。**

### (d) 受控车数 / 编队规模 / 场景 / 仿真或实车 / 闭环 / CI / 种子

| 项 | 事实（逐字/表格） |
|---|---|
| **受控车数** | **3 辆**。逐字：`Due to communication distance and latency constraints, the number of vehicles in a platoon is typically limited to 2 to 5. In our case, the number of platoon vehicles is 3.` |
| **编队规模** | 上界 2–5 辆（通信距离与时延约束，原文）；**构型动作空间** m = C¹_{n−1}+…+C^{n−1}_{n−1}+1（式 7） |
| **场景** | **三车道高速公路**。**Case 1 = 横向高风险**（含**匝道汇入区**，右车道人工车激进左换道 cut-in 插入编队）；**Case 2 = 纵向高风险**（编队前方车辆急减速）。 |
| **是否高速主线 / 是否含人工车** | **是**高速；**是**混行。编队 = CAV（`equipped with advanced autonomous driving capabilities and V2X or DSRC`）；背景车流 = HDV，`generated randomly, with different driving styles to simulate the uncertainty of the environment`，纵向 IDM、横向 MOBIL。 |
| **仿真 or 实车** | **纯仿真**。`an OpenAI Gym environment`；`The vehicles in the simulator are built on the basis of kinematic models`；动作经 `closed-loop PID controller` 转为低层转向/加速度。**无实车、无硬件在环**。 |
| **闭环** | **是**（闭环仿真）；**不是实车**。F-2 措辞上限同 `auto-driving/AGENTS.md` §5。 |
| **重复次数** | Case 1 与 Case 2 **各 100 次**随机交通流。逐字：`To eliminate uncertainties, the simulation experiments were repeated 100 times under random traffic flow conditions. The results were then subjected to statistical analysis, and the key performance metrics are summarized in Table III.` |
| **CI / 显著性** | **无**。全文无置信区间、无标准差、无 p 值；`statistical analysis` 的实际呈现只有 Fig. 9–13 的盒图/小提琴图。 |
| **随机种子** | **无**。`seed` 0 命中，只写 `random traffic flow`。 |
| **代码** | **无**（见 ★ 行第 6 条：仓库只有 765 字节 README、无 LICENSE）。 |
| **超参完整性** | 仅 TABLE I 的 9 项 PPO 超参；**奖励权重 `ws/we/wd/wr`、`w_col/w_ris`、`k_t/k_v`，以及 `GRM/k1/k2` 全部未给数值。** |

### (e) ★ P1 能从它那里借什么，以及 OTF 势场与 risk potential field 的**本质差别**（本卡最重要产出）

**能借的四件（具体到方法/协议/术语）**

1. **2024+ 的"势场量化风险"在用证据（补时效）**。它摘要逐字写 `a risk potential field is established to quantitatively assess driving risks`，且用在**多车道高速编队**场景 —— 这正好回应 `00-scope.md` §一提出的"2024 年后这条线上发生了什么"。P1 的 Introduction 可据此写：势场作为风险量化器在 2025 年仍是活跃路线，但**我们查到的工作都把势场当作 RL 奖励项**（新证据）。
2. **"势场 → 奖励塑形"可作 P1 的对照臂设定**。P1 是把 OTF 势场作为 **ODE 边界条件/结构条件**（structure-informed）；本文是把风险势场作为 **RL 奖励加项**（`A risk potential field model is established in the reward function to explicitly assess the risk of exploration actions`）。**P1 的 A1（OTF 开/关）消融在本文没有对应物**：全文没有任何"势场开/关"或"势场项权重"的消融，也没有风险场与碰撞率的归因分析 → **与 PINC（Neurocomputing 2024）一样，开关消融仍是 P1 的净增量**（与 `AGENTS.md` §1 的术语口径一致）。
3. **同 ODD 的闭环评价协议骨架（可直接沿用）**：① 100 次随机交通流重复；② **逐场景分别报告**（Case 1 横向 / Case 2 纵向各一张表），而不是只报总平均；③ 指标分层为"安全（碰撞率、最小 TTC）/ 效率（平均车速）/ 任务完成（重构成功率、重构时间）"；④ 用盒图 + 小提琴图呈现分布而非只给均值。P1 的「种子 ≥5 + 逐场景报告 + 分工况」可直接采用这一骨架并补上本文缺的 CI 与种子。
4. **一个可引的"缺口句"材料（P1 的定位弹药）**：本文把风险场的构造**整体转引 `[30]` 且不给 `GRM/k1/k2` 的值**、也不给频率与算力开销 → P1 可以正当地主张：**"现有势场类工作把势场当黑箱（参数不报告、量纲不说明、无开关消融）"**，而 P1 的 OTF 势场有**可解释的物理量（超车频次）**与**零额外传感器成本**。这一条比"性能提升 X%"更稳（不触碰 `AGENTS.md` §1 的 P1 红线）。
   - 附：**PDI** 的动机（"用一个可解释标量替代纯误差指标来刻画编队分布状态"）与 OTF 的动机同构，可作为 P1 论证"为什么需要一个可解释标量"的**同类先例**引用（不是 OTF 的先例）。

**本质差别（逐条对照）**

| 维度 | 本文 **risk potential field** | P1 的 **OTF 势场** |
|---|---|---|
| **自变量** | **运动学量**：间距 `d_i` 与速度 `v_i`（`GRM`/`d_min`/`v_max`/`k1`/`k2` 为常数） | **行为/社会量**：超车频次（交通流社会压力）；出处为黄梦圆 2023 学位论文 |
| **值域** | 原文未声明；结构上归一化（推断 ≤1），但图 4 色标为 10⁵ 量级 → 口径不自洽 | P1 自定 |
| **参数标定** | **未标定**：构造转引 `[30]`（Wang et al. 2016，中文期刊），`GRM/k1/k2` 全文无值 | P1 有学位论文的 OTF 定义与动态时间窗函数 |
| **注入位置** | **RL 奖励函数的加项**（式 9/10/12）→ 只影响**训练期**的探索偏好 | **控制器 ODE 的边界条件/结构条件** → 影响**推理时**的状态演化 |
| **是否产生力/梯度** | **否**。只作为标量奖励，不取梯度、不生成虚拟力 | 否；作为 inductive bias 进入动力学 |
| **局部极小** | **全文 0 次提及 → 未处理（形式下不出现）** | **P1 必答题**：须显式处理 |
| **时标/演化方程** | 场本身**无演化方程**；时间只通过 TTC（`τ`，进观测式 8 与激励奖励式 17）间接进入 | P1 有 |
| **"频次"语义** | **无"超车频次"概念**。`r_rf` 是**编队重构频次**（式 16：`N_trigger/N_step`），**与 OTF 不是一回事** | OTF = 超车频次 |
| **场景角色** | 势场服务于**编队构型重构**（split/merge） | OTF 服务于**跟车/编队控制的 ODE 结构条件** |
| **可解释性主张** | 未主张；`GRM/k1/k2` 不透明 | P1 主张可解释 + 零额外传感器成本 |

> **★ 一句话结论**：它们共享"用一个标量场把风险/压力写进学习系统"的**结构直觉**，但在**自变量（运动学 vs 社会行为）、注入位置（奖励 vs 动力学边界）、可复现性（未标定 vs 有定义）、以及是否面对局部极小**四点上**本质不同**。P1 **不应**把本文写成"OTF 势场的先行工作"，也不应写"势场×编队的路线已被本文占据"。

**引用时必须带的限定语（一句）**

> **Kong 等（IEEE TCE 2025，正式版；本卡数值出自 arXiv:2506.16311v1 预印本）提出的多车道编队重构框架中，风险势场仅作为强化学习奖励函数的加项使用，其构造整体转引 Wang 等 2016 的中文期刊工作，`GRM`、`k1`、`k2` 等参数在正文中未给出取值或标定方法，全文亦未报告任何控制/决策频率、计算耗时、随机种子或置信区间；该工作在 OpenAI Gym 的三车道高速混行仿真（编队 3 辆 CAV + IDM/MOBIL 控制的 HDV）中经 100 次随机交通流重复验证，无实车实验，代码仓库仅含 README。**

---

## 7. 缺失信息（≥3 条，写成可执行动作）

1. **【最高优先】取得 IEEE TCE 正式版全文**（`10.1109/TCE.2025.3612821`，pp. 11719–11733）。→ 2026-10-06 实测 Unpaywall：`is_oa:false`、`oa_status:"closed"`、`has_repository_copy:false`、`oa_locations:[]`，**无 OA 副本**。→ **后果**：本卡全部数值的正式版地位未定，档位被 §2.2 压在 C；若正式版改了式 12 或 TABLE II/III，本卡需同步修订。**动作**：走机构订阅（项目 `01-2024增量分诊.md` §8 记录本项目可用 Springer 机构通道）或向作者索取。
2. **索取风险场的参数标定：`GRM`、`k1`、`k2` 的取值、量纲、取值范围与标定数据**，并索取 `[30]`（Wang, Wu & Li, *China Journal of Highway and Transport* 29(1):105–114, 2016）原文。→ 2026-10-06 用 Crossref `query.bibliographic` 查该题名（HTTP 200）**未定位到该 2016 条目**（该通道为 OR 语义，返回 2024 年 SSRN 等不相关记录）。→ **后果**：**该势场不可复现**；P1 不得引用其任何具体函数形式作为对照或基线。**动作**：走 CNKI/万方或直接向作者索取。
3. **索取全部频率**：分布层决策周期、联盟博弈求解周期、lattice 规划周期、LQR/PID 控制周期，以及各层的单次求解耗时。→ 全文 `Hz` 0 命中。→ **后果**：P1 的「端到端延迟」无法与本文对齐；本文也不能作为任何实时性论据。
4. **索取 100 次重复的随机种子列表与逐次原始指标**。→ **后果**：Case 1 的碰撞率 0.884/0.965 → 0.021（"reduction of 97.6% and 97.8%"）与 Case 2 的 0.21 → 0.01/0 **无任何不确定度**，不可复算、不可做等价/非劣检验。
5. **澄清 TABLE II 的 `Collision Rate` 定义**（是 100 次试验中发生碰撞的比例？每次试验的碰撞次数？每公里的碰撞次数？）。→ **后果**：0.884 与 0.965 作为"碰撞率"在语义上异常高（若为比例即 88.4%/96.5% 的试验发生碰撞）；无定义则 P1 不能把它当作安全基线的量级锚点。
6. **索取 PDI 的 MIP 规模与求解耗时**（0-1 变量数 `n_u`、约束数、分支定界求解时间）。→ 式 28–29 给了目标与约束但**未给规模**，正文只写 `The PDI can be computed using common MIP solving methods, such as branch and bound, etc.`。→ **后果**：本文以 PDI 加速重构为卖点，却未报告任何计算开销，无法判断其在车载算力下的可行性；P1 若想借 PDI 思路必须自测。

---

## 8. 关键数字（只抄本 .txt 明确印出的表格/正文，不得目测估读）

> 纪律：以下全部逐字抄自 arXiv:2506.16311v1 的**文本层**（TABLE I/II/III 的表体在本 .txt 中可读）。凡原文未印出者标"未报告"，**不作任何估算或目测读数**（唯一例外是 FIG-GRDF-4 的色标刻度，为文本层可逐字读取的数字，已注明其含义未说明）。

### 8.1 正文/摘要印出的数字

| 指标 | 值 | 不确定度 | 出处 |
|---|---|---|---|
| 碰撞率降幅（引用其原文） | `a reduction of 97.6% and 97.8%` | **未报告** | §VI-B-1 正文（对应 TABLE II） |
| 最小 TTC 提升 | `2.25 times and 2.13 times higher than the baseline models` | **未报告** | §VI-B-1 正文 |
| 平均车速提升 | `an improvement of 3.9% and 5.6%` | **未报告** | §VI-B-1 正文 |
| 编队车辆数 | 3（编队规模上界 2–5） | — | §VI-A |
| 目标跟车距离 `d_target` | 10 m | — | 式 14 下方 |
| 车长 | 5 m | — | §VI-B-1 |
| 观测空间 | `O = {x, y, vx, vy, ax, ay, jx, jy, τ}`（9 维） | — | 式 8 |
| 编队内共享信息 | `F = {l_target,i, xi, yi, vx,i, vy,i, ax,i, ay,i}`（8 项） | — | 式 2 |
| MLP 结构 | 1 隐藏层 + 2 全连接层，hidden/FC 尺寸 **256** | — | §VI-A |
| 联盟形成阈值 | `e_xlim = 30 m`；`e_ylim = 1.5 m`（原文第二个符号写作 `ylim`） | — | 式 20 下方 |
| PDI 节点间距 | `d_n^min = 10 m`，`d_n^max = 20 m` | — | §V-C |
| PDI 等价距离车道项权重 | `k_l = 10` | — | 式 27 下方 |
| TTC 临界值 | `τ⁰_min = 2.5 s` | — | 式 17 下方 |
| 仿真重复次数 | 100（Case 1 与 Case 2 各 100 次） | **无 CI / 无 std / 无种子** | §VI-B-1、§VI-B-2 |
| 重构成功判据的时间上限 | 15 min（`successfully restores its original formation and completes the reorganization process within 15 min`） | — | §VI-B-2 i) |

### 8.2 TABLE I（逐字：`HYPERPARAMETERS OF DPL MODEL`）

| Symbol | Definition | Value（原文如此） |
|---|---|---|
| `Nt` | Total Training Steps | `106`（**原文如此；疑为 10⁶，上标在提取中丢失**） |
| `λ` | Learning Rate | `3−4`（**原文如此；疑为 3×10⁻⁴**） |
| `γ` | Discount Factor | 0.85 |
| `B` | Batch Size | 64 |
| `ϵ` | Clip Parameter | 0.2 |
| `Su` | Number of Forward Steps | 128 |
| `τ` | Target Update Rate | **0.0** ⚠（符号与式 8/17 的 TTC `τ` **冲突**） |
| `cv` | Value Loss Coefficient | 0.5 |
| `ce` | Entropy Term Coefficient | 0.0 |

### 8.3 TABLE II（逐字：`PERFORMANCE EVALUATION OF CASE 1`）

| Index | SiPLC | SuPLC | GRDF |
|---|---|---|---|
| Collision Rate | 0.884 | 0.965 | **0.021** |
| Average Speed (m/s) | 24.47 | 24.08 | **25.42** |
| Minimum TTC (s) | 3.21 | 3.39 | **7.23** |
| Average Distance (m) | 7.39 | 9.57 | 9.09 |

不确定度：**全表无**（无 std / CI / n）。

### 8.4 TABLE III（逐字：`PERFORMANCE EVALUATION OF CASE 2`）

| Index | RRL | GRDF | GRDF-GT |
|---|---|---|---|
| Collision Rate | 0.21 | 0.01 | **0** |
| Average Speed (m/s) | 24.27 | **26.08** | 24.91 |
| Minimum TTC (s) | 6.50 | 4.13 | 4.08 |
| Average Distance (m) | 12.58 | 10.19 | **9.74** |
| Formation Success Rate | 0.80 | 0.88 | **0.94** |
| Formation Time (min) | 6.45 | 6.16 | **4.56** |

不确定度：**全表无**。
⚠ 正文称 `the Average Distance decreased from 12.58 m and 10.09 m to 9.74 m`，但表内 GRDF 列为 **10.19**（见 ⚠2）。

### 8.5 FIG-GRDF-4 的色标刻度（文本层可逐字读取；**含义原文未说明**）

`181608 / 191274 / 200939 / 210604 / 220270 / 229935 / 239601 / 249266 / 258931 / 268597`（10 个刻度，量级 10⁵）。四幅子图坐标轴：`X Position` 刻度 60/80/…/220，`Y Position` 刻度 −5…5。
→ **本卡不作解释**：它可能是风险场强度、也可能含 `GRM` 的尺度因子；**在取得式 12 的参数前，这组数字不得作为风险场取值的证据写入任何稿件。**

---

## ⚠内部不一致（本卡核验发现，逐条给出可复算证据）

1. **横向/纵向场景张冠李戴（结论段）**：§VII 写 `reduces the collision rate in longitudinal risk scenarios from 0.884 and 0.965 to 0.021`，但 **0.884 / 0.965 / 0.021 是 TABLE II 即 Case 1（横向风险）** 的数字；Case 2（纵向）的碰撞率是 0.21 → 0.01 / 0（TABLE III）。→ 结论段把横向结果写成了纵向。
2. **Average Distance 中间项不符**：正文 `decreased from 12.58 m and 10.09 m to 9.74 m` vs TABLE III 的 `12.58 / 10.19 / 9.74` → 中间项差 0.10 m。
3. **框架命名四处不统一**：题名/摘要/正文 = **GRDF**；**TABLE I 表题 = `HYPERPARAMETERS OF DPL MODEL`**；Case 2 正文与 Fig. 12/13 = **GRDF-GT**；Fig. 11 的组名却是 **GRDF-PDI**（同一方法三个名字 + 一个未解释的缩写）。
4. **式 10 与式 11 的符号方向矛盾**：式 10 写 `Rs = w_col × r_col + w_ris × r_ris`，式 11 给 `r_col = (0, if collision happened; 1, else)` —— 碰撞时给 **0**、不碰撞给 **1**，作为正文所称的 collision **penalty** 其符号方向与命名相反（可读作"安全奖励"，但文中称为惩罚）。
5. **同一量的两个符号**：式 15 写 `Rr = w_rf × r_rf + w_re × r_re + w_ri × r_ri`，而紧接着的正文与式 17 把该量称作 `platoon reorganization incentive r_rc`。→ `r_ri` / `r_rc` 混用。
6. **Fig. 11 的坐标轴单位错误**：下半幅面板标注为 `Minimum TTC`，其坐标轴单位却印成 `Value (m)`（TABLE II/III 与 Fig. 10 均为 `(s)`）→ TTC 被标成米。
7. **符号冲突**：`τ` 同时用作 TTC（式 8、式 17）与 TABLE I 的 `Target Update Rate`；且 PPO 通常无 target network，`Target Update Rate = 0.0` 与算法描述不符。
