# P2 新颖性核验：以交通流社会压力场（OTF 场）为结构条件模态的驾驶世界模型

> 核验对象：P2 定位句「**首个以交通流社会压力场（OTF 场）为结构条件模态的驾驶世界模型**」（对标 DriveDreamer, ECCV 2024，其结构条件模态为 HDMap / 3D Box）
> 核验性质：**零算力案头核验**，全部判定基于①项目内文件 ②联网检索取得的摘要/方法原文
> 执行日期：**2026-10-13** ｜ 执行者：文献分析（本会话） ｜ 落点：`literature/p2/P2-novelty-check.md`
> 上游文件：[`文献需求-50篇顶刊.md`](文献需求-50篇顶刊.md)、[`search-log.md`](search-log.md)
> 证据等级声明：本报告是**检索证据报告**（等级 C–B），**不是**"不存在性证明"。所有"未发现"均须按 §3 的检索边界阅读。

---

## §0 结论

### 0.1 「首个」能否站住

**分两句回答，不可合并：**

| 命题 | 判定 | 依据 |
|---|---|---|
| P2 原句：**首个以"交通流社会压力场（OTF 场）"为结构条件模态的驾驶世界模型** | **可以站住，但必须改写措辞**（当前措辞不够精确，会被审稿人从"力场是不是条件"这一层打穿） | §2：检索未发现**任何**以力场/势场/社会场作为**显式结构条件模态**的驾驶（或交通）世界模型 |
| 更宽命题：**首个以"任何交互场/社会力/势场"为条件的世界模型** | **站不住** | §2：已定位 1 篇把**社会力（Social Force）显式用作去噪引导**的生成模型（SPDiff, AAAI 2024）；1 篇把**力作为控制信号**的视频生成模型（StreamForce, 2026） |

**核心理由（一句话）**：现有工作里"场/力"要么是**网络内部的中间量**（SPDiff 把社会力做成去噪器内部的等变嵌入，输出的就是力），要么是**控制信号/引导项**（StreamForce 的力控制、势场法的规划代价），**没有一篇把场当作世界模型的"输入型结构条件"（与 HDMap / 3D Box 同级的那种 condition）**。P2 的差异在**"条件模态的位置"**，不在"用了场"这件事本身。

### 0.2 建议措辞（按推荐度排序）

| # | 建议措辞 | 适用条件 | 风险 |
|---|---|---|---|
| **①（推荐）** | "首个以**交通流社会压力场（OTF）作为显式结构条件模态**的驾驶世界模型——既有驾驶世界模型的结构条件为 HDMap / 3D Box 等**几何布局**条件，交互信息则一律以**隐空间或注意力权重**隐式编码" | 立即可用。把差异锚在"**显式 / 可解释**"与"**几何 vs 社会**"两条轴上 | 低。SPDiff 仍构成"社会力在生成模型里"的先例，但它在场的位置不同，措辞已把它排除 |
| **②** | "首个以**交通流社会压力场这一阶可解释标量**为结构条件模态的驾驶世界模型" | 若审稿人指出"力控制/力引导已有先例" | 低。与项目既有口径（"OTF 作为交通社会压力的一阶可解释标量"）一致 |
| **③（保守）** | "据我们在 [OpenAlex, arXiv, Semantic Scholar, 2026-10-13] 的检索，**未发现**以交通流社会压力场为结构条件模态的驾驶世界模型；本文首次将 OTF 场引入驾驶世界模型的条件模态空间" | 若目标 venue 对"first"敏感 | 最低，但卖点弱 |

**不建议**保留原句的裸"首个"——因为它没有说明"**作为结构条件模态**"这一限定究竟是"显式输入"还是"网络内部表示"，这正是 §2 里 SPDiff 的攻击面。

### 0.3 一句话给出对 P2 写作的直接命令

> P2 的 Introduction / Related Work **必须**显式处理 SPDiff（AAAI 2024）与 StreamForce（2026），并在同一段里把"**力作为网络内部中间量 / 控制信号**"与"**场作为结构条件模态**"的差别讲清楚。**不写这段 = 把最容易被一击致命的地方留白。**

---

## §1 三节文献的条件模态判定表

**范围**：`文献需求-50篇顶刊.md` 的三节，共 **18 条**（8 + 3 + 7），与任务预估一致。

**判定依据来源说明**：
- `OA` = OpenAlex `works/doi:<DOI>` 的 `abstract_inverted_index`（本次取用 2026-10-13）
- `S2` = Semantic Scholar Graph API `paper/DOI:<DOI>` 的 `abstract` 字段
- `URL` = 本次实际 `web_fetch` 到的落地页/全文

### 1.1 「驾驶世界模型（预测/规划）」（8 条）

