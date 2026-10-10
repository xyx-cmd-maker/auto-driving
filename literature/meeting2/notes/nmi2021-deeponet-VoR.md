# DeepONet **NMI 2021 正式版** 版本核验卡 ｜Learning nonlinear operators via DeepONet based on the universal approximation theorem of operators

> **本卡是什么**：`nmi2021-deeponet.md`（依据 **arXiv:1910.03193v3** 预印本）的**正式版配套卡**。
> 该卡 §7 第 1 条列为最高优先动作的是"取回 NMI 2021 正式版并逐条复核版本差异，差异表须写入本卡"——**本卡就是执行该动作的产物**。
> ⚠ **但仍未取得正式版正文**：Nature Machine Intelligence 为订阅刊，正文付费。本卡的正式版信息**只覆盖公开可得的落地页内容**（官方摘要、图注、章节标题、参考文献表、元数据、数据/代码可用性声明），**不覆盖正文数值与表格**。
> **引用纪律**：正式版**元数据、标题、作者、图号**可以用本卡；**数值仍只能用 `nmi2021-deeponet.md` 的 arXiv v3 值并标注版本**。

---

- **出处**：*Nature Machine Intelligence* **3(3):218–229**, March 2021（在线 2021-03-18）｜ **类型**：期刊论文（Article）
- **作者（正式版，5 人）**：Lu Lu｜Jin Pengzhan｜**Pang Guofei**｜**Zhang Zhongqiang**｜Karniadakis George Em
  - ⚠ 本地预印本 PDF 只印 **3 人**（Lu Lu, Pengzhan Jin, George Em Karniadakis）→ 引用必须以 5 人版为准
- **DOI**：10.1038/s42256-021-00302-5
- **核验通道与日期**：
  - Crossref `works/10.1038/s42256-021-00302-5`（2026-10-04）：题名、作者 5 人、卷 3 / 期 3 / 页 218–229 / 年 2021 全部命中；`is-referenced-by-count` = **3388**
  - Crossref `license` 字段：**仅 Springer Nature Text and Data Mining**，无 CC 许可 → **正式版不是开放获取**
  - Europe PMC `search?query=DOI:"10.1038/s42256-021-00302-5"`：**hitCount = 0** → 未收录（无 PMC 版本）
  - OpenAlex `works/doi:10.1038/s42256-021-00302-5`：`oa_status = green`，`oa_url = https://arxiv.org/pdf/1910.03193` → **绿色 OA 指向的就是本地那份 arXiv v3 预印本**，不是 VoR
  - arXiv API `id_list=1910.03193`：**只有 v3（2020-04-15）**，`arxiv:doi = 10.1038/s42256-021-00302-5`（即作者自己把预印本指向正式版）；**arXiv 上没有 v4/v5，也没有与正式版一致的版本**
  - Nature 落地页 `https://www.nature.com/articles/s42256-021-00302-5`（2026-10-04 取用）：**公开返回了官方摘要、6 条图注、12 个章节标题、55 条参考文献、数据/代码可用性声明**；正文 PDF 端点 `…-00302-5.pdf` 返回的是 HTML（**未取得正文**）
  - 全文落地页副本：`literature/fulltext/deeponet-nmi2021-VoR-landingpage.txt`（16,130 字符）
- **分组**：连续时间 / 流体神经网络
- **证据等级初判**：**C 级** — 全部证据为**纯数值仿真**（参考解由 Runge-Kutta (4,5) / 二阶有限差分生成，无实验数据、无真实系统），无参数量、无硬件、无不确定度完整报告。**正式版元数据与摘要已核验【确定】；正式版正文数值仍未核验 `[待核实]`。**
- **档位建议**：**C 仅引用** — D1=1（低维 ODE/PDE 基准，与车辆控制、编队、混行交通无一相同），不满足 A 档"D1=2"硬条件；在 B 档预算（≤5）已被更高分条目占满的情况下按预算降 C。
  > ★ **但相对预印本卡有一项实质升级**：正式版有**明确的代码可用性声明**（见下），故 **D3 由 1 升为 2**（代码/协议可直接复用），加权分由 11 升为 **13**。若你愿意放宽 B 档预算，它是 B 档候补的第一顺位。
