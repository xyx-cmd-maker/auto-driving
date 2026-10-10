# TinyML 与端侧推理综述：应用、挑战与未来方向｜Tiny Machine Learning and On-Device Inference: A Survey of Applications, Challenges, and Future Directions

- **出处**：Sensors **2025, 25(10):3191**（MDPI；Received 28 February 2025 / Revised 2 April 2025 / Accepted 16 May 2025 / Published 19 May 2025）｜ **类型**：**综述**（MDPI 文章类型页眉逐字标注 "**Systematic Review**"）
- **作者**：Soroush Heydari, Qusay H. Mahmoud（**n=2**；Department of Electrical, Computer and Software Engineering, Ontario Tech University, Oshawa, ON, Canada）
- **DOI**：10.3390/s25103191（逐字；每页页脚复现）
- **全文来源**：`literature/fulltext/fresh2024/sensors2025-tinyml-survey__5e086a04.txt`（PAGES=23, CHARS=86,094 为题面给定值；**本机实测**：总字符 87,610（含 CRLF）／去换行 84,760，LINES=1,425，PAGE 分隔符 23 个）｜ **材料版本**：**出版社正式版（VoR）**。逐字证据：① "Copyright: © 2025 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license"；② 首页自引条目逐字 "Heydari, S.; Mahmoud, Q.H. Tiny Machine Learning and On-Device Inference: A Survey of Applications, Challenges, and Future Directions. **Sensors 2025, 25, 3191.** https://doi.org/10.3390/s25103191"；③ 每页页脚 "Sensors 2025, 25, 3191" + "N of 23"；④ 无 "preprint"／"author's version" 字样。【确定】
- **分组**：2024+ 增量
- **证据等级初判**：**C 级** — 自称系统综述且给出 PRISMA 流程图，但 **26 项纳入实验中有 22 项来自 6 篇综述的引文雪球**，只有 4 项来自一条检索式（且只扫前 100 条命中）；**无偏倚风险评估工具、无 meta 分析、无效应量、无注册**；其被引最多的定量边界（0–5 ms、95%→85%、49× 压缩）**均为二级转引**（逐字标注引自 [1] Abadade 等 2023 年的另一篇综述），**不是本文实测**；作者自承"只纳入成功实验，因此存在发表偏倚，可能高估 TinyML 能力"。**【确定】**
- **档位建议**：**B（略读）** — 加权 11 落 B 档（9–13）。**它不能替代 P1 缺失的"MCU 部署可行性"证据**（见 §6.2），其价值只在两处：① 提供 P1 资源类指标（MCU 内存占用／端到端延迟）的**可引用量级口径**（须标二级来源）；② 提供一条**负向证据**——在其语料中不存在 LNN/CfC/ODE 类模型的端侧案例。**【判断】**
- **五维打分（各维 0–2，满分 20）**：D1=1 D2=1 D3=1 D4=2 D5=1 → 加权 = 3·1+2·1+2·1+1·2+2·1 = 3+2+2+2+2 = **11**
  - D1=1：**不给 P1 所需的控制器/决策方法，也不是同 ODD 下的闭环控制评价协议**；它给的是 P1 相邻环节（部署与资源约束）的综述、术语与量级边界。按母协议 D1=1 档"提供动机、术语、基线候选或对照设计"判 1。
  - D2=1：**与母协议已评的两篇综述口径保持一致**（`meeting2/00-triage-protocol.md` §8.3 中 T-ITS 2022 DRL 综述与 T-ITS 2020 高速公路运动规划综述均给 D2=1）。综述本身无对照实验（非 2 分），但有明确纳入/排除标准与 PRISMA 流程图（高于"观点/无对照"）。
  - D3=1：可提供**资源约束量级口径**与**已部署硬件型号清单**（STM32 系列、nRF52、ESP32、ATMega2560、OpenMV STM32H7、Arduino Nano 33 BLE Sense、Raspberry Pi 4 + Coral Edge TPU、Jetson Nano），P1 可据此选 MCU 目标平台 → 部分迁移；但**无可复用数据/代码/协议**（Data Availability: "Not applicable"）。
  - D4=2：2025 年发表，≤5 年。
  - D5=1：VoR 全文 23 页 + 10 张结果表，但**无效应量、无 meta 分析、无可复现材料**，且**只纳入成功实验**（发表偏倚自承）。**D4 一律指时效性。**

## 1. 标题

原文标题（逐字）：**Tiny Machine Learning and On-Device Inference: A Survey of Applications, Challenges, and Future Directions** ｜ 中文直译：**微型机器学习与端侧推理：应用、挑战与未来方向综述**

## 2. 摘要（≤400 字）

本文是自称按 **PRISMA** 流程的 TinyML 端侧推理综述（MDPI 标注 "Systematic Review"）。作者从 **6 篇最新综述**出发，**由其引文雪球出 22 项实验**，再用一条检索式（命中 **2150 篇**、限 2021 年后 **1880 篇**、只扫前 **100** 条）**补入 4 项**，合计 **26 项端侧实验**（医疗 7、生态 9、车载检测 4、其他 2）。给出的定量边界（**均转引自其他综述**）：MCU 通常 **Flash <1 MB、SRAM 128–512 KB、主频 100–480 MHz**；云端推理时延 **10–500 ms**，TinyML **0.18–300 ms**（另称"低至 0–5 ms"）；量化把 **32/64 位浮点压到 8 位及以下**；剪枝可减 **13×**，压缩比可达 **49×**；功耗 **25–300 mW**（云端 50–1000 W）。作者自承三条局限：证据主要来自综述引文、各实验指标不统一、**只纳入成功实验因而存在发表偏倚**。

## 3. 结论（≤350 字）

作者结论：TinyML 已"从承诺走向实用"，在带宽受限、要求快速响应的场景优于云端推理；实验中最常见的选型理由是**降低推理时延**与**保护数据隐私**。研究缺口与未来方向：① 传感器—模型—硬件三者能力不匹配；② 缺乏标准化与基准（硬件从 Arduino Nano 到专用 TPU 高度异质）；③ 面向资源受限设备的训练方式与专用架构；④ 持续／联邦／迁移学习；⑤ 规模化部署下的能耗与安全。**⚠ 本卡另需提醒两点，作者未自承**：一是 **22/26 项证据来自 6 篇综述的引文雪球而非可复现检索**；二是**关键定量边界为二级转引**（引自 [1] Abadade 2023 综述）而非本文实测。此外正文与表格在 **0.17 W / 0.17 mW** 上不一致（见文末 ⚠ 清单）。

## 4. 方法一句话（≤60 字）

PRISMA 式综述：6 篇综述引文雪球出 22 项 + 1 条检索式补 4 项 = 26 项端侧实验的定性汇总。

