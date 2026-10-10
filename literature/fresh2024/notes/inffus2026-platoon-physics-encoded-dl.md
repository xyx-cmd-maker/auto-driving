# 知识–数据融合的编队动力学物理编码深度学习｜Knowledge-data fusion dominated vehicle platoon dynamics modeling and analysis: A physics-encoded deep learning approach

- **出处**：Information Fusion, 126: 103622, 2026（Crossref `published-print` = 2026-02；`created` = 2025-08-25 → 2025 年在线首发）｜ **类型**：期刊论文（本地材料 16 页）
- **作者**：Hao Lyu, Yanyong Guo, Pan Liu, et al.（n=6；完整署名：Hao Lyu, Yanyong Guo, Pan Liu, Shuo Feng, Weilin Ren, Quansheng Yue。Yanyong Guo 为通信作者 `∗`）
- **DOI**：10.1016/j.inffus.2025.103622（Crossref `works/10.1016/j.inffus.2025.103622` 返回 http 200，`article-number` = 103622，`alternative-id` = S1566253525006943；取用日期 2026-10-05，通道 Crossref REST）
- **全文来源**：`literature/fulltext/fresh2024/inffus2026-platoon-knowledge-data__424b59df.txt`（**PAGES=16, CHARS=60,952**，口径：Node `readFileSync(path,'utf8').length`；去掉 3 行页眉与 16 个 `===== PAGE n =====` 标记后 60,556）｜
  **材料版本**：**预印本（arXiv v2 作者版，投往 Elsevier 的稿件），非 Information Fusion VoR**。逐字证据：① 每页页脚 `Hao Lyu et al.: Preprint submitted to Elsevier`；② 第 63 行 `arXiv:2502.08658v2 [cs.RO] 13 Mar 2025`；③ 每页页脚 `Page N of 16`；④ **参考文献仅 39 条**（本卡脚本按条目首行统计），而 Crossref 记录正式版 `reference-count` = **75** → 两版内容差异是**实质性**的，不能假定本地预印本等于 VoR。
  ⚠ **与任务给定不符**：任务写 CHARS=59,124，本卡实测 60,952（Node 口径），差 1,828 字符；去页标记后亦为 60,556。**以实测为准并留痕**。
- **分组**：2024+ 增量
- **证据等级初判**：**C 级（偏 B 的下沿）** — 用**真实公开轨迹数据集**（HIGH-SIM，739 个编队）做 7:1:2 划分、5 个对照/消融模型、效应量齐全，明显强于纯仿真；但**无随机种子、无置信区间、无显著性检验**，弦稳定性与安全分布复现只取 **3 个"随机"挑选的编队**，且无实车/台架。
- **档位建议**：**B** — D1=1 是硬门槛：本文建模的是**编队动力学（模型）而非控制器**，不直接测 P1 的 RQ，故按母协议 §5 进不了 A 档。
  ⚠ **同时报一个协议缺口（请组会处理）**：本文 D3=2、D4=2（有开源代码 + 公开数据集 + 超参数表 + 16 页全文）。若把 D5 记为 2（这三项确实都在），加权 = **15** 而 D1=1，**既不是 A**（判据要求 D1=2）**也不是 B**（B 的区间是 9–13）——母协议 §5 的档位判定式存在"**D1=1 且加权 ≥14**"的空档。本卡按"D1 为门槛、加权为序"的意图归 **B**，并建议母协议补一条兜底规则（如"加权 ≥14 但 D1=1 → 归 B 档顶格并标注"）。本卡主口径取保守的 D5=1。
- **五维打分（各维 0–2，满分 20）**：D1=**1** D2=**1** D3=**2** D4=**2** D5=**1** → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = **13**
  ⚠ 必须 0–2 制；D4 一律指**时效性**（2026 卷 / 2025 在线 → ≤5 年 → 2）。
  - **D1=1 的依据**：本文给的是**编队级跟驰动力学模型**（含可解释参数、局部稳定性条件、弦稳定性复现、安全代理指标复现），属母协议 D1=1 明确列举的"**行为预测 / 可解释性评价**"相邻环节；它**不提供控制器、不做控制实验、不产生控制性能数字**，故不构成 D1=2 的"直接给出 P1 所需控制器/决策方法"。
  - **D2=1**：有对照（PeLSTM / PeTransformer）与两组消融（w/o TFL、w/o PFL）+ IDM 基线，且用真实数据；但**无种子、无 CI、无显著性检验**，"有统计"缺项 → 取 1（若按"2 分档为析取式"的读法则为 2，加权升至 15，落入上述空档）。
  - **D3=2**：**开源代码**（正文脚注 `https://github.com/SpaceTrafficSafetyTeam/PeMTFLN`，**本卡未联网核验其可访问性与许可证**）+ **公开数据集**（HIGH-SIM，Shi et al. 2021）+ 完整超参数表（Table 1）→ 数据/代码/协议三项均可直接复用。
  - **D4=2**：2026 卷（2025 在线）。
  - **D5=1**：有全文 + 效应量（Table 2 逐时间步精度、KL/Hellinger 距离）+ 可复现材料线索；但**本地为预印本而非 VoR**、且两版差异实质（39 vs 75 refs），按 `00-scope.md` §2.2 保守取 1（若取得 VoR 且内容一致，D5 可升至 2 → 加权 15，见上）。

