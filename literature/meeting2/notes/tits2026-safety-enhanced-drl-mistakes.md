# 敢犯错的动态安全引导 DRL｜Safety-Enhanced Deep Reinforcement Learning for Autonomous Driving: Dare to Make Mistakes to Learn Better and Faster

- **出处**：IEEE Transactions on Intelligent Transportation Systems, Vol. 27, No. 5, May 2026, pp. 5136–5148（起始页 5136；全文 13 页）｜ **类型**：期刊论文
- **作者**：Zhuoren Li（Tongji University）et al.（Bo Leng, Lu Xiong, Tongji University；Arno Eichberger, Graz University of Technology；Chao Huang, The University of Adelaide；Jia Hu（通讯）, Tongji University）
- **DOI**：10.1109/TITS.2026.3670584
- **全文来源**：`literature/fulltext/meeting2/safety-enhanced-deep-reinforcement-learning-for-autonomous-d__8e6c5959.txt`
- **分组**：决策基线 / TITS
- **证据等级初判**：B 级 — 三模型闭环对照（baseline / SSE-DRL / PSE-DRL）+ 两模块单因素消融 + 3 次训练 × 多交通密度 6 次测试 + 两个代表性场景案例，设计属"良好但有边界"；边界是**全部为 Highway-env 纯仿真、无实车、3 次运行且未报种子/CI/显著性检验、六张表表体在可得全文中缺失**（等级判据：平台边界写进理由，不因"仿真"二字单独降级；但本文的统计强度明显弱于同组另两篇）
- **档位建议**：B 略读 — 加权 13 落在 B 档（9–13），且 D1 = 1（相邻环节：**高速公路换道决策**的安全约束与风险经验回放方法，ODD 与本项目最接近，但任务是换道决策而非编队控制，不提供 P1 可复用的评价协议），不满足 A 档"D1 = 2"的硬条件
- **五维打分**：D1=1 D2=2 D3=1 D4=2 D5=1 → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = 3+4+2+2+2 = **13**

## 1. 标题
Safety-Enhanced Deep Reinforcement Learning for Autonomous Driving: Dare to Make Mistakes to Learn Better and Faster｜面向自动驾驶的安全增强深度强化学习：敢于犯错，才能学得更好更快

## 2. 摘要（≤400 字中文，保留关键数字与结论成立条件）

DRL 已成为自动驾驶的重要方法，但其运动规划在**学习质量、收敛速度与安全保障**三方面仍有局限。本文提出带**动态安全引导**的安全增强 DRL 方法（摘要中称 **DSG-DRL**，正文与表格中称 **PSE-DRL**，见文末 ⚠），用于**换道运动规划**，三个特征：① 通过额外纳入**潜在不安全行为**学到更安全的策略；② 通过让**危险驾驶经验"令人印象深刻"**加速安全策略学习；③ 通过**避免意外鲁莽动作**进一步提升安全性。核心机制：用**预期风险（anticipated risk）** 评价预测轨迹，使智能体不仅从碰撞瞬间的经验学习，也从"正在驶向碰撞的危险动作"学习；危险经验用**额外记忆批次 + 采样优先级**强化；并用**训练与测试中的动态约束**阻止鲁莽动作。具体实现为 **PSE-DRL**（trajectory-parameterized actions + 轨迹级预测安全增强模块）：以高斯不确定势场 U(t) 构造预期风险 J（式 7–8），按风险把 transition 分入安全批次 Ds、碰撞批次 Dc、预期风险批次 Dar 并优先采样（式 14–15），用随 episode 递减的动态阈值 Jthres(k) 判定"犯错"并生成安全修正动作 a*（式 9–10）。**摘要只写"Simulation validation shows…"**——即所有结论均来自仿真，无实车。作者报告：PSE-DRL 学习更快、收敛更好，在保持驾驶效率的同时取得高安全性能。成立条件：三车道单向高速公路、Highway-env 仿真、IDM/MOBIL 周边车、交通密度 0.3–0.5。

## 3. 结论（≤350 字中文：作者结论节要点 + 关键数字 + 作者自承的局限）

