# 面向自动驾驶的深度多模态目标检测与语义分割综述｜Deep Multi-Modal Object Detection and Semantic Segmentation for Autonomous Driving: Datasets, Methods, and Challenges

- **出处**：IEEE Transactions on Intelligent Transportation Systems, Vol. 22, No. 3, March 2021, pp. 1341–1360 ｜ **类型**：综述
- **作者**：Di Feng et al.（Di Feng 与 Christian Haase-Schütz 共同第一作者 / contributed equally；其余：Lars Rosenbaum, Heinz Hertlein, Claudius Gläser, Fabian Timm, Werner Wiesbeck, Klaus Dietmayer）
- **DOI**：10.1109/TITS.2020.2972974
- **全文来源**：`literature/fulltext/meeting2/deep-multi-modal-object-detection-and-semantic-segmentation-__1aa920d0.txt`
- **分组**：TITS
- **证据等级初判**：C 级 — 综述类文章无作者自有独立实验（正文自述 "This review paper attempts to systematically summarize methodologies and discuss challenges"），全部定量数字为转引他人结果，且转引数字的主体表格位于 IEEE Xplore 附录、本 PDF 内未见
- **档位建议**：D 排除 — 命中排除词表第 1 条「感知层专用」（object detection / semantic segmentation / LiDAR–camera fusion / BEV perception 全部出现于标题与正文），理由「P1 不做感知；假设邻车状态可观测」；加权分仍按协议算出为 4（已落在 D 档区间 ≤4，与排除词判据结论一致，非仅靠排除词降档）
- **五维打分**：D1=0 D2=0 D3=0 D4=2 D5=1 → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = 0+0+0+2+2 = 4（D5 按本卡第 6 节陷阱第 2 条口径记 1：该文无作者自有实验与效应量，其 interactive online platform 是文献导航页、非可复现代码/数据）

## 1. 标题
Deep Multi-Modal Object Detection and Semantic Segmentation for Autonomous Driving: Datasets, Methods, and Challenges｜面向自动驾驶的深度多模态目标检测与语义分割：数据集、方法与挑战

## 2. 摘要（≤400 字中文，保留关键数字与结论成立条件）

感知层综述。作者针对「what to fuse / when to fuse / how to fuse」三个问题，系统梳理 2013–2019 年间发表的**多模态数据集**与**深度融合方法**，聚焦目标检测与语义分割两个任务，并讨论准确、鲁棒、实时三项要求下的挑战与开放问题。

数据集侧：所有被综述数据集均含 RGB 相机图像；LiDAR 点云见 [6], [59], [73]–[88]，热成像见 [89]–[91]；KAIST Multispectral [92] 同时给热成像与 LiDAR；仅 nuScenes [88]、Oxford Radar RobotCar [84]、Astyx HiRes2019 [93] 提供 Radar。规模从 1,569 帧到逾 1,100 万帧；作者自述有真值标签的最大数据集是 nuScenes，近 1.4M 帧（原文逐字作 "nearly 1,4M frames"，千位分隔符为逗号，本卡片未改值）；2014–2019 年数据集规模增长两个数量级。相比 ImageNet 的 1,034,908 样本，KITTI 仅 80,256 个目标。作者称 Eurocity [87] 为其综述中条件最多样的数据集（多国多城、全季节、天气与昼夜），但该数据集迄今仅相机模态。

方法侧：融合分为 early / middle / late 三类，融合操作为 addition/average、concatenation、ensemble、Mixture of Experts（MoE，含门控权重 wMi + wMj = 1）。**关键成立条件**：作者明确声明，从所综述方法中**未找到某一融合方案优于其他的确凿证据**，性能高度依赖传感模态、数据与网络架构。结论另指出 Radar 融合研究稀缺、不确定性建模尚未进入多模态感知、跨方法推理速度因硬件与编程语言不同而**难以比较**。附交互式在线平台导航各参考文献。

## 3. 结论（≤350 字中文：作者结论节要点 + 关键数字 + 作者自承的局限）

