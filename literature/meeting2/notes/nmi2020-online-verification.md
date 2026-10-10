# 在线验证防止自动驾驶致事故｜Using online verification to prevent autonomous vehicles from causing accidents

- **出处**：Nature Machine Intelligence, vol. 2, no. 9, September 2020, pp. 518–528 ｜ **类型**：期刊论文（Article）
- **作者**：Christian Pek et al.（Pek C, Manzinger S, Koschi M, Althoff M；其中 Pek/Manzinger/Koschi 三人为共同贡献作者；TU Munich, Cyber-Physical Systems Group）
- **DOI**：10.1038/s42256-020-0225-y（PDF 内印出；Crossref 核验 2026-10-03 通过：NMI 2(9):518–528，2020-09-14 online，被引 146）
- **全文来源**：`literature/fulltext/meeting2/using-online-verification-to-prevent-autonomous-vehicles-fro__7690174f.txt`（PAGES=11, CHARS=71,670）
- **分组**：连续时间 / 流体神经网络
- **证据等级初判**：B 级 — 顶刊正式版全文可得、方法（可达性分析 + 凸优化 + 归纳法安全证明）完整；但**全部结果为两个城市场景、用一辆 BMW 7 系录制的数据离线后处理得到**，**无闭环实车、无硬件规格、无重复次数、无置信区间**，且**ODD 是城市交叉口与人行横道，不是高速公路**。**【确定】**
- **档位建议**：B 略读 — 与 P1 的**安全性验证/回退轨迹**论证直接相关（P1 若要声称"OTF-CfC 控制器是安全的"，本文提供"安全层 + 失效安全轨迹"这一整套可直接借用的架构与措辞纪律），但其 ODD、证据类型（离线后处理）与硬件缺口，使其**不值得占 A 档精读预算**，按"仅引用其安全层架构与限定语"处理即可。**【确定】**
- **五维打分**：D1=3 D2=3 D3=4 D4=1 D5=5 → 加权 = 3·3+2·3+2·4+1·1+2·5 = 9+6+8+1+10 = **34**

## 1. 标题
Using online verification to prevent autonomous vehicles from causing accidents｜用在线验证防止自动驾驶车辆造成事故

## 2. 摘要（≤400 字中文）
作者提出一种面向**任意城市交通场景**的形式化验证技术，保证"**法律安全（legal safety）**"：自动驾驶车辆**永不自致事故**，同时允许其他交通参与者做出**一切合法行为**。它作为**已有运动规划框架之上的安全层**工作——规划器只给"意图轨迹（intended trajectory）"，本技术验证其是否合法安全，并在安全攸关时给出**回退方案**。三项关键性质：① **在线态势评估**——运行中严格预测其他参与者**所有合法未来演化**（可达性分析 + 形式化交通规则过滤），并计入测量不确定性；与经典测试法不同，**任意道路几何与任意交通参与者数**的未见场景都能处理；② **失效安全运行**——车辆始终持有一条通往**指定安全区**的失效安全轨迹；③ **构造即正确**——无论上游规划器（可含机器学习成分）如何，都保证合规；且**只从"所有动力学可行行为"中剔除"违规行为"**，故即使规则集不完整，保证依然成立（规则越少，行为越保守）。验证周期 c：收到意图轨迹 I_c 后，只把其中时长 Δt 的一段 I_c^safe 视为安全，随后计算**连续的失效安全轨迹 F_c**（需平滑接续、在全程时域上无碰撞、并停到安全区）；I_c^safe 与 F_c 的拼接即"已验证轨迹"。若验证失败，继续执行上一次已验证的轨迹。作者用**一辆 BMW 7 系在真实交通中录制的两个城市关键场景**（交叉口左转、行人乱穿马路）**离线**应用该方法，并另用三种不同意图规划器（含**一个完全忽略其他交通参与者的规划器**，用于模拟"尚未学会避撞的强化学习"）验证了"任意规划器下均保证合法安全"。