- **五维打分（按 `00-triage-protocol.md` §5，各维 0–2，满分 20）**：D1=**1** D2=**1** D3=**2** D4=**2** D5=**1** → 加权 = 3·1+2·1+2·2+1·2+2·1 = 3+2+4+2+2 = **13**

---

## 1. 标题

**正式版**：Learning nonlinear operators via DeepONet based on the universal approximation theorem of operators
**预印本（本地 PDF）**：DeepONet: Learning nonlinear operators for identifying differential equations based on the universal approximation theorem of operators
中文直译：基于算子通用逼近定理、用 DeepONet 学习非线性算子

> ⚠ **两版标题不同**（正式版是 "Learning … via DeepONet"，预印本是 "DeepONet: Learning … for identifying differential equations"）。引用必须锁定版本。

---

## 2. 摘要（正式版官方摘要，逐字原文 + 中文）

**官方摘要（逐字）**：
> It is widely known that neural networks (NNs) are universal approximators of continuous functions. However, a less known but powerful result is that a NN with a single hidden layer can accurately approximate any nonlinear continuous operator. This universal approximation theorem of operators is suggestive of the structure and potential of deep neural networks (DNNs) in learning continuous operators or complex systems from streams of scattered data. Here, we thus extend this theorem to DNNs. We design a new network with small generalization error, the deep operator network (DeepONet), which consists of a DNN for encoding the discrete input function space (branch net) and another DNN for encoding the domain of the output functions (trunk net). We demonstrate that DeepONet can learn various explicit operators, such as integrals and fractional Laplacians, as well as implicit operators that represent deterministic and stochastic differential equations. We study different formulations of the input function space and its effect on the generalization error for **16 different diverse applications**.

**中文**：神经网络是连续函数的通用逼近器；一个更少被注意但更强的结果是，**单隐层网络可精确逼近任意非线性连续算子**。该算子通用逼近定理暗示了深度网络从**散乱数据流**中学习连续算子或复杂系统的结构与潜力。本文把该定理**推广到深度网络**，并设计出泛化误差小的新网络 **DeepONet**：一个 DNN 编码离散输入函数空间（**branch net**），另一个 DNN 编码输出函数的定义域（**trunk net**）。作者证明 DeepONet 既能学**显式算子**（积分、分数阶 Laplacian），也能学**隐式算子**（确定性与随机微分方程），并研究了输入函数空间的不同表述及其对泛化误差的影响，**覆盖 16 个不同的应用**。

> ★ **与预印本摘要的实质差异**：预印本（本地 PDF）的自述是"对**动态系统与偏微分方程两类算子**做系统仿真"、正文四个问题；**正式版摘要明确写"16 different diverse applications"**。→ 预印本卡的"四个问题"这一计数**不能代表正式版的覆盖面**；P1 若引用"本文验证了多少个问题"，必须按正式版写 **16 个应用**，或明确标注"arXiv v3 版为 4 个问题"。

---

## 3. 结论（正式版正文不可得，只能给可核验的部分）

**能核验的（正式版）**：
- 落地页章节结构（12 项）：Abstract｜Access options｜**Data availability**｜**Code availability**｜References（**55 条**）｜Acknowledgements｜Author information｜Ethics declarations｜Additional information｜Supplementary information｜Rights and permissions｜About this article。
- **数据可用性**与**代码可用性**均为独立声明节（存在性【确定】；内容因正文付费未取）。
- 参考文献 **[55]** 逐字为：*Lu, L. **DeepONet** `https://doi.org/10.5281/zenodo.4319385` (13 December 2020).* → **正式版给出了独立的代码归档（Zenodo DOI）**，这是预印本卡未记录的。
- 期刊自述（Nature 落地页 `og:description`）："Neural networks are known as universal approximators of continuous functions, but they can also approximate any mathematical operator (mapping a function to another function), which is an important capability for complex systems such as **robotics control**." → ⚠ 这是**期刊的推介语**，不是作者的实验结论；P1 若引用"该工作面向机器人控制"须标注为期刊推介措辞，**不得写成作者验证了控制任务**。

