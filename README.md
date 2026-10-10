# auto-driving — OTF 论文集群（工作仓库）

> **项目不变量在 [`AGENTS.md`](AGENTS.md)，优先级高于本文件。** 本文件只讲"东西放在哪、数字从哪来"。

## 1. 这个仓库在做什么

以黄梦圆《基于超车频次的自动驾驶车辆行为决策研究》（吉林大学，2023）的 OTF 参数为锚点，做五篇论文（P1 OTF-CfC → P2 SocialDreamer → P3 TalkOTF → P4 IsoLNN → P5 AdjointStack）。台账见 [`papers/portfolio.md`](papers/portfolio.md)（唯一状态来源）。

**当前状态（诚实版）**：无 GPU；学位论文数据与 TD3 代码不在本机；CARLA 环境未见。因此当前可做的是**契约冻结**与**文献底座**，不是实验。**例外**：交通仿真工具 **Eclipse SUMO 1.27.1 已装于 `D:\SUMO\sumo-1.27.1` 并四项实测通过（含 Python TraCI）**——它纯 CPU 可跑，是目前唯一能独立产出"带 OTF 真值的合成交通流"的工具；但其在五篇论文中的定位**尚未裁决**（见 [`AGENTS.md`](AGENTS.md) §2、§7）。

> **跨对话**：本项目由多个分支对话并行推进，分支登记与协作契约见 [`AGENTS.md`](AGENTS.md) §0。本文件只讲"东西放在哪、数字从哪来"。
>
> **★ 每次会话开工先做三件事**（用户 2026-10-08 指定，详见 [`AGENTS.md`](AGENTS.md) §0）：① 读 `AGENTS.md`；② 同步分支与主支的信息差（目录是否被搬动、引用路径是否失效）；③ 跑一次进度快照校验
> `node scripts/smoke/check_progress_snapshot.mjs`（不一致即退出码 1，**先修再干活**）。

## 2. 三个契约

### 2.1 数字只有一个入口

```
results/<paper>/<experiment>_<scenario>_<seedset>.json
```

例：`results/p1/main_otf_cfc_highway-mixed_s1.json`

- 命名取值域见 [`docs/README.md`](docs/README.md)；**禁止** `final.json` / `v2.json` / 带日期的文件名——版本靠 git。
- 任何进入论文、回复信、报告的数字，必须能指到上述文件的**具体字段**。
- JSON 必填字段与 schema：[`configs/schema/results.schema.json`](configs/schema/results.schema.json)（字段只增不改）。

### 2.2 自检与真实算例物理隔离

| 目录 | 内容 | 能否被引用 |
|---|---|---|
| `runs/smoke/` | 冒烟、管线自检、调试产物 | **绝对不能**（`mode: "smoke"`） |
| `runs/real/` + `results/` | 真实算例产物 | 只有 `mode: "real"` 且 `config_hash` 可追溯的可引用 |

### 2.3 每个实验先有配置

`scripts/run/` 只接受 `configs/<paper>/*.yaml` 的路径，不接受手敲参数。环境锁在 `configs/env/`。

## 3. 目录地图

| 路径 | 放什么 |
|---|---|
| [`AGENTS.md`](AGENTS.md) | **项目不变量（最高优先级）**：主张上限、数据与结果、统计口径、分支登记（§0） |
| [`audit/`](audit/) | 审计产物，**按会议轮次分子目录**：`第一次组会/`（盘点 00／骨架 02／风险 03／数据申请 04／引用核验 05）、`第二次组会/`（三组主题会前材料与汇报） |
| [`literature/`](literature/) | **文献底座**：检索日志、P1 引用库（`library/P1-library.jsonl`）、逐篇精读笔记（`notes/`、`meeting2/notes/`、`fresh2024/notes/`）、原文（`fulltext/`）、`refs.bib` |
| [`papers/`](papers/) | 台账（唯一状态来源）、P1 详纲、主张—证据台账 |
| [`sources/`](sources/) | 只读资料库（学位论文全文、蓝图、核验后引用清单） |
| [`configs/`](configs/) | 实验配置、环境锁、种子集、结果 schema |
| [`src/`](src/) | 模块实现——**谁生成数字写在这里** |
| `scripts/` | 薄壳入口（不含逻辑）＋ 组会文档生成器 |
| `runs/` | 运行日志与清单（原始产物；`.gitignore` 已排除） |
| `results/` | ⚠️ **数字唯一来源**；只允许 `scripts/run` 写入（当前为空） |
| [`docs/`](docs/) | 规范与清单：ODD、指标口径、场景判定规则（给人读，不是数字来源） |
| `自动驾驶_世界模型科研汇总/` | ⚠️ **用户手工资料库，只读**：蓝图×2、参考文献清单、DriveDreamer、Drive as You Speak、黄梦圆学位论文、按来源分类的顶刊 PDF。**不作结论来源** |