## 3. 结论（≤350 字中文）
作者结论（Discussion）：**认证（certification）**是该技术商业化的主要障碍；铁路、工业机器人、航空已有监管指引，而自动驾驶运动规划**只有有限规范（例如 ISO 26262 与 ISO 21448）**。作者称已通过形式化"legal safety"为该技术铺好认证基础，并主张：若 legal safety 成为公认标准，出行服务商可对其验证技术做认证，从而提升社会信任、**显著减少测试工作量**，即使更换意图轨迹规划器也不受影响。给出的定位对照：RSS（responsibility-sensitive safety）假定他人遵守常识规则并据此定义安全距离，**故不能排除自致事故**；not-at-fault driving 计算单条可证无碰撞轨迹；ref. 55 用有限个离线验证的局部模型在线拟合，**若找不到有效组合可能产生不安全行为**。**作者自承的局限**：① 保证建立在"**其他交通参与者遵守所有交通规则**"前提上（若发生碰撞，可论证是他人违规所致——但作者同时说明会在线监测违规行为并把它加入预测，以便重新寻找失效安全轨迹）；② 连续时间下的无碰撞（含控制扰动与模型不确定性）**未在本文证明**，而是"refer to the approach in ref. 67"；③ 只演示**两个（正文另称三个）城市场景**；④ 全部为**离线后处理**（正文逐字："applying our verification technique **offline**"）。

## 4. 方法一句话
意图轨迹 + 环境模型（车道/人行横道/禁停区 + 参与者类型与含不确定性的状态）→ 可达性分析得动力学可行行为、再用形式化交通规则过滤 → 占据集与可行驶域 + 凸优化求失效安全轨迹。

