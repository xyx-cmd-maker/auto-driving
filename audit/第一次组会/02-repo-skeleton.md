# 仓库骨架建议（Repo Skeleton）

> 指令来源：`auto-driving/prompts/00-kickoff.md` §3；命名契约来源：`auto-driving/AGENTS.md` §2。
> **本文件只给目录与 README 规划，不含实现代码。**
> 约束前提：**无 GPU、数据不在本机**（盘点结论）→ 骨架必须做到"**零算力、零数据也能先把契约落地**"。
> ⚠️ **前提纠正（2026-10-11）**：上句的"**无 GPU**"**已作废**——实测 GPU 存在可用（RTX 5060 Laptop 8 GB / sm_120）。骨架的"零算力可落地"设计**依然成立且更有价值**（它让契约先于算力到位），但**不再是唯一路径**：立即可推的是装 CUDA torch + CARLA 后跑闭环 A1。见 `AGENTS.md` §2。
> **修订记录（2026-10-02）**：① §2 目录树重写，纳入 `literature/`、`自动驾驶_世界模型科研汇总/`、按会议轮次分目录的 `audit/`、`configs/schema/`、`scripts/smoke/**`；② 删除全部"【待建】/下一轮"过期标记（目录已实际建立）；③ §3.2 增补 `provenance` 与 `seed_independence` 两个必填字段，并给 `metrics` 补口径约束；④ §5 新增两条过度声称检查。

---

## 1. 设计原则（4 条，先定原则再定目录）

| # | 原则 | 理由（来自本项目硬约束） |
|---|---|---|
| P1 | **数字只有一个入口**：任何进入论文/回复信/报告的数字，必须能指到 `results/<paper>/<experiment>_<scenario>_<seedset>.json` 的**具体字段** | `AGENTS.md` §2；工作区约定 §2.1"数字的唯一来源" |
| P2 | **自检产物与真实产物物理隔离** | `AGENTS.md` §2 末句 + 工作区约定 §2.2：自检/冒烟/调试产物不得进入任何对外文本。物理隔离比纪律更可靠 |
| P3 | **每个实验一个配置文件**：不允许"手敲命令跑出来的结果" | 复现性要求环境锁、种子、超参（技能 `discipline-rigor` §0.8） |
| P4 | **不确定的数字写占位符，不写估计值** | `AGENTS.md` §2 + 全局 §0.1"不编造" |

---

## 2. 目录骨架（2026-10-02 实测重写）

