# 检索日志（Search Log）— auto-driving / P1 OTF-CfC 技术知识地图

> 技能：`paper-discovery`（协议七要素）＋ `citation-and-related-work`（引用三层核验）
> 执行日期：2026-10-02 ｜ 执行者：DSH 会话（Node fetch 探针脚本，未用 Invoke-WebRequest）
> 交付对象：`文献需求-50篇顶刊.md`、`final_list_table.md`、`final_list.jsonl`、`refs.bib`
> 全部检索式与原始日志：`scripts/*.mjs`、`candidates_*.log.json`、`dois_*_log.txt`

---

## 一、检索目标与边界

**目标问题六要素**（P1 = 论文 1「OTF-CfC：基于超车频次势场与液态神经网络的高速主线混行编队连续时间控制」）

| 要素 | 内容 |
|---|---|
| 对象 | 高速公路主线多车道、人工+自动混行交通流中的自车/编队 |
| 干预 | Liquid Neural Network（CfC/LTC）连续时间控制器 + OTF（超车频次）势场作为 ODE 边界条件 |
| 比较 | PID、线性化 MPC、学位论文 TD3 直控（基线） |
| 结局 | 跟车误差 RMSE、加速度平方积分、Jerk 峰值、车道居中偏差、前轮转角方差、端到端延迟、MCU 内存占用 |
| 条件 | 仿真（CARLA Town04）+ 学位论文高速实车数据回放；非均匀采样；边缘 MCU 部署 |
| 时间窗 | 无下限（保留奠基文献）；上界 2026-10-02 |
| 语言/类型 | 英文；期刊论文为主（含少量会议论文作附录） |

**纳入判据（三条同时满足）**：
1. 与 P1 的六要素至少一项直接相关（方法学 / 场景 / 基线 / 指标 / 安全 / 部署）；
2. 有 DOI 或 arXiv 持久标识，且经核验可解析；
3. 发表于本领域主流期刊（IEEE T-ITS / TIV / TAC / TCST / TPAMI / TNNLS、Transportation Research Part C、Automatica、Nature Machine Intelligence、Science Robotics、Annual Review of Control Robotics and Autonomous Systems 等）或奠基性会议（NeurIPS / ICML / ICLR / AAAI / CVPR / CoRL / ECC）。

## 二、词表（关键词三层法）

| 层 | 词 |
|---|---|
| 核心层 | liquid neural network｜liquid time-constant｜closed-form continuous-time｜neural ODE｜car-following｜string stability｜platoon｜mixed traffic｜lane change／overtaking｜control barrier function｜model predictive control｜reinforcement learning |
| 扩展层 | LNN｜LTC｜CfC｜NCP｜neural circuit policy｜continuous-depth｜adjoint sensitivity｜Dopri5／adaptive step size｜ACC｜CACC｜mixed autonomy｜cut-in｜safety filter｜reachability｜online verification｜embedded／microcontroller／TinyML｜quantization／pruning／knowledge distillation |
| 限定层 | autonomous driving｜automated vehicle｜highway｜vehicle platoon｜intelligent transportation｜vehicle control｜edge deployment |
| 排除层 | 生物医学、材料、社科等领域同词异义命中（由 venue ISSN 限定层排除） |

## 三、通道与理由

| 通道 | 为什么必要 | 状态 | 命中（sum of `hits`） | 导出 |
|---|---|---|---|---|
| OpenAlex `api.openalex.org/works`（主题检索 T01–T16） | 全学科首选、可做被引排序与 venue 分布 | 200（前 16 式） | 774,531 | 480 |
| OpenAlex（venue ISSN 锚定 K01–K22 × 3 簇） | 把检索钉在顶刊集合内，避免跨领域噪声（第一轮实测：T08 类宽词命中 46.7 万且 90% 无关） | 200 ×58 式，**失败 ×16 式** | 13,777 | 440 |
| OpenAlex（缺口主题 D01–D12 × 3 簇） | 补嵌入式部署/车辆控制两个缺口 | **全部失败 ×36 式** | 0 | 0 |
| Crossref `api.crossref.org/works` | DOI 元数据权威校验（题名/年/卷期页/作者） | 200 | — | 121 条 DOI 逐条核验 |
| arXiv `export.arxiv.org/api/query` | 预印本存在性、版本号、journal-ref | 200（分批请求） | — | 32 个 arXiv ID 逐条核验 |

