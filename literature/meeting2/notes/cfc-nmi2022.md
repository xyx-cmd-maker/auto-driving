# Closed-form 连续时间神经网络（CfC）｜Closed-form continuous-time neural networks

- **出处**：Nature Machine Intelligence 4(11):992–1003, 2022 ｜ **类型**：期刊论文（Article）
- **作者**：Hasani R, Lechner M, Amini A, Liebenwein L, Ray A, Tschaikowski M, Teschl G, Rus D
- **DOI**：10.1038/s42256-022-00556-7（VoR 版另有一篇更正：**10.1038/s42256-022-00597-y**，2022-11-29）
- **全文来源（主）**：`literature/fulltext/meeting2/cfc-nmi2022-VoR__b4789122.txt` ｜ **VoR 正式版**（PAGES=22；文件头标 CHARS=77,259，本机实测 79,140 字符 / 80,823 字节）｜ SOURCE_URL = `https://www.nature.com/articles/s42256-022-00556-7.pdf`，MD5 = `b4789122ce04bfb4ac042390f59aaa8b`
- **全文来源（对照）**：`literature/fulltext/meeting2/cfc-nmi2022__9f9cb876.txt` ｜ **arXiv 预印本 v2**（PAGES=40；任务书标 CHARS=62,050，本机实测 64,216 字符 / 65,835 字节；MD5 = `9f9cb876656c5cddfce2cb3438fbd6dd`）—— 第 1 页逐字印有 `arXiv:2106.13898v2 [cs.LG] 2 Mar 2022`
- **分组**：连续时间 / 流体神经网络（P1 控制器的方法学底座）
- **★ 版本与材料核验**：见下（8 问，逐条附页码与逐字证据）
- **证据等级初判**：**B 级** — 四个公开基准 + 两个新增基准上给出 mean ± s.d. (n = 5) 的完整对照表、超参与开源代码，属"设计良好但有边界"；但**基线数字多为跨论文引用、无显著性检验与 CI、无种子、真车实验零量化指标、全文零硬件**，其速度与"可上嵌入式"两项主张实际处于 C/D 级。
- **档位建议**：**A 精读** — 它是 P1 控制器（OTF-CfC）的方法学底座与 A2 消融（LNN vs CfC vs ODE-RNN）的直接对照来源；且**本次核验推翻了项目既有笔记对本文图表编号的全部引用**，不精读会直接导致 P1 稿件引用失实。
- **五维打分（按 `00-triage-protocol.md` §5，各维 0–2，满分 20）**：D1=**2** D2=**1** D3=**1** D4=**2** D5=**2** → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = **16/20** → **A 档**（≥14 且 D1=2 且 D5≥1 ✓）
  - D1=2：本文给出的**就是** P1 要注入 OTF 的那个连续时间网络族（P1 代号即 OTF-CfC），且其 Table 3 / Table 4 已把 **CfC / CfC-noGate / Cf-S / CfC-mmRNN 与 ODE-RNN、ODE-LSTM、LTC** 放在同一张表、同一 n=5 下对照 —— 这正是 P1 消融 A2 的现成对照骨架。**弱在哪**：它给的是 backbone 不是控制器，零闭环指标，ODD 为乡村单车横向控制。若把 D1 第二分句读成"数字须可复用"，则 D1=1、总分 13（B 档）——**本卡取"协议/对照设计可复用"这一支**，并在此显式声明该判断。
  - D2=1：真车闭环有做但**不产出任何量化指标**；表内基线多来自 refs. 7/9/55/57（跨论文拼接）；全文无显著性检验、无 CI、无种子 → 达不到"对照 + 实车闭环 + 有统计"三条同时成立。
  - D3=1：**代码可直接复用**（Apache 2.0 + Zenodo `10.5281/zenodo.7135472`）；但数据（自采车道保持数据不公开）、协议（accuracy/AUC/MSE vs P1 七项控制指标）、场景（rural vs 高速多车道编队）均不可直接迁移。
  - D4=2：2022 年发表，距今 ≤5 年。
  - D5=2：全文 22 页 + Extended Data 图 10 张 + 完整超参数 + 开源代码与 Zenodo 存档。唯一不达标项是**效应量（无 CI、无显著检验）**，该缺陷已计入 D2，不重复扣分。
  ⚠ 本卡**严格遵守 0–2 制**；D4 一律指**时效性**，未改写为其他含义。

---

## ★ 版本与材料核验（8 问，逐条给页码与逐字证据）

> 结论先行：**本卡以 NMI 正式版（VoR）为准；arXiv v2 仅作差异对照。两份材料是不同文件，且正式版的图表编号与 arXiv v2 大面积错位。**

### Q1 正式版标题（逐字）

**`Closed-form continuous-time neural networks`** ｜ 位置：VoR p.1（期刊页 992），行 13–14；同页抬头逐字 `Nature Machine Intelligence | Volume 4 | November 2022 | 992–1003`、`Article`、`https://doi.org/10.1038/s42256-022-00556-7`。

- arXiv v2 题名（行 7）为 `Closed-form Continuous-time Neural Networks`（Continuous-time / Neural / Networks 三词首字母大写）。
- 项目既有笔记 `literature/notes/p01-cfc-nmi2022.md` 第 4 行记录的引文题名是 **"Closed-form Continuous-time Neural Models"** —— **这不是本机任何一份材料的题名**。它对应的是 arXiv 的**更晚版本（HTML v3+）**题名，而不是 NMI 正式版。
- **判定：项目记录里写 NMI 题名 "neural networks" 是对的；写 "Neural Models" 是错的（那是 arXiv 后续版题名）。** 正式版题名以小写 `Closed-form continuous-time neural networks` 为准（NMI 句首大写、其余小写）。

### Q2 正式版作者列表与顺序（逐字）

VoR p.1 行 15–21 逐字：

> `Ramin Hasani 1,5, Mathias Lechner1,2,5, Alexander Amini1, Lucas Liebenwein 1, Aaron Ray1, Max Tschaikowski3, Gerald Teschl 4 & Daniela Rus1`

单位脚注（行 62–64）：`1Massachusetts Institute of Technology, Cambridge, MA, USA. 2Institute of Science and Technology Austria, Klosterneuburg, Austria. 3Aalborg University, Aalborg, Denmark. 4University of Vienna, Vienna, Austria. 5These authors contributed equally: Ramin Hasani, Mathias Lechner.`｜通讯：`e-mail: rhasani@mit.edu`

- **顺序与 arXiv v2 完全一致**（8 人同序，无差异）。
- **唯一差异在单位**：arXiv v2 中 Lechner 只挂 IST Austria（单位 2）；**VoR 中 Lechner 挂 MIT + IST Austria（1,2）**。若项目"50 篇地图"或 `refs.bib` 记了不同作者顺序，**以 VoR 为准**。

### Q3 正式版的图号体系

| 内容 | 正式版（VoR）编号 | 位置 |
|---|---|---|
| **参数量（车道保持模型）** | **Extended Data Fig. 9** —— **注意：正式版里它不是"表"，是"扩展数据图"** | p.21 |
| Bit-stream XOR 结果 | **Extended Data Fig. 5** | p.17 |
| PhysioNet 结果 | **Extended Data Fig. 6** | p.18 |
| IMDB 结果 | **Extended Data Fig. 8** | p.20 |
| Walker2D 结果 | **Table 3**「Per time-step regression」 | p.6（997） |
| 事件式 sMNIST 结果 | **Table 4** | p.6（997） |
| 人活动识别结果 | **Table 2** | p.5（996） |
| 神经元/突触动力学 | Fig. 1 | p.2（993） |
| 闭式解紧致性（MSE 0.006） | **Fig. 2** | p.4（995） |
| 求解器与序列复杂度 | **Table 1**（左右两栏合并） | p.3（994） |
| CfC 架构图 / LTC 两神经元实例 | **Extended Data Fig. 2 / Fig. 1** | p.14 / p.13 |
| **真车车道保持** | **没有专属图表**：试验叙述在正文 p.6（997）与 Methods p.9（1000）；参数量在 **Extended Data Fig. 9**；注意力可视化在 **Extended Data Fig. 10** | p.6 / p.9 / p.21 / p.22 |

**正式版新增（arXiv v2 无）**：Table 2 人活动识别（6,554 条序列、561 维惯导特征、6 类逐时刻分类，行 497–502）、Table 4 事件式 sMNIST（784 长序列压缩为 256 长事件序列，行 1085–1101）。正式版把 arXiv v2 的 Table 1 与 Table 2 **合并成一张 Table 1**（左栏求解器复杂度、右栏序列/单步复杂度）。

### Q4 arXiv v2 的 Tables S1–S4 在正式版里还在不在？

**不在，且正式版根本没有"补充材料"这一载体。**