---

## 1. 标题

**原文题名（逐字，首页第 7–8 行）**：
`Knowledge-data fusion dominated vehicle platoon dynamics modeling and analysis: A physics-encoded deep learning approach`

标题关键词与正文用词对照（逐字）：题名用 `physics-encoded`；Abstract 用 `a novel physics-encoded deep learning network, named PeMTFLN`；§1 又把它称为 `a physics-encoded deep learning framework for vehicle platoon dynamics modeling and analysis, named PeDL`。
⚠ **内部不一致（本卡第 1 处）**：**Abstract 通篇未出现 "PeDL"**，只出现 "PeMTFLN"；而 §1 把框架命名为 PeDL、把网络命名为 PeMTFLN，§3.3 又把 PeMTFLN 展开为 `parameters encoder multi-scale trajectory feature learning network`。此外 APeCG 的展开式两处不同：Abstract 作 `analyzable parameters encoded computational graph`，§1 作 `analyzable parameters encoder computational graph`。**引用时统一用 "PeDL 框架 / PeMTFLN 网络"，并注明系作者自己的双重命名。**

**Keywords（逐字，第 17–21 行）**：`Platoon Dynamics Modeling` / `Physics-encoded Deep Learning` / `Feature Learning Network` / `Knowledge-data fusion`

---

## 2. 摘要（≤400 字）

论文提出物理编码深度学习框架 PeDL 及其网络 PeMTFLN，做**编队级**非线性跟驰动力学建模：用可解释参数编码计算图（APeCG）承载广义跟驰模型的线性时变形式，用 MTFLN（Mamba＋变分编码器＋因果注意力＋非自回归解码器）从真实轨迹反推该参数。物理是**硬结构嵌入**：式(4) 的三条符号条件由 θ=[−1,1,1]·Softplus(·) 直接实现，再由式(10) 的递推图生成编队未来状态；损失（式 13）只有预测损失与 KL 项，无物理残差项。数据为公开高速公路轨迹数据集 HIGH-SIM 抽取的 739 个七车编队（15 s @0.1 s，>212,751 样本），按 7:1:2 划分。实验：多步预测平均速度 RMSE 0.469 m/s、间距 RMSE 0.643 m；滚动生成中复现了头尾弦稳定性（\|G(jω)\|>1 判为弦不稳定）与 PET/SSDD 安全分布（KL 0.001 / 0.013）。

---

## 3. 结论（≤350 字）

作者自述（§6）：2 s 时域内最大平均间距误差 1.117 m、速度误差 0.526 m/s；两代理安全指标分布复现良好，KL 散度 0.013 与 0.001；并复现真实编队的头尾稳定性，生成优于在线标定 IDM。

**本卡判定**：① 精度优势小且无统计：速度 RMSE 在 0.5/1.0 s 上 PeMTFLN（0.492/0.536）**不如其消融版 w/o PFL（0.486/0.528）**，故"consistently outperforms"不可引用；② 弦稳定性只是**复现被建模车流的**\|G(jω)\|，非控制器判据，**不得写成"弦稳定性保证"**；③ KL/Hellinger 是分布相似度非检验，**不得当显著性证据**；④ 无种子、CI、多重校正与实车，按 `AGENTS.md` §1 红线不得表述为实车验证。

---

## 4. 方法一句话（≤60 字）

用 Softplus 加固定符号把跟驰模型的三条物理符号条件硬编码进计算图，再由注意力网络从真实轨迹反推该时变参数。

---

## 5. 图表清单（占位符）

> 全文共 **13 个**图表条目（Figure 1–11、Table 1–2）。已超 12 条阈值，**本卡仍完整覆盖全部 13 条并在此写明总数**。