结论节（§VI）要点：PSE-DRL 通过预期风险评价识别潜在不安全行为，使智能体不仅从碰撞事件学习，也从碰撞之前的高风险动作学习；危险驾驶经验通过额外记忆批次与采样优先级被强化，加速向更安全策略收敛；动态风险约束与安全动作修正可在**训练与测试**两阶段阻止意外鲁莽动作。仿真结果表明 PSE-DRL 学习性能更优、收敛更快；在不同交通密度测试下，训练后的 PSE-DRL 及其带在线安全约束的版本 **PSE-DRL(on)** 保持更低的预期风险与更大的 TTC，仅轻微牺牲驾驶效率。

**关键数字（全部取自正文行文，表格表体缺失）**：训练全程，PSE-DRL 相对 baseline 与 SSE-DRL 的 TR 提升 **51.13% / 28.34%**，EL 提升 **49.94% / 26.39%**，CR 降低 **61.75% / 31.49%**；收敛期（最后 200 episode）TR、EL、CR 分别优于 baseline 约 **32.75% / 27.65% / 92.31%**，优于 SSE-DRL 约 **14.52% / 18.02% / 60.16%**；达到 baseline 收敛水平仅需 **31% / 30% / 28%** 的总 episode 数。测试期平均 CR 由 baseline **5.14%**、SSE-DRL **1.16%** 降到 **0.29%**（相对降低 **94.75% / 76.9%**），PSE-DRL(on) 进一步降到 **0.06%**；平均/最小 TTC 分别较 baseline 与 SSE-DRL 提升 **14.02%/55.31%** 与 **7.85%/22.02%**；平均速度仅下降 **1.60% / 2.97% / 3.63%**。消融：完整模型训练期 **TR = 72.28、CR = 0.27%**，测试期 **TR = 86.71、CR = 0.07%**；去掉 REE 后 CR 收敛至 **1.80%**、约需 **1000** episode（增加约 **75%** 训练量）；去掉 DRC 后训练期 **TR = 67.26**、测试期 CR 仍为 **0.08%** 但平均速度降 **10%**。

**作者自承的局限**：① 仅仿真验证（Highway-env），无实车；② 轨迹参数化表达力有限，未来需更灵活的参数化；③ 参考了作者团队此前工作（风险经验与模糊权重来自 [33]，baseline 为团队自研 [37]）；④ 在线安全约束产出的数据可留作后续在线更新，属未来工作。

## 4. 方法一句话（≤60 字）

自车与 8 辆周边车的 Frenét 位姿（含高斯噪声）→ D3QN + 轨迹参数动作 + 预测安全引导模块（预期风险 J、风险经验批次优先采样、动态阈值与安全动作修正）→ 换道/超车轨迹（跟踪控制器执行 15 步）。

