# 物理增强 DeePC 的混行生态驾驶｜Physics-Augmented Data-EnablEd Predictive Control for Eco-driving of Mixed Traffic Considering Diverse Human Behaviors

- **出处**：IEEE Transactions on Control Systems Technology, 32(4): 1479–1486, 2024（Crossref `published-print` = 2024-07）｜ **类型**：期刊论文（本地材料 8 页）
- **作者**：Dongjun Li, Kaixiang Zhang, Haoxuan Dong, et al.（n=6；完整署名：Dongjun Li, Kaixiang Zhang, Haoxuan Dong, Qun Wang, Zhaojian Li, Ziyou Song）
- **DOI**：10.1109/TCST.2024.3361393（Crossref `works/10.1109/TCST.2024.3361393` 返回 http 200，字段 `DOI` 为小写 `10.1109/tcst.2024.3361393`；DOI 大小写不敏感。取用日期 2026-10-05，通道 Crossref REST）
- **全文来源**：`literature/fulltext/fresh2024/tcst2024-physaug-deeplcc__20c1e0c6.txt`（**PAGES=8, CHARS=46,142**，口径：Node `readFileSync(path,'utf8').length`，与本项目 `fulltext/fetch-log.md` 同口径；去掉 3 行页眉与 8 个 `===== PAGE n =====` 标记后 45,907）｜
  **材料版本**：**作者版（arXiv 预印本 v2），非 IEEE VoR**。逐字证据：① 第 111 行 `arXiv:2306.01387v2 [eess.SY] 2 Feb 2024`；② 第 63–64 行 `Color versions of one or more figures in this article are available at https://xxxx` 与 `Digital Object Identifier xxx`（占位符未填）；③ 第 51 行 `Recommended by xxx.`（占位符未填）；④ 正文题名印为 "Eco-**d**riving"，而 Crossref 正式版题名为 "Eco-**D**riving"（首字母大小写不同）。
  ⚠ **内部不一致（本卡第 1 处）**：第 50–51 行印为 `Manuscript received 24 April 2024; accepted 30 Jan 2023`——**录用日期早于投稿日期一年**，作者版排版错误，与 Crossref（created 2024-02-09、printed 2024-07）不相容。
  ⚠ **与任务给定不符**：任务写 CHARS=44,798，本卡实测 46,142（Node 口径），差 1,344 字符；去页标记后亦为 45,907。差值来源未查明，**以实测为准并留痕**。
- **分组**：2024+ 增量
- **证据等级初判**：**C 级** — 全部结果为纯 MATLAB 仿真，**无随机种子、无重复次数、无置信区间、无显著性检验**，物理注入的对照只在"一个算例"（`in one case`）上做，且无实车/台架/硬件验证。
- **档位建议**：**A（临界，机械达标；敏感性见下）** — 加权恰为 14 且 D1=2、D5≥1，按母协议 §5 判定式达标；但 14 全部靠 D1=2 撑起：若把"单车道、无横向、控制器为 QP 而非神经网络"读作**非同 ODD**而将 D1 降为 1，则加权 = 11，落 **B 档**。**该口径敏感性请组会裁定，本卡不自行降级。**
- **五维打分（各维 0–2，满分 20）**：D1=**2** D2=**1** D3=**1** D4=**2** D5=**1** → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = **14**
  ⚠ 必须 0–2 制；D4 一律指**时效性**（2024 年 → ≤5 年 → 2）。
  - **D1=2 的依据（写明，避免自我拔高）**：论文把"物理残差如何注入数据驱动控制器"给成了一个三选一的设计空间（等式约束 / 不等式约束 / 罚项，§II-C），这正是 P1"把 OTF 势场作为结构条件注入连续时间控制器"这一核心设计问题的**可对标设计空间**；其 576 场景驾驶员异质性扫描协议亦可被 P1 的 A1 消融直接复用。ODD 差异（单车道纯纵向）不改变方法层可对标性——沿用母协议 §8.1"方法或架构层可迁移者按 D1 正常计分"。
  - **D2=1**：有对照（2 个基线 + 物理开/关 + 576 场景）与多场景滚动时域闭环仿真，但**无统计检验、无种子、无实车** → 按 D2 二分档的"有统计"缺项取 1。
  - **D3=1**：协议与全部参数逐值印出（IDM 参数、N/Tini、权重、约束边界、场景构造），数据可用公开 NGSIM；但**论文未给代码、未给数据、未给补充材料** → 部分迁移。
  - **D4=2**：2024 年。
  - **D5=1**：有全文 + 效应量（Table II 逐车与合计能量、预测误差上界），但**无可复现材料**，且 IEEE VoR 未取得（本地为作者版，按 `00-scope.md` §2.2 保守取 1）。

