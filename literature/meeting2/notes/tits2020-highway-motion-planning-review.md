# 高速公路运动规划综述｜A Review of Motion Planning for Highway Autonomous Driving

- **出处**：IEEE Transactions on Intelligent Transportation Systems, vol. 21, no. 5, May 2020, pp. 1826–1848 ｜ **类型**：综述
- **作者**：Laurène Claussmann et al.（Claussmann, Revilloud, Gruyer, Glaser）
- **DOI**：10.1109/TITS.2019.2913998
- **全文来源**：`literature/fulltext/meeting2/a-review-of-motion-planning-for-highway-autonomous-driving__d8c63ec6.txt`
- **分组**：TITS
- **证据等级初判**：D 级 — 叙事性综述：无检索式、无纳入/排除标准、无筛选流程图；分类与打分（Fig. 3 雷达图、Table II 比较表）为**作者主观赋值**，非实证证据；正文 200 条参考文献仅作汇编。
- **档位建议**：B 略读 — 与 P1 同 ODD（高速主线），可直接复用其**高速公路八大场景划分**与**实时性量级判据**，但无闭环数据、无协议可对标，不占 A 档精读预算。
- **五维打分**：D1=1 D2=1 D3=1 D4=2 D5=2 → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = 11

## 1. 标题
A Review of Motion Planning for Highway Autonomous Driving｜高速公路自动驾驶运动规划综述

## 2. 摘要（中文）
回顾近十年运动规划技术，聚焦**高速公路**：高速、小曲率、特定驾驶规则、受限环境。作者把"运动规划"定义为**路径生成 + 决策**，覆盖变道、避障、跟车、汇入。先给分层架构（Fig. 1）与运动策略五功能（路径规划、预测、决策、生成、变形；Fig. 2），再界定高速特殊性：单向车流、动态车速 > 60 km/h、道路为直线/回旋线/小曲率圆、标称情形仅机动车且共守同一规则、邻车行为限于左右变道与加/保/减。随后按**输出类型、时空属性、数学域**三属性建立分类学（Fig. 3），逐族综述空间构型、寻路、引力斥力场、参数与半参数曲线、数值优化、人工智能六族，并给出高速适用性五档比较表（Table II）。结论明确不声称穷尽。摘要无任何性能数字。

## 3. 结论（中文）
算法数量庞大，本文目标是识别高速场景的主要方法族：不声称穷尽、不排名，而是"从实用角度分类"，考察算法在仿真或实验中的表现与优缺点，**最优性次于可行性**——高速上必须至少存在一条可行运动，而"沿自车道跟随并调节纵向状态"天然可行。结论重申给出不同分解方式（雷达图属性刻画）、帮使用者按自身问题选方法、推动思考工程实现。

**作者自承的局限**：① 不声称穷尽；② 不排名；③ 明确**排除编队（platooning）专项研究**——"编队从运动规划角度不如从控制角度有意义"（§II-C，另见 [35]）；④ §III 引言承认分类方式无限多；⑤ §V-D 指出该领域**缺乏形式化分析与分层评估方法**，评估长期依赖大量仿真与人工按个人指标（安全、平顺、运行时间）打分。

## 4. 方法一句话
分类学（输出/时空/数学域）→ 六大家族归类 → 高速适用性打分表与缺口清单（非系统检索）。