## 5. 图表清单（占位符）

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-SEDRL-1} | Fig. 1 | "The safety-enhanced DRL approach via predictive safety guidance module for autonomous driving." | 全方法框架图：EV 由当前动作 a_t 生成未来轨迹 Tr(e)，SVs 预测 Tr(s)，据二者评估预期风险并给出安全引导。要点：这是"轨迹级"而非"状态级"安全约束的图示——与只做当前状态约束的方法的区别所在 |
| {FIG-SEDRL-2} | Fig. 2 | "State space definition. The green vehicle is EV, and the blue vehicles are SVs." | 状态定义图（绿=EV，蓝=SVs）；要点：周边车集合 = 当前车道前/后车 + 左/右车道最近车与前/后车，共 **8 辆**（j = 1~8）——P1 编队场景可对齐的车道级状态定义模板 |
| {FIG-SEDRL-3} | Fig. 3 | "Vehicle kinematic model in the Fren´et Coordinates. C is the mass center point and Psl is the root point on the reference path. Lf and Lr are the distances to C from the front and rear axles respectively." | Frenét 坐标下的车辆运动学模型（式 6 的图示）；要点：给出曲率约束的几何含义，是轨迹生成可行性判据的来源 |
| {FIG-SEDRL-4} | Fig. 4 | "Dynamic uncertainty risk of predicted trajectory for SV." | 正文写"…calculated from the Mamdani fuzzy system (more detail in our previous work [33]), which can be shown in Fig. 4"——即该图应展示**模糊系统给出的置信权重**；⚠ 图注却写作"Dynamic uncertainty risk…"，与 Fig. 5 图注**逐字相同**（见文末 ⚠） |
| {FIG-SEDRL-5} | Fig. 5 | "Dynamic uncertainty risk of predicted trajectory for SV." | 正文写"The schematic figure of the dynamic uncertainty risk is shown in Fig. 5. It can be seen that the uncertainty risk of SV increases gradually in short predicted horizon and then decreases over time."要点：**短时域内风险上升、随后下降**——这是 A(t) = A0·cos(0.9·π/2·t/tp) 时间衰减设计的图证据 |
| {FIG-SEDRL-6} | Fig. 6 | "The overall training framework of the proposed PSE-DRL planner." | 完整训练框架：状态 → 策略网络输出决策动作 → 生成 Tr(e) → 15 个时间步更新环境 → 动态安全引导模块评估风险并按风险与场景相似度分批次存储。要点：本图是"风险经验记忆（Dar）"与"安全修正 a*"的流程依据 |
| {FIG-SEDRL-7} | Fig. 7 | "Training performance curves for each planner model in highway task." | 各规划模型训练性能曲线（EMA 平滑因子 **0.9**）；要点：PSE-DRL 训练速度最快、收敛最好——但曲线经 EMA 平滑，**瞬时波动被掩盖** |
| {FIG-SEDRL-8} | Fig. 8 | "TR of different planner models in multi-group testing." | 多组测试下的 TR；要点：PSE-DRL 测试 TR 更高更稳；具体数值需读 TABLE II（表体缺失） |
| {FIG-SEDRL-9} | Fig. 9 | "Statistical results for maneuver safety in different traffic density tests." | 不同交通密度下的安全性统计（EL、TTC、CR、DAR）；要点：这是"结果不随密度崩坏"的证据图，具体数值需读 TABLE III（表体缺失） |
| {FIG-SEDRL-10} | Fig. 10 | "Statistical results for maneuver efficiency in different traffic density condition tests." | 不同交通密度下的效率统计（AS、每 episode 步的超车数）；要点：用于证明"安全提升没有以过度保守为代价"，具体数值需读 TABLE IV（表体缺失） |
| {FIG-SEDRL-11} | Fig. 11 | "Case studies comparing diﬀerent DRL models in representative scenarios. Red and blue markers denote the driving trajectories of EV and SVs, respectively." | 两个案例：(a) 超车场景、(b) cut-in 场景；红=EV、蓝=SVs 轨迹。要点：baseline 激进（安全裕度不足、换道中止）、SSE-DRL 过度保守（放弃可行超车）、PSE-DRL 兼顾——**这是全文唯一的定性行为对比证据** |
| {FIG-SEDRL-12} | Fig. 12 | "Bin-averaged learning curve of PSE-DRL without diﬀerent modules in training by the PSE-DRL (green curve), w/o REE (red curve) and w/o DRC (blue curve)." | 消融训练曲线（bin 平均）；绿=完整、红=w/o REE、蓝=w/o DRC。要点：w/o REE 收敛慢且 CR 停在 1.80%；w/o DRC 早期奖励更高但波动更大、收敛水平更低（TR=67.26） |
| {FIG-SEDRL-13} | Fig. 13 | "Test of PSE-DRL without diﬀerent modules by the PSE-DRL (green bar), w/o REE (red bar) and w/o DRC (blue bar)." | 消融测试柱状图；要点：w/o REE 的 CR 由 0.07% 升到 0.32%（**相对增加 357.14%**）；w/o DRC 的安全性基本保留但平均速度降 **10%** |
| {TAB-SEDRL-1} | TABLE I | "LEARNING PERFORMANCE OF DIFFERENT PLANNER MODEL IN TRAINING" | 训练期学习性能（TR、EL、CR；全 episode 平均与最后 200 episode 两口径）。**表体未随全文文本提取**（见 §7 第 1 条） |
| {TAB-SEDRL-2} | TABLE II | "AVERAGE TOTAL REWARD OF DIFFERENT PLANNER MODEL IN TESTING WITH DIFFERENT TRAFFIC DENSITY" | 不同交通密度下的测试平均 TR。表体缺失 |
| {TAB-SEDRL-3} | TABLE III | "STATISTICAL MANEUVER SAFETY RESULTS OF DIFFERENT PLANNER MODELS IN TESTING WITH DIFFERENT TRAFFIC DENSITY" | 不同密度下的安全性统计（EL、CR、TTC、DAR）。表体缺失——**正文引用的 TTC/CR 数字只能从行文取** |
| {TAB-SEDRL-4} | TABLE IV | "STATISTICAL MANEUVER EFFICIENCY RESULTS OF DIFFERENT PLANNING MODEL DURING TESTS WITH DIFFERENT TRAFFIC DENSITY" | 不同密度下的效率统计（AS、超车数）。表体缺失 |
| {TAB-SEDRL-5} | TABLE V | "STATISTICAL AVERAGE RESULTS OF PSE-DRL WITHOUT DIFFERENT MODULES DURING TRAINING" | 消融的训练期统计（正文摘数：完整模型 TR=72.28、CR=0.27%）。表体缺失 |
| {TAB-SEDRL-6} | TABLE VI | "STATISTICAL AVERAGE RESULTS OF PSE-DRL WITHOUT DIFFERENT MODULES IN TESTING" | 消融的测试期统计（正文摘数：完整模型 TR=86.71、CR=0.07%）。表体缺失 |
| {ALG-SEDRL-1} | Algorithm 1 | "The Safety-Enhanced Deep Reinforcement Learning With Dynamic Safety Guidance"（算法标题逐字） | 双层循环（episode k = 1~KN，步 t = 1~Te）：采样动作 → 生成 Tr(e)/Tr(s) → 评估 J → **while J > Jthres 循环**：写入 Dar 并生成安全修正 a*；按 |D| 与 ND 选择存储概率；按是否碰撞写入 Dc 或 Ds；每 tr 步采样三种批次、算 IS 权重、更新网络与目标网络。要点：**"犯错—修正—记录"三步在算法里是显式的 while 循环**，这是本文与普通安全约束方法的可核验差异 |