**不能核验的（正式版正文）**：结论节的具体措辞、16 个应用的逐项结果、任何数值与表格。
→ 这些仍以 `nmi2021-deeponet.md`（arXiv v3）为准，并**必须标注版本**。**本卡不重复该卡的数字。**

**作者自承的局限（来自 arXiv v3 结论节，正式版未核）**：① 尚无算子逼近的网络规模理论结果；② 理论上仍不理解 DeepONet 为何泛化误差小；③ 两个子网均为全连接，卷积/注意力未做；④ Theorem 2 的 Te^{cT} 界相对计算结果是**松的**；⑤ 对拟合出的收敛形式目前无法完全解释。

---

## 4. 方法一句话

输入函数 u 在 m 个固定传感器上的采样 + 输出位置 y → **branch net 与 trunk net 双网内积**（显式归纳偏置）→ G(u)(y) 标量输出，逐点拼出输出函数。

---

## 5. 图表清单（占位符）

**正式版共 6 个 Figure**（落地页 `figcaption` 逐字，全部收录）；**Table 数量在落地页不可见**（Nature 落地页不列 table 标题）→ 表格编号与内容**仍以 arXiv v3 的 3 张表为准并标版本**。

| 占位符 | 图/表号 | 原文图注（正式版逐字） | 读图要点 |
|---|---|---|---|
| {FIG-DONV-1} | Fig. 1 | Illustrations of the problem set-up and new architectures of DeepONets that lead to good generalization. | 问题设定 + DeepONet 架构总览（对应预印本 Figure 1 的 A–D；**正式版是否保留 stacked/unstacked 两分支需核**） |
| {FIG-DONV-2} | Fig. 2 | Learning explicit operators using different V spaces and different network architectures. | **显式算子**（积分、分数阶 Laplacian 一类）在不同输入函数空间 V 与不同网络架构下的学习结果。→ 正式版把"显式算子"独立成图，预印本无对应编号 |
| {FIG-DONV-3} | Fig. 3 | Fast learning of implicit operators in a nonlinear pendulum (k = 1 and T = 3). | **隐式算子**：非线性摆，k=1、**T=3**（⚠ 预印本主实验是 T=1，正式版此图为 T=3，**不是同一组设置**） |
| {FIG-DONV-4} | Fig. 4 | Fast learning of implicit operators in a diffusion-reaction system. | **扩散-反应系统**（对应预印本 §4.3；预印本给的是 10 图 3 表体系，编号不可直接对应） |
| {FIG-DONV-5} | Fig. 5 | DeepONet prediction for a stochastic ODE. | ★**随机 ODE**——预印本摘要未提"随机"算子，正式版摘要明确写 "deterministic and stochastic differential equations"；**这是正式版新增/前置的内容** |
| {FIG-DONV-6} | Fig. 6 | DeepONet prediction for a stochastic elliptic equation. | ★**随机椭圆方程**（PDE + 随机），同样属正式版摘要新增表述 |

> **版本差异（关键）**：预印本是 **10 图 3 表**（编号 Figure 1–10 / Table 1–3，含 FNN 网格搜索、传感器数扫描、收敛率拟合等机制图）；**正式版只有 6 图**。→ **两版的图号不可互换**。P1 稿件中若要指"某一张图"，必须写明版本。

---

## 6. 对 P1 的用处

- **与 P1 的关系**：**不同问题（远邻方法学）**，与预印本卡结论一致，D1 仍为 1。
- **可迁移（相对预印本卡新增/强化的一条）**：
  - ★ **代码归档可核验**：正式版参考文献 [55] 给出 **Zenodo DOI `10.5281/zenodo.4319385`**（2020-12-13），另有正文中的 **DeepXDE**（`github.com/lululxvi/deepxde`）。→ 若 P1 要用算子学习给 OTF 势场做代理模型，**这是两个可直接取用的起点**（D3 因此由 1 升为 2）。**本卡未克隆、未运行这两个仓库。**
  - 其余四条可迁移项（"双网分解 = 显式归纳偏置"作为 structure-/prior-informed 的已发表支撑；传感器数 vs 函数空间复杂度的扫描范式；误差三分解的报告纪律；"输入函数多样性 > 单函数采样密度"）**沿用 `nmi2021-deeponet.md` §6**，本卡不重复。