| 占位符 | 图/表号 | 原文图注（逐字，可截断 100 字符） | 读图要点 |
|---|---|---|---|
| `FIG-1` | Figure 1 | `The architecture of PeMTFLN under PeDL Framework` | 全局架构：VFL（TFL+FUL）→ PFL（拓扑因果注意力）→ NARP 解码器 → APeCG。**图的右下角 Loss 框里标了 `Physics Encoding`，而式(13) 的损失只有两项**（见 §6 陷阱④） |
| `FIG-2` | Figure 2 | `The structure of the mamba block in TFL module` | TFL 的 Mamba 块与选择性 SSM；正文称 8 个 SSM 子系统、共享时间步 τ_t、各维 τ_t 不同 |
| `FIG-3` | Figure 3 | `The structure of the topology-based causal attention in PFL module` | 编队级交互的因果掩码注意力（单向拓扑掩码，假设驾驶员只看前方）；**这是"编队级而非单车级"建模的关键结构** |
| `FIG-4` | Figure 4 | `Platoon modeling errors among PeMTFLN, PeLSTM and PeTransformer. (a) Gap; (b) Velocity` | 多元箱线图，横轴为编队内车辆序号，每箱 20 个值（步 1–20）→ **误差随车辆序号累积**；只给箱线、无数值表 |
| `FIG-5` | Figure 5 | `Visualization of platoon trajectory samples replicated by PeMTFLN and real trajectory samples.` | 100 批 × 32 × 6 = 19,200 个样本的真值–预测散点；正文给 2 s 步的 RMSE 1.137 m / 0.574 m/s 与 bias 0.143 m / 0.051 m/s |
| `FIG-6` | Figure 6 | `The safety statistics of platoon evolution replicated by PeMTFLN. (a)PET; (b) SSDD` | 两个代理安全指标（PET、SSDD）的分布复现；正文给 KL 0.001/0.013 与 Hellinger 0.118/0.386。**这是全文唯一的"分布级"评价** |
| `FIG-7` | Figure 7 | `The reproduced platoon trajectory examples of PeMTFLN. (a) continuous acceleration; (b)…` | 三种驾驶模式的真实 vs 预测轨迹（深/浅同色系）；定性证据，**无数值** |
| `FIG-8` | Figure 8 | `The platoon stability evolution replicated by PeMTFLN. (a) continuous accel- eration;…` | ★ **弦稳定性图**：头车→尾车传递函数幅值 \|G(jω)\|，蓝色区（>1）判为扰动放大＝弦不稳定；正文称振荡场景 (b) 呈弦不稳定。**P1 可直接借用的口径** |
| `FIG-9` | Figure 9 | `The reproduced position evolution of IDM and PeMTFLN. (a) continuous acceleration;…` | 位置演化：实线为真值、虚线为生成；IDM 在头车速度变化剧烈时偏差大 |
| `FIG-10` | Figure 10 | `The reproduced speed evolution of IDM and PeMTFLN. (a) Continuous acceleration;…` | 速度生成误差热力图（蓝→红）；**无数值色标范围**，不可估读 |
| `FIG-11` | Figure 11 | `The PET distributions of reproduced trajectory with IDM and PeMTFLN. (a) Continuous…` | 三组（IDM / PeMTFLN / 真值）PET 分布对比；红框＝PeMTFLN 与真值吻合，黑框＝IDM 偏差 |
| `TAB-1` | Table 1 | `Hyperparameters of PeMTFLN` | **完整超参数表，可直接复用**：Mamba 块 1、SSM 子系统 8、变分编码器 3 层（ReLU）、注意力 2 层 4 头、模型维度 64、lr 1e-5、m=5、α_KL=0.0025、batch 32、max epoch 20、输入长 21、输出长 20 |
| `TAB-2` | Table 2 | `Comparison of platoon dynamic modeling accuracy indicators` | 唯一的核心效应量表：5 个模型 × 4 个时间步 × 4 个指标。**已完整转录于 §8**；注意 `Avg` 列**不是**四个时间步的平均（见 §8.3 口径说明） |

---

## 6. 对 P1 的用处

### 与 P1 的关系：**相邻问题（提供术语、评价口径与基线候选；不含控制器）**

本文建模的是**编队动力学**（不是控制器），P1 要的是**控制器**。它不回答 P1 的 RQ，但在四个点上直接服务 P1：① 给 P1 的"物理注入"术语提供**结构嵌入**这一现成先例；② 给 P1 缺失的**弦稳定性口径**一个可搬的度量；③ 给 P1 的"长尾/分布一致性"评价提供 PET/SSDD + 分布距离的做法；④ 给 P1 一个**公开数据集 + 开源代码**的基线候选（在线标定 IDM）。

### 可迁移