## 6. 对 P1 的用处

- **与 P1 的关系**：**相邻问题**（本组三篇中 ODD 最接近 P1 的一篇）。它同样在**三车道单向高速公路 + 人工驾驶周边车（IDM/MOBIL）混行**的设定下做闭环决策，但：① 任务是**换道/超车决策**（离散轨迹参数动作 + D3QN 值方法），不是 P1 的纵横向编队跟车控制；② 输出是"目标车道偏移 + 目标纵向距离/速度变化"的离散组合，不是连续控制量；③ 没有 OTF 势场、没有连续时间网络、没有编队概念。它**不回答** P1 的 RQ，但在**场景库、安全评价指标、消融范式**三处对 P1 有直接可用的素材。
- **可迁移**：
  1. **ODD 与交通流设置**（三车道单向高速；SVs = 当前车道前/后车 + 左右车道最近车与前/后车共 8 辆；IDM 参数 v ∈ [10,15] m/s、d_tar ∈ [2,4] m、T_tar ∈ [1,2] s；MOBIL 换道判据阈值 0.2（式 17，原文未印单位）；训练交通密度 0.3–0.5 随机、测试在多个密度下各 6 次）→ **P1 的混行交通流参数与"逐密度报告"协议可直接参照**（P1 用 CARLA Town04，需做一次映射并说明差异）。
  2. **安全增强三件套**可作为 P1"小心修正"层与安全监督层的候选设计：(a) **预期风险 J** —— 高斯不确定势场 U(t)（式 7）+ 时间衰减幅值 A(t) = A0·cos(0.9π/2·t/tp)，把"不确定性随预测时域增长"与"长时域风险不该过度压制"同时编码；(b) **风险经验回放** —— 分 Ds/Dc/Dar 三批次，按风险值 J 与场景相似度 F_S 定优先级 p_t，用重要性采样权重 It 校正偏差（式 14–15）；(c) **动态风险阈值** Jthres(k) 随 episode 从 Jmax 分段降到 Jmin，超出则拦截动作并生成满足风险约束的最小偏离安全动作 a*（式 9–10）。
  3. **消融范式**：w/o REE、w/o DRC 两个**单因素**消融 + 训练表与测试表分开报——与 P1 §4"消融一次只改一个因素，并报告失败设定与放弃的路线"完全同构，可直接借骨架。
  4. **指标补充**：本文的 CR（碰撞率）、EL（碰撞前行驶时长）、TTC（平均/最小）、DAR（决策预期风险）中，**TTC 与 CR 可作为 P1 高速场景的安全类补充指标**——P1 现有七项指标偏控制性能，缺安全类指标，这是本文最实的一块可迁移内容。
  5. **报告完整性模板**：本文把 episode length、训练/测试 episode 数、学习率、γ、**分批 batch size**、**回放采样权重**逐项写出（§V-A），P1 报告复现配置时应对齐到这一粒度。
  6. **诚实的失败设定**：w/o DRC "早期奖励更高但波动更大、收敛到更低水平"这一点被如实报告，是"报告失败设定"的现成范例。