**通道失败记录（必须写进限制）**：OpenAlex 对匿名 IP 采用日额度制，本会话在第一轮 16 式 + 第二轮 74 式之后额度耗尽（`429 Insufficient budget ... creditsRemaining 9, resets at midnight UTC`）。第三轮缺口检索（D01–D12）与 `title.search` 精确匹配路径**全线 429**，因此**嵌入式部署（TinyML/MCU 量化）一类证据在本清单中薄弱**——这不是"没有文献"，而是**本会话未检索到**，见第八节限制。

## 四、检索式全集（可原样复制）

**Q-T（主题检索，OpenAlex；T01–T16 见 `scripts/search.mjs` 的 `QUERIES`）**
```
https://api.openalex.org/works
  ?search=<主题式>
  &filter=type:article,language:en
  &sort=cited_by_count:desc&per-page=30
  &select=id,doi,title,display_name,publication_year,publication_date,type,cited_by_count,authorships,primary_location,language
  &mailto=research@example.org
```

**Q-K（venue 锚定检索，OpenAlex；K01–K22 × 3 簇，见 `scripts/search3.mjs`）**
```
https://api.openalex.org/works
  ?search=<主题式>
  &filter=primary_location.source.issn:<ISSN 用 | 连接>,from_publication_date:2012-01-01,language:en
  &sort=cited_by_count:desc&per-page=8
  &select=id,doi,display_name,publication_year,publication_date,type,cited_by_count,authorships,primary_location,language
  &mailto=research@example.org
```
venue 簇的 ISSN（**经 OpenAlex `/sources` 端点核验，2026-10-02**）：

| 簇 | ISSN |
|---|---|
| transport | 1524-9050 (T-ITS)｜2379-8858 (T-IV)｜0968-090X (TR-C)｜0191-2615 (TR-B)｜0018-9545 (TVT)｜0041-1655 (Transportation Science)｜0965-8564 (TR-A) |
| control | 1063-6536 (TCST)｜0018-9286 (TAC)｜0005-1098 (Automatica)｜2377-3766 (RA-L)｜1556-4959 (JFR)｜2470-9476 (Science Robotics)｜2573-5144 (Annu. Rev. Control Robot. Auton. Syst.) |
| ml | 2522-5839 (NMI)｜0162-8828 (TPAMI)｜2162-237X (TNNLS)｜1532-4435 (JMLR)｜2041-1723 (Nat. Commun.)｜2471-285X (TETCI)｜0925-2312 (Neurocomputing) |

**Q-D（DOI 存在性 + 字段核验，Crossref）**
```
https://api.crossref.org/works/<DOI>            # 返回 JSON = 存在；404 / "Resource not found." = 不存在
https://api.crossref.org/works?query.bibliographic=<题名>&rows=6
  &select=DOI,title,author,issued,container-title,type,volume,issue,page,is-referenced-by-count,publisher
  &mailto=research@example.org
```

**Q-A（arXiv 存在性/版本，分批 ≤6 个 ID，间隔 ≥4 s）**
```
https://export.arxiv.org/api/query?id_list=<id1,id2,...>&max_results=20
```

## 五、去重与规范化