```
auto-driving/
├─ AGENTS.md                      # 项目不变量（最高优先级，含 §0 分支对话登记）
├─ README.md                      # 新人上手：项目是什么、三个契约在哪、当前阻塞项
├─ papers/
│  ├─ portfolio.md                # 唯一状态来源（分支只读不改）
│  └─ p1-otf-cfc/
│     ├─ outline.md               # 【待建】P1 详纲（claim → 图表 → 实验 的一一映射）
│     ├─ claims-ledger.md         # 【待建】主张—证据台账：Claim｜证据｜等级A–D｜缺口｜最小补法
│     └─ venue-strategy.md        # 【待建】T-ITS / IV / ICRA 三档对比与 desk-reject 风险
├─ prompts/                       # 一次性任务指令（append-only，不改旧文件）
│  └─ 00-kickoff.md
├─ audit/                         # 审计产物：⚠ 按会议轮次分子目录
│  ├─ 第一次组会/                  # 立项前置：00 盘点 / 02 骨架 / 03 风险 / 04 数据申请 / 05 引用核验
│  └─ 第二次组会/                  # 会前材料（三组主题 PDF：TITS / 决策基线 / 连续时间流体神经网络）
├─ sources/                       # 只读资料库（不再新增副本）
│  ├─ thesis-huang2023.fulltext.txt      # 基准论文全文（可 grep）
│  ├─ references-list.txt                # 历史留存（有 17 处错误）
│  ├─ references-list-verified.txt       # ✅ 引用库唯一来源（30 条已核验）
│  ├─ blueprint-papers-v1.1.txt          # 论文规划（规划唯一依据）
│  ├─ blueprint-overview-v1.1.txt        # 架构与规范依据
│  ├─ drivedreamer-2023.fulltext.txt     # P2 对标原文
│  └─ drive-as-you-speak-2023.fulltext.txt  # P3 对标原文
├─ literature/                    # ✅ 已建立（252 文件）：文献检索与层 3 精读的落点
│  ├─ search-log.md               # 检索协议七要素与各轮命中/去重记录（可复现证据链）
│  ├─ 文献需求-50篇顶刊.md          # P1 的 50 篇期刊文献图 + 18 条附录
│  ├─ final_list.jsonl / refs.bib # 机器可读清单 / 可编译 BibTeX
│  ├─ library/                    # P1-library.jsonl（98 条唯一记录）+ merge-report.md
│  ├─ notes/                      # 逐篇精读笔记 + citation-qualifiers.md（逐字限定语基准）
│  ├─ meeting2/notes/             # 第二次组会主题的 23 篇精读记录
│  ├─ fresh2024/notes/            # 2024+ 增量分诊与笔记
│  ├─ fulltext/                   # 原文与提取文本（_raw / meeting2 / _tools）
│  └─ scripts/                    # 检索/核验/渲染脚本（*.mjs，可复跑）
├─ 自动驾驶_世界模型科研汇总/        # ⚠ 用户手工资料库，只读，不作结论来源
│  ├─ 蓝图×2 / 参考文献清单 / DriveDreamer / Drive as You Speak / 黄梦圆学位论文
│  └─ Automatic_feild_Top_Paper/  # 按来源分类：Arxiv预印本 / IEEE ACESS / Nature及其子刊 /
│                                 #   Top Journals / Top Conferences / 国家自然科学基金 / 个人感悟
├─ configs/                       # 每个实验一份配置；跑之前必须先有配置
│  ├─ env/
│  │  ├─ local-cpu.lock.yaml      # 本机现状：CPU-only（无 GPU）
│  │  └─ cloud-gpu.lock.yaml      # 云端：供应商待定，字段留空
│  ├─ schema/results.schema.json  # ✅ 结果 JSON 的字段契约（14 必填 + seed_independence）
│  ├─ seeds/seedset_s1.yaml       # 种子集 ≥5 + 独立性声明与泄漏检查清单
│  ├─ p1/                         # 【待填】baseline_pid / baseline_mpc / baseline_td3 / main_otf_cfc / ablation_a1..a5
│  └─ p2/ … p5/                   # 占位
├─ src/                           # 模块边界；谁生成数字写在这里
│  ├─ otf/ eval/ ctrl/ envs/      # OTF 复现 / 分层评估 / 控制器 / CARLA 与回放（回放命名强制含 replay）
│  ├─ metrics/                    # 指标口径唯一实现（见 §3.2 口径约束）
│  ├─ stats/                      # 聚合、区间估计、等价检验、种子独立性自检
│  └─ plots/                      # 出图脚本（每图一脚本，保证可从 json 重生成）
├─ scripts/                       # 入口脚本（薄壳，不含逻辑）
│  ├─ smoke/                      # 冒烟与自检（含 check_seed_independence.SPEC.md；产物进 runs/smoke/）
│  ├─ run/                        # 真实算例入口：只接受 configs/ 下的配置路径
│  └─ make_group_meeting_docx.py  # 组会文档生成器（python-docx，不装新包）
├─ runs/                          # 运行日志（smoke 与 real 物理隔离；`.gitignore` 已排除 runs/）
├─ results/                       # ⚠ 数字唯一来源；只允许由 scripts/run 写入（当前为空，符合无算力现状）
│  └─ p1/ … p5/                   # 命名见 §3.1
└─ docs/                          # 给人读的规范（不是数字来源）
   ├─ odd.md                      # ODD 声明（含天气边界：晴天）
   ├─ metrics.md                  # 指标定义、单位、采集平台与档位（含 MCU 内存的 Flash/RAM 拆分）
   ├─ scenario-taxonomy.md        # 四类工况 + 长尾四类的判定规则
   └─ data-licenses.md            # 学位论文数据许可、nuScenes/Waymo 条款、可否再分发
```

---

## 3. 命名契约（唯一来源规则的可执行化）

### 3.1 `results/` 文件命名

