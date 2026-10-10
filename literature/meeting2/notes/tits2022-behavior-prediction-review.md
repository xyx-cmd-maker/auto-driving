# 深度学习车辆行为预测综述｜Deep Learning-Based Vehicle Behavior Prediction for Autonomous Driving Applications: A Review

- **出处**：IEEE Transactions on Intelligent Transportation Systems, vol. 23, no. 1, pp. 33–47, January 2022 ｜ **类型**：综述
- **作者**：Sajjad Mozaffari et al.（Sajjad Mozaffari, Omar Y. Al-Jarrah, Mehrdad Dianati, Paul Jennings, Alexandros Mouzakitis）
- **DOI**：10.1109/TITS.2020.3012034
- **全文来源**：`literature/fulltext/meeting2/deep-learning-based-vehicle-behavior-prediction-for-autonomo__474d5b70.txt`
- **分组**：TITS
- **证据等级初判**：C 级 — 综述类；无独立实验、无自有效应量与 CI，仅做分类与转引式比较，且其统一比较表的正文未随文本提取，属「相关/汇总」级，不达 B。
- **档位建议**：B 略读 — 加权 9 落在 B 区间下限（9–13）；D1=1（行为预测属 P1 相邻环节）满足非 D 条件；**未命中排除词**：该文唯一的统一定量比较做在高速公路数据集（NGSIM I-80 / US-101）上、与 P1 的 ODD 重叠，交叉口/环岛仅在「意图预测」子类中作举例（第 III-B1 节，4 处），且作者在第 IV-C(5) 节反过来把「局限于环岛/交叉口/T 型路口」列为领域缺陷。
- **五维打分**：D1=1 D2=0 D3=1 D4=2 D5=1 → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = **9**（D4 按正式卷期年 2022 计；若改按在线首发 2020-08-04 计则 D4=1、加权=8、落到 C 档边界——本卡取正式卷期年，理由见第 6 节陷阱条目）

## 1. 标题

Deep Learning-Based Vehicle Behavior Prediction for Autonomous Driving Applications: A Review｜面向自动驾驶应用的基于深度学习的车辆行为预测：一篇综述

## 2. 摘要（≤400 字中文，保留关键数字与结论成立条件）

综述把车辆行为预测定义为：由自车（EV）可获得的、对周边环境的当前与历史观测，推断目标车（TV）未来状态的条件分布 P(X_TV|O_EV)，其作用是支撑决策与风险评估。作者称传统（物理 / 机动 / 交互感知）方案只适用于短时域与简单场景，2014 年后深度学习方案在复杂环境表现更好，但缺少系统且可比的综述，故按三条准则分类——**输入表征、输出类型、预测方法**，并讨论若干知名方案性能、给出研究缺口与新方向。

关键事实：**摘要本身无量化数字**。全文唯一的统一比较在第 IV-B 节：用 NGSIM 的 **US-101 与 I-80 高速公路数据集**、以 **1.0–5.0 s** 预测时域的开环位移 RMSE 比较若干模型；并给出计数「among the reviewed deep learning-based articles, there are only seven works that use unified evaluation method」。

成立条件：①**仅高速公路、开环、离线位移误差**，不含任何闭环控制指标；②比较数值为**转引原作者**（仅 [28] 的 RMSE 由 [21] 换算为 SI 单位、[25] 取两数据集平均），协议不同，不可直接比较；③纳入文献截至 2019–2020 年成稿，数据集仅 NGSIM，全文未出现 highD / INTERACTION / Argoverse / nuScenes / INTERSECTION。

## 3. 结论（≤350 字中文：作者结论节要点 + 关键数字 + 作者自承的局限）

作者在第 V 节（Conclusion）称：深度学习行为预测方案虽在复杂场景表现可观，但要在自动驾驶中落地仍有开放挑战——多数方案虽考虑了车间交互，**环境条件与交通规则集合并未被直接输入预测模型**；且**传感器损伤与有限算力**等实际限制未被充分考虑。**结论节无任何数字**；全文数字见第 8 节。