## 5. 图表清单（占位符，覆盖全部图表）

全文共 **2 个 Figure + 10 个 Table**（合计 12 个，全部收录）。图注为逐字（截断到约 100 字符）。⚠ **本文没有任何性能对比图、没有任何原文实验数据图**——2 幅图分别是硬件示意与流程图，全部结果都以表格文字给出。

| 占位符 | 图/表号 | 原文图注（逐字） | 读图要点 |
|---|---|---|---|
| {FIG-TINYML-1} | Figure 1 | TinyML hardware schema from [1]. TinyML models are chosen based on the required task and the available hardware. The device must have sufficient memory to run the model and enough storage to store the trained model weights as well as the input data collected by the sensors. | **唯一的技术示意图，而且是转引 [1] 的**（"from [1]" 逐字在标题里）。说明 TinyML 的硬件约束三件套：**内存容纳模型 + 存储容纳权重 + 存储容纳传感器输入数据**。→ P1 写"MCU 内存占用"指标时可用它定义口径边界。 |
| {FIG-TINYML-2} | Figure 2 | PRISMA selection flowchart. | **本卡评估其方法学强度的关键图**：画出"6 篇综述 → 引文筛选"与"检索式 → 100 条扫描"两条支路如何汇成 26 项。**注意主支路是引文雪球，不是检索式。** |
| {TAB-TINYML-1} | Table 1 | Surveys cited in Sections 1 and 2. | 6 篇被用作背景的综述及其**被本文指出的不足**：[1] Abadade 2023（指出问题但不给解法）、[2] Capogrosso 2024（用例覆盖不足）、[3] Elhanashi 2024（性能解释不足）、[4] Tsoukas 2024（广度有限）、[5] Liu 2024（偏 edge inference 而非 TinyML）、[6] Ren 2022（仅限工业场景）。**⚠ [6] 的出版信息写成 "arXiv 2022, arXiv:2202.09113"——是预印本，不是期刊论文，被当作"state-of-the-art 综述"引用须注意。** |
| {TAB-TINYML-2} | Table 2 | Rejected older or narrower breadth surveys. | 排除 8 篇综述及理由（"out of date"／"covered by newer surveys"／"too limited"）。**排除理由全部是"旧/窄/被覆盖"这类主观判断，无日期阈值、无双向筛选记录。** |
| {TAB-TINYML-3} | Table 3 | Rejected experiments that used external inference. | 排除 6 项实验，理由均为"用了云端/外部 PC 推理"。**这是本文最硬的一条纳入标准（必须在嵌入式设备上推理），P1 若要在综述中证明"端侧"口径，可引此表。** |
| {TAB-TINYML-4} | Table 4 | Studies rejected for lack of stated use case. | 排除 3 项实验，理由为"提出了框架/加速器但没有用例"。 |
| {TAB-TINYML-5} | Table 5 | TinyML experiments chosen from surveys. | **22 项雪球来源实验一览**（年份 2020–2024）：助听器语音增强、帕金森步态、心律失常 ECG、癫痫、肝脏病变、癫痫无创监测、车辆 CO₂、温室温度、大气压预测、霍乱水质、车辆行人检测、公交乘客计数、蚊虫识别、驾驶员困倦、葡萄叶病害、植物生长、农业气体识别、路面异常、旋转机械故障、边缘设备安全、结肠息肉、UAV 智慧农业。**注意：其中 15 项（2020–2022）早于本综述的时间窗，属"旧实验"而非 2024+ 增量。** |
| {TAB-TINYML-6} | Table 6 | TinyML experiments chosen from search strings. | **仅 4 项**来自检索式：Ren 2021（工业 IoT 事件处理）、Abadade 2024（肺病分类）、Im 2024（车载网络入侵检测）、Bustamante 2023（工业边缘部署）。⚠ **其中 Ren [48] 与 Im [50] 在正文第 4 节从未被分析**（只出现在本表），见 ⚠清单 3。 |
| {TAB-TINYML-7} | Table 7 | Experiments that covered TinyML in healthcare. | 医疗 8 行结果：ECG 87% 准确率；癫痫 >90%；肝病变 80% 准确率 + **75 ms** 延迟；息肉 **92.8%** + **2.5488 mW**；肺病 **97%** 精确率/召回率 + **127 ms**。正文另给关键数字：助听器模型**剪枝 47%**、延迟 **4.26 ms**（基准要求 10 ms）；ECG 模型 **210 KB** 二进制、**95 ms** 延迟、**21 mW/h**；肺病模型 **12 KB RAM + 约 250 KB Flash + 127 ms**。**→ 这是全文最接近 P1"MCU 内存占用 + 端到端延迟"两项指标的一组数字。** |
| {TAB-TINYML-8} | Table 8 | Experiments that covered TinyML for ecology. | 生态 9 行：温室预测 **0.17 mW**（⚠ 正文写 **0.17 W**）；车辆排放 **94% + 1 ms**；大气压 **RMSE 0.0255 / 512 kB 内存**；霍乱 **94%**；蚊虫 **88.3% + 337 ms**；葡萄叶 **98.0% + 64.2 ms（15.5 fps）+ ~13 kB ROM**；植物生长 **136 kB**；气体 **72%**；UAV 土壤 **99%**。**⚠ 注意"fewer LSTM structures resulted in faster inference and less memory usage"——这是全文唯一与循环网络内存相关的结论，但没有给 LNN/CfC。** |
| {TAB-TINYML-9} | Table 9 | Experiments that covered TinyML usage in vehicular detection. | **车载类只有 4 项，且全部是感知/检测任务**：行人+车辆检测（Tiny YOLO v3 + Tucker 张量分解，精确率 **77.5%**，存储 **10.7 MB vs 875 MB**）、公交乘客检测（Tiny YOLO，文件 **60.5 MB → 7 MB**，准确率 0.945）、路面坑洼/减速带（F1 **0.76**）、驾驶员困倦（准确率 **0.9964**）。**→ 关键判定：本文语料中"车载 TinyML"= 感知，无一项做纵横向控制、无一项做编队/跟驰。** 正文另给平台：**Raspberry Pi 4 + Coral USB Accelerator（Edge TPU）与 NVIDIA Jetson Nano 2 GB** —— **⚠ 这两个都不是 MCU**。 |
| {TAB-TINYML-10} | Table 10 | TinyML experiments in other categories. | 其他 3 行：旋转机械异常（准确率 1.0，训练+推理均在 STM32 MCU：**1 MB RAM + 2 MB Flash**）、FPGA 上的恶意软件检测（J48 F1 **0.918**）、云端训练→边缘部署流水线（Kunbus 设备、Docker 内运行 **1.267 s**、>12000 请求/分钟）。**→ "边缘训练 + 边缘推理"的先例在此，可作 P1"在线自适应"的相邻引用（但任务不是控制）。** |