- **不可迁移 / 陷阱**：
  1. **正式版正文未取得** → 正式版的数值、表格、16 个应用的逐项结果**全部不可引用**；引用数值只能引 arXiv v3 并标版本。
  2. 预印本卡列的其余六条陷阱（无控制/无车辆/无混行、参考解由数值求解器生成、无参数量与硬件、不确定度报告不完整、数据集大小≠输入函数个数、"首次观察到指数收敛"是作者主张）**继续有效**。
  3. **★ 新增陷阱：不要把正式版摘要的 "16 different diverse applications" 当成"16 个工程系统"** —— 摘要未说明这 16 个应用是否仍全部是数值基准。在取得正式版正文前，**不得**写"已在 16 类真实系统上验证"。
  4. **★ 新增陷阱：期刊推介语 ≠ 作者结论**。Nature 落地页把该工作与 "robotics control" 关联，这是**期刊编辑/宣传措辞**；P1 不得据此写"DeepONet 已用于机器人控制"。
- **与 CfC（NMI 2022）的关系**：不变（互不引用、层面不同：operator learning vs continuous-depth sequence model）。
- **引用时必须带的限定语**（在预印本卡的限定语基础上**改三处**）：
  - 作者写作 **Lu L, Jin P, Pang G, Zhang Z, Karniadakis GE（5 人）**，不是 3 人；
  - 题名用 **"Learning nonlinear operators via DeepONet based on the universal approximation theorem of operators"**；
  - 版本句改为："**正式版元数据与官方摘要已核验（Crossref / Nature 落地页，2026-10-04）；正式版正文付费未取得，本文所引全部数值与图表编号来自 arXiv:1910.03193v3（2020-04-15，3 作者），与正式版（6 图、16 个应用）不可互换。**"

---

## 7. 缺失信息（可执行动作）

1. **★ 仍需取得正式版正文**（唯一未闭合项）。→ 路径：① 用你所在机构的 Nature 订阅（你的 T-ITS PDF 水印显示 **Shenzhen Polytechnic University**，该校若订了 Springer Nature 即可直接下载）；② 通过 Springer Nature 的 **TDM 端点**（Crossref `link` 字段给出 `https://www.nature.com/articles/s42256-021-00302-5.pdf`，`content-version: vor`，`intended-application: text-mining`）；③ 向作者索取。**取得后需补**：正式版 Table 编号与内容、16 个应用的清单与逐项结果、结论节原文、以及"6 图 vs 10 图"的映射表。
2. **需核 Data availability / Code availability 两节的逐字内容**（落地页只显示章节标题存在，正文付费未见内容）。（后果：现在只能引参考文献 [55] 的 Zenodo DOI，无法确认作者声明的可复现边界。）
3. **需核正式版是否保留了预印本的不确定度口径**（±1 SD 只在个别图给出、Fig. 6/7/8/10 明确不画 SD）。（后果：若正式版已补，预印本卡的"无不确定度"结论需撤回。）
4. 预印本卡 §7 的其余 5 条动作（参数量/FLOPs、Theorem 2 松界量化、GRF/Chebyshev 与工程输入分布的差距、DeepXDE 复现、T2 取代检查）**继续有效**，本卡不重复。

---

## 8. 关键数字

**本卡不产生新的数值**（正式版正文未取得）。正式版可核验的**计数类**事实如下：

| 指标 | 值 | 不确定度 | 出处 |
|---|---|---|---|
| 正式版作者数 | **5** | — | Crossref `author` 数组（2026-10-04）+ Nature 落地页 `citation_author` ×5 |
| 正式版图数 | **6** | — | Nature 落地页 `figcaption` 计数 |
| 正式版参考文献数 | **55** | — | Nature 落地页 `citation_reference` meta 计数 |
| 正式版自述应用数 | **16 个不同应用** | — | 官方摘要逐字 "for 16 different diverse applications" |
| 正式版被引数 | **3388** | — | Crossref `is-referenced-by-count`（2026-10-04 快照；与 OpenAlex `cited_by_count`=3405 **口径不同、跨库不可比**） |
| 代码归档 | Zenodo DOI **10.5281/zenodo.4319385**（2020-12-13） | — | 正式版参考文献 [55] 逐字 |
| 正式版卷期页 | **3(3):218–229**，在线 2021-03-18 | — | Crossref + 落地页 `citation_firstpage/lastpage/citation_online_date` |
| 开放获取状态 | **非 OA**（license 仅 Springer Nature TDM；Europe PMC 0 命中；OpenAlex green OA 指向 arXiv v3） | — | Crossref `license`、Europe PMC、OpenAlex（三通道一致） |