## 5. 图表清单（占位符）
全文共 **12 个 Figure + 2 个 Table**（合计 14 个，全部收录）。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-CLAUSS-1} | Fig. 1 | A hierarchical scheme of Autonomous Ground Vehicle systems. | 感知/定位/通信 → 场景表示 → 运动策略 → 控制 → 执行器；含驾驶员与运动策略的双向闭环。P1 若要声明"同等可用信息"，可据此图界定各基线共享的输入边界。 |
| {FIG-CLAUSS-2} | Fig. 2 | Motion planning functions. Motion planning acts as a global, local, and reactive motion strategy. | 五个功能（路径规划/预测/决策/生成/变形）与全局—局部—反应三层对应；本文的核心分解框架。 |
| {TAB-CLAUSS-1} | TABLE I | SPACE AND TIME HORIZON FOR THE MOTION PLANNING FUNCTIONS | 各规划功能的空间/时间视野对照。⚠ **表格正文为图像，PDF 文本层未提取到任何行内容**；仅图注可得。 |
| {FIG-CLAUSS-3} | Fig. 3 | Taxonomy attribute classification. The radar charts show the distribution of each of the families considering the selected attributes. At the center of the chart, the methods do not suit the corresponding att | 六大家族的属性雷达图（0=完全不适用，3=很适用）；明示"赋值依据族定义与文献中出现频次"，即**主观打分**。 |
| {FIG-CLAUSS-4} | Fig. 4 | Space configuration illustrations. The points/cells/maneuvers are candidate solutions in blue, dismissed in red, and the solution in green. | 三类空间分解：(a) 采样点、(b) 连通单元、(c) 格（lattice）；候选解/被排除解/最终解的配色约定。 |
| {FIG-CLAUSS-5} | Fig. 5 | Illustrations of connected cells decompositions. | (a) 可见性分解、(b) Voronoi、(c) 驾驶走廊、(d) 向量场直方图 VFH、(e) 精确分解、(f) 动态窗口 DW。 |
| {FIG-CLAUSS-6} | Fig. 6 | Illustrations of the processes of (a) Dijkstra, (b) A*, and (c) RRT. | 三种图搜索的扩展过程；用于说明确定性 vs 随机的取舍。 |
| {FIG-CLAUSS-7} | Fig. 7 | Illustrations of attractive and repulsive forces approaches. | (a) 人工势场 APF、(b) 虚拟力场 VFF、(c) 弹性带。**与 P1 的 OTF 势场最直接相关的一族**。 |
| {FIG-CLAUSS-8} | Fig. 8 | Illustrations of the point-free and point-based curves methods. | (a) 无点曲线（tentacles，触须）；(b) 基于点的 Bézier 曲线；高速上 tentacles 被作者判为优于 lattice。 |
| {FIG-CLAUSS-9} | Fig. 9 | A map of AI-based algorithms. | AI 四子族：逻辑法、启发式、近似推理、类人方法（认知/理性 × 规则/学习两轴）。 |
| {FIG-CLAUSS-10} | Fig. 10 | Illustration of an FSM for highway [129]. Ci, Ei, Fi are specific conditions to transit between the vehicle behaviors Si. | 高速有限状态机；行为状态 S 与转移条件 C/E/F 的对应。 |
| {FIG-CLAUSS-11} | Fig. 11 | Illustration of the fuzzy logic decision in [138]. | 模糊推理判断变道时间是否充足（近/中/远间隙评价）。 |
| {FIG-CLAUSS-12} | Fig. 12 | Illustration of the first elementary tasks for "passing" in [161]. | 超车任务的层级任务分解（McKnight & Adams 45 项主任务 / 1700 项基本任务）的首批基本任务。 |
| {TAB-CLAUSS-2} | TABLE II | COMPARISON TABLE FOR HIGHWAY APPLICATIONS OF MOTION PLANNING METHODS ('−−' VERY INAPPROPRIATE, '−' INAPPROPRIATE,'∼' INTERMEDIARY, '+' APPROPRIATE, '++' VERY APPROPRIATE) | **本文对 P1 最有价值的表**：按族给出内在限制（性能/易用性/数据分析）与外在限制（对高精度传感器与基础设施的依赖）、复杂环境适应性、是否考虑环境与自车运动学约束，并用 −−/∼/++ 量化；参考文献以"上标=仿真、下标=实验"标注实现程度。⚠ **表格正文为图像，PDF 文本层未提取到任何行/列内容**；表内出现的族名与判据只能从 §IV 正文与 §III 各小节标题推出（六族：空间构型、寻路、引力斥力场、参数/半参数曲线、数值优化、人工智能）。 |

**（无 >12 项的情形；全文 12 图 2 表已全部覆盖。）**

## 6. 对 P1 的用处

- **与 P1 的关系**：**直接回答（同 ODD）**。ODD 完全对齐：单向车流、动态车速 > 60 km/h、直线/回旋线/小曲率、标称情形只有机动车——这正是 P1 声明的高速主线、多车道混行 ODD。但它是**规划层综述**，不提供编队控制闭环协议，也不处理"人工与自动混行"的社会交互建模（仅把邻车行为限制为左右变道与加/保/减）。

