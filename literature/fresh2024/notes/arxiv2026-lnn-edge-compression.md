# LNN 双阶段蒸馏与 Pareto 压缩（边缘电池预测）｜When Smaller Wins: Dual-Stage Distillation and Pareto-Guided Compression of Liquid Neural Networks for Edge Battery Prognostics

- **出处**：arXiv:2601.06227v3，v1 提交 **2026-01-09**（arXiv API：`published 2026-01-09T10:20:21Z`；v3 更新 2026-06-11，本机 PDF 第 1 页逐字印 `arXiv:2601.06227v3 [cs.LG] 11 Jun 2026`）｜ **类型**：预印本（**但已有正式版且已出版**：Springer **Lecture Notes in Computer Science**（Pattern Recognition / **ICPR 2026**），pp. 414–429，2026-07-25，DOI 见下）
- **作者**：Dhivya Dharshini Kannan, Wei Li, Wei Zhang, et al.（n=6；全序：Dhivya Dharshini Kannan, Wei Li, Wei Zhang, Jianbiao Wang, Zhi Wei Seh, Man-Fai Ng；新加坡理工 SIT + A\*STAR IMRE/IHPC；通讯作者 Wei Zhang）
- **DOI**：**10.1007/978-3-032-31441-3_28**（正式版，Crossref 逐字；ISBN 9783032314406 / 9783032314413）。arXiv 预印本本身**无 arXiv DOI**：arXiv API 返回的 `arxiv:doi` 字段为 **null**，故本卡不写 `10.48550/arXiv.2601.06227`
- **全文来源**：`literature/fulltext/fresh2024/arxiv2026-lnn-edge-compression__6e9ac96a.txt`（PAGES=15；任务书标 CHARS=45,113，**本机实测 46,286 字符 / 46,585 字节**，含 4 行提取头；MD5=`6e9ac96a9edcc61f45fbc75b83d155d4`）
- **分组**：2024+ 增量
- **★ 正式版核验**（执行日 **2026-10-06**，晚于 `00-scope.md` §2.1 声明的检索上界 2026-10-04；原始返回已存档）
  1. **arXiv comment 逐字**（arXiv API，2026-10-06，HTTP 200）：`Accepted at International Conference on Pattern Recognition, ICPR 2026. Code available at: https://github.com/Dhivya-DD17/DLNet` —— 与任务书所述一致；`journal_ref` **为空**（作者未回填正式版题录）。
  2. **Crossref 题名匹配**（模板指定的一次查询）：`https://api.crossref.org/works?query.bibliographic=When%20Smaller%20Wins%3A%20Dual-Stage%20Distillation%20and%20Pareto-Guided%20Compression%20of%20Liquid%20Neural%20Networks%20for%20Edge%20Battery%20Prognostics&rows=3` → **HTTP 200**，**第 1 条即命中正式版**：`10.1007/978-3-032-31441-3_28`，题名逐字与预印本**完全一致**，`container-title` = `Lecture Notes in Computer Science | Pattern Recognition`，`type` = `book-chapter`，`issued` = `{"date-parts":[[2026,7,25]]}`。第 2、3 条为不相关记录（BERT 压缩、图像压缩伪影）——该端点为 **OR 语义**。
  3. **DOI 记录反查**（`api.crossref.org/works/10.1007/978-3-032-31441-3_28`，HTTP 200）：`page 414-429`，作者逐字 `Dhivya Dharshini Kannan ; Wei Li ; Wei Zhang ; Jianbiao Wang ; Zhi Wei Seh ; Man-Fai Ng`（**与预印本同序 6 人**），`reference-count` 8，`is-referenced-by-count` 0。
  4. **T5 更正/撤稿检查**：同记录 `update-to` = **null**、`updated-by` = **null**、`relation` = `{}` → **Crossref 无更正或撤稿记录**（截至 2026-10-06）。
  5. **正式版可得性**：Unpaywall（`api.unpaywall.org/v2/10.1007/978-3-032-31441-3_28`，2026-10-06，HTTP 200）→ `is_oa: false`、`oa_status: "closed"`、`has_repository_copy: false`、`oa_locations: []`，`published_date: 2026-07-24` → **正式版无 OA 副本，本机取不到该章全文**。
  6. **代码材料核查**：GitHub REST API（2026-10-06，HTTP 200）确认 `Dhivya-DD17/DLNet` 存在且为**官方实现**（仓库 description 逐字含 `official implementation of the paper ... International Conference on Pattern Recognition, ICPR 2026`），**MIT License**，`created_at 2026-06-09`、`pushed_at 2026-08-14`；根目录含 `README.md` / `Install.md` / `LICENSE` / `Data_for_Main/` / `Docker Implementation/` / `Model Compression All/` / `Model train and Figure/` / `Prototype_Deployment/`。→ **本批中可复现材料最完整的一篇**。
  - **原始返回存档**：`literature/fresh2024/verify_two_cards.json`、`verify_two_cards_round2.json`、`verify_two_cards_round3.json`
  - **★ 按 `00-scope.md` §2.2 处置与理由（任务书要求明确说明）**
    - §2.2 原文：「arXiv 条目必须先做正式版核验（Crossref 题名匹配 + `journal_ref` 检查）才能进 A/B 档；**若存在正式版：以正式版为准，预印本降 C**」。
    - 本次核验结果是**比"已被接收"更强的事实**：不只是 `Accepted at ICPR 2026` 的 comment，而是**已在 Springer LNCS 出版、有 DOI、有页码（pp. 414–429）、有 ISBN、日期 2026-07-25**。→ **存在正式版**，故本条命中 §2.2 第二分句，**预印本降 C**。
    - §2.2 未给"已接收但尚未出版"的中间档；本案已越过该中间态，**不需要**适用"若确无正式版…截至 2026-10-04 仅有预印本"那一支。
    - **降 C 的性质**：降的是"**以 arXiv v3 的数字作证据**"的等级（正式版可能改动数值，本机又拿不到正式版全文），**不是**对该工作质量的判定；引用对象应改为正式版 DOI。
    - **一个减轻因素（不能替代核验）**：本机 arXiv v3 的排版是 **Springer LNCS 会议论文格式**（`Abstract.` / `Keywords:` / `⋆Corresponding author` / 页眉 `D. D. Kannan et al.`），即**已按会议版式排版**，与正式版内容多半一致；但"多半"不是证据，仍须逐格比对。
    - **升级条件**：取得 `10.1007/978-3-032-31441-3_28`（pp. 414–429）全文并逐格比对 TABLE 1–4 后按正式版重判。