1. **★ 弦稳定性评价口径（P1 目前七项指标里没有，这是最强的一条）**：逐字 `the transfer function magnitude value |G(jw)| is calculated, which describe the evolution of disturbance transmission from the head vehicle to the tail vehicle (Montanino and Punzo, 2021)`；判据逐字 `|G(jw)| greater than 1 (the blue area) indicates that the disturbance has been amplified, reflecting the characteristics of string instability`。**P1 的 P33 图谱（Lp 弦稳定，TCST 2014）给的是理论判据，本文给的是"如何从轨迹数据估计并画出来"的操作化路径**——P1 若要在 CARLA 回放中报编队弦稳定性，可直接照此实现。
2. **"结构嵌入"而非"软损失"的写法模板**：`θt = [−1, 1, 1] · Softplus(H_Dec)`（式 10）把三条物理符号条件**硬编进计算图**：既不需要选 λ，也不存在"物理项权重怎么调"的问题。这是 P1 把 OTF 势场作为**边界条件 / 结构条件**注入 CfC 时最贴近的写法先例。
3. **线性时变广义跟驰模型 + 局部稳定性充分条件**：式(3)(4) 把任何跟驰模型在期望状态处一阶展开，用三个偏导数（对 v、s、Δv）表征驾驶员意图，并把 `f'v* < 0, f's* > 0, f'Δv* > 0` 作为**局部稳定性充分条件**。P1 若要给"OTF 势场改变的是哪一个可解释通道"一个可辩护的参数面，这是现成的参数化写法。
4. **分布级评价（比平均 RMSE 强）**：PET（post-encroachment time）与 SSDD（safe stopping distance difference）两个代理安全指标 + **KL 散度与 Hellinger 距离**作为"生成分布 vs 真实分布"的量化。P1 的长尾场景（前车急刹、cut-in、编队单车退出）若只报平均 RMSE 会掩盖分布尾部差异，**建议照此增设分布距离指标**。
5. **公开资产**：HIGH-SIM 数据集（Shi et al. 2021, Communications in Transportation Research 1:100014）+ 开源代码 `https://github.com/SpaceTrafficSafetyTeam/PeMTFLN`（**本卡未联网核验**）+ 完整超参数表 → P1 的"人工车流"若需要一个**有真实数据支撑**的替代方案（取代手设 OVM/IDM 参数），这是候选。
6. **在线 GA 标定的 IDM 基线**：`an online genetic algorithm (GA)-based personalized calibration procedure is designed to determine the IDM parameters for each vehicle` —— 这是比"固定参数 IDM"更公平的人驾车基线，P1 若用 IDM 做背景车流，应照此**逐车在线标定**，否则会低估人驾的异质性。

### 不可迁移 · 陷阱

1. **本文没有任何控制器**：无控制律、无闭环控制实验、无控制性能数字。**不得**把本文当作 P1 的基线或对照数字来源；P1 的四条基线（PID / MPC / TD3 / OTF-CfC）在本文全无对应。
2. **单车道、无横向、无换道、无混行**：本文是**纯人驾车编队**（`human-driven vehicle trajectory datasets`），没有 CAV、没有混合交通、没有车道居中偏差与前轮转角方差。P1 的混行 + 多车道 + 横向指标在本文零对应。
3. **固定编队规模**：数据抽取为**七车**（1 头车 + 6 跟随车），Remark 3 自认 `we conducted experiments using platoons with a uniform number of vehicles`，可扩展性只是声称（`the PeDL is flexible and scalable`），**无不同 N 的实验** → 不得引用为"可扩展到任意编队规模"的证据。
4. **"Simulation" 一词的歧义（本卡第 2 处 ⚠）**：§5 标题为 `Simulation`，但它**不是交通仿真器**（无 SUMO/VISSIM/CARLA），而是**用数据集里的真实样本做模型自反馈滚动生成**（`providing only the initial states of the leading vehicle, while following vehicles within the platoon are simulated by their initial states (2 seconds here) and the simulated results of the vehicle ahead`）。引用时写"仿真验证"会低估其数据真实性，写"实测"则越级；准确写法是"**在真实高速轨迹数据集上的多步预测与滚动生成实验**"。
5. **弦稳定性是"复现"不是"保证"**：\|G(jω)\| 描述的是**被建模的人类车流本身**的扰动传递，模型复现了观测到的弦不稳定。**没有任何控制器稳定性判据、没有证明**。P1 引用时必须写"该文复现了实测车流的弦不稳定性"，**不得**写"该文给出了弦稳定性保证/判据"。
6. **无 λ=0 消融（对 P1 的 A1 至关重要，见下）**。
7. **作者自认的模型限制**：`APeCG is grounded in linear vehicle dynamics and requires iterative trajectory generation` → 线性车辆动力学 + 逐点迭代生成，与 P1 的连续时间非线性控制器（CfC 的 ODE 前向）不是同一族；且未报推理时延。
8. **⚠ 数值口径不一致（本卡第 3 处）**：§4.2.1 正文写 `the RMSE for gap and speed are 1.137m and 0.574m/s`（100 批散点比较），而 Table 2 的 2.0 s 列为 gap 1.117 m、velocity 0.526 m/s，§6 结论又用 1.117/0.526。**两组数字来自不同评价集，不可互换**；引用时必须写明是哪一组。