- **不可迁移 / 陷阱**：
  1. **动作空间与范式不同**：离散轨迹参数（l_tar ∈ {−3.5, 0, 3.5} m；s_tar 五等分离散、步长 1 m；Δv_tar ∈ {−2,−1,0,1,2} m/s）+ D3QN。P1 走连续控制（TD3 / CfC），**不能**把本文的动作设计或其超参直接搬到 P1。
  2. **纯仿真、无实车**：全文（含摘要）只有 "Simulation validation"；平台是 `highway-env`（GitHub 开源环境），不是 CARLA，也不是实车。→ 任何引用都必须写成"在 Highway-env 仿真中"。
  3. **统计强度弱**：**3 次训练运行**、测试重复 6 次、**未报随机种子、无 CI、无显著性检验**；正文只给百分比变化。→ 本文的数字**不能**作为 P1 的对标基线值（P1 §4 要求种子 ≥5 + CI）。
  4. **六张表的表体在可得全文中缺失**（§7 第 1 条）：所有逐项数值（其实只有正文行文可引），无法核验 TR/CR/TTC 的完整分布。
  5. **对照公平性需注意**：baseline [37] 与 risk 相关组件 [33] 均为**作者团队自研**，SSE-DRL [19] 亦为第三方但无公开实现说明；未见代码/数据可用性声明。P1 §3 要求"同等调参预算"，本文无法核验。
  6. **测试期也启用安全约束**：PSE-DRL(on) 在测试时施加在线约束，与"纯策略性能"口径不同；引用任何 CR 数字必须写清是 PSE-DRL 还是 PSE-DRL(on)。
  7. **EMA 平滑（因子 0.9）**：训练曲线经指数滑动平均，图的"最快收敛"是平滑后的结论；评估学习速度时应以文中的 episode 数口径（31%/30%/28%）为准。
- **引用时必须带的限定语**：**"在 Highway-env 三车道单向高速公路、IDM/MOBIL 人工驾驶周边车、交通密度 0.3–0.5 的纯仿真设定下（每模型 3 次训练、多密度 6 次测试、无种子与显著性检验），作者报告 PSE-DRL 将平均碰撞率由基线 5.14%、SSE-DRL 1.16% 降至 0.29%，平均速度仅下降 1.60%–3.63%；该结论出自离散轨迹参数 + D3QN 的换道决策任务，与 P1 的连续编队控制协议不同，属文献报告值，不可直接比较。"**

## 7. 缺失信息（≥3 条，写成可执行动作）

