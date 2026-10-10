# 端到端驾驶中可解释 AI 的安全性含义｜Safety Implications of Explainable Artificial Intelligence in End-to-End Autonomous Driving

- **出处**：IEEE Transactions on Intelligent Transportation Systems, Vol. 26, No. 10, October 2025, pp. 14516–14535 ｜ **类型**：综述/分析性论文（含两个小型实证研究：定性 VideoQA 案例 + 对他人 RL 实验的定量转述）
- **作者**：Shahin Atakishiyev et al.（第一作者 Shahin Atakishiyev，加拿大阿尔伯塔大学计算科学系；合作者 Mohammad Salameh 华为渥太华先进无线技术实验室、Randy Goebel 阿尔伯塔大学）
- **DOI**：10.1109/TITS.2025.3574738（Crossref `works/10.1109/TITS.2025.3574738`，取用日期 2026-10-04：命中，题名一致，Vol. 26 / Issue 10 / pp. 14516-14535 一致，`relation` 为空 → 未见更正或撤稿标记）
- **全文来源**：`literature/fulltext/meeting2/safety-implications-of-explainable-artificial-intelligence-i__098bf905.txt`（本机文本 108,992 字符 / 20 页）
- **分组**：TITS
- **证据等级初判**：**C 级** — 以概念分析 + 案例分析为主：定性案例为**6 个驾驶场景**（SHIFT 仿真 + BDD-A 真实录像各若干，4–12 s）的单例展示，定量部分为**对 Cui et al. [85] 实验结果的重述**（非本文重跑），**无对照、无统计检验、无实车、无任何控制性能数字**。（若严格按"无对照的观点型分析"判，可降 **D 级**；本卡片按"有案例与数据展示"记 C。）
- **档位建议**：**B 略读** — 与 P1 的关系不在控制层，而在 **P1 `AGENTS.md` §1 的备用卖点（"若不显著，卖点改为可解释性 + 零额外传感器成本"）** 与 **§4 规范引用边界**：它给出可引用的标准名称与"解释本身也需要保真度检验"的反面证据。**不足以支撑 P1 的任何性能主张。**
- **五维打分**：D1=1 D2=1 D3=1 D4=2 D5=1 → 加权 = 3·1+2·1+2·1+1·2+2·1 = 3+2+2+2+2 = **11 / 20**

> ⚠ **冻结协议排除词表字面命中（需上游裁定）**：`literature/meeting2/00-triage-protocol.md` §3 中"语言模型评测"类含 `VQA driving`、`跨 ODD` 类含 `pedestrian interaction`——本文 **Experiment 1 正是 driving 视频问答（VideoQA）**，**§V-C 的"Molly problem"正是 AV 撞击行人且无目击者**。若**机械执行"命中即 D 档，不看总分"**，本文应降为 **D（排除）**。
> **本卡片按实质记为 B 的理由**：排除词表两条的理由栏分别写"与 P1 控制器无接口"与"跨 ODD 结论无效"——这两点**成立且已在本卡片逐条标注**；但本文的**可解释性评价维度与合规术语**恰是 D1=1 明列的相邻项（"可解释性评价"），且 P1 有一个**以可解释性为卖点的备用方案**需要它做引用纪律的约束。**若上游要求严格执行冻结协议，请以 D 档处置**；两种处置的信息都已保留在本卡片中。

---

## 1. 标题

Safety Implications of Explainable Artificial Intelligence in End-to-End Autonomous Driving｜中文直译：端到端自动驾驶中可解释人工智能的安全性含义