作者结论（Sec. VII）：已给出多模态数据集与融合方法（what / how / when to fuse）综述及挑战讨论。尽管多模态数据集持续增加，多数仍只记录 RGB 相机、热成像与 LiDAR，因此多数被综述方法只把 RGB 与热成像或 LiDAR 点云融合；Radar 融合只是近期才被研究，包括 nuScenes [88]、Oxford Radar RobotCar [84]、Astyx HiRes2019 [93]，以及 Chadwick et al. [133] 融合 RGB 与 Radar 点做远距车辆检测的开创性工作。作者预期未来出现更多 Radar 数据集与融合方法，并指出开放集条件与传感器失效下的多模态感知研究不足。

自承局限（逐条取自结论与 Sec. VI）：① 未见某一种融合方法优于其他的确凿证据；② 因缺乏标准硬件与编程语言的基准，跨方法推理速度难以比较，各方法推理时间仅由作者自行报告，"It is an open question how these methods perform when they are deployed on automotive hardware"；③ 多数方法只在 KITTI [6]、KAIST Pedestrian [92] 等公开集上训练评估，未专门处理传感器冗余；④ 融合 LiDAR/相机与 Radar、超声波、V2X 的研究极少，作者称不知道任何融合超声波信号的深度多模态感知工作；⑤ 就 LiDAR 前视表示优劣只有 Pfeuffer and Dietmayer [110] 做过研究；⑥ 据作者所知 BNN 尚未被引入多模态感知；⑦ 多模态学习的可视分析尚无研究；⑧ 常用评测指标不考虑开放集条件或传感器退化/失效；⑨ 多数方法为单帧 CNN，预测不依赖前帧、时间上不一致。

## 4. 方法一句话（≤60 字，必须含「输入 → 模型 → 输出」三要素）

文献（2013–2019 数据集与融合方法）→ 按 what/how/when to fuse 分类归纳 → 数据集表、方法表与开放问题清单。

## 5. 图表清单（占位符）

全文共 **12 个 Figure（Fig. 1–Fig. 12）+ 1 个正文 Table（Table I）**；另有 5 个附录表（Tab. II、III、IV、V、VI）被正文引用，但**本 PDF 提取文本内未见其表体与表题**，故不列入下表（详见第 7 节与「⚠内部不一致」）。因此上表覆盖全文可见图表 13 项中的 13 项。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-MMOD-1} | Fig. 1 | "A complex urban scenario for autonomous driving. The driverless car uses multi-modal signals for perception, such as RGB c" | 城市复杂场景示意；驾驶舱视角叠加多模态输入（RGB/ LiDAR 点/ Radar 点/ 地图）与部分目标的框与分类分，说明感知任务的对象 |
| {FIG-MMOD-2} | Fig. 2 | "Average precision (AP) vs. runtime. Visualized are deep learning approaches that use LiDAR, camera, or both as inputs for car" | AP–运行时间散点；数据取自 KITTI leaderboard（visited on Apr. 20, 2019），仅收录已发表方法，融合相机+LiDAR 者多数优于单模态 |
| {FIG-MMOD-3} | Fig. 3 | "(a) The Boss autonomous car at DARPA 2007 [2], (b) Waymo self-driving car [14]." | 两台试验车外观与传感器布置的实拍图，用于说明测试平台代际 |
| {FIG-MMOD-4} | Fig. 4 | "The Faster R-CNN object detection network. It consists of three parts: a pre-processing network to extract high-level image fe" | 两阶段检测器结构：特征提取 → RPN 生成候选 → Faster-RCNN head 精修 |
| {FIG-MMOD-5} | Fig. 5 | "(a) Normalized percentage of objects of car, person, and cyclist classes in KAIST Multispectral [92], KITTI [6], Apolloscape" | (a) 四个数据集 car/person/cyclist 类占比（car 远多于另两类，类别极不平衡）；(b) 各数据集相机帧数，显示两个数量级增长 |
| {FIG-MMOD-6} | Fig. 6 | "RGB image and different 2D LiDAR representation methods. (a) A standard RGB image, represented by a pixel grid and color cha" | LiDAR 六种 2D 表示对照：RGB、稀疏前视深度、插值深度、反射率插值、球面图（环视）、BEV（前向、无插值） |
| {FIG-MMOD-7} | Fig. 7 | "An illustration of the Mixture of Experts fusion method. Here we show the combined features which are derived from the output" | MoE 融合结构：各模态专属 expert 网络输出经门控网络加权平均，权重和约束为 1 |
| {FIG-MMOD-8} | Fig. 8 | "An illustration of early fusion, late fusion, and several middle fusion methods." | 三类融合时机的结构对照图，含 deep fusion 与 short-cut fusion 的中间层连接方式 |
| {FIG-MMOD-9} | Fig. 9 | "Examplary fusion architectures for two-stage object detection networks. (a). MV3D [97]; (b). AVOD [102]; (c). Frustum PointNe" | 四个两阶段检测融合架构并列图（MV3D / AVOD / Frustum PointNet / Ensemble Proposals），对应 what/how/when 的不同取法 |
| {FIG-MMOD-10} | Fig. 10 | "Two examples of increasing data labeling efﬁciency in LiDAR data. (a) Collaborative labeling LiDAR points for 3D detection [174" | (a) 人弱标 + F-PointNet 预训练模型精修，报告 30× 标注加速；(b) 用预训练图像 SegNet 把图像语义迁移到 LiDAR 点 |
| {FIG-MMOD-11} | Fig. 11 | "(a) An illustration for the inﬂuence of label quality on the performance of an object detection network [195]. The network is" | 标签质量消融：随机噪声（高斯 σ）与系统性偏移（全部框平移 σ）对比，网络对随机错误远比对有偏标签鲁棒 |
| {FIG-MMOD-12} | Fig. 12 | "The importance of explicitly modeling and propagating uncertainties in a multi-modal object detection network. Ideally, the n" | 不确定性传递示意：夜间相机应给高不确定性，该信息供机动规划/紧急制动等下游模块使用 |
| {TAB-MMOD-1} | Table I | "AN OVERVIEW OF CHALLENGES AND OPEN QUESTIONS" | 挑战与开放问题总览表（正文 Sec. VI 开头引用为 "Tab. I summarizes the challenges and open questions"）；**本 PDF 提取文本内只有表题、未见表格内容**，无法逐项引用 |