## 5. 图表清单（占位符）
全文共 **6 个 Figure + 0 个 Table**（合计 6 个，全部收录；正文另引用 Supplementary Fig. 8 与 Supplementary Videos，**不在本 .txt 内**）。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-ONVER-1} | Fig. 1 | Verification of legal safety. Intended trajectories (black line) are usually planned by only considering the most likely behaviours (grey lines) of other traffic participants. Our online verification technique ensures that the autonomous vehicle is safe in accordance with legal safety by maintaining fail-safe trajectories (red lines) at all times. … | **全文总纲图，P1 若引用"安全层"概念只需引这一张**：灰=最可能行为（规划器假设）、蓝=全部合法行为集合、红=失效安全轨迹、灰区=安全状态集。**要义：意图轨迹可以乐观，但必须始终有一条对"全部合法行为"都无碰撞的回退轨迹。** |
| {FIG-ONVER-2} | Fig. 2 | Verification during replanning. a, In each verification cycle c, the given intended trajectory Ic is verified by computing the safe part Isafe c and the fail-safe trajectory Fc. b, If the verification result of cycle c is successful (as in c ∈ {1, 2, 4}), the verified trajectory Isafe c ‖ Fc is executed starting at tc. | 验证周期的时序与状态机：(a) 每周期只取 I_c 的前 Δt 段作为 I_c^safe，并计算 F_c；(b) c=3 验证失败 → 继续执行上一周期已验证轨迹。**P1 的"OTF-CfC 输出不可信时怎么办"可直接照此设计**（且这是形式化保证，不是启发式）。 |
| {FIG-ONVER-3} | Fig. 3 | Results of Scenario I (urban intersection). a, Camera images and top view of the scenario. b, Verification results of selected verification cycles c. The intended trajectory Ic is only shown if it is successfully verified. Credit: Google, GeoBasis-DE/BKG (satellite images). | 场景 I（城市交叉口左转）：c=1 (t=0 s) 正常、c=6 (t=3 s) 失效安全轨迹把车停在交叉口内之前、c=10 (t=5.4 s) 骑行者在通过后重新验证成功继续左转。**同时演示"预测里含交通规则"**：对向车 ID 1718 在 t=5.4 s 只被允许直行或左转、不允许右转。⚠ 底图为 Google 卫星图（版权行必须保留）。 |
| {FIG-ONVER-4} | Fig. 4 | Results of Scenario II (jaywalking pedestrian). a, Camera images and top view of the scenario. b, Verification results of selected verification cycles c. The intended trajectory Ic is only shown if it is successfully verified. | 场景 II（行人乱穿马路）：行人 ID 323（蓝夹克、低头看手机）。作者**通过放松该行人预测中的约束来"主动扩大"其合法行为集**（同时考虑横穿与沿人行道边缘行走），于是 F₁ 让车保持在行人后方；c∈{2,3,4} 意图轨迹全部与行人冲突 → 执行 F₁ 减速；t=7.8 s 行人通过后加速通过。**这是"对脆弱道路使用者主动放宽行为假设"的可引用范例。** |
| {FIG-ONVER-5} | Fig. 5 | Results of the verification technique with different intended planners. a, Executed velocity profiles in Scenario I (results of cycles c ∈ {1, 6, 10} are labelled). b, Executed velocity profiles in Scenario II (results of cycles c ∈ {1, 4, 14} are labelled). | 三种意图规划器（Planner 1 连续优化 + 最可能行为；**Planner 2 = Planner 1 但忽略其他交通参与者，用于模拟"尚未学会避撞的 RL"**；Planner 3 离散状态空间采样）下的速度剖面。**要义：即使上游规划器完全不看别人，安全层仍能保证无自致事故**；代价是 Planner 2 在场景 I 会产生 −6 m/s² 的急减速。⚠ 图内**无任何均值/方差/重复次数**。 |
| {FIG-ONVER-6} | Fig. 6 | Computation steps of the verification technique. a, Time discretization t0 k in one verification cycle c. b, Overview of the computation steps for verifying an arbitrary intended trajectory. (1) We compute occupancy sets, that is, all legally occupied positions of other traffic participants over time. (2) The drivable area of the autonomous vehicle is computed to determine fail-safe manoeuvres. (3) Longitudinal and lateral driving corridors are selected from the reachability graph, and longitudinal and lateral trajectories are optimized such that a fail-safe trajectory is obtained. | **算法三步的可实现细节（P1 若自建安全层可逐步照抄）**：(1) 占据集 = 动力学可行可达集 ∩ 合法区域；(2) 可行驶域 = 把自车可达集**投影到位置域**得轴对齐矩形并存入有向图 G_R；(3) 在 G_R 上**反向搜索**从安全终态集出发选累积可行驶面积最大的纵向走廊 → 凸优化纵向轨迹（**四阶积分器、以 jounce 为输入、约束 v/a/jerk**，二次代价最小化 a/jerk/jounce 与速度偏差）→ 横向同理（**线性化运动学单轨模型 + 转向执行器限幅**）。⚠ 本图信息密度最高，但**所有约束的具体数值都不在正文**（在补充材料）。 |

**（无 >6 项的情形；全文 6 图 0 表已全部覆盖。）**

## 6. 对 P1 的用处

- **与 P1 的关系**：**相邻问题（安全层架构可直接借用）+ 不同 ODD（城市 vs 高速主线）**。本文与 P1 的控制器（OTF-CfC）**不在同一层**：本文是**规划层之上的验证/回退层**，P1 是**控制层的连续时间策略**。二者天然互补——**P1 若要回答"学习型控制器出错怎么办"，本文是唯一在顶刊给出"构造即正确"方案的可引用来源**。