- VoR 全文 `Supplementary` **0 命中**（`Supplementary Information` / `Supplementary Figure` / `Supplementary Table` / `List of Supplementary materials` 全部 0 命中）。
- arXiv v2 的 p.36 有 `List of Supplementary materials` + `Materials and Methods.` + `Tables S1 to S4.`，另有 p.37 的 `Supplementary Materials` 标题与 Lemma 1 完整证明（pp.37–38）、Tables S1–S4（pp.39–40）。**这种「List of Supplementary materials / One Sentence Summary / Main Text」是 Science 家族的投稿排版，不是 Nature 家族排版** —— 这也是判定 v2 非正式版的旁证之一。
- 正式版的去向：① Lemma 1 的证明并入 **Methods**（p.7–8 / 998–999）；② 超参数改为 **Extended Data Fig. 3（Human activity + Walker2D，p.15）、Fig. 4（ET-sMNIST + Bit-stream XOR，p.16）、Fig. 7（PhysioNet + IMDB，p.19）** 三张图；③ Methods 新增一份**超参数名词表**「Description of hyperparameters」（p.9 / 1000，行 1208–1246），含 v2 未列的新项 **`τ_data`**（elapsed time 输入的常数乘子，默认 1）与 **`init`**（Xavier 均匀分布增益，默认 1）。
- **推论（对 P1 直接相关）**：若 P1 稿件写"超参数见 Supplementary Table S2"，在正式版里**指向一个不存在的东西**。

### Q5 正式版 Abstract 逐字原文

VoR p.1（992）行 22–47 逐字（提取文本中的连字已还原）：

> Continuous-time neural networks are a class of machine learning systems that can tackle representation learning on spatiotemporal decision-making tasks. These models are typically represented by continuous differential equations. However, their expressive power when they are deployed on computers is bottlenecked by numerical differential equation solvers. This limitation has notably slowed down the scaling and understanding of numerous natural physical phenomena such as the dynamics of nervous systems. Ideally, we would circumvent this bottleneck by solving the given dynamical system in closed form. This is known to be intractable in general. Here, we show that it is possible to closely approximate the interaction between neurons and synapses—the building blocks of natural and artificial neural networks—constructed by liquid time-constant networks efficiently in closed form. To this end, we compute a tightly bounded approximation of the solution of an integral appearing in liquid time-constant dynamics that has had no known closed-form solution so far. This closed-form solution impacts the design of continuous-time and continuous-depth neural models. For instance, since time appears explicitly in closed form, the formulation relaxes the need for complex numerical solvers. **Consequently, we obtain models that are between one and five orders of magnitude faster in training and inference compared with differential equation-based counterparts.** More importantly, in contrast to ordinary differential equation-based continuous networks, closed-form networks can scale remarkably well compared with other deep learning instances. Lastly, as these models are derived from liquid networks, they show good performance in time-series modelling compared with advanced recurrent neural network models.

**`orders of magnitude` 措辞核验**：正式版**逐字保留** `between one and five orders of magnitude faster in training and inference`，仅把 arXiv v2 的 `compared to` 改为 `compared with`。→ **该主张在正式版中同样存在、同样无图表支撑**（详见下方 ⚠ 内部不一致第 8 条与 §8 关键数字）。

**与 arXiv v2 摘要的逐条差异**（v2 位置：p.1 行 17–29 + p.2 行 34–45）：

| 项 | arXiv v2 | VoR 正式版 |
|---|---|---|
| 开头 | `Continuous-time neural processes are performant sequential decision-makers that are built by differential equations (DE).` | 改为两句：`Continuous-time neural networks are a class of machine learning systems that can tackle representation learning on spatiotemporal decision-making tasks. These models are typically represented by continuous differential equations.` |
| 措辞 | `significantly slowed down` | `notably slowed down` |
| 连字符 | `in closed-form` | `in closed form` |
| 引文 | `constructed by liquid time-constant networks (LTCs) (1)` | `constructed by liquid time-constant networks`（删 LTCs 缩写与引文） |
| 比较词 | `compared to` | `compared with`（全文三处） |
| ODE 表述 | `in contrast to ODE-based continuous networks` | `in contrast to ordinary differential equation-based continuous networks` |
| 末句 | `they show **remarkable** performance in time series modeling, compared to advanced recurrent models.` | `they show **good** performance in time-series modelling compared with advanced recurrent neural network models.` |

→ **净结论**：核心速度主张逐字未变；**但末句措辞被正式版从 `remarkable` 下调为 `good`** —— 引用"remarkable"即引用 arXiv 版措辞，与正式版不符。

### Q6 正式版是否出现任何硬件字样？

**全文未见任何硬件字样。** 逐项字面计数（VoR 全文，含正文/图注/表注/Methods/Extended Data 图注/参考文献，共 79,140 字符）：

| 检索词 | 命中 | 检索词 | 命中 | 检索词 | 命中 |
|---|---|---|---|---|---|
| `GPU` | **0** | `CPU` | **0** | `NVIDIA` | **0** |
| `Jetson` | **0** | `microcontroller` | **0** | `MCU` | **0** |
| `memory footprint` | **0** | `memory usage` | **0** | `latency` | **0** |
| `FLOP` | **0** | `fp32` | **0** | `fp16` / `float32` | **0** |
| `wall-clock` | **0** | `power consumption` | **0** | ` KB` / ` MB` / ` GB` | **0 / 0 / 0** |
| `ARM` | **0** | `Cortex` | **0** | `TensorRT` / `ONNX` / `quantiz*` | **0 / 0 / 0** |

唯一近似项（逐字给位置）：
1. p.3（994）行 129–130：`...as the complexity of the data, task and state space increases (that is, requiring more precision)11...` —— 指**求解器精度**，不是数值格式。
2. p.6（997）行 684–685：`(2) the training and inference efficiency of a model is important (for example, embedded applications39–41)` —— **建议句 + 三篇引文**，不是本文实测。
3. Table 1（p.3 / 994）给的是**渐进复杂度**（`𝒪(Kp)`、`𝒪(nk)`、`𝒪(kp)`），不是实测时延。
4. 速度量只有 `Time per epoch (min)` **单值**（Tables 2/3/4），**无硬件、无精度、无 batch size、无重复次数说明**。
5. `memory` 命中 19 次，**全部是机器学习语义**（memory state / mixed memory / long short-term memory / working memory），无一条指内存占用。

→ **正式版与 arXiv v2 在这一项上完全一致：本文没有任何硬件实测、没有单步时延、没有内存占用、没有功耗。** 项目 `AGENTS.md` §1「该文未报告任何硬件」的结论**在正式版上复核成立**。

### Q7 ★参数量口径（最高优先项）——**已在正式版上读图核验通过（2026-10-04 补做）**

这是本卡最重要的一条核验项，现**已闭合**，逐字记录如下：

1. **正式版正文只有一句话**（p.6 / 997，行 644–647，逐字）：
   > `Moreover, similar to NCPs, CfCs are parameter efficient. They performed the end-to-end autonomous lane-keeping task with around 4,000 trainable parameters in their RNN component (Extended Data Fig. 9).`
   注意：arXiv v2 写的是 `around 4k trainable parameters`，**正式版改写为 `around 4,000`**。
2. **承载完整参数量的 Extended Data Fig. 9 在本地提取文本中只有图注、没有表体**（p.21，逐字）：
   > `Extended Data Fig. 9 | Lane-keeping models' parameter count. CfC and NCP networks perform lane-keeping in unseen scenarios with a compact representation.`
   表体是**图像**，数值不在文本层。
3. **字面计数**：VoR 全文 `230,828` = **0**、`230828` = 0、`4,184` = 0、`4184` = 0、`226,644` = 0、`259,733` = 0、`233,139` = 0、`227,728` = 0、`235,052` = 0、`2,124,901` = 0。→ **一条都不在正式版文本层里**（它们在图里）。
4. **★ 核验补做（成功，2026-10-04）**：把 VoR PDF 的 **p.21 以 220 dpi 栅格化**为 PNG 后**直接读图抄录**，取得 ED Fig. 9 全表。**方法可复现**：PyMuPDF 渲染 → 读图；脚本 `literature/fulltext/_tools/` 会话内使用，渲染件在 `literature/meeting2/_pages/cfc-vor-p21.png`。

   **Extended Data Fig. 9 逐字读出的全表（VoR p.21）**：

   | Modes | Total Parameter Count (CNN head + RNN) | RNN Parameter Count |
   |---|---|---|
   | CNN | 2,124,901 | – |
   | LSTM | 259,733 | 33089 |
   | NCP | 233,139 | 6495 |
   | Cf-S | 227,728 | 1084 |
   | **CfC** | **230,828** | **4184** |
   | **CfC-NoGate** | **230,828** | **4184** |
   | CfC-mmRNN | 235,052 | 8408 |

   **★ 结论：正式版 ED Fig. 9 的数值与 arXiv v2 Table 3 逐格一致**（含 CfC 与 CfC-NoGate 参数完全相同这一点）。复算自洽性同样成立：五组「Total − RNN」恒为 **226,644**。

**→ 对 P1 的直接后果（口径必须这样写）：**