**合计**：Figure 2 个 + Table 10 个 = **12 个**（无补充材料、无附录、无补充图表；Data Availability Statement 逐字 "Not applicable"）。

## 6. 对 P1 的用处

- **与 P1 的关系**：**相邻（部署与资源约束环节），不是 P1 的控制器方法，也不是 P1 的 ODD。** 它不给任何车辆动力学、编队、跟驰或控制回路内容；它的 4 项"车载"实验全部是感知/检测。

### 6.1 特别要求逐条回答（任务 §3 第 3 篇的 ①②③）

**① 综述给出哪些可引用的定量边界？** —— **有，但必须全部标为"二级转引"。** 逐字抄录并标出处级别：

| 边界 | 数值（逐字） | 本文中的出处 | 一级/二级 |
|---|---|---|---|
| MCU Flash 上限 | "typically operating with **less than 1 MB of flash memory**" | §2.1（自述，无引用标记） | 本文自述 |
| MCU 硬件包络 | "most devices have clock frequencies ranging from **100 MHz to 480 MHz**, flash memory capacities **under 1 MB**, and SRAM sizes between **128 KB and 512 KB**" | §2.3（引 [1]） | **二级**（引自 Abadade 2023） |
| 主流内核 | "ARM Cortex-M series processors have become central to TinyML deployments, with **Cortex-M4** emerging as a popular choice" | §2.3（引 [1]） | **二级** |
| 云端 vs 端侧时延 | "cloud-based IoT solutions typically exhibit latencies in the range of **10–500 ms**, TinyML solutions can achieve latencies as low as **0–5 ms**… with only a slight decrease in accuracy from **95% to 85%**" | §2.1（引 [1]） | **二级** |
| 端侧推理时延区间（另一处口径） | "typically achieve inference latencies in the range of **0.18–300 ms**, which is significantly lower than the **10–500 ms** commonly observed in cloud-based solutions" | §2.4（引 [1]） | **二级**（**与上一行的 0–5 ms 口径不同，见 ⚠清单 1**） |
| 时延约束的可选阈值 | "Given low-latency constraints (**0.3 s or less**), on-device inference is comparable to on-server inference… As latency constraints become looser and reach **1.0 s**, on-server and cooperative inference shows more power efficiency" | §2.1（引 [5] Liu 2024） | **二级** |
| 时延改善倍数 | "latency reductions of up to **44.5×** compared to traditional cloud-based approaches" | §2.4（引 [1]） | **二级** |
| 量化位宽与精度损失 | "reducing the precision of weights and activations from **32-bit or 64-bit floating-point numbers to 8-bit or lower fixed-point representations**, thereby enabling significant memory savings while **preserving most of the model's accuracy**" | §2.2（引 [1]） | **二级**；⚠ **"most of the accuracy" 无任何数字** |
| 剪枝压缩倍数 | "techniques such as pruning can reduce the network size by **up to 13 times** without significant accuracy loss" | §2.2（无引用标记） | 本文自述；⚠ **"without significant accuracy loss" 无数字、无检验** |
| 整体压缩比 | "TinyML algorithms can achieve compression ratios of **up to 49×** while maintaining acceptable accuracy levels" | §2.2（引 [1]） | **二级** |
| 内存足迹削减 | "optimized models reduced their memory footprint **more than 90%** while preserving most of their inferential capabilities" | §2.2（"Other surveys provide examples"，无编号） | **二级**（且未指明来源） |
| 静态内存上限 | "static memory requirements for model storage (**typically limited to a few hundred kilobytes**)" | §2.4 | 本文自述 |
| 可部署 RAM 下限 | "deployment on devices with as little as **256 KB of RAM** while maintaining acceptable inference accuracy" | §2.4（引 [1]） | **二级** |
| 功耗 | "TinyML-optimized MCUs can achieve inference operations while using only **25–300 mW** of power"；"**25–300 mW** for TinyML implementations compared to **50–1000 W** for cloud-based processing" | §2.3、§2.4（均引 [1]） | **二级** |
| 加速器增益 | "These accelerators can achieve performance improvements of **up to 20 times** compared to standard MCU implementations" | §2.3（无引用标记） | 本文自述 |
| 传统 DL 内存需求 | "traditional deep learning models require **hundreds of megabytes** of memory" | §2.2；§2.4 复述 "hundreds of megabytes" | 本文自述 |
| 纳入实验的模型大小 | "Many of the experiments in this study attained accurate results with highly compressed models **below 1 MB in size**" | §5.1 | 本文对 26 项实验的汇总 |

**→ P1 可直接引用的三条（口径最干净）**：① **Flash <1 MB、SRAM 128–512 KB、主频 100–480 MHz** 作为"典型 MCU 包络"；② **量化 32/64 位 → 8 位及以下**作为位宽口径；③ **"模型存储通常限制在几百 KB"**作为静态内存口径。**其余全部要带"转引自 Abadade 2023 综述"的限定语。**

**② 有没有 LNN/CfC/ODE 类模型的端侧案例？** —— **没有。本卡已逐词核验，结论是明确的零命中。** 核验方式与结果：
- 对全文（含参考文献表）执行正则检索 `liquid|LTC|CfC|neural circuit|ordinary differential|ODE|differential equation|spiking|SNN|state-space model|Mamba|transformer|liquid time` → **0 命中**。
- 检索 `RNN` → **1 命中**，且是转述 [26] Fedorov 等的工作："found the optimized model satisfactory and a latency low enough to consider **pruned RNNs** for their task"（§4.1）。**该处用的是 LSTM 类递归网络，不是 LNN，也没给出参数量。**
- 检索 `LSTM` → **4 处实质命中**，全部是常规 LSTM：① [26] TinyLSTMs（助听器语音增强，**剪枝 47%、延迟 4.26 ms**、STM32）；② [34] Alongi 等（**2 个 LSTM 单元 × 每单元 30 单元**，dropout 20%，STM32F401RET6 **512 KB Flash + 96 KB SRAM**，RMSE **0.0255**）；③ [47] Hayajneh 等（DNN + LSTM 于 ESP32 跑 TFLM，**97% 准确率 + 97.8 ms**）；④ Table 8 结论行 "fewer LSTM structures resulted in faster inference and less memory usage"。
- **→ 结论：本篇综述（**截止 2025 年 5 月**）的 26 项纳入实验语料中，不存在任何液态神经网络（LTC/CfC）、神经常微分方程（neural ODE）或脉冲神经网络（SNN）的端侧部署案例。** 这对 P1 是**重要信息**：它意味着 ① P1 的"LNN/CfC 上 MCU"主张在 2025 年中的 TinyML 综述语料里**没有先例可引**，因此**不能**用"综述已收录 LNN 端侧案例"这类措辞；② 也意味着 P1 若做成，**相对该综述语料是净增量**（但**这不等于文献中没有**——见 §6.2 的边界说明与 §7 缺失信息 5 的取代检查动作）。
- ⚠ **口径限定**：本结论的适用范围**仅限这篇综述的纳入语料**，不构成"文献中不存在 LNN 端侧工作"的全称断言。已知的反例边界：`meeting2/notes/ral2022-interpretable-flight-ncp.md` 记录 Tylkin 等（RA-L 2022）把 NCP（**LTC 细胞、需 ODE 求解器**）压缩为 **TFLite ≈170 KB** 并在 **Raspberry Pi Zero** 上实时推理——**那是一项 LNN 家族的端侧工作，但既不在本综述的语料内，也不是 MCU**。（注意：RA-L 2022 早于本综述"2021 年后"的检索窗下限吗？不早于——检索式那条只扫 2021 年后，但它属于检索式支路；RA-L 2022 未被纳入，说明该支路的召回明显不足。）