- **证据等级初判**：**B** — 设计良好但有边界：公开数据集（MIT-Stanford）+ 多基线同超参对照（6 类模型 × 3 实现）+ **真机部署**（Arduino Nano 33 BLE Sense，nRF52840）+ MIT 许可的官方代码仓与 Docker 环境；但**单数据集、单设备、无随机种子、无置信区间、无显著性检验、无端侧功耗实测**，且核心卖点（学生优于教师）是单点估计。
- **档位建议**：**C（仅引用）** — 按 §2.2「存在正式版 → 预印本降 C」；**降档唯一原因是材料**（正式版 closed、本机未取得）。按母协议 §5 打分该工作本身**加权 15 分、具备 A/B 档资质**；取得正式版全文后即可上调。**不与"该文不重要"混为一谈**：它仍是本批唯一给出 LNN 类模型 MCU 真机字节数与时延的论文。
- **五维打分（各维 0–2，满分 20）**：D1=**1** D2=**1** D3=**2** D4=**2** D5=**2** → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = 3+2+4+2+4 = **15/20**
  - D1=1：取「**给出 P1 相邻环节的方法、术语与对照设计**」这一支 —— 它提供的正是 P1 七项指标里**端到端延迟**与 **MCU 内存占用**两项的**唯一同类实证与报告模板**（真 MCU、int8、字节数、单步时延、资格阈值）。**弱在哪（必须写明）**：它的任务（电池 SoH 预测）**与车辆纵横向闭环控制无关**，按 D1=0 的字面分句「或与车辆纵横向闭环控制无关」应给 **D1=0**；若取该读法，加权 = **12**（B 档）。**本卡取 D1=1 支，并在此显式声明该判断**（理由：`00-scope.md` §一明确本批要回答"端侧部署这块 2024+ 发生了什么"，而这是该问题上唯一有真机数字的论文）。**两种口径的档位结论相同（均由 §2.2 压至 C），故该判断不影响本卡结论。**
  - D2=1：有对照（6 类模型 × PyTorch/float16/int8 三实现，`with the same hyper-parameters`）+ **真机部署**；但**无统计检验、无种子、无 CI**，「对照 + 实车/闭环 + 有统计」三条不同时成立。⚠ 需注意：其"真机"是**单次推理的部署验证**，不是任何闭环控制；按 AD 口径**不得表述为实车验证**。
  - D3=2：**代码 + Docker + 公开数据集 + 完整导出链可直接复用**（GitHub 官方实现、MIT、8 个顶层目录含 `Prototype_Deployment`）。对 P1 的迁移是**管线级**而非任务级。
  - D4=2：2026 年，≤5 年。
  - D5=2：全文 + 4 张完整数据表 + MIT 许可代码仓 + Docker + 公开数据集。唯一不达标项是**效应量（无 CI / 无显著检验）**，该缺陷**已计入 D2，不重复扣分**（沿用本项目 `cfc-nmi2022.md` 的处理惯例）。
  - ⚠ 本卡严格遵守 0–2 制；**D4 一律指时效性**，未改写为其他含义。

---

## 1. 标题

`When Smaller Wins: Dual-Stage Distillation and Pareto-Guided Compression of Liquid Neural Networks for Edge Battery Prognostics`（预印本第 1 页逐字；与 Crossref 正式版题名**逐字一致**）｜中文直译：**当更小者胜：面向边缘电池预测的液态神经网络双阶段蒸馏与 Pareto 引导压缩**

---

## 2. 摘要（≤400 字；实测 **333 字**＝去空白字符数，脚本 `literature/scripts/count_card_sections.mjs`）

电池管理系统日益需要在严格的端侧约束下做准确的健康预测。本文提出 **DLNet**：对液态神经网络做双阶段蒸馏，把高容量模型变成紧凑、可边缘部署的学生模型。DLNet 先**用 Euler 离散化重写液态动力学以适配嵌入式**；再做双阶段知识蒸馏，迁移教师模型的时间行为并在进一步压缩后恢复之；在误差—代价联合目标下做 Pareto 引导选择，保留精度与效率平衡的学生。在广泛使用的数据集上评估，并在 **Arduino Nano 33 BLE Sense 上用 int8 部署**验证真机可行性。最终部署的学生在预测未来 100 个循环的电池健康时误差低至 **0.0066**，比教师低 **15.4%**；模型由 **616 kB 降到 94 kB**（降 **84.7%**），单次推理 **21 ms**。

---

## 3. 结论（≤350 字；实测 **347 字**）

作者总结：DLNet 用双阶段蒸馏与 Pareto 压缩把高容量教师变成紧凑可部署的学生。在 MIT-Stanford 电池数据集上验证，并在 Arduino Nano 33 BLE Sense 上以 int8 部署：最终学生预测未来 100 循环 SoH 的 MAE **0.0066**，比教师低 **15.4%**；模型由 **616 kB 降到 94 kB**（84.7%）；MCU 上单次推理 **21 ms**。作者把结论概括为"**更小者胜**"：在恰当监督与选择下，紧凑模型可既准确又可部署，框架亦可推广到其他资源受限的工业分析任务。

**本卡核验发现的局限（非作者自承**，原文无局限段）：① 未给 Euler 步长 Δt 的数值与选取准则；② 未测端侧功耗；③ 教师 1.9 ms 与学生 21 ms 分属工作站与 MCU 两平台却同列一表；④ 无种子与置信区间。

---

## 4. 方法一句话（≤60 字；实测 **57 字**）

LNN 教师（ODE）→ Euler 学生池 → 蒸馏+Pareto 选择 → 剪枝+再蒸馏 → int8/LiteRT 部署到 MCU。

---

## 5. 图表清单（占位符，覆盖全部图表）