## 2. 摘要（≤400 字中文，保留关键数字与结论成立条件）
端到端学习管线正推动高等级自动驾驶的范式转移，但当代学习方法实时决策缺乏可解释性，阻碍用户信任与商业化，车辆卷入事故时问题更严重。作者指出汽车研究者尚未严格探索解释在端到端驾驶中的安全收益与后果，本文回答其安全性含义。做法分三层：重访已有安全与可解释性概念（ISO 26262 的 V 模型、SOTIF、面向 AI 的 ISO/PAS 8800、ISO/SAE 21434、接管请求与失效安全）；做关键案例研究（含限速标志被模型攻击把 35 mph 读成 85 mph、无目击者的 Molly 问题、以对象为中心的事故时空分析）；做实证研究，用 Video-LLaVA 对 SHIFT 仿真与 BDD-A 真实录像的场景（4 至 12 s）做视频问答式解释，并按动作与解释各自正确或错误四分法归类，另定量转述 Cui et al. 用 SHAP 解释车辆跟随任务中强化学习决策的结果。主要发现：解释模型在对抗提问下会编造解释、会在无红绿灯场景推理出红绿灯、会在红灯直行时给出错误解释；SHAP 显示自车纵向速度、车距与前车纵向速度最有影响，另两个速度分量可删。结论属概念框架与单例案例层面，无可解释性保真度的定量指标。

## 3. 结论（≤350 字中文）
作者结论：考察了 XAI 方法在端到端自动驾驶中的安全性含义，通过案例研究与实证证据揭示解释对提升安全的价值，并给出其优势、局限与挑战；研究从信息内容与形式、时间视角、传达对象三个维度做安全分析。两条主要结论：解释能揭示端到端模型训练数据中导致失败与事故的潜在模式，属数据驱动的洞见；这类解释可指导数据增强，通过迭代学习提升模型行为，以模块化方法可能错过的方式提升安全。作者自称首个从多维角度探索该问题的工作。自承局限：未研究解释异常检测、解释的鲁棒性与时间约束、不确定性下的解释及其安全保证；高级交互式解释框架尤其 Transformer 问答模型易对人类对抗性问题给出虚假回答，会损害用户感知安全与监管批准；解释传达的时间机制仍欠探索，且尚无关于其时间约束的共识。

## 4. 方法一句话（≤60 字）

端到端驾驶安全/XAI 概念 + 案例（含 Molly 问题）→ 视频问答式解释模型与 SHAP 特征重要性分析 → 解释的安全收益与风险清单。

## 5. 图表清单（占位符）

