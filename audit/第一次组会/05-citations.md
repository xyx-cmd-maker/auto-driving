# 引用核验清单（Citation Verification）

> 文件编号：`05-`。原为 `01-pending-citations.md`，因 `01-` 按 `prompts/00-kickoff.md` §6 保留给 P1 计划而改名；编号表见 `AGENTS.md` §6。项目内其它文件对本文件的引用已统一为**完整路径** `audit/第一次组会/05-citations.md`（遵循 `AGENTS.md` §0 路径纪律：分支新增产物必须写完整相对路径）。

> 指令来源：`auto-driving/prompts/00-kickoff.md` §1 末段 + `auto-driving/AGENTS.md` §8"引用核验（硬要求）"。
> 核验对象：`sources/references-list.txt` 全 30 条（核心锚点 2 + 五组 28）。
> 核验方式：arXiv 摘要页（journal-ref / comments）＋ DOI 注册元数据（Crossref）＋ 官方 proceedings 页（ECVA / CVF / PMLR / OpenReview / AAAI OJS / NeurIPS proceedings）＋ Nature Portfolio 官方站。
> **会话限制（必须记录）**：dblp.org 全站、dl.acm.org、ieeexplore 正文、iso.org、nature.com 直读被反爬或 403 拦截 → 上述来源改用官方 proceedings、OpenReview 官方 API 与 Crossref DOI 元数据替代；受影响字段逐条标 `[待核实]`，未标即表示有官方页面或 DOI 元数据支撑。
> 状态：**核验完成**（30/30 有结论，0 条无法确认）。

---

## 0. 汇总结论

`30 条中：已正式发表 26 条 / 仅预印本或非正式渠道 7 条（含 2 条 workshop、1 条软件仓库）/ 有更新版本 6 条 / 无法确认 0 条`

- "已正式发表 26"：A1 B1 B2 B3 B4 C1 C3 C4 C5 C6 D1 D3 D5 D6 D7 D8 D9 E1 E2 F1 F2 F3 F4 F5 F7 F8 F11
- "仅预印本/非正式渠道 7"：A2、D2（均为 **workshop** 论文，不计主会正式发表）、B5（软件仓库）、C2、D4、F9、F10
- "有更新版本 6"：B1(v5)、B3（期刊题名不同 + Publisher Correction）、B4（**清单链接指向另一篇论文**）、F11（arXiv v2 晚于正刊）、A1（v2 之后才被 ECCV 接收）、C1（v2 之后才被 AAAI 接收）
- "有更新版本"与"已正式发表"**不互斥**（同一条可同时命中）。

### 0.1 本会话独立抽查（不采信子代理自述的 2 条）

| 条目 | 子代理结论 | 我的独立核验 | 是否一致 |
|---|---|---|---|
| A1 DriveDreamer | ECCV 2024 Poster | ECVA 官方虚拟会场页：标题 "DriveDreamer: Towards Real-world-driven World Models for Autonomous Driving"，作者 Wang ⋅ Zhu ⋅ Huang ⋅ Xinze ⋅ Zhu ⋅ Lu，标注 **2024 Poster**；含 Paper PDF `papers_ECCV/papers/06416.pdf` | ✅ 一致 |
| A2 Drive as You Speak | WACV 2024 Workshops (LLVM-AD), pp. 902–909 | CVF Open Access：**"Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV) Workshops, 2024, pp. 902-909"**；bibtex booktitle 为 WACV Workshops；作者 5 人 Cui, Ma, Cao, Ye, Wang | ✅ 一致 |

> 其余 28 条**未逐条独立抽查**——它们将在我实际写入稿件时按 `AGENTS.md` §8 二次核对。**抽查不等于复核**：本表的用途是"写入前的第一道闸"，不是"已核验可直引"。

---

## 1. 逐条核验表

