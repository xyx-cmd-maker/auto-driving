# 相机–LiDAR 融合感知深度学习综述｜Deep Learning for Image and Point Cloud Fusion in Autonomous Driving: A Review

- **出处**：IEEE Transactions on Intelligent Transportation Systems, vol. 23, no. 2, pp. 722–739, Feb. 2022 ｜ **类型**：综述
- **作者**：Yaodong Cui et al.（Yaodong Cui, Ren Chen, Wenbo Chu, Long Chen, Daxin Tian, Ying Li, Dongpu Cao；通讯作者 Dongpu Cao）
- **DOI**：10.1109/TITS.2020.3023541
- **全文来源**：`literature/fulltext/meeting2/deep-learning-for-image-and-point-cloud-fusion-in-autonomous__08b26da3.txt`
- **分组**：TITS
- **证据等级初判**：C 级 — 二次综合型综述（作者无自有实验、无对照组、无效应量与 CI）；表格对比为转引公开榜单的文献报告值
- **档位建议**：D 排除 — 加权分 4 分（≤4）且命中排除词表「LiDAR–camera fusion / object detection / semantic segmentation」；D1=0，本文属感知层、与 P1 的纵横向闭环控制无接口
- **五维打分**：D1=0 D2=0 D3=0 D4=2 D5=1 → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = 4

## 1. 标题
Deep Learning for Image and Point Cloud Fusion in Autonomous Driving: A Review｜面向自动驾驶的图像与点云融合深度学习：一篇综述

## 2. 摘要（≤400 字中文，保留关键数字与结论成立条件）

本文评述基于深度学习的相机–LiDAR 融合。按融合层级（signal/feature/multi/result-level）梳理 2014–2020 年工作，覆盖六类任务：深度补全、动/静态目标检测、语义分割、目标跟踪、在线跨传感器标定。作者在公开数据集（KITTI 的深度补全、3D 检测、road、MOT 四榜，另加 ScanNet）上列表对比。成立条件：只汇总**他人文献报告值**，作者无自有实验；性能数字在 TABLE I–V 表格正文（本提取文本缺失）；比较仅在 KITTI/ScanNet 等城市与室内感知基准、且多限良好光照与天气。作者自承：融合引入信号耦合（单路失效可拖垮下游）；全天候能力不足；开集检测缺协议；速度–精度与掉帧未解。

## 3. 结论（≤350 字中文：作者结论节要点 + 关键数字 + 作者自承的局限）

结论节（Section X）要点：按融合方法学组织，覆盖深度补全、动/静态目标检测、语义分割、跟踪与在线标定；表格给数据集性能对比、图给典型架构；提出被忽视且妨碍实车部署的开放问题。关键数字：2014–2020；10 图 6 表；参考文献 138 条；正文**未印出任何单一方法的性能数值**（数值在 TABLE I–V 正文，本提取文本缺失）。作者自承局限（Section IX）：① 信号耦合，单路失效可致整条流水线崩溃，sensor-agnostic 框架无最优解；② 数据集与方法多限良好光照与天气；③ 对抗攻击与 corner case 处理不足；④ 开集检测缺协议与指标；⑤ 速度–精度与掉帧未解。并表态：传统方法可解释性更好、算力消耗显著更低，当前深度学习不可回溯（not back-traceable），不适合决策与规划。

## 4. 方法一句话（≤60 字，必须含「输入 → 模型 → 输出」三要素）

输入相机图像＋LiDAR 点云 → 按融合层级归纳深度网络 → 输出六类感知任务的方法谱系与榜单对比表

## 5. 图表清单（占位符）