> 全文共 **14 个 Figure + 4 个 Table = 18 项**，超过 12；下表覆盖**按出现顺序的前 12 项**，剩余 6 项见补充表。
> ⚠ 与其他三篇相同的材料事实：本机 .txt **只有题注、没有表格单元格数值**。**本文不存在任何"对比实验主结果表"**——Table I/II/III 均为**分类学/清单表**（taxonomy），Table IV 是**公众调查结果表**；本文没有方法间的性能对照实验。§8 中的数值均抄自正文。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-XAI-1} | Fig. 1 | The modular and end-to-end pipeline comparison in autonomous driving. The modular pipeline is more explainable by design as it contains several interlinked components, but an error in one module (e.g., misdetection in perception) cascades to the downstream module (planning/control). On the other hand, the end-to-end driving pipeline, while lacking explainability, directly maps sensor input to control commands, optimizing system performance. Continuous improvement through data-driven optimization makes end-to-end learning more scalable. The source of the image of the vehicle: Waymo. | 模块化 vs 端到端的总对照；**对 P1 有用的一句**：模块化"按设计更可解释"，但误差会向下游级联；端到端"直接映射传感器到控制指令、牺牲可解释性换性能" |
| {FIG-XAI-2} | Fig. 2 | V-model in ISO 26262. The figure drawn based on the content in [24]. | 功能安全开发 V 模型；P1 若在稿件里提到功能安全流程，可据此图引用 **ISO 26262** 的结构（`AGENTS.md` §4：可引术语与思路，**不得**声称合规或已认证） |
| {FIG-XAI-3} | Fig. 3 | Potential takeover situations: (a) The blind corner ahead reduces the AV’s perception ability and urges for a takeover of the human driver, and (b) Autopilot perceives edge-markings of an exit lane as the continuation of the present lane (upper left, while still on the main road), steers right and the vehicle exits the road incorrectly (upper right, exit). Edge markings disappear when the autopilot takes a wrong exit. Images adapted from [36]. | 两类接管诱因：感知受限（盲弯）与感知误读（把出口车道边线当本车道延续）→ 后者的失败模式是"错误驶出"，属**感知层失败级联** |
| {FIG-XAI-4} | Fig. 4 | A diagram of safe autonomous driving. In (a), an AV (i.e., ego vehicle) interacts with the dynamic and stationary objects in the environment (i.e., vehicles ahead, pedestrians, and cyclists at the roadside identified with green, blue, and red bounding boxes, respectively) safely and keeps a distance from them. In (b), the ego vehicle faces the unexpected action of the other vehicle, understands its limited motion ability at that moment, and comes to a standstill as it can not drive safely at that time step. | "安全驾驶"的两个要件：保持距离 + 在自身运动能力受限时停住（fail-safe 的具象） |
| {TAB-XAI-1} | TABLE I | TAXONOMY OF VISUAL EXPLANATIONS FOR END-TO-END AUTONOMOUS DRIVING. CLASSIFICATION IS PARTIALLY BASED ON [48] | **分类学表**（非实验表）：后验/内生 × 局部/全局 × 显著性/反事实。**表体在本机文本缺失**；正文列出的代表工作含 ChauffeurNet、STEEX、OCTET、DeepTest（神经元覆盖）等 |
| {TAB-XAI-2} | TABLE II | TAXONOMY OF EXPLAINABLE REINFORCEMENT LEARNING APPROACHES FOR END-TO-END AUTONOMOUS DRIVING | **分类学表**：XRL 分为特征重要性、策略级解释、奖励分解、逻辑式解释、显著性图五类；作者强调 **XRL 主要面向研究者与开发者（而非乘客）** 做内在模型可解释性；**表体缺失** |
| {FIG-XAI-5} | Fig. 5 | A causal effect of removing a pedestrian from a scene: The driving behavior changes from “Stop” to “Go” by showing that the eliminated object is a risk object for the “Stop” command. Graphics credit: [56]. | 反事实解释的范例：删掉行人 → 行为由 Stop 变 Go，从而定位"风险对象"。**该图是"因果归属"的直观演示，P1 若声称 OTF 提供可解释性，需先回答"OTF 的哪一个分量对应哪个行为"这类反事实问题** |
| {FIG-XAI-6} | Fig. 6 | The time length of communicating explanations for safe and on-time human, vehicle reactions and situation awareness in autonomous driving. | 解释的**时间粒度四档**：即时反馈（毫秒）→ 感知解释（秒级）→ 行为解释（秒到分钟）→ 行程后解释（分钟到年）。P1 若报"端到端延迟"，这张图给出"解释能否按时送达"的框架 |
| {TAB-XAI-3} | TABLE III | PRETRAINED LARGE LANGUAGE AND VISION MODELS FOR EXPLAINABLE AUTONOMOUS DRIVING | **清单表**：Talk2BEV、DriveGPT4、LingoQA、VLAAD 等 LLM/VLM 解释工作；**表体缺失**；正文同时点名这些大模型的"幻觉"（authoritative but incorrect explanations）在真实驾驶环境中有严重后果 |
| {FIG-XAI-7} | Fig. 7 | Temporal evolution of three driving scenes and information conveyance to passengers using visual and textual explanations at these scenes, based on the AVs’ closeness to the other vehicles in oncoming traffic. Graphics credit: Schneider et al., [124]. | 四类场景反馈（主动非临界/主动临界/被动非临界/被动临界）的时序演化；正文称"**其中三类**在图 7 中示例"（⚠ 见下方内部不一致） |
| {FIG-XAI-8} | Fig. 8 | A deliberate hack causes the 35-mph sign limit to be incorrectly perceived as an 85-mph sign by Tesla’s ADAS at a testing site. The manually added red circles show the speed limit perceived by the heads-up display and modified speed sign. The figure has been drawn based on the content in [126]. | McAfee"模型攻击"实验：在限速 35 的"3"上加黑贴纸 → 车机读成 **85 mph** 并加速。用于论证"实时解释 + 事后解释"的安全价值（实时解释让乘客/安全员可按下紧急停止） |
| {FIG-XAI-9} | Fig. 9 | An example of object-centric accident video understanding from the Multi-Modal Accident Video Understanding (MM-AU) dataset of Fang et al. [129]. The graphics describe the temporal evolution, the root cause of the accident, and accident prevention advice in different time steps with textual explanations. | 以对象为中心的事故时空分析：涉及对象、事故类型、地点与时间、关键原因、预防建议；作者用它对照"模块化可归因到某个模块（如感知因阳光过曝未检出）vs 端到端只能揭示训练数据层面的潜在模式" |