| 编号 | 题名（简） | 清单标注 | 核验结论 | 建议引用版本 |
|---|---|---|---|---|
| **A1** | DriveDreamer | 📄 arXiv 预印本 | **已正式发表**：ECCV 2024（Poster）；arXiv v2 的 comments 仅写 Project Page、无 journal-ref | Wang X, Zhu Z, Huang G, Chen X, Zhu J, Lu J. DriveDreamer: Towards Real-world-driven World Models for Autonomous Driving. In: *Computer Vision – ECCV 2024*. Springer, 2024. DOI 10.1007/978-3-031-73195-2_4 |
| **A2** | Drive as You Speak | 📄 arXiv 预印本 (cs.HC) | **workshop 论文，非主会**：WACV 2024 Workshops (LLVM-AD), pp. 902–909 | Cui C, Ma Y, Cao X, Ye W, Wang Z. Drive As You Speak: Enabling Human-Like Interaction With Large Language Models in Autonomous Vehicles. *Proc. IEEE/CVF WACV Workshops*, 2024: 902–909 |
| B1 | Neural ODE | ✅ NeurIPS 2018（最佳论文奖） | 已正式发表；**最佳论文奖属实**（NeurIPS 官方 Awards 页）；arXiv 最大 v5、无 journal-ref | Chen RTQ, Rubanova Y, Bettencourt J, Duvenaud D. Neural Ordinary Differential Equations. *Advances in NeurIPS 31*, 2018: 6571–6583 |
| B2 | Liquid Time-Constant Networks | ✅ AAAI 2021 | 已正式发表（标注正确）；arXiv comments 逐字 "Accepted to the Thirty-Fifth AAAI Conference（AAAI-21）"，v4 | Hasani R, Lechner M, Amini A, Rus D, Grosu R. Liquid Time-constant Networks. *Proc. AAAI* 2021;35(9):7657–7666. DOI 10.1609/aaai.v35i9.16936 |
| **B3** | CfC | ✅ Nature Machine Intelligence 2022 | 已正式发表：**NMI 4(11): 992–1003**；⚠ 期刊题名用 "neural **networks**"，与 arXiv 版 "neural **Models**" 不同；另有 Publisher Correction (NMI 4:1267) | Hasani R, Lechner M, Amini A, et al. Closed-form continuous-time neural networks. *Nature Machine Intelligence* 2022;4(11):992–1003. DOI 10.1038/s42256-022-00556-7 |
| **B4** | Neural Circuit Policies | ✅ NMI 2020 | 已正式发表：**NMI 2(10): 642–652**；⚠⚠ **清单的 arXiv 链接指向完全不同的论文**（`arXiv:2003.08554` 实为 *Adjust Planning Strategies to Accommodate Reinforcement Learning Agents*，Xuerun Chen 单作者）；NCP 本身未发现 arXiv 预印本 | Lechner M, Hasani R, Amini A, Henzinger TA, Rus D, Grosu R. Neural circuit policies enabling auditable autonomy. *Nature Machine Intelligence* 2020;2(10):642–652. DOI 10.1038/s42256-020-00237-3 |
| B5 | torchdiffeq | GitHub 开源工具 | **软件仓库，非论文**；作者 Ricky T. Q. Chen 拼写成立、MIT 许可；无 Zenodo DOI、未发现 JMLR/MLOSS 软件论文（**不得臆造软件论文**） | Chen RTQ. torchdiffeq [Computer software]. 2018. https://github.com/rtqichen/torchdiffeq （学术机理引用请引 B1） |
| **C1** | DriveDreamer-2 | 📄 arXiv 预印本 | **已正式发表**：AAAI-25 **39(10): 10412–10420**；⚠⚠ 清单 **arXiv 编号错**（2403.0684**6** 实为 *DiaLoc*，CVPR 2024；正确为 **2403.06845**）、**题名错**（应为 "…for **Diverse** Driving Video Generation"） | Zhao G, Wang X, Zhu Z, et al. DriveDreamer-2: LLM-Enhanced World Models for Diverse Driving Video Generation. *Proc. AAAI* 2025;39(10):10412–10420. DOI 10.1609/aaai.v39i10.33130 |
| C2 | GAIA-1 | 📄 arXiv 预印本 | 仍为预印本（Wayve 技术报告，comments="Technical Report"，仅 v1） | Hu A, Russell L, Yeo H, et al. GAIA-1: A Generative World Model for Autonomous Driving. arXiv:2309.17080v1, 2023 |
| **C3** | World Models for AD: An Initial Survey | 📄 arXiv 预印本 | **已正式发表**：IEEE T-IV，DOI 10.1109/TIV.2024.3404834（arXiv v3 无 journal-ref） | Guan Y, Liao H, Li Z, et al. World Models for Autonomous Driving: An Initial Survey. *IEEE Transactions on Intelligent Vehicles*, 2024. DOI 10.1109/TIV.2024.3404834 |
| C4 | Wayformer | ✅ ICRA 2023 | 已正式发表：ICRA 2023, pp. 2980–2987；arXiv 仅 v1、无 comments；**未发现期刊扩展版** | Nayakanti N, Al-Rfou R, Zhou A, Goel K, Refaat KS, Sapp B. Wayformer: Motion Forecasting via Simple & Efficient Attention Networks. *2023 IEEE ICRA*, 2023: 2980–2987. DOI 10.1109/ICRA48891.2023.10160609 |
| **C5** | MTR | ✅ NeurIPS 2022 | 已正式发表（NeurIPS 2022 main track, pp. 6531–6543）；**另存在期刊扩展版 MTR++**（TPAMI 46(5): 3955–3971, 2024）；"Oral" 仅见作者自填 arXiv comments【待核实】 | 期刊版（IEEE 格式推荐）：Shi S, et al. MTR++: Multi-Agent Motion Prediction with Symmetric Scene Modeling and Guided Intention Querying. *IEEE TPAMI* 2024;46(5):3955–3971 |
| **C6** | SceneTransformer | ✅ ICLR 2022 | 已正式发表（ICLR 2022 Poster）；⚠ 官方题名含 "predicting **future** trajectories"；⚠ 官方第 2/3 作者顺序为 Vasudevan、Caine（与 arXiv 相反）；⚠ 官方分写 "Scene Transformer" | Ngiam J, Vasudevan V, Caine B, et al. Scene Transformer: A unified architecture for predicting future trajectories of multiple agents. *ICLR 2022* |
| D1 | DiLu | ✅ ICLR 2024 | 已正式发表（标注正确）；arXiv comments 逐字 "Published as a conference paper at ICLR 2024"，v3 | Wen L, Fu D, Li X, et al. DiLu: A Knowledge-Driven Approach to Autonomous Driving with Large Language Models. *ICLR 2024* |
| **D2** | GPT-Driver | ✅ NeurIPS 2023 Workshop | **workshop，非主会**：NeurIPS 2023 Foundation Models for Decision Making Workshop (FMDM@NeurIPS2023)；另曾被 ICLR 2024 拒稿，无主会正式发表 | Mao J, Qian Y, Ye J, Zhao H, Wang Y. GPT-Driver: Learning to Drive with GPT. *NeurIPS 2023 FMDM Workshop*, 2023（**须显式标注 workshop**） |
| **D3** | DriveGPT4 | ✅ IEEE RA-L 2024 | 已正式发表：**RA-L 9(10): 8186–8193, Oct 2024**；arXiv comments "Accepted by RA-L."，v5；ICRA 2025 宣读版【待核实】 | Xu Z, Zhang Y, Xie E, et al. DriveGPT4: Interpretable End-to-end Autonomous Driving Via Large Language Model. *IEEE RA-L* 2024;9(10):8186–8193. DOI 10.1109/LRA.2024.3440097 |
| D4 | LanguageMPC | 📄 arXiv 预印本 | 仍为预印本（标注正确）；**版本有更新 v3（2025-04）**，比 v2 晚约 18 个月；ICLR 2024 拒稿；⚠ 同一作品有两个题名 | Sha H, Mu Y, Jiang Y, et al. LanguageMPC: Large Language Models as Decision Makers for Autonomous Driving. arXiv:2310.03026v3, 2025（**须写 preprint**） |
| **D5** | Agent-Driver | ✅ COLM 2024 | 已正式发表（venue 正确）；⚠ 官方题名**无 "Agent-Driver:" 前缀** | Mao J, Ye J, Qian Y, Pavone M, Wang Y. A Language Agent for Autonomous Driving. *COLM 2024* |
| **D6** | Driving with LLMs | 📄 arXiv 预印本 | **已正式发表**：ICRA 2024, pp. 14093–14100；作者与 arXiv 逐位一致 | Chen L, Sinavski O, Hünermann J, et al. Driving with LLMs: Fusing Object-Level Vector Modality for Explainable Autonomous Driving. *2024 IEEE ICRA*, 2024: 14093–14100. DOI 10.1109/ICRA57147.2024.10611018 |
| D7 | DriveVLM | ✅ CoRL 2024 | 已正式发表：CoRL 2024, **PMLR 270: 4698–4726**；TPAMI 扩展版检索无阳性证据【待核实】 | Tian X, Gu J, Li B, et al. DriveVLM: The Convergence of Autonomous Driving and Large Vision-Language Models. *Proc. 8th CoRL*, PMLR 270: 4698–4726, 2025 |
| D8 | DriveLM | ✅ ECCV 2024 (Oral) | 已正式发表，**Oral 属实**（ECVA 官方标 "2024 Oral"）；LNCS pp. 256–274 | Sima C, Renz K, Chitta K, et al. DriveLM: Driving with Graph Visual Question Answering. *Computer Vision – ECCV 2024*, LNCS: 256–274. DOI 10.1007/978-3-031-72943-0_15 |
| D9 | Talk2BEV | ✅ ICRA 2024 | 已正式发表：ICRA 2024, pp. 16345–16352；作者集合一致但顺序不同 | Choudhary T, Dewangan V, Chandhok S, et al. Talk2BEV: Language-enhanced Bird's-eye View Maps for Autonomous Driving. *2024 IEEE ICRA*, 2024: 16345–16352. DOI 10.1109/ICRA57147.2024.10611485 |
| **E1** | Control Barrier Functions | ✅ ECC 2019（欧洲控制会议） | 已正式发表（**写法需补全**）：2019 18th European Control Conference (ECC), Naples, pp. 3420–3431；arXiv 无 comments/journal-ref，仅 v1 | Ames AD, Coogan S, Egerstedt M, Notomista G, Sreenath K, Tabuada P. Control Barrier Functions: Theory and Applications. *2019 18th European Control Conference (ECC)*, 2019: 3420–3431. DOI 10.23919/ECC.2019.8796030 |
| **E2** | ISO 26262 | 国际功能安全标准 | **标注不完整**：`iso.org/standard/68383` **只是 Part 1**，即 **ISO 26262-1:2018（Vocabulary）**；系列共 12 个 part、最新版本均 2018 年【部分待核实：iso.org 正文 403】 | ISO 26262-1:2018, *Road vehicles — Functional safety — Part 1: Vocabulary*. ISO, 2018.（泛引 Parts 1–12:2018；精确到 part：HARA/ASIL → -3/-9，软件 → -6，半导体 → -11。**只引术语，不得声称合规**） |
| **F1** | UniAD | ✅ CVPR 2023（最佳论文奖） | 已正式发表，**Best Paper 属实**；⚠ CVPR 官方正式题名为 **"Planning-Oriented Autonomous Driving"**（UniAD 是系统名） | Hu Y, Yang J, Chen L, et al. Planning-Oriented Autonomous Driving. *Proc. IEEE/CVF CVPR*, 2023: 17853–17862 |
| F2 | BEVFormer | ✅ ECCV 2022 | 已正式发表（标注正确）；正式出处为 Springer LNCS pp. 1–18（CVF 不收录 ECCV）；**BEVFormer v2 是独立工作（CVPR 2023），不是本篇扩展版** | Li Z, Wang W, Li H, et al. BEVFormer: Learning Bird's-Eye-View Representation from Multi-Camera Images via Spatiotemporal Transformers. *Computer Vision – ECCV 2022*, LNCS: 1–18. DOI 10.1007/978-3-031-20077-9_1 |
| F3 | End-to-end AD: Challenges and Frontiers | ✅ IEEE TPAMI 2024 | 已正式发表（年份正确，**勿写 2023**）：TPAMI **46(12): 10164–10183, 2024** | Chen L, Wu P, Chitta K, Jaeger B, Geiger A, Li H. End-to-end Autonomous Driving: Challenges and Frontiers. *IEEE TPAMI* 2024;46(12):10164–10183. DOI 10.1109/TPAMI.2024.3435937 |
| F4 | TD3 | ✅ ICML 2018 | 已正式发表（标注正确） | Fujimoto S, van Hoof H, Meger D. Addressing Function Approximation Error in Actor-Critic Methods. *Proc. 35th ICML*, PMLR 80: 1587–1596, 2018 |
| F5 | nuScenes | ✅ CVPR 2020 | 已正式发表（标注正确）；⚠ CVF 页码 11621–11631 与 IEEE 页码 11618–11628 **不可混用** | Caesar H, Bankiti V, Lang AH, et al. nuScenes: A Multimodal Dataset for Autonomous Driving. *Proc. IEEE/CVF CVPR*, 2020: 11621–11631 |
| **F6** | Waymo Open Dataset: Perception and Motion | ✅ CVPR 2020 | ⚠⚠ **两篇论文被合并，且第二篇会议标错**：(a) 感知数据集 = **CVPR 2020**；(b) 运动数据集 = **ICCV 2021**（不是 CVPR 2020） | (a) Sun P, et al. Scalability in Perception for Autonomous Driving: Waymo Open Dataset. *CVPR 2020*: 2443–2451 ／ (b) Ettinger S, et al. Large Scale Interactive Motion Forecasting for Autonomous Driving: The Waymo Open Motion Dataset. *ICCV 2021*: 9710–9719 |
| F7 | CARLA | ✅ CoRL 2017 | 已正式发表（标注正确）：PMLR 78: 1–16 | Dosovitskiy A, Ros G, Codevilla F, Lopez A, Koltun V. CARLA: An Open Urban Driving Simulator. *Proc. 1st CoRL*, PMLR 78: 1–16, 2017 |
| F8 | OpenVLA | ✅ CoRL 2024 | 已正式发表：CoRL 2024, **PMLR 270: 2679–2713**（PMLR 出版年 2025） | Kim MJ, Pertsch K, Karamcheti S, et al. OpenVLA: An Open-Source Vision-Language-Action Model. *Proc. 8th CoRL*, PMLR 270: 2679–2713, 2025 |
| F9 | Qwen-VL | 📄 arXiv 技术报告 | 仍为预印本（标注成立）；⚠ 作者须写 **Jinze Bai 等 9 位具名作者**，页面不出现 "Qwen Team"/Alibaba | Bai J, Bai S, Yang S, et al. Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond. arXiv:2308.12966v3, 2023 |
| F10 | Qwen2-VL | 📄 arXiv 技术报告 | 仍为预印本（未见接收）：arXiv v2，无 journal-ref；DBLP 仅 CoRR | Wang P, Bai S, Tan S, et al. Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution. arXiv:2409.12191v2, 2024 |
| **F11** | DeepSeek-R1 | ✅ Nature 2025（封面论文） | 已正式发表；**"封面论文"说法属实**（Nature Portfolio 官方站该期目录 + Cover Story 专页）；⚠ **正刊题名与署名均不同于 arXiv**：正刊题名 "DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning"，且**不列集体作者 DeepSeek-AI**（第一作者 Daya Guo） | Guo D, Yang D, Zhang H, et al. DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning. *Nature* 2025;645(8081):633–638. DOI 10.1038/s41586-025-09422-z |