全文共 **10 个 Figure（Fig. 1–10）＋ 6 个 Table（TABLE I–VI），合计 16 个，已全部覆盖**。图注逐字抄自全文原文（英文照抄，超长者截断，截断处以 `…` 标注）。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-imgpc-1} | Fig. 1 | A comparison between image data and point cloud data. | 图像（规则、有序、离散）与点云（稀疏、不规则、无序、连续）的数据结构对比；是全文"为什么不能直接套用同一套特征提取"的动机图 |
| {FIG-imgpc-2} | Fig. 2 | Tasks related to image and point cloud fusion based perception and their corresponding sections. | 全文组织结构图：融合感知的各任务与对应章节的映射 |
| {FIG-imgpc-3} | Fig. 3 | Timeline of depth completion models and their corresponding fusion levels. | 深度补全模型时间线（按融合层级着色）；覆盖 mono-camera+LiDAR 与 stereo+LiDAR 两条线 |
| {FIG-imgpc-4} | Fig. 4 | Timeline of 3D object detection networks and their corresponding fusion levels. | 3D 目标检测网络时间线及其融合层级 |
| {FIG-imgpc-5} | Fig. 5 | A comparison between three typical model architectures for dynamic object detection. | 动态目标检测三类典型架构对比：2D 提议序列式、3D 提议序列式、one-step |
| {FIG-imgpc-6} | Fig. 6 | Some typical model architectures and fusion methods for road/lane detection. | 道路/车道检测的典型架构与融合方式（BEV 系 vs 前视系） |
| {FIG-imgpc-7} | Fig. 7 | A typical fusion-based trafﬁc-sign recognition pipeline. | 交通标志识别融合流水线：先用 LiDAR 反光特性在点云中定位，再投影到图像面生成 patch 交图像分类器 |
| {FIG-imgpc-8} | Fig. 8 | Timeline of 3D semantic segmentation networks and their corresponding fusion levels. | 3D 语义分割网络时间线及其融合层级 |
| {FIG-imgpc-9} | Fig. 9 | Some typical model architectures and fusion methods for semantic segmentation. | 语义分割的典型架构与融合方式（voxel 系、point 系、lattice 系） |
| {FIG-imgpc-10} | Fig. 10 | A comparison between Detection-Based Tracking (DBT) and Detection-Free Tracking (DFT) approaches. | 目标跟踪两大范式对比：DBT（tracking-by-detection）与 DFT（基于 FISST 的滤波，MeMBer / PHD） |
| {TAB-imgpc-1} | Table I | COMPARATIVE RESULTS ON KITTI DEPTH COMPLETION BENCHMARK [41]. | KITTI 深度补全榜单对比表；表头图例定义了学习范式（supervised/self-supervised/unsupervised）、输入模态（RGB image / sparse depth / confidence / stereo disparity）与四项指标（iRMSE、iMAE、RMSE、MAE）。**表格正文数值未出现在本提取文本中** |
| {TAB-imgpc-2} | Table II | COMPARATIVE RESULTS ON KITTI 3D OBJECT DETECTION BENCHMARK (MODERATE DIFFICULTIES) [56]. | KITTI 3D 检测（moderate 难度）对比表；图例含融合层级（FL）、融合类型（FT）、运行时间（RT）、模型参数量（MS）、点云表示（PCR）。图注给出 IOU 阈值：Car 70%、Pedestrian 50%、Cyclist 50%。**表格正文数值未出现在本提取文本中** |
| {TAB-imgpc-3} | Table III | A SUMMARIZATION AND COMPARISON BETWEEN DYNAMIC OBJECT DETECTION MODELS | 动态目标检测模型的定性汇总对比（优点/缺点/融合层级类），非纯数值表 |
| {TAB-imgpc-4} | Table IV | COMPARATIVE RESULTS ON KITTI ROAD BENCHMARK [56] WITH SUMMARIZATION AND COMPARISON BETWEEN LANE/ROAD… | KITTI road 榜单对比＋车道/道路检测模型汇总；图注定义 MAXF 为 KITTI urban marked road 测试集上的最大 F1，并列 FL（融合层级）与 MS（参数规模）。**表格正文数值未出现在本提取文本中** |
| {TAB-imgpc-5} | Table V | COMPARATIVE RESULTS ON KITTI MULTI-OBJECT TRACKING BENCHMARK (CAR) [56]. | KITTI MOT（car）对比表；图注定义 MOTA、MOPT、MT（mostly tracked）、ML（mostly lost）、IDs（ID 切换数）、Frag（碎片数）。**表格正文数值未出现在本提取文本中** |
| {TAB-imgpc-6} | Table VI | OPEN CHALLENGES RELATED TO PERFORMANCE IMPROVEMENT, RELIABILITY ENHANCEMENT | 开放挑战清单表，分两类：性能提升类（融合数据表示、时序上下文编码、学习范式、何时该用深度学习）与可靠性提升类（解耦相机–LiDAR、全天候/光照、对抗攻击与 corner case、开集检测、速度–精度权衡） |