---

## 附：与预印本卡的差异表（执行 `nmi2021-deeponet.md` §7 第 1 条动作的产出）

| 项 | 预印本 arXiv:1910.03193v3（2020-04-15） | **正式版 NMI 3(3):218–229（2021）** | 对 P1 的影响 |
|---|---|---|---|
| 题名 | "DeepONet: Learning nonlinear operators **for identifying differential equations** based on…" | "**Learning nonlinear operators via DeepONet** based on…" | 引用题名必须用正式版 |
| 作者 | **3 人**（Lu, Jin, Karniadakis） | **5 人**（+ **Pang G**, **Zhang Z**） | 作者列表必须用 5 人版 |
| 图数 | **10 图 3 表**（含 FNN 网格搜索、传感器数扫描、收敛率拟合等机制图） | **6 图**（表格数落地页不可见） | **图号不可互换**；P1 指图必须写版本 |
| 自述覆盖面 | 正文四个 ODE/PDE 问题 | 摘要写 **16 个不同应用** | 不得用"四个问题"代表正式版覆盖面 |
| 算子类型 | 摘要：动态系统 + PDE | 摘要明确含 **随机** ODE 与 **随机椭圆方程** | 正式版把"随机算子"前置为主打内容 |
| 代码 | 正文给 DeepXDE 仓库 | 另有独立 **Code availability** 节 + Zenodo 归档 DOI | D3 由 1 升 2；取用起点更明确 |
| 数据可用性 | 未单独声明 | 有独立 **Data availability** 节 | 引用可复现性时须以正式版声明为准 |
| 参考文献数 | 48 条（arXiv 版，项目既有记录） | **55 条** | 版本差异的直接量化证据 |

【确定】：上表所有正式版列均来自 Crossref / Nature 落地页 / Europe PMC / OpenAlex 四通道核验（2026-10-04），落地页原文存于 `literature/fulltext/deeponet-nmi2021-VoR-landingpage.txt`。
【待核实】：正式版**正文数值、表格编号与内容、结论节逐字** —— 全部未取得，标 `[待核实]`。

---

citation_qualifier: Lu L, Jin P, Pang G, Zhang Z, Karniadakis GE (5 authors), Nature Machine Intelligence 2021;3(3):218-229, DOI 10.1038/s42256-021-00302-5 — Verifier's note (2026-10-04): the version of record is NOT open access (Crossref license = Springer Nature text-and-data-mining only; Europe PMC hitCount=0; Unpaywall oa_status=green resolves only to the arXiv submitted version), and no accepted manuscript exists in any repository, so ALL numerical values and figure/table numbers attributable to this work come from arXiv:1910.03193v3 (15 Apr 2020, 3 authors, title "DeepONet: Learning nonlinear operators for identifying differential equations ...", 10 figures / 3 tables) and NOT from the version of record, which differs in title ("Learning nonlinear operators via DeepONet based on ..."), in author count (5 vs 3), in figure count (6 main figures), and in claimed coverage (16 different diverse applications vs four ODE/PDE benchmark problems in the preprint); the version-of-record values verifiable here are limited to metadata (volume/issue/pages/DOI/authors), the official abstract, 6 figure captions, 55 references, and the existence of Data/Code availability sections, with code archived at Zenodo DOI 10.5281/zenodo.4319385; all evidence in the preprint is numerical simulation (reference solutions from Runge-Kutta (4,5) and second-order finite differences, no experimental data, no real system), with no controller, no closed loop, no hardware, no parameter count or FLOPs, and +/-1 SD shown only in a few figures while convergence-rate fits (x^-0.5 to x^-3.7, e^-x/k) carry no uncertainty; the "16 different diverse applications" claim must NOT be restated as "16 engineering systems validated" until the version of record is obtained.