> 全文共 **3 张 Figure + 4 张 TABLE = 7 个**（≤12，**全部收录**）。图注逐字，截断至 100 字符（截断处加 `…`）。四张表的**表体在本 .txt 中全部可读**（数值见 §8）。

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-DLNET-1} | Fig. 1 | `Fig. 1: An illustration of the system architecture of DLNet with two compression, distillation, and model selection stages followed by edge deployment.` | **全文总架构图**，唯一权威流程图。链条逐字可读：`Euler` ← `LNN ODE` → `Discretization`；教师/学生预测 → `MSE / Cosine (Distillation Loss)` 与 `MSE (True Loss)` 按 `λ` / `1−λ` 加权；`Hidden Dimension 128 → 64 → 2 …`；`Global Structured Pruning`；`Cost Objective` / `Error Objective` → `Pareto-Optimal Student Models`；`Quantization + LiteRT Conversion` → `C Header File` → `Edge Deployment`。**P1 若要画自己的"压缩—部署"流程图，这是可直接对照的唯一版式。** |
| {FIG-DLNET-2} | Fig. 2 | `Fig. 2: Illustration of student models from the two distillation stages in the error–cost space. Pareto-selected students with low error-cost are highlighted.` | 两个子图 (a) 第一阶段 / (b) 第二阶段，坐标轴为 `Error` 与 `Cost`；图例 `Cosine Students` / `MSE Students` / `Teacher` / `Pareto-Optimal`。**P1 若要论证"选型应看误差—代价前沿而非单点精度"，这是唯一可引的图。** |
| {FIG-DLNET-3} | Fig. 3 | `Fig. 3: A demonstration of DLNet with Arduino-based on-device deployment.` | 真机演示照片（含 `DLNET Arduino Deployment` 与 `Remote Webpage`）。**是"真 MCU 部署"的物证图**，但**不是**控制闭环实验图。 |
| {TAB-DLNET-1} | Table 1 | `Table 1: Comparison of ML models implemented in PyTorch, LiteRT with float16, and LiteRT with int8 under two minimized objectives. Error metrics include MAE, RMSE, and MAPE (%). Cost metrics include inference time (ms) and model size (kB). Model eligibility for error requires MAE ≤0.01. Model eligibility for cost requires int8 format and a quantized model size ≤500 kB.` | **本卡最重要的表**：6 类模型 × 3 实现 = 18 行，含 LNN/CNN/TCN/LSTM/GRU/Transformer 的 MAE、RMSE、MAPE、推理时延、模型大小与 Error/Cost 两列 ✓/×。**表注里的 500 kB 是本文自设的边缘资格判据**——P1 写"<500 KB"时最可直接对照的同类口径（用法见 §6-(e)）。 |
| {TAB-DLNET-2} | Table 2 | `Table 2: The performance of the student models in the first stage distillation with different hidden state dimensions in {2^1, . . . , 2^7} = {2, . . . , 128} and MSE and Cosine losses. Error indicators include MAE (×10−2), RMSE (×10−2), MAPE (%), uncertainty (×10−3), and confidence. Cost indicators include inference time (ms), model size (kB), energy (×10−8 kWh), and CO2 emission (×10−8 kg).` | 第一阶段：教师 + 14 个学生（7 维 × 2 损失）。**"更小者胜"的原始数据在此**（dim-16 Cosine 学生 MAE 0.75×10⁻² < 教师 0.78×10⁻²）；同时给出**scale 的边界**（dim-2 学生误差翻倍到 1.96/1.93×10⁻²）。 |
| {TAB-DLNET-3} | Table 3 | `Table 3: The performance of the student models in the second distillation with different sparsity in {0.1, . . . , 0.9} based on the three optimal students from the first distillation. Error indicators include MAE (×10−2), RMSE (×10−2), MAPE (%), uncertainty (×10−3), and confidence. Cost indicators include inference time (ms), model size (kB), energy (×10−8 kWh), and CO2 emission (×10−8 kg).` | 第二阶段：M-4 / C-16 / C-64 三个精英 × 稀疏度 0.1–0.9。**含"剪枝—精度非单调"的关键反例**（M-4 稀疏度 0.8 的 MAE 0.86 反而优于 0.5 的 1.02）。 |
| {TAB-DLNET-4} | Table 4 | `Table 4: Comparison between the teacher on a workstation and DLNet on an Arduino Nano MCU. Error metrics including MAE, RMSE, MAPE, MAE10, and MAE100 are reported in ×10−2. Efficiency metrics include memory (MB), model size (kB), FLOPs (M), parameter count (×103), and inference time (ms). The gap row reports relative change (%) of DLNet with respect to the teacher.` | **final 部署产物的唯一权威数字表**（P1 复刻口径的模板）：MAE 0.78→0.66、Model Size 616.1→94.1 kB、# Paras 155.8→70.5（×10³）、FLOPs 0.288→0.068 M、Inference 1.9→21.1 ms、Memory 640.43→0.02 MB。⚠ Gap 行的 RMSE/MAPE 与两列不自洽（见 ⚠1），且 Inference/Memory 两项跨平台（见 ⚠2）。 |

---

## 6. 对 P1 的用处

### 与 P1 的关系：**相邻**（**方法层：直接可用**；**任务层：无关**——它做电池 SoH 预测，不做车辆控制）

这是本项目"`<500 KB` / 可上 MCU"痛点**唯一有真机字节数的 2024+ 证据**。它与 P1 共享"把连续时间（液态）模型压到端侧"这一命题，但**任务、指标、时序尺度全都不同**。

### (a) Euler 离散化具体怎么做；步长怎么选；离散化后还算不算"连续时间模型"

**教师（真连续时间）**：式 (1) `dh(t)/dt = −αh(t) + β tanh(W h(t) + ū)`（`h(t)` 隐藏状态，`α`/`β` 可训练，控制衰减与非线性；`W` 可学习动力学矩阵；`ū` 是输入 `X` 的均值）。式 (2) `h_T = odeint(dh(t)/dt, h_0, t ∈ [0, T])` —— 逐字：`This ODE is integrated once per inference to obtain the evolved latent state hT`。

**学生（显式/前向 Euler）**：式 (3) `h(t + ∆t) = h(t) + ∆t · dh(t)/dt`；代入教师 ODE 得式 (4) `h(t + ∆t) = h(t) + ∆t · (−αh(t) + β tanh(W h(t) + ū))`。
另加**低秩 + 对角稳定**参数化（式 5）：`W′ = diag(w_diag) + (1/r) U Vᵀ`，参数量由 `O(d²)` 降到 `O(d + dr)`（`r < d`）。