- **可迁移**：
  1. **高速公路八大标称情形清单**（§II-C，逐字可引）：Lane keeping / Car following / Lane changing / Lateral-most lane changing / Passing / **Overtaking** / Merging / Highway toll。P1 的 OTF 由"超车频次"定义，此处的 **Overtaking** 定义可逐字作为 P1 场景库的上位术语："This complex maneuver consists of a lane change, then passing a vehicle or an obstacle, and finally another lane change to return to the previous ego lane."
  2. **实时性量级判据（P1 可引用的硬数字，见 §IV）**：高速运动（> 17 m/s）、误差 1 m 时，运动规划算法须在 **10 ms 量级**内返回解才算实时。P1 的"端到端延迟"指标可据此设定数量级锚点（注意：这是作者的量级论断，非实测）。
  3. **P1 可直接引用的"缺口句"出处**：
     - §V-D-2 Evaluation："There is a lack of formal analysis and evaluation methods to hierarchically classify algorithms' performances."（**P1 提出 A1–A5 消融与逐场景报告的动机句**）
     - §V-D-2 Evaluation："the validation of motion planning algorithms mostly relies on extensive simulation and experimental testing results, where a human driver evaluates the action according to a personal reference index, such as safety, smoothness, or operation time"（**P1 反对人工主观打分、主张统一协议的动机句**；该句引 [54]）
     - §V-A-1 Data Uncertainty and Trustworthiness：需回答"多少数据才够、如何在延迟与不同步数据下决策"。
     - §V-D-1 Transition Stability：多规划器组合时架构是否稳定、是否需上层监督者。
  4. **势场族的两条可用结论**（§III-B-3，与 P1 的 OTF 势场同族）：
     - 优点："The main advantage is thus to be reactive to the dynamic evolution of the scene representation… no explicit space decomposition is needed."
     - 两条公认缺陷：**障碍附近振荡**（可用平滑算法解决）与**局部极小**；且作者给出反向观点——"local minima might be necessary in highway planning to keep the ego vehicle safe from inopportune lane changes"（引 [99]）。P1 若用 OTF 势场，**必须显式处理局部极小**，并可引此句说明"局部极小在高速上未必是纯缺点"。
  5. **可迁移的对照设计**：Table II 的"内在限制 / 外在限制"二分可借来组织 P1 的基线对比维度（实现在线重规划能力、对高精度长时域感知的依赖、是否考虑运动学约束）。

- **不可迁移 / 陷阱**：
  1. **ODD 反向陷阱**：本文明确把交叉口、城市、停车场、环形等排除在外——P1 不能借本文的任何结论去支撑城市/交叉口场景。反向也成立：本文的城市结论不能拿来否定 P1。
  2. **编队被作者显式排除**（§II-C）："We therefore do not consider any specific studies on platooning in this review." P1 是编队跟车控制，**不能再引本文作为编队控制的证据来源**，只能作为单车主线规划的综述来源。
  3. **无实验、无闭环、无统计**：Table II 的 −−/∼/++ 是作者赋值（§III-A 明示"按照族的定义与文献中出现频次赋值"），引为"性能排序"即为误用。
  4. **Table I 与 Table II 的正文在本 .txt 中完全缺失（图像）**：任何"本文报告了某族在某维度为 ++"的具体取值，**未从文本取得前不得写入稿件**。
  5. 本文是**规则式/几何/优化为主**的 2019 年定稿，AI 部分对 DRL 的覆盖极浅（§III-B-6 仅提及强化学习用于场景中各智能体策略与多目标超车），不能代表 2026 年的方法图景。

- **引用时必须带的限定语**：
  "在 Claussmann 等对**高速公路自动驾驶运动规划**（单向车流、动态车速 > 60 km/h、小曲率道路、标称情形仅含机动车）的综述中，作者给出的分类与适宜性打分基于族定义与文献出现频次的**主观赋值**，且该综述**明确排除编队（platooning）研究**，因此其结论不覆盖本文的多车编队跟车控制场景。"