- `4,184`（RNN 分量）与 `230,828`（含 CNN 头全模型）**现在有两个可核验出处**：arXiv v2 Table 3（文字表格）**与 NMI 正式版 Extended Data Fig. 9（p.21，图像，本次已读图核验）**，两者一致。
- 因此：**P1 的「不得写 <500 KB」红线结论不变，且证据等级上调** —— 230,828 参数 fp32 = 923,312 B ≈ **901.7 KiB > 500 KB**；fp16 = 461,656 B ≈ **450.8 KiB** 才达标。引用写法可改为：「**NMI 正式版 Extended Data Fig. 9（p.21）报告：CfC 全模型 230,828 参数（含 CNN 头），RNN 分量 4,184**」。
- ⚠ **残留口径注意**：ED Fig. 9 的两列表头逐字为 `Total Parameter Count (CNN head + RNN)` 与 `RNN Parameter Count`，**全表未出现"KB"、未提量化精度**。所以"901.7 KiB / 450.8 KiB"是**本项目的换算**，不是论文的报告值 —— 引用时必须写明这是我们的换算。
- 正式版正文的 `around 4,000` **只支持"RNN 分量约 4k"，不支持任何"全模型 < 500 KB"的说法**；且正式版**同样没有任何嵌入式/内存实测**（见 Q6）。
- **同法可读**（尚未做，成本各约 1 分钟）：`{FIG-CFC-ED5}` p.17（Bit-stream XOR）、`{FIG-CFC-ED6}` p.18（PhysioNet）、`{FIG-CFC-ED8}` p.20（IMDB）、`{FIG-CFC-ED3/4/7}` pp.15/16/19（超参）—— 读图后即可把 §8.2 整块从"仅 arXiv 可核"升级为"正式版可核"。


### Q8 图/表编号映射表（既有笔记 → 正式版）★ 本次交付的关键产物

既有笔记 `literature/notes/p01-cfc-nmi2022.md` 引用的编号，逐条映射：

| 既有笔记引的编号 | 该编号在 arXiv v2 中的内容 | 正式版（VoR）对应编号 | 是否一致 |
|---|---|---|---|
| **Table 3** | 车道保持模型参数量表（文字表格） | **Extended Data Fig. 9**（p.21；图注同名，**表体为图像**） | ✗ **编号与载体类型都变**（表→扩展数据图） |
| **Table 4** | Bit-stream XOR | **Extended Data Fig. 5**（p.17） | ✗ |
| **Table 5** | PhysioNet AUC | **Extended Data Fig. 6**（p.18） | ✗ |
| **Table 6** | IMDB test accuracy | **Extended Data Fig. 8**（p.20） | ✗ |
| **Table 7** | Walker2D 平方误差 | **Table 3**（p.6；列名改为 `Mean Squared Error (MSE)`） | ✗（编号撞车纯属巧合，内容对应的是 Table 3） |
| **Fig. 3** | 闭式解紧致性（MSE 0.006） | **Fig. 2**（p.4） | ✗ |
| **Fig. 5** | 注意力剖面（真车视觉回传） | **Extended Data Fig. 10**（p.22） | ✗ |
| Fig. 1 | 神经元/突触动力学 | **Fig. 1**（p.2） | ✓ 唯一不变项之一 |
| Fig. 2 | LTC 两神经元实例 | **Extended Data Fig. 1**（p.13） | ✗ |
| Fig. 4 | CfC 架构图 | **Extended Data Fig. 2**（p.14） | ✗ |
| Table 1 | 求解器复杂度 | **Table 1 左栏**（p.3） | ✓（合并） |
| Table 2 | 序列/单步复杂度 | **Table 1 右栏**（p.3） | ✗（并入 Table 1） |
| Tables S1–S4 | 超参数表 | **正式版无此物**；改为 Extended Data Figs. 3 / 4 / 7（p.15 / 16 / 19） | ✗ |
| —（无） | — | 正式版新增：**Table 2**（人活动识别，p.5）、**Table 4**（事件式 sMNIST，p.6） | 新增 |

> **★ 引用纪律结论**：既有笔记引用的编号中，**只有 Fig. 1 与 Table 1 在正式版里保持不变**；**Table 3 / Tables 4–7 / Fig. 3 / Fig. 5 全部错位**。若 P1 稿件沿用既有笔记写「CfC 的参数量见 Table 3」「XOR 见 Table 4」「真车见 Fig. 5」，在正式版中会分别指向 **Walker2D 回归表、事件式 sMNIST 表、以及不存在的内容** —— **属引用失实，必须改写为 Extended Data Fig. 9 / Fig. 5 / Fig. 10**。

---

## 1. 标题

`Closed-form continuous-time neural networks`（VoR p.1 逐字；arXiv v2 作 `Closed-form Continuous-time Neural Networks`）｜中文直译：**闭式连续时间神经网络**

---

## 2. 摘要（以本 PDF 的 Abstract 为准）

正式版摘要（p.1 / 992）中译要点：连续时间神经网络是一类能处理时空决策任务表征学习的机器学习系统，通常用连续微分方程表示；但其在计算机上的表达能力受**数值微分方程求解器**瓶颈限制，这显著拖慢了对神经系统动力学等自然物理现象的规模化与理解。理想上应以闭式求解该动力系统，但一般不可行。作者证明：由**液态时间常数网络（LTC）**构成的神经元—突触相互作用可在闭式下被紧密近似；为此给出 LTC 动力学中一个积分的**紧致有界**近似（该积分此前无已知闭式解），使**时间显式进入闭式**，从而摆脱复杂数值求解器。由此所得模型在训练与推理上比基于微分方程的对应模型**快 1–5 个数量级**；与 ODE 连续网络不同，闭式网络"可显著良好地扩展"；因源自液态网络，其在时间序列建模上相对先进循环网络模型表现良好。**摘要内无任何具体数字、数据集、指标或硬件。**

---

## 3. 结论（作者结论/讨论节要点 + 关键数字 + 作者自承局限）

讨论节（p.6 / 997）与 Methods 的变体选择建议（p.9 / 1000）：作者称 CfC 兼具 ODE 网络的建模能力而"更快、更准、更稳"；建议序列数百步内用 CfC、长程依赖用 CfC-mmRNN、要最快推理用 Cf-S、CfC-noGate 当超参试。**自承局限**：① 可能出现**梯度消失**，长程依赖宜配混合记忆网络或恰当的转移矩阵参数化；② 生成建模须用 ODE（保证可逆/双射），**CfC 只近似 ODE，不再保证双射**；③ 由 ODE 推断因果可能更直接（作者自标为推测）。**口径自相矛盾**：同段先写"闭环性能重要的场合 CfC 可带来大价值"（唯一支撑为引文 24），紧接着写"隐式 ODE 与 PDE 模型在连续定义的物理问题与**控制任务**上仍可能有益"。适用清单含"嵌入式应用"与"可解释性重要"，**均为引文支撑的建议句，全文零嵌入式实测**。关键数字：真车 1 km 私有路、30 km/h 恒速、"所有网络均成功完成车道保持"——无任何闭环性能数字。

---

## 4. 方法一句话

**输入**不规则采样时序/像素流 → **模型**LTC 闭式近似的时间门控网络 `σ(−ft)⊙g+(1−σ(−ft))⊙h` → **输出**逐步预测或转向曲率。

---

## 5. 图表清单（占位符）