作者自列（第 IV-C 节，5 条缺口）：①领域无统一基准，「among the reviewed deep learning-based articles, there are only seven works that use unified evaluation method」，且很少报告计算时间；②多数工作假设周边车辆状态**全可观测**，实际不可行，缺信息会降低预测精度；③交通规则很少作为显式输入；④未利用车辆转向灯、鸣笛等视听线索；⑤**多数现有工作局限于单一场景（roundabout / intersection / T-junction），缺少可跨场景的模型**。

注意：该文对「局限」的表述是**领域级**的；作者未报告自己的失败设定、消融或不确定度（因为该文没有自己的实验）。

## 4. 方法一句话（≤60 字，必须含「输入 → 模型 → 输出」三要素）

输入 69 篇深度学习行为预测文献 → 按输入表征/输出类型/预测方法三维分类并统一 RMSE 比较口径 → 输出分类体系、指标定义与 5 条缺口。

## 5. 图表清单（占位符）

全文共 **4 个 Figure（Fig. 1–4）与 4 个 Table（TABLE I–IV）**，合计 8 项，未超过 12 个，**已全部列出**。图注/表题逐字抄自全文（PDF 折行已按空格拼接；Fig. 4 原文跨行连字符 con-/nected 已还原为 connected）；超过 100 字符的按词边界截断并以 `...` 标记。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-BP-1} | Fig. 1 | Fig. 1. An illustration of the adopted terminology and limited observability of the EV’s onboard... | 定义 TV / EV / SV / NV 四类术语，并用「到 TV 的距离阈值 d」区分 SV 与 NV；被遮挡的 SV 以模糊效果表示。图注末尾给出机制示例：TV 的前车（EV 不可见）换道，使 TV 可加速——即**有限可观测性直接导致预测失真**。这是 P1 声明「邻车状态可观测」假设时必须处理的反例。 |
| {FIG-BP-2} | Fig. 2 | Fig. 2. Proposed classiﬁcations of state-of-the-art deep learning approaches... | 三条分类准则的类/子类树：输入表征（TV 轨迹 / TV+SV 轨迹 / 简化 BEV / 原始传感器）、输出类型（机动意图 / 单模态轨迹 / 多模态轨迹 / 占据栅格）、预测方法（RNN / CNN / 其他）。图注原文续文为「...for vehicle behaviour prediction.」可作 Related Work 的组织骨架图直接对标。 |
| {FIG-BP-3} | Fig. 3 | Fig. 3. An illustration of invalidity of the average of manoeuvres. The red car is... | 论证「模态平均不是合法机动」：红车接近绿车时可能减速（绿点）或换道（蓝点），单模态非机动条件预测器会输出两者均值（红点）以降低误差，但该均值会与前车碰撞。是**用 RMSE 评多模态预测会被"均值解"刷分**的经典论据（与第 IV-A 节 cross entropy 条目呼应）。 |
| {FIG-BP-4} | Fig. 4 | Fig. 4. An illustration of the vehicle behaviour prediction problem for connected autonomous... | 联网自动驾驶场景下的预测问题：其他自动车与路侧基础设施上的传感器可补充 SV 信息、缓解自车遮挡（对应第 IV-C 缺口 2 提出的 V2V/V2I 解法）。这是全文唯一涉及「车-车/车-路协同」的图示。 |
| {TAB-BP-1} | TABLE I | SUMMARY OF CLASSIFICATION OF EXISTING STUDIES BASED ON INPUT REPRESENTATION AND THE... | 四类输入表征的文献归类表，并逐类列优点/缺点（表题续文「...ADVANTAGES/DISADVANTAGES OF EACH CLASS」）。**表格正文未随 PDF 文本提取，txt 内只有表题**；正文对应说明在第 III-A 节。 |
| {TAB-BP-2} | TABLE II | SUMMARY OF CLASSIFICATION OF EXISTING STUDIES BASED ON OUTPUT TYPE AND THE... | 四类输出类型（机动意图 / 单模态轨迹 / 多模态轨迹 / 占据栅格）的文献归类与优缺点。**表格正文未提取**；正文对应说明在第 III-B 节。 |
| {TAB-BP-3} | TABLE III | SUMMARY OF CLASSIFICATION OF EXISTING STUDIES BASED ON THE PREDICTION METHOD AND... | 三类预测方法（RNN / CNN / 其他：全连接、RNN+CNN、GNN）的文献归类与优缺点。**表格正文未提取**；正文对应说明在第 III-C 节。 |
| {TAB-BP-4} | TABLE IV | COMPARISON OF TRAJECTORY PREDICTION ERROR OF SOME OF THE EXISTING WORKS... | 表题续文「...FOR DIFFERENT PREDICTION HORIZONS」：若干既有工作在**不同预测时域**上的轨迹预测误差比较，时域 **1.0–5.0 s**，数据集 NGSIM I-80/US-101（高速）。正文点名参与比较的模型为 GRIP [29]、ST-LSTM [25]、M-LSTM [24]、CS-LSTM [37] 及 [21]、[28]，另有从 [29] 取得的常速度卡尔曼滤波（CV）基线。**表格正文（各时域 RMSE 数值）未随文本提取，txt 内无任何误差绝对值。** |