| 轮次 | 去重前 | 去重后 | 合并对数 | 规则 |
|---|---|---|---|---|
| 第一轮（主题 T01–T16） | 480 | 420 | 60 | DOI（小写）> OpenAlex Work ID |
| 第二轮（venue K01–K22 × 3） | 440 | 321 | 119 | 同上；同 key 合并 `theme_ids` |
| 第三轮（缺口 D01–D12 × 3，OpenAlex） | 0 | 0 | 0 | **通道失败（额度耗尽），未产出** |
| 第四轮（缺口补检，Crossref 短语精确式） | 225 | 150 | 75 | DOI 去重；`gap_embedded_crossref.jsonl` |
| 第五轮（近两年增量，Crossref，`sort=published`） | 225 | 131 | 94 | 同上；`gap_recent_crossref.jsonl` |
| 第六轮（近两年增量，arXiv `sortBy=submittedDate`） | 163 | 163 | 0 | 仅保留 `published ≥ 2024-01-01`；`gap_recent_arxiv.jsonl` |
| **候选池合计** | 1,533 | **765** | 348 | 420（T）+ 321（K）+ 150（E）+ 131（R）+ 163（arXiv）－重叠 |

**第四轮检索式（Crossref 精确短语，可原样复制；注意 Crossref 不支持 `language` 过滤器，加了会 400）**
```
https://api.crossref.org/works?query.bibliographic=<"短语" 空格分隔>
  &filter=from-pub-date:2017-01-01,type:journal-article
  &sort=is-referenced-by-count&order=desc&rows=25
  &select=DOI,title,author,issued,container-title,type,volume,issue,page,is-referenced-by-count,publisher,abstract
  &mailto=research@example.org
```
短语集（9 式）：`"TinyML" "microcontroller"`｜`"tiny machine learning" survey`｜`"post-training quantization"`｜`"quantization" "neural network inference" survey`｜`"knowledge distillation" survey`｜`"model compression" "deep neural network" survey`｜`"edge intelligence" "deep learning" survey`｜`"Cortex-M" neural network kernel`｜`"on-device" inference latency microcontroller`

**第五轮** 同式但 `sort=published`、`from-pub-date:2024-01-01`，短语集（9 式）：`"liquid neural network"`｜`"liquid time-constant"`｜`"closed-form continuous-time"`｜`"neural ordinary differential equation" control`｜`"string stability" "mixed traffic"`｜`"car-following" "reinforcement learning"`｜`"control barrier function" "learning-based control"`｜`"vehicle platoon" "mixed traffic" control`｜`"overtaking" "traffic flow" stability`

**第六轮（arXiv，`export.arxiv.org`，间隔 ≥3.6 s）**
```
https://export.arxiv.org/api/query?search_query=<all:"短语" 布尔式>
  &start=0&max_results=30&sortBy=submittedDate&sortOrder=descending
```


**终选方法（非"凭记忆列表"）**：
1. 从 321 条 venue 锚定候选池中按「引用数 × 主题归属 × 期刊」取每刊头部；
2. 加上 P1 蓝图与学位论文明确点名的方法学锚点（CfC/LTC/NCP/CBF/TD3 等）；
3. 每条给 DOI 后用 `scripts/check_dois.mjs` **逐条回 Crossref 核验**：题名 token-Jaccard、年份、卷期页；
4. 无 Crossref DOI 的条目（arXiv/无 DOI 经典文献）用 arXiv API 单列核验，标 `ARXIV-ONLY`。

**核验结果（Crossref 逐条）**：`dois.json` 53 条 → 51 条题名完全匹配（Jaccard = 1.0）、2 条 arXiv DOI 未在 Crossref 注册（`10.48550/arXiv.1802.09477`、`10.48550/arXiv.1801.01290`，属预期）；`dois_appendix.json` 26 条 → 16 条匹配、10 条需人工判定 → 已逐条处置（见核验证伪记录）。**最终清单 75 条**（n=1–53 与 101–125），其中期刊论文 62 条。

## 五之二、缺口补检的最终结果（第四～六轮）