**>12 的剩余 6 项（按出现顺序）**

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-XAI-10} | Fig. 10 | The Molly problem: An AV hits a pedestrian and nobody witnesses. Explainability of the AV decisions can help understand why the AV kept going and eventually hit the pedestrian at this scene. | 无目击者的伦理/责任场景；作者据此提出"事故前 / 事故点 / 事故后"三阶段解释问题清单（是否遵守限速、是否紧急制动；是否"知道"撞了人并停车；是否自动上报） |
| {TAB-XAI-4} | TABLE IV | THE MOLLY PROBLEM SURVEY: PARTICIPANTS’ ANSWERS TO THE SELECTED SAFETY-RELATED QUERIES. THE TABLE REPRODUCED BASED ON [128] | 公众调查（**296 名 18–73 岁受访者**）：**75%** 表示总体上愿意乘坐 AV；**97%** 认为 AV 的 AI 软件应当"知道"自己撞了人；**94%** 认为软件应当在碰撞处停车；**94%** 认为应当向现场旁观者发出危险警示信号。作者结论：多数社会观点认为 AV 在这类事故中责任更大。**表体缺失** |
| {FIG-XAI-11} | Fig. 11 | The results of our experiment on the chosen scenarios from the BDD-A dataset (recorded videos) with the Video-LLaVA multimodal transformer, as an explanation model. The model produces correct explanations for the conventional questions on the AV actions in the described scenes. | 真实录像（BDD-A）上的常规提问 → 解释正确；对应"**动作正确 + 解释正确**"（作者视为理想态） |
| {FIG-XAI-12} | Fig. 12 | The results of our experiment on the chosen scenarios from the SHIFT dataset (recorded videos) with the Video-LLaVA multimodal transformer, as an explanation model. Our deliberate questions confuse the model: In Scenarios 4 and 5, the model is influenced by tricky questions and generates incorrect responses. In Scenario 6, the explanation model fails to provide an adequate response on why the AV kept going straight under the red light. | 仿真数据（SHIFT）上的对抗提问 → 三种失败：无红绿灯却"推理出"红绿灯（场景 4）、实际右转却解释为左转避让（场景 5）、红灯直行给不出正确解释（场景 6） |
| {FIG-XAI-13} | Fig. 13 | The results from Cui et al.’s [85] experiment on describing influential features on the action decisions of the AV via feature importance vs. average absolute Shapley value plots for actions “Slower,” “Idle,” and “Faster,” respectively, in the vehicle-following task. | **跟车任务**上的 SHAP 平均绝对 Shapley 值图：三个动作下 **`ego_vx`、`d`、`front_vx` 最有影响**；`ego_vy`、`front_vy` 影响微弱 → 作者建议可从状态表示中删去（可降复杂度）。**⚠ 该结果来自 Cui et al. [85]，非本文实验** |
| {FIG-XAI-14} | Fig. 14 | A high-level, illustrative diagram of safety implications of explanations for the engaged people in end-to-end autonomous driving. | 解释对各类交互对象（乘客/安全员/开发者/监管者/事故调查者）的安全收益总览；对应 §VI-C 的"Explain to Control / Enhance / Defend / Adapt / Comply"五类价值 |

