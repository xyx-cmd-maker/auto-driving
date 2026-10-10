# 混行编队系统级安全的安全强化学习｜Enhancing System-Level Safety in Mixed-Autonomy Platoon via Safe Reinforcement Learning

- **出处**：IEEE Transactions on Intelligent Vehicles, 2024（**卷/期未取得**：Crossref 该记录 `volume`/`issue` 均为空，`page = "1-13"`；本地作者版未印卷期）｜ **类型**：期刊论文
- **作者**：Jingyuan Zhou, Longhao Yan, Kaidi Yang（n=3，均为新加坡国立大学土木与环境工程系）
- **DOI**：10.1109/TIV.2024.3373512
- **全文来源**：`literature/fulltext/fresh2024/tiv2024-safe-rl-platoon__52a625ae.txt`（PAGES=13, CHARS=63,207；MD5=52a625ae67248d5d0e1607ecc8192049）｜ **材料版本**：**作者版／预印本（非 VoR）** — 逐字证据：首页正文下方印有 "arXiv:2401.11148v2 [eess.SY] 1 Mar 2024"；正文含 "A preliminary version of this paper [16] was presented at the 2023 Intelligent Transportation Systems Conference."；版式为单栏作者稿、页码 1–13。
- **正式版存在性核查（T5 前置，动作已执行）**：Crossref `works/10.1109/TIV.2024.3373512`（2026-10-06 取用）HTTP 200，`container-title = ["IEEE Transactions on Intelligent Vehicles"]`，`link` 字段含 `content-version: "vor"`（`http://xplorestaging.ieee.org/ielx7/7274857/7448921/10462535.pdf?arnumber=10462535`）→ **正式版（VoR）存在**（IEEE Xplore arnumber=10462535）。`update-to` 与 `updated-by` 均为 `null` → **未发现撤稿或更正**；`is-referenced-by-count = 27`（Crossref 端点）。DataCite `dois/10.48550/arXiv.2401.11148` 返回 `version = "2"`，与本地版一致。**本卡全部数字取自作者版 v2，未与 VoR 逐页比对**；按 `fresh2024/00-scope.md` §2.2，以正式版为准，作者版仅作阅读材料。
- **分组**：2024+ 增量
- **证据等级初判**：**C 级（经验证据）** — 全部为纯仿真、**单次运行**、5 车编队且**仅 1 辆 CAV** 的单车道算例，无种子/重复/CI/实车。**但形式化部分独立成立**：CBF 前向不变性对 **CAV 自身的头时距硬约束**是定理级保证（依赖由学习辨识得到的 HDV 模型）；对后随 HDV 的约束带松弛变量，作者自承非保证。→ 引用其"安全保证"时必须按此二分限定。
- **档位建议**：A 精读 / B 略读 / C 仅引用 / D 排除 — **B 略读**。理由：加权 11 落在 9–13；其价值集中在**方法层**（可微 CBF-QP 安全层与"系统级安全"的口径），而算例规模、单车受控、无代码/无统计的现状使它不值得占用 A 档预算。
- **五维打分（母协议 §5，各维 0–2，满分 20）**：D1=1 D2=1 D3=1 D4=2 D5=1 → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = **11** → **B 档（9–13）**
  ⚠ **必须 0–2 制**；D4 一律指**时效性**（2024+ 基本应为 2）。
  - **D1=1 依据**：母协议 D1 一分档逐字点名"**安全约束**"为 P1 的相邻环节——本文正是可微 CBF-QP 安全层，提供术语、基线候选与对照设计，但**不直接测 P1 的 RQ**（无 OTF、无连续时间网络、无多车道、无编队级多车受控）。故不能给 2。
  - **D2=1 依据**：对照策略齐备（4 组模型）且有多场景闭环（训练场景 + 2 个安全关键场景 + 安全域扫描），**但"有统计"不成立——单次运行、无重复、无检验、无 CI**，故落在"仿真"档。
  - **D3=1 依据**：方法（安全层架构、降阶 CBF 构造、物理计算图 + NN 偏置的辨识拆分）可部分迁移；**数据/代码/协议不可直接复用**（全文无 code/data availability，实验协议非基准协议）。
  - **D5=1 依据**：有结果但缺细节——全文无表格、无代码/数据、效应量仅 3 个孤值（60%、0.8 s、MSE），且**手上是作者版而非 VoR**。