- **可迁移**：
  1. **★"安全层 + 失效安全轨迹"这套架构可整体搬到 P1 的论证里**：逐字可引的规格是"**legal safety** = 自车永不自致事故 ∧ 其他参与者可做一切合法行为"（Abstract + §引言）。→ P1 若在 OTF-CfC 之外加一层形式化回退（哪怕只是概念设计），措辞上限是"**在 CARLA 与真实数据回放中引入了合法安全层的设计**"，**不得写成已认证或已实车验证**（`AGENTS.md` §4 明确禁止声称 ISO 26262 / 21448 合规）。
  2. **可逐字引用的"为什么必须在线上验证"的动机句**：正文逐字 —— "*However, **offline verification is not suitable for autonomous vehicles**, as these vehicles operate in highly uncertain environments in which **each scenario is unique**.*" → 直接对应 P1 `AGENTS.md` §5 的"开环 ≠ 闭环"与"场景覆盖/长尾"要求，是**反对"仿真里测够就行"的顶刊级引用锚点**。
  3. **"合法安全"把安全责任二分的论证结构（P1 可借用其逻辑）**：正文逐字 —— "*If a collision occurs nonetheless, we can **verifiably argue that another traffic participant must have violated traffic rules** and that the collision is **not self-inflicted** by the autonomous vehicle.*"（前提：已在预测中纳入全部合法行为）。→ P1 若做混行场景，可据此把"我方无责"与"对方违规"分开报告；**但前提条件（预测必须涵盖全部合法行为）必须一并写出，否则是断章取义。**
  4. **对"脆弱道路使用者主动放宽假设"的做法**：Scenario II 中作者**主动放松行人预测中的约束**（考虑其可能横穿），并明确这可由用户按场景配置 —— "*when driving past a school, one may wish to anticipate that any child or even any pedestrian may cross the road*"。→ P1 的"激进车流扰动 / cut-in 急并入"长尾场景，可照此写成**可配置的假设放宽（relaxation）**，而不是把长尾硬编码进损失函数。
  5. **"对上游规划器不敏感"这一强性质可作 P1 的鲁棒性论证模板**：本文用三种规划器（含一个**完全忽略他车**的 Planner 2）证明安全保证与规划器无关。→ P1 的基线对比（PID / MPC / TD3 / OTF-CfC）若要论证"我们的方法不依赖某个特定上游"，可引用这一**"与上游无关（correct by construction）"**的性质及其代价（Planner 2 出现 **−6 m/s²** 急减速 = 舒适性代价）。
  6. **具体的计算时延量级（P1"端到端延迟"指标的唯一可对照数字）**：正文逐字 "*detailed computation times (**177 ms on average**)*"，并说明"为避免仅因超时而无法验证新意图轨迹，意图轨迹应在 t_c − Δverify 之前提供，其中 **Δverify 是验证方法所需的计算时间**"。→ **177 ms ≈ 5.6 Hz**，对 P1 的 100 Hz（10 ms）回路**差约 18 倍**；P1 若把验证层放进实时回路，必须显式说明二者的频率比与"验证层异步、控制层同步"的分工。⚠ 177 ms 的硬件、样本数与统计量**均未报告**（详见 §8）。
  7. **失效安全轨迹优化的具体建模选择（可照抄的工程细节）**：纵向用**四阶积分器、以 jounce 为输入**并约束 v/a/jerk；横向用**线性化运动学单轨模型**并限幅转向执行器；代价函数二次、最小化 a/jerk/jounce 与速度偏差（纵向）、最小化横向距离/朝向偏差与曲率变化率（横向）。→ **这套"纵向四阶 + 横向单轨"的组合正是 P1 舒适性指标（加速度平方积分、Jerk 峰值）在文献里的标准建模口径**，可用于 P1 的基线 MPC 设计（`AGENTS.md` §3 的 MPC 基线）。