| 问题 | 答案 |
|---|---|
| **把连续动力学离散成什么形式？** | **一步显式 Euler 更新**，逐字：`replaces iterative ODE-solver-based integration at inference with a solver-free and learnable state-update`；`Explicit Euler-based discretization reformulates the hidden-state evolution into a single solver-free tensor update`。 |
| **步长 `∆t` 怎么选？** | **原文未给数值，也未给选取准则。** `∆t` 仅以符号出现在式 (3)(4)；全文无 step size / 时间步长讨论，也不在 Table 1–4 的任何列中。→ **这是 P1 复现该流程的最大单点空白**（见 §7-1）。 |
| **为什么要离散化？** | **不是为精度，是为导出工具链。** 逐字：`A widely-used embedded inference standard is LiteRT … LiteRT, however, does not support general ODE solvers or iterative numerical integration operators, so a continuous-time teacher model cannot be exported directly to LiteRT for edge deployment.` → 离散化是**部署约束驱动的重写**。 |
| **离散化后还算"连续时间模型"吗？** | **按原文口径：不算。** 原文的措辞层级清楚：只有**教师**被称 `continuous-time`（`Its continuous-time state dynamics are modeled through a learned ODE system`；`the teacher model, while accurate, relies on continuous-time ODE solving that is heavy for edge deployment`）；学生一律称 `Euler-based discretized variants` / `solver-free … state-update`，并明说 `Euler is only an approximation of the teacher' ODE dynamics and there can be a non-trivial performance gap`（正因如此才需要蒸馏）。 → **部署产物是"对连续时间动力学的离散近似"，不是连续时间模型。** |

### (b) 参数量与内存的完整口径（★ 本卡对 P1 的第二重要产出）

| 量 | 教师 | 最终部署学生（DLNet） | 出处 |
|---|---|---|---|
| **模型类型** | LNN 教师（learned ODE，`odeint`） | **M-4 @ 稀疏度 0.1**，post-training **int8** + LiteRT → C header | §3.5、Table 4 |
| **参数量** | **155.8 × 10³ = 155,800** | **70.5 × 10³ = 70,500**（↓54.7%） | Table 4 |
| **模型（文件）大小** | **616.1 kB** | **94.1 kB**（↓84.7%） | Table 4 |
| **内存** | **640.43 MB**（工作站） | **0.02 MB**（MCU 张量区） | Table 4 |
| **FLOPs** | 0.288 M | 0.068 M（↓76.4%） | Table 4 |
| **量化位宽** | 无（PyTorch 全精度） | **int8**（导出期 post-training 量化）；float16 亦有对照 | §3.5、Table 1 |
| **单步推理** | 1.9 ms（工作站） | **21.1 ms（MCU）** / 0.14 ms（同工作站） | Table 4、§3.5 |
| **目标硬件** | — | **Arduino Nano 33 BLE Sense** | §3.5、Fig. 3 |

**目标硬件逐字（最高价值的一句）**：`The board is a Nordic nRF52840 BLE microcontroller with 1 MB on-chip flash memory and 4 kB page size.`

- **是不是 MCU**：**是真 MCU**（不是 MCU 级 SBC）。论文显式把 Arduino 与 Raspberry Pi 对比：`Arduino is chosen as the edge platform because it is widely used in embedded prototyping and represents more compact deployments than typically single-board edge devices such as Raspberry Pi.`
- **Flash 上限：1 MB（论文原文）**。**RAM 上限：论文未给** —— 全文无 RAM/SRAM 容量数字。nRF52840 的 RAM 容量须查 Nordic 数据手册，**本卡不引外部数字**（见 §7-2）。
- **部署链**（P1 可直接照抄）：`post-training int8 quantization` → `export into a LiteRT-compatible graph` → `convert the exported model into an embedded C representation`（C header 文件）；`We allocate a fixed tensor arena, load the model, register the required operators, and run inference`。
- **一个对 P1 有直接约束的硬件事实**：`when practical settings are considered for edge devices such as Arduino Nano 33 BLE Sense and ESP32, there is no native hardware support for float16.` → **端侧只能用 int8，float16 不算可部署格式**。
- **★ 论文自设的边缘资格判据（逐字，P1 最可直接对照的口径）**：`Model eligibility for error requires MAE ≤0.01. Model eligibility for cost requires int8 format and a quantized model size ≤500 kB.`
  - ⚠ 三条限制：① 这是**该文的工程判据**，不是 MCU 厂商或车规限制；② `500 kB` 指**模型文件字节数**，不是参数量换算；③ 原文写 `kB`，**未说明是 kB(1000 B) 还是 KiB(1024 B)**。

### (c) 双阶段蒸馏与 Pareto 选择的精度损失（逐字抄表）

**Table 1（教师候选，MAE）**：LNN `PyTorch 0.00781 → LiteRT float16 0.00892 → LiteRT int8 0.00934`（尺寸 `616.1 → 199.6 → 197.4 kB`）→ **量化使误差上升，但仍在 0.01 阈值内**。

**Table 2（第一阶段，MAE ×10⁻²；教师 0.78）**：
- MSE 学生（dim 128 / 64 / 32 / 16 / 8 / 4 / 2）：`1.02 / 1.01 / 1.02 / 1.03 / 0.90 / 0.84 / 1.96`
- Cosine 学生（同序）：`1.18 / 0.78 / 0.90 / 0.75 / 0.88 / 1.10 / 1.93`
- 模型大小（kB，两损失相同）：`685 / 460 / 371 / 333 / 315 / 306 / 302`（教师 616）
- → **最优学生（Cosine, dim 16）MAE 0.0075 < 教师 0.0078，同时体积 333 kB**；**dim 2 崩到 0.0196/0.0193（2.51×/2.47× 于教师）**。
- 第一阶段 Pareto 精英：**M-4、C-16、C-64** 三个。

**Table 3（第二阶段 = 剪枝 + 再蒸馏，MAE ×10⁻²；教师 0.78）**：
- **M-4**（稀疏度 0.1 / 0.2 / 0.3 / 0.4 / 0.5 / 0.8 / 0.9）：`0.76 / 0.91 / 0.99 / 1.08 / 1.02 / 0.86 / 1.30`；尺寸 `273 / 245 / 220 / 198 / 180 / 138 / 128 kB`
- **C-16**（0.1 / 0.2 / 0.3 / 0.4 / 0.5 / 0.9）：`1.31 / 1.48 / 0.81 / 1.23 / 1.78 / 2.20`；尺寸 `281 / 251 / 223 / 199 / 182 / 143 kB`
- **C-64**（仅 0.1 / 0.2 稳定）：`1.01 / 1.03`；尺寸 `404 / 366 kB`
- → 第二阶段 Pareto 精英 **4 个**：M-4 @ 0.1 / 0.2 / 0.5，C-16 @ 0.3。**最终部署选 M-4 @ 稀疏度 0.1。**