### 引用时必须带的限定语

```
citation_qualifier: single-lane, purely HUMAN-DRIVEN seven-vehicle platoon (1 leading + 6 following vehicles, uniform platoon size only - the paper itself states experiments used platoons with a uniform number of vehicles, so the claimed scalability to other platoon lengths is NOT demonstrated), no CAV, no mixed traffic, no lateral dynamics and no lane change, dynamics-model paper with NO controller, NO control law and NO closed-loop control experiment of any kind; physics is HARD STRUCTURALLY ENCODED (theta = [-1,1,1]*Softplus(.) enforcing the three sign conditions f'_v*<0, f'_s*>0, f'_dv*>0 of Eq.(4), with the state recursion of Eq.(10) hard-wired) and NOT a soft physics-residual loss - the training loss Eq.(13) contains only the prediction loss and a KL term, so there is NO lambda=0 ablation and none is even definable in this paradigm; data are the public HIGH-SIM highway trajectory dataset (Shi et al. 2021) re-extracted into 739 platoons of 15 s at 0.1 s (>212,751 examples, 7:1:2 train/val/test split), so the underlying trajectories are real-world but all experiments are offline; the "Simulation" section is NOT a traffic simulator but autoregressive rollout of the model on dataset samples, with only 3 randomly picked platoons (8, 10, 14) used for the qualitative, stability and safety-distribution results; NO vehicle test, NO hardware-in-the-loop and NO traffic-simulator validation; NO random seeds, NO repeats, NO confidence intervals and NO significance tests - the KL divergences (0.001 for PET, 0.013 for SSDD) and Hellinger distances (0.118, 0.386) are DISTRIBUTION-SIMILARITY measures and NOT hypothesis tests; the string-stability result is a REPRODUCTION of the observed head-to-tail transfer-function magnitude |G(jw)| of the modelled human traffic (|G(jw)|>1 marking amplification in the oscillation case) and is NOT a stability guarantee or criterion for any controller; PeMTFLN is not best at every step (velocity RMSE at 0.5 s and 1.0 s is worse than its own w/o-PFL ablation), so "consistently outperforms" must not be quoted; the body text's 1.137 m / 0.574 m/s (Fig. 5, 100-batch sample) and Table 2's 1.117 m / 0.526 m/s (2.0 s step) are two different evaluation sets and must not be interchanged; and the version analysed here is the arXiv v2 author preprint (39 references) whereas the published Information Fusion version has 75 references, so published-version details may differ.
```

### ★ 关于 P1 的 A1 消融：这个问题必须回答清楚

**问：有没有 λ=0 消融？答：没有；而且在"结构嵌入"范式下 λ=0 这一档在原理上不存在。**

- 全文的消融只有两条，**都是特征学习模块的消融**，不是物理的消融：逐字 `PeMTFLN w/o TFL: Remove TFL module from MTFLN and keep PFL module.` / `PeMTFLN w/o PFL: Remove PFL module from MTFLN and keep TFL module.`
- 两个基线（PeLSTM、PeTransformer）逐字 `A neural network comprising an LSTM encoder-decoder and a variational encoder` / `... a Transformer and a variational encoder, with an architecture analogous to that of PeLSTM` → **它们仍然带变分编码器、仍然要用 APeCG 生成状态**，只是把 MTFLN 换成 LSTM/Transformer。**没有"去掉物理编码"的对照组。**
- 损失函数逐字 `L = L_Pred + αKL · L_KL`（式 13）→ **没有任何物理残差项**，因此**不存在可调权重 λ，也就不存在 λ=0 这一档**；要"关掉物理"只能把 θ 的网络输出直接接到式(10) 的递推上（这会改变模型的物理可解释性主张本身）。
- **对 P1 的直接后果（两条，都很重要）**：
  1. **本文与 PINC（Neurocomputing 2024）一样从未做物理开关消融** → P1 的 A1（OTF 势场开/关）相对**两篇都是净增量**（与 `AGENTS.md` §1 已有结论一致，本文是第二条独立证据）。
  2. **★ 但 P1 不能因此照抄"结构嵌入 + 声称有 A1"**：若 P1 把 OTF 走结构嵌入路线（例如把 OTF 势场做成 CfC 的边界条件/门控），那么"OTF 开/关"就不再是扫一个连续 λ，而是**两个不同模型族的对照**；P1 必须在实验设计里**事先声明**这一点，且 A1 的两档要**共享其余全部结构、训练轮次与种子**，否则 A1 会退化成"改结构"的消融而非"改条件"的消融——**这正是本文没有做、也做不了的那一步**。