---

## 2. 必须修正的清单错误（17 条，按严重度排序）

| # | 严重度 | 编号 | 清单写 | 实际为 |
|---|---|---|---|---|
| 1 | **硬错误（链接指向另一篇论文）** | B4 | 链接 `arXiv:2003.08554` | 该号实为 *Adjust Planning Strategies to Accommodate Reinforcement Learning Agents*（Xuerun Chen）；NCP 无 arXiv 版 → 改用 DOI 10.1038/s42256-020-00237-3 |
| 2 | **硬错误（题名不存在）** | F6 | "Waymo Open Dataset: Perception and Motion" | 不是任何论文的正式题名；实为两篇合并，且 (b) 是 **ICCV 2021** 而非 CVPR 2020 |
| 3 | **硬错误（编号错文）** | C1 | `arXiv:2403.06846` | 该号实为 *DiaLoc*（CVPR 2024）；正确为 2403.06845；题名亦错；且已由 AAAI-25 正式发表 |
| 4 | venue 判定错（已发表写成预印本） | A1 | 📄 arXiv 预印本 | ECCV 2024 Poster |
| 5 | venue 判定错 | A2 | 📄 arXiv 预印本 | WACV 2024 **Workshops** (LLVM-AD), pp. 902–909 |
| 6 | venue 判定错 | C3 | 📄 arXiv 预印本 | IEEE T-IV 正式论文 |
| 7 | venue 判定错 | D6 | 📄 arXiv 预印本 | ICRA 2024, pp. 14093–14100 |
| 8 | workshop 未标清 | D2 | ✅ NeurIPS 2023 Workshop | FMDM@NeurIPS2023 Workshop（**须写"非主会"**）；曾被 ICLR 2024 拒稿 |
| 9 | 题名不符官方 | C6 | "…architecture for multiple agents" | "…for predicting **future** trajectories of multiple agents"；且官方第 2/3 作者顺序为 Vasudevan, Caine |
| 10 | 题名不符官方 | D5 | "Agent-Driver: A Language Agent…" | 官方题名无 "Agent-Driver:" 前缀 |
| 11 | 题名不符官方 | F1 | "UniAD: Planning-oriented Autonomous Driving" | CVPR 官方题名 "Planning-Oriented Autonomous Driving" |
| 12 | 题名不符官方 | B3 | "…Neural Models" | 期刊正式题名 "…neural **networks**"；另有 Publisher Correction |
| 13 | 标准标注不完整 | E2 | "ISO 26262" + standard/68383 | 68383 = **ISO 26262-1:2018**（仅 Part 1）；系列 12 个 part |
| 14 | 写法不完整 | E1 | "ECC 2019（欧洲控制会议）" | 2019 18th European Control Conference (ECC), Naples, pp. 3420–3431 |
| 15 | 漏标期刊扩展版 | C5 | NeurIPS 2022 | 会议版成立，但另有 **MTR++ (TPAMI 2024)**；IEEE 格式建议引后者 |
| 16 | 署名/题名与正刊不符 | F11 | arXiv 题名 + 集体作者 DeepSeek-AI | 正刊题名不同，且不列集体作者 |
| 17 | 署名不精确 | F9 | "Qwen-VL（技术报告）" | 须列 Jinze Bai 等具名作者，页面无 "Qwen Team" |