**Table 4（教师 → 最终部署学生，含 Gap 行）**：MAE `0.78 → 0.66`（↓15.4%）；RMSE `0.85 → 0.73`（表给 ↓13.9%，**复算为 14.1%，见 ⚠1**）；MAPE `0.91 → 0.76`（表给 ↓15.8%，**复算为 16.5%，见 ⚠1**）；MAE10 `0.51 → 0.43`（↓15.6%）；MAE100 `1.28 → 1.03`（↓19.4%）。
→ **注意方向**：这不是"压缩导致精度损失"，而是**蒸馏后的学生反超教师**；论文用 `a non-monotonic trends, e.g., increasing sparsity does not consistently worsen MAE` 明确否定了"剪枝必然掉精度"的假设。**P1 引用时必须写清这是该文在电池回归任务上的一次观测，不能外推为"压缩总能提精度"。**

### (d) 单步推理时延与功耗

| 项 | 数值 | 出处 |
|---|---|---|
| **MCU 单步推理时延** | **21 ms**（Table 4 印 `21.1`；摘要与 §3.5 写 `21 ms`） | Table 4、Abstract、§3.5 |
| 工作站上同一学生 | **0.14 ms**（`7% of the teacher's time only`） | §3.5 |
| 教师工作站推理 | **1.9 ms** | Table 4 |
| **端侧功耗** | **无。全文没有任何 mW / W 级功率测量。** | — |

- 关于"21 ms 可接受"的**论证方式**（逐字，对 P1 是重要陷阱）：`DLNet completes one inference in 21 ms on Arduino, which is acceptable for battery analytics since degradation evolves slowly over long time scales.` → **该论证依赖任务的慢变特性，不能搬到闭环控制。**
- 表中 `Energy (×10⁻⁸ kWh)` 与 `CO2 (×10⁻⁸ kg)` 来自 `EmissionsTracker from CodeCarbon`，属**主机侧软件估算**（§3.1 明确 `All models are trained on a workstation with an NVIDIA RTX 4050 GPU`），**不是 MCU 实测功耗**。→ **P1 若需"端侧功耗"指标，本篇不能作出处。**

### (e) ★ 这套压缩流程能不能搬到 CfC 上？需要什么改动？搬过去后 P1 能不能写"<500 KB"？

**结论：能搬，且是本批最可操作的一条路线；但"Euler 离散化"这一步对 CfC 是多余的，真正能搬的是后三步。**

1. **❌ 第一步（Euler 离散化）对 CfC 不需要。** 本文的教师是 **LTC 式 ODE**（`dh/dt = −αh + β tanh(Wh + ū)`），必须靠数值积分；而 **CfC 本身就是该 ODE 的闭式近似**（`x(t) = σ(−f·t)⊙g + (1−σ(−f·t))⊙h`），**不含求解器**。→ 本文离散化的**动机**（`LiteRT does not support general ODE solvers`）在 CfC 上不成立。
   - **但**：CfC 的算子集（`sigmoid`/`tanh`/逐元素乘/matmul）是否**全部被 LiteRT 支持**，必须**实测**，不能由本文推断（本文只证明了"ODE 求解器不被支持"）。
2. **✅ 真正能搬的四步**：
   - ① **双阶段"蒸馏 → 剪枝 → 再蒸馏"流程**（§2.2–2.4 完整可复刻）；
   - ② **Pareto 双目标选择**：误差目标 5 项、代价目标 4 项、阈值剔除 + 支配关系筛精英（式 7–9）。**这一步是本文最可迁移的方法学贡献**；
   - ③ **导出链**：int8 后训练量化 → LiteRT 图 → C header → MCU（含 fixed tensor arena）；
   - ④ **"资格阈值 + 逐模型全列"的报告法**（误差阈值、尺寸阈值、FLOPs、参数量、时延、字节数全列）。
3. **必须改的口径**：
   - `f_err` 的 5 项（MAE/RMSE/MAPE/不确定性/置信度）→ 换成 P1 的控制指标（跟车误差 RMSE、加速度平方积分、Jerk 峰值、车道居中偏差、前轮转角方差）；`MAE10/MAE100`（近端/远端）这一分解方式可映射为 P1 的**短/长时域跟车误差**。
   - `f_cst` 的 4 项（模型大小/推理时间/能量/CO₂）保留，但**能量项必须改成 MCU 侧实测**（本文是 CodeCarbon 主机估算）。
   - **教师必须先训好并可冻结**：本文的"更小者胜"完全依赖"高容量教师 + 冻结作知识源"。**P1 目前连 CfC 控制器的实测参数量都没有**（只有 NMI 2022 的车道保持文献值），这是搬流程的**前置阻塞项**。
   - **量化必须做控制指标的回归测试**：回归任务的 MSE 退化不等于控制闭环的性能退化。本文 Table 1 已给出警示：**LNN 的 int8 使 MAE 由 0.00781 升到 0.00934**；**LSTM 由 0.00832 崩到 0.09570、GRU 由 0.00460 到 0.01807**。
4. **★ 一个必须写进 P1 的风险（如不慎会变成硬伤）**：本文的 21 ms 之所以"可接受"，是因为**电池退化是慢变量**。**P1 是闭环控制**，21 ms 在控制回路里是**不可接受**的量级（对照：`meeting2` 的 Claussmann et al. 给出高速运动规划需在 **10 ms 量级**内返回解）。→ **P1 引用本文时，只能引它的"压缩—部署管线与报告口径"，绝不能引它的"时延可接受"论证。**

5. **★ P1 能不能写"<500 KB"？——合规/不合规写法对照（严格按 `auto-driving/AGENTS.md` §1 参数量口径）**

> **前置事实（不得回避）**：CfC 原文（NMI 2022）报告的是**车道保持模型**：**递归分量 4,184 参数、含 CNN 感知头全模型 230,828 参数**；fp32 ≈ **902 KiB > 500 KB**，fp16 ≈ 451 KiB 才达标；且该文**未报告任何硬件**。→ 在拿到本项目自己的实测参数量之前，P1 **不得写"<500 KB"**。

- **❌ 不合规写法（禁止）**
  > 「OTF-CfC 是一个 **<500 KB** 的模型，可直接部署到 MCU。」
  四条硬伤：① **未写量化精度**；② **未说明是否含感知头**（4,184 与 230,828 差 55 倍）；③ 把 CfC 原文 fp32 902 KiB 超 500 KB 的既有事实掩盖掉；④ **未区分"论文报告值"与本项目实测值**，等于把未实测的结论写成已成立。