---

## 7. 缺失信息（≥3 条）

1. **未报告随机种子、重复次数、置信区间、显著性检验、多重比较校正**。
   - 影响：Table 2 是 5 模型 × 4 时间步 × 4 指标 = 80 个格子，最好的与次好的差距常在 1%–2%（如速度 Avg RMSE 0.469 vs 0.474）；**无检验则"最优"不可判**。P1 若照此报单次结果，与本项目 `AGENTS.md` §4（种子 ≥5、mean±std 或 95% CI）直接冲突。
   - 最小补法：给出种子列表与 5 次以上重复，报 mean±std；对"最优"做配对检验并校正 80 次比较。
2. **未报告模型规模、参数量、推理时延与硬件实测**（Table 1 只有超参数；无 FLOPs、无参数量、无单步推理时间，训练平台 i9-13900K + RTX 4090 只是训练环境）。
   - 影响：P1 的"端到端延迟"与"MCU 内存占用"两项在本文**无对应物**；无法判断该架构是否可能上端侧。
   - 最小补法：报参数量、单步推理时延与目标硬件。
3. **未报告线性时变参数 θ_t 的可辨识性分析**。
   - 影响：θ_t ∈ R^{N×F×3} 由网络从轨迹反推，其"可解释"依赖参数唯一可辨识；论文只由 `Softplus + 固定符号` 保证**符号**合法，**未讨论**同一轨迹是否可由不同 θ 解释（f'v*、f's*、f'Δv* 之间的耦合与共线性）。
   - 最小补法：给出参数敏感性/置信区间或合成数据上的可辨识性实验。
4. **未报告弦稳定性分析的可复算细节**：\|G(jω)\| 的**估计方法、ω 范围、采样与窗长**均未给出（只给结果图 Fig. 8）。
   - 影响：Fig. 8 **不可复算**；P1 想照搬该口径时缺关键步骤。
   - 最小补法：给出传递函数估计的公式、频段与参数。
5. **未报告 3 个抽样编队的选取机制**（`three platoon simulation cases are randomly selected` 无种子、无筛选准则），且 Fig. 7/8/9/10/11 的定性结论全部建立在这 3 个编队上。
   - 影响：不可复现；且 3 个样本无法支撑"跨多种驾驶模式"的普遍性主张。
   - 最小补法：给出抽样脚本与种子，或报全部 739 编队的分布。
6. **未报告 HIGH-SIM 抽取的筛选细节**：论文只说 `Our extraction method follows Mo et al. (Mo et al., 2021) and adds the recognition of continuous following vehicles`，未给车道/路段/车型分布/时间窗/是否排除换道。
   - 影响：739 个编队的代表性不可判定（是否集中于某一拥堵状态）。
   - 最小补法：给数据卡（路段、时段、速度区间、编队长度分布）。
7. **本地材料与正式版内容不一致且差异未量化**：预印本 39 条参考文献 vs 正式版 75 条（Crossref `reference-count`）。
   - 影响：**正式版可能新增了实验、消融或统计**；本卡的"无 λ=0 消融""无显著性检验"等判断**只对预印本成立**。
   - 最小补法：取得 Information Fusion VoR（PII S1566253525006943）并逐节 diff。
8. **未联网核验开源代码与数据集**：`https://github.com/SpaceTrafficSafetyTeam/PeMTFLN` 的可访问性、许可证、commit 均未核验；HIGH-SIM 的获取条件亦未核验。

---

## 8. 关键数字（只抄印出的表格/正文，不得估读）

> `[计算值]` 为本卡按论文印出数字复算。本卡未使用任何图内估读数值（Fig. 4/5/9/10/11 的数值一律不取）。

### 8.1 Table 1 完整转录（第 658–700 行）

`Table 1 — Hyperparameters of PeMTFLN`

| 模块 | 超参数 | 值 | 超参数 | 值 |
|---|---|---|---|---|
| VFL Module | Number of Mamba Block | 1 | Number of SSM Sub-System | 8 |
| | Number of Variational Encoder Layer | 3 | Activate Function of Variational Encoder | ReLU |
| PFL Module & NARP Decoder | Number of Attention Layer | 2 | Number of Attention Head | 4 |
| Other Parameter | Dimension of Model | 64 | Learning Rate | 10⁻⁵ |
| | m | 5 | α_KL | 0.0025 |
| | Batch Size | 32 | Max Epoch | 20 |
| | Inputs Length | 21 | Outputs Length | 20 |

### 8.2 Table 2 完整转录（第 747–771 行）

`Table 2 — Comparison of platoon dynamic modeling accuracy indicators`