---

## 1. 标题

**原文题名（逐字，按本地作者版正文首页）**：
`Physics-Augmented Data-EnablEd Predictive Control for Eco-driving of Mixed Traffic Considering Diverse Human Behaviors`

**正式版题名（Crossref 字段 `title`，逐字）**：
`Physics-Augmented Data-EnablEd Predictive Control for Eco-Driving of Mixed Traffic Considering Diverse Human Behaviors`
（差别仅在 `Eco-driving` / `Eco-Driving`。**入稿引用以正式版为准。**）

**Index Terms（逐字，第 36–37 行）**：`Connected and automated vehicles, data-driven control, eco-driving, diverse driving behaviors.`

---

## 2. 摘要（≤400 字）

论文提出物理增强数据驱动预测控制（PA-DeePC），处理人工与自动混行交通流的生态驾驶。其"物理"是一阶输入–输出关系定义的**残差** ε_k，可按三选一注入 DeePC：等式约束（物理准确时）、不等式约束（不准确时）或软罚项（仿真取 M=500）。人驾异质性用 NGSIM 实车轨迹标定的 IDM 表征，只放开期望车头时距 T_gap 一个参数；在 [0.5, 2.9] s 内分 12 组、每组随机取 2 名驾驶员，全组合得 576 个场景。第二个贡献是去掉参考轨迹跟踪项的优化框架：直接最小化凸化功率模型，用松/紧两套间距约束（CTH 安全界、TG 效率界）替代参考轨迹。MATLAB R2022b 仿真显示：预测误差由原版 DeePC 的 ≤0.06 降至 ≤0.01；能量消耗相对 Original DeePC 降 4.14%、相对两组 OVM 巡航控制降 9.29% 与 4.97%；CAV1 最临界点 TTC>7.47 s。

---

## 3. 结论（≤350 字）

作者自述（§VI）：并入部分物理后 DeePC 表征动力学能力 "significantly improved"；新框架平均降低全体车辆能耗 4.14%，相对两组参数 OVM 巡航控制分别降 4.97% 与 9.29%。

**本卡判定**：① 4.14% 是单一确定性仿真设置下的 576 场景均值，无种子、无重复、无 CI、无检验，只能写"论文报告值"；② "physics 显著改进预测"只有单算例（Fig. 4b）≤0.06→≤0.01 支撑，"significantly" 属修辞非统计判断；③ 未报弦稳定性、计算时间、渗透率与碰撞计数——TTC>7.47 s、TG∈1.5–2.6 s 仅说明该次仿真约束未被逼近，不构成安全保证；④ 全文无实车（MATLAB R2022b 仿真），按 `AGENTS.md` §1 红线不得表述为实车验证。

---

## 4. 方法一句话（≤60 字）

把一阶运动学残差以罚项或约束注入 DeePC 滚动时域 QP，并用 NGSIM 标定的 IDM 车头时距表征驾驶员异质性。

---

## 5. 图表清单（占位符）

> 全文共 **8 个**图表条目（Figure 1–6、Table I–II），未超 12，**全部覆盖**。