> 占位符约定：正式版的补充材料名为 **Extended Data**，故用 `{FIG-CFC-EDn}`（等价于模板的 `{FIG-CFC-Sn}`，EDn ≡ Sn）；arXiv v2 的补充部分另用 `{TAB-CFC-Sn}` 标注。图注逐字，截断至 100 字符（截断处加 `…`）。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-CFC-1} | Fig. 1（p.2 / 993） | `Fig. 1 \| Neural and synapse dynamics. A postsynaptic neuron receives the stimuli I(t) through a nonlinear conductance-based synapse model. Here, S(t) …` | 全文唯一"物理直觉图"：把 LTC 的 ODE 与本文闭式解 `x(t) = (x(0) – A)e^(–[1+f(I(t))]t) f(–I(t)) + A` 并置。是 P1 在 Introduction 里解释"连续时间 vs 离散 RNN"的唯一图标来源；**与 P1 的 OTF 势场无直接关系**。 |
| {TAB-CFC-1} | Table 1（p.3 / 994） | `Table 1 \| Computational complexity of models … Left: The time complexity of the process to compute K solver steps. ϵ is step size. ϵ̃ is the maximum step size and δ ≪ 0. K̃ is …` | 左栏为**引用自 ref. 17（Hypersolvers）**的求解器复杂度，右栏才是本文的序列/单步复杂度。**CfC 与离散 RNN 同为 𝒪(nk)/𝒪(k)**，ODE-RNN 为 𝒪(nkp)/𝒪(kp)，Transformer 为 𝒪(n²k)/𝒪(nk)。P1 论证"CfC 适合 100 Hz 定步长回路"时**只能引右栏**，且须注明左栏非本文数据。 |
| {FIG-CFC-2} | Fig. 2（p.4 / 995） | `Fig. 2 \| Tightness of the closed-form solution in practice. We approximate a closed-form solution for LTC networks1 while largely preserving the trajectories of their equivalent ODE systems. We …` | 图注含全文最激进的单点加速断言 `at least 100 fold faster than neural ODEs`（正文对应的 MSE 数字 = 0.006，见 Methods p.8 / 999）。**该 100× 与 Table 3（Walker2D 上 CfC/ODE-RNN = 9.9×）冲突**，见 ⚠ 内部不一致第 4 条。 |
| {TAB-CFC-2} | Table 2（p.5 / 996） | `Table 2 \| Human activity recognition, per time-step classification … Numbers represent mean ± s.d. (n = 5). The performance of the models marked by † is reported from ref. 7. Bold …` | **正式版新增实验**。12 行同表对照：Cf-S **87.04 ± 0.47**（最高）> CfC-mmRNN 85.97 ± 0.25 > CfC-noGate 85.57 ± 0.34 > **CfC 84.87 ± 0.42** > Latent-ODE-ODE 84.60 ± 1.3。注意 **vanilla CfC 仅比最强 ODE 基线高 0.27 个百分点**，而正文只点名 Cf-S/CfC-noGate/CfC-mmRNN 三者"outperform with a high margin"（**选择性列举**）。 |
| {TAB-CFC-3} | Table 3（p.6 / 997） | `Table 3 \| Per time-step regression … Modelling the physical dynamics of a walker agent in simulation. Numbers present mean ± s.d. (n = 5). The performance of the models marked by † is reported …` | **= arXiv v2 的 Table 7**（数值逐条一致）。19 行同表：CfC-mmRNN **0.617 ± 0.006**、CfC **0.643 ± 0.006**、CfC-noGate 0.650 ± 0.008、LTC 0.662 ± 0.013、Transformer 0.761 ± 0.032、ODE-LSTM 0.883 ± 0.014、ODE-RNN 1.904 ± 0.061。**这是 P1 消融 A2 最可直接挪用的对照表**（CfC vs ODE-RNN vs ODE-LSTM vs LTC 同表同 n=5）。 |
| {TAB-CFC-4} | Table 4（p.6 / 997） | `Table 4 \| Event-based sequence classification on irregularly sequential MNIST … Test accuracy shown as mean ± s.d. (n = 5). Bold values indicate the highest accuracy and best time per …` | **正式版新增实验**（arXiv v2 无）。17 行同表：CfC-mmRNN **98.09 ± 0.18**（SOTA）、CfC-noGate **96.99 ± 0.30**、CfC 95.42 ± 0.21、Cf-S 95.23 ± 0.16、ODE-LSTM 95.73 ± 0.24、Lipschitz RNN 95.92 ± 0.16、ODE-RNN **72.41 ± 1.69**、CT-RNN 72.05 ± 0.71。**同表内 ODE-RNN/CT-RNN/GRU-ODE 全部崩到 72–82%，是 P1 论证"ODE 基线在长事件序列上失效"的最强单表证据。** |
| {FIG-CFC-ED1} | Extended Data Fig. 1（p.13） | `Extended Data Fig. 1 \| Instantiation of LTCs in ODE and closed-form representations. a) A sample LTC network with two nodes and five synapses. b) the ODE representation of this …` | **= arXiv v2 的 Fig. 2**。两神经元五突触实例的 ODE 式与闭式解并列；是 Methods 里 Algorithm 1（LTC→闭式编译）的图解入口。 |
| {FIG-CFC-ED2} | Extended Data Fig. 2（p.14） | `Extended Data Fig. 2 \| Closed-form Continuous-depth neural architecture. A backbone neural network layer delivers the input signals into three head networks g, f and h. f acts as a …` | **= arXiv v2 的 Fig. 4**。P1 若照搬 CfC 架构，这张图就是"backbone 分 f/g/h 三头 + σ 时间门"的唯一权威图。 |
| {FIG-CFC-ED3} | Extended Data Fig. 3（p.15） | `Extended Data Fig. 3 \| Hyperparameters for Human activity and Walker. List of hyperparameters used to obtain results in Human activity and Walker2D Experiments.` | **= arXiv v2 Table S1(S4) 的去向之一**（超参在正式版变成"图"）。P1 复现 Walker2D 基线或对齐调参预算时，必须从此图取数（文本层无数值）。 |
| {FIG-CFC-ED4} | Extended Data Fig. 4（p.16） | `Extended Data Fig. 4 \| Hyperparameters for ET-sMNIST and Bit-stream XOR. List of hyperparameters used to obtain results in Event-based MNIST and Bit-stream XOR Experiments.` | **= arXiv v2 Table S1 的去向**。想复现 XOR 或 ET-sMNIST 的 CfC 设定，只能读这张图。 |
| {FIG-CFC-ED5} | Extended Data Fig. 5（p.17） | `Extended Data Fig. 5 \| Bit-stream XOR sequence classification. The performance values (accuracy %) for all baseline models are reproduced from9. Numbers present mean ± standard deviations, (n=5). …` | **= arXiv v2 的 Table 4**。⚠ **表体为图像，本地文本层无任何 XOR 数值** → 既有笔记抄录的 XOR 数字（CfC 99.42 ± 0.42 等）**只能以 arXiv v2 为出处**，正式版无法复核。 |
| {FIG-CFC-ED6} | Extended Data Fig. 6（p.18） | `Extended Data Fig. 6 \| PhysioNet. AUC stands for area under curve. Numbers present mean ± standard deviations, (n=5). Note: The performance of the models marked by † are reported …` | **= arXiv v2 的 Table 5**。⚠ **表体为图像，无 AUC 数值** → "160 times / 220 times / three times" 三项正文断言在正式版里**同样无法复算**（只能回到 arXiv v2 Table 5 复算）。 |
| {FIG-CFC-ED7} | Extended Data Fig. 7（p.19） | `Extended Data Fig. 7 \| Hyperparameters for Physionet and IMDB. List of hyperparameters used to obtain results in Physionet and IMDB sentiment classification experiments.` | **= arXiv v2 Table S2/S3 的去向**。对齐 P1"同等调参预算"时，这里能拿到 CfC 各变体的最终取值，但**仍无搜索空间、无搜索算法、无预算**。 |
| {FIG-CFC-ED8} | Extended Data Fig. 8（p.20） | `Extended Data Fig. 8 \| Results on the IMDB datasets. The experiment is performed without any pretraining or pretrained word-embeddings. Thus, we excluded advanced attention-based models78,79 …` | **= arXiv v2 的 Table 6**。⚠ **表体为图像，无 IMDB 数值** → "vanilla CfC 低于 LSTM" 这一关键反差**在正式版文本层不可复核**，只能以 arXiv v2 为出处。 |

> **总数**：本 PDF（VoR）共 **Fig. 1–2（2 张主图）+ Table 1–4（4 张主表）+ Extended Data Fig. 1–10（10 张扩展数据图）= 16 个**（>14，按模板只列前 14 个）。
> 第 15、16 个（**P1 最高优先项所在**）：`{FIG-CFC-ED9}` = **Extended Data Fig. 9**（p.21）`Extended Data Fig. 9 | Lane-keeping models' parameter count. CfC and NCP networks perform lane-keeping in unseen scenarios with a compact representation.` —— **参数量全表在此，表体为图像，文本层无数值（见核验 Q7）**；`{FIG-CFC-ED10}` = **Extended Data Fig. 10**（p.22）`Extended Data Fig. 10 | Attention Profile of networks. Trained networks receive unseen inputs (first column in each tab) and generate acceleration and steering commands. We use the Visual-Backprop algorithm65 to compute the saliency maps of the convolutional part of each network. a) results for networks tested on data collected in summer. b) results for networks tested on data collected in winter. c) results for inputs corrupted by a zero-mean Gaussian noise with variance, σ2 = 0.35.`
> 另：**Algorithm 1**（p.8 / 999，`Translate the architecture of an LTC network into its closed-form variant`）是算法框，不计入图表数。

---

## 6. 对 P1 的用处

### 与 P1 的关系：**相邻问题（方法学底座），不是"直接回答"**

CfC 给的是**连续时间序列建模 backbone**，不是控制器：它没有状态反馈结构、没有控制代价、没有约束处理、没有稳定性论证。其唯一真车实验是**乡村道路（rural）单车横向车道保持**（pixel→steering curvature，模仿学习），与 P1 的「高速主线、多车道、人工自动混行、编队纵向跟车」在 ODD、任务维度（横向 vs 纵向/编队）、评价指标上**三者皆不同**。

### 可迁移（具体到方法/协议/数字/图表）