---

## 3. 对项目定位的**结构性影响**（比清单纠错更重要）

### 3.1 锚点 A1：DriveDreamer 已不再是预印本 → "首个经同行评议"这一措辞失效

| 项 | 原状态 | 核验后 | 后果 |
|---|---|---|---|
| `AGENTS.md` §6"引用锚点" | "DriveDreamer（arXiv:2309.09777）——**预印本引用须核对最新版本**" | **ECCV 2024 正式论文** | 引用锚点须改为 ECCV 版；`blueprint-papers-v1.1.txt` L178 的措辞建议"可用'**首个经过同行评议的 OTF 条件世界模型**'占位"——**该措辞现在不成立**：DriveDreamer 本身已经过同行评议 |
| 剩余的真实新颖性 | — | **只剩"条件模态"这一层**：DriveDreamer 的条件是 HDMap / 3D Box，本文提出"交通流社会压力场"（OTF 场）作为**新的条件模态** | P2 的定位句应改写为："首个以交通流社会压力场（OTF 场）为结构条件的世界模型"，**不再依赖"经同行评议"这一对比** |

> ⚠️ 这是本轮核验最有价值的一条：**一个看似有利的修辞（"我们是首个经同行评议的"）建立在过时的事实上**，若写进 Abstract 会被审稿人一句话推翻。