| 占位符 | 图/表号 | 原文图注（逐字，可截断 100 字符） | 读图要点 |
|---|---|---|---|
| `FIG-1` | Fig. 1 | `Schematic of the mixed traffic flows. The preceding vehicle is indexed as 0.…` | 定义拓扑：头车（PV）索引 0，其后 n 辆含 m 辆 CAV 与 n−m 辆"动力学不确定"的 HDV。**这是 P1 唯一可借用的编队拓扑画法** |
| `FIG-2` | Fig. 2(a)(b) | `Absolute and relative error of the estimated power under different acceleration (i.e.…` | 功率模型降阶带来的精度损失；正文给数值"maximum power error is 0.42 kW"，图内数值不可估读 |
| `FIG-3` | Fig. 3 | `Distribution of desired time headway Tgap.` | 驾驶员异质性的**唯一维度** T_gap 的经验分布（横轴 0–5 s，纵轴为计数）。**只给分布图，未给拟合分布与参数**，故不可复现抽样 |
| `FIG-4` | Fig. 4(a)(b) | `Prediction error during of update and online implementation. The errors are computed via ev = …` | 图例含 `Original DeePC` / `PA-DeePC-Cost` / `PA-DeePC-Constraint`——**物理注入的开关与两种注入方式都在此比较**；但正文明确只在"one case"上做，且纵轴同时有 Velocity (m/s) 与 Spacing (m)，0.06/0.01 两个数字**未标注对应哪个量纲** |
| `FIG-5` | Fig. 5 | `Comparison of the energy consumption distribution between two different optimization frameworks und…` | 新/旧优化框架的能量分布直方图（横轴 kJ，纵轴 Counts），测量噪声已注入。**这是全文唯一的不确定度可视化**，但无分布检验 |
| `FIG-6` | Fig. 6 | `Traffic information of s, v, TTC = − si / ∆vi−1,i , TG = si/vi .` | 四联图（间距、速度、TTC、时距）逐车给出；安全/效率结论（TTC>7.47 s、TG 1.5–2.6 s）来自此图 |
| `TAB-I` | TABLE I | `IDM PARAMETERS` | **可直接复用的 HDV 参数集**：a=4 m/s²、δ=4、s_gap=2 m、b=5 m/s²、v_d=25 m/s、T_gap=(0−5) s |
| `TAB-II` | TABLE II | `PLATOON ENERGY CONSUMPTION UNDER DIVERSE DRIVING CHARACTERISTICS` | 唯一的核心效应量表（逐车 + TOTAL，3 个基线列）；**已完整转录于 §8** |

---

## 6. 对 P1 的用处

### 与 P1 的关系：**相邻问题（方法层可迁移，ODD 层不可迁移）**

对象同为"人工与自动混行下的编队纵向控制"，但**控制器族**（滚动时域 QP / 非参数数据驱动 vs 连续时间神经网络）与 **ODD**（单车道纯纵向 vs 高速公路多车道）都不同。它不直接回答 P1 的 RQ，却直接给出：

1. **P1 必须对照的"物理先验注入设计空间"**——论文把注入方式显式写成三选一（等式约束 / 不等式约束 / 软罚项），并以 `PA-DeePC-Cost` 与 `PA-DeePC-Constraint` 两组对照落地。P1 的"OTF 势场作为结构条件"可以把这张表当作**设计空间的对照坐标**：先声明 OTF 属于哪一类（见下方陷阱②），再谈消融。
2. **可复用的混行异质性评价协议**——"一个异质性维度 + 分组抽样 + 全组合扫描"（T_gap 分 12 组各 2 名驾驶员 → 576 场景）。P1 的 A1 消融（OTF 开/关）可直接套用这一"同场景集、只改一个因素"的设计。
3. **一组可直接对齐的安全/效率约束口径**——CTH（th）与 TG 两套时距边界。

### 可迁移

- **HDV 异质性参数集与抽样设计**：Table I 的 IDM 六参数（逐值印出）+ "T_gap 为唯一异质性维度"的做法 + 12 组 × 2 名驾驶员的测试集构造 + 576 全组合。P1 若要构造"激进车流扰动"长尾场景，这是**逐值可直接实现**的协议。
- **物理残差的定义—注入—消融三步结构**：定义残差（式 8）→ 选择注入方式（三种）→ 开/关对照（Fig. 4b）。P1 写方法节时可照此结构组织"OTF 势场如何进入 CfC"的论证。
- **凸化功率模型的精度量化方式**：先给降阶近似，再用绝对/相对误差图与一个数值上界（0.42 kW）量化损失。P1 若把 OTF 势场做任何简化，应照此**给出简化带来的误差量化**，而不是只声称"近似合理"。
- **测量噪声注入声明**：`w ∈[−0.1, 0.1]` 注入实时间距与速度——一个廉价且必须的鲁棒性声明，P1 应显式做同类声明。