> 材料说明：TABLE I–IV 的**表格正文在该 txt 中全部缺失**（仅存表题），Fig. 1–4 的**图本体**同样无法从 txt 读出；上述「读图要点」来自正文对图表的描述（第 II-B、III-A~III-C、IV-A、IV-B、IV-C 节），非目测读图。

## 6. 对 P1 的用处

- **与 P1 的关系**：**相邻问题**（不是直接回答，也不是无关）。该文给出的是 P1 上游**行为预测**环节的方法综述与开环评测协议，不给控制器、不给决策方法、不给闭环控制评价协议，因此不直接测 P1 的 RQ；但按冻结协议 D1=1 的定义，行为预测明确属于 P1 的相邻环节，故**不因「行为预测」判 D**。
- **可迁移**（具体到方法/协议/数字/图表）：
  1. **术语体系**（Fig. 1）：TV / EV / SV / NV + 「距离阈值 d 划分 SV/NV」——P1 声明 ODD 内邻车可见性与参与交互的车辆集合时可直接沿用，省去自造术语。
  2. **三维分类骨架**（Fig. 2 + TABLE I–III 表题）：输入表征 × 输出类型 × 预测方法——可直接做 P1 Related Work 的组织图；P1 若把 OTF 势场作为**输入表征**的一类（结构先验而非原始传感器数据），这张分类树正好是它落位的坐标系。
  3. **评测指标定义**（第 IV-A 节）：意图预测侧 accuracy / precision / recall / F1 / NLL / average prediction time；轨迹预测侧 FDE / MAE / RMSE / min-of-K / cross entropy / computation time。若 P1 或其后续工作（P2 世界模型的条件模态）要报预测精度，可复用这批指标的**定义与命名**。
  4. **可直接引用的方法性警示两条**：① min-of-K 只评最优轨迹、忽略其余 K−1 条，故「高分模型可能大部分预测很差」；② MAE/RMSE 偏向预测模态均值的模型，多模态场景应报交叉熵（式 (8)）或对称化交叉熵（式 (9)）。这两条对 P1 报告任何「预测/势场」类附加指标都是现成的防御性引用。
  5. **基线候选池**（均为转引，需回原文核协议）：高速换道/车道保持意图——Ding et al. [27]（GRU 编码器组建模 TV 与各 SV 的两两交互，长时域意图）、Xin et al. [21]（双 LSTM：一条预测目标车道、一条预测轨迹）；**cut-in 意图**——Lee et al. [34]（六层 CNN + 前后向雷达/相机融合的二值双通道 BEV，输入堆叠 2n 通道，预测 EV 左右前车的 cut-in 意图，面向 ACC）；高速 6 类机动的多模态轨迹——Deo & Trivedi [24]（6 个解码 LSTM + 1 个编码 LSTM + 机动 one-hot 初始化）、[37]（CS-LSTM，social tensor）。这些是 P1 Related Work 里「换道/cut-in 预测」一节的现成引用骨架。
  6. **动机段落**（第 IV-C 节 5 条缺口）：①无统一基准、很少报计算时间；②全可观测假设不成立；③交通规则少作显式输入；④未用视听线索；⑤多数工作局限于单一场景。前三条可作 P1 的 motivation 引用（**但必须做取代检查**，见第 7 节）。