1. **★ P1 消融 A2（LNN vs CfC vs ODE-RNN）的对照骨架是现成的**：正式版 **Table 3（Walker2D）** 与 **Table 4（ET-sMNIST）** 在同一张表、同一 n = 5、同一代码库下给出 **CfC / CfC-noGate / Cf-S / CfC-mmRNN / LTC / ODE-RNN / ODE-LSTM** 的并列数值。P1 的 A2 可直接沿用「同表并列 + 一次只改一个因素 + 报 mean ± s.d. (n=5)」这一协议骨架，并在文中注明"对照设计参照 Hasani et al. 2022 Table 3/4"。
2. **变体消融的"参数对齐"做法**：arXiv v2 Table 3 显示 **CfC 与 CfC-noGate 参数完全相同（230,828 / 4,184）**，即两变体的差异纯来自门控机制而非容量 —— 这正是 P1「消融一次只改一个因素」的范例。
3. **时间门控与 100 Hz 定步长回路机理相容**：`x(t) = σ(−f·t)⊙g + (1−σ(−f·t))⊙h`（式 4，p.4 / 995）不需要 ODE 求解器，`t` 显式进入门控；Table 1 右栏给 CfC 单步复杂度 𝒪(k)，与离散 RNN 同阶。P1 若要论证"连续时间模型能在固定控制周期内跑完"，**这是可引的机理证据**（但**不是**时延实测）。
4. **代码与超参可直接取用**：`Data availability` / `Code availability`（p.9 / 1000，行 1247–1255）逐字给出 `https://github.com/raminmh/CfC`（Apache 2.0）+ Zenodo DOI **`10.5281/zenodo.7135472`**（正式版**新增**了 Zenodo 存档号，arXiv v2 没有）；超参数在 **Extended Data Figs. 3 / 4 / 7**；Methods 附**超参数名词表**（p.9 / 1000）。
5. **P1 需要的"失败设定"证据**：正式版 **Table 4** 同表内 `ODE-RNN 72.41 ± 1.69`、`CT-RNN 72.05 ± 0.71`、`GRU-ODE 80.95 ± 1.52`，而 CfC 系 95.2–98.1 —— 这是 P1 报告"哪些基线在长事件序列上失效"的现成对照行。

### 不可迁移 / 陷阱

- **★ 参数量口径（最高优先）**：正文 `around 4,000 trainable parameters in their RNN component`（p.6 / 997）**只指 RNN 分量**；含 CNN 感知头的全模型为 **230,828**（arXiv v2 Table 3；fp32 = 923,312 B ≈ **901.7 KiB > 500 KB**）。→ **P1 不得写"<500 KB"**；若必须写，须同时写明**量化精度**（fp16 ≈ 450.8 KiB 才达标）与**是否含感知头**。且该数字在正式版**只能通过 Extended Data Fig. 9 的图读**，文本层不可核验（核验 Q7）。
- **★ 术语陷阱**：本文用 `causal representation learning`（p.4 / 995，行 405–408）、`dynamic causal models`（p.9 / 1000）、`liquid` 等词，但**从未做任何"结构条件注入"的开关消融**。P1 把 OTF 势场作为边界条件注入，**不宜自称 `physics-informed`**（OTF 势场是启发式先验、无可判真伪的残差）；宜用 **structure-informed / prior-informed / boundary-conditioned**，并把 OTF 定位为 **inductive bias**。P1 的 A1 消融（OTF 开/关）相对本文是净增量。
- **★ 指标完全不可迁移**：正式版全部指标是 `Accuracy (%)` / `AUC` / `MSE` / 参数量 / `Time per epoch (min)`；P1 的七项（跟车误差 RMSE、加速度平方积分、Jerk 峰值、车道居中偏差、前轮转角方差、端到端延迟、MCU 内存占用）**一项都没有**。尤其：**端到端延迟与 MCU 内存占用在正式版中仍为零**（核验 Q6），P1 不得从本文推出任何实时性结论。
- **★ ODD 不可升格**：正式版仍只写 `a variety of rural driving environments`（p.9 / 1000，行 1152）；`highway` / `motorway` / `freeway` 全文 0 命中。**不得表述为"高速"证据**，更不得表述为编队/多车证据。
- **★ 版本陷阱**：**不能按 arXiv 编号引用正式版**（映射表见核验 Q8：Table 3/4/5/6/7、Fig. 3、Fig. 5 全部错位）。
- **★ 更正陷阱**：正式版页脚逐字印有 `© The Author(s) 2022, corrected publication 2022`（p.12 / 1003，行 1609），Crossref 亦记录类型为 `correction` 的 **`10.1038/s42256-022-00597-y`（2022-11-29）**。**引用前必须读该更正**，确认它修正的是哪一处。既有笔记只写了"若已有更正未反映"，**本卡已实查：确有更正**。
- **★ 统计陷阱**：正式版 `seed` **0 命中**、`significan*` **0 命中**、无 CI、无 p 值；Tables 2/3/4 的基线大多标 `†`/`*` 来自 refs. 7 / 9 / 55 / 57（**跨论文拼接**，非本文重跑）。P1 引用其"更快更准"时必须带上这一层限制。

### 与已有笔记 `literature/notes/p01-cfc-nmi2022.md` 的差异（★ 本卡最大价值）

| # | 项 | 既有笔记（依据 arXiv HTML 2106.13898） | 本卡（依据 VoR 正式版 + arXiv v2 对照） | 以谁为准 |
|---|---|---|---|---|
| 1 | **版本归属** | 自承"依据 arXiv HTML 版，**未与 NMI 2022 正式版逐字比对**"，并把核验列为待办（§九-1） | **本卡已完成该核验**：正式版 = VoR（22 页，nature.com PDF，DOI/卷期页齐全，`arXiv` 大写 0 命中、`arxiv.org` 6 次全在参考文献 URL 中）；arXiv v2 = 40 页预印本（p.1 印 `arXiv:2106.13898v2 [cs.LG] 2 Mar 2022`，Science 家族排版，含 Tables S1–S4） | **正式版（VoR）** |
| 2 | **图表编号** | 引用 Table 3 / Table 4–7 / Fig. 3 / Fig. 5 / Tables S1–S4 | **这些编号在正式版中全部错位**（映射见 Q8）：参数量→ED Fig. 9；XOR→ED Fig. 5；PhysioNet→ED Fig. 6；IMDB→ED Fig. 8；Walker2D→**Table 3**；紧致性→**Fig. 2**；注意力→**ED Fig. 10**；Tables S1–S4→**正式版无此物**（改为 ED Figs. 3/4/7） | **正式版**；arXiv 编号仅在与 v2 对照时可用，**引用必须注明版本** |
| 3 | **参数量口径** | Table 3：CfC 全模型 230,828 / RNN 分量 4,184（**正确，且表内自洽**：五组「总−RNN」恒为 226,644） | **正式版文本层两数皆 0 命中**；正文只写 `around 4,000 ... in their RNN component`；承载数值的 **ED Fig. 9 表体为图像** → **无法从正式版复核** | 数字仍以 **arXiv v2 Table 3** 为准，但**引用时必须补注"正式版对应 ED Fig. 9，文本层不可核验"** |
| 4 | **摘要措辞** | 引 `one and five orders of magnitude`（arXiv 版） | **正式版逐字同样保留**该句；但末句由 `remarkable performance` **下调为 `good performance`**，比较词由 `compared to` 改为 `compared with`，开头两句重写 | 引速度句两者皆可；**引"remarkable"则只对 arXiv 版成立** |
| 5 | **真车场景** | 写"**高速公路**/乡村车道保持" | **正式版与 v2 都只写 `rural driving environments`**；`highway` 全文 0 命中 | **以原文为准：乡村道路，"高速公路"是笔记的额外概括，须删** |
| 6 | **实验范围** | 五个设置（XOR / PhysioNet / IMDB / Walker2D / 车道保持） | **正式版为七个**：新增 **人活动识别（Table 2）** 与 **事件式 sMNIST（Table 4）**；XOR 与 PhysioNet、IMDB 三项被移入 Extended Data | 正式版 |
| 7 | **更正状态** | §九-6 仅写"若该文已有更正或撤稿，本笔记未反映" | **实查结果：确有更正** —— Crossref `update-to` = `10.1038/s42256-022-00597-y`（type `correction`，2022-11-29）；正式版页脚印 `corrected publication 2022` | 本卡；引用前须读更正 |
| 8 | **数据点补全** | 未收录：PhysioNet 的 RNN-VAE（0.515 ± 0.040 / 2.0 min）与 Latent-ODE-RNN（0.781 ± 0.018 / 6.7 min）；IMDB 的 ReLU GRU（84.8 ± n/a）与 Skip LSTM（86.6 ± n/a）；Walker2D 的 CT-RNN/CT-GRU/RNN-Decay/Bi-RNN/GRU-D/PhasedLSTM/GRU-ODE/CT-LSTM/coRNN/Lipschitz RNN 各行 | 本卡在 §8 补齐**正式版文本层可逐字读取**的全部行（Tables 2/3/4）；XOR/PhysioNet/IMDB 三表因**正式版表体为图像**，仍需回到 **arXiv v2** 取数 | 数字出处必须逐项注明版本 |