### 不可迁移 · 陷阱

1. **单车道、无横向动力学**——全文只有纵向跟驰链；P1 七项指标里的**车道居中偏差**与**前轮转角方差**在本文**零对应物**。不得把本文协议当作 P1 的完整基准。
2. **术语陷阱：本文的"physics"是运动学恒等式，不是动力学方程**。式(17) 的两条"物理"是 `v_{i,k+1} − v_{i,k} = a_{i,k}Δt`（欧拉积分）与 `s_{i,k+1} − s_{i,k} = (v_{i−1,k} − v_{i,k})Δt + ½(a_{i−1,k} − a_{i,k})(Δt)²`，且第二条在 `near equilibrium state (ai−1,k − ai,k ≈ 0) or the sampling time step ∆t is small enough` 时**直接丢掉二次项**。→ 本文之所以敢叫 "physics-augmented"，是因为它有一个**可判真伪的残差** ε_k（能算出来、能判是否为零）。**OTF 势场没有这样的残差**，这正是 `AGENTS.md` §1"P1 不宜自称 physics-informed"的同类证据，**P1 不能拿本文当"我们也可以叫 physics-informed"的先例**。
3. **基线命名与实现不一致（本卡第 2 处 ⚠ 内部不一致）**：§V-A 把基线①描述为 `implementing the PA-DeePC with a conventional optimization framework, where the weighting parameters for reference (∥yk −r∥2 Q) are the same as those in [24]`——即**仍带物理、只换成参考跟踪代价**；而 Table II 的列名是 `Original DeePC`（字面义为原版 DeePC、无物理）。二者不是同一件事。→ **Table II 的 4.14% 究竟度量的是"物理开/关"还是"优化框架替换"，无法从论文判定**；P1 引用时不得把它写成"加物理带来的提升"。
4. **`4.07%` 与 `4.14%` 并存（本卡第 3 处 ⚠）**：§V-B 正文写 `a notable reduction in energy consumption (4.07%) when compared to this baseline`（指旧优化框架），Abstract/§VI/Table II 写 `4.14%`（指 Original DeePC）。两个数字的自变量不同，**不可混用**。
5. **无统计**：574 个场景的数字都是确定性仿真平均值，**无种子、无 CI、无检验**；P1 的 A1 消融若只有单次结果，将与本项目 `AGENTS.md` §4（种子 ≥5、报 mean ± std 或 95% CI）直接冲突。
6. **"ACC"名不副实**：所谓 ACC 基线实为 `OVM-based adaptive cruising control (ACC) algorithm with two identical parameter sets`（α=0.8/β=0.5 与 α=0.5/β=0.8），**不是标准 ACC/CACC**，与 P1 的 PID/MPC/TD3 基线集也不重合。
7. **渗透率未报告**：论文印出 `a 5-vehicle platoon (S = {1, 3})`，Table II 与实际图的车辆标签只到 CAV1/HDV1/CAV2/HDV2 四辆跟随车 → **n=4、m=2**（**推断**，论文未印 n 与 m 的数值）；渗透率 2/4=50%（不含头车）或 2/5=40%（含头车）【计算值】。**与 DeeP-LCC 的 25% 口径不可直接并排**。

### 引用时必须带的限定语