1. **需回原始 PDF 取回 TABLE I–VI 的表体数值**（可得全文中六张表**只有表题、无表体**：可核对 `TABLE I` 后紧接正文 "Moreover, the TTC between EV and the SV…"）。至少需要：TR/EL/CR 的逐项均值与离散度、多密度下的 AS/超车数、消融的完整指标。（后果：本卡片 §8 的数字全部来自正文行文，**无法核验任何逐项统计量**，也无法知道是否给了标准差。）
2. **需向作者索取随机种子与重复次数明细**：文中只写 "All models are trained 3 runs" 与 "test them in different traffic density condition 6 times"，**未报种子、未报每次运行的数值、无 CI、无显著性检验**。（后果：正文的 +51.13%、CR 0.29% 等百分比无法判断是否超出运行间波动；P1 §4 的 CI 要求无法从本文满足。）
3. **需澄清方法命名**：摘要/引言称 **DSG-DRL**（dynamic safety guidance），正文与图表称 **PSE-DRL**（predictive safety enhancement DRL），另有 **SSE-DRL**（对照）与 **PSE-DRL(on)**。（后果：检索与引用时极易混名，P1 引用必须二选一并注明对应关系。）
4. **需澄清未定义缩写与公式交叉引用**：正文出现未定义缩写 **CT**（"PSE-DRL significantly decreases the average CT"，全文仅此一处）、**AV**（后文与已定义的 AS 并用）、**VOel**（前文定义为 OVes）；公式编号交叉引用亦漂移（"Also, **(10)** is normalized…"实指式 (8)；"the decision anticipated risk (DAR) in **(10)**"实指式 (8)；Algorithm 1 中 "a* = **(11)**"实指式 (10)、"P(t) in **(15)**"实指式 (14)、"IS weight It = **(16)**"实指正文 IS 权重定义；"as shown in **(18) and (19)**"对应展示的式 (16)(17)）。（后果：P1 若转述本文公式必须回 PDF 逐一核对编号，不得照抄文本编号。）
5. **需澄清 IDM/MOBIL 的参数来源与引文**：正文写 "the control model of SVs is MOBIL/IDM [31]"，而 [31] 是 Z. Gu et al., T-ITS 24(9) 2023 的一篇安全增强 RL 论文，非 IDM/MOBIL 原始文献（Treiber 等）。（后果：P1 复刻混行交通流时需另找 IDM/MOBIL 原始参数，不能引本文。）
6. **需确认代码、数据与 highway-env 版本**：全文只引 `highway-env` 仓库 [36]（E. Leurent, 2018），未给版本号、未声明作者代码或数据是否公开。（后果：P1 §3 要求的"同一地图版本 + 同一组交通流随机种子"无法从本文获得，且无法复现其交通密度设定。）
7. **需澄清消融的统计口径**：Table V/VI 的"统计平均结果"未在正文说明统计量（均值？均值 ± SD？中位数？），也未说明 w/o REE 的 CR=1.80%、1.80%→0.32% 等数字的样本量。（后果：357.14% 这类相对增幅在极小分母（0.07%）下极其敏感，P1 引用需注明分母。）
8. **需明确 PSE-DRL 与 PSE-DRL(on) 的测试协议差异**：正文写 "test them … without any safety guidance and anticipated risk memory enhancement module"，随后又说 PSE-DRL(on) 用在线安全约束，二者在测试期的启用项需逐项列表。（后果：CR 0.29% 与 0.06% 属不同测试配置，混用即失实。）

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