**③ 它的检索协议（是否系统综述、检索式、纳入标准）** —— 逐字给出：
- **自称与遵循的指南**："This review was carried out using the guidelines for systematic literature reviews [7] and **PRISMA guidelines [8]**."（[7] = Kitchenham 2007；[8] = Moher 等 PRISMA 2009）。MDPI 类型标注为 "**Systematic Review**"。**但全文没有 PRISMA 检查表、没有检索日期、没有注册号（无 PROSPERO）、没有偏倚风险评估、没有 meta 分析。**
- **信息源**："we found recent TinyML literature reviews by searching in **Google Scholar, IEEE Explore, and ACM Digital Library** using the search string "**TinyML Survey**", prioritizing the latest survey papers in the field."（⚠ "IEEE Explore" 为原文拼写，应为 IEEE Xplore，全文 3 处一致地写错。）
- **主证据支路（22/26）**："Overall, **22 papers** on TinyML experiments that met the eligibility criteria described in Section 3.3 were chosen for analysis, **which were taken from citations of the six comprehensive surveys examined**." → **这是引文雪球（citation harvesting），不是检索。**
- **补证据支路（4/26）**：检索式逐字 "("instantaneous inference" OR "real-time") (TinyML OR "Edge AI") "implement"—review"，入口 **Google Scholar**；"This string returned **2150 studies**, which were filtered to **1880 studies** by limiting the results to studies released **since 2021**. The **first ten pages** consisting of the **top 100 hits** were scanned." → **只读了排名前 100 条命中。**
- **纳入/排除标准（§3.3 逐条）**：**Relevance**（须能回答 RQ 之一；实验须描述 ML 框架、硬件与用例）；**Language**（仅英文）；**Publication Type**（仅同行评议期刊与会议论文，来源数据库为 IEEE Explore / ACM DL，"and references cited within those papers"）；**Repetition**（只收更新的综述）；**On-Device Inference**（"Chosen experiments had to carry out inference from an **embedded device** to be considered as TinyML. Studies that used external cloud-based or server-hosted inference models were **excluded**."）；**Usability**（"Experiments that proposed a machine learning framework **without also including a use case example** were excluded."）。
- **排除记录**：Table 2（8 篇综述）、Table 3（6 项外部推理实验）、Table 4（3 项无用例研究）——**有排除清单，但无"排除后再做敏感性分析"，也未报告检索者数量与一致性（无 κ）**。
- **研究问题**：RQ1 "What is TinyML's performance in a real-world low-latency application?"；RQ2 "For which use cases could TinyML on-device inference prove optimal?"。**范围声明**："The scope of the research is **inference, not training**."
- **→ 评估**：**是"自称的系统综述"，但主证据链是雪球式而非可复现检索**，因此**不满足**"可复现多源检索协议 + 检索日志"这一本机标准（全局 `AGENTS.md` §2.1 共用硬约束第 4 条）。P1 引用它时，**必须写成"该综述汇总的 26 项实验"，不得写成"系统检索得到的证据"**。

### 6.2 ★ 这篇能不能替代 P1 目前缺失的"MCU 部署可行性"证据？如果不能，缺的是什么？

**结论先行：不能替代。** 它既不是关于 CfC/LNN 的证据，也不是关于 P1 控制任务的证据，更不是 P1 需要的"实测"证据。

**它能供的三样东西（有限但真实）**：
1. **可引用的量级口径**（见 §6.1① 表）：MCU 包络（Flash <1 MB、SRAM 128–512 KB、100–480 MHz）、量化位宽（→8 位及以下）、静态内存口径（几百 KB）、时延量级（0.18–300 ms）、功耗（25–300 mW）。→ P1 在写"本方法的资源占用**落在典型 MCU 包络之内/之外**"时，可引本综述定义包络，**但所有数值必须标"转引自该综述所引的 [1] Abadade 2023"**。
2. **一条负向证据**：在其 26 项端侧实验语料中**没有 LNN/CfC/neural-ODE/SNN 案例**（见 §6.1②）。→ 这可以支撑 P1 写"**在我们检索到的端侧推理综述语料中，连续时间神经网络尚无端侧案例**"这样**有范围限定**的表述（**不能**写成"文献中没有"）。
3. **一份可照抄的硬件/任务对照清单**：STM32F401RET6（512 KB Flash/96 KB SRAM）、STM32L476、STM32H7（OpenMV Cam）、STM32（1 MB RAM + 2 MB Flash）、nRF52（Cortex-M4）、ATMega2560、ESP32、Arduino Nano（256 KB RAM）、Arduino Nano 33 BLE Sense、BioWolf 可穿戴、Raspberry Pi 4 + Coral Edge TPU、Jetson Nano 2 GB、Pixel 4、Kunbus、FPGA。→ P1 选 MCU 目标平台与做"对照平台"时，这是现成的**已被同行评议收录过的平台集合**。