- **✅ 合规写法 A（本项目已有实测时）**
  > 「在 **[MCU 型号，如 nRF52840]** 上以 **int8** 量化导出后，OTF-CfC 的部署产物为 **XX kB**（**不含**感知头；RNN 分量 **XX,XXX** 参数，含感知头全模型 **XXX,XXX** 参数），张量区 **XX kB**，单步推理 **XX ms**（编译器 **X**，优化选项 **-O2**），控制周期 **XX ms**。作为参照，CfC 原文报告的全模型为 **230,828** 参数（含 CNN 头，NMI 2022 Extended Data Fig. 9），其 **902 KiB（fp32）/ 约 226 KiB（int8）**均系**本项目换算**，论文未报告任何硬件或字节数。」

- **✅ 合规写法 B（尚无实测、只能引文献口径时）**
  > 「我们尚无 OTF-CfC 的 MCU 实测。可资对照的同类证据是 **Kannan 等（ICPR 2026，LNCS pp. 414–429）** 在 **Arduino Nano 33 BLE Sense（nRF52840）** 上以 **int8** 部署 LNN 学生模型的报告：模型 **94.1 kB**、参数量 **70.5×10³**、单次推理 **21.1 ms**、张量区 **0.02 MB**；该文的**边缘资格判据为「int8 量化后模型大小 ≤500 kB」——这是该文的工程判据，不是 MCU 厂商或车规限制**，且其任务为**电池 SoH 预测**，时序尺度与控制回路不可直接类比。」

- **三条纪律**（写给 P1 的作者）：
  1. **500 kB 只能作为"他人论文的资格判据"引用**，不得写成"MCU 的硬上限"或"车规要求"；
  2. 任何 KB 数字必须同时给出**量化精度 + 是否含感知头 + 是论文报告值还是本项目换算/实测**；
  3. 报量化时**必须同时报量化后的控制指标退化**（本文 Table 1 已给出 LNN/LSTM/GRU 的量化退化反例）。

**引用时必须带的限定语（一句）**

> **Kannan 等（ICPR 2026；本卡数值出自 arXiv:2601.06227v3 预印本）在电池 SoH 预测任务上报告：以 int8 量化部署到 Arduino Nano 33 BLE Sense（nRF52840，1 MB Flash）的 LNN 学生模型为 94.1 kB、70.5×10³ 参数、单次推理 21.1 ms，且"学生优于教师"；但该文未报告 Euler 步长 Δt 的取值、未测端侧功耗、其"21 ms 可接受"的论证依赖电池退化的慢变特性，教师与学生的时延/内存数字分属工作站与 MCU 两个平台。**

---

## 7. 缺失信息（≥3 条，写成可执行动作）

1. **【最高优先】索取或复算 Euler 步长 `∆t` 的取值与选取准则**（是否与数据采样周期绑定？是否按 `T` 与隐藏层深度确定？是否随学生维度变化？）。→ 全文 `∆t` 仅以符号出现在式 (3)(4)。→ **后果**：**迁移到 CfC 之外**倒不致命（CfC 无求解器），但**P1 若要复现本文的双阶段流程作为方法学对照**，缺这一步无法复现其学生池；且 `∆t` 与 `1/r UVᵀ` 的低秩因子 `r` 一起决定学生容量，二者缺一则 Pareto 前沿不可重建。
2. **索取 nRF52840 上的 RAM 占用明细**：模型张量区（0.02 MB 已给）、激活峰值、LiteRT 解释器与算子表开销，以及 `1 MB Flash` 中模型实际占用比例。→ 论文只给 `1 MB on-chip flash memory and 4 kB page size`，**全文无任何 RAM 容量数字**。→ **后果**：P1 若声明"可上 MCU"，**必须报 MCU 型号的 RAM 上限**，而本文**不能**提供这一半信息（须查 Nordic 数据手册或自行实测）。
3. **索取端侧功耗实测**（MCU 工作时平均电流/功率、单次推理能量），替换 CodeCarbon 的主机侧估算。→ 全文无 mW/W 级数字；`Energy (×10⁻⁸ kWh)` 来自 `EmissionsTracker from CodeCarbon`。→ **后果**：P1 的"端侧"证据链若要含功耗，须自测；本文不可作出处。
4. **索取训练细节与随机种子**：优化器、学习率、批大小、`λ` 的上下界具体值、`∆λ` 之外的超参，以及全部实验的随机种子。→ §3.1 只给 `200 epochs`、`λ` 由 0.1 每 epoch +0.004 至 0.9、`τ = τ′ = 100`、数据划分 80:20；**无种子**。→ **后果**："更小者胜"（0.0078 → 0.0066）**无不确定度**，无法判断该 15.4% 降幅是否超出运行间波动；这是 P1 引用其"学生反超教师"时最脆弱的一点。
5. **取得正式版全文并逐格比对**（`10.1007/978-3-032-31441-3_28`，pp. 414–429）。→ 2026-10-06 实测 Unpaywall：`is_oa:false`、`oa_status:"closed"`、`has_repository_copy:false`、`oa_locations:[]`。→ **后果**：本卡全部数字的正式版地位未定，档位被 §2.2 压在 C。
6. **澄清 Table 4 中跨平台的 Inference 与 Memory 两行**：教师 1.9 ms / 640.43 MB 是工作站值，学生 21.1 ms / 0.02 MB 是 MCU 值，但 Gap 行把它们当成同一口径的相对变化（`↑1002`、`↓100.0`）。→ **后果**：P1 引用"↑1002%"会得出"部署后慢 10 倍"的误导结论；真实可比的只有 §3.5 里同工作站的 0.14 ms vs 1.9 ms（= 7%）。

---

## 8. 关键数字（只抄本 .txt 明确印出的表格/正文，不得估读）

> 纪律：以下全部逐字抄自 arXiv:2601.06227v3 的**文本层**（Table 1–4 的表体在本 .txt 中全部可读）。误差类指标的单位见各表注（Table 2/3/4 为 ×10⁻²），本卡一律按原表单位抄录并标注。

### 8.1 部署产物与目标硬件（Table 4 + §3.5）