> 完整目录树（含每个目录的职责与命名契约）见 [`audit/第一次组会/02-repo-skeleton.md`](audit/第一次组会/02-repo-skeleton.md) §2。

## 4. 引用库（两处同源，各管一段）

| 范围 | 唯一来源 | 说明 |
|---|---|---|
| 跨论文共用的 30 条锚点 | [`sources/references-list-verified.txt`](sources/references-list-verified.txt) | 30 条已全量核验，17 处清单错误已修正；原 `references-list.txt` 仅作历史留存 |
| P1 的候选引用库（98 条） | [`literature/library/P1-library.jsonl`](literature/library/P1-library.jsonl) | 98 条唯一记录（75 主记录 + 23 旧库独有），合表报告见同目录 `merge-report.md` |

**写稿引用这 6 篇时必须逐字带上限定语**（CfC / PINC / 类人跟驰 / Lp 弦稳定 / 波消散 / DeeP-LCC）：[`literature/notes/citation-qualifiers.md`](literature/notes/citation-qualifiers.md)。

## 5. 零算力可开工顺序（W0–W3）

| 阶段 | 做什么 | 依赖 |
|---|---|---|
| W0 | 本骨架 + `docs/odd.md`、`docs/metrics.md`、`docs/scenario-taxonomy.md` | 无 |
| W1 | `src/otf/`、`src/eval/` 规则层复现（用合成轨迹自检） | 无 |
| W2 | `src/stats/`：种子聚合、mean±std / 95% CI、Wilson / Clopper-Pearson、种子独立性自检 | 无 |
| W3 | `configs/` 全量冻结 | 无 |
| W4+ | CARLA 闭环、A1–A5 真实算例 | **GPU + 数据** |

> ⚠️ W0–W3 的产物**不得**写成任何结论；它们的唯一用途是冻结契约。W0–W3 **不计入实验里程碑**（见 [`audit/第一次组会/02-repo-skeleton.md`](audit/第一次组会/02-repo-skeleton.md) §5）。

## 5.1 文献线（已完成，不依赖算力）

| 工作 | 产物 |
|---|---|
| 检索协议与日志（含失败检索式与额度原因） | [`literature/search-log.md`](literature/search-log.md) |
| P1 文献图（50 篇期刊 + 18 条附录，DOI 经 Crossref 逐条核验） | [`literature/文献需求-50篇顶刊.md`](literature/文献需求-50篇顶刊.md) |
| 层 3 精读（第二次组会主题 23 篇 + 2024+ 增量） | `literature/meeting2/notes/`、`literature/fresh2024/notes/` |
| 由此产生的三条硬约束 | [`AGENTS.md`](AGENTS.md) §1（参数量口径、术语口径）＋ [`audit/第一次组会/03-risk-register.md`](audit/第一次组会/03-risk-register.md) R20 |

## 6. 当前阻塞项

| 阻塞 | 状态 | 解除路径 |
|---|---|---|
| 数据不可得（A1 消融做不了） | 申请信待发出 | [`audit/第一次组会/04-data-request-and-ethics.md`](audit/第一次组会/04-data-request-and-ethics.md) |
| 无 GPU | 未决策（云端 or 降级） | 需你拍板 |
| TD3 基线：引用 vs 复现 | **未决策** | 影响 P1 主表结构 |
| OTF 增益口径（1.0–1.7% vs 论文实际 +2.23~+3.60） | **已修正**（口径统一为 +1.0~+5.5 个百分点，见 [`AGENTS.md`](AGENTS.md) §1） | — |
| P1 指标集无可对标物（延迟 / MCU 内存） | **开放**（新增） | [`audit/第一次组会/03-risk-register.md`](audit/第一次组会/03-risk-register.md) R20 |
| P1 参数量口径（"<500 KB" 已作废） | **已修正** | [`AGENTS.md`](AGENTS.md) §1 参数量口径 |
| git 未初始化（版本靠 git 的约定暂无法执行） | **未决策** | 需你确认是否 `git init` |
| SUMO 定位（替换 CARLA／只做交通流生成／并存） | **未决策（新增 2026-10-08）** | 见 [`AGENTS.md`](AGENTS.md) §2 与 §7；环境事实见 [`configs/env/local-cpu.lock.yaml`](configs/env/local-cpu.lock.yaml) 的 `sumo:` 段 |
| CARLA 是否已装、版本为何 | **仍未被核实** | 与 SUMO 是两件事，不得互相替代结论 |