## 1. 标题
Enhancing System-Level Safety in Mixed-Autonomy Platoon via Safe Reinforcement Learning ｜ 中文直译：通过安全强化学习提升混行自动驾驶编队的系统级安全性

## 2. 摘要（≤400 字中文，保留关键数字与结论成立条件）

网联自动车（CAV）的纵向控制可提升混行交通的效率、稳定性与安全，深度强化学习（DRL）因"充分离线训练后可实时应对复杂场景"而具前景。作者指出 DRL 混行编队控制的三个空白：① 缺乏理论无碰撞保证；② 普遍假设驾驶员熟练理性、不会追尾前车（因而只考虑自车安全）；③ 强假设人类驾驶模型已知。为此提出安全 DRL 控制器：把**控制屏障函数（CBF）安全约束**与 DRL 通过**基于二次规划（QP）的可微神经网络层**结合，给出理论安全保证；把**系统级安全约束**纳入以同时覆盖 CAV 与其**后随** HDV（应对非理性人类驾驶）；并用**基于学习的系统辨识**估计真实系统中未知的人类跟驰行为。仿真表明该方法保证 CAV 安全、提升混行编队中 HDV 的安全性，同时提升通行能力与弦稳定性（**本卡核验：后两项在正文中没有对应的度量值，见 §3 与 §6 陷阱 2**）。**结论成立条件**：单车道高速路段（直线或曲线）、5 车编队、**第 3 辆为 CAV、其余为 HDV，且 |ΩC| = 1**（论文明确"假设编队内只有一辆 CAV"）、HDV 由最优速度模型（α=0.6、β=0.9、s_st=5、s_go=35）生成、平衡间距 20 m、平衡速度 15 m/s。

## 3. 结论（≤350 字中文：作者结论节要点 + 关键数字 + 作者自承的局限）

结论节要点：把 DRL 与可微 CBF 层结合以实现**系统级驾驶安全**；用基于学习的人类驾驶员行为辨识获得混行中未知的 HDV 动力学；通过构造综合奖励把交通效率与弦稳定性纳入优化。仿真结果表明该方法在提供系统级安全保证的同时提升效率与稳定性；**安全层通过收窄探索范围加速了训练**（Fig. 3：500 回合内两者均收敛，带安全层者收敛更快）。**关键数字**：安全域在场景 1 扩大 "almost 60%"；场景 2 中后随 HDV 的安全持续时间**平均增加 0.8 s**；系统辨识加速度预测 MSE **0.0019**（本文）vs **0.0024**（RLS），对象为 vehicle 4。**作者自承的局限（关键）**：对后随 HDV 的 CBF 保证**不成立**——逐字 "it should be noted that the assurance for the value of the CBF candidate for the following HDVs within the safe set is not guaranteed but rather enhanced"（因其为带松弛变量的软约束）；未来工作：决策 Transformer 应对时变车辆数、多智能体 RL 扩展到多 CAV、meta-RL 提升泛化、扩展到汇入/分流/交织段与城市道路。**本卡核验的补充局限**：Abstract 所称"通行能力"与"弦稳定性"提升在实验节无任何度量值；全部结果为单次仿真，无种子/重复/CI/实车，且无代码数据发布。

## 4. 方法一句话（≤60 字，必须含「输入 → 模型 → 输出」三要素）

前/后车状态 + 在线辨识的 HDV 跟驰模型 → PPO 策略经可微 CBF-QP 安全层修正 → 输出满足头时距约束的 CAV 加速度。

## 5. 图表清单（占位符）