### 引用时必须带的限定语（一句）

> **Hasani et al., NMI 2022（正式版 Fig. 2 的紧致性实验与 Tables 2/3/4 的逐时刻分类/回归；XOR、PhysioNet、IMDB 三组结果见 Extended Data Figs. 5/6/8，参数量见 Extended Data Fig. 9）——该文的 CfC 在 6 个序列建模基准上以 mean ± s.d. (n = 5) 报告，但基线数字多引自 refs. 7/9/55/57 而非同协议重跑、无显著性检验、无 CI、无随机种子；其真车实验仅为乡村道路 1 km 单车横向车道保持且未报告任何闭环量化指标；全文未报告任何硬件、单步时延或内存占用；"比 ODE 快 1–5 个数量级"与"至少快一个数量级"两项断言在全文图表中不可追溯（可复算区间约 9.9×–101×）；参数量须区分 RNN 分量约 4,000（正式版正文）与含 CNN 头全模型 230,828（arXiv v2 Table 3，正式版 Extended Data Fig. 9 表体未能在文本层核验）；本文使用的图表编号以 NMI 正式版为准（与 arXiv v2 大面积错位），且正式版另有一篇更正（10.1038/s42256-022-00597-y）。**

---

## 7. 缺失信息（写成可执行动作）

1. ~~**【最高优先】人工打开 VoR PDF 第 21 页读 Extended Data Fig. 9，逐字抄录参数量表**~~ → **✅ 已于 2026-10-04 完成**（读图结果见 §7 核验 Q7 第 4 条）。**结论：正式版 ED Fig. 9 与 arXiv v2 Table 3 逐格一致**（CfC 全模型 **230,828** / RNN 分量 **4,184**；CfC-NoGate 与之完全相同；复算「Total − RNN」恒为 226,644）。→ **P1 的「不得写 <500 KB」红线由"C 级：仅 arXiv 可核"升为正式版可核，结论不变。** 残留动作：引用时须写明 901.7 KiB / 450.8 KiB 是**本项目的换算**（论文只给参数个数，未提量化精度与 KB）。
2. **同法读 Extended Data Figs. 5 / 6 / 8（pp.17 / 18 / 20），抄录 XOR、PhysioNet、IMDB 三张表的全部行**。→ **后果**：这三组数字的正式版出处目前不可核验，既有笔记的 XOR 99.42%、PhysioNet 0.839、IMDB 85.9/88.3 全部只有 arXiv v2 一个来源；若投稿时审稿人按正式版页号核对，会找不到数字。
3. **读并摘要更正 `10.1038/s42256-022-00597-y`（2022-11-29）**，明确它修正了哪一处（正文数字？图？作者信息？）。→ **后果**：正式版页脚已印 `corrected publication 2022`；若更正涉及本文被 P1 引用的数字或图表编号，本卡与既有笔记均需同步修订。
4. **向作者索取计时协议与硬件规格**（每个数据集、每个模型的 GPU/CPU 型号、精度、batch size、计时边界是否含数据加载与求解器自适应步、重复次数与方差）。→ **后果**：`Time per epoch` 全部是**单值**，正文的 `160×/220×/three times/8,752%` 与 Fig. 2 图注的 `100 fold` 全都**没有不确定度**；P1 无法据此推断任何 MCU 上的可行性（这也正是 `AGENTS.md` 禁止写"<500 KB"和禁止据此声称可上 MCU 的直接原因）。
5. **向作者索取 n = 5 的随机种子列表与逐次重复结果**（正式版全文 `seed` 0 命中）。→ **后果**：方差不可复算，"CfC vs ODE-LSTM 差 0.003 AUC" 是否超出机器噪声不可判断。
6. **要求作者在统一代码库/统一硬件/统一种子集上重跑全部基线，并给出配对比较与多重比较校正**（Tables 2/3/4 的 `†`/`*` 行来自 refs. 7 / 9 / 55 / 57）。→ **后果**：现有"CfC 更快更准"的一半证据是跨论文拼接，这正是项目 `AGENTS.md` §1 第 3 条禁止的引用方式。
7. **向作者索取真车车道保持试验的原始统计**：每模型试验次数、每次里程、**接管次数与接管率（每公里 / 每次机会）**、越界次数、转向误差或车道居中偏差，以及 `all trained networks were able to successfully complete` 的判据。→ **后果**：全文唯一真车闭环实验**不可复现、不可比较**，P1 无法据此建立任何控制器基线；P1 的七项指标此项对应"车道居中偏差"。
8. **索取正式版 Extended Data Figs. 3 / 4 / 7 的数值表（非图像）**，并补出各基线的超参数。→ **后果**：正式版把超参放进图里，`Description of hyperparameters` 只给名词解释不给搜索空间/搜索算法/调参预算，P1 的「同等调参预算」公平性无法对齐。

---

## 8. 关键数字（只抄本 PDF 明确印出的表格/正文，不得目测估读）

> 纪律：以下全部逐字抄自 **VoR 正式版文本层**。凡正式版表体为图像、数值不可读取者，**单列一行并注明"仅 arXiv v2 可核"**，不以任何方式估读。

### 8.1 正式版文本层可逐字读取（VoR Table 2 / Table 3 / Table 4 + 正文）

| 指标 | 值 | 不确定度 | 出处（表/图/节/页码） |
|---|---|---|---|
| 人活动识别 准确率 Cf-S | **87.04 ± 0.47** | s.d., n = 5 | Table 2, VoR p.5（996） |
| 人活动识别 准确率 CfC-mmRNN | 85.97 ± 0.25 | s.d., n = 5 | Table 2, p.5 |
| 人活动识别 准确率 CfC-noGate | 85.57 ± 0.34 | s.d., n = 5 | Table 2, p.5 |
| 人活动识别 准确率 **CfC（vanilla）** | **84.87 ± 0.42** | s.d., n = 5 | Table 2, p.5 |
| 人活动识别 准确率 最强 ODE 基线 Latent-ODE-ODE | 84.60 ± 1.3（8.49 min/epoch） | s.d., n = 5 | Table 2, p.5 |
| 人活动识别 准确率 ODE-RNN / Latent-ODE-RNN / RNN-VAE | 82.90 ± 1.6 / 83.50 ± 1.0 / 34.30 ± 4.0 | s.d., n = 5 | Table 2, p.5 |
| 人活动识别 每 epoch 时间 CfC / Cf-S / CfC-noGate | 0.084 / 0.097 / 0.093 min | **未报告**（单值） | Table 2, p.5 |
| Walker2D MSE CfC-mmRNN / CfC / CfC-noGate | **0.617 ± 0.006 / 0.643 ± 0.006 / 0.650 ± 0.008** | s.d., n = 5 | Table 3, VoR p.6（997） |
| Walker2D MSE LTC / Transformer | 0.662 ± 0.013 / 0.761 ± 0.032 | s.d., n = 5 | Table 3, p.6 |
| Walker2D MSE ODE-LSTM / ODE-RNN | 0.883 ± 0.014 / 1.904 ± 0.061 | s.d., n = 5 | Table 3, p.6 |
| Walker2D 每 epoch 时间 CfC / ODE-RNN / ODE-LSTM | 0.08 / 0.79 / 0.29 min | **未报告**（单值） | Table 3, p.6 |
| 事件式 sMNIST 准确率 CfC-mmRNN / CfC-noGate / CfC / Cf-S | **98.09 ± 0.18 / 96.99 ± 0.30 / 95.42 ± 0.21 / 95.23 ± 0.16** | s.d., n = 5 | Table 4, VoR p.6（997） |
| 事件式 sMNIST 准确率 ODE-LSTM / Lipschitz RNN | 95.73 ± 0.24 / 95.92 ± 0.16 | s.d., n = 5 | Table 4, p.6 |
| 事件式 sMNIST 准确率 ODE-RNN / CT-RNN / GRU-ODE | **72.41 ± 1.69 / 72.05 ± 0.71 / 80.95 ± 1.52** | s.d., n = 5 | Table 4, p.6 |
| 事件式 sMNIST 每 epoch 时间 Cf-S / CfC-noGate / CfC / CfC-mmRNN | 2.73 / 3.36 / 3.62 / 5.50 min | **未报告**（单值） | Table 4, p.6 |
| 事件式 sMNIST 每 epoch 时间 ODE-RNN / CT-RNN / GRU-ODE | 14.57 / 17.30 / 6.76 min | **未报告**（单值） | Table 4, p.6 |
| 闭式解 vs ODE 神经元轨迹的 MSE | **0.006** | **未报告**（无单位、无 n、无 CI） | Methods「Experimental details of the tightness experiment」, VoR p.8（999），行 1056–1058；图见 Fig. 2 |
| 紧致性实验的载体网络 | 训练好的 NCP：**19 neurons, 253 synapses** | — | Methods, p.8（999），行 1043–1044 |
| 车道保持 RNN 分量参数量（正文） | **`around 4,000`** | **未报告** | VoR p.6（997），行 645–647 |
| 真车试验规模 | 1 km 私有测试路；30 km h⁻¹ 恒速；30 Hz BlackFly PGE-23S3C 相机；3 h 原始数据 + 增广 | **未报告**（无试验次数、无接管次数、无成功率、无转向误差） | Methods「Setting of the driving experiment」, VoR p.9（1000），行 1151–1169 |
| 真车试验输入噪声 | 零均值高斯，方差 **σ² = 0.35** | 未报告（无重复、无各模型对比数字） | Extended Data Fig. 10 图注, VoR p.22 |
| 声称的训练/推理加速 | **`between one and five orders of magnitude`** | **未报告** | Abstract, VoR p.1（992），行 40–42 |
| 声称的"至少一个数量级" | `at least one order of magnitude faster`（出现在 3 处：p.3 行 215–218；p.4 行 423–425；p.5 行 486–488） | 未报告 | VoR pp.3 / 4 / 5（994 / 995 / 996） |
| 声称的 vs neural ODE 加速 | **`at least 100 fold faster`** | 未报告 | **Fig. 2 图注**, VoR p.4（995），行 476–478 |
| 声称的 accuracy-per-compute 改进 | **`over 150 fold improvements over ODE-based compartments`** | **未报告，且全文无对应图/表** | VoR p.3（994），行 239–241 |
| 声称的人活动识别加速 | **`a speed-up of more than 8,752% over ... (Latent-ODE-ODE)`** | 未报告 | VoR p.5（996），行 506–509 |
| 声称的 PhysioNet 加速 | `160 times faster ... compared with ODE-RNN and 220 times compared with continuous latent models`；`on average, three times faster than advanced discretized gated recurrent models` | 未报告 | VoR p.5（996），行 567–571 |
| 声称的事件式 sMNIST 加速 | `around 200–400% faster than ODE-based models such as GRU-ODE and ODE-RNN` | 未报告 | VoR p.5（996），行 537–540 |