```
citation_qualifier: single-lane pure-longitudinal platoon of 5 vehicles (1 preceding vehicle indexed 0 + 4 following vehicles inferred from Table II / Fig. 4 / Fig. 6 legends as CAV1, HDV1, CAV2, HDV2, i.e. m=2 CAVs at S={1,3}, n=4; the paper never prints n or m and never reports a CAV penetration rate - 50% excluding / 40% including the head vehicle by our own count), no lateral dynamics and no lane-change, simulation-only in MATLAB R2022b with NO vehicle, bench or hardware test, offline trajectory data are SIMULATION-GENERATED (T=1000 samples at dt=0.1 s = 100 s) while HDV behaviour is IDM calibrated on the real NGSIM field-test data with only the desired time headway T_gap released as the heterogeneity dimension (5 other IDM parameters fixed as constants; 12 headway groups x 2 sampled drivers = 24 drivers, all 24x24 = 576 combinations evaluated), performance numbers are deterministic simulation averages with NO seeds, NO repeats, NO confidence intervals and NO significance tests, the physics-on/off contrast is shown in ONE case only (Fig. 4b) and the 0.06 vs 0.01 prediction-error figures are not labelled with their unit (velocity m/s vs spacing m are plotted together), the baselines are a reference-tracking variant of the same PA-DeePC and a self-implemented OVM-based adaptive cruising controller (not standard ACC/CACC) with two parameter sets, the reported energy reductions are 4.14% vs 'Original DeePC', 9.29% and 4.97% vs the two OVM parameter sets (an additional body-text figure of 4.07% refers to a DIFFERENT baseline and must not be interchanged with 4.14%), no computation time, no solver, no MCU/embedded data, and NO string-stability result is reported.
```

### ★ 与 DeeP-LCC（`notes/p45-deeplcc-tcst2023.md`）的关系

**判断：以"补充"为主，三条原局限中只修正了半条；不是修正版，更不是替代版。**

本文**自己引用并定位 DeeP-LCC 为 [24]**，且逐字自述其缺口：`However, their research did not consider the diverse driving behaviors of human drivers or the optimization of energy consumption, which are vital aspects of CAV operation.` → 本文是 DeeP-LCC 的**同族续作**（同一 DeePC/基本引理骨架 + 同一混行编队对象），三条"补充"如下：

| 维度 | DeeP-LCC（TCST 2023） | 本文（TCST 2024） | 是补充/修正/照旧 |
|---|---|---|---|
| **HDV 行为** | OVM；Experiment B/C 用 Table I 六组异质参数（α、β、s_go） | IDM，**参数由 NGSIM 实车轨迹标定**；只放开 T_gap 一个异质性维度；576 场景全组合 | **补充**（异质性从"手设几组"升级为"真实数据标定 + 分布抽样"） |
| **物理/先验注入** | 无（纯非参数 Hankel 表征） | 有一阶运动学残差 ε_k，可作等式/不等式/罚项三种注入 | **补充**（这是本文的核心新意） |
| **目标函数** | J(y,u)=Σ(‖y‖²_Q+‖u‖²_R)，**跟踪预定义参考** | 去掉参考跟踪项，直接最小化凸化功率模型，用松/紧间距约束兜底 | **补充**（不同目标，不同基线口径） |
| **安全指标** | 无任何安全事件统计（仅约束式） | TTC 与 TG 被显式检查（TTC>7.47 s、TG∈1.5–2.6 s） | **补充**（但仍是单次仿真的极值，非分布） |
| **数据来源** | 仿真生成的 40 s 单轨迹（T=800 @0.05 s） | **仍是仿真生成**，但 T=1000 @0.1 s = 100 s【计算值】，且 IDM 参数与头车速度剖面取自 NGSIM | **半修正**（更长 + 真实数据驱动参数；但"预采集轨迹"仍**不是**实测混行轨迹） |
| **弦稳定性** | **无** | **仍无**（全文 `string stability` 仅出现 1 次，位于参考文献 [6] 的题名内） | **照旧未修正** |
| **显著性检验 / 种子** | **无** | **仍无**（无种子、无重复、无 CI、无检验） | **照旧未修正** |
| **实车** | 无 | 无 | **照旧** |
| **计算时间** | 报 28.07 ms（桌面 CPU） | **完全不报** | **倒退**（P1 的"端到端延迟/MCU 内存"两项在本文比 DeeP-LCC 更无可对齐物） |