**它缺的（也就是 P1 真正缺的）—— 按缺口大小排序**：
1. **缺"LNN/CfC 本体"的端侧实测**。综述里的递归网络案例全是 LSTM/RNN；**没有任何一篇给出 CfC 或 LTC 的参数量、量化档位、RAM/Flash 占用或单步时延**。→ P1 的"MCU 内存占用"指标**必须自测**；外部可引的最近锚点仍是 `meeting2/notes/ral2022-interpretable-flight-ncp.md` 记录的 **RA-L 2022 NCP：TFLite ≈170 KB + 预处理器 ≈10 KB，Raspberry Pi Zero 上 10→>30 FPS**（**口径是 TFLite 部署产物字节数，不是参数量；平台是单板机，不是 MCU**）。
2. **缺控制回路的时延与抖动**。综述统计的全是"**推理**时延"（inference latency），且明写 "The scope of the research is inference, not training"；**没有任何一项给出"感知→推理→执行器"的端到端闭环时延或抖动（jitter）**。→ P1 的"端到端延迟"指标在本综述**零证据**。
3. **缺车规/功能安全维度的任何信息**。全文无 AEC-Q100、ISO 26262、ASIL、SOTIF、UL 4600 等词（`AGENTS.md` §4 允许引术语与思路，但**本文连术语都不提供**）。
4. **缺"控制任务"的端侧案例**。4 项车载实验全部是检测（行人/乘客/坑洼/困倦），**无一项闭环控制**。
5. **缺可复现性**。Data Availability Statement 逐字 "Not applicable"；**无检索日志、无数据、无代码**。→ P1 无法据此复算任何数字。

**→ 给 P1 的措辞上限（建议）**：
> 可写："在 Heydari & Mahmoud 的 TinyML 端侧推理综述中（*Sensors* 2025;25(10):3191），26 项纳入实验的典型 MCU 包络为 Flash <1 MB、SRAM 128–512 KB、主频 100–480 MHz（**转引自该综述所引的 Abadade 等 2023 综述**），车载类端侧工作全部为感知/检测任务，且**其语料中不存在液态神经网络、神经常微分方程或脉冲神经网络的端侧案例**。"
> **不可写**："该综述表明 CfC/LNN 可以在 MCU 上运行"、"该综述给出了 LNN 的端侧时延"、"该综述证明端侧推理能满足 100 Hz 控制"、"系统检索的文献中不存在 LNN 端侧工作"。

### 6.3 可迁移

1. **★ "端侧"的判定标准（P1 可直接引的硬规则）**：必须是"在嵌入式设备上完成推理"（"carry out inference from an embedded device"），**用云端或外部 PC 推理的一律排除**（Table 3 列了 6 项被排除的例子）。→ P1 若要声称"端侧部署"，**必须报告推理发生在哪块芯片上、用什么运行时**；本文给出了这条界线的已发表版本。
2. **四项资源指标的成套报告口径**："The **four most common metrics** are the **model accuracy, inference latency, memory utilization, and power consumption**"，并强调"improvements in one dimension often requiring tradeoffs in others"。→ P1 的七项指标中的"MCU 内存占用"与"端到端延迟"正落在这四项里，**报告时宜同时给功耗与精度损失**（否则会被问"是不是拿精度换的"）。
3. **量化位宽的报告写法**："from 32-bit or 64-bit floating-point numbers to **8-bit or lower** fixed-point"——**写明"从什么到什么"**。→ `AGENTS.md` §1 的参数量红线要求"若必须写 <500 KB 须写明量化精度"，本文的口径正是这个要求的范式。
4. **模型大小 vs 内存占用要分开报**：综述反复区分"static memory requirements for model storage"与"dynamic memory needed during inference"。→ P1 的"MCU 内存占用"必须拆成 **Flash（权重）+ RAM（激活/峰值）** 两项，**不能合并成一个数**。
5. **平台型号清单**（见 §6.2 第 3 条）：P1 选"目标 MCU + 对照单板机"时的候选集合。
6. **"边缘训练 + 边缘推理"的先例**（§4.4 + Table 10）：[44] Mostafavi & Sadighi 在 **STM32（1 MB RAM + 2 MB Flash）** 上完成数据采集、训练与推理，用 **Wavelet Packet Decomposition** 降维以适配 MCU 内存，用 C 实现反向传播、**顺序训练**以规避存储限制。→ 若 P1 将来要做"在线/增量自适应"，这是端侧训练的先例（**但任务不是控制**）。
7. **诚实的局限写法**：§5.2 三条自承（证据来自综述引文、指标不统一、只纳入成功实验故有发表偏倚）可直接作为"综述类引用必须带限定语"的范例。

### 6.4 陷阱 / 不可迁移

1. **⚠ 它不是真正的系统综述**：主证据（22/26）来自 6 篇综述的引文；补证据只扫了 Google Scholar 前 100 条命中；**无检索日期、无注册、无 κ、无偏倚风险评估、无 meta 分析**。→ 引用时**不能写"系统检索表明"**。
2. **⚠ 关键数字是二级转引**：0–5 ms、95%→85%、49×、13×、25–300 mW、100–480 MHz、128–512 KB 等**绝大多数标注引自 [1]（Abadade 等 2023，IEEE Access）**。**P1 若要用这些数字，正确做法是引原始综述 [1]，而不是引本篇。**
3. **⚠ 两处时延口径自相矛盾**：§2.1 说 TinyML 时延"as low as **0–5 ms**"，§2.4 说"typically achieve inference latencies in the range of **0.18–300 ms**"——**两处都标引自 [1]**，但区间相差近两个数量级（0 与 300 不能同时是"典型"）。见 ⚠清单 1。
4. **⚠ 实测值区间很宽，且与"典型包络"张力明显**：其 26 项实验里，**时延从 1 ms 到 1.6 s**（[32] 车辆排放 1 ms vs [46] 息肉检测 1.6 s）、**准确率从 72% 到 99%**、**功耗 0.17 mW~21 mW**（口径还互相冲突）。→ **不能把"TinyML 能做到 X"当作任何单一数值的保证**；P1 引"MCU 可行性"必须给**任务条件**。
5. **车载 ≠ 控制，MCU ≠ 车载计算平台**：4 项车载实验**全部是感知**；其中 [36] 用的是 **Raspberry Pi 4 + Coral Edge TPU 与 Jetson Nano 2 GB**（**单板机/加速器，不是 MCU**）。→ **不得把本文当作"车辆控制可端侧运行"的证据。这是本卡最重要的陷阱。**
6. **发表偏倚自承**："only successful experiments were included and analyzed… may lead to an overestimation of TinyML implementation capabilities"。→ 本文给出的任何"可行性"结论**系统性偏乐观**。
7. **【确定】参数量/模型大小两个量纲不被区分**：综述通篇混用"model size / memory footprint / flash usage / storage cost / ROM"，**单位从 kB 到 MB 跳变**（如 [40] ~13 kB ROM、[35] 1.6 KB RAM + 15 KB Flash、[36] 10.7 MB storage、[44] 2 MB flash、[41] 136 kB model）。→ 与 `AGENTS.md` §1 的"参数量 vs 部署产物字节数"红线直接相关：**P1 不能从本文推出任何"参数量"表述**。
8. **"TinyML"的定义边界本文自定**：只要求"推理在嵌入式设备上"，**未给 MCU 的主频/内存硬阈值**（"less than 1 MB flash"是描述性而非判定性）。→ 引"TinyML"标签时须说明用的是本文口径还是别的口径。
9. **参考文献 [36] 的出版信息可疑**：逐字 "In Proceedings of the IEEE Transactions on Intelligent Transportation Systems, Edmonton, AB, Canada, 24–27 September 2024"。**把期刊名（IEEE T-ITS）与会议地点/日期并列在同一个 "Proceedings" 条目里**——按地点与日期判断，该文更像是 **IEEE ITSC 2024（Edmonton，2024-09-24~27）的会议论文**而非 T-ITS 期刊论文。**引用前必须回原库核对**（`[待核实]`）。