> 图注逐字取自全文 txt，按 ≤100 字符截断，其余逐字未改。**正文共 11 个 Figure、0 个 Table（合计 11，已全覆盖）**；全部图均为曲线图或区域色块图，**无任何表格**（grep `TABLE` / `Table ` 零命中于图表语境）。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-tiv-safe-1} | Fig. 1 | Overview of the proposed controller for CAVs in mixed-autonomy traffic framework, the dotted line represents backpropagation of the differentiable QP. | 三模块总览：RL 控制器（Actor/Critic）、学习型人类驾驶员行为辨识、可微安全层（CBF-QP）。**虚线=可微 QP 的反传路径**，是全方法的架构核心。 |
| {FIG-tiv-safe-2} | Fig. 2 | Learning-based human driver behavior identification module. | 辨识模块结构：物理计算图（估 α₁,α₂,α₃）+ 神经网络偏置估计。要点：拆分是为了给 CBF 提供**解析偏导**。 |
| {FIG-tiv-safe-3} | Fig. 3 | Training rewards per episode. | 500 回合训练奖励曲线（safe-RL with SI vs PPO without safety guarantee）。要点：两者均收敛，带安全层者更快——**单次运行，无重复**。 |
| {FIG-tiv-safe-4} | Fig. 4 | Comparison between online learning-based system identification and RLS. | 在线辨识 vs 递归最小二乘的加速度预测（200 时间步，Ground Truth / Proposed / RLS 三条曲线）。要点：本文方法贴合更好，但**无误差棒**。 |
| {FIG-tiv-safe-5} | Fig. 5 | Safety-guaranteed regions associated with two specific scenarios: (a) the deceleration disturbance of the preceding vehicle and (b) the acceleration disturbance of the… | **全文最重要的图**：横轴扰动幅值、纵轴持续时间；深蓝=无安全层的安全域，浅蓝=有安全层**扩张出来的**域，白=不安全区。(a) 扩张近 60%，(b) 后随 HDV 安全持续时间平均 +0.8 s。 |
| {FIG-tiv-safe-6} | Fig. 6 | Value of the CBF candidate for CAV when the preceding vehicle emergency decelerates. | CAV 的 h_th,2(x) 时程（3 条曲线：safe-RL with SI / PPO 无安全层 / 纯跟驰）。要点：PPO 无安全层时 h 变负=碰撞；本文方法全程 ≥0。 |
| {FIG-tiv-safe-7} | Fig. 7 | Spacing, velocity and acceleration for vehicles in scenario 1. (a), (b), (c) are the results for safe-RL with SI. (d), (e), (f) correspond to the results for PPO… | 场景 1 的**逐车**（Vehicle 0–4）间距/速度/加速度时程。(c) 中本文控制输入仍在执行器上界（红虚线）内，对应式 (20) 的可行性约束。 |
| {FIG-tiv-safe-8} | Fig. 8 | Value of the CBF candidate for vehicle 3 when it accelerates emergently. | 后随 HDV（vehicle 3）的 h_th,3(x) 时程，4 条曲线。要点：**safe-RL with SI 与 w/o SI 都避免碰撞** → 该例中辨识精度影响很小。 |
| {FIG-tiv-safe-9} | Fig. 9 | Value of the CBF candidate for vehicle 4 when it accelerates emergently. | 后随 HDV（vehicle 4）的 h_th,4(x) 时程。要点：**只有 safe-RL with SI 保证安全**（w/o SI 也碰撞）→ 全文论证"辨识精度重要"的关键图。 |
| {FIG-tiv-safe-10} | Fig. 10 | Spacing, velocity and acceleration for vehicles in scenario 2 when vehicle 4 accelerates. (a), (b), (c) are the results for safe-RL with SI. (d), (e), (f) show the… | 场景 2 逐车时程（4 组 × 3 面板）。⚠ 图注写 vehicle 4，正文却把 vehicle 3 归给 Fig. 10（见文末 ⚠）。 |
| {FIG-tiv-safe-11} | Fig. 11 | Spacing, velocity and acceleration for vehicles in scenario 2 when vehicle 5 accelerates. (a), (b), (c) are the results for safe-RL with SI. (d), (e), (f) show the… | 场景 2 逐车时程（4 组 × 3 面板）。⚠ 图注写 vehicle 5，正文写 vehicle 4，而全篇只有 Vehicle 0–4（见文末 ⚠）。 |

## 6. 对 P1 的用处