| 缺口 | 结论 | 证据 |
|---|---|---|
| **嵌入式 / TinyML / MCU 部署** | **部分补上**：Concept-drift 审核后保留 6 条可用候选（见下）。但**仍未达到与原 50 篇相同的筛选强度**——Crossref 无法按被引做主题内排序（相关性为 OR 语义），逐条排序需 OpenAlex | `gap_embedded_crossref.jsonl`（150 条）+ 关键词过滤（26 条命中）+ 人工挑选 |
| **2024 年以后的新工作** | **补上且发现 1 篇高相关竞争工作**：`Liquid-Graph Time-Constant Network for Multi-Agent Systems Control`（**IEEE CDC 2024**，DOI 10.1109/cdc56724.2024.10886394）——LNN/LTC 直接用于**多智能体控制**，与 P1 的编队控制同域，**必须引用** | `gap_recent_arxiv.jsonl`（163 条）+ Crossref 版本核验 |
| **OpenAlex 引文展开（外部复现状态）** | **未做**：额度 00:00 UTC 重置（本机 UTC 04:33 时仍需约 19.5 小时）；`filter=cites:` 路径不可用 | 429 响应 `retryAfter:72922` |

**第六轮新增、且已核验有正式发表版本（可入 P1 引用库）**

| 新增 | 题名 | 正式出处 | DOI / 链接 | 与 P1 的关系 |
|---|---|---|---|---|
| N1 | Liquid-Graph Time-Constant Network for Multi-Agent Systems Control | **IEEE CDC 2024** | [10.1109/CDC56724.2024.10886394](https://doi.org/10.1109/CDC56724.2024.10886394) | **最接近 P1 的 LNN 控制类新工作**（LTC + 图结构 + 多智能体控制）；P1 必须引用并说明差异（P1 是公路编队 + OTF 势场，非一般多智能体图控制） |
| N2 | LNN-Powered Fluid Antenna Multiple Access | IEEE Access 2026 | [10.1109/ACCESS.2026.3685975](https://doi.org/10.1109/ACCESS.2026.3685975) | LNN 在通信系统中的应用；**旁证**：LNN 已进入工程系统的实时决策，不再是纯 toy 模型 |
| N3 | Liquid Fourier Latent Dynamics Networks for fast GPU-based numerical simulations in computational cardiology | Computers in Biology and Medicine 2026 | [10.1016/j.compbiomed.2025.111355](https://doi.org/10.1016/j.compbiomed.2025.111355) | LNN 类模型做**高维动力系统快速仿真**；P1/P5 的"连续时间模型替代数值积分"论据旁证 |

**第四轮新增、可用作 P1 部署论证的候选（题名与 DOI 均经 Crossref 返回核验）**

| 新增 | 题名 | 出处 | DOI | 与 P1 的关系 |
|---|---|---|---|---|
| N4 | Efficient Processing of Deep Neural Networks: A Tutorial and Survey | Proceedings of the IEEE 2017 | [10.1109/JPROC.2017.2761740](https://doi.org/10.1109/JPROC.2017.2761740) | 边缘推理的**标准综述**（数据流/能耗/加速器）；P1 的 `<1 ms / <500 KB` 工程论证的方法学入口 |
| N5 | Machine Learning for Microcontroller-Class Hardware: A Review | IEEE Sensors Journal 2022 | [10.1109/JSEN.2022.3210773](https://doi.org/10.1109/JSEN.2022.3210773) | **MCU 级硬件的 ML 综述**（内存/算力约束、TinyML 工具链）；P1 部署章节的直接依据 |
| N6 | Knowledge Distillation: A Survey | International Journal of Computer Vision 2021 | [10.1007/s11263-021-01453-z](https://doi.org/10.1007/s11263-021-01453-z) | 若 P1 需把 CfC 压到 MCU 预算，蒸馏是候选手段；也是"<500 KB"路线的备选方案 |
| N7 | TinyML-Enabled Frugal Smart Objects: Challenges and Opportunities | IEEE Circuits and Systems Magazine 2020 | [10.1109/MCAS.2020.3005467](https://doi.org/10.1109/MCAS.2020.3005467) | TinyML 的**问题定义文献**；用于界定"何为微控制器级部署" |
| N8 | TinyML Meets IoT: A Comprehensive Survey | Internet of Things 2021 | [10.1016/j.iot.2021.100461](https://doi.org/10.1016/j.iot.2021.100461) | 部署流程与工具链综述；P1 复现性章节可引 |

## 六、检索核验证伪记录（本次抓出的真实错误）

| # | 原拟写法 | 核验发现 | 处置 |
|---|---|---|---|
| 1 | "Swaroop & Hedrick. String stability of interconnected systems. IEEE TAC 1996. DOI 10.1109/9.539424" | DOI `10.1109/9.539424` 实为 **Morse, "Supervisory control of families of linear set-point controllers – Part 1"**（同卷同页段），**题名 Jaccard = 0**；该弦稳定性论文作者实为 **Darbha & Hedrick**（[researchr 记录](https://researchr.org/publication/DarbhaH96)） | **不附 DOI**，仅给题录并标注更正（附录 #105） |
| 2 | "MOBIL: General lane-changing model for traffic simulators" | DOI `10.3141/1999-10` 的正确题名为 **"General Lane-Changing Model MOBIL for Car-Following Models"**（TRR 1999: 86–94, 2007） | 题名按 CrossRef 权威值更正（附录 #109） |
| 3 | "TransFuser… IEEE TPAMI 2023, DOI 10.1109/TPAMI.2022.3200242" | **Crossref 无此 DOI 记录**（返回 Resource not found） | 该条本次**不入选**，标 `[待核实]` 并列入待办 |
| 4 | "DAgger… DOI 10.5555/3157743.3157871" | Crossref 未注册该 DOI（AISTATS/PMLR 类常无 Crossref DOI） | 本次不入选 |
| 5 | "Hamiltonian Neural Networks DOI 10.48550/arXiv.1906.01563" | arXiv **存在且题名一致**（NeurIPS 2019），但 arXiv DOI 不在 Crossref | 本次不入选（避免混入未核验条目） |
| 6 | 6 篇 IEEE 期刊论文的年份（9/10/11/14/29/31/32/40/46/48/49/50） | Crossref 记录的**卷期年**比在线首发年晚 1–2 年 | 输出以 **Crossref 卷期年**为准，并逐条留 `year_note` |
| 7 | TD3 / SAC 的 arXiv DOI | `10.48550/*` 在 Crossref 无注册记录（预期行为） | 保留 arXiv DOI + 明确标注"引 PMLR/ICML 正式版" |

## 七、候选池摘要

- 年份分布（P1 清单 75 条）：1995–1999 年 2 条｜2000–2012 年 2 条｜2013–2019 年 24 条｜2020 年及以后 47 条。
- venue 分布（n=1–53，按 Crossref `short-container-title`）：IEEE T-ITS 10｜Transportation Research Part C 7｜IEEE TCST 7｜Nature Machine Intelligence 6｜IEEE TAC 6｜Annual Review of Control Robotics and Autonomous Systems 4｜IEEE T-IV 4｜Automatica 3｜Science Robotics 2｜ICML (PMLR 80) 2｜IEEE RA-L 1｜Neurocomputing 1。
- 被引（Crossref `is-referenced-by-count`，2026-10-02 快照）：清单最高 **6145**（Milanés 等, IEEE T-ITS 2014, CACC 真车实测）；>500 的条目共 **30 条**（1–53 条内 20 条）。**该数值与 OpenAlex / Google Scholar 口径不同，跨库不可比**。

## 八、限制（≥3 条，按实际执行写）

1. **通道覆盖限制**：本次成功使用了 **OpenAlex（额度内）+ Crossref + arXiv** 三个通道。**Semantic Scholar、OpenCitations COCI、dblp、Web of Science、Scopus 未使用**；学位论文库与非英文文献库未覆盖。dblp / ieeexplore 正文在本机被反爬或 403（沿用项目 `audit/第一次组会/05-citations.md` 的既有记录；该文件由主支 2026-10-08 从 `audit/05-citations.md` 迁入 `第一次组会/` 子目录）。
2. **额度限制（硬，且未解除）**：OpenAlex 匿名 IP 日额度在前两轮耗尽（`429 Insufficient budget ... retryAfter 72922 s`，按 **UTC 午夜**重置；本机 UTC 04:33 时仍需约 19.5 小时）。后果有二：① 第三轮（D01–D12 × 3 簇）36 式全 429；② **`filter=cites:` 引文展开不可用 → 六篇精读笔记的"外部复现"列只能写"未检"**（这是信息缺失，不是"无外部证据"）。
3. **缺口补检的强度不等价**：第四轮用 Crossref 精确短语式补嵌入式主题，但 **Crossref 无法做主题内按被引排序**（`query.bibliographic` 是 OR 语义，命中数高达 75 万–250 万），因此 N4–N8 是"关键词过滤 + 人工挑选"的产物，**强度低于原 50 篇**（后者由 OpenAlex venue 锚定 + 被引排序得到）。**P1 的 `<1 ms / <500 KB` 主张仍不得仅凭本轮补检下定论**。
4. **截断限制**：每式仅导出 `cited_by_count` 或 `published` 降序的前 8–30 条（`per-page` 见各脚本），属**排序截断**而非穷尽。
5. **时间限制**：检索截止 **2026-10-02**；Crossref 被引数为当日快照。
6. **核验层级限制**：层 1（存在性）与层 2（字段一致性）已完成；**层 3 仅完成 6 篇**（#1/#7/#15/#33/#43/#45，见 `notes/citation-qualifiers.md`），其余 69 条**未做层 3**。因此本清单**只能作为候选引用库，不能作为"可直接写入稿件"的引用表**。
7. **版本口径限制**：#1（CfC）与 #7（PINC）的精读基于 **arXiv 版**，未核对 NMI / Neurocomputing 正式版；两条的 `citation_qualifier` 末尾已显式写入该缺口。
8. **题名口径限制**：终选题名一律取 **Crossref 权威题名**；若与 arXiv 题名或常用简称不同（如 CfC 的 "neural networks" vs "Neural Models"；MOBIL；DriveDreamer 的 "Real-World-Driven"），以 Crossref 为准并已在清单标注。

## 九、下一步（本轮的完成情况与剩余项）

**已完成**：① 合表（`library/P1-library.jsonl`，98 条唯一记录 = 75 主记录 + 23 旧库独有）；② 缺口补检（第四～六轮，新增 8 条候选 N1–N8）；③ 层 3 精读 6 篇（`notes/*.md` + `notes/citation-qualifiers.md`）。

**剩余项（按优先级）**：
1. **（推荐）等 OpenAlex 额度重置（UTC 00:00）后做引文展开**：对 6 篇精读文献执行 `filter=cites:<WorkID>`，把"外部复现"列从"未检"升级为"已检：N 篇同向/反向"——这是**唯一能把经典文献从 B_int 升到 A 级**的路径（`deep-paper-reader` §3.1.1）。
2. **取两篇正式版复核**：#1 的 NMI 4(11):992–1003 与 #7 的 Neurocomputing 579:127419（arXiv 版 48 条参考文献 vs VoR 57 条），逐条核对表号与数值。
3. **对剩余 69 条做层 3 抽查**：至少覆盖 n=2/4/9/23/44（LNN 实机、安全验证、RL 综述、CBF-QP、混行编队）五条，方法同本轮。
4. **把 N1–N8 并入 `final_list.jsonl`**（下一轮重建时一并处理），并按 `AGENTS.md` §6 的登记规则同步到 `sources/` 的引用库说明。