### 6.5 引用限定语（一句，含范围/来源边界）

> 在 Heydari & Mahmoud 关于 **TinyML 与端侧推理**的综述中（*Sensors* 2025;25(10):3191，MDPI 类型标注 "Systematic Review"），其 26 项端侧实验由 **6 篇综述的引文雪球（22 项）** 与一条 Google Scholar 检索式的前 100 条命中（4 项）汇总而成，**并非可复现的系统检索**；综述给出的典型 MCU 包络（Flash <1 MB、SRAM 128–512 KB、主频 100–480 MHz、量化至 8 位及以下、模型存储通常数百 KB）**绝大多数转引自该综述所引的 Abadade 等 2023 年综述而非本文实测**；其 4 项车载端侧工作**全部为感知/检测任务**（行人车辆检测、公交乘客计数、路面坑洼、驾驶员困倦），**平台包含 Raspberry Pi 4 + Coral Edge TPU 与 Jetson Nano 2 GB 等非 MCU 设备**；**该综述语料中不存在液态神经网络（LTC/CfC）、神经常微分方程或脉冲神经网络的端侧案例**，也**不提供任何控制回路的端到端时延或车规/功能安全信息**；作者自承只纳入成功实验因而**存在发表偏倚、可能高估 TinyML 能力**；该综述**无数据或代码共享**（"Not applicable"）。

## 7. 缺失信息（≥3 条，写成可执行动作）