| 指标 | 教师 | DLNet（最终部署） | Gap（原文） | 出处 |
|---|---|---|---|---|
| MAE（×10⁻²） | 0.78 | **0.66** | ↓15.4 | Table 4 |
| RMSE（×10⁻²） | 0.85 | 0.73 | ↓13.9（**复算 14.1，见 ⚠1**） | Table 4 |
| MAPE（×10⁻²） | 0.91 | 0.76 | ↓15.8（**复算 16.5，见 ⚠1**） | Table 4 |
| MAE10（×10⁻²） | 0.51 | 0.43 | ↓15.6 | Table 4 |
| MAE100（×10⁻²） | 1.28 | 1.03 | ↓19.4 | Table 4 |
| Memory (MB) | 640.43 | **0.02** | ↓100.0 | Table 4 |
| Model Size (kB) | 616.1 | **94.1** | ↓84.7 | Table 4 |
| FLOPs (M) | 0.288 | 0.068 | ↓76.4 | Table 4 |
| # Paras (×10³) | 155.8 | **70.5** | ↓54.7 | Table 4 |
| Inference (ms) | 1.9 | **21.1** | ↑1002 | Table 4 |
| 同工作站推理 (ms) | 1.9 | **0.14**（`7% of the teacher's time only`） | — | §3.5 |
| 目标硬件 | — | **Arduino Nano 33 BLE Sense** | — | §3.5 |
| MCU 芯片 | — | `Nordic nRF52840 BLE microcontroller` | — | §3.5 |
| Flash | — | **1 MB**（on-chip） | — | §3.5 |
| Flash 页大小 | — | **4 kB** | — | §3.5 |
| RAM 上限 | — | **未报告** | — | — |
| 量化 | — | post-training **int8**，LiteRT → C header | — | §3.5 |

### 8.2 Table 1（教师候选筛选；MAE / Inference ms / Size kB）

| Model | Version | MAE | RMSE | MAPE | Inference | Size | Error | Cost |
|---|---|---|---|---|---|---|---|---|
| CNN | PyTorch | 0.03997 | 0.04148 | 4.59535 | 1.569 | 1418.1 | × | × |
| CNN | LiteRT float16 | 0.00659 | 0.00721 | 0.76039 | 0.541 | 373.9 | ✓ | × |
| CNN | LiteRT int8 | 0.01298 | 0.01337 | 1.42713 | 0.471 | 371.3 | × | ✓ |
| TCN | PyTorch | 0.03451 | 0.03501 | 3.91782 | 1.969 | 1351.8 | × | × |
| TCN | LiteRT float16 | 0.00877 | 0.00999 | 1.01778 | 0.416 | 363.5 | ✓ | × |
| TCN | LiteRT int8 | 0.01113 | 0.01207 | 1.27697 | 0.451 | 362.2 | × | ✓ |
| LSTM | PyTorch | 0.00832 | 0.00990 | 0.96733 | 2.047 | 831.4 | ✓ | × |
| LSTM | LiteRT float16 | 0.09316 | 0.09586 | 10.60240 | 1.245 | 638.6 | × | × |
| LSTM | LiteRT int8 | 0.09570 | 0.09847 | 10.89683 | 1.272 | 960.2 | × | × |
| GRU | PyTorch | 0.00460 | 0.00513 | 0.53256 | 3.968 | 816.6 | ✓ | × |
| GRU | LiteRT float16 | 0.00371 | 0.00425 | 0.42814 | 1.080 | 855.9 | ✓ | × |
| GRU | LiteRT int8 | 0.01807 | 0.02145 | 2.02840 | 1.137 | 1143.6 | × | × |
| Transformer | PyTorch | 0.00719 | 0.00763 | 0.83094 | 2.389 | 1327.8 | ✓ | × |
| Transformer | LiteRT float16 | 0.00659 | 0.00719 | 0.76240 | 0.658 | 413.5 | ✓ | × |
| Transformer | LiteRT int8 | 0.00900 | 0.00969 | 1.03755 | 1.215 | 377.6 | ✓ | ✓ |
| **LNN (ours)** | PyTorch | **0.00781** | 0.00850 | 0.90772 | 1.912 | **616.1** | ✓ | × |
| **LNN (ours)** | LiteRT float16 | 0.00892 | 0.00950 | 1.03398 | 0.081 | 199.6 | ✓ | × |
| **LNN (ours)** | LiteRT int8 | **0.00934** | 0.01000 | 1.08152 | 0.132 | **197.4** | ✓ | ✓ |

不确定度：**全表无**。表注给出资格判据：`MAE ≤0.01`、`int8 format and a quantized model size ≤500 kB`。

### 8.3 Table 2（第一阶段；MAE / Model Size 两行逐字；单位 ×10⁻² / kB）

| Hidden Dim | Teacher | MSE: 128 | MSE: 64 | MSE: 32 | MSE: 16 | MSE: 8 | MSE: 4 | MSE: 2 | Cos: 128 | Cos: 64 | Cos: 32 | Cos: 16 | Cos: 8 | Cos: 4 | Cos: 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MAE | 0.78 | 1.02 | 1.01 | 1.02 | 1.03 | 0.90 | 0.84 | 1.96 | 1.18 | 0.78 | 0.90 | **0.75** | 0.88 | 1.10 | 1.93 |
| RMSE | 0.85 | 1.08 | 1.07 | 1.08 | 1.10 | 0.97 | 0.90 | 2.09 | 1.22 | 0.84 | 0.94 | 0.81 | 0.95 | 1.14 | 2.03 |
| MAPE | 0.91 | 1.18 | 1.17 | 1.18 | 1.19 | 1.05 | 0.97 | 2.25 | 1.37 | 0.91 | 1.04 | 0.87 | 1.02 | 1.26 | 2.21 |
| Uncertainty | 2.50 | 2.69 | 2.78 | 3.03 | 3.22 | 3.20 | 2.87 | 3.53 | 3.35 | 3.07 | 3.28 | 3.76 | 3.78 | 3.27 | 7.73 |
| Confidence | 58.3 | 50.3 | 56.9 | 58.0 | 56.5 | 61.4 | 58.6 | 26.6 | 48.9 | 61.6 | 60.8 | 64.1 | 63.6 | 47.9 | 46.5 |
| Inference | 1.91 | 0.76 | 0.98 | 1.09 | 1.03 | 0.94 | 0.93 | 0.82 | 1.02 | 0.90 | 1.04 | 0.97 | 1.06 | 0.94 | 0.93 |
| Model Size | 616 | 685 | 460 | 371 | 333 | 315 | 306 | 302 | 685 | 460 | 371 | 333 | 315 | 306 | 302 |
| Energy | 3.90 | 2.69 | 3.06 | 3.21 | 3.20 | 3.12 | 2.97 | 2.86 | 3.10 | 2.83 | 3.17 | 3.04 | 3.20 | 2.93 | 2.95 |
| CO2 | 1.83 | 1.27 | 1.44 | 1.51 | 1.51 | 1.39 | 1.40 | 1.35 | 1.46 | 1.15 | 1.49 | 1.43 | 1.51 | 1.38 | 1.39 |