- **不可迁移 / 陷阱**：
  1. **★ ODD 完全不同**：本文全部场景是**城市交叉口左转**与**行人乱穿马路**（补充材料另有一个安全变道场景，正文仅提及"where the third most accidents occur"）。**无高速公路、无多车道主线、无编队、无跟驰**。→ **P1 不得用本文支撑任何高速/编队结论**；反之本文的城市结论也不能否定 P1。
  2. **★ 无闭环实车**：数据来自**一辆 BMW 7 系在真实交通中的录制**，然后**离线后处理**并离线施加验证技术（正文逐字："*we created two scenarios by recording real traffic with a BMW 7 series vehicle. By post-processing the real-world recordings, as described in the Supplementary Information, and **applying our verification technique offline***"）。→ 证据级别 = **真实数据录制 + 离线仿真**，**不是**在线闭环、**不是**实车验证。引用时措辞上限："在**真实交通录制数据上的离线验证**"。
  3. **无硬件规格**：全文未给计算平台（CPU/GPU 型号、主频、核数、内存）。177 ms 这个数字**无法复现也无法外推**。
  4. **无重复次数、无置信区间、无显著性检验**：全部结果为**单次运行**的轨迹与速度剖面（每个场景、每个规划器各一条）；作者亦未给出试验次数。
  5. **交通规则参数的具体数值不在正文**：正文只写"the values of the parameters are stored in a **database generated offline**, can be updated online, and are provided in the Supplementary Information"，以及规则清单（限速 × 超速因子 f_S、禁倒车、加速度上界 a_veh/cyc、不得驶离道路、跟车安全距离、变道方向一致；行人速度上界 v_ped 参考 ISO 13855、加速度上界 a_ped、禁止进入车道、人行横道例外、朝向偏离角 α、路缘条带宽度 d_slack）。→ **正文里没有任何一个具体数值**（v_limit、f_S、a_veh、a_ped、α、d_slack 全在补充材料）。P1 若引用这些量**必须标注来源为补充材料并自行取得**。
  6. **安全性的连续时间部分不在本文证明**：正文逐字"*To ensure that the autonomous vehicle is collision-free along Isafe and F **in continuous time** and despite control disturbances and model uncertainties, we **refer to the approach in ref. 67***"。→ **本文的保证是离散时间步上的**（归纳法在离散 t_k 上做）；连续时间与扰动鲁棒性**引他文**。P1 若引用"形式化保证"必须写明这一个缺口。
  7. **"guarantee" 的前提条件必须随引用带上**：合法安全成立的前提是**其他参与者遵守交通规则**，且**驾驶走廊的凸优化必须可行**（正文逐字："*In the rare event that **no feasible fail-safe trajectory is found**, the previously verified trajectory is further executed.*"）。→ 与 DeeP-LCC（本项目 #45）的"collision-free 仅在约束可行时成立"属同类限定，**P1 引用时不得省略**。
  8. **"显著减少测试工作量"是作者预期，不是本文测量结果**：Discussion 逐字 "*we **expect** that societal trust in autonomous vehicles will increase and that **testing efforts can be significantly reduced***"。→ 属 D 级（假设），**不得写进 P1 的任何主张句**。

- **与 CfC（NMI 2022）的关系**：**无同源关系；属"不同层"的互补，且互不引用。**
  - **无引文关系**：本文（2020-09 见刊）与 CfC（NMI 2022）在时间上互不引用；本文的 67 条参考文献全部是控制/形式化验证/交通领域，**没有任何 liquid neural network / LTC / CfC 条目**（本地 .txt grep `liquid|LTC|CfC` 零命中）。
  - **层面不同**：CfC 在**控制/表示层**（学习一条连续时间策略）；本文在**验证/回退层**（不学习，做可达性分析 + 凸优化 + 归纳证明）。二者**可以叠加**：CfC 作为意图轨迹/控制生成器，本文式验证层作为安全网。**但两篇论文都没有做过这个组合。**
  - **对 P1 的直接含义**：P1 若要在论文里写一段"安全与验证"，正确的引用组合是"**CfC 给出连续时间控制律（NMI 2022）+ Pek 等给出与上游规划器无关的形式化安全层（NMI 2020）**"，并明确说明**这是本文（P1）的设计组合，两篇原文均未验证该组合**。
  - **与 CfC 共有的缺口（可合并陈述）**：两篇**都没有报告硬件平台**；CfC 无可追溯的延迟数字，本文有 177 ms 但**无硬件、无重复**。→ **P1 的"端到端延迟可测"这一工程命题，在本组五篇中没有任何一篇提供可对齐的实测基线**（唯一有实测帧率的是 RA-L 2022 的 10→>30 FPS，任务为无人机躲避球）。