## 6. 对 P1 的用处

- **与 P1 的关系**：**不同问题**。本文是**感知层**综述（目标检测 + 语义分割），P1（OTF-CfC）做的是高速公路主线多车道混行的**纵横向闭环编队控制**，二者在系统栈上不在同一层，且 P1 的 ODD 与本文实证数据所在场景（KITTI 为德国卡尔斯鲁厄中等城市、多为白天晴天；Cityscapes/Mapillary Vistas 为城市街景；Eurocity 为欧洲多城）不重合。本文不提供任何控制器、决策方法或同 ODD 闭环控制评价协议，D1 = 0 属结构性不吻合，非质量问题。
- **可迁移**（**均可迁移到 P2 世界模型，对 P1 无直接接口——以下四点显式标注为「对 P2 而非 P1」**）：
  1. **对 P2 而非 P1｜数据集与 ODD 标注**：nuScenes [88]（近 1.4M 帧，含 Radar）、Waymo Open Dataset [83]、Argoverse [81]、H3D [78]、A2D2 [86]、PandaSet [82]、Lyft Level 5 [80]、BLVD/BLV3D [79]、KAIST Multispectral [92]、Eurocity [87] 等 2013–2019 数据集清单，可作为 P2 选数据集的候选池与「数据条件多样性」核对表。**注意**：本 PDF 内缺失承载这些字段的 Tab. IV，引用具体数据集规模/模态/标签字段时**必须回查 IEEE Xplore 附录原文**，不得从本卡片二手转抄。
  2. **对 P2 而非 P1｜术语与论证框架**："what to fuse / how to fuse / when to fuse" 三分法，以及 early / middle / late fusion 的数学描述（式 1–6），可作为 P2 世界模型**条件模态注入位置**的写法模板与术语来源（对应 P2 的结构条件模态 = HDMap / 3D Box / OTF 场）。
  3. **对 P2 而非 P1｜开放集与不确定性论证**：第 VI-B2 节「显式建模各模态信息量/不确定性」与「感知不确定性需传播到运动规划 [199]」的论述，可作为 P2 讨论「条件模态在传感器退化时如何降级」的动机引用；但作者自述 BNN 尚未进入多模态感知，此点只能作为 gap 陈述、不能当作已完成工作引用。
  4. **对 P2 而非 P1｜评测口径警告**：作者明确指出跨方法推理速度因**硬件与编程语言缺乏统一基准**而不可比、"the inference time is reported only by the authors"。这条可直接支撑本项目对「资源类指标须记录采集平台与档位」的纪律。
  5. **对 P1 唯一勉强可用的一点（术语层，非方法层）**：Sec. VI-B1 末段提出「把物理约束/模型驱动方法与数据驱动网络结合」，并举例 Ramos et al. [198] 在贝叶斯框架内融合语义与几何线索、Liang et al. [115] 用多任务学习加入物理约束。这只能作为**「把先验注入网络是已有方向」的一句话动机引用**，与 OTF 势场作为 ODE 边界条件的做法不是同一类机制，**不得据此声称 OTF-CfC 有先例支撑**。