- **与 P1 的关系**：**相邻问题**。它不测 P1 的 RQ（无 OTF、无连续时间网络、无多车道、无编队级多车受控），但它给出的正是母协议 D1 一分档里点名的"**安全约束**"环节——一个可微、可证明、可与任意 RL 策略耦合的**安全层**。
- **可迁移**：
  1. **安全层架构可直接对应 P1 的"大胆决策，小心修正"**：u = u_RL + u_safe，u_safe 由 CBF-QP 求出，并通过 KKT 条件对 QP 求导把梯度回传到策略网络（式 22–26）。P1 若按 `AGENTS.md` §6 的架构原则做 MPC+LNN 混合闭环，"学习器出意图 + 优化层做安全修正 + 梯度回流"这条路径有了**同构的可引用先例**。
  2. **"系统级安全"的口径可借用（责任边界）**：不只保本车，还要保**后方**被自身动作影响的 HDV。这正是 P1 在混行 ODD 下必须声明的责任边界（CAV 的动作会改变后随人工车的行为）。其**降阶 CBF 构造** h_j = h_th,j − h_th,i = s_j − s_i − τ(v_j − v_i) ≥ 0（式 15，把相对度从 j−i+1 降到 1）是一个具体可用、避免高阶 CBF 求导的技巧。
  3. **学习型 HDV 辨识的"可解释核 + 神经残差"拆分**（式 12：α₁s − α₂v + α₃v_{i−1} + ζ_ψ）——把线性物理计算图与 NN 偏置分开训练，既保留解析偏导（供 CBF 用）又不牺牲非线性精度。这与 P1 "CfC 递归分量 + 可解释 OTF 标量"的拆分哲学一致，是 Related Work 里一条**方法论旁证**。
  4. **失败场景可直接参数化进 P1 的长尾清单**：前车紧急制动（−4 m/s² × 2.5 s，随后低速保持 2.5 s）、后随车误加速（+1 m/s² × 4 s，随后高速保持 4 s）。P1 的长尾清单里有"前车急刹"但缺具体参数与持续时间，这里可直接取用为 CARLA 场景参数。
  5. **"安全域"可视化范式**：横轴扰动幅值、纵轴持续时间、色块区分"有/无安全层的安全域"——比单条时程曲线更能刻画鲁棒边界。P1 报 A1（OTF 开/关）消融时可用同型图给出"有效域"差异。
  6. **奖励设计的两个阈值可直接引用为对照**：TTC 阈值 4 s（式 11，并引文献称 car-car 跟驰对的 TTC 统计中位数约 4 秒）、headway 阈值 2.5 s（式 10）。
- **不可迁移 / 陷阱**：
  1. **规模差一个量级、且是"单车受控"**：5 车编队、**仅 1 辆 CAV**（逐字 "we assume that only one CAV is present in the platoon, i.e., |ΩC| = 1"）、单车道，且论证前提是"CAV 渗透率在部署早期很低"。P1 是**编队级（多车受控）多车道**。其 "system-level safety" 是在 **1 个受控车 + 4 个 HDV 的链条**上成立的，**不是编队级协同安全**；P1 不得把它当作"多车编队安全"的证据。
  2. **弦稳定性与通行能力只进了奖励，没有进结果**：Abstract 与结论声称 "enhancing traffic capacity and string stability"，但 §V 只报安全域与碰撞。本卡核验：全文 `capacity` 仅出现于 Abstract 与参考文献 [6] 的标题，`string stability` 仅出现于 Abstract、奖励式 (9) 的说明、结论与未来工作。→ **没有任何通行能力指标，也没有任何弦稳定性度量（无传递函数、无 ‖H(jω)‖∞、无放大率）**。引用它做"弦稳定性更好 / 通行能力更高"的论据属**超出证据**；P1 若需要弦稳定性，得自己算。
  3. **HDV 模型是最优速度模型（OVM），不是 IDM**：F = α(V(s_i) − v_i) + β(v_{i−1} − v_i)，V(s) 为余弦型（式 27–28），α = 0.6、β = 0.9、s_st = 5、s_go = 35，平衡间距 20 m、平衡速度 15 m/s。同时**假设 F(·) 的形式与参数对 CAV 均未知**（逐字 "we make a realistic assumption that both the formulation and parameters of F(·) remain unknown to the CAV"）。讨论"混行里 HDV 用什么模型"时，这两句必须一起带上。
  4. **形式化保证的边界必须写明**：硬约束只有 CAV 自己的头时距 h_i(x) = s_i − τv_i ≥ 0（τ = 0.3 s）；对后随 HDV 的约束带松弛变量 σ_j，作者自承 "not guaranteed but rather enhanced"。→ **标题与摘要里的 "system-level safety guarantee" 强于被证明的内容**，这是引用时最容易被审稿人抓的一句，P1 必须逐字带限定。
  5. **我们手上不是 VoR**：本卡数字全部来自 arXiv:2401.11148v2。引用前须下载 IEEE Xplore 正式版（arnumber=10462535）核对 "almost 60%"、"average of 0.8s" 与 "0.0019 / 0.0024"，并核对 Fig. 5 的安全域度量口径。
  6. **无代码/无数据**：全文无 code availability / GitHub / 数据说明。P1 **无法复现**其 CBF-QP 层与可微 QP 层，只能重写；因此**不得**声称"我们复现了该安全层"（`AGENTS.md` §1 对 TD3 基线的同类纪律）。
  7. **单次运行、无不确定度**：MSE 0.0019 vs 0.0024（相对差约 21%）在单次运行下**不构成证据**；P1 不得引用为"学习型辨识优于 RLS"。
  8. **ODD 交集只有"单车道纵向混行"**：它不做侧向、不做多车道、不做汇入/分流/交织（未来工作明确列为待做）。P1 的"多车道 + 车道居中偏差 + 前轮转角方差"与它的实验设置**无交集**。
  9. **实验数据的来源未说明**：训练/测试用的是 OVM 生成的合成轨迹还是真实数据，**正文未交代**（§V-A 只说用 OVM 作 F，扰动为高斯噪声）。P1 不得把它当作"真实数据驱动"的工作。