| Model | Velocity RMSE (m/s) 0.5s / 1.0s / 1.5s / 2.0s / **Avg** | Gap RMSE (m) 0.5s / 1.0s / 1.5s / 2.0s / **Avg** | Velocity MAPE (%) 0.5s / 1.0s / 1.5s / 2.0s / **Avg** | Gap MAPE (%) 0.5s / 1.0s / 1.5s / 2.0s / **Avg** |
|---|---|---|---|---|
| PeLSTM | 0.494 / 0.534 / 0.549 / 0.602 / **0.492** | 0.396 / 0.674 / 0.943 / 1.204 / **0.689** | 3.42 / 3.70 / 3.89 / 4.43 / **3.48** | 1.15 / 2.03 / 2.94 / 3.88 / **2.12** |
| PeTransformer | 0.483 / 0.550 / 0.507 / 0.551 / **0.479** | 0.389 / 0.652 / 0.907 / 1.158 / **0.666** | 3.20 / 3.67 / 3.41 / 3.86 / **3.25** | 1.12 / 1.92 / 2.73 / 3.59 / **1.99** |
| PeMTFLN w/o TFL | 0.490 / 0.537 / 0.512 / 0.555 / **0.476** | 0.388 / 0.651 / 0.909 / 1.162 / **0.667** | 3.28 / 3.60 / 3.54 / 4.01 / **3.28** | 1.12 / 1.93 / 2.78 / 3.69 / **2.02** |
| PeMTFLN w/o PFL | 0.486 / 0.528 / 0.507 / 0.543 / **0.474** | 0.386 / 0.651 / 0.905 / 1.154 / **0.664** | 3.15 / 3.48 / 3.39 / 3.79 / **3.17** | 1.11 / 1.90 / 2.72 / 3.56 / **1.98** |
| **PeMTFLN** | 0.492 / 0.536 / **0.484** / 0.526 / **0.469** | 0.379 / **0.627** / 0.872 / 1.117 / **0.643** | **3.11** / 3.43 / 3.22 / 3.68 / **3.09** | **1.08** / 1.82 / **2.17** / 3.47 / **1.91** |

### 8.3 口径说明与自洽性检查（本卡复算）

- **`Avg` 列不是四个时间步的平均**：速度 RMSE（0.492+0.536+0.484+0.526)/4 = **0.5095** ≠ 0.469【计算值】；间距 RMSE（0.379+0.627+0.872+1.117)/4 = **0.7488** ≠ 0.643【计算值】。→ `Avg` 应为**全 1–20 步**的平均，论文未写明。**引用 Avg 时必须写明它是"全步平均"而非"列出的四步平均"。**
- **消融反超（论文自己承认）**：逐字 `PeMTFLN achieved state-of-the-art performance in all scenarios except for speed prediction with a step size of 0.5s and 1.0s`。核对：0.5 s 速度 RMSE PeTransformer **0.483** < PeMTFLN 0.492；w/o PFL **0.486** < 0.492；1.0 s w/o PFL **0.528** < 0.536 ✓ **与表内一致**。
- **Avg 列全部由 PeMTFLN 取得最优**：速度 RMSE 0.469 < 0.474 < 0.476 < 0.479 < 0.492 ✓；间距 RMSE 0.643 < 0.664 < 0.666 < 0.667 < 0.689 ✓；速度 MAPE 3.09 < 3.17 < 3.25 < 3.28 < 3.48 ✓；间距 MAPE 1.91 < 1.98 < 1.99 < 2.02 < 2.12 ✓【计算值，与论文一致】
- **⚠ 与 Table 2 并存的两组数字**：§4.2.1 正文 `the RMSE for gap and speed are 1.137m and 0.574m/s, respectively, with corresponding bias of 0.143m and 0.051m/s`（100 批散点）vs Table 2 的 2.0 s 列 1.117 m / 0.526 m/s。**两组不可互换。**

### 8.4 其他印出数字