- **引用时必须带的限定语**：
  "在 Pek 等关于**在线验证**的工作中（Nature Machine Intelligence 2020;2(9):518–528），结论限定于**城市交叉口左转与行人乱穿马路**两个场景（补充材料另含一个安全变道场景），数据为**一辆 BMW 7 系在真实交通中的录制**，验证技术**离线后处理施加**（**非在线闭环、非实车**）；方法基于**二阶积分器抽象的可达性分析 + 形式化交通规则过滤 + 凸优化失效安全轨迹**，其交通规则参数（限速、超速因子、加速度上界、行人速度/加速度上界、朝向偏离角、路缘条带宽度）**全部存放在补充材料，正文未给任何数值**；安全保证建立在**离散时间步**上并在**其他交通参与者遵守交通规则**的前提下成立，**连续时间无碰撞与控制扰动鲁棒性系引用他文（ref. 67）而非本文证明**；平均计算时间 **177 ms** 的报告**未说明硬件平台、试验次数与统计量**；全文**无闭环实车、无硬件规格、无重复次数、无置信区间、无显著性检验**，且**不覆盖高速公路、多车道或编队场景**。"

- **P1 落地三问**：
  1. **是否有硬件实测？** **无（有真实车辆的数据录制，但没有硬件/实时性实测）。** 唯一硬件事实是"数据由一辆 **BMW 7 系**录制"；计算侧**完全未报告**平台型号、主频、核数、内存。唯一的时间数字是"**177 ms on average**"（正文 §Results，细节在补充材料），**无样本数、无方差、无 min/max、无硬件**。**无 MCU、无嵌入式、无实时性验证**；正文明确写验证是**离线**施加的。
  2. **是否报告参数量？** **无，且不适用。** 本文**没有任何学习模型**（形式化方法 + 凸优化）；"参数"一词在文中指交通规则参数（v_limit、f_S、a_veh/cyc、a_ped、α、d_slack 等），**这些数值全部在补充材料，正文未给**。→ P1 的参数量指标与本文**无从对齐**。
  3. **训练是在线还是离线？** **不适用（无训练）。** 需要区分的是**验证**的在线/离线：方法**设计为在线**（每个验证周期 c 在 t_c 前完成计算），但**本文的实验是在线下的**。作者自述的在线性要求是"意图轨迹应在 t_c − Δverify 之前提供，其中 Δverify 是验证方法的计算时间"——这是一个**实时性约束的定性表述**，没有给出 Δverify 的分布。**无任何训练/学习的内存或时间开销可报告。**