### 8.2 正式版表体为图像，**参数量四项已读图核验**（2026-10-04）；XOR/PhysioNet/IMDB 仍仅 arXiv v2 可核 —— 引用时**必须注明出处版本**

| 指标 | 值 | 不确定度 | 出处 |
|---|---|---|---|
| 车道保持 CfC **全模型（CNN head + RNN）参数** | **230,828** | 确定性计数 | **NMI 正式版 Extended Data Fig. 9（p.21，本次读图核验 ✅）**；与 **arXiv v2 Table 3**（v2 p.18）逐格一致 |
| 车道保持 CfC **RNN 分量参数** | **4,184** | 确定性计数 | 同上（两版一致） |
| 车道保持 CNN 头（复算，五组一致） | 226,644 | — | 由两版参数表复算（230,828−4,184 = 259,733−33,089 = 233,139−6,495 = 227,728−1,084 = 235,052−8,408 = **226,644**，正式版 ED Fig. 9 读图后同样自洽 ✓） |
| 其余模型参数量 | CfC-mmRNN 235,052 / 8,408；NCP 233,139 / 6,495；Cf-S 227,728 / 1,084；LSTM 259,733 / 33,089；纯 CNN 2,124,901 | 确定性计数 | **NMI 正式版 ED Fig. 9（p.21，读图核验 ✅）**；与 arXiv v2 Table 3 一致 |
| Bit-stream XOR（event-based）准确率 | CfC **99.42 ± 0.42**；CfC-mmRNN 99.72 ± 0.08；CfC-noGate 96.29 ± 1.61；Cf-S 85.42 ± 2.84；ODE-LSTM 98.89 ± 0.26；GRU-D 97.90 ± 1.71；ODE-RNN 51.21 ± 0.37；LTC 49.11 ± 0.00 | s.d., n = 5 | **arXiv v2 Table 4**（v2 p.21）；正式版对应 ED Fig. 5（图像） |
| PhysioNet AUC | CfC-noGate 0.840 ± 0.003；CfC **0.839 ± 0.002**；CfC-mmRNN 0.834 ± 0.006；Phased-LSTM 0.836 ± 0.003；ODE-RNN 0.833 ± 0.009；Latent-ODE-ODE 0.829 ± 0.004；Cf-S 0.643 ± 0.018；LTC 0.6477 ± 0.010；RNN-VAE 0.515 ± 0.040 | s.d., n = 5 | **arXiv v2 Table 5**（v2 p.22）；正式版对应 ED Fig. 6（图像） |
| IMDB 测试准确率 | CfC-mmRNN **88.3 ± 0.1**；CfC-noGate 87.5 ± 0.1；**CfC（vanilla）85.9 ± 0.9**；LSTM 87.3 ± 0.4；HiPPO 88.0 ± 0.2；LTC 61.8 ± 6.1 | s.d., n = 5 | **arXiv v2 Table 6**（v2 p.23）；正式版对应 ED Fig. 8（图像） |

### 8.3 由 8.1 / 8.2 复算的比值（本卡复算，**非论文印出值**；正式版因表体为图像而无法复算，故一律基于 arXiv v2 与 VoR Table 3/4 的可读行）

| 复算项 | 算式 | 结果 | 与正文声称对照 |
|---|---|---|---|
| CfC vs ODE-RNN（Walker2D，**VoR Table 3 可读**） | 0.79 / 0.08 | **9.88×** | < 10×，**不满足** p.3/p.4/p.5 的 `at least one order of magnitude` |
| CfC vs ODE-RNN（XOR，arXiv v2 Table 4） | 4.11 / 0.75 | **5.48×** | 同上，XOR 任务上**全部 ODE 基线均 < 10×**（最大 CT-RNN 4.83/0.75 = **6.44×**） |
| CfC vs ODE-RNN（PhysioNet，arXiv v2 Table 5） | 16.5 / 0.1 | **165×** | 正文写 `160 times`（绝对数对不上，量级一致） |
| CfC vs Latent-ODE-ODE（PhysioNet） | 22.0 / 0.1 | **220×** | 正文 `220 times compared with continuous latent models` —— 220× 只对应 Latent-ODE-ODE 这一项；同组 Latent-ODE-RNN 为 6.7/0.1 = **67×** |
| CfC vs 离散门控组（PhysioNet 五个基线 0.5/0.5/0.7/0.7/0.3） | 各除以 0.1 | **5× / 5× / 7× / 7× / 3×**，区间 3–7×，组均值 ≈ **5.4×** | 正文 `on average, three times faster` —— **均值复算不出**，3× 只等于最快的 Phased-LSTM |
| CfC 系 vs Latent-ODE-ODE（人活动识别，**VoR Table 2 可读**） | 8.49 / 0.084（CfC）；8.49 / 0.097（Cf-S） | **101.1× / 87.5×** | 正文写 `more than 8,752%` —— 8,752 与 87.5 数值相近，**疑为把"倍"写作百分数**（见 ⚠ 第 5 条） |
| CfC 系 vs ODE-RNN / GRU-ODE（ET-sMNIST，**VoR Table 4 可读**） | 14.57/3.62 = 4.03×；14.57/3.36 = 4.34×；14.57/5.50 = 2.65×；6.76/5.50 = **1.23×** | 1.23×–5.34× | 正文写 `around 200–400% faster than ... GRU-ODE and ODE-RNN` —— **相对 GRU-ODE 仅 1.23×–2.48×**，口径不闭合（见 ⚠ 第 6 条） |
| 参数量 230,828 换算 | 230,828 × 4 B / 1024 | **901.7 KiB（fp32）** | **> 500 KB** → P1 不得写"<500 KB" |
| 参数量 230,828 换算 | 230,828 × 2 B / 1024 | **450.8 KiB（fp16）** | 需量化到 fp16 才达标 |
| 参数量 (x0−A) 4,184 换算 | 4,184 × 4 B / 1024 | **16.3 KiB（fp32，仅 RNN 分量）** | 正文 `around 4,000` 对应的就是这个分量 |

---

## ⚠ 内部不一致（逐条给出页码与逐字/复算证据）