**P1 该引哪一篇、怎么说（可直接照抄的写法）**：
- **两篇都引，但分工不同**：引 DeeP-LCC 说"非参数数据驱动混行编队控制不需要 HDV 模型、但需要一段满足持续激励的预采集轨迹，且其预采集轨迹是仿真生成的"；引本文说"同一族工作的最新一步把**可判真伪的运动学残差**注入该类控制器，并把 HDV 异质性升级为 NGSIM 标定的 IDM 参数分布，同时**仍然没有**弦稳定性结论与任何统计检验"。**两篇合并起来是 P1 最好的"数据驱动混行编队控制"背景句，且合起来仍留出 P1 的三个空白：弦稳定性、统计报告、OTF 这类启发式结构先验的注入。**
- **不得写**：不得写"已有工作把物理先验注入混行编队控制并取得 X% 提升"（本文的 4.14% 是确定性仿真平均值、基线口径还有歧义，且按项目 `AGENTS.md` §1 红线属"文献报告值，协议不同，不可直接比较"）；不得写本文有弦稳定性或统计检验；不得写本文做了实车。

---

## 7. 缺失信息（≥3 条）

1. **未印出编队规模 n 与受控车数 m 的数值**（仅有 `a 5-vehicle platoon (S = {1, 3})`），**未报告 CAV 渗透率**。
   - 影响：无法与 DeeP-LCC 的 `n=8, m=2, 25%` 并排比较；P1 引用时只能写"5 车编队、2 辆 CAV"。
   - 最小补法：向作者索取车辆清单与渗透率定义（分母是否含头车）。
2. **未报告任何计算时间、求解器、实时性数据**（无 QP 求解器/版本/容差、无单步耗时、无 MCU/嵌入式数据）。
   - 影响：P1 的"端到端延迟"与"MCU 内存占用"两项在本文**无对应物**；也无法评估 PA-DeePC 是否可能实时。
   - 最小补法：给出求解器与计时脚本，报 mean/median/p95/worst-case。
3. **未报告随机种子、重复次数、置信区间、显著性检验、多重比较校正**。
   - 影响：576 场景的 4.14%/9.29%/4.97% 全部是**确定性平均**，无不确定度；"physics significantly improves" 无统计支撑。
   - 最小补法：给出种子与重复次数，对每对基线做配对检验或 bootstrap CI。
4. **物理注入的实现在仿真节未交代**：式(18) 的目标函数只出现软罚项 `‖ϵk‖2 M`（M=500），但 Fig. 4b 图例同时出现 `PA-DeePC-Cost` 与 `PA-DeePC-Constraint`，正文**没有说明哪个结果用了哪种注入，也没有比较两者的性能**。
   - 影响：P1 无法判断"约束式注入 vs 罚项式注入"哪一种在该问题上更好——这恰是 P1 选 OTF 注入方式时最需要的证据。
   - 最小补法：给出两组注入在同一场景集上的并列结果。
5. **基线①的口径不可判定**（见 §6 陷阱 3）：`Original DeePC` 与 `PA-DeePC with a conventional optimization framework` 在文中是同一列还是两件事，无法确定。
   - 影响：**Table II 的 4.14% 不能被解读为"物理带来的提升"**。
   - 最小补法：明确列名与实现（是否含物理残差项）的对应表。
6. **PE（持续激励）条件未做实际校验**：Definition 1/2 与 Prop. 1 给出理论下界 `T ≥(m + 1)L + n −1`，但仿真节未核验 T=1000 是否满足、未做秩检验、未说明预采集轨迹是否覆盖足够丰富的驾驶行为。
   - 影响：论文称 `a consecutive trajectory with the inclusion of different and representative driving behaviors is collected to construct Hankel matrices`，但"representative"无操作化定义与校验。
   - 最小补法：给出 Hankel 矩阵秩的数值校验与预采集轨迹的行为覆盖度统计。
7. **未给代码、数据或补充材料**（无仓库链接、无数据可用性声明、无许可证）。
   - 影响：D3 只能给 1；P1 无法直接复现其 576 场景协议。
   - 最小补法：提供仓库 + commit + 数据说明。