- **引用时必须带的限定语**：**"该工作（作者版 arXiv:2401.11148v2）报告：在单车道、5 车编队、仅 1 辆 CAV、HDV 由最优速度模型（α=0.6, β=0.9）生成的数值仿真中，CBF-QP 安全层把（扰动幅值 × 持续时间）平面上的安全域扩大近 60%、把后随 HDV 的安全持续时间平均延长 0.8 s；其形式化保证只覆盖 CAV 自身的头时距硬约束（τ = 0.3 s），对后随 HDV 的约束带松弛变量、作者自述为 'not guaranteed but rather enhanced'；结果基于单次仿真，未报告种子、重复次数或置信区间，无实车验证，且摘要所称的通行能力与弦稳定性提升在正文中没有对应度量值。"**

### ★ 特别要求逐项（本批次指定）

**① Safe RL 用的是哪种形式**：**不是约束 MDP、也不是拉格朗日法**，而是 **CBF 安全层 + 可微 QP 的联合训练**（论文自述 "combining CBF and DRL via a QP-based differentiable neural network layer"）。流程：PPO actor 输出 u_RL → 解 **CBF-QP**（式 21，目标 min ‖u_safe‖² + Σ b_jσ_j²，含 CAV 硬约束、后随 HDV 软约束、可行性约束、执行器上下界）得残差 u_safe → 最终动作 **u = u_RL + u_safe**；再用 **KKT 条件对 QP 求导**得到 ∂u_safe/∂u_RL 与 ∂u_safe/∂θ_CBF（式 22–26），使 θ_CBF = {k_i,…,k_n, k_f} 与策略网络**同时训练**（"allowing for adaptive adjustments to the training environment"）。奖励函数里**确有**安全项（TTC 的对数型惩罚，式 11，阈值 4 s），但它只是**软激励**；安全保证来自 CBF-QP，不来自奖励。松弛变量 σ_{i+1}…σ_n 的罚系数 b_j 全部设为 1。

**② "system-level safety" 怎么定义与度量**：
- **定义**：同时保证 **CAV 与其后方所有 HDV** 的头时距安全条件 **s_j ≥ τ v_j，j ∈ {i, …, n}**（式 13；CAV 索引 i，后随 HDV 索引 i+1,…,n；τ 为最小允许车头时距，取 **0.3 s**）。由于后随车的原始 CBF 候选 h_th,j 相对度为 j−i+1 ≥ 2，作者用**降阶构造**（式 15）：**h_i(x) = s_i − τv_i**（与 h_th,i 相同，保 CAV 自身）与 **h_j(x) = h_th,j − h_th,i = s_j − s_i − τ(v_j − v_i) ≥ 0**（j ∈ {i+1,…,n}），并指出 h_j ≥ 0 是 h_th,j ≥ 0 的**充分条件**，从而"ensures system-level safety"，且相对度保持 1。
- **度量**：(a) **安全域（safety-guaranteed region）**——在（扰动加速度幅值 × 持续时间）平面上比较有/无安全层的安全区（Fig. 5）：场景 1 扩大 **"almost 60%"**，场景 2 中后随 HDV 的**安全持续时间平均 +0.8 s**；(b) **案例研究**——逐车 CBF 候选值 h 的时程是否全程 ≥ 0（Fig. 6 对 CAV 的 h_th,2、Fig. 8 对 vehicle 3 的 h_th,3、Fig. 9 对 vehicle 4 的 h_th,4）与**是否发生碰撞**（由间距/位置轨迹判断）。
- ⚠ **关键限定**：对后随 HDV 的约束是**带松弛变量的软约束**，作者自承其安全性是 "enhanced" 而非 "guaranteed"。**因此"system-level safety guarantee"这一措辞的严格覆盖范围只有 CAV 自身的头时距硬约束。**