## 7. 缺失信息（≥3 条，写成可执行动作）
1. **★ 需取得补充材料中的全部数值**：交通规则参数数据库（v_limit、超速因子 f_S、|a_veh/cyc|、v_ped、a_ped、朝向偏离角 α、路缘条带宽度 d_slack）、Δverify 的详细计算时间分布（177 ms 的样本数、方差、最坏值）、以及第三个场景（安全变道）的全部结果。→ 动作：下载 NMI 2(9) 的 Supplementary Information。**在取得前，本卡与 P1 稿件不得引用任何规则参数的具体数值。**
2. **需作者提供计算平台规格与计时协议**：177 ms 是在什么 CPU 上、单线程还是多线程、是否含占据集预测与凸优化求解、求解器与容差为何？（后果：**没有硬件就无法判断该延迟能否满足 P1 的 100 Hz 回路**；P1 若要用 177 ms 做对照，必须写明"报告值，硬件未说明，不可直接比较"。）
3. **需作者提供重复次数与逐周期统计**：每个场景、每个规划器的运行次数；177 ms 的分布；Planner 2 的 5% 平均速度差是否为单次运行结果。（后果：目前**所有性能数字均为单次轨迹**，无不确定度，不能做任何统计推断。）
4. **需作者说明"其他交通参与者遵守交通规则"这一前提的实际覆盖率**：作者称会在线监测违规行为并加入预测，但**未报告在真实录制数据中检测到多少次违规、加入后对安全性与机动性的影响**。（后果：这决定"legal safety"在实际混行交通中的可用性——P1 的 ODD 是**人工与自动混行**，人工驾驶员的违规率正是关键；本文未覆盖。）
5. **需核验 ref. 67（Schürmann 等，ITSC 2017）到底证明了什么**：连续时间无碰撞与控制扰动鲁棒性被转引给该文。（后果：P1 若要声称"安全层在连续时间下有效"，**证据实际上在该文而非本文**，必须另行精读并引用。）
6. **需向作者确认 ODD 的边界**：本文声称"任意道路几何与任意数量交通参与者"，但全部演示是城市交叉口/人行横道。→ 动作：确认其在**高速公路主线、多车道、编队**下是否需要额外的规则集（如最小跟车时距、变道间隙判据），并记入 `[待核实]`。
7. **需做 T2 取代检查**：检索 2020 年后"online verification / fail-safe trajectory / legal safety"方向是否有更新且含硬件实测或高速公路场景的工作。→ 动作：OpenAlex/Crossref 检索并记录检索式与日期（本卡未做，标 `[待核实]`）。

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 验证计算时间 | **177 ms 平均**（"177 ms on average"） | **无**（无样本数、无方差、无最坏值；明细称在补充材料） | §Results（Experiments on real data 段） |
| 场景数（演示） | 正文称**两个**（城市交叉口左转、行人乱穿马路）；补充材料另给**一个**（安全变道） | — | §Results + §Results 末段 |
| 意图规划器数 | **3**（Planner 1 连续优化+最可能行为；**Planner 2 = Planner 1 但忽略其他交通参与者**；Planner 3 离散状态空间采样） | — | §Results（Legal safety for arbitrary intended trajectories） |
| 车辆期望速度（场景 I / II） | **8 m s⁻¹** | — | §Results（Scenario I / II） |
| Planner 2 在场景 I 的峰值减速度 | **−6 m s⁻²** | **无** | §Results（Scenario I） |
| Planner 2 在场景 I 的停车时间 | **< 2 s** | **无** | §Results（Scenario I） |
| 场景 II 平均速度（Planner 2 vs Planner 1） | Planner 2 **6.36 m s⁻¹**；Planner 1 **6.09 m s⁻¹**（Planner 2 **高 5%**） | **无** | §Results（Scenario II） |
| 场景 I 关键时间点 | t₁ = 0 s；t₅ = 2.4 s；t₆ = 3 s（执行失效安全轨迹）；t₁₀ = 5.4 s（验证成功、继续左转） | — | §Results + Fig. 3b + Fig. 3 图注 |
| 场景 II 关键时间点 | t₁ = 0 s；t₄ = 1.8 s（依 F₁ 减速）；t₁₄ = 7.8 s（行人通过后可通行） | — | §Results + Fig. 4b + Fig. 4 图注 |
| 场景 II 对比用的车辆/行人 ID | 车辆 ID **1718**、**1719**；行人 ID **323** | — | Fig. 3b / Fig. 4b |
| 验证循环的时域结构 | 周期 c 起始 t_c；I_c^safe 时长 **Δt = Δt_c^safe**（实验中对所有 c 取为常数重规划率）；F_c 起始于 **t_c + Δt_c^safe**，终止于 **t_c + Δt_c^safe + T_Fc** | — | §Results + Methods（Preliminaries） |
| 失效安全轨迹的终端约束 | 必须**停到指定安全区的静止状态**（例如最右车道、距交叉口足够远） | — | Methods（Driving corridor and trajectory optimization） |
| 纵向轨迹模型 | **四阶积分器**，控制输入为 **jounce**；约束纵向速度、加速度、**jerk**；代价最小化加速度、jerk、jounce 与速度偏差 | — | Methods（Driving corridor and trajectory optimization） |
| 横向轨迹模型 | **线性化运动学单轨模型**，含**转向执行器限幅**；代价最小化横向距离/朝向偏差与高曲率变化率 | — | Methods（同上） |
| 他车动力学抽象 | **二阶积分器**，速度与加速度有界；可达集只算**位置域**的紧过近似 R^(p)(t, t₀) | — | Methods（Occupancy prediction / Drivable area computation） |
| 行人速度上界（v_ped） | 正文只写"例如基于 **ISO 13855**"，**未给数值** | — | Methods（Occupancy prediction，行人规则） |
| 交通规则参数数据库 | **离线生成、可在线更新**，数值**在补充材料**，正文未给 | **无** | Methods（Occupancy prediction） |
| 交通规则条文的法源 | 维也纳道路交通公约（UNECE, 1968，2006 合并版）第 7、11.2c、11.2d、13.2、13.5、14.1、14.2、20.2、20.3、20.4、20.6b–d、21.1、21.2 条 | — | Methods + ref. 7 |
| 硬件平台 | **未报告**（无 CPU/GPU 型号、主频、核数、内存） | — | 全文（grep `Intel|CPU|processor|GPU` 无硬件命中） |
| 重复次数 / 统计检验 | **未报告**（全部为单次轨迹结果） | **无** | 全文（无 CI、无 SD、无 p 值） |
| 数据来源与处理 | 一辆 **BMW 7 系**在**真实交通**中录制；**离线后处理**施加验证技术 | — | §Results（Experiments on real data） |
| 实验性质 | **离线**（逐字："applying our verification technique offline"） | — | §Results |
| 连续时间保证的归属 | 本文**未证明**；引 **ref. 67**（Schürmann 等, ITSC 2017） | — | Methods（Guarantees of our verification technique 末段） |
| 安全保证的前提 | 其他交通参与者**遵守交通规则**；驾驶走廊凸优化**可行** | — | Methods（Occupancy prediction / Guarantees） |
| 未找到可行失效安全轨迹时的行为 | **继续执行上一次已验证的轨迹**（"In the rare event that no feasible fail-safe trajectory is found"） | — | Methods（Driving corridor and trajectory optimization 末段） |