1. **⚠内部不一致**：VoR p.5（996）行 486–488 称 `Each of these four proposed variants leverages our proposed solution and thus is at least one order of magnitude faster than continuous-time ODE models.` —— 但 **Table 3（p.6 / 997）** 中 `CfC-mmRNN 0.34` min/epoch **慢于**同为连续时间 ODE 模型的 `†ODE-LSTM 0.29`（0.29/0.34 = 0.85×，即**更慢**）。→ **"四个变体全部至少快一个数量级"被本文自己的 Table 3 证伪**（Table 4 中 CfC-mmRNN 5.50 < ODE-LSTM 6.35，方向相反，故该矛盾**专属 Table 3**）。
2. **⚠内部不一致**：VoR p.3（994）行 215–218 与 p.4（995）行 423–425 均称 `at least one order of magnitude faster`；但按 **Table 3** 复算，CfC 相对 ODE-RNN 仅 **9.88×**（0.79/0.08），相对 GRU-ODE 7.0×（0.56/0.08），相对 ODE-LSTM 3.6×（0.29/0.08），相对 LTC 9.75×（0.78/0.08）；**只有相对 CT-RNN（0.91/0.08 = 11.4×）超过 10×**。→ "至少一个数量级"在 Walker2D 上对多数 ODE 基线不成立。
3. **⚠内部不一致**：VoR p.4（995）行 476–478，**Fig. 2 图注**称 `at least 100 fold faster than neural ODEs at both training and inference on complex time-series prediction tasks`；但正文可读的 **Table 3** 上 CfC vs ODE-RNN = 9.88×，**Table 4** 上 CfC vs ODE-RNN = 4.03×（14.57/3.62），**两项都远低于 100×**。→ 图注的 "100 fold" 在本文自己的表里找不到对应。
4. **⚠内部不一致**：VoR p.3（994）行 239–241 称 `our results indicate that, when considering accuracy per compute time, CfCs exhibit over 150 fold improvements over ODE-based compartments` —— 全文**无任何图/表/定义**支撑该数字（"accuracy per compute time" 的计算方式、聚合范围、覆盖数据集均未给出）。
5. **⚠内部不一致**：VoR p.5（996）行 506–509 称人活动识别上 CfC 变体 `do so with a speed-up of more than 8,752% over the best-performing ODE-based instance (Latent-ODE-ODE)`。按 **Table 2** 复算：CfC/Latent-ODE-ODE = 8.49/0.084 = **101.1×**，Cf-S = 8.49/0.097 = **87.5×**。**8,752 与 87.5 数值相近，疑为把"倍数"写成"百分数"（量纲错误）**；若按"倍数"读，则最大为 101.1 倍而非 8,752%。→ 该数字**不可直接引用**。
6. **⚠内部不一致**：VoR p.5（996）行 537–540 称事件式 sMNIST 上 CfC 变体 `do so around 200–400% faster than ODE-based models such as GRU-ODE and ODE-RNN`。按 **Table 4** 复算：CfC vs ODE-RNN = 4.03×（+303%）、CfC-noGate = 4.34×（+334%）—— 落在区间内；但 **CfC-mmRNN vs ODE-RNN = 2.65×（+165%）**，且**相对 GRU-ODE 全部只有 1.23×–2.48×**（CfC-mmRNN 1.23×、CfC 1.87×、CfC-noGate 2.01×、Cf-S 2.48×）。→ "such as **GRU-ODE** and ODE-RNN" 的后半句不成立。
7. **⚠内部不一致**：VoR p.5（996）行 506–507 称人活动识别上 `the CfC variants Cf-S, CfC-noGate and CfC-mmRNN outperform other models with a high margin`，**独独略去 vanilla CfC** —— 而 Table 2 显示 `CfC 84.87 ± 0.42` 相对最强 ODE 基线 `Latent-ODE-ODE 84.60 ± 1.3` **仅高 0.27 个百分点**（两者 s.d. 分别为 0.42 与 1.3，差值远小于不确定度）。→ **选择性列举**：正文点名三个变体而回避第四个。
8. **⚠内部不一致**：VoR p.1（992）摘要称 `we obtain models that are between one and five orders of magnitude faster in training and inference compared with differential equation-based counterparts` —— **可复算的最大加速为 101.1×（人活动识别，Table 2）**，即约 2.0 个数量级；`five orders of magnitude`（10⁵×）在正式版的任何表/图中**均无对应测量**。→ 摘要措辞强度超出可追溯证据（既有笔记基于 arXiv v2 得出同一结论，本卡在正式版上复核成立）。
9. **⚠内部不一致**：VoR p.6（997）行 656–662 同一段先写 `For large-scale time-series prediction tasks, and where closed-loop performance matters24, CfCs can bring great value.`，随后写 `On the other hand, implicit ODE- and partial differential equation-based models17,29–31 can be beneficial in solving continuously defined physics problems and control tasks.` → 对"控制任务该用哪一类"**同段自相矛盾**；且第一句的唯一支撑是引文 24，本文**没有任何闭环控制性能实验**。
10. **⚠内部不一致**：VoR **Table 4** 的 `ODE-LSTM 95.73 ± 0.24` 与 `Lipschitz RNN 95.92 ± 0.16` 均**高于** `CfC 95.42 ± 0.21`，正文却称 `All CfC variants perform well on this task and establish the state-of-the-art on this task` → "all variants / SOTA" 的表述与表内 vanilla CfC 行不符（真正达到最高的是 CfC-mmRNN 98.09）。
11. **⚠内部不一致（跨版本）**：arXiv v2 Table 4 的文字断言 `ODE-based RNNs cannot solve the event-based encoding tasks regardless of their choice of solvers`，与同表 `ODE-LSTM 98.89% ± 0.26`（标 ODE-based = Yes）冲突；该句在正式版 p.5（996）行 554–556 **原样保留**，而 ODE-LSTM 在正式版 Table 4 中取得 **95.73 ± 0.24**（在 ET-sMNIST 上）—— **同一矛盾在正式版中依然存在，且表中亦无 solver 消融**。

---

## 字符数自查（实测）

> **计数口径（两种都报，避免歧义）**：`CJK` = 中文字符 + 中文标点（正则 `[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]`）；`可见总数` = 去掉 `**` 加粗标记与反引号后的**全部非空白字符**（含拉丁字母、数字、数学符号、箭头）。
> **复现命令**：取各节正文 → `-replace '\*\*','' -replace '`',''` → `-replace '\s',''` → 分别用上述正则与 `.Length` 计数。
> **口径歧义（须由你裁定）**：模板写"摘要 ≤400 字 / 结论 ≤350 字 / 方法一句话 ≤60 字"，未说明"字"是否含拉丁字符与公式。下表中 §2 两种口径皆达标；**§3 与 §4 只在"字 = 中文字符"口径下达标**。

| 节 | 限额 | CJK 实测 | 可见总数实测 | 判定 |
|---|---|---|---|---|
| §2 摘要 | ≤400 字 | **333** | 355 | ✓ 两种口径均达标 |
| §3 结论 | ≤350 字 | **292** | 396 | ✓ 按"字 = 中文字符"；✗ 按"字 = 全部字符"（超 46，超出部分**全部是页码与英文模型名**，如 `p.6 / 997`、`CfC-mmRNN`、`Cf-S`，属核验所需，未删） |
| §4 方法一句话 | ≤60 字 | **37** | 64 | ✓ 按"字 = 中文字符"；✗ 按"字 = 全部字符"（超 4，超出部分为公式 `σ(−ft)⊙g+(1−σ(−ft))⊙h`，为模板强制"输入→模型→输出"三要素所需） |

---

## 材料问题（交付时一并回报）

1. **任务书给的字符数与实测不符**：VoR 文件任务书标 `CHARS=77,259`，实测 79,140 字符（80,823 字节）；arXiv v2 文件任务书标 `PAGES=40, CHARS=62050`，实测 64,216 字符（65,835 字节）。两处差异均在 2.4%–3.5%，疑似计数口径不同（是否含 `===== PAGE n =====` 行、是否按字节计）。本卡在表头同时记录两个数字。
2. **VoR 的 Extended Data 图体不在文本层**：Extended Data Figs. 3/4/5/6/7/8/9 的表体均为图像，提取文本只保留图注。→ **XOR / PhysioNet / IMDB 三组结果与「参数量」这一 P1 最高优先项，在正式版上无法通过文本核验**，必须人工读图。
3. **nature.com 抓取被重定向**：`https://www.nature.com/articles/s42256-022-00556-7` 返回 `cross-origin redirect to https://idp.nature.com`，未能取得 ED Fig. 9 的数值表；Crossref 元数据（`api.crossref.org/works/10.1038/s42256-022-00556-7`）可正常读取，且已确认 **Correction 10.1038/s42256-022-00597-y（2022-11-29）** 的存在。
4. **arXiv v2 是 Science 家族排版**：v2 含 `One Sentence Summary` / `Main Text` / `List of Supplementary materials`，且 `Nature Machine Intelligence` 作为连续字符串在 v2 中 **0 命中**（唯一近似是参考文献 22 的期刊名跨行出现在 v2 p.30 行 1261–1262：`Nature` / `Machine Intelligence 2, 642–652 (2020)`，指 NCP 那篇）。→ 这解释了为什么 v2 的图表编号与正式版完全不同。
5. **既有笔记的 8 处需修订点已在上文 §6「与已有笔记的差异」列全**，其中 **#2（图表编号全错位）、#3（参数量正式版不可核）、#5（高速公路→乡村）、#7（确有更正）** 四条会直接影响 P1 稿件的正确性，建议优先回改 `literature/notes/p01-cfc-nmi2022.md` 与 `AGENTS.md` §1 的参数量口径条目（后者需补注"正式版 ED Fig. 9 文本层不可核验"）。