- **不可迁移 / 陷阱**（具体）：
  1. **无任何可用数字**：TABLE IV 正文缺失，txt 内不存在任何准确率/召回/F1/RMSE 绝对值。**不得**凭该文写「高速换道预测准确率 X%」。
  2. **不是控制器、不是闭环**：该文全部评测是开环离线位移误差（RMSE/FDE），与 P1 的 7 项指标（跟车误差 RMSE、加速度平方积分、Jerk 峰值、车道居中偏差、前轮转角方差、端到端延迟、MCU 内存占用）**没有一项重合**。用它支撑 P1 的控制性能主张属越界。
  3. **数据集停留在 NGSIM 时代**：全文仅 NGSIM（I-80 / US-101）。已 grep 确认**无 highD、无 Argoverse、无 nuScenes、无 INTERACTION 数据集、无 INTERSECTION 数据集**（第 1453 行的 "Interaction-" 是文献 [47] 标题 "Interaction-aware Kalman neural networks"，不是数据集）。**不能**引它说明「当前公开数据集现状」。
  4. **无混行、无编队/队列**：全文**无 "mixed"（人工+自动混行）字样、无 "platoon"（编队/队列）字样**；唯一的协同内容在第 IV-C 缺口 2 提到 connected autonomous vehicles 与 V2V/V2I，且那只是**建议句、无实验**。P1 的「人工与自动混行编队控制」在这一篇里找不到任何支撑，**不得**把该文写成混行编队的研究基础。
  5. **cut-in 只有一处、且是转引**：第 III-B1 节一句「the latter designs a model to predict the cut-in intention of right/left preceding TVs w.r.t. the EV」（指 [34]），无任何量化结果。
  6. **D4 的年份敏感性**：该文 2019-10-20 投稿、2020-07-06 录用、2020-08-04 在线首发、正式卷期为 2022 年 1 月（vol. 23, no. 1）。本卡按正式卷期年 2022 记 D4=2（年龄 4 ≤5）；若按在线首发 2020 记，年龄 6 落在 5–15 区间 → D4=1 → 加权 8 → 落到 **C 档**。跨论文比较时须与本批次其他卡片统一口径。
  7. **它的「换道预测」是行为层（意图/轨迹），不是控制层的换道执行**；P1 的 OTF 势场若要用它，只能走「势场→预测化」的接口（P2/P3），不能反向当作 P1 的控制器依据。
- **引用时必须带的限定语**：该综述的结论建立在对 2014–2019 年间深度学习行为预测工作的**叙述性归类**之上，其唯一的统一比较是 **NGSIM I-80/US-101 高速公路数据集上、1.0–5.0 s 时域的开环位移 RMSE（数值为转引原作者，协议不同，不可直接比较）**，**不构成闭环控制评价**，也未覆盖人工-自动混行、编队队列与 2022 年后的公开数据集。

## 7. 缺失信息（≥3 条，写成可执行动作）