### 3.2 锚点 A2：Drive as You Speak 是 **workshop** 而非主会

| 项 | 核验后 | 后果 |
|---|---|---|
| A2 地位 | WACV 2024 **Workshops**（LLVM-AD），pp. 902–909；5 页级短文 | 对 **P3 有利**：P3 宣称"解决其未解决的语言意图无定量物理对应物"时，对手是 workshop 论文，反驳空间更小 |
| 引用要求 | 必须写成 "Proc. IEEE/CVF WACV **Workshops**, 2024: 902–909"，**不得写成 WACV 主会** | 若误写成主会，属可核查的引用失实 |

### 3.3 其他影响

- **F11 的 DeepSeek-R1**：`AGENTS.md` 未直接引用，但清单解释为"DeepSeek Harness 本地工具链引用"——若写进稿件，**必须引 Nature 正刊题名与作者**，不能引 arXiv 题名。
- **E2 的 ISO 26262**：`AGENTS.md` §4 要求"只能引术语与思路，不得声称合规"——核验后追加一条：**引用时须精确到 part**（如 HARA/ASIL 相关引 -3/-9，软件引 -6），只写 "ISO 26262" 属引用不精确。

---

## 4. 使用规则（写入稿件前必做）

1. 本表是**第一道闸**，不是"可直引清单"：写入稿件时按 `AGENTS.md` §8 逐条复核 arXiv 版本号与最终卷期页码。
2. 表中标 `[待核实]` 的字段（C5 的 Oral、D3 的 ICRA 2025 宣读版、D9 的 CVPRW 版、F2 本篇 TPAMI 扩展版、D7 的 TPAMI 扩展版、E2 的 iso.org 正文、F11 的封面题字原文）**不得在稿件中作肯定表述**。
3. **workshop 论文必须显式标注 workshop**（A2、D2）——不得用 "NeurIPS 2023" / "WACV 2024" 的简写造成主会印象。
4. **他人数字**（DriveDreamer 的 FID/minADE 等）引用时必须标"文献报告值，协议不同，不可直接比较"（`AGENTS.md` §1）。
5. 五篇论文约 70% 共享引用库——**任何一条修正都要同步到共享库**，否则同一错误会在五篇稿件里复现。