## 6. 对 P1 的用处

- **与 P1 的关系**：不同问题。本文整篇面向**感知层**（相机–LiDAR 融合的深度补全/检测/分割/跟踪/标定），P1 假设邻车状态可观测、不做感知，研究的是高速公路主线多车道混行下的纵横向编队控制；本文不含任何车辆动力学、控制器、闭环仿真或编队评价协议。
- **可迁移**（仅落在术语/数据集/协议命名层）：
  1. **融合层级术语**：本文用的是 signal-level（≈ 数据级/早期融合）、feature-level、multi-level、result-level（≈ 决策级/结果级）四档，与常见的 data/feature/decision 三分法不完全同名；P1/P2 写相关工作若借用这套词，须按本文原词引用，并说明映射关系。
  2. **公开数据集与评测协议清单**：KITTI depth completion / 3D object detection / road / multi-object tracking 四个榜单（均引 [56] Geiger et al. 2012）与室内 ScanNet [110]；可作为"感知基准长什么样"的对照参照。
  3. **一条方向性判断**：作者指出多数感知系统忽视时序上下文（temporal context），建议用 RNN/LSTM 编码，并称这可缓解 LiDAR 低刷新率带来的点云形变与传感器时间不同步——与 P1 关注端到端延迟/时间一致性有主题上的邻接，但本文没有给出任何时序编码的控制闭环证据。
  4. **可作 P1 动机的外部引文**：Section IX.A.4 明确写"traditional methods have better interpretability and consume signiﬁcantly less computational resources"、"current deep learning algorithms are not back-traceable, making them unﬁt for these applications"（决策与规划），并主张深度学习只用于"有明确且可客观验证目标"的应用。这一段可支撑 P1「用结构先验+轻量连续时间网络替代端到端黑箱」的动机叙述——但只能作为**观点性引文**（本文该处无实验，属 D 级证据），不得包装成实证结论。
  5. **对 P2 而非 P1（显式注明）**：以上第 2、3 条以及本文对"多模态融合层级""开集检测缺协议""标注昂贵→需要弱监督/无监督"的论述，只对 **P2（以 OTF 场为结构条件模态的世界模型 / OTF 自动标注流水线）** 有间接用途，用于相关工作的术语与动机铺垫；**不可用于 P1 的任何性能主张**。
- **不可迁移 / 陷阱**：
  1. 本文的数据与协议是城市道路/室内**感知基准**，P1 的 ODD 是高速主线多车道混行，跨 ODD 结论无效。
  2. 本文**没有**任何纵横向闭环控制、跟车误差、舒适性、Jerk、车道居中偏差、前轮转角方差、端到端延迟或 MCU 内存占用的评价——不得从本文引出 P1 的任何指标阈值或基线。
  3. 本提取文本中 TABLE I–V 只有标题与图例，**表格数值正文完全缺失**；即便回到原 PDF，那些数字也是各方法原始论文的报告值，协议与硬件各不相同，**不可直接比较**。
  4. 本文对融合层级的优劣判断（如"sensor-agnostic framework 最优解仍未定"）是作者观点，非实验结论。
  5. 本文未提供任何代码、数据或在线榜单链接，无法据其复现对比。
- **引用时必须带的限定语**：本文是 2014–2020 年相机–LiDAR 融合**感知**方法的综述，其对比数字为 KITTI/ScanNet 等感知基准上的**文献报告值（协议不同，不可直接比较）**，作者未做自有实验，且全文不涉及高速公路多车道编队控制，故不能用于支撑 P1 的闭环控制性能主张。

## 7. 缺失信息（≥3 条，写成可执行动作）