8. **Fig. 3 的头时距分布"只有图没有分布"**：无拟合分布函数与参数，且 `we randomly select two distinct human drivers` 未给随机机制/种子。
   - 影响：24 名驾驶员的抽样**不可复现**。
   - 最小补法：给出 24 个 T_gap 取值清单与抽样脚本。

---

## 8. 关键数字（只抄印出的表格/正文，不得估读）

> `[计算值]` 为本卡按论文印出数字复算，**不是**论文印出的数字，不得作为文献报告值引用。本卡未使用任何图内估读数值。

### 8.1 TABLE II 完整转录（第 1088–1137 行，逐字数据）

`TABLE II — PLATOON ENERGY CONSUMPTION UNDER DIVERSE DRIVING CHARACTERISTICS`
`Energy consumption (Average) (kJ)`

| 车辆 | PA-DeePC | Original DeePC | Improvement | OVM(α=0.8, β=0.5) | Improvement | OVM(α=0.5, β=0.8) | Improvement |
|---|---|---|---|---|---|---|---|
| CAV1 | 1788.97 | 1998.23 | 10.47% | 1919.95 | 6.82% | 1886.48 | 5.17% |
| HDV1 | 1751.59 | 1807.26 | 3.08% | 1895.27 | 7.58% | 1824.67 | 4.01% |
| CAV2 | 1728.48 | 1742.90 | 0.83% | 1918.97 | 9.93% | 1814.87 | 4.82% |
| HDV2 | 1706.86 | 1728.71 | 1.26% | 1956.10 | 12.74% | 1814.89 | 5.95% |
| **TOTAL** | **6975.90** | **7277.09** | **4.14%** | **7690.29** | **9.29%** | **7340.91** | **4.97%** |

**本卡自洽性复算（全部通过）**：
- 行和：1788.97+1751.59+1728.48+1706.86 = 6975.90 ✓；1998.23+1807.26+1742.90+1728.71 = 7277.10 ≈ 7277.09（末位舍入）✓；1919.95+1895.27+1918.97+1956.10 = 7690.29 ✓；1886.48+1824.67+1814.87+1814.89 = 7340.91 ✓
- 降幅：(7277.09−6975.90)/7277.09 = **4.14%** ✓；(7690.29−6975.90)/7690.29 = **9.29%** ✓；(7340.91−6975.90)/7340.91 = **4.97%** ✓【计算值，均与论文一致】

### 8.2 其他印出数字