---

## 5. 需要你裁决的事项（阻塞后续写入）

| # | 事项 | 我的建议 | 是否已动文件 |
|---|---|---|---|
| V1 | `AGENTS.md` §6 引用锚点：DriveDreamer 由"预印本"改为"ECCV 2024"；Drive as You Speak 改为"WACV 2024 Workshops, pp. 902–909" | 建议改（属可核查事实，不改会持续误引） | **未改，等你批准** |
| V2 | `blueprint-papers-v1.1.txt` L178 的"首个经过同行评议"措辞：改为"首个以交通流社会压力场为条件模态的世界模型" | 建议改（否则 P2 定位句不成立） | **未改**（蓝图是内部资料原文，我只在审计文件中记录，不擅改原文） |
| V3 | `sources/references-list.txt` 的 17 处错误：是否原地修正，还是另存 `references-list-verified.txt`？ | 建议**另存新文件**并保留原文件（可追溯修正历史） | **未动** |
| V4 | 是否现在做剩余 28 条的独立抽查（我逐条复核子代理结论）？ | 建议**推迟到实际写入时**（写入时必须复核），现在做性价比低 | **未做** |

---

## 6. 质量门自检（本文件）

| 门 | 结论 | 说明 |
|---|---|---|
| A 真实性 | **通过** | 每条给建议引用版本与依据来源类型；两条锚点由我独立核验；无法直读的来源（dblp/ieeexplore/iso.org/nature.com）已显式记录，受影响字段标 `[待核实]` |
| B 证据等级 | **通过** | 核验结论属"事实层"，不涉及研究结论强度；未把任何"已发表"写成"重要性/质量"判断 |
| C 统计与因果 | **N/A** | 本文件不含统计量 |
| D 顶刊匹配 | **未过（本轮不适用）** | 内部审计，不产出投稿材料；但 §3.1 的定位修正直接服务 P2 的 venue 匹配 |
| E 伦理合规 | **通过（有条件）** | 引用纪律已按 §4 收紧；`[待核实]` 字段清单已列出，禁止肯定表述 |
| F 语言 | **通过** | 中文说明；英文题名与 venue 保留原文 |

---

## 7. 下一步（3 个选项，推荐在前）

1. **(推荐) 修正 `AGENTS.md` §6 的引用锚点（V1）并为 P2 定位句换措辞（V2）**：这是"先改台账再改稿"的最小动作，且防止同一个事实错误在五篇稿件里扩散。**最低成本路径**（两处文本改动）。
2. **另存 `sources/references-list-verified.txt`（V3）**：把 17 处修正落到一份可审计的新清单里，原件保留。可与选项 1 同批完成。
3. **回到实验线**：按 `02-repo-skeleton.md` 建目录 + README 契约（零算力可做），或起草数据使用申请（解除 R8）。venue 线已收口，不构成阻塞。