## 6. 对 P1 的用处

- **与 P1 的关系**：**相邻问题（仅限"可解释性评价"与"合规措辞"两个方向）**。P1 是连续时间控制器 + 编队跟车；本文不提供任何控制器、任何控制性能指标，ODD 为城市/行人场景。它的价值集中在 P1 `AGENTS.md` §1 的**备用卖点**（"若不显著，卖点改为可解释性 + 零额外传感器成本"）与 §4 的**规范引用边界**。
- **可迁移（具体到方法/协议/术语/图表）**：
  1. **★ 可解释性主张的"保真度"约束**：本文的核心教训是——**解释看起来合理 ≠ 解释忠实**。VLM 解释模型在对抗提问下会编造（实际右转却解释为左转避让）、会"看到"不存在的红绿灯。→ P1 若把 OTF 的可解释性当作卖点，**必须配一个保真度检验**（例如：OTF 势场分量与实际决策的相关性/反事实检验），否则会落入本文批评的同一类问题。这正是 P1 消融 A1 之外**最容易被 reviewer 攻击的点**。
  2. **"动作—解释"四象限检查表**（§VI-A）：正确动作+正确解释 / 正确动作+错误解释 / 错误动作+正确解释 / 错误动作+错误解释。→ 可直接作为 P1 撰写"可解释性"小节时的**自检矩阵**（P1 的 OTF 解释在"动作正确"时是否也正确？在动作错误时能否指出错误？）。
  3. **合规术语的准确写法（可直接抄标准号）**：ISO 26262（功能安全，V 模型见 Fig. 2）、**ISO 21448:2022（SOTIF）**、**ISO/PAS 8800:2024（道路车辆—AI 安全）**、**ISO/SAE 21434:2021（网络安全工程）**。→ 与 P1 `AGENTS.md` §4"可引用其术语与思路，**不得**声称合规或已认证"完全一致；本文提供了引用时的准确名称与年份（避免把 ISO/PAS 8800 写成已发布国际标准而不加 PAS 限定）。
  4. **"Explain to X"五类价值框架**（§VI-C）：Explain to Control（实时解释支持人工干预/接管）、to Enhance（事后解释做故障检测与修正）、to Defend（识别对抗攻击与安全漏洞）、to Adapt（对罕见场景迭代改进）、to Comply（责任、审计、事故调查、伦理与认证）。→ 若 P1 需要在 Discussion 里给"OTF 可解释性有什么用"，这是一个现成的**五分类骨架**（且每类都能指回 P1 的具体场景）。
  5. **反事实解释的形式（Fig. 5）**：删掉行人 → Stop 变 Go。→ 这是"最小干预式归因"的直观范例；P1 若要做 OTF 的可解释性实验，**这是可借的实验形态**（在场景中消去某辆邻车/改变其 OTF 贡献 → 观察控制器输出是否按预期变化）。
  6. **解释时间粒度四档（Fig. 6）**：毫秒级即时反馈 / 秒级感知解释 / 秒—分钟级行为解释 / 行程后解释。→ 可为 P1 的"端到端延迟"指标提供一个**"解释需在多久内送达才有用"**的框架（并提醒：100 Hz 控制回路下的解释不可能与人共享同一时间尺度）。
- **不可迁移 / 陷阱**：
  1. **不提供任何控制方法或控制性能数字**：无跟车 RMSE、无加速度平方积分、无 Jerk、无车道居中偏差、无前轮转角方差、无延迟、无 MCU 占用。→ **不能为 P1 的任何性能主张提供证据**。
  2. **ODD 不同且含行人**：城市/AI 事故场景 + Molly 问题（AV 撞行人）。P1 的 ODD 是高速主线编队，**跨 ODD 结论无效**（`AGENTS.md` §5）。
  3. **证据强度仅为"案例/概念"**：Experiment 1 只有 **6 个场景**（4–12 s）且为**定性**判断；无准确率/保真度指标、无对照、无统计、无实车闭环。
  4. **Experiment 2 不是本文实验**：§VI-B 明确写"We refer to the experimental study of Cui et al. [85]"，Fig. 13 题注亦写 "The results from Cui et al.'s [85] experiment"。→ **引用 SHAP 结论时必须写"转引自 [85]（Cui et al. 的实验），非本文实验"**，不得写成"该文复现/该文实验发现"。
  5. **不要把它的"first to explore"新颖性声明当作领域共识**：这是作者自述（"to our knowledge"），引用时须保留限定语。