**③ 混行里 HDV 用什么模型**：**最优速度模型 OVM（Bando 等 1998，该文参考文献 [42]）**，逐字 "Without loss of generality, we choose the optimal velocity model (OVM) [42] as the car-following model F, following the setting of LCC [7]. Note that the OVM can be replaced by any car-following model without influencing the applicability of the proposed method." 形式为 F = α(V(s_i(t)) − v_i(t)) + β(v_{i−1}(t) − v_i(t))（式 27），V(s) 为分段余弦型期望速度（式 28）；参数 **α = 0.6、β = 0.9、s_st = 5、s_go = 35**，平衡间距与速度 **20 m / 15 m/s**；**v_max 未在正文给出数值**。**不是 IDM。** 且关键设定是"模型形式与参数对 CAV 均未知"，由学习型系统辨识模块估计（式 12：α₁s_i − α₂v_i + α₃v_{i−1} + ζ_ψ(s_i,v_i,v_{i−1})，其中线性计算图对应 α₁ = ∂F̂/∂s、α₂ = −∂F̂/∂v、α₃ = ∂F̂/∂v_{i−1}）。训练阶段另加高斯速度扰动（零均值、标准差 **2 m/s**，每时间步独立，乘以时间步 **0.1 s** 后加到头车速度上）。

**④ 是否给出逐车误差传播或弦稳定性结果**：
- **弦稳定性：没有给任何度量值。** 见 §6 陷阱 2 的核验（grep `capacity` / `string stability` 的全部命中位置）。
- **逐车层面给的是两类证据**：(i) **逐车轨迹时程**——Fig. 7 / Fig. 10 / Fig. 11 均画出 **Vehicle 0–4 全部 5 辆车**的间距、速度、加速度（3 面板 × 4 组对照）；(ii) **逐车约束时程**——Fig. 6（CAV 的 h_th,2）、Fig. 8（vehicle 3 的 h_th,3）、Fig. 9（vehicle 4 的 h_th,4）。
- **结论**：**有逐车轨迹级与逐车约束级证据，无误差传播度量、无弦稳定性判据、无 head-to-tail 放大率。** P1 若需逐车误差传播，必须自算。

### 闭环 / 实车 / 统计（逐字证据）

- **有没有闭环**：**有，但是仿真闭环**。PPO 与含 OVM 的 HDV 环境交互训练，逐字 "The training episodes are 500."，测试也在该环境的变体上闭环推进（"we evaluate the proposed method in simulations of a typical mixed-autonomy platoon"）。**注意：全文从未出现 "closed-loop" 字样（grep 零命中）**，措辞一律为 "simulations"。
- **有没有实车**：**没有**。grep `real vehicle` / `field test` / `hardware` **全部零命中**；Abstract 与结论一律写 "Simulation results demonstrate…"。作者把向汇入/分流/交织段与城市道路扩展**列为未来工作**。
- **有没有统计检验 / CI / 种子**：**三者皆无**。逐字证据：唯一定量比较是 "The mean square error is 0.0019 for the proposed method and 0.0024 for RLS."（对 vehicle 4 的加速度预测，**单次**）；训练曲线 Fig. 3 为**单次运行**；**grep `seed` / `confidence` / `p-value` 全部零命中**，无重复次数说明，无标准差。

## 7. 缺失信息（≥3 条，写成可执行动作）