1. **TABLE I–V 的数值正文在本 txt 中完全缺失**（只有表题与图例）。动作：回原 PDF 用 pdfplumber/PyMuPDF 抽取第 725、726、727、730、733 页的表格区域，逐格核对方法名—指标—数值并标注是否为原文印刷值。
2. **无代码 / 数据 / 在线榜单链接**（全文 grep `code|github|open source|leaderboard|available at` 未命中任何仓库或榜单地址）。动作：若需复现对比，改以各方法**原始论文**为引用源，本文只作谱系索引；不要把本文当作实现来源。
3. **作者未报告检索协议**（无检索式、数据库、纳入/排除标准、检索截止日期）。动作：如需评估覆盖完备性，自建 PRISMA 式补充检索并注明本文仅按"融合层级"组织、非系统综述。
4. **无效应量与统计**（无 mAP/RMSE/MOTA 的均值±方差、无置信区间、无显著性检验）。动作：任何需要不确定度的引用都必须回原方法论文；本文只能提供"有哪些方法、按什么层级分类"。
5. **运行时间（RT）列的测时硬件/平台未在本 txt 中说明**。动作：读原 PDF 的 TABLE II 表注与实验设置节，确认是否给出 GPU 型号与批大小；若未给，则本文的 RT 数字不可与 P1 的端到端延迟指标对标。
6. **摘要列 5 类主题、贡献列表与正文列 6 类**（摘要少写 stationary object detection）。动作：引用主题范围时以正文章节 III–VIII 的六类为准，并核对原 PDF 摘要是否确为 5 类。
7. **本提取文本含连字（ligature）替换**（如 `identiﬁed`、`ﬁrst`、`trafﬁc`、`ﬂawless`），会破坏按 ASCII 字符串匹配的 grep 与引用抄录。动作：抄录英文原句时先做 U+FB01/U+FB02 → fi/fl 的规范化，并保留原始字符备查。

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 综述覆盖时间范围 | 2014–2020 | 未报告 | 第 I 节贡献列表："the most up-to-date (2014-2020) overviews" |
| 出版信息 | vol. 23, no. 2, pp. 722–739, Feb. 2022 | — | 各页页眉（PAGE 1 起为 722，PAGE 18 为 739） |
| DOI | 10.1109/TITS.2020.3023541 | — | 第 1 页脚注 |
| 稿件时间线 | received April 9, 2020；revised August 27, 2020；accepted September 8, 2020；published March 17, 2021；current version February 2, 2022 | — | 第 1 页脚注 |
| 参考文献条数 | 138（[1]–[138]） | — | REFERENCES 节 |
| 图数 / 表数 | 10 图（Fig. 1–10）/ 6 表（TABLE I–VI） | — | 全文 |
| LiDAR 通道数 | 16 to 128 channels | 未报告 | 第 I 节（"low-resolution (ranging from 16 to 128 channels)"） |
| LiDAR 刷新率 | 10 Hz | 未报告 | 第 I 节（"low-refresh rates (10Hz)"） |
| KITTI 3D 检测 IOU 阈值 | Car 70%、Pedestrians 50%、Cyclists 50% | — | TABLE II 图注 |
| 各方法性能数值（iRMSE/iMAE/RMSE/MAE、3D 检测精度、MAXF、MOTA/MOPT/IDs/Frag、参数量 MS、运行时间 RT） | **本提取文本未印出**（TABLE I–V 仅有表题与图例，表格正文缺失） | — | TABLE I–V（正文缺失） |

⚠内部不一致：第 I 节写 "Trends, open challenges and promising directions are discussed in Section VII. Finally, a summary is given in Section VIII."，但正文中该内容实际位于 **Section IX**（TRENDS, OPEN CHALLENGES AND PROMISING DIRECTIONS）与 **Section X**（CONCLUSION）；Section VII 实为 OBJECTS TRACKING。

⚠内部不一致：正文把 PointNet 归到文献 [30]（如 "One of the pioneering works of direct learning on point clouds is the PointNet [30], [31]"），但参考文献 [30] 是 PointNet++，[31] 才是 PointNet；同一编号 [30] 在正文中既被当作 PointNet（"Qi et al. [30] extended the PointNet"）又被当作 PointNet++（"the PointNet++ [30] based encoders"），编号与文献存在错位。

⚠内部不一致（轻微）：摘要只列 5 类主题（depth completion, object detection, semantic segmentation, tracking and online cross-sensor calibration），而贡献列表与正文章节为 6 类（多出 stationary object detection）；属范围描述不一致，非数值矛盾。