1. **补录 TABLE I–IV 的表格正文**：从 `TITS (IEEE Transactions on Intelligent Transportation Systems)/Deep_Learning-Based_Vehicle_Behavior_Prediction_for_Autonomous_Driving_Applications_A_Revi.pdf`（15 页，MD5 `474d5b700a05a4c3b0e221fba64b32fb`）或 IEEE Xplore HTML 版导出 TABLE IV 全部行（各模型 × 1.0–5.0 s 各时域的 RMSE），否则本卡**无法给出任何被引数字**。
2. **核对 TABLE IV 行数与正文计数**：正文第 IV-C 节称「only seven works that use unified evaluation method」，而第 IV-B 节点名的被比较工作为 6 篇（[21] [24] [25] [28] [29] [37]）＋ 1 个从 [29] 取得的 CV 基线。补录表格后数一遍行数，确认「seven」指 7 篇深度学习工作还是 6 篇 + 1 个基线。
3. **数据集现状须另找来源**：本文只到 NGSIM。若要写「换道/cut-in 预测的当前数据集与 SOTA」，需另取 2022 年后的预测综述或基准论文（highD / INTERACTION / Argoverse 2 / nuScenes 系），**不要**用本文充当现状引用。
4. **做取代检查（T2）**：该文缺口 1「行为预测无统一基准」成文于 2019–2020。引用前须检索 2022 年后是否已出现被广泛采用的 benchmark / 在线榜单（如 Argoverse / INTERACTION 挑战赛）；若已出现，该缺口陈述只能作为历史动机，不得写成「至今仍无基准」。
5. **核验 DOI 与卷期对应、并做撤稿/更正检查（T5）**：DOI `10.1109/TITS.2020.3012034` 属期刊（非 10.48550/ arXiv），按注册机构分流应查 Crossref `api.crossref.org/works/10.1109/TITS.2020.3012034` 的 `update-to` 字段，确认无更正/撤稿，并确认 pp. 33–47 与 2022 年卷期的对应关系。
6. **术语对齐**：该文第 II-C 节明确「behaviour」与「manoeuvre」在文献中常互换使用，并声称自己把 vehicle behaviour 作为上位词。P1 若用该文的「换道/切入」事件定义，须先把它与学位论文的 OTF 时间窗、四类工况（前车减速 / 邻车插入 / 前车驶离 / 前方无车）在事件边界上对齐，避免同一词指两个不同事件集。
7. **图本体不可读**：本卡所有「读图要点」均来自正文描述而非图像。若 P1 Related Work 要复用 Fig. 1 的 SV/NV 划分图或 Fig. 2 的分类树，须从 PDF 取原图并核对文字标签与正文一致。

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 预测时域范围（统一比较口径） | 1.0 to 5.0s | 未报告 | 正文第 IV-B 节（「RMSE errors for prediction horizons of 1.0 to 5.0s on NGSIM I-80 and US-101 highway driving datasets [69]」） |
| 统一比较所用数据集 | NGSIM I-80 与 US-101（高速公路） | 未报告 | 第 IV-B 节 + 参考文献 [69]（NGSim-FHWA Operations） |
| TABLE IV 各模型 RMSE 数值 | **PDF 提取文本内未见**（txt 内只有表题，无表格正文） | 不适用 | TABLE IV（第 12 页表题）；值缺失 |
| 参与统一比较的工作数（作者自述计数） | seven works | 未报告（且与本节点名的 6 篇 + 1 个 CV 基线存在计数疑点，见缺失信息第 2 条） | 第 IV-C 节缺口 1 |
| 加入统一比较的简单基线 | 常速度卡尔曼滤波（CV）模型，取自 [29] | 未报告 | 第 IV-B 节 |
| 被比较的深度学习模型（点名） | GRIP [29]、ST-LSTM [25]、M-LSTM [24]、CS-LSTM [37]、[21]、[28] | 未报告 | 第 IV-B 节 |
| 高速机动类别数（多模态轨迹） | 六类机动（six manoeuvre classes / six decoder LSTMs） | 未报告 | 第 III-B3、III-C1 节（[24]、[37]） |
| 意图预测最远提前距离（转引 [23]） | up to 150m before reaching three- and four-way intersections | 未报告 | 第 III-B1 节（Phillips et al. [23]，**转引**） |
| SV 选取规模示例（转引） | TV + 6 个最近邻 [23]–[25]；三车道 9 辆车 [28]；距离阈值划分 [29]–[31] | 未报告 | 第 III-A2 节（**转引**） |
| 网络规模示例（转引） | 六层 CNN [34]；三层 LSTM [18][19]；两层 LSTM [23]；单层 LSTM [28] | 未报告 | 第 III-C1、III-C2 节（**转引**） |
| 被引文献数 | [1]–[69]，共 69 篇 | 不适用 | 参考文献（第 13–14 页） |
| 全文页数 / 期刊页码 | 15 页（PDF）；pp. 33–47 | 不适用 | 提取头 `PAGES: 15`；各页眉页码 33…47 |
| 投稿—录用—上线时间 | received October 20, 2019；revised April 22, 2020；accepted July 6, 2020；Date of publication August 4, 2020；date of current version December 28, 2021 | 不适用 | 第 1 页脚注 |
| 基金 | TASCC Programme, Grant EP/N01300X/1（Jaguar Land Rover 与 U.K.-EPSRC 联合资助） | 不适用 | 第 1 页脚注 |

⚠内部不一致：无（未发现可证实的内部不一致——Fig. 1–4 与 TABLE I–IV 的正文引用位置均与图注/表题匹配；正文「seven works」与本节点名的 6 篇工作 + 1 个 CV 基线的计数疑点，因 TABLE IV 正文未随文本提取而**无法证实**，已列入缺失信息第 2 条）