> **重要限制**：本文六张表（TABLE I–VI）的表体未随全文文本提取，**下表数字全部取自正文行文**；凡需从表中读取的逐项统计量一律记"表体缺失"。

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 训练全程 TR 提升（vs baseline / SSE-DRL） | **+51.13% / +28.34%** | 未报告（无种子、无 CI） | §V-D-1；TABLE I（表体缺失） |
| 训练全程 EL 提升（vs baseline / SSE-DRL） | **+49.94% / +26.39%** | 未报告 | §V-D-1 |
| 训练全程 CR 降低（vs baseline / SSE-DRL） | **−61.75% / −31.49%** | 未报告 | §V-D-1 |
| 收敛性能（最后 200 episode）优于 baseline | TR **≈+32.75%**、EL **≈+27.65%**、CR **≈+92.31%** | 未报告 | §V-D-1 |
| 收敛性能（最后 200 episode）优于 SSE-DRL | TR **≈+14.52%**、EL **≈+18.02%**、CR **≈+60.16%** | 未报告 | §V-D-1 |
| 学习速度（达到 baseline 最后 200 episode 水平所需 episode 占比） | TR **31%**、EL **30%**、CR **28%** | 未报告 | §V-D-1 |
| 测试期 EL 提升（vs baseline / SSE-DRL，跨密度平均） | **+26.84% / +6.11%** | 未报告 | §V-D-2 |
| 测试期平均碰撞率 CR | baseline **5.14%**、SSE-DRL **1.16%** → PSE-DRL **0.29%**（相对降低 **94.75% / 76.9%**） | 未报告（Table III 表体缺失） | §V-D-2；TABLE III |
| 测试期 CR（在线约束版） | PSE-DRL(on) **0.06%**（0.3 交通密度下几乎无碰撞） | 未报告 | §V-D-2 |
| 测试期 TTC（平均 / 最小）提升 | vs baseline **14.02% / 55.31%**；vs SSE-DRL **7.85% / 22.02%** | 未报告 | §V-D-2 |
| 测试期平均速度 AS 变化（PSE-DRL vs baseline，三档密度） | **−1.60% / −2.97% / −3.63%** | 未报告 | §V-D-3；TABLE IV |
| 测试期超车数变化（PSE-DRL vs baseline，三档密度；原文此处写作 **VOel**，前文定义为 OVes） | **−3.38% / −8.88% / −8.23%** | 未报告 | §V-D-3 |
| 测试期 AS 变化（SSE-DRL vs baseline） | **−5.64% / −6.69% / −9.12%** | 未报告 | §V-D-3 |
| 测试期超车数变化（SSE-DRL vs baseline） | **−28.52% / −25.89% / −44.02%** | 未报告 | §V-D-3 |
| 消融（训练，最后 200 episode） | 完整 PSE-DRL：**TR = 72.28、CR = 0.27%**；w/o REE：CR 收敛至 **1.80%**、约需 **1000** episode（**+75%** 训练量）；w/o DRC：**TR = 67.26、CR = 0.27%**（早期奖励更高、波动更大、收敛水平更低） | 未报告 | §V-E；TABLE V；Fig. 12 |
| 消融（测试） | 完整 PSE-DRL：**TR = 86.71、CR = 0.07%**；w/o DRC：**CR = 0.08%**，平均速度（AV）比完整模型低 **10%**；w/o REE：**CR 0.07% → 0.32%**（相对 **+357.14%**），TR 显著下降 | 未报告 | §V-E；TABLE VI；Fig. 13 |
| Episode 长度 Te | **100** | — | §V-A |
| Episode 数 | 训练 **1500**；测试 **100** | — | §V-A |
| 学习率 σ | **1e-4** | — | §V-A |
| 折扣因子 γ | **0.9** | — | §V-A |
| Batch size（安全/碰撞/风险三批次） | **[N_Ds, N_Dc, N_Dar] = [20, 4, 8]** | — | §V-A |
| 回放采样权重 | **[w_Ds, w_Dc, w_Dar] = [10, 3, 3]** | — | §V-A |
| 训练/测试交通密度 | 训练随机 **0.3–0.5**；测试在多个不同密度（正文未逐一列举）各 **6** 次 | — | §V-B |
| 训练运行次数 | 每模型 **3** 次 | 未报告（无种子） | §V-B |
| 动作空间 | 横向 l_tar ∈ {**−3.5, 0, 3.5**} m（车道宽 3.5 m）；纵向 s_tar 五等分离散、步长 **Δs = 1** m；Δv_tar ∈ {**−2, −1, 0, 1, 2**} m/s | — | §V-A |
| 周边车（SV）数量 | **8** 辆（j = 1~8）：当前车道前/后 + 左/右车道最近、前、后 | — | §III-A；Fig. 2 |
| SV 交通流参数 | 速度 v_s^j ∈ [**10, 15**]；目标间距 d_tar^j ∈ [**2, 4**]；目标时距 T_tar^j ∈ [**1, 2**]；MOBIL 换道判据阈值 **0.2** | — | §V-A 式 (16)(17) |
| 策略网络 | **D3QN**（dueling double DQN）[35] | — | §IV-D |
| 规划执行粒度 | 决策动作生成的轨迹由跟踪控制器在 **15** 个时间步内执行以更新环境状态 | — | §IV-D；Fig. 6 |
| 曲线平滑 | 训练曲线用 EMA，平滑因子 **0.9** | — | §V-D-1 |
| 仿真平台 | **highway-env**（开源）[36]，三车道单向高速公路 | — | §V-A |
| 对照模型 | baseline [37]（作者团队前作，ITSC 2023）、SSE-DRL [19]、PSE-DRL、PSE-DRL(on) | — | §V-B |
| 风险函数构成 | J = (α1·n_risk/tp + α2·U_max + α3·t_Umax)(α1 + α2·A0 + α3·tp)；U 为高斯不确定势场，幅值 A(t) = A0·cos(0.9·π/2·t/tp)；U(t) > U_thres 记为高风险点 | 权重 αi 数值**未给** | §IV-C 式 (7)(8) |
| 动态风险阈值 | Jthres(k)：k < K0 时 = J_max；(K0, Km) 区间线性降到 J_min；k > Km 时 = J_min | **K0、Km、J_max、J_min 数值均未给** | §IV-C 式 (9) |
| 奖励构成 | R_eff = (v(e) − v_min)/(v_max − v_min)；R_s = −1（碰撞）或 −0.5(α·f_d + (1−α)·f_J)；R_con = ½|a_t − a_{t−1}|² | v_min/v_max、α 数值**未给** | §IV-C 式 (11)(12)(13) |