| 指标 | 值 | 出处 | 备注 |
|---|---|---|---|
| 预测误差上界（原版 DeePC） | ≤0.06 | §V-B 正文 | **单位未印**；Fig. 4 纵轴同时为 Velocity (m/s) 与 Spacing (m) |
| 预测误差上界（PA-DeePC） | ≤0.01 | §V-B 正文 | 同上；对照只在 `one case`（Fig. 4b） |
| 能量降幅（新 vs 旧优化框架） | 4.07% | §V-B 正文 | ⚠ 与 4.14% 并存且基线不同（见 §6 陷阱 4） |
| CAV1 最临界点 TTC | > 7.47 s | §V-B 正文 | 单次仿真；判据 `0 ≤TTC ≤4s` 为不安全 |
| 两 CAV 的 time gap 范围 | 1.5 − 2.6 s | §V-B 正文 | 单次仿真；判据 `TG ≥3s` 为低效 |
| 功率模型最大绝对误差 | 0.42 kW | §III-B 正文 | 相对误差"almost all 0%"（真值接近 0 kW 时除外） |
| 预采集轨迹长度 T | 1000 samples | §V-A | Δt=0.1 s → **100 s**【计算值】 |
| 采样间隔 Δt | 0.1 s | §V-A | |
| 预测时域 N / 初始时域 T_ini | 40 / 20 | §V-A | |
| 代价权重（新框架） | S=0.1, R=1, M=500 | §V-A | |
| 正则权重 | λ_g=20, λ_y=1000 | §V-A | |
| 时距边界 | th = 1/1.3 s；TG = 3.5/2.1 s | §V-A | 用于算 s_min/safe 与 s_max/effi |
| 编队与 CAV 位置 | `5-vehicle platoon (S = {1, 3})` | §V-A | **n、m 的数值未印出** |
| 驾驶员异质性范围 | T_gap ∈[0.5, 2.9] s，分 **12** 组，每组 0.2 s | §V-A | |
| 每组抽取驾驶员数 | 2（两名不同驾驶员） | §V-A | 驾驶员总数 **24**【计算值 = 12×2】 |
| 场景总数 | **576** | §V-A | 与 24² 一致【计算值】 |
| 头车速度剖面时长 | 6 minutes @ 0.1 s | §V-A | 取自 NGSIM |
| 测量噪声 | w ∈[−0.1, 0.1]（高斯项） | §V-B | 注入实时间距与速度 |
| OVM 基线参数 | 激进 α=0.8, β=0.5；温和 α=0.5, β=0.8 | §V-A | 论文称其为 "ACC" |
| IDM 参数（TABLE I） | a=4 m/s²、δ=4、s_gap=2 m、b=5 m/s²、v_d=25 m/s、T_gap=(0−5) s | TABLE I | 前五项在仿真中固定为常数 |
| 仿真平台 | MATLAB R2022b，Windows 11，3.8 GHz，32 GB RAM | §V-A | **非**嵌入式、**非**实车 |
| 参考文献数 | 33 | Crossref `reference-count` = 33 | 与本地作者版一致（[1]–[33]）✓ |
| Crossref 被引数 | 37 | `api.crossref.org/works/10.1109/TCST.2024.3361393` 字段 `is-referenced-by-count` | **端点已写明**（T6）；取用日期 2026-10-05 |
| 撤稿/更正检查 | Crossref `relation` 字段为**空对象** `{}` | 同上端点 | 未见撤稿/更正登记（T5，按 DOI 注册机构分流：非 `10.48550/` → 查 Crossref）✓ |

---

## 9. 字数核验（纪律要求：实测）

| 项 | 上限 | 实测 |
|---|---|---|
| §2 摘要 | 400 字 | 见文末核验命令输出 |
| §3 结论 | 350 字 | 见文末核验命令输出 |
| §4 方法一句话 | 60 字 | 见文末核验命令输出 |

**核验方法**（可复现）：
```powershell
node -e "const fs=require('fs');const t=fs.readFileSync('D:/Deepseek Harness/auto-driving/literature/fresh2024/notes/tcst2024-physics-augmented-deeplcc.md','utf8');const sec=(h)=>{const i=t.indexOf(h);const j=t.indexOf('\n## ',i+1);return t.slice(i,j)};for(const [n,h] of [['摘要','## 2. 摘要'],['结论','## 3. 结论'],['方法一句话','## 4. 方法一句话']]){const s=sec(h).replace(/^#+[^\n]*\n/,'').replace(/\s/g,'');console.log(n, s.length)}"
```

---

## 10. 本卡限制

1. **材料限制**：仅有 arXiv 2306.01387v2 的作者版纯文本（PDF 提取），**未获 IEEE VoR、未获补充材料**。正式版与作者版已确认存在差异（题名 `Eco-driving` vs `Eco-Driving`）；若正式版补充了计算时间、种子或额外实验，本卡未反映。
2. **图内数值不可用**：Fig. 2–6 的曲线/柱高**无任何印出数值**（除正文给出的 0.42 kW、7.47 s、1.5–2.6 s、0.06/0.01）。本卡一律不估读。
3. **口径限制**：D1–D5 为母协议 §5 判据，权重（3/2/2/1/2）是本机自定惯例，换权重会改变排序；本卡已标出 D1 的口径敏感性（14 → 11）。
4. **未做外部复现检索**：本卡不检索是否有第三方复现或后续批评（那是 `cross-paper-synthesizer` 的职责）；Crossref 被引 37 次**不等于**有独立复现。
5. **未联网核验的项**：论文未给代码/数据，故无仓库可核；NGSIM 数据集的可得性与许可本卡未核验。