1. **需取回其关键数字的一级来源**：[1] Abadade, Y.; Temouden, A.; Bamoumen, H.; Benamar, N.; Chtouki, Y.; Hafid, A.S. *A Comprehensive Survey on TinyML*. **IEEE Access 2023, 11, 96892–96922**（本文参考文献 1）。请核对 0–5 ms、95%→85%、49×、13×、25–300 mW、100–480 MHz、128–512 KB、0.18–300 ms 这些数字在 [1] 中的原始出处（它们是 [1] 自己的实测，还是 [1] 又转引了别人？）。（后果：**在那之前，这些数字不能作为"MCU 包络"的证据写进 P1 稿件；本卡已按二级来源标注。这是本卡最重要的一条。**）
2. **需作者澄清两处时延口径**：§2.1 "as low as **0–5 ms**" 与 §2.4 "typically…**0.18–300 ms**" 为何相差近两个数量级？各自对应什么任务与硬件？是否一个是"最佳案例"、一个是"典型区间"？（后果：**P1 若引"端侧时延 0–5 ms"，等于把最佳案例当典型值。**）
3. **需作者澄清 0.17 W / 0.17 mW 与两处功率单位**：Table 8 写 "extremely low power constraints of **0.17 mW**"，§4.2 正文写 "used only **0.17 W** of power compared to the base model which used **3.5 W**"。二者相差 1000 倍。（后果：**该数字在澄清前不可引用。**）
4. **需作者说明 [48]（Ren 2021）与 [50]（Im 2024）为何只出现在 Table 6 而未被第 4 节分析**：26 项纳入实验中至少 2 项（工业 IoT 事件处理、车载网络入侵检测）在 Findings 章无对应段落。（后果：**"26 项实验"这一计数与实际被综合的项数不符；P1 若写"该综述综合了 26 项实验"，严格说应为"纳入 26 项、讨论了 24 项"。**）
5. **需做 T2 取代检查（本卡未做，标 `[待核实]`）**：检索 **2025 年 5 月之后**是否存在 ① **CfC/LTC/神经 ODE 在车规 MCU（如 S32K、TC3xx、RH850、STM32H7）上的实测部署**（含量化档位、RAM/Flash、单步时延）；② 面向**车辆纵横向闭环控制**（而非感知）的 MCU 端侧网络；③ 对该综述"语料中无 LNN 端侧案例"这一判断的反例。动作：OpenAlex + Crossref + arXiv（`Liquid neural network` / `closed-form continuous-time` / `neural ODE` × `microcontroller` / `MCU` / `TinyML`），**记录检索式、日期与命中数**（`00-scope.md` §2.3 要求）。**若 ① 存在，P1 的"可上 MCU"应改引该文，本综述与 RA-L 2022 都退为背景。**
6. **需核验参考文献 [36] 的真实出版载体**：确认 Falaschetti 等 2024 的车辆/行人检测工作是 **IEEE T-ITS 期刊论文**还是 **IEEE ITSC 2024 会议论文**（Edmonton，2024-09-24~27）。（后果：**venue 写错即引用失实**，与 `AGENTS.md` §6 的"引用版本纪律"直接冲突。）
7. **需核对"车载 TinyML"是否真的只有 4 项**：本文的检索式支路只扫了前 100 条命中、且排除了"无用例"与"外部推理"；**很可能漏掉大量车载端侧控制工作**。→ 动作：以 OpenAlex 另行检索 `TinyML`/`microcontroller` × `lateral control`/`longitudinal control`/`path tracking`，与本文的 4 项比对。（后果：**P1 若据本文写"车载端侧工作都是感知"，属基于不完整检索的全称断言。**）
8. **需确认本文是否被更正或撤稿**：Crossref `api.crossref.org/works/10.3390/s25103191` 的 `update-to` 字段（**本卡未查**，标 `[待核实]`）。

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| 纳入实验总数 | **26**（雪球 **22** + 检索式 **4**） | — | §3.5；Table 5、Table 6 |
| 分类计数（雪球 22 项） | 医疗 **7**、生态 **9**、车载检测 **4**、其他 **2** | — | §3.5 |
| 检索式与命中 | `("instantaneous inference" OR "real-time") (TinyML OR "Edge AI") "implement"—review`；**2150** 篇 → 限 2021 年后 **1880** 篇 → 扫前 **10 页 / 前 100 条** → 取 **4** 项 | — | §3.5 |
| 起始综述检索 | Google Scholar / IEEE Explore / ACM DL，检索式 "**TinyML Survey**"，取 **6** 篇综述 | — | §3.2 |
| 排除记录 | 综述 **8** 篇；外部推理实验 **6** 项；无用例研究 **3** 项 | — | Table 2、Table 3、Table 4 |
| MCU Flash 上限 | **< 1 MB**（典型） | — | §2.1 |
| MCU 硬件包络 | 主频 **100–480 MHz**；Flash **<1 MB**；SRAM **128–512 KB** | — | §2.3（引 [1]） |
| 主流内核 | **ARM Cortex-M4** | — | §2.3（引 [1]） |
| 云端 vs 端侧时延 | 云端 **10–500 ms**；TinyML **低至 0–5 ms** | — | §2.1（引 [1]） |
| 端侧时延（另一口径） | **0.18–300 ms** | — | §2.4（引 [1]） |
| 精度代价（该处） | **95% → 85%** | — | §2.1（引 [1]） |
| 时延约束阈值 | **≤0.3 s** 时端侧与服务器/协同推理相当；放宽到 **1.0 s** 时服务器/协同更省电 | — | §2.1（引 [5]） |
| 时延改善倍数 | 最高 **44.5×** | — | §2.4（引 [1]） |
| 量化位宽 | **32/64 位浮点 → 8 位及以下定点** | 精度损失仅写 "most of the model's accuracy"，**无数字** | §2.2（引 [1]） |
| 剪枝压缩 | 网络规模最大减 **13×**（"without significant accuracy loss"，无数字） | 未报告 | §2.2 |
| 整体压缩比 | 最高 **49×** | 未报告 | §2.2（引 [1]） |
| 内存足迹削减 | **>90%** | 未报告 | §2.2（未指明来源） |
| 静态内存上限 | 模型存储"**typically limited to a few hundred kilobytes**" | — | §2.4 |
| 可部署 RAM 下限 | 低至 **256 KB RAM** | — | §2.4（引 [1]） |
| 传统 DL 内存需求 | **数百 MB** | — | §2.2；§2.4 |
| 功耗（端侧 vs 云端） | **25–300 mW** vs **50–1000 W** | — | §2.3、§2.4（引 [1]） |
| 加速器增益 | 最高 **20×**（相对标准 MCU 实现） | — | §2.3 |
| 26 项实验的模型规模（综述汇总） | 多数"**below 1 MB**" | — | §5.1 |
| 医疗类时延（综述汇总） | 多在 **~100 ms**；复杂诊断（癌变）**1–2 s** | — | §4.1 末 |
| 医疗类准确率（综述汇总） | **80–99%** | — | §4.1 末 |
| 生态类时延（综述汇总） | **0.1–1 s** | — | §4.2 末 |
| 生态类准确率（综述汇总） | **72%**（复杂气体分析）~ **98%**（简单图像分类） | — | §4.2 末 |
| 车载检测类准确率（综述汇总） | 约 **76–78%**（作者自评"indicating a need for improvement"） | — | §4.3 末 |
| 助听器语音增强（[26]，STM32） | 模型剪枝 **47%**；延迟 **4.26 ms**（基准要求 10 ms） | 未报告 | §4.1 |
| ECG 心律失常（[28]，nRF52/Cortex-M4，CMSIS-NN） | 准确率 **87%**；二进制 **210 KB**；延迟 **95 ms**；功耗 **21 mW/h** | 未报告 | §4.1 |
| 肝病变（[30]） | 准确率 **80%**；延迟 **75 ms** | 未报告 | §4.1；Table 7 |
| 癫痫（[29]，STM32L476） | 准确率 **>90%**；低误报率 | 未报告 | §4.1 |
| 结肠息肉（[46]，MCR 内 MCU，四层 CNN） | 准确率 **92.8%**；功率 **2.5488 mW**；主频 **8 MHz**；推理延迟 **1.6 s** | 未报告 | §4.1 |
| 肺病分类（[49]，Arduino Nano + Arm Cortex，TFLM） | 准确率 **96%**；精确率/召回率 **97%**；推理 RAM **12 KB**；Flash **约 250 KB**；推理时间 **127 ms** | 未报告 | §4.1；Table 7 |
| 温室温度预测（[33]，Arduino Nano 33 BLE Sense） | **0.17 mW**（Table 8）／**0.17 W**（正文，⚠ 冲突）；基线模型 3.5 W | 未报告 | Table 8；§4.2 |
| 车辆排放（[32]，ESP32 / Freematics ONE+，TEDA 无监督） | 准确率 **94%**；推理时间 **约 1 ms**；RAM **1.5 KB** | 未报告 | §4.2；Table 8 |
| 大气压预测（[34]，STM32F401RET6；2×LSTM×30 单元、dropout 20%） | **RMSE 0.0255**；硬件 **512 KB Flash + 96 KB SRAM** | 未报告 | §4.2；Table 8 |
| 霍乱水质（[35]，ARM Cortex-M4 离线套件，SVM） | 准确率 **94%**；延迟 **1 ms**；RAM **1.6 KB**；Flash **15 KB** | 未报告 | §4.2；Table 8 |
| 蚊虫识别（[38]，Arduino Nano） | 准确率 **88.3%**；推理 **337 ms**；RAM **9.2 kB**；Flash **43.4 kB**（1 秒数据） | 未报告 | §4.2；Table 8 |
| 葡萄叶病害（[40]，OpenMV Cam STM32H7 Plus） | 准确率 **98.0%**；**64.2 ms/图（15.5 fps）**；**~13 kB ROM**（相机 RAM 31 kB） | 未报告 | §4.2；Table 8 |
| 植物生长（[41]，电池供电 Sony 相机） | 模型 **136 kB**（<140 kB）；准确率 **96%**（10 类）；功耗 **约 2.63 mW/小时** | 未报告 | §4.2；Table 8 |
| 农业气体（[42]，STM32 + XCubeAI） | 准确率 **72%**；18 个测试样本中 **5 个分类错误** | 未报告 | §4.2；Table 8 |
| UAV 土壤湿度（[47]，ESP32 + TFLM，DNN+LSTM） | 准确率 **97%**；平均推理 **97.8 ms** | 未报告 | §4.2；Table 8 |
| 车辆/行人检测（[36]，**Raspberry Pi 4 + Coral USB Edge TPU / Jetson Nano 2 GB**） | 精确率 **77.5%**；内存占用为基线的 **22–32%**；存储 **10.7 MB vs 875 MB** | 未报告 | §4.3；Table 9 |
| 公交乘客检测（[37]，Tiny YOLO） | 准确率 **0.945**（高峰时段）；文件 **60.5 MB → 7 MB** | 未报告 | §4.3 |
| 路面坑洼/减速带（[43]，Arduino Nano） | F1 **0.76–0.78** | 未报告 | §4.3；Table 9 |
| 驾驶员困倦（[39]，量化轻量 DL） | 准确率 **0.9964** | 未报告 | §4.3；Table 9 |
| 旋转机械异常（[44]，STM32：**1 MB RAM + 2 MB Flash**，小波包分解 + 自编码器，端侧训练） | 训练准确率 **0.997**（3400 样本中 1 个假正）；测试 **100 样本准确率 1.0**；作者自评"100 tests on only one machine may be insufficient" | 未报告 | §4.4；Table 10 |
| FPGA 恶意软件检测（[45]） | J48 最高 **F1 0.918** | 未报告 | §4.4；Table 10 |
| 云端训练→边缘部署流水线（[51]，Kunbus + Docker） | 运行 **1.267 s**；构建镜像 **457.4 s**；部署合计 **约 38 s**；吞吐 **>12,000 请求/分钟** | 未报告 | §4.4；Table 10 |
| 数据集/代码可用性 | **无**（"Not applicable"） | — | Data Availability Statement |
| 资助 | 加拿大 **NSERC** | — | Funding |
| 论文时间线 | Received **28 February 2025**；Revised **2 April 2025**；Accepted **16 May 2025**；Published **19 May 2025** | — | 首页 |