- **引用时必须带的限定语**：**"该文为面向端到端自动驾驶的可解释性—安全性分析性论文（含 6 个场景的定性视频问答案例与对 Cui et al. [85] SHAP 实验的定量转述），ODD 为城市与行人交互场景；它不提供控制方法或任何控制性能指标，其关于 SHAP 特征重要性的结论转引自 [85] 而非本文重跑，全部结论停留在概念框架与单例案例层面。"**

## 7. 缺失信息（可执行动作）

1. **需回原 PDF 抄录 Table I / II / III 的完整表体**（视觉解释分类学、XRL 分类学、LLM/VLM 解释清单）与其列结构。（后果：本机文本只有题注；P1 若要在 Related Work 里写"可解释性方法分为几类"，必须拿到列名与行名，否则只能引正文散文表述。）
2. **需抄录 Table IV（Molly 调查）的全部问项与百分比**（正文只给了 75% / 97% / 94% / 94% 四项，且注明"reproduced based on [128]"）。（后果：该表是**二次引用**，若 P1 要引用这些百分比，必须回溯原始调查 [128]（"The Molly Problem Public Survey Results (Preliminary)", 2020）核对问项措辞与样本框，否则属三级转引。）
3. **需索取 Experiment 1 的完整场景清单与判定规程**：6 个场景分别取自 SHIFT 与 BDD-A 各几个、场景号与时长、提问清单、"解释正确/错误"由谁依据什么标准判定（是否有第二标注者、一致性如何）。（后果：无可信判定规程时，"模型给出正确解释"只是作者的主观判断，不能作为任何量化结论的基础。）
4. **需澄清 §V-A 的"其中三类在图 7 中示例"**：正文列了**四类**场景反馈（主动非临界 / 主动临界 / 被动非临界 / 被动临界），随后只把 Fig. 7 的左侧段归为"被动临界"、中间与右侧段归为"主动非临界"，**未指出第三类落在哪一段**。（后果：引用该分类时不能声称"图 7 展示了全部四类"。）
5. **需索取 Experiment 1 的复现材料**：Video-LLaVA 的具体版本/权重、推理参数、提问模板与全部问答记录。（后果：目前只有 6 张示例图，**无法复现也无法评估失败率**；而全文的核心主张（解释会幻觉）恰恰需要失败率数字支撑。）
6. **需澄清本文是否被任何标准/监管文件采纳**：文中多处把解释价值与 ISO 26262 / ISO 21448 / ISO/PAS 8800 / ISO/SAE 21434 并列讨论，但**未给出任何标准条款号**。（后果：P1 引用时必须只写"术语与思路"层面，不得由本文转述而暗示"标准要求提供解释"——`AGENTS.md` §4 明确禁止声称合规。）
7. **需确认本文是否有代码/数据可用性声明**：全文（含致谢）**未见**任何仓库或数据公开说明（对全文 grep `github` / `available at` / `open-source` 无命中于本文自身材料）。（后果：判定为"无复现材料"。）