```
results/<paper>/<experiment>_<scenario>_<seedset>.json
```

| 字段 | 取值域（本项目） | 说明 |
|---|---|---|
| `<paper>` | `p1` … `p5` | 小写 |
| `<experiment>` | `main_otf_cfc` / `baseline_pid` / `baseline_mpc` / `baseline_td3` / `ablation_a1…a5`(+ 变体后缀) | 下划线分词，**不用连字符**（连字符留给变体值，如 `otf-off`） |
| `<scenario>` | `highway-mixed`（主场景）；长尾：`lead-brake` / `cutin-hard` / `platoon-exit` / `aggressive-flow`；辅助：`city-expressway-replay` | 与 `docs/scenario-taxonomy.md` 一一对应 |
| `<seedset>` | `s1`… | 指向 `configs/seeds/seedset_s1.yaml` 的具体种子列表 |

**禁止**：`final.json`、`v2.json`、`new.json`、带人名或日期的文件名。**版本靠 git，不靠文件名。**

### 3.2 每个 JSON 必须含的字段（缺一即不可用作出处）

| 字段 | 含义 | 为什么必须 |
|---|---|---|
| `paper` / `experiment` / `scenario` / `seedset` | 与文件名一致（自校验） | 防止文件被改名后失去可追溯性 |
| `seeds` | 实际使用的种子列表（≥5） | 只报最优运行是最常见的不端嫌疑（`discipline-rigor` §0.2） |
| `config_path` + `config_hash` | 配置路径与内容哈希 | 配置改了结果就不可复现 |
| `platform` | 平台类型（simulator/replay/mcu/cpu/cloud-gpu）与细节；MCU 须填 `compiler` | `AGENTS.md` §3 要求记录采集平台与档位 |
| `provenance` | `ours-reproduced` \| `literature-reported` \| `mixed` | 防止把他人论文数字当本方结果并列（`AGENTS.md` §1） |
| `mode` | `smoke` \| `real` | **`smoke` 产物一律不得引用** |
| `metrics.per_scenario` | 指标名 → 值，**逐场景**（不只总平均） | `AGENTS.md` §5"逐场景报告" |
| `aggregates` | `method` 枚举（mean-std / ci95-t / ci95-bootstrap / Wilson / Clopper-Pearson） | 小样本禁用正态近似（`AGENTS.md` §4） |
| `fairness` | 无特权输入 / 同等调参预算 / 同地图同种子 | `AGENTS.md` §3 公平性要求 |
| `failure_modes` | 失败案例分类与计数（闭环时） | 开环≠闭环；失败分类是评审必问项 |
| `notes.abandoned_settings` / `known_biases` | 失败设定与已知偏差 | 消融须报失败设定（`AGENTS.md` §4） |
| `notes.seed_independence` | `verified` / `split_policy` / `entity_group` / `partial_scope` | **任一检查 `not-run` 时 `verified` 必须为 false**；判定逻辑见 `scripts/smoke/check_seed_independence.SPEC.md` |

**口径约束（新增，写实现时必守）**

| 指标 | 口径要求 | 依据 |
|---|---|---|
| MCU 内存占用 | **必须拆成 Flash（权重）与 RAM（激活/峰值）两项，不得合并成一个数**；同时报量化位宽"从什么到什么"、以及精度的对应损失 | 层 3 精读结论（`literature/fresh2024/notes/sensors2025-tinyml-ondevice-survey.md`） |
| 端到端延迟 | 必须报控制周期，使"计算时间 / 采样周期"成为**可比的相对比值** | `literature/notes/p45-deeplcc-tcst2023.md` |
| 与弦稳定相关的结论 | **RMSE 小 ≠ 弦稳定**；若声称稳定性，须报**逐车误差传播曲线**；LTI 判据不得直接套到非线性 CfC | `literature/notes/p33-lpstring-tcst2014.md` |
| 参数量/模型大小 | 须写明**是否含感知头**与**量化精度**；在本项目实测前不得写"<500 KB" | `AGENTS.md` §1 参数量口径（2026-10-02） |

### 3.3 隔离规则（P2 原则的落地检查）