- **不可迁移 / 陷阱**：
  - 本文的**全部定量数字（AP、mAP、IoU、fps、推理时间）都是转引他人结果**，且承载它们的 Tab. II–VI 在本 PDF 内不可见。**不得把本卡片或本文正文里出现的任何性能数字搬进 P1 的对比表**；如需引用须标「文献转引值，原表见 IEEE Xplore 附录，协议不同，不可直接比较」。
  - 本文**没有作者自己的实验、代码或数据**；"interactive online platform"（https://boschresearch.github.io/multimodalperception/）是文献导航页，**不是可复现代码/数据**，不得当作可复现材料计入 D5。
  - **ODD 不匹配**：本文实证场景为城市道路（KITTI 卡尔斯鲁厄城市、Cityscapes 城市街景），**与本项目高速公路主线 ODD 不重合**；按 AGENTS.md §5「跨 ODD 结论无效」，本文的任何结论都不得用于支撑 P1 的高速场景主张。
  - 本文的"鲁棒性"指**感知鲁棒性**（恶劣天气、传感器退化、开放集），与 P1 关心的控制鲁棒性/舒适性不是同一概念，术语不可混用。
  - 本文的 MoE 门控（式 1，wMi + wMj = 1 加权平均专家输出）**不是**可用于 P1 的控制融合机制，仅为感知特征融合算子；不要把它误读为「多模态决策融合」而类推到 P1 的 OTF 势场与控制器的融合。
- **引用时必须带的限定语**：本文为 2013–2019 年文献的感知层综述，实证场景为城市道路公开数据集（KITTI/Cityscapes 等），所引性能与推理时间均为转引他人报告值、协议与硬件互不相同、不可直接比较；其结论不覆盖高速公路主线多车道混行的纵横向闭环控制。

## 7. 缺失信息（≥3 条，写成可执行动作）