1. **取 VoR 并核对三个关键数字 + 安全域的度量口径**：正文只说 "the safety region is expanded by almost 60%"，**60% 的口径未说明**（是面积比？网格格点数比？还是某一维度的边界位移比？），0.8 s 是"平均"但未给样本与分布。→ **动作**：从 IEEE Xplore（arnumber=10462535）下载正式版，逐字核对 "almost 60%" / "average of 0.8s" / "0.0019 / 0.0024"，并找出安全域的精确度量定义；若 VoR 仍未定义，直接向作者索取（jingyuanzhou@u.nus.edu、kaidi.yang@nus.edu.sg）。
2. **补种子与重复，或明确降级措辞**：全文无种子、无重复次数。→ **动作**：向作者索取代码后固定 ≥5 个种子重跑 500 回合训练与两个测试场景；**在拿到重复结果之前，P1 引用 60% 与 0.8 s 时只能写"单次仿真报告值，未给不确定度"，且不得进入任何对照表。**
3. **补弦稳定性度量**：全文无弦稳定性数值（§6 陷阱 2）。→ **动作**：用其式 (5)–(7) 的状态空间（OVM 参数 α=0.6、β=0.9）在频域计算 head-to-tail 传递函数 ‖H(jω)‖∞，把结果作为 **P1 自己的计算值**报告并注明"依据该文模型"，**不得**写成"该文报告弦稳定性提升"。
4. **补通行能力定义与数值**：Abstract 提 "traffic capacity"，正文无任何流量/通行能力数值（式 10 只把 headway 阈值 2.5 s 写进奖励）。→ **动作**：若 P1 需要通行能力对比，须自行定义稳态流量（如 v/s）并自测；不得引用该文的"提升通行能力"。
5. **核实场景 2 的扰动对象与图号**：图注与正文三处不一致（详见文末 ⚠）。→ **动作**：以 VoR 为准确认 Fig. 10 / Fig. 11 各自对应的加速车辆编号；在确认之前，P1 引用该例时**只写"后随 HDV 误加速场景"，不得指认具体车号**。
6. **补齐 OVM 的 v_max 与仿真时长/时间步**：正文给了 α、β、s_st、s_go 与平衡态（20 m、15 m/s），**未给 v_max 数值**；训练时间步在扰动设定中写作 0.1 s，但正文未写出测试仿真时长。→ **动作**：从 VoR 或作者处补齐 v_max 与仿真时长，否则 P1 无法复现其场景。
7. **索要代码与数据**：全文无 code/data availability。→ **动作**：邮件作者索取 CBF-QP 与可微 QP 层实现及实验脚本；**在此之前 P1 不能声称复现该安全层**。
8. **核对 τ = 0.3 s 的取值依据**：正文只写 "the minimum time headway τ is set to 0.3s"，**无出处、无敏感性分析**，而 τ 直接决定安全域的宽窄。→ **动作**：P1 若采用安全层，须自行做 τ 的敏感性扫描（建议 τ ∈ {0.3, 0.6, 0.9, 1.2} s）并报告，同时说明 τ=0.3 s 与 CACC 常用 0.6–1.5 s 的差异。
9. **确认实验轨迹的来源**：训练/测试的状态轨迹是 OVM 生成的合成数据还是真实轨迹，正文未交代。→ **动作**：查 VoR 的 §V 或作者代码；在此之前不得把该文归为"真实数据驱动"的工作。

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 编队规模 | 5 辆车（第 3 辆为 CAV，其余 4 辆为 HDV） | — | §V（"Simulation Results"） |
| CAV 数量 | 1（|ΩC| = 1，"only one CAV is present in the platoon"） | — | §III |
| 道路 | 单车道高速路段（直线或曲线） | — | §III |
| HDV 跟驰模型 | OVM（Bando 等 1998） | — | §V-A（式 27–28） |
| OVM 参数 | α = 0.6，β = 0.9，s_st = 5，s_go = 35 | 未报告 | §V-A |
| 平衡间距 / 平衡速度 | 20 m / 15 m/s | 未报告 | §V-A |
| v_max | **未在正文给出数值** | — | 本卡核验 |
| 训练速度扰动 | 高斯，零均值、标准差 2 m/s，每时间步独立，乘时间步 0.1 s | 未报告 | §V-A |
| 训练回合数 | 500 | 未报告 | §V-A |
| 学习率（actor 与 critic） | 0.0003（线性衰减） | — | §V-A |
| batch size / GAE 衰减 / PPO clip / experience 利用次数 | 2048 / 0.95 / 0.2 / 10 | — | §V-A |
| 系统辨识学习率 | 0.0001 | — | §V-A |
| 最小允许车头时距 τ | 0.3 s | 未报告（无敏感性分析） | §V-A |
| CBF 可训练参数初值 | {k₀, k₁, k₂, k_f} = {1, 1, 1, 10} | — | §V-A |
| 松弛变量罚系数 b_j | 全部设为 1 | — | §IV-C-1 |
| TTC 阈值（安全奖励） | 4 s（并引文献称 car-car 跟驰对 TTC 统计中位数约 4 秒） | — | 式 (11) |
| headway 效率阈值 | TH_i ≥ 2.5 s 时奖励 −1 | — | 式 (10) |
| 系统辨识精度（vehicle 4，加速度预测 MSE） | **0.0019**（本文）vs **0.0024**（RLS） | **未报告**（单次运行） | §V-A |
| 安全域扩张（场景 1，前车减速扰动） | "expanded by almost 60%"（**度量口径未说明**） | 未报告 | §V-B-1 |
| 后随 HDV 安全持续时间（场景 2） | 平均 +0.8 s | 未报告 | §V-B-1 |
| 场景 1 扰动参数 | 前车（索引 0 或 1）以 −4 m/s² 减速 2.5 s，低速保持 2.5 s，再加速回平衡 | — | §V-B-2 |
| 场景 2 扰动参数 | 后随 HDV 以 1 m/s² 加速 4 s，高速保持 4 s，再减速回平衡 | — | §V-B-3 |
| 场景 1 结果 | 纯跟驰与 safe-RL with SI 的 CBF 候选值 > 0（无碰撞）；PPO 无安全层**发生碰撞** | — | §V-B-2（Fig. 6–7） |
| 场景 2 / vehicle 3 结果 | 纯跟驰与 PPO 无安全层**碰撞**；safe-RL with SI 与 w/o SI **均避免碰撞**（"the safety impact of disturbances resulting from inaccurate dynamics is minimal"） | — | §V-B-3（Fig. 8、Fig. 10） |
| 场景 2 / vehicle 4 结果 | 纯跟驰、PPO 无安全层、safe-RL **w/o SI 均碰撞**；**仅 safe-RL with SI 保证安全** | — | §V-B-3（Fig. 9、Fig. 11） |
| 对照模型 | 4 类：pure car following / PPO without safety guarantee / safe-RL without SI / safe-RL with SI | — | §V |
| 弦稳定性度量值 | **全文未见**（grep 仅命中 Abstract、式 9 说明、结论、未来工作） | — | 本卡核验 |
| 通行能力度量值 | **全文未见**（grep `capacity` 仅命中 Abstract 与参考文献 [6] 标题） | — | 本卡核验 |
| 代码/数据可用性声明 | **全文未见** | — | 本卡核验 |
| 前身会议论文 | Zhou, Yan, Yang, "Safe reinforcement learning for mixed-autonomy platoon control," 2023 IEEE 26th ITSC, pp. 5744–5749 | — | §I（参考文献 [16]） |