不确定度：**无 CI**；`Uncertainty` 列本身是**100 次重复推理的逐次标准差均值**（×10⁻³），`Confidence` = 1 − 95% 预测区间的经验覆盖率。

### 8.4 Table 3（第二阶段；MAE / Model Size 逐字；单位 ×10⁻² / kB）

| Model | 教师 | M-4: 0.1 | M-4: 0.2 | M-4: 0.3 | M-4: 0.4 | M-4: 0.5 | M-4: 0.8 | M-4: 0.9 | C-16: 0.1 | C-16: 0.2 | C-16: 0.3 | C-16: 0.4 | C-16: 0.5 | C-16: 0.9 | C-64: 0.1 | C-64: 0.2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MAE | 0.78 | **0.76** | 0.91 | 0.99 | 1.08 | 1.02 | 0.86 | 1.30 | 1.31 | 1.48 | **0.81** | 1.23 | 1.78 | 2.20 | 1.01 | 1.03 |
| RMSE | 0.85 | 0.83 | 0.96 | 1.09 | 1.14 | 1.10 | 0.97 | 1.40 | 1.34 | 1.52 | 0.87 | 1.27 | 1.84 | 2.37 | 1.05 | 1.08 |
| MAPE | 0.91 | 0.87 | 1.05 | 1.15 | 1.25 | 1.18 | 0.99 | 1.50 | 1.50 | 1.71 | 0.94 | 1.42 | 2.07 | 2.55 | 1.16 | 1.19 |
| Uncertainty | 2.50 | 2.98 | 3.13 | 4.07 | 3.42 | 3.28 | 4.89 | 5.81 | 3.67 | 4.29 | 3.59 | 3.14 | 4.74 | 3.24 | 2.57 | 3.58 |
| Model Size | 616 | 273 | 245 | 220 | 198 | 180 | 138 | 128 | 281 | 251 | 223 | 199 | 182 | 143 | 404 | 366 |

不确定度：**无 CI**。另：`some exhibit poor stability, e.g., reporting compilation errors or collapse, especially for the pruned students based on C-64` → C-64 只报 0.1/0.2 两档。

### 8.5 训练与实验设置（§3.1）

| 项 | 值 |
|---|---|
| 数据集 | **MIT-Stanford battery cycle dataset**（引 Severson et al., *Nature Energy* 4(5):383–391, 2019） |
| 划分 | 训练:测试 = **80:20** |
| 输入窗 / 预测窗 | `τ = τ′ = 100` 循环 |
| 训练轮数 | 200 epochs |
| 蒸馏损失权重 `λ` | 起点 **0.1**，每 epoch **+0.004**，至 **0.9** |
| 误差目标 `f_err` | 5 项；MAE/RMSE/MAPE 共 50%（均分），不确定性与置信度共 50%（均分） |
| 代价目标 `f_cst` | 4 项；模型大小 **50%**、推理时间 **20%**、能量与 CO₂ 共 **30%**（均分） |
| Pareto 剔除阈值 | `f_err^max = 0.25`，`f_cst^max = 0.25` |
| 不确定性定义 | 100 次重复推理的逐次标准差均值 |
| 能量/CO₂ 工具 | `EmissionsTracker from CodeCarbon` |
| 训练硬件 | `NVIDIA RTX 4050 GPU`；数据集侧验证在 **Docker** 内进行 |
| 隐藏维度网格 | `{2^1, …, 2^7} = {2,…,128}`（原文写 `powers of 2`） |
| 剪枝稀疏度网格 | `{0.1, …, 0.9}`（9 档），magnitude-based |
| 随机种子 | **未报告** |

---

## ⚠内部不一致（本卡核验发现，逐条给出可复算证据）

1. **Table 4 的 Gap 行与同行两列不自洽**：用表内印出的教师/学生两列复算 —— RMSE `(0.85−0.73)/0.85 = 14.1%`，表给 `↓13.9`；MAPE `(0.91−0.76)/0.91 = 16.5%`，表给 `↓15.8`。其余各项复算一致（MAE 15.4%、MAE10 15.7%、MAE100 19.5%、Size 84.7%、FLOPs 76.4%、Paras 54.7%）。
2. **Gap 行的 Inference 与 Memory 是跨平台比较**：教师 1.9 ms / 640.43 MB 取自**工作站**，学生 21.1 ms / 0.02 MB 取自 **MCU**，但 Gap 行按"DLNet 相对教师的相对变化（%）"呈现（`↑1002`、`↓100.0`）。表注只说 `The gap row reports relative change (%) of DLNet with respect to the teacher`，**未声明平台不同**。→ 同口径可比数字只在 §3.5 正文（同工作站 0.14 ms vs 1.9 ms）。
3. **尺寸比例的两种写法**：§3.3 写 dim-16 Cosine 学生 `with around only half of the teacher's model size`，§3.4 写 `333 kB, which is 52.0% of the teacher model size` —— 但 Table 2 给 333 kB、Table 4 给教师 616.1 kB，**333/616.1 = 54.1%**，与 `52.0%` 不符（且 54.1% 严格大于"一半"）。**52.0% 对不上表内任何一对数字。**
4. **"更小者胜"与 Table 2 首列的反差未解释**：hidden dim = 128 的 Euler 学生模型大小为 **685 kB**，**比教师 616 kB 更大**；论文未解释同维度学生为何反而更大，也未说明该行是否用于 Pareto 选择。
5. **符号与句子残缺**：§2.2 式 (4) 的说明句 `where W is the teacher trained dynamics matrix that students imitate, α and β are inherited parameters, and ū.` —— 末项 `ū` 后**句子残缺**（缺谓语）；同段 `the parameter count is reduced from from O(d2) to O(d + dr)` 重复 `from`。
6. **Table 2 表注维度集合的印刷/提取形态**：原文表注作 `{21, . . . , 27}`（上标在文本层丢失），正文表述为 `powers of 2, e.g., 64 and 128` 与 `from 2 to 128` → 应读作 `{2^1,…,2^7}`；**引用该表时必须自行还原上标并注明**。