| 规则 | 检查方式（下一轮可做成自检脚本） |
|---|---|
| `runs/smoke/**` 永不进入 `results/` | 目录层级物理隔离 + 自检脚本扫描 `results/` 内的 `mode` 字段 |
| 对外文本只能引用 `mode: "real"` 且 `config_hash` 可追溯的 JSON | 出图脚本只接受 `results/` 路径 |
| `src/` 不写数字，`results/` 不出结论 | 代码评审项 |

---

## 4. 生成时机与"零算力可开工"顺序

| 阶段 | 可做（无需 GPU/数据） | 需 GPU 或数据 | 产物 |
|---|---|---|---|
| W0（本周） | 目录建立、README 契约、`docs/odd.md`、`docs/metrics.md`、`docs/scenario-taxonomy.md` 草案 | — | 骨架 + 契约 |
| W1 | `src/otf/` + `src/eval/` 的**规则层**复现（确定性函数，可用合成轨迹自检） | — | 单测 + smoke JSON |
| W2 | `src/stats/`（种子聚合 + Wilson/CP + 等价检验）——纯 CPU | — | 统计脚本 + 单测 |
| W3 | `configs/` 全量配置冻结 | — | 配置冻结记录 |
| W4+ | — | CARLA 闭环、TD3 训练/复现、A1–A5 真实算例 | `results/p1/*.json` |

> ⚠️ W1–W3 的产物**不得**写成任何结论；它们的唯一用途是把"契约"冻结，使拿到算力与数据后能直接产出可引用数字。

---

## 5. 风险与过度声称检查（本文件为非论文交付物，按技能输出契约第 5 条替换 `Limitations`）

| # | 风险 | 说明 | 缓解 |
|---|---|---|---|
| 1 | **骨架 ≠ 进展** | 建目录不产生任何科学证据；若把 W0–W3 当作里程碑汇报，会掩盖 R7/R8（算力与数据缺口） | 在 `portfolio.md` 中把 W0–W3 明确标为"契约冻结期"，不计入实验里程碑 |
| 2 | **契约先于数据风险** | JSON 字段按当前设想定义，拿到真实数据后可能需要增字段 | 版本化 schema 文件 `configs/schema/results.schema.json`，字段只增不改；改动需在 audit 记录 |
| 3 | **回放器命名带来过度声称** | `envs/replay` 若命名为 `real_*` 会被误读为实车验证 | 目录与脚本名强制含 `replay`；对外文本措辞上限为"在 CARLA 与真实数据回放中"（`AGENTS.md` §1） |
| 4 | **`baseline_td3.yaml` 的 mode 字段被忽略** | 若无人检查，仍可能出现"复现/引用"混称 | 该字段设为**必填枚举**，缺失即配置校验失败 |
| 5 | **工程指标被写成已成立**（2026-10-02 新增） | 本骨架初版曾写"参数量 <500KB"，而 CfC 原文全模型 230,828 参数（fp32 ≈ 902 KiB）且零硬件证据 → 已删除。同类风险还有"<1 ms 延迟""可上 MCU" | 写工程数字前先查 `AGENTS.md` §1 参数量口径；未实测一律写目标/`{{占位符}}`，并注明量化精度与是否含感知头 |
| 6 | **指标集无可对标物却被当作通用指标**（2026-10-02 新增） | P1 七项指标中，**端到端延迟与 MCU 内存占用在已检索的同类文献中均无对标物**；若把它们写进"与 X 对比"的表里会造成不公平比较 | 对标表只放**协议可比**的指标；不可比项单列并注明"文献无对应指标"；详见 `03-risk-register.md` R20 |

---

## 6. 下一步（3 个选项，推荐在前）

1. **(推荐) 我按本骨架建立目录 + README 契约文件**（仅目录与 README，不写实现代码）：一次写操作即可完成，之后 W1 的 `src/otf/`、`src/eval/` 才有落点。**最低成本路径**。
2. **先出 `docs/odd.md` + `docs/scenario-taxonomy.md`**（纯文档，从论文第 2、4、5 章抽取 ODD 边界与四类工况判定规则）：这两份是任何实验的前置，且不依赖算力与数据。
3. **等 venue 核验结果落地后一并复核骨架**（把待核验引用清单纳入 `docs/`）：避免引用库与目录结构二次返工。