1. **附录 Tab. II–VI 表体与表题全部缺失**。正文共 6 处引用（行 146、435、535、537、1070、1432–1433），但提取文本在行 2453（参考文献 [251] 结束）后直接进入行 2454 起的作者简介，**附录未被 PDF 导出**。动作：到 IEEE Xplore 该文页面下载 supplementary downloadable material（正文第 71–79 行自述 "This article has supplementary downloadable material available at https://ieeexplore.ieee.org, provided by the authors."），补齐 Tab. IV（数据集清单：传感器、记录条件、规模、标签）与 Tab. V/VI（方法清单）后，再把数据集字段写进 P2 的数据集候选表；在补齐前，本卡片不得作为 P2 数据集字段的引用来源。
2. **Table I 只有表题 "AN OVERVIEW OF CHALLENGES AND OPEN QUESTIONS"，表格内容缺失**。动作：向 IEEE Xplore 取原页（p. 1350）核对该表条目，确认「挑战与开放问题」的完整列表；在拿到原表前，第 3 节的自承局限只能依据正文 Sec. VI/VII 的散落陈述，不能声称已穷尽 Table I。
3. **缺少交互式在线平台的可核验快照**。平台 https://boschresearch.github.io/multimodalperception/ 是本文声称的主要交付物之一，但卡片无法核验其当前内容与 2020 年版本是否一致（作者自述 "We plan to frequently update this tool"，即内容会漂移）。动作：取一次带日期的抓取快照（记录访问日期 + 页面版本或 commit），并注明「平台内容随时间变动，本记录日期为 X」。
4. **缺少数据集许可与再分发条款信息**。本文只列数据集名称与文献编号，未给出各数据集的许可类型。动作：对 P2 拟用的 nuScenes / Waymo 逐一到官方 Datasheets 核对许可与允许用途（与 auto-driving/AGENTS.md §2「遵守各自许可，不得再分发原始数据」对齐），不得依据本文推断许可。
5. **缺少作者本人对融合方案取舍的定量证据**。作者明确写 "we do not ﬁnd conclusive evidence ... that one fusion method is better than the others"，即本文**没有**给出 what/how/when to fuse 的定量结论。动作：若 P2 需要「条件模态注入位置」的经验依据，须另找带单因素消融（注入位置为唯一变量）的原始论文，不能引用本综述作为该结论的证据。
6. **缺少对 KITTI leaderboard 取数口径的完整说明**。Fig. 2 注明数据主要基于 KITTI leaderboard，"visited on Apr. 20, 2019"，且 "On the leader-board only the published methods are considered"。动作：若要引用 Fig. 2 的 AP–运行时间关系，须注明取数日期与「仅已发表方法」的筛选口径，并说明该榜单此后已变动。

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 综述覆盖的数据集年份范围 | 2013–2019 | — | Sec. I-B（"a summary of newly-published datasets (2013-2019)"） |
| 被综述数据集规模下界 | 1,569 frames | — | Sec. III-C 正文 "The dataset size ranges from only 1,569 frames up to over 11 million frames." |
| 被综述数据集规模上界 | over 11 million frames | — | Sec. III-C 正文（同上句） |
| 有真值标签的最大被综述数据集（作者自述） | nuScenes [88]，nearly 1,4M frames | — | Sec. III-C 正文（原文千位分隔符即为逗号，逐字为 "1,4M"） |
| 2014–2019 数据集规模增长 | 两个数量级（two orders of magnitudes） | — | Sec. III-C 正文 + Fig. 5(b) 图注 |
| KITTI 目标数 vs ImageNet 样本数 | 80,256 objects vs 1,034,908 samples | — | Sec. VI-A1 正文 "KITTI [6] records only 80,256 objects whereas ImageNet [162] provides 1,034,908 samples." |
| VoxelNet（Zhou and Tuzel [134]）推理时间 | 225 ms（KITTI 数据集） | 未报告 | Sec. V-A1 正文（**转引**他人结果：They report an inference time of 225 ms on the KITTI dataset） |
| SECOND（Yan et al. [137]）推理时间 | 25 ms | 未报告 | Sec. V-A1 正文（**转引**：achieving an inference time of only 25 ms） |
| 协同标注工具的标注加速比 | 30× labeling speed-up | 未报告 | Sec. VI-A1 正文（**转引** Lee et al. [174]）+ Fig. 10(a) |
| 参考年 2026 − 出版年 2021 = 年龄 | 5 年 | — | 本卡片据首部 "MARCH 2021" 与 DOI 年份 2020 取刊期年 2021（D4 记 2） |

**数字口径声明**：本表全部数值均为本文正文（非表格）印出的数字，其中 225 ms / 25 ms / 30× 明确为**转引**他人论文的结果，本文作者**未做独立实验、未报告不确定度**。Tab. II–VI 中的 AP/IoU/fps 明细因附录缺失**无法抄录**，不得由本卡片推测。

---

⚠内部不一致：正文 Sec. IV 开头称 "we show an overview of the existing methods in Tab. V and Tab. VI, and an accuracy and runtime comparison among several methods in Tab. II and Tab. III"，Sec. III 与 Sec. I 称数据集总览见 "Tab. IV in the appendix"，Sec. VI-B4 称 "Tab. II and Tab. III in the appendix summarize the inference speed"，但本 PDF 提取文本自参考文献 [251]（行 2453）后**直接进入作者简介（行 2454 起）**，**附录整体未被导出**，Tab. II–VI 的表题与表体均不可见——被引用的表在本文可读范围内不存在。

⚠内部不一致：行 1108–1109 出现表题 "TABLE I / AN OVERVIEW OF CHALLENGES AND OPEN QUESTIONS"，但行 1110 紧接着是 "A. Multi-Modal Data Preparation"（Sec. VI-A 正文），**表格本体缺失**，无法核对该表条目与正文 Sec. VI 的陈述是否一致。

⚠内部不一致：Fig. 5(a) 图注逐字写作 "nuScene dataset [88]"，而正文 Sec. III-C 与 Fig. 2 相关段落写作 "nuScenes Dataset [88]"；同一数据集在本文内名称不统一（图注为原文如此，非本卡片笔误）。