⚠内部不一致 1：Discussion 写 "*Although **it cannot be excluded that autonomous vehicles are involved in accidents**, such as when a following car deliberately provokes a rear-end collision, **self-inflicted accidents can and should be eliminated***"（引言段），而 Abstract 写 "*Legal safety means that autonomous vehicles **never cause accidents** although other traffic participants are allowed to perform any behaviour in accordance with traffic rules*"。→ 两处对"永不"的**范围界定不同**：Abstract 的 "never cause" 事实上受"他方合法行为"与"失效安全轨迹存在"两个前提约束，Discussion 的表述更严格地承认了例外。**引用时必须采用 Discussion 的限定口径，不得直接引 Abstract 的 "never cause accidents"。**

⚠内部不一致 2：Results 段写 "*we created **two** scenarios by recording real traffic with a BMW 7 series vehicle*"，同段后文又写 "*In the Supplementary Information, we further provide **a scenario** illustrating safe lane changes (where the third most accidents occur)*"。→ **演示场景计数在"两个"与"三个"之间摇摆**（正文两个 + 补充一个），引用场景数时须注明"正文 2 个，补充材料另 1 个"。

【确定】/【待核实】标注：以上数字均为 PDF 印出值【确定】；"177 ms 的硬件与样本数" **`[待核实]`**（正文未给，称在补充材料）；"连续时间保证"归属 ref. 67 **`[待核实]`**（未读该文）；交通规则具体参数值 **`[待核实]`**（在补充材料）。