### ⚠内部不一致

- `⚠内部不一致（命名）：` **摘要与引言把方法命名为 DSG-DRL（dynamic safety guidance），而第 III–V 节、六张表与全部结果都写作 PSE-DRL（"a DRL model with trajectory-parameterized actions with a predictive safety enhancement module embedded at the trajectory level, termed PSE-DRL"）**。同一篇论文两套方法名，且 "DSG" 与 "PSE" 的首字母展开不同。
- `⚠内部不一致（图注重复）：` **Fig. 4 与 Fig. 5 的图注逐字相同**——均为 "Dynamic uncertainty risk of predicted trajectory for SV."，但正文对 Fig. 4 的引用是"…calculated from the Mamdani fuzzy system (more detail in our previous work [33]), which can be shown in Fig. 4"（应为模糊置信权重图），对 Fig. 5 的引用才是动态不确定性风险示意。两图之一（很可能是 Fig. 4）的图注有误。
- `⚠内部不一致（公式交叉引用漂移）：` 正文 "Also, **(10)** is normalized through predicted duration tp and initial risk amplitude A0" 与 "the decision anticipated risk (DAR) in **(10)**" 描述的都是式 **(8)**；Algorithm 1 中 "a* = **(11)**" 对应式 **(10)**、"Store Tar(t) in Dar with P(t) in **(15)**" 对应式 **(14)**、"Compute IS weight It = **(16)**" 对应正文 IS 权重定义；§V-A "as shown in **(18) and (19)**" 对应实际展示的式 **(16)(17)**。
- `⚠内部不一致（缩写漂移）：` 效率指标前文定义为 "the number of overtaken vehicles per episode step (**OVes**)"，后文写成 "**VOel** is reduced by 3.38%, 8.88%, 8.23%"；平均速度前文定义为 "average speed (**AS**)"，消融节写成 "**AV**"（"a 10% decrease AV compared to PSE-DRL"）；**"CT"**（"PSE-DRL significantly decreases the average **CT**"）全文仅此一处、从未定义。
- `⚠内部不一致（小节编号）：` §V-D 的效果指标列为 "i) learning performance; **ii)** maneuver safety; **ii)** maneuver efficiency"——第二个 "ii)" 应为 "iii)"。