---

⚠内部不一致：场景 2 的图号与车号三处不符。正文写 "In Fig. 10, both pure car following and PPO without safety guarantee fail to prevent a collision **when vehicle 3 accelerates**"、又写 "In Fig. 11, **if vehicle 4 accelerates**, collisions occur when applying pure car following, PPO without safety guarantee, or safe-RL without SI"；但 **Fig. 10 图注写 "when vehicle 4 accelerates"、Fig. 11 图注写 "when vehicle 5 accelerates"**；而全篇仿真只含 Vehicle 0–4（5 车编队），**vehicle 5 不存在**。

⚠内部不一致（主张-证据缺口）：Abstract 与结论声称 "enhancing traffic capacity and string stability"，但 §V 未报告任何通行能力指标、也未报告任何弦稳定性度量——全文 `capacity` 仅出现于 Abstract 与参考文献 [6] 标题，`string stability` 仅出现于 Abstract、奖励式 (9) 的说明、结论与未来工作。

⚠内部不一致（保证强度）：标题与摘要使用 "system-level safety guarantee"，但作者在 §V-B-3 自承对后随 HDV 的约束为软约束——逐字 "the assurance for the value of the CBF candidate for the following HDVs within the safe set is not guaranteed but rather enhanced"。

⚠内部不一致（符号）：式 (12) 中偏置估计项写作 ζ_ψ,i(s_i, v_i, v_{i−1})，但紧随其后的解释句写作 "η_ξ,i(s_i, v_i, v_{i−1}) := α₁s_i − α₂v_i + α₃v_{i−1} represents a physics-based computation graph"，把 ζ_ψ,i 与 η_ξ,i 的符号对调了一次（后文 "the construction of CBF requires the estimation of the partial derivatives of F̂_i, i.e., α₁ = F̂_i/∂s_i, α₂ = −F̂_i/∂v_i, α₃ = F̂_i/∂v_{i−1}" 中 ∂ 符号也脱漏）。

---
**字数实测**：§2 摘要 = 332 汉字（含中文标点 382）；§3 结论 = 303 汉字（含中文标点 340）；§4 方法一句话 = 37 汉字（含中文标点 38）。
**取用记录**：Crossref `works/10.1109/TIV.2024.3373512` 与 DataCite `dois/10.48550/arXiv.2401.11148`，取用日 2026-10-06，均 HTTP 200（版本与更正检查，见页首）。