## 7. 缺失信息（可执行动作）
1. **补 Table I 全文**：当前 .txt 只有图注。→ 动作：从本机 PDF 原件（若存在）用 OCR 或表格提取，取出"各规划功能 × 空间/时间视野"的具体行；在取得前，P1 稿件不得引用 Table I 的任何具体数值。
2. **补 Table II 全文**：同上。→ 动作：定位 PDF（`literature/fulltext/` 对应的原始 PDF 路径）并提取表格；重点取"Artificial intelligence 族"与"Attractive and repulsive forces 族"两行在"real-time implementation / uncertainty / kinematic constraints"三列的取值，用于 P1 的势场方法定位。
3. **核验 [35] Axelsson 编队安全系统综述**（IEEE T-ITS 18(5), 2017, pp. 1033–1045）是否为 P1 编队稳定性的合适引用锚点。→ 动作：Crossref 查 DOI 并读摘要，确认其 ODD 是否覆盖高速主线混行。
4. **核验作者关于"10 ms 实时性"的出处链**：该句为作者量级论断，未给实验支撑。→ 动作：检索"highway motion planning real-time 10 ms budget"类工作，或本项目自行以 CARLA 实测给出延迟预算；不得把 10 ms 当作本文实测值引用。
5. **核验 OA/许可**：本文页脚为 "© 2019 IEEE. Personal use is permitted"，非 CC-BY。→ 动作：确认本项目引用与图文复用范围（引用文字无碍；复用整表需走 IEEE 许可）。
6. **核验是否已被更新的高速运动规划综述取代**（T2 取代检查）。→ 动作：用 OpenAlex 检索 2020 年后 "highway motion planning survey/review"，记录检索式与日期，判断本文作为"分类学来源"是否仍为最新。

## 8. 关键数字（只抄论文明确印出的表格/正文）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 高速场景动态车速阈值 | > 60 km/h（fluid traffic, dynamic speed over 60km/h） | 未给 | §II-C 首段 |
| 高速运动定义（用于实时性判据） | > 17 m/s | 未给 | §IV |
| 实时性要求（误差 1 m 时） | 解须在 **10 ms 量级**内返回（"within the order of magnitude of 10ms to be real-time"） | 无实测/无区间；作者量级论断 | §IV |
| 高速公路标称情形数 | 8（lane keeping, car following, lane changing, lateral-most lane changing, passing, overtaking, merging, highway toll） | — | §II-C |
| 运动策略功能数 | 5（route planning, prediction, decision making, generation, deformation） | — | §II-B、Fig. 2 |
| 空间分解子族数 | 3（sampling points, connected cells, lattice） | — | §III-B-1、Fig. 4 |
| 算法家族数（分类学） | 6（space configuration / pathfinding / attractive-repulsive forces / parametric & semi-parametric curves / numerical optimization / artificial intelligence） | — | §III-B、Fig. 3 |
| AI 子族数 | 4（logic approaches, heuristic algorithms, approximate reasoning, human-like methods） | — | §III-B-6、Fig. 9 |
| 分类学属性数 | 3（type of output / space-time property / mathematical domain） | — | §III-A |
| 适宜性打分档数 | 5（'−−' very inappropriate, '−' inappropriate, '∼' intermediary, '+' appropriate, '++' very appropriate） | — | §IV、Table II 图注 |
| 参考文献条数 | 200（[1]–[200]） | — | 参考文献表 |
| 综述页数 / 图数 / 表数 | 23 页（pp. 1826–1848）；12 图；2 表 | — | 全篇统计 |
| Fig. 3/Table II 赋值的性质 | 主观赋值（"according first to the definitions of the families, and to their occurrence in the literature"） | — | §III-A、Fig. 3 图注 |
| McKnight & Adams 驾驶任务分解规模 | 45 项主任务，分解为 1700 项基本任务 | — | §III-B-6-d（引 [160]–[163]） |

⚠内部不一致：§IV 的适宜性标度被作者写成 "a '–/∼/+' scale"，但同段随即展开为五档 '−− / − / ∼ / + / ++'，Table II 图注也写五档——正文首句与后文/表注**档数不一致**（3 档 vs 5 档），属笔误，引用时以五档为准并注明。