| # | 论文（题名 / 期刊 / 年 / DOI） | 条件模态 | 判定依据来源 | 确信度 |
|---|---|---|---|---|
| 1 | Research on World Models for Connected Automated Driving: Advances, Challenges, and Outlook ／ Applied Sciences ／ 2025 ／ [10.3390/app15168986](https://doi.org/10.3390/app15168986) | **无单一模态（综述）**：覆盖协同感知/预测/决策/控制/场景生成六域的多源异构融合；**未提力场/势场** | OA | 高（摘要） |
| 2 | Learning Robust Control Policies for End-to-End Autonomous Driving From Data-Driven Simulation ／ IEEE RA-L ／ 2020 ／ [10.1109/lra.2020.2966414](https://doi.org/10.1109/lra.2020.2966414) | **图像 / 视频 + 语义**（用真人采集轨迹渲染新局部轨迹，条件为道路外观与语义） | OA | 高（摘要） |
| 3 | Probing Multimodal LLMs as World Models for Driving ／ IEEE RA-L ／ 2025 ／ [10.1109/lra.2025.3608656](https://doi.org/10.1109/lra.2025.3608656) | **图像 / 视频（车载相机视角）**；评测四个维度（自车动态、交互、轨迹规划、开放集推理） | OA | 高（摘要） |
| 4 | Addressing corner cases in autonomous driving: A world model-based approach with mixture of experts and LLMs ／ TR-C ／ 2026 ／ [10.1016/j.trc.2025.105456](https://doi.org/10.1016/j.trc.2025.105456) | **HDMap + BEV + agent 历史状态 + LLM 语言先验**；MoE 路由器在潜空间分配专家。**无任何场/力条件** | S2（该条 `abstract=null`）+ **arXiv 全文 <https://ar5iv.labs.arxiv.org/html/2510.21867> §3.1–3.5**（输入显式列为 history+HD map `M`+BEV `I`） | 高（读了方法节） |
| 5 | World Models for Autonomous Driving: An Initial Survey ／ IEEE T-IV ／ 2024 ／ [10.1109/tiv.2024.3398357](https://doi.org/10.1109/tiv.2024.3398357) | **无单一模态（综述）**；**未提力场/势场** | OA | 中（仅摘要；综述内部可能有） |
| 6 | A survey on occupancy perception for autonomous driving: The information fusion perspective ／ Information Fusion ／ 2025 ／ [10.1016/j.inffus.2024.102671](https://doi.org/10.1016/j.inffus.2024.102671) | **占用（occupancy）/ 多源传感器融合**；3D 占用感知综述 | S2（OpenAlex 与 Crossref 均无摘要；SciPy 落地页 403） | 高（摘要） |
| 7 | Dream to Drive With Predictive Individual World Model ／ IEEE T-IV ／ 2024 ／ [10.1109/tiv.2024.3408830](https://doi.org/10.1109/tiv.2024.3408830) | **个体级意图感知潜状态 + 交互关系**（`intention-aware latent states`，经轨迹预测任务学得）。**"交互"在潜空间，不是显式场** | OA | 中高（摘要措辞明确） |
| 8 | Social Interactions for Autonomous Driving: A Review and Perspectives ／ FnT Robotics ／ 2022 ／ [10.1561/2300000078](https://doi.org/10.1561/2300000078) | **无单一模态（综述）**；但**明确覆盖 social force theory**（与优化/深度学习/图模型并列） | OA | 高（摘要） |

### 1.2 「条件模态与可控 rollout」（3 条）

| # | 论文（题名 / 期刊 / 年 / DOI） | 条件模态 | 判定依据来源 | 确信度 |
|---|---|---|---|---|
| 15 | Primitives and world model for road transportation foundation models ／ CommTR ／ 2026 ／ [10.26599/commtr.2026.9640042](https://doi.org/10.26599/commtr.2026.9640042) | **轨迹原语 + 交通流时空序列（历史）+ 控制/管理动作时间序列**（信号配时、路径诱导、车道关闭方案）。**无场/力** | OA | 高（摘要） |
| 16 | Introduction to latent variable energy-based models ／ J. Stat. Mech. ／ 2024 ／ [10.1088/1742-5468/ad292b](https://doi.org/10.1088/1742-5468/ad292b) | **潜变量 + 能量函数（H-JEPA）**；LeCun 架构的教程性综述，**非驾驶、非交通**。注意：是 *energy-based model*（能量模型），**不是势场条件** | OA | 高（摘要） |
| 17 | World model-driven process industry operations: An offline RL solution based on conditional diffusion ／ Computers in Industry ／ 2026 ／ [10.1016/j.compind.2026.104442](https://doi.org/10.1016/j.compind.2026.104442) | **操作参数 + 历史状态转移**（conditional trajectory generation）；**流程工业（烟草制丝线），非交通** | OA | 高（摘要） |

### 1.3 「多智能体交通流仿真与生成」（7 条）

| # | 论文（题名 / 期刊 / 年 / DOI） | 条件模态 | 判定依据来源 | 确信度 |
|---|---|---|---|---|
| 34 | Development of a Game Engine-Based Multi-Agent Model to Characterize Human-Autonomous Vehicle Interactions ／ IJTST ／ 2026 ／ [10.1016/j.ijtst.2025.07.011](https://doi.org/10.1016/j.ijtst.2025.07.011) | **脚本化行为规则 + 3D 环境资产**（Unity3D + SketchUp，C# 脚本）；**人因被试实验**，非生成式条件模态 | OA | 高（摘要） |
| 35 | What Do Traffic Simulations Have to Provide for Virtual Road Safety Assessment? ／ IEEE T-ITS ／ 2022 ／ [10.1109/tits.2022.3220961](https://doi.org/10.1109/tits.2022.3220961) | **人因错误分类学 + 认知驾驶员行为模型**（Rasmussen 错误分类学扩展到交通；提出 DReaM） | OA | 高（摘要） |
| 36 | Investigating of machine learning's capability in enhancing traffic simulation models ／ TR Procedia ／ 2025 ／ [10.1016/j.trpro.2024.12.122](https://doi.org/10.1016/j.trpro.2024.12.122) | **仿真变量（方式选择、行程距离/时长、等待时间）**；用 ML 复现 agent-based 仿真结果 | OA | 高（摘要） |
| 37 | Multi-Agent Reinforcement Learning for Traffic Flow Management of Autonomous Vehicles ／ Sensors ／ 2023 ／ [10.3390/s23052373](https://doi.org/10.3390/s23052373) | **无显式条件（MARL 控制）**：MA2C / IA2C + 智能路由，SUMO 七路口路网 | OA | 高（摘要） |
| 38 | Multimodal Multi-Agent Joint Traffic Simulation With Collision and Run-Off-Road Mitigation ／ IEEE T-ITS ／ 2025 ／ [10.1109/tits.2025.3602664](https://doi.org/10.1109/tits.2025.3602664) | **图结构场景表示（agents + road elements）→ 联合目标集 → 参考线**；显式目标：可解释性（批评潜空间联合分布） | OA | 高（摘要） |
| 39 | Delay-aware multi-agent reinforcement learning for mixed-autonomy platoon control ／ TR-C ／ 2027 ／ [10.1016/j.trc.2026.106054](https://doi.org/10.1016/j.trc.2026.106054) | **延迟观测 + 车队扰动传播结构**（delayed Markov game；multi-agent transformer） | OA | 高（摘要） |
| 40 | MARLens: Understanding MARL for Traffic Signal Control via Visual Analytics ／ IEEE TVCG ／ 2025 ／ [10.1109/tvcg.2024.3392587](https://doi.org/10.1109/tvcg.2024.3392587) | **无显式条件（可视化分析系统）**：信号控制策略的 reward / 队列长度 + 仿真回放 | OA | 高（摘要） |

### 1.4 本表的三条统计结论

1. **18 条中，0 条**以力场 / 势场 / 社会力作为世界模型或生成模型的结构条件模态。
2. **18 条中，0 条**在摘要或（第 4 条）方法节中出现"force field / potential field / social force"作为**条件输入**。
3. 与"社会/交互"最沾边的两条（#7 PIWM、#38）**都把交互放在隐空间或图表示里**——这恰好是 P2 可以拿来立论的对比面（"交互信息一律隐式编码"）。

---

## §2 是否有"力场/势场条件"先例（核心）

### 2.1 结论

**在 18 条文献图内：没有。**
**在 18 条之外（本次定向检索）：找到了 3 个必须处理的相关工作，但无一条与 P2 命题正面冲突。**

### 2.2 三个相关先例（逐条给出与 OTF 的差别）

#### 先例 A（**最危险的一个**）：SPDiff — Social Physics Informed Diffusion Model for Crowd Simulation

- **出处**：Chen H., Ding J., Li Y., Wang Y., Zhang X.-P. *Proc. AAAI 2024*, 38(1): 474–482. DOI [10.1609/aaai.v38i1.27802](https://doi.org/10.1609/aaai.v38i1.27802)；arXiv [2402.06680](https://arxiv.org/abs/2402.06680)
- **它做了什么**：条件扩散模型做**人群（行人）仿真**。摘自摘要与正文（[AAAI 摘要页](https://ojs.aaai.org/index.php/AAAI/article/view/27802)、[arXiv HTML §"Network Parameterization"](https://arxiv.org/html/2402.06680v1)）：
  - 条件输入 `c_t` = **图节点消息（位置/速度/加速度）+ 历史状态**；
  - 网络含 **equivariant crowd interaction module**，输出 **2 维向量即"力"** `f_ped`；`f_ped` 与历史力 `f_hist` 相加，再加**目的地牵引力** `f_dest`，得到输出 `ŷ₀ = a_{t+1}`（**加速度**）。
  - 章节标题即 **"Physics Guided Conditional Diffusion Process"**。
- **与 OTF 场的差别（四条，逐条可写进 P2）**：
  1. **场的位置不同**：SPDiff 的"力"是**去噪器内部的中间表示**，输出量就是力/加速度；OTF 是**外部给定的结构条件模态**（与 HDMap / 3D Box 同级）。
  2. **状态量不同**：SPDiff 生成**加速度**（`a_{t+1}`），**不生成场景/视频/轨迹场**；不是"世界模型"意义上的未来状态生成。
  3. **主体不同**：SPDiff 面向**行人群体**（crowd），不是车辆交通流；OTF 是**车辆交通流社会压力**（超车频次驱动）。
  4. **可解释标量的来源不同**：SPDiff 的力是**学出来的**（EGCL 等变图卷积）；OTF 是**行为学定义的一阶标量**（超车频次），可独立于网络计算、可外部注入。
- **判定**：**不构成 P2 命题的反例**（不是驾驶世界模型、场不是输入型条件）；**但构成"社会力已在生成模型里出现过"的反例**，因此原句的裸"首个"需要 §0.2 的改写。

#### 先例 B：StreamForce — Streaming Video Generation with Streaming Force Control

- **出处**：Wang H. et al., arXiv [2606.07508](https://arxiv.org/abs/2606.07508)（2026-06-05，cs.CV）
- **它做了什么**：流式视频生成框架，**以连续力输入作为控制信号**（"unified force representation as a control signal"），支持局部与全局、时变力。
- **与 OTF 的差别**：① **不是驾驶场景**（通用物理视频生成）；② 力是**用户给的控制信号**（control signal / 蒸馏得到的可控条件），**不是表征交通社会压力的结构条件**；③ 不涉及交通流、不涉及 OTF 这类行为学标量。
- **判定**：不构成 P2 反例；但**"力作为条件/控制信号"的先例已存在**，须在 Related Work 里划清。

#### 先例 C（弱，仅备查）：NIFTY — Neural Object Interaction Fields

- **出处**：Kulkarni et al., CVPR 2024；arXiv [2307.07511](https://arxiv.org/abs/2307.07511)
- **它做了什么**：为物体建 **neural interaction field**（输入人体姿态，输出到"有效交互流形"的距离），**该场引导（guide）物体条件下的人体运动扩散模型的采样**。
- **与 OTF 的差别**：① 任务是人-物交互的**3D 人体运动合成**，非驾驶；② "交互场"是**几何距离场（affordance/contact）**，不是社会压力；③ 场用于**采样引导**，不是结构条件模态本身。
- **判定**：不构成反例。**列入备查**，因为它是"以场引导生成模型"的最干净先例（若审稿人用英文 "field-guided generation" 作为检索词，会命中它）。

### 2.3 另一类必须区分的先例：力场/势场在**非生成式**任务里的先例（大量存在，但不威胁 P2）

本次检索确认"势场 / 安全场 / 社会力"在下列位置**早已成熟**，**但都不是世界模型的条件模态**：

| 用法 | 代表命中（本次检索） | 为什么不同 |
|---|---|---|
| 势场做**规划代价/轨迹跟踪** | GeoPF arXiv [2505.19688](https://arxiv.org/abs/2505.19688)；Time-Varying APF arXiv [2603.13136](https://arxiv.org/abs/2603.13136)；DT-PF Sensors [10.3390/s23229180](https://doi.org/10.3390/s23229180) | 场是**代价函数**，不是生成条件 |
| 势场做**RL 奖励整形** | APF-DPPO, Machines [10.3390/machines10070533](https://doi.org/10.3390/machines10070533) | 场进奖励，不进条件 |
| 社会力做**仿真器底层动力学** | 社会力模型的疏散/人群仿真文献群；Enactor（[arXiv 2606.23588](https://arxiv.org/abs/2606.23588) 引言明确把 SFM 列为行人动力学基线） | 场**替代**了学习模型，不是条件 |
| 社会力做**轨迹预测内的隐式交互** | DMRGCN, AAAI [10.1609/aaai.v35i2.16174](https://doi.org/10.1609/aaai.v35i2.16174)（"estimating social forces among individual pedestrians" 后用图网络聚合） | 力是**中间量**，最终是隐空间 |
| 交互场做**风险预测（非生成）** | RiskNet arXiv [2504.15541](https://arxiv.org/abs/2504.15541)（`field-theoretic model ... via interaction fields and force`） | 用于多维修风险**评估**，不生成未来 |
| 社会力/社会梯度做**MARL 状态表示** | SocialGFs arXiv [2405.01839](https://arxiv.org/abs/2405.01839)（用去噪分数匹配学 social gradient fields 作为**状态表示**） | 场是**表示**，不是条件模态；非驾驶 |

> **注意**：SocialGFs 与本类其余条目**均不在 P2 的 50 条文献图内**（原因：P2 检索设了"驾驶语境锚词"过滤，且 OpenAlex `type:article` 会排除部分会议/预印本）。**这是 P2 文献图的一个真实覆盖缺口**，见 §4。

### 2.4 对标对象 DriveDreamer 的条件模态（核验）

- **出处**：Wang X. et al. *DriveDreamer: Towards Real-world-driven World Models for Autonomous Driving*, ECCV 2024, DOI [10.1007/978-3-031-73195-2_4](https://doi.org/10.1007/978-3-031-73195-2_4)；arXiv [2309.09777](https://arxiv.org/abs/2309.09777)（v2, 2023-11-27）
- **核验到的原文措辞**（[arXiv abs 页](https://arxiv.org/abs/2309.09777)）："In the initial phase, DriveDreamer acquires a deep understanding of **structured traffic constraints**"；"faithfully captures the **structural constraints** of real-world traffic scenarios"。
- **判定**：P2 定位句里"DriveDreamer 的结构条件模态是 HDMap / 3D Box"**与原文一致、可用**。项目内另有 `sources/drivedreamer-2023.pdf`，写入稿件前建议再做一次层 3 逐字核验（见 §5）。

### 2.5 §2 总结判定

| 问题 | 答案 |
|---|---|
| 有没有任何一篇以"交互场/社会力/势场"作为**世界模型的结构条件模态**？ | **本次检索未发现** |
| 有没有以"力/场"作为**生成模型条件或引导**的？ | **有**：SPDiff（社会力去噪引导，行人）、StreamForce（力控制信号，通用视频）、NIFTY（交互场引导，人体运动） |
| P2 的"首个"是否需要降级？ | **不需要从"首个"降级**，但**必须把限定语写实**：从"首个以 OTF 场为结构条件模态"→"首个以 **显式、可解释的**交通流社会压力场为**结构条件模态**的驾驶世界模型"，并在 Related Work 显式对比上述三篇 |

---

## §3 检索与核验方法

### 3.1 通道与取用

| 通道 | 用途 | 取用日期 | 覆盖量 |
|---|---|---|---|
| **OpenAlex API** `api.openalex.org/works/doi:<DOI>` | 18 条逐条取 `abstract_inverted_index` 重建摘要 | 2026-10-13 | 18 条中 **16 条**成功 |
| **Semantic Scholar Graph API** `api.semanticscholar.org/graph/v1/paper/DOI:<DOI>` | 补 2 条 OpenAlex 无摘要者 | 2026-10-13 | 补到 **1 条**（#6）；#4 仍 `abstract=null` |
| **Crossref API** `api.crossref.org/works/<DOI>` | 兜底摘要 | 2026-10-13 | 0 条（两条均无） |
| **DataCite API** `api.datacite.org/dois/<DOI>` | 按 DOI 前缀分流核验 | 2026-10-13 | 2 条均 404（非 arXiv 前缀，**符合预期**） |
| **OpenAlex search** | 8 条定向新颖性检索式（N1–N8） | 2026-10-13 | 累计命中 20,346 条；每式取相关度前 25 逐条读摘要 |
| **arXiv API** `export.arxiv.org/api/query` | 8 条定向检索式（A1–A8） | 2026-10-13 | A1/A3/A5/A6 **0 命中**；A2 1 条；A4 10 条；A7/A8 各 15 条，全部读摘要 |
| **Web 检索 + 落地页/全文抓取** | 定位并读方法节 | 2026-10-13 | 有效抓取 12 个页面（含 2 篇 arXiv HTML 全文、1 篇 ar5iv 全文） |

### 3.2 定向检索式全集（可原样复跑）

**OpenAlex（`search=` 参数，`from_publication_date:2019-01-01`，相关度降序，前 25）**

| ID | 检索式 | 命中 |
|---|---|---|
| N1 | `"social force" AND ("world model" OR "generative" OR diffusion)` | 2,618 |
| N2 | `"potential field" AND ("world model" OR condition AND generation) AND driving` | 3,047 |
| N3 | `"social force model" AND (conditioning OR "conditional" OR "as input")` | 2,882 |
| N4 | `("force field" OR "potential field" OR "interaction field") AND ("scene generation" OR "trajectory generation" OR "world model")` | 2,344 |
| N5 | `"social pressure" AND traffic AND (field OR model)` | 6,351 |
| N6 | `"driving world model" AND (condition OR conditional OR controllable)` | 383 |
| N7 | `"social value orientation" AND ("diffusion model" OR "world model")` | 113 |
| N8 | `"repulsive force" AND ("diffusion" OR "generative model") AND (pedestrian OR vehicle OR traffic)` | 948 |

**arXiv（`search_query`，相关度降序，前 15）**

| ID | 检索式 | 命中 |
|---|---|---|
| A1 | `all:"social force" AND all:"world model"` | **0** |
| A2 | `all:"social force" AND all:"diffusion model"` | 1（= SPDiff） |
| A3 | `all:"potential field" AND all:"driving world model"` | **0** |
| A4 | `all:"interaction field" AND all:"trajectory"` | 10 |
| A5 | `abs:"force field" AND abs:"scene generation"` | **0** |
| A6 | `all:"social pressure field"` | **0** |
| A7 | `all:"driving world model" AND all:"condition"` | 15 |
| A8 | `all:"social force" AND all:"conditional"` | 15 |

**Web 检索用的自然语言检索式（共 8 组，含）**：`social force field conditioning diffusion driving scene generation`、`potential field conditioned trajectory prediction diffusion model driving`、`interaction field world model autonomous driving conditioning`、`social value orientation conditioning diffusion model driving`、`driving safety field world model generation conditioning`、`OTF social pressure field driving world model`、`超车频次 OTF 行车风险场 势场 世界模型` 等。

### 3.3 覆盖条数

- **项目文献图内：18/18 条**（三节全部）完成条件模态判定；其中 **1 条**（#4）读到了方法节而非仅摘要。
- **项目文献图外：** 定向检索后**逐条读摘要**的候选约 **200 条**（OpenAlex 8×25）+ **41 条**（arXiv）+ **12 个抓取页面**。其中**新识别出 3 条与 P2 命题相关的先例**（SPDiff / StreamForce / NIFTY）与 **6 类"场在非条件位置"的用法**（§2.3）。

### 3.4 本节的规范性声明（**写作时可直接引用**）

> 据我们在 **[OpenAlex, arXiv, Semantic Scholar, 通用 Web 检索；2026-10-13]** 的检索，**未发现**以交通流社会压力场（或任何力场/势场/社会力）作为**结构条件模态**的驾驶世界模型。检索式为 §3.2 所列，共覆盖项目文献图 18/18 条与文献图外约 240 条候选。

**不得**写成"不存在"。**也不得**写成"经系统综述确认"。本项目文献图为**代表性抽样**（每式前 60 → 入选 50），本次定向检索亦为**相关度前 N 抽样**，二者都不是系统综述。

---

## §4 不确定性（≥3 条）+ 反证检查

### 4.1 不确定性清单（6 条）

**U1 — 检索深度不对称：18 条里只有 1 条读了方法节。**
#1、#5、#6、#8 是**综述**，摘要完全不透露其内部覆盖了哪些条件模态。**综述里出现"以社会场为条件的驾驶世界模型"是可能的**——尤其 #8（*Social Interactions for Autonomous Driving*）**摘要明确写了覆盖 `social force theory`**。#8 是本次最大的单条盲区。
→ 影响：若 #8 内部举出某一篇"以社会场为条件的驾驶世界模型"，P2 的"首个"会被直接打掉。**必须读全文。**

**U2 — 检索式与词表偏差。**
我的检索式以英文力场术语（social force / potential field / interaction field / force field）为主。**若该先例只用交通工程术语命名**（如 `driving safety field`、`risk field`、`field theory of traffic`、`social pressure`、`interaction-aware`），我的 N1/N3/N4/N8 会漏。
→ 缓解证据：N5（`"social pressure"`）命中 6,351 条、N2 命中 3,047 条，我已读前 25——但**只是前 25**。

**U3 — venue 与类型覆盖缺口（★ 这是 P2 文献图的结构性缺口）。**
本次定位到的 3 篇先例中，**SPDiff 是 AAAI 会议论文**、**NIFTY 是 CVPR 论文**、**StreamForce / Enactor / SocialGFs / RiskNet 是 arXiv 预印本**。P2 文献图的检索式设了 `type:article` + 驾驶语境锚词过滤，**系统性地排除会议论文与预印本**——而 P2 的直接竞争面恰好在 CVPR/ICCV/NeurIPS/ICLR 这条线上。
→ 影响：**"18 条里没有先例"这一结论的证据力，弱于它看起来的样子**。P2 的文献图不能作为新颖性证据。

**U4 — 无法判断的条目（明确"需读全文"）。**
按任务要求逐条列明：

| # | 论文 | 为什么无法从摘要判定 |
|---|---|---|
| 1 | Research on World Models for Connected Automated Driving（Applied Sciences 2025） | 六域综述，摘要只说"多源异构数据融合/物理规律映射"，未列条件模态清单 |
| 5 | World Models for Autonomous Driving: An Initial Survey（T-IV 2024） | 综述，摘要只给"理论/应用/开放问题"三段式 |
| 6 | A survey on occupancy perception（Information Fusion 2025） | 综述，聚焦 3D 占用感知的输入模态与融合，与"条件模态"不同层 |
| 8 | **Social Interactions for Autonomous Driving（FnT Robotics 2022）** | **最需要读**：综述且摘要明确含 social force theory；是否把社会场用作"条件"必须看正文分类 |
| 34 | Game Engine-Based Multi-Agent Model（IJTST 2026） | 摘要为被试实验描述，"行为脚本"的具体条件量未列 |
| 40 | MARLens（TVCG 2025） | 摘要为可视化系统描述，条件量为 reward/queue length 的推论 |

> 另有 **2 条**摘要本身缺失，已用替代通道补到 1 条：
> - #4（TR-C 2026）→ S2 无摘要，**改读 arXiv 全文方法节解决**（§1.1 已标"高"）
> - #6（Information Fusion 2025）→ OpenAlex/Crossref 均无，S2 补到摘要（§1.1 已标"高"）

**U5 — 我读的 SPDiff 是 arXiv v1，不是 AAAI 正式版。**
AAAI 正式版把 arXiv 的 "crowd interaction **module**" 改成了 "crowd interaction **encoder**"（[AAAI 摘要](https://ojs.aaai.org/index.php/AAAI/article/view/27802) vs [arXiv 摘要](https://arxiv.org/abs/2402.06680)）。**措辞变了，机制可能也微调过**。我把 SPDiff 判定为"力是网络内部量"依据的是 arXiv v1 的 §"Network Parameterization"——**须用 AAAI 正式版 PDF 复核**。</br>→ 注意：这个复核**可能反向**——若正式版把社会力改成了**显式条件输入**，SPDiff 的攻击性会上升。

**U6 — 我没有检索中文文献与学位论文库。**
黄梦圆（2023，吉林大学）学位论文定义了 OTF。**中文文献里"行车风险场/势场"与"世界模型"的组合我完全没查**（检索动作：仅 1 次中文 web 检索，未系统化；CNKI/万方/维普无接口）。项目 `AGENTS.md` 已自认此缺口。

### 4.2 反证检查：我最可能错在哪里（红队三条）

**红队①（领域最懂的人）：错在"结构条件模态"这个词的边界。**
最可能的致命质疑：*"SPDiff 的 `f_ped` 已经在去噪器的**每一次条件注入**里起作用了，而且它就叫 conditional diffusion——你说'力不是条件'只是修辞。"*
→ **我承认这是本报告最弱的接缝。** 我的判定依据是"力是网络的**输出量**的构成部分（`f_ped + f_hist + f_dest → ŷ₀`），而非与 `c_t` 并列的**输入条件**"。这个区分**站得住，但脆弱**——它依赖读者接受"条件 = 输入侧"这一约定。
→ **消解所需证据**：读 SPDiff AAAI 正式版 §3 与 Fig.2 的数据流图，确认 `f_ped` 是否同时作为**输入条件**（若图中 `c_t` 含力，则我的区分崩塌）。
→ **缓解设计**：P2 措辞采用 §0.2 的②（"**一阶可解释标量**"），把差异锚在**标量的可解释性与外部可计算性**上，而**不是**锚在"力是不是条件"上。这条锚更硬：SPDiff 的力是学出来的等变嵌入，**不可外部独立计算**；OTF 由超车频次直接算出。

**红队②（方法与统计审稿人）：错在把抽样当穷尽。**
最可能的致命质疑：*"你的 N1–N8 每式只读相关度前 25，命中却有两三千条。用前 25 条断言'未发现'，选择性偏倚是明显的。"*
→ **这条质疑成立，我不辩解。** §3.4 的规范性措辞（"据我们在[通道, 日期]的检索未发现"）就是为了把结论强度限制在检索边界内。
→ **消解所需证据**：对"未发现"这一断言，必须在稿件里**同时给出检索式与截断规则**；若 reviewer 追问，改走 `research-gap-hunter` 的四道闸门 + 一次"倒排"检索（从 DriveDreamer 的引用网络与 CVPR/ICCV 世界模型论文的 Related Work 反向找）。

**红队③（主编/邻域读者）：错在漏了最直白的一条路——"世界模型 + 场"的交叉检索。**
最可能的致命质疑：*"你为什么不去查 DriveDreamer / GAIA-1 / Drive-WM / OccWorld 这些驾驶世界模型的 **Related Work 与引用网络**？真正抢你 novelty 的那篇一定在那里面，不在 OpenAlex 的关键词命中里。"*
→ **这条我确实没做**（只做了关键词通道）。这是方法论上最实质的漏洞。
→ **消解所需证据**：以 DriveDreamer（arXiv 2309.09777）与 A Survey of World Models for Autonomous Driving（arXiv 2501.11260，本次 N2 命中）为种子，展开其**引用网络前向/后向**各 1 层，按"条件模态"逐条打标。

### 4.3 结论强度（据实标注）

| 断言 | 等级 | 说明 |
|---|---|---|
| 18 条文献图内无"场作为条件模态"的先例 | **B** | 18/18 判定了条件模态，但 6 条仅凭摘要（U4） |
| 本次定向检索未发现"场作为结构条件模态的驾驶世界模型" | **C** | 关键词通道 + 前 N 抽样；未做引用网络（红队③） |
| SPDiff 的"力"是网络内部量而非输入条件 | **C** | 依据 arXiv v1；正式版未复核（U5），且该区分本身脆弱（红队①） |
| DriveDreamer 的结构条件为 HDMap/3D Box | **B** | 官方摘要"structured traffic constraints"支持；项目内 PDF 未逐字复核 |

---

## §5 下一步需读全文的清单（具体到论文与章节）

> 按**对 P2 命题的威胁度**降序。**最低成本路径**见文末。

### 第 1 优先级（不读就不能写"首个"）

| # | 读什么 | 读哪一节 | 要找什么（判定问题） | 若命中则后果 |
|---|---|---|---|---|
| **R1** | **SPDiff**, *Social Physics Informed Diffusion Model for Crowd Simulation*, **AAAI 2024 正式版 PDF**（[ojs.aaai.org/…/27802/27636](https://ojs.aaai.org/index.php/AAAI/article/view/27802/27636)） | **§3（Methodology）全节 + Fig. 2 数据流图** + **Appendix A** | ① `f_ped` 是否进入条件集 `c_t`（还是仅参与输出合成）？② 正式版是否把 SFM 改成显式条件输入？ | **若力进入输入侧条件** → P2 措辞**必须**改用 §0.2 的②（一阶可解释标量），不可再用"首个以场为条件" |
| **R2** | **Social Interactions for Autonomous Driving: A Review and Perspectives**（[10.1561/2300000078](https://doi.org/10.1561/2300000078)） | **social force theory 那一节的分类表/综述段**（约 §3–§5）+ **末节 open questions** | 该综述是否列出"以社会力/交互场为条件的世界模型或生成模型"？ | **若列出** → P2"首个"直接失效，须整体重定位 |
| **R3** | **DriveDreamer** ECCV 2024 正式版（项目内 `sources/drivedreamer-2023.pdf`） | **§3.1 Two-stage training / 条件定义句 + Fig. 2 条件输入标注** | "structure condition = HDMap + 3D box"的**逐字原文** | 若无逐字支持 → P2 定位句里的对标描述改为"其结构条件为交通结构约束（HDMap/3D Box）"，降为间接引用 |

### 第 2 优先级（威胁度次高，直接影响 Related Work 写法）

| # | 读什么 | 读哪一节 | 要找什么 |
|---|---|---|---|
| **R4** | **PIWM**, *Dream to Drive With Predictive Individual World Model*（[10.1109/tiv.2024.3408830](https://doi.org/10.1109/tiv.2024.3408830)） | **§III 方法：world model 的状态定义 + 交互建模模块** | `intention-aware latent states` 里是否**显式构造**了交互场/势场（若是，则它是"驾驶世界模型 + 交通交互场"的最强先例） |
| **R5** | **WM-MoE**（[arXiv 2510.21867](https://arxiv.org/abs/2510.21867)；正式版 TR-C [10.1016/j.trc.2025.105456](https://doi.org/10.1016/j.trc.2025.105456)） | **§3.3 Perception Module 输入清单 + §2.1 World Models in AD 综述段** | ① 它的条件输入清单是否真的只有 history+HD map+BEV；② 它的 §2.1 列了哪些驾驶世界模型（**可当作反向检索的种子清单**） |
| **R6** | **StreamForce**（[arXiv 2606.07508](https://arxiv.org/abs/2606.07508)） | **§3 力表示与条件注入方式** | 力是"控制信号"还是"结构条件"；其力表示是否可迁移到交通语义 |
| **R7** | **NIFTY**（[arXiv 2307.07511](https://arxiv.org/abs/2307.07511) / CVPR 2024） | **§3.2 interaction field 定义 + guidance 注入公式** | "field guides diffusion sampling"的**具体注入位置**——这是"以场引导生成"的标准范式，P2 需要说明自己不是这一类 |

### 第 3 优先级（补齐 §4 的六条"需读全文"）

| # | 读什么 | 读哪一节 |
|---|---|---|
| **R8** | #1 Applied Sciences 2025 驾驶世界模型综述 | 条件模态分类表（若有） |
| **R9** | #5 T-IV 2024 世界模型综述 | 同上 |
| **R10** | #6 Information Fusion 2025 占用感知综述 | 输入模态分类（确认"占用"是否被当作结构条件） |
| **R11** | #34 IJTST 2026 游戏引擎多智能体 | 行为脚本的条件量清单 |
| **R12** | #40 TVCG 2025 MARLens | 可视化所依赖的状态量 |

### 第 4 优先级（本次未做、但审稿人可能要求的通道）

| # | 动作 | 具体做法 |
|---|---|---|
| **R13** | **引用网络反向检索**（红队③的消解） | 以 DriveDreamer（2309.09777）与 *A Survey of World Models for Autonomous Driving*（[arXiv 2501.11260](https://arxiv.org/abs/2501.11260)）为种子，展开后向引用 1 层，按"条件模态"逐条打标 |
| **R14** | 中文文献通道 | CNKI/万方检索`行车风险场 + 世界模型`、`势场 + 场景生成`、`社会力 + 扩散模型`（需人工，无接口） |
| **R15** | 会议线补检 | CVPR/ICCV/NeurIPS/ICLR 2024–2026 的 driving world model 论文（P2 文献图的 `type:article` 过滤系统性排除了这条线） |

### 最低成本路径（若时间只够做一件事）

> **只做 R1**：花 20 分钟读 SPDiff 的 AAAI 正式版 §3 + Fig.2。
> 理由：它是唯一一篇"社会力 + 生成模型"且**已经发表在顶会**的工作；它的判定结果**直接决定 P2 措辞用 §0.2 的①还是②**。其余 14 项都是加固，不改结论方向。

---

## 附：本次核验的产物清单（可复跑）

| 文件 | 内容 |
|---|---|
| [`_novelty_tmp/fetch_abstracts.mjs`](_novelty_tmp/fetch_abstracts.mjs) | 18 条 DOI 的 OpenAlex/Crossref 摘要抓取脚本 |
| [`_novelty_tmp/abstracts.json`](_novelty_tmp/abstracts.json) / [`abstracts.txt`](_novelty_tmp/abstracts.txt) | 18 条摘要原始结果（含 `abstract_inverted_index` 重建文本） |
| [`_novelty_tmp/novelty_search.mjs`](_novelty_tmp/novelty_search.mjs) | N1–N8 + A1–A8 定向检索脚本（可原样复跑） |
| [`_novelty_tmp/novelty_search.json`](_novelty_tmp/novelty_search.json) / [`novelty_search.txt`](_novelty_tmp/novelty_search.txt) / [`arxiv_hits.txt`](_novelty_tmp/arxiv_hits.txt) | 定向检索命中与摘要原始结果 |

> 复跑提示（沿用项目既有教训）：**OpenAlex 命中数随时间漂移**，本报告所有命中数均为 **2026-10-13** 取用值；复跑前先确认是否需要。

---

## 限制与风险检查（≥3 条，按项目纪律）

1. **检索非穷尽**：定向检索为关键词通道 + 相关度前 N 抽样，**未做引用网络展开**（红队③）。"未发现"不得升级为"不存在"。
2. **判定深度不均**：18 条中 17 条仅据摘要；6 条（U4）明确无法判定条件模态，其中 #8 是高风险盲区。
3. **SPDiff 版本未对齐**：判定依据为 arXiv v1，AAAI 正式版措辞已变（module→encoder），**未复核**；复核结果可能**反向削弱**本报告对 SPDiff 的区分（红队①）。
4. **会议/预印本通道系统性缺口**：P2 文献图的 `type:article` + 驾驶锚词过滤排除了 CVPR/ICCV/NeurIPS/ICLR 与 arXiv 线，而竞争恰恰在这条线上（U3）。
5. **中文文献与学位论文库未查**（U6）。
6. **DriveDreamer 引文未逐字复核**（项目内 PDF 未读），本节依据官方 arXiv 摘要措辞。