**⚠内部不一致（逐条列出，引用前必须处理）**

- ⚠内部不一致 1（**最关键**）：**两处端侧时延区间自相矛盾且同引一个来源**。§2.1 逐字："TinyML solutions can achieve latencies as low as **0–5 ms** for inference tasks… [1]"；§2.4 逐字："Surveys of TinyML implementations show that they typically achieve inference latencies in the range of **0.18–300 ms**… [1]"。**同引 [1]，但"低至 0–5 ms"与"典型 0.18–300 ms"相差近两个数量级**；引用任一数字前必须澄清其"典型/最佳"口径。
- ⚠内部不一致 2：**功率单位冲突**。Table 8 逐字 "Greenhouse temperature forecasting successfully implemented under extremely low power constraints of **0.17 mW**"；§4.2 正文逐字 "The resulting experimental model used only **0.17 W** of power compared to the base model which used **3.5 W**"。**相差 1000 倍。**
- ⚠内部不一致 3：**纳入 26 项，但第 4 节只讨论了其中 24 项**。Table 6 列入 **Ren, H. [48]（2021，工业 IoT 事件处理）** 与 **Im, H. [50]（2024，车载网络入侵检测）**，但第 4 节（含 Table 7–10）**从未出现 [48] 或 [50]**（全文检索仅命中 Table 6 两行）。→ "综合了 26 项实验"这一表述与实际被综合的项数不符。
- ⚠内部不一致 4：**易混的"内存/存储"口径未被区分**。§4.3 逐字："using a much smaller **memory size (22 to 32%)** compared to their baseline model, and a **storage cost of 10.7 MB compared to an 875 MB** solution"——**22–32% 与 10.7/875 MB（=1.2%）不是同一口径**；读者无法判断"22–32%"指的是内存、参数还是别的量。
- ⚠内部不一致 5：**"剪枝 13×"与"压缩 49×"无来源标注、且与"内存减 >90%"三种口径并列**：§2.2 同一段里，"pruning can reduce the network size by up to **13 times** without significant accuracy loss"（无引用标记）、"compression ratios of up to **49×**"（引 [1]）、"optimized models reduced their memory footprint **more than 90%**"（"Other surveys provide examples"，无编号）。**三者不可互相换算，也不可叠加。**
- ⚠内部不一致 6（**参考条目**）：**参考文献 [36] 的载体可疑**。逐字："Falaschetti, L.; Manoni, L.; Palma, L.; Pierleoni, P.; Turchetti, C. Embedded Real-Time Vehicle and Pedestrian Detection Using a Compressed Tiny YOLO v3 Architecture. **In Proceedings of the IEEE Transactions on Intelligent Transportation Systems, Edmonton, AB, Canada, 24–27 September 2024**; IEEE: New York, NY, USA, 2024; pp. 1–16."——**把期刊名与会议地点/日期写进同一个 Proceedings 条目**；按地点与日期判断应为 **IEEE ITSC 2024 会议论文**。**引用前必须回原库核对载体（`[待核实]`）。**
- ⚠内部不一致 7（**数据库名拼写**）：全文 **3 处**把 IEEE Xplore 写成 "**IEEE Explore**"（§3.2 两处、§4 前一处）。**引用其检索协议时须照录原文拼写或加 [sic]。**
- ⚠内部不一致 8（**转引层级未标**）：由 [1] 等综述转引的数字（0–5 ms、95%→85%、49×、25–300 mW 等）在正文中**只写引用编号，未说明是"某实验的实测值"还是"另一篇综述的汇总值"**；而 Table 1 又明确把 [1] 标为"does not suggest how to solve them"的综述。→ **读者极易把这些数字误当本文的实测汇总。**
- ⚠内部不一致 9（**预印本被当期刊综述引用**）：Table 1 收录的 [6] Ren 等 2022 出版信息为 "**arXiv 2022, arXiv:2202.09113**"，属预印本；而 §3.2 声称选取的是"peer-reviewed journals and conference papers"且"Older surveys were considered out of date and excluded"。→ **纳入标准与实际纳入情况不一致**，且按 `00-scope.md` §2.2 的预印本口径该条应降档。
- ⚠内部不一致 10（**表内人名拼写**）：**Table 8 写 "Hayajineh, A. [47]"，而 Table 5 与参考文献 47 均写 "Hayajneh, A.M."**（本机 grep `Hayaj` 命中 3 处：L583 = Hayajneh、L802 = Hayajineh、L1408 = Hayajneh）。→ 转引该条工作时须以参考文献表拼写为准。

**字数实测（口径：该节内去除全部空白与 Markdown 标记 `# * \` | > \ -` 后的字符数，含中英文标点）**：§2 = **359 字**（上限 400）；§3 = **298 字**（上限 350）；§4 = **45 字**（上限 60）。**【确定，本机 PowerShell 脚本实测，测量式：`$s -replace '\s','' -replace '[#*`|>\\-]',''`】** ⚠ 若三节中有任何一节在后续编辑中变动，须重测并更新本行。

【确定】/【待核实】标注：以上引文、表格数字与两次零命中检索（`liquid|LTC|CfC|neural circuit|ordinary differential|ODE|differential equation|spiking|SNN|state-space model|Mamba|transformer`）均为本机 .txt 直接核验结果【确定】；"0–5 ms 与 0.18–300 ms 何者为典型"、"0.17 W 还是 0.17 mW"、"[36] 的真实载体"、"[48]/[50] 为何未被分析"为 **`[待核实]`**；"文献中是否存在 LNN 端侧工作"**本卡未做检索，标 `[待核实]`**（动作见 §7 第 5 条）；本文是否被更正或撤稿**本卡未查**，标 `[待核实]`。