| 指标 | 值 | 出处 | 备注 |
|---|---|---|---|
| 编队数 | **739** platoons | §4.1.1 | 每编队 7 车（1 头车 + 6 跟随车） |
| 样本总数 | > **212,751** examples | §4.1.1 | |
| 每编队时长 / 采样 | **15 s** @ **0.1 s** | §4.1.1 | |
| 划分比例 | **7:1:2**（训练:验证:测试） | §4.1.2 | |
| 输入 / 输出长度 | **21** / **20** | Table 1 | 对应 P=21、F=20 → 20 步 × 0.1 s = **2 s 时域**【计算值】 |
| 参数共享步数 m | **5** | Table 1；Remark 2 | 每 5 步（0.5 s）换一组参数；正文亦称 "we adopt a new set of prediction parameters every 5 steps (0.5s)" |
| 最优速度平均 RMSE | **0.469 m/s**；平均 MAPE **3.09%** | §4.2.1；Table 2 | PeMTFLN |
| 最优间距平均 RMSE | **0.643 m**；平均 MAPE **1.91%** | §4.2.1；Table 2 | PeMTFLN |
| 2 s 时域最大平均间距误差 | **1.117 m** | §6 结论；Table 2 2.0s 列 | 与 Table 2 一致 ✓ |
| 2 s 时域最大平均速度误差 | **0.526 m/s** | §6 结论；Table 2 2.0s 列 | 与 Table 2 一致 ✓ |
| Fig. 5 散点集（100 批） | gap RMSE **1.137 m** / speed RMSE **0.574 m/s**；bias **0.143 m** / **0.051 m/s** | §4.2.1 | 样本量正文：`100 batches of samples (a total of 100X32X6=19200)`；⚠ 与 Table 2 不同口径 |
| PET 分布复现 | **KL 0.001**；**Hellinger 0.118** | §4.2.2 | 分布相似度，**非**假设检验 |
| SSDD 分布复现 | **KL 0.013**；**Hellinger 0.386** | §4.2.2；§6 结论 | 同上 |
| 弦稳定性判据 | \|G(jω)\| **> 1** ⇒ 扰动被放大 ⇒ 弦不稳定 | §4.3.2；Fig. 8 | 方法引自 Montanino & Punzo (2021) |
| 弦稳定性观察结果 | 振荡场景（Fig. 8b）**呈弦不稳定**；减速场景收敛到较一致速度 | §4.3.2 | 仅 3 个编队；无数值 |
| 滚动生成的抽样编队 | 3 个：**Platoon 8 / 10 / 14**（连续加速 / 减速 / 振荡） | §5.1 | `randomly selected`，无种子 |
| 生成实验的初始状态窗 | 跟随车初始 **2 seconds** | §5.1 | 其余由前车模拟结果递推 |
| 训练平台 | PyTorch；Intel **i9-13900K** CPU + **NVIDIA RTX 4090** GPU | §4.1.2 | **非**嵌入式、**非**实车 |
| 参考文献数（本地预印本） | **39** 条 | 本卡脚本统计参考表条目首行 | |
| 参考文献数（正式版） | **75** | Crossref `reference-count` | ⚠ 与本地预印本差 36 条 → 两版实质不同 |
| Crossref 被引数 | **7** | `api.crossref.org/works/10.1016/j.inffus.2025.103622` 字段 `is-referenced-by-count` | **端点已写明**（T6）；取用日期 2026-10-05 |
| 撤稿/更正检查 | Crossref `relation` 字段为**空对象** `{}`（字段 `update-policy` 存在，`crossmark-restriction: true`） | 同上端点 | 未见撤稿/更正登记（T5，按 DOI 注册机构分流：非 `10.48550/` → 查 Crossref）✓ 但 **Crossmark 详情未展开核验**，属本卡未完成项 |

---

## 9. 字数核验（纪律要求：实测）

| 项 | 上限 | 实测（非空白字符） |
|---|---|---|
| §2 摘要 | 400 字 | 见文末核验命令输出 |
| §3 结论 | 350 字 | 见文末核验命令输出 |
| §4 方法一句话 | 60 字 | 见文末核验命令输出 |

**核验方法**（可复现，与卡片 1 共用脚本）：`node "D:/Deepseek Harness/out/checkcard.mjs"`

---

## 10. 本卡限制

1. **材料限制（最重要）**：仅有 arXiv 2502.08658v2 的作者预印本纯文本（16 页，**39 条参考文献**），**未获 Information Fusion VoR**（正式版 **75 条参考文献**，PII S1566253525006943）。→ §6/§7 中"无 λ=0 消融""无显著性检验""无参数量/时延"等判断**只对预印本成立**，正式版可能已补充；入稿前必须取 VoR 复核。
2. **图内数值不可用**：Fig. 4/5/6/7/8/9/10/11 的数值一律未取（本卡不含任何估读值）；Fig. 8 的 \|G(jω)\| 曲线与 Fig. 10 的误差热力图**无法从文本复算**。
3. **口径限制**：D1–D5 为母协议 §5 判据，权重（3/2/2/1/2）是本机自定惯例；本卡已标出 D2/D5 的口径敏感性（13 → 15 并落入档位空档）。
4. **未联网核验的项**：开源代码仓库、HIGH-SIM 数据集可得性与许可、Crossref Crossmark 详情。
5. **未做外部复现检索**：Crossref 被引 7 次**不等于**有独立复现；是否有后续工作批评其可辨识性或弦稳定性口径，本卡未查。