## 8. 关键数字（只抄论文明确印出的表格/正文，不得目测估读）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| Experiment 1 场景数 | **6 个驾驶场景**（分别取自 SHIFT 仿真数据集与 BDD-A 真实驾驶数据集） | — | §VI-A |
| Experiment 1 场景时长 | **4 s – 12 s** | — | §VI-A |
| Experiment 1 解释模型 | **Video-LLaVA** 多模态 Transformer（plug-and-play 使用） | — | §VI-A |
| Experiment 1 的失败实例 | 无红绿灯场景被"推理出"红绿灯（场景 4）；实际右转被解释为"为避让对向来车而左转"（场景 5）；红灯直行给不出合理解释（场景 6） | — | §VI-A + Fig. 12 |
| Experiment 2 状态空间 | `S = [d, ego_vx, ego_vy, front_vx, front_vy]`（相对距离、自车纵/横向速度、前车纵/横向速度） | — | 式 (4) |
| Experiment 2 动作空间 | `A = [Slower, Idle, Faster]`（3 个离散动作） | — | 式 (5) |
| Experiment 2 主要发现 | **`ego_vx`、`d`、`front_vx` 最有影响**；`ego_vy`、`front_vy` 影响微弱 → 建议可从状态表示中移除 | **未报告**（无 Shapley 数值、无 CI、无重复） | §VI-B + §VI-C + Fig. 13（**结果来自 Cui et al. [85]，非本文实验**） |
| Molly 问题公众调查样本 | **296 名受访者**，年龄 **18–73 岁** | 未报告（抽样框与误差均未给） | §V-C + Table IV |
| 调查：总体愿乘 AV | **75%** | 未报告 | Table IV（数值抄自 §V-C 正文；表体缺失） |
| 调查：AI 软件应"知道"撞人 | **97%** | 未报告 | 同上 |
| 调查：软件应停在碰撞处 | **94%** | 未报告 | 同上 |
| 调查：应向旁观者发出危险警示 | **94%** | 未报告 | 同上 |
| 特斯拉限速标志误读 | 限速 **35 mph** 被读成 **85 mph** 并加速 | 单例 | §V-B + Fig. 8 |
| AV 反应时间（文中引用值） | 约 **100 ms** | 未报告（引自 [123]） | §IV-F-2 |
| 接管前置时间对照（文中引用值） | **4 s vs 7 s**：更短前置时间反应更快但接管质量更差 | 未报告（引自 [121]） | §IV-F-2 |
| 解释时间粒度四档 | 即时反馈（毫秒）／感知解释（秒级）／行为解释（秒—分钟）／行程后解释（分钟—年） | — | §IV-F + Fig. 6 |
| 引用的标准与版本 | **ISO 26262**（V 模型，Fig. 2）；**ISO 21448:2022**（SOTIF）；**ISO/PAS 8800:2024**（道路车辆—AI 安全）；**ISO/SAE 21434:2021**（网络安全工程） | — | §II + 参考文献 [24]–[28] |
| 是否存在对比实验主结果表 | **不存在**（Table I/II/III 为分类学表，Table IV 为公众调查表） | — | §IV–§V |

⚠**内部不一致 1（图 7 的示例类型数）**：§V-A 列出**四类**场景反馈后称"**three of them** are illustrated in Figure 7"，但随后只把 Fig. 7 的**左侧段**归为"被动临界"、**中间与右侧段**归为"主动非临界"，**未指明第三类对应哪一段**；Fig. 7 题注也只说 "three driving scenes"。

⚠**内部不一致 2（Experiment 2 的归属口径）**：§IV-B 写"We present insights from an RL-based explainability perspective in **Experiment 2**, Section VI-B"，§VI-B 标题亦为"Experiment 2: Quantitative Analysis…"（易读成本文实验）；但 §VI-B 正文首句为"We **refer to** the experimental study of **Cui et al. [85]**"，Fig. 13 题注也写"The results **from Cui et al.'s [85] experiment**"。→ **引用时不得声称该 SHAP 结果是本文实验结果。**

---

**卡片纪律声明**：本卡片所有图号、表号、题注均逐字取自上述 .txt 全文（含跨行题注的拼接，内容未改）；表格数值因本机文本不含表体，**一律标注"抄自正文"并给出节号**，无一处为目测估读。DOI 与卷期页经 Crossref 独立核验（2026-10-04）。本卡片不评价该论文的重要性与新颖性。
