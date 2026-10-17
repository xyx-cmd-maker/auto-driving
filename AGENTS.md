# 自动驾驶全栈研究（OTF 论文集群）项目不变量

> ⚠️ **项目实例，只对本项目生效。不要复制到其他项目**——新项目请用模板 `C:\Users\本手\.dsh\templates\PROJECT-AGENTS.template.md`。
> 来源文档：`sources/blueprint-papers-v1.1.docx`（论文规划）、`sources/blueprint-overview-v1.1.docx`（综合文档）、`sources/thesis-huang2023.pdf`（学位论文，全文文本见 `sources/thesis-huang2023.fulltext.txt`，可 grep）。
> 基准资产：黄梦圆（2023，吉林大学，导师李世武）——OTF 参数、分层递阶评估、TD3 基线、实车数据集、四类工况场景库。**完整题名以 `sources/thesis-huang2023.pdf` 为准，引用须用全名。**

## 文件族（三份 AGENTS 效力相同，开工都要读）

| 文件 | 管什么 | 何时读 | 何时改 |
|---|---|---|---|
| **`AGENTS.md`**（本文件） | 入口：身份与红线、分支登记、开工协议、三问自检、待确认项、资料库索引 | **每次开工** | 红线/登记/协议变更时 |
| [`AGENTS-PROJECT.md`](AGENTS-PROJECT.md) | **项目进程同步**：目的、成果形态、venue 策略与纪律、进度快照、术语表、收工检查清单 | **每次开工** | **每轮收工**（快照必须更新） |
| [`AGENTS-NORMS.md`](AGENTS-NORMS.md) | **技能路由**（代码类/学术类触发即调用）、学术写作工作流、多轮验证协议、拆分规则 | **每次开工** | 技能或协议变更时 |
| [`AGENTS-LESSONS.md`](AGENTS-LESSONS.md) | **错误登记与预防**（★用户 2026-10-12 指定）：8 类反复错误模式 + 逐次明细 + 强制手段；**每轮收工必须追加一行** | **每次开工** | **每轮收工**（哪怕"本轮无新增"也要写一行） |

> 规则：新增规范**优先落到子文件**；本文件只保留入口级内容。**拆分与登记规则**见 `AGENTS-NORMS.md` §3；校验脚本 `scripts/smoke/check_agents_family.mjs`。
> **开工时**先跑 `node scripts/smoke/check_agents_family.mjs`（文件族完整性）＋ `check_progress_snapshot.mjs`（快照常量）＋ `check_branch_freshness.mjs`（分支新鲜度）。

## 0. 分支对话登记（跨对话信息同步）

> **会话结构**由用户 2026-10-02 指定：本文件是**跨对话同步的唯一落点**。任何分支产生的项目级事实、约束、状态变更，都要写回本文件才能被其它分支读到。

| 分支 | 角色 | 主要产出/落点 | 状态 | 最后更新 |
|---|---|---|---|---|
| **主支**（本对话） | 立项、资产盘点、引用核验、实验契约、风险登记、组会材料、**文件族与同步协议**；**负责把分支产出收编进项目级约定** | `AGENTS.md`＋`AGENTS-PROJECT.md`＋`AGENTS-NORMS.md`、`scripts/smoke/check_agents_family.mjs`、`audit/第一次组会/00`–`05`、`audit/第二次组会/组会汇报-第二次-*.docx`、`README.md`、`configs/**`、`papers/portfolio.md` | 进行中（2026-10-11：文件族拆分＋技能路由＋venue 策略＋三问/验证协议；2026-10-08：骨架重写、风险 12 条、第二次组会文档） | 2026-10-11 |
| **层 3 精读分支** | 文献检索与深度精读（九技能流水线）；产出 P1 的文献图与逐篇限定语 | `literature/**`（`search-log.md`、`library/P1-library.jsonl`＋`merge-report.md`、`notes/citation-qualifiers.md`、`meeting2/notes/**`、`fresh2024/notes/**`、`fulltext/**`、`refs.bib`） | 已产出，见 §1 新增约束。**2026-10-11 由主支补记**：`literature/` 下新增 **P3/P4/P5 三张文献图**（`p3/`、`p4/`、`p5/`）。**2026-10-12 由主支补记**：新增 **P2 文献图**（`p2/`，50 条 / 8 节 / 核验 394-404），至此 **P2–P5 四张图齐备**；工具 `scripts/literature/discover.mjs`、`triage.mjs` 已加入 p2 主题与**双层过滤**（驾驶语境 + 世界模型方法词）。**注意：复跑检索会漂移**（OpenAlex 命中数随时间变化，实测 P3-T1 3077→3084），已提交的图与日志保持同一取用日期，**复跑前先确认是否需要** | 2026-10-12 |
| **第二次组会分支** | 按主题归档论文原文并做会前材料 | `audit/第二次组会/**`（TITS、决策基线、连续时间流体神经网络三组 PDF） | 进行中 | 2026-10-08 |
| **分支：SUMO 环境线**（本对话，2026-10-08 登记） | 本机交通仿真工具链落地与验证（老师指派装 SUMO）；**只记录环境事实，不改研究设计** | SUMO 1.27.1 已装至 `D:\SUMO\sumo-1.27.1`（便携 ZIP、官方 SHA256 核验一致、无需管理员）；完整事实与四条验证记录见 `configs/env/local-cpu.lock.yaml` 的 `sumo:` 段；本文件 §2、§3、§7 与 `README.md` 已同步。**2026-10-11 由主支补记**：该锁文件新增 `gpu:` 段（GPU 实测纠正） | 安装完成且实测通过；**定位已裁决＝路线 B（2026-10-08）**，见 §2 | 2026-10-11 |
| **分支：GPU 环境线**（2026-10-11 登记，同属本对话） | CUDA 版 PyTorch 落地与验证；**只记录环境事实，不改研究设计** | [`configs/env/local-gpu.lock.yaml`](configs/env/local-gpu.lock.yaml)（安装记录＋11 项验证证据＋sm_120 约束）、`scripts/smoke/check_gpu_env.py`（可复跑自检） | 完成：torch 2.11.0+cu128 ＋ torchvision 0.26.0+cu128，**11/11 通过、6.7× 加速**；CARLA 见下行 | 2026-10-11 |
| **分支：CARLA 环境线**（2026-10-11 登记，同属本对话） | CARLA 仿真器落地与验证；**只记录环境事实，不改研究设计** | [`configs/env/local-carla.lock.yaml`](configs/env/local-carla.lock.yaml)、`scripts/smoke/check_carla_env.py`（连通冒烟 8/8）、**`src/envs/carla_town04.py`（闭环环境，自检 8/8）**、`src/ctrl/cfc.py`、`src/eval/metrics.py`；**装于 `D:\CARLA`**（18.07 GB，原 F: 因掉盘搬迁），桌面 3 个快捷方式；**并装 Python 3.12.10**（仅 CARLA 用） | **✅ 全线打通**：服务端 25 s 就绪、客户端 8/8、**Town04 可用**、**闭环环境自检 8/8**（前车检测 50.9 m、场景注入 500 样本、实时倍率 2.27×） | 2026-10-11 |
| **资料归档（非分支）** | 用户手工整理的原始资料库 | `自动驾驶_世界模型科研汇总/**`（蓝图×2、参考文献清单、DriveDreamer、Drive as You Speak、黄梦圆学位论文、`Automatic_feild_Top_Paper/**` 分期刊归档） | 只读，**不视为项目结论来源** | —（非分支，不校验） |

> ⚠️ **上表"最后更新"列的校验**：`scripts/smoke/check_branch_freshness.mjs` 会读下表的 `watch-paths`，算出每个分支**产出落点的最新文件 mtime**，与本列比对；**落后超过 3 天即报 stale（退出码 1）**。
> 规则：分支只要改了产出，**必须当场更新本行的"最后更新"**；否则其它分支看到的是过期状态。
>
> ```text
> branch-watch:
>   主支: AGENTS.md, AGENTS-PROJECT.md, AGENTS-NORMS.md, AGENTS-LESSONS.md, audit/第一次组会, audit/第二次组会, papers, configs, docs, scripts, README.md
>   层 3 精读分支: literature
>   第二次组会分支: audit/第二次组会
>   分支：SUMO 环境线: configs/env, scripts/smoke
>   分支：GPU 环境线: configs/env/local-gpu.lock.yaml, scripts/smoke/check_gpu_env.py
>   分支：CARLA 环境线: configs/env/local-carla.lock.yaml, scripts/smoke/check_carla_env.py
> ```

> ⚠️ **路径纪律**：`audit/` 下的文件**按会议轮次分子目录**（`第一次组会/`、`第二次组会/`）。本文件中出现的 `audit/00-…` 等简写，实际路径为 `audit/第一次组会/00-…`；分支新增产物必须写**完整相对路径**，避免跨分支引用失效。
> ⚠️ **环境事实也算项目级事实**：分支装了工具、改了环境变量、跑通了什么，**不能只写在 `configs/env/` 的分支文件里**——必须同时提升到本文件 §2 与 `README.md` §1/§6，否则其它分支读不到（SUMO 的登记即按此办理）。

**协作契约**

1. **先改本文件，再改产物**：分支若要新增项目级硬约束（如 §1 的参数量口径、术语口径），须落在本文件 §1–§7 对应位置，并注明**日期 + 出处路径**；只在分支目录里写 = 其它分支读不到。
2. **冲突以本文件为准**：分支结论与主支产物冲突时，改主支产物；**不擅改 `sources/` 下的原始文档**（蓝图/学位论文/清单）——只在项目文件中标注差异。
3. **分支不得覆盖主支的台账**：`papers/portfolio.md` 是唯一状态来源，分支只读不改；需要改状态时向主支提出。
4. **文献库同源**：引用库以 `literature/library/P1-library.jsonl`（P1）与 `sources/references-list-verified.txt`（跨论文共用 30 条）为准，二者关系见 `literature/library/merge-report.md`。

**每次会话开工协议（用户 2026-10-08 指定，强制）**

1. **先读本文件族**：动作之前先读 `AGENTS.md` ＋ [`AGENTS-PROJECT.md`](AGENTS-PROJECT.md) ＋ [`AGENTS-NORMS.md`](AGENTS-NORMS.md)。**不读不开工**——防止凭记忆做事、把已作废的口径写回去。
   - 顺带跑三个自检：`check_agents_family.mjs`、`check_progress_snapshot.mjs`、`check_branch_freshness.mjs`（均在 `scripts/smoke/`）。
2. **先同步，再干活**：核对**本分支 vs 主支**的信息差：
   - 本分支在 §0 表里的行是否还在？角色/产出/状态/"最后更新"是否需要更新？
   - 主支是否搬动了目录、改了文件名、更新了 `papers/portfolio.md` 或本文件族？
   - **本分支上一轮的产出是否已被收编**（例：`audit/` 文件被移入 `第一次组会/`）？**被搬动就必须同步修正引用路径**。
   - 发现信息差 → **先修引用、先补登记，再开始本轮任务**。
3. **实时更新进度，不攒到最后**：完成任何改变项目状态的工作（新增/搬动/重命名文件、装工具、改环境变量、产出风险条目、改台账）后，**当场**更新：§0 本分支行状态 → [`AGENTS-PROJECT.md`](AGENTS-PROJECT.md) §4 快照 →（涉及状态变更时）`papers/portfolio.md`。
3.1. **收工时写错题本**（用户 2026-10-12 指定，强制）：在 [`AGENTS-LESSONS.md`](AGENTS-LESSONS.md) §4 追加一行（含"本轮无新增"）；若有本轮被证据推翻的判断/返工/被用户纠正/造成副作用，追加到 §2 明细表；同一模式出现 ≥2 次则升级到 §1 并**补一条机器可校验的强制手段**。
4. **不凭记忆**：任何"已完成/已核对/我记得"必须先落到文件或命令输出上。长对话里记忆会与磁盘事实分叉，**磁盘优先**。
5. **不瞎猜**：判断前按 [`AGENTS-NORMS.md`](AGENTS-NORMS.md) §2 的多轮验证协议取证；工具与平台行为查官方文档，文献主张查本库或做一次可核验检索。

### 0.1 进度快照（每轮收工时更新；**必须来自文件或命令输出，不来自记忆**）

> 快照日期：**2026-10-11**（主支复核：GPU 纠错 + A1 负结果 + git 推送）；初版由 SUMO 环境线分支填写。
> 取数方式：读 `papers/portfolio.md` ＋ 按文件 mtime 扫描 ＋ 检查 `results/`、`src/`、`audit/`、`configs/env/`。**不来自记忆。**

| 论文 | 状态（来源：`papers/portfolio.md`） | 前提是否满足 |
|---|---|---|
| P1 OTF-CfC | 蓝图完成，未开工 | **环境前提已清空**：GPU＋torch 2.11.0+cu128（11/11）＋**CARLA 全线打通**（服务端 25 s 就绪、Python 客户端 8/8、**Town04 可用**）＋ **CfC 单元已实现并自检 11/11**；**唯一缺口＝实车数据** |
| P2 SocialDreamer | 蓝图完成，未开工 | 未验证（依赖公开数据访问） |
| P3 TalkOTF | 蓝图完成，未开工 | 未验证（需自建 500–1000 条配对数据） |
| P4 IsoLNN | 蓝图完成，未开工 | 未验证（依赖 P1 控制器） |
| P5 AdjointStack | 蓝图完成，未开工 | 未验证（依赖 P1–P3） |

| 类别 | 已完成 | 未完成 |
|---|---|---|
| 立项与契约 | 资产盘点、仓库骨架、结果 schema、环境锁、**风险登记表 12 条**、审计编号表、**`audit/第一次组会/01-p1-plan.md` 二十四周逐周计划（2026-10-08 交付）** | —（`01-` 已补，编号表齐全） |
| 文献 | 30 条 venue 全量核验（17 处修正，清单已由 `audit/05-` 迁至 `audit/第一次组会/05-citations.md`，**literature 分支已同步其引用路径**）；`literature/**` 文献图＋逐字限定语；**第二次组会精读记录 23 篇 + 2024+ 增量分诊** | P2–P5 的文献图；OpenAlex 引文展开（额度耗尽，**"外部复现"列仍为"未检"**） |
| 组会交付物 | **第一次组会**：汇报 docx（7 页）＋前提准备 PDF；**第二次组会（2026-10-08 新增）**：`组会汇报-第二次-P1文献底座与三条硬约束.docx`（5 页/3933 字/6 表）＋同名 PDF，生成器 `scripts/make_meeting2_docx.py` | 第二次组会正文待补汇报人与日期两处 `【待填】` |
| 环境 | **环境前提已全部清空**：GPU（RTX 5060 8 GB / sm_120）＋ **torch 2.11.0+cu128**（11/11、6.7×）＋ **CARLA 0.9.16 全线打通**（服务端 25 s 就绪；**Python 3.12.10 并装；客户端连通 8/8；Town04 可用**）＋ **SUMO 1.27.1** 四项通过 | **学位论文实车数据**（唯一实质缺口，申请函待发）；**闭环 A1 所需的 `src/ctrl` 训练循环 + CARLA 场景封装**（CfC 单元本身已完成） |
| 工具与数据 | **`src/ctrl/cfc.py`＋自检 `test_cfc_unit.py`（11/11 通过，GPU 单步 0.35 ms/256 样本）**；**`results/p1/` 有 36 份真实算例**（schema 通过、种子独立性 4/4）；**A1 信息量版负结果已出结论**（含三族复算） | 实车数据、TD3 代码/权重、`src/eval` 指标实现、`src/ctrl` 的闭环训练脚本、与论文的严格对拍 |

**待裁决（阻塞）**：① ~~SUMO 定位~~ **已裁决＝路线 B（§2）**；② ~~算力路线~~ **已裁决＝先降级只跑 CPU（§3）**；③ ~~TD3 基线~~ **已裁决＝先写引用值、主表分两栏（§3）**；④ ~~时间基准~~ **已裁决＝按相对周排**；⑤ **仍待确认**：起始日（相对周起算点）与各论文投稿截止；⑥ **仍待确认**：P1 是否补报振荡阻尼比 g_p 与交通流稳定性 f_flow（第二次组会 §3.3）；⑦ ~~P1/P2 是否并行~~ **已裁决（2026-10-13）＝先做完 P1 再开 P2 实验线**，理由与三个月路线见 [`audit/第一次组会/07-task-order-decision.md`](audit/第一次组会/07-task-order-decision.md)；**P2 只允许零算力的维护性动作**（更新新颖性核验），**不得开数据流水线或训练**。
> **★ 由此产生的最高优先级行动项**：**实车数据申请函必须本周发出**——它是 P1 唯一不在我们控制内的前提（唯一实质缺口），越晚发越可能赶不上写作窗口。条款已备好于 [`audit/第一次组会/04-data-request-and-ethics.md`](audit/第一次组会/04-data-request-and-ethics.md)（8 条承诺），**该函至今未寄出**；发出后须在该文件登记日期与回复状态。

**已知未修问题**：
- ~~`papers/portfolio.md` 里程碑注记的 docx 路径缺 `第一次组会/`~~ → **2026-10-08 已修**（留作示范：开工同步时发现的信息差必须当轮修掉）。
- `literature/meeting2/03-链接清单.md` 有 **2 条坏链**指向 `../../scripts/check_links.mjs`（该脚本不存在，正确落点应为 `literature/scripts/`）。**属 literature 分支产物，主支按协作契约第 2 条只报告不擅改**。
- **git 已初始化**（2026-10-11）：`main` 分支（仓库 `auto-driving/`），提交 `ac6956d`（289 文件 / 约 4 MB）与 `7186b44`；工作区干净，提交者身份已**持久写入仓库 local 配置**（未动全局 git 配置）。策略与公开范围见 §7.1。

> **下列常量由 `scripts/smoke/check_progress_snapshot.mjs` 自动校验**（用户 2026-10-08 要求：把"自觉执行"变成"可校验"）。**改快照必须同步改这里**，否则脚本退出码 1。
> **开工时跑一次**：`node scripts/smoke/check_progress_snapshot.mjs`（4 项全过 exit 0；任一不符 exit 1）＋ `node scripts/smoke/check_branch_freshness.mjs`（分支登记是否过期）。两个脚本均已于 2026-10-08 实测：通过态、故意不一致、还原后复测三种情形均符合预期。
> **本协议目前的强制边界（诚实说明）**：脚本只校验 §0.1 的四条可机器判定常量与 §0 表的新鲜度；引用路径是否失效、协议是否被完整执行**仍无自动强制**。
>
> ```text
> snapshot-date: 2026-10-11
> results-json-count: 36
> src-code-file-count: 13
> env:sumo-version: 1.27.1
> portfolio:source: papers/portfolio.md
> portfolio-check: status-column
> ```

**防局部最优检查点（用户 2026-10-08 指定，强制）**

长对话会收敛到局部最优（只打磨手头那条线，忘掉全局）。**每完成一个阶段、或每 60–90 分钟连续工作、或用户说"继续"时**，做一次三问自检并写进回复：

1. **全局问**：本轮工作在五篇论文的哪一条线上？它是否在服务**当前最关键的那件事**（见 §0.1 待裁决与阻塞项）？如果不在，**先停下来说明**，不要顺手做别的。
2. **前提问**：我是否在**前提未满足**的情况下继续往下堆产物（例如没有数据却在写实验章节、没有算力却在排训练计划）？若在堆，改为补前提或明确标注为待验证。
3. **反证问**：本轮结论**最可能错在哪里**？有没有一条与我结论相反的证据被跳过？→ 必须给出至少一条反证或明确写"未找到反证及其检索方式"。

> 三问的答案要短（各 1–2 句），但不能空。"本轮进展顺利"这类无信息量的回答视为未执行。


## 1. 主张上限（硬约束，越界即回退）

- **集群叙事**：OTF 作为"交通社会压力"的一阶可解释标量，在 WLA / VLA / LNN 三条赛道上完成"**升维**（势场化、预测化）与**下沉**（注入 ODE 边界条件）"。
- **P1 红线**：不得预先声称"OTF 势场带来 X% 性能提升"。学位论文报告的分类器准确率增益为 **+1.0 ~ +5.5 个百分点**（SVM +2.23~+3.60／LSTM +2.23~+5.46／Bi-LSTM +1.00~+1.73；**分类器准确率，论文报告值，未经我们复现**），在 LNN 控制范式下**未经本项目实测即属 C/D 级证据**。A1 消融须诚实报告；若不显著，卖点改为"**可解释性 + 零额外传感器成本**"。
- **不得把仿真/回放写成实车验证**：CARLA（Town04）与实车数据回放都是仿真或开环证据。未做真车闭环前，措辞上限是"在 CARLA 与真实数据回放中"。
- **不得把 TD3 基线写成"我们复现"**，除非确实重训；须二选一并注明：① 学位论文实现（原样引用）② 我们复现（附协议与差异清单）。
- **不得直接搬用他人论文数字**：与 DriveDreamer 等对比若未同协议复现，必须标注"文献报告值，协议不同，不可直接比较"。
- **★ 参数量口径（2026-10-02 层 3 精读后新增，直接约束蓝图的"<500 KB"）**：CfC 原文（NMI 2022）的参数量只有**车道保持模型**一组数据——**递归分量 4,184 参数，含 CNN 感知头的全模型 230,828 参数**（fp32 ≈ 902 KiB，**超 500 KB**；fp16 ≈ 451 KiB 才达标）。且该文**未报告任何硬件**，可追溯加速仅 3×–220×（Abstract 的"1–5 个数量级"在全文找不到对应图表），"可上 MCU"只是建议句、**零实验证据**。→ 在拿到本项目自己的实测参数量之前，**P1 不得写"<500 KB"**；若必须写，须写明量化精度与是否含感知头。出处：`literature/notes/p01-cfc-nmi2022.md`；汇总见 `literature/notes/citation-qualifiers.md`。
- **★ 术语口径（同上）**：P1 若把 OTF 势场作为 ODE 边界条件，**不宜自称 "physics-informed"**——已核验的最接近工作（PINC, Neurocomputing 2024, #7）用的是**软损失项**且其基准方程有可判真伪的残差，而 OTF 势场是启发式先验、不存在可判真伪的残差。宜用 structure-informed / prior-informed / boundary-conditioned，并把 OTF 定位为 inductive bias。该文**从未做 λ=0 消融**，故 P1 的 A1 消融（OTF 开/关）相对它是净增量。

## 2. 数据与结果

- **本机数据资产**：`[待确认]` 学位论文实车数据集的位置、格式与规模（毫米波雷达 + GPS、CAN 总线、高速/城市双工况）；CARLA 版本与 Town04 改造地图。
- **★ 本机交通仿真工具（2026-10-08 实测，非计划）**：**Eclipse SUMO 1.27.1 已装于 `D:\SUMO\sumo-1.27.1`**（便携 ZIP 解压，非 MSI；官方 SHA256 核验一致），`SUMO_HOME` 与用户级 `PATH` 已配置，14 个工具齐全；`sumo --version`、`netgenerate` 造网、端到端仿真、**Python TraCI 实连仿真** 四项均已跑通。完整事实与验证记录见 `configs/env/local-cpu.lock.yaml` 的 `sumo:` 段。
  - **★ 定位已裁决（用户 2026-10-08）＝ 路线 B：只做交通流生成 / 合成 OTF 真值**。即：**SUMO 不替换 CARLA、不做联合仿真**，只承担"生成带 OTF 真值的合成高速混行交通流"（风险 R13 备选 B1），供 A1 消融的合成版本使用。
    - **因此下列硬约束一字不改**：§1 的措辞上限仍为"在 CARLA 与真实数据回放中"；SUMO 结果只能表述为"**在 SUMO 合成交通流中**"，**不得**写成 CARLA、不得写成实车；§3 的公平性条款（同一 CARLA 地图版本）照旧；§5 的 sim-to-real 条款照旧。
    - **连带后果（2026-10-11 更新）**：**CARLA 已于同日全线打通**（服务端＋Python 客户端＋Town04 可用，见下"本机算力"段），因此 **R14（CARLA 从零重建）风险关闭**；**闭环实验的环境前提已清空**。
- **★ 本机算力（2026-10-11 实测，纠错）**：**NVIDIA GeForce RTX 5060 Laptop GPU，显存 8151 MiB，驱动 592.15，compute capability 12.0（Blackwell / sm_120）**；CPU i7-14650HX（16 核 24 线程）；内存 15.7 GB。
  - **旧口径作废**：此前多处写的"本机无 GPU"**来自一次问答选项，从未实测核实**——现予撤销，全库已同步纠正。
  - **✅ 已完成（2026-10-11）**：装好 CUDA 版 PyTorch 并**实测通过 11/11**——最终配对 **torch 2.11.0+cu128 ＋ torchvision 0.26.0+cu128**，`cuda.is_available()=True`、`version.cuda=12.8`、**sm_120 一致**、2048² matmul+backward 实测 **6.7× 加速**、fp32/fp16/bf16 均可用。完整安装与验证记录见 [`configs/env/local-gpu.lock.yaml`](configs/env/local-gpu.lock.yaml)；复跑命令 `python scripts/smoke/check_gpu_env.py`。
  - **sm_120 硬约束（给其它分支）**：Blackwell 需 **CUDA 12.8+** 的 PyTorch 构建；**环境锁必须记 `cuXXX` 后缀**，只写"torch 2.x"无法判断本机能否跑。可用索引：`https://download.pytorch.org/whl/cu128`。
  - **✅ CARLA 全线打通（2026-10-11）**：**0.9.16（UE 4.26）装于 `D:\CARLA`，18.07 GB**（原装 `F:\CARLA`，因移动 SSD 在大 I/O 后掉盘而**搬迁到内置 D:**，`robocopy` 校验 31 417 文件 / 18.065 GB 完全一致）；桌面 3 个快捷方式。完整记录见 [`configs/env/local-carla.lock.yaml`](configs/env/local-carla.lock.yaml)，冒烟脚本 `scripts/smoke/check_carla_env.py`。
    - **服务端**：`CarlaUE4.exe -quality-level=Low` → **25 秒**端口就绪（GPU 显存约 3.9 GiB）。
    - **Python 客户端**：官方 wheel 仅 `cp312`。**实测**：3.14 被 pip 拒；改标签进 3.13 报 `No module named 'carla.libcarla'`（ABI 不兼容）；**装 Python 3.12.10 后成功**。
      - **Python 3.12.10 为并装**（`py -3.12`，`C:\Users\...\Programs\Python\Python312`），**只给 CARLA 用**；**主用 3.14 不受影响**（实测 torch 2.11.0+cu128、cuda=True 仍正常）。安装包签名 **Authenticode Valid，签名者 Python Software Foundation**。
      - **注意**：3.12.11–3.12.15 **只有源码包、无 Windows 安装器**（实测逐个 HEAD 均 404）→ 3.12.10 是最新可用版本。
    - **连通冒烟 8/8 通过**：客户端已连接（默认 `Town10HD_Opt`），**可用地图 13 张且 Town04 在**（P1 目标地图 ✓）。
    - ⚠️ **操作提示**：冒烟后 `CarlaUE4-Win64-Shipping` 子进程可能残留（约 1.3 GB 内存），需显式 `Stop-Process` 清理。
    - 注意：本机虽已装 **UE 5.3**（`F:\UE_5.3`），但 CARLA 0.9.16 基于 **UE 4.26**，**不能复用该引擎**。
  - **仍缺**：**实车数据不在本机**（唯一的实质前提缺口）。**闭环 A1 的环境前提已全部清空。**
  - **磁盘布局（2026-10-18 实测，F: 已掉线）**：**C:/D:/E: 为本机固定盘**（CARLA 在 `D:\CARLA`，18.07 GB）；
    **`F:` 移动 SSD 再次掉线**（2026-10-17 复现，盘符与卷均不可见）。
  - **★ 由此定死的两条纪律（2026-10-18）**：
    1. **运行产物一律写仓库内 `runs/p1/`**（`P1_RUNS_DIR` 可覆盖，但默认不再是外部盘）。
       理由：单局结果仅 ~3 KB，放仓库毫无压力；而放在 F: 的直接后果是
       **2026-10-13 的 4 局 A1 结果在盘符消失后不可访问**——数据丢失。
       只有真正的大文件（checkpoint、原始轨迹）才考虑外置，且必须**同时**在仓库留可追溯的摘要。
    2. **不把任何"唯一副本"放在移动盘上**；移动盘只作一次性传输或可重建的备份。
- **公开数据**：nuScenes / Waymo（P2 用）遵守各自许可，**不得再分发**原始数据；**OTF 自动标注流水线是 P2 的隐性关键路径，须在第 2 个月启动**。
- **结果唯一来源**：`results/<paper>/<experiment>_<scenario>_<seedset>.json`（本项目约定）。数字必须可指到文件名与字段；自检、冒烟、调试产物不得进入任何对外文本。

## 3. 评价协议与公平性

- P1 基线：① PID ② MPC（线性化车辆模型）③ 学位论文 TD3 直控 ④ OTF-CfC（本文）。
- **★ TD3 基线的呈现方式已裁决（用户 2026-10-08）＝ 先写"引用值"**：主表**分两栏** —— ① 同协议复现结果（PID / MPC / OTF-CfC）② **文献报告值（学位论文实现，协议不同，不可直接比较）**。**稿件不得出现"我们复现了 TD3"**；`configs/p1/baseline_td3.yaml` 用 `mode: cited`。按论文表 5.1/5.2 的重实现推迟到**有 GPU 与实车数据之后**，届时须附协议与差异清单才可改口径。
- **★ 算力路线已裁决（用户 2026-10-08）＝ 先降级，只跑 CPU 可做的事**：公式/规则复现、SUMO 合成数据与 OTF 采集、统计脚本、契约冻结优先；**CARLA 闭环与任何训练一律后移**，云端算力在"确定要跑 CARLA 闭环"时再申请。
- **公平性**：同等可用信息（不得给本方法额外的特权输入）、同等调参预算与训练轮次、同一 CARLA 地图版本与同一组交通流随机种子。
- P1 指标：跟车误差 RMSE、加速度平方积分（舒适性）、Jerk 峰值、车道居中偏差、前轮转角方差、端到端延迟、MCU 内存占用。资源类指标须记录采集平台与档位（MCU 型号、编译器与优化选项）。

## 4. 统计与报告

- 种子 ≥5，报 mean ± std 或 95% CI；长尾/成功率类小样本用 Wilson 或 Clopper-Pearson 区间，**不得**用正态近似。
- 消融一次只改一个因素，并报告失败设定与放弃的路线。
- 规范引用边界：AD 无单一报告标准；可引用 ISO 26262（功能安全）、ISO 21448（SOTIF）、UL 4600 的**术语与思路**，**不得**声称合规或已认证。数据集按其 Datasheets 思路说明来源、偏差与允许用途。

## 5. 领域必查项（AD，细则见技能 `science-top-journal-writing` 的 `references/discipline-rigor.md` §3）

- **ODD 声明**：本项目 ODD ＝ 高速公路主线、多车道、人工与自动混行。跨 ODD（交叉口、城市道路、环形道路）结论无效——学位论文已自承未覆盖。
- **开环 ≠ 闭环**：回放与 CARLA 结果不得表述为"驾驶能力"；若做闭环，须报告场景数、初始条件分布、失败分类。
- **场景覆盖**：四类工况（前方无车、邻车插入、前车减速、前车驶离）+ 长尾（前车急刹、cut-in 急并入、编队单车退出、激进车流扰动）；**逐场景报告**，不只报总平均。
- **实车测试（若开展）**：安全员、区域许可、里程与暴露量；接管率的分母写清（每公里 / 每次干预机会）。
- **sim-to-real**：CARLA 与真实高速数据的差距须量化或至少定性说明，不得默认可迁移。

## 6. 交付与语言

- 稿件：**英文**（目标 venue 均为英文）；与我讨论、解释、给判断：**中文**。

### 6.1 ★ 首选 venue 已裁决（2026-10-18 二次联网核验后定稿；**取代 2026-10-12 版**）

**裁决：P1 首投 `IEEE Transactions on Intelligent Vehicles`（T-IV）；第一备选 `IEEE T-ITS`；
若"毕业/考核必须在某日期前拿到录用"优先于刊物资历 → 改投 `IEEE Open Journal of ITS`（OJ-ITS）。**

**完整取证、不确定性标注与两种情形的选择标准见 [`audit/第一次组会/08-venue-decision.md`](audit/第一次组会/08-venue-decision.md)。**
**判据是 desk-reject 风险，不是影响因子**：T-ITS 有一条被第三方明确描述为"最常见转投原因"的
硬门槛——"交通系统贡献必须是**承载性**主张，去掉交通语境仍成立就会被转投 TVT/TCST"；
T-IV 的范围原文即"roadway environment, and in particular automated vehicles"，
我们的"高速混行 AV 控制器"**不需要为范围辩护**。因此 T-IV 的接受概率更高，且改投 T-ITS 成本最小
（换摘要前两句 + 换 Fig.1 即可）。

| venue | 联网核验到的事实（2026-10-18 取用） | 判定 |
|---|---|---|
| **T-IV** | CiteScore **19.9**；Control & Optimization **3/198**、Automotive Eng **3/143**、AI 28/570；SCIE；年发文 **382**；ISSN 2379-8858；范围明写"**roadway environment, and in particular automated vehicles**"；第三方估审稿 **3–5 个月** | **★ 首投**。范围逐字对口、无需为"交通贡献承载性"辩护 |
| **T-ITS** | CiteScore **20.5**；Automotive Eng **2/143**、Mechanical Eng 16/740、CS Appl 27/1022；SCIE；WoS **Q1**（Eng. Civil 8/193；EE 25/369；Trans. Sci. 7/80）；年发文 **1656**；Regular 10 页（+6 页 $175/页）、Survey 18 页、Short 6 页；第三方估录用 **15–20%**、审稿 **3–6 个月** | 第一备选。指标略高但**desk 门槛更严**（见下），改投时须重写摘要与 Fig.1 |
| **OJ-ITS** | 同属 ITSS、全开放获取；第三方估录用 **约 30%**、约 **10 周**到发表 | **只在"时间硬约束"情形下选**——资历明显低于前两者 |
| TVT / IoT-J | 第三方定位：适合"方法为主角"的稿件 | 不作首选（我们是 ITS/AV 问题，不是通信/IoT 方法问题） |

**⚠️ 三项必须记住的不确定性（不得写进稿件或投稿信）**：
1. **T-IV 的 WoS 分区未闭合**【需核实】：LetPub 显示 `N/A`，而其 SCIE 收录已确认。
   若所在单位硬性要求"JCR Q1"，**投稿前必须自行在 Clarivate JCR 核实**，否则改用 T-ITS。
2. **两刊 JIF 口径冲突**【需核实】：T-IV 中文页称 14.300、英文页无值；T-ITS 同页先 8.4 后 9.1。
   **稿件正文一律不引 JIF**。
3. **审稿速度与录用率均为第三方估计**【推测】，不得作为承诺写入任何对外材料。

**T-ITS 的 desk 硬规则（必须照做，否则会被转投 TVT/TCST）**——核验来源明确指出：
T-ITS 编辑会检查"**交通系统贡献是否为承载性主张，而不只是应用场景**"；
若把"道路/车辆/交通/基础设施/移动性"语境**去掉之后贡献仍然成立**，稿件会被转投 T-COM / T-WC / TCST / TVT。
此外要求**用已建立的 ITS 基准**做对比（其示例清单含 **CARLA**、NGSIM、PeMS、nuScenes 等）。

**因此本项目 P1 的写作纪律（不可违背）**：
1. **标题/摘要前两句必须落在交通现象上**（高速混行中的跟车与换道压力），**不得**先讲"我们提出一个 CfC/LNN 控制器"。
2. **Figure 1 必须是交通场景示意图**（多车道高速 + 混行流 + OTF 场/跟车几何），**不得**用网络结构图当 Fig.1（网络图放后面）。
3. **OTF 是交通流量**——这是 P1 通过 T-ITS/T-IV 范围审查的**最强论据**（OTF 本身是交通流社会压力的一阶标量，不是神经网络技巧）；写作时必须把这条讲出来。
4. **必须出现 CARLA 基准**（已在核验清单内）；CARLA+SUMO 的协议须**逐项写清版本与场景**，因为对比数据是自建的，需要用协议透明度补足。
5. 若 P1 最终是负结果 → **卖点改为"可解释性 + 零额外传感器成本 + 混行交通的社会压力表征"**，此时 **T-ITS 比 T-IV 更合适**（T-ITS 更接受系统级/可解释性贡献）。**负结果时优先投 T-ITS。**

**待核实（不得直接写进稿件）**：
- 两刊的**最新 JIF**：联网来源口径不一（同一来源内先写 9.1、后写 8.4）⇒ **标 `【需核实：以投稿时 Clarivate JCR 为准】`**，稿件正文**不引 JIF 数字**。
- T-IV 的 **WoS 分区**：取到的页面显示 "N/A"（可能尚未入 JCR 分区或数据缺失）⇒ 若毕业/评奖要求"JCR Q1 期刊"，**须先自行核实 T-IV 的分区状态**，否则改用 T-ITS。**这是本裁决唯一的实质风险点。**
- 检索到的"ITSC 2026 混行交通 invited session"：会议线备选，未核实截稿日期与具体分会要求。

- 五篇论文的台账 `papers/portfolio.md` 是**唯一状态来源**：先改台账，再改稿。
- 审计文件编号（`audit/`）：`00-` 资产盘点、`01-` P1 计划（待补）、`02-` 仓库骨架、`03-` 风险登记表、`04-` 数据申请与伦理、`05-` 引用核验清单。
- 引用锚点（**已于本轮逐条核验，见 `audit/第一次组会/05-citations.md`**）：
  - DriveDreamer —— **已正式发表**：ECCV 2024（Poster）。引用须用正式版：Wang X, Zhu Z, Huang G, Chen X, Zhu J, Lu J. DriveDreamer: Towards Real-world-driven World Models for Autonomous Driving. In: *Computer Vision – ECCV 2024*. Springer, 2024. DOI 10.1007/978-3-031-73195-2_4。**不得再写"arXiv 预印本"**。
  - Drive as You Speak —— **workshop 论文（非主会）**：WACV 2024 Workshops (LLVM-AD), pp. 902–909。引用格式：Cui C, Ma Y, Cao X, Ye W, Wang Z. Drive As You Speak: Enabling Human-Like Interaction With Large Language Models in Autonomous Vehicles. *Proc. IEEE/CVF WACV Workshops*, 2024: 902–909。**写成 WACV 主会即属引用失实**。
  - 黄梦圆. 基于超车频次的自动驾驶车辆行为决策研究. 吉林大学博士学位论文, 2023.
- 引用版本纪律：优先引正式发表版；arXiv 条目必须核对版本号（vN）与是否已被接收；**workshop 论文必须显式标注 workshop**。
- 架构原则（综合文档 §7.1）在写作中不得违背：不训练统一大模型、VLA 阶梯指令 + LNN 自适应积分、LNN 与 Transformer 不用直接 BP 串联、闭环用 MPC+LNN 混合（"大胆决策，小心修正"）。

## 7. 待确认（写死之前先问我）

- 学位论文数据集位置/规模/标注格式；TD3 代码或权重是否可得。
- CARLA：**✅ 已装并全线打通（0.9.16 / UE 4.26 / Python 客户端连通 8/8，Town04 可用），见 §2**。环境侧**无待决项**；P5 的云端 A100/H100 仍需另行决策（8 GiB 显存对 P2/P5 训练是否够用未测）。**唯一实质前提缺口＝学位论文实车数据（申请函待发）。**
- ~~SUMO 定位~~ → **已裁决 2026-10-08＝路线 B（只做交通流生成 / 合成 OTF 真值），见 §2**。
- ~~算力路线~~ → **已裁决 2026-10-08＝先降级只跑 CPU，见 §3**。
- ~~TD3 基线引用还是复现~~ → **已裁决 2026-10-08＝先写引用值、主表分两栏，见 §3**。
- 综合文档 §6.2 的 43 个 MCP 组件属于**待安装清单**：按我的要求**当前不安装任何包**，是否安装由我逐项决定。
- 五篇论文的作者、单位、基金信息；各论文的实际投稿时间（蓝图给的是 0–18 月相对周期）。**时间基准已裁决：按相对周排（W1 = 用户确认后的第一个工作日），不写绝对日期。**

### 7.1 版本管理（2026-10-11 落地）

| 项 | 决定 | 说明 |
|---|---|---|
| 仓库范围 | `auto-driving/` **独立**仓库，`main` 分支 | 工作区根**不**初始化，避免把 DSH 配置与其它项目卷进同一历史 |
| 提交者身份 | `本手 <243991048+xyx-cmd-maker@users.noreply.github.com>`，仅写**仓库 local** 配置 | 用 GitHub 官方 noreply（[文档](https://docs.github.com/en/account-and-profile/reference/email-addresses-reference)：2017-07-18 后注册为 `ID+USERNAME` 形式，**改用户名不丢归属**）；避免在提交历史里公开 QQ 邮箱与校邮 |
| 生效前提（**待用户操作**） | 需在 GitHub 开启 **Settings → Emails → Keep my email addresses private**，并把该 noreply 地址加入账号邮箱列表 | 否则提交虽成功但**不归属账号**。漏开时若尚未推送，用 `git commit --amend --reset-author` 修正 |
| 忽略策略 | 已发表论文 PDF 副本（`sources/*.pdf`、`audit/第二次组会/**/*.pdf`）、用户手工资料库（`自动驾驶_世界模型科研汇总/`）、提取的中间文本（`literature/fulltext/_raw/`、`meeting2/`）、`runs/` 冒烟产物、临时文件 | 合计排除约 **440 MB** 外部资料副本；**磁盘原样保留**，引用一律用「路径 + DOI」，不依赖 git 版本 |
| 版本纪律 | 文件名不写 v2/final/日期；版本由提交表达 | 自此 `results/` 的 `config_hash` 可回指到具体提交 |
| 私人联系信息 | 真实邮箱（QQ、校邮）**不写入受版本控制的文件** | 需要时用未跟踪文件或会话内传递；仓库文件里只出现 noreply |
| 校邮的用途 | 仅用于 GitHub Student Pack 等**学生身份验证**与在学期内的会议注册 | 校邮毕业后失效，**不得**作为论文通讯作者的长期联系方式（投稿前须换成长期邮箱） |

## 8. 资料库（`sources/`）与附件处理

| 文件 | 内容 | 用途 |
|---|---|---|
| `blueprint-papers-v1.1.docx` / `.txt` | 论文规划：五篇详纲、时间线、风险 | 规划唯一依据 |
| `blueprint-overview-v1.1.docx` / `.txt` | 综合文档：架构五层、模块规范、工具链、车规原则 | 架构与规范依据 |
| `references-list.docx` / `.txt` | 核心参考文献清单（30 篇，含 venue 标注与链接，按 P1–P5 分组） | 引用库与 Related Work 起点 |
| `../literature/文献需求-50篇顶刊.md` | **P1（OTF-CfC）50 篇期刊文献图**＋18 条附录（奠基会议/经典），全部 DOI 经 Crossref 逐条核验；附 6 篇层 3 精读结论与风险检查 | P1 候选引用库；**新增于 2026-10-02** |
| `../literature/search-log.md`、`final_list.jsonl`、`refs.bib` | 检索协议七要素、机器可读清单、可编译 BibTeX | 引用核验的可复现证据链 |
| `../literature/library/P1-library.jsonl` | **P1 唯一候选引用库（98 条 = 75 主记录 + 23 旧库独有）**，每条带 `project_refs` 可追溯来源；合表报告见同目录 `merge-report.md` | 取代"两处各自维护"；**任何修正只改本文件** |
| `../literature/notes/citation-qualifiers.md` | 6 篇核心文献的**逐字 `citation_qualifier`**（#1 CfC / #7 PINC / #15 类人跟驰 / #33 Lp 弦稳定 / #43 波消散 / #45 DeeP-LCC）＋各自对 P1 的直接后果 | **层 3 核验基准**；写稿引用这 6 篇时必须逐字带上限定语 |
| `thesis-huang2023.pdf` / `.fulltext.txt` | 黄梦圆博士论文（133 页 / 30 万字符，可 grep） | 基准资产出处：OTF 定义、动态时间窗函数、分层递阶评估、TD3、实车数据集 |
| `drivedreamer-2023.pdf` / `.fulltext.txt` | DriveDreamer 原文（15 页） | P2 直接对标对象 |
| `drive-as-you-speak-2023.pdf` / `.fulltext.txt` | Drive as You Speak 原文（8 页） | P3 方法论对标对象 |

**附件处理规则**：DSH 会话里的附件形如 `C:\Users\本手\.dsh\attachments\...\<hash>\<原名>`，是**会话级只读副本，换会话即失效**。
凡需长期引用的材料，**先复制到本项目 `sources/` 并改 ASCII 文件名**，再在提示词与 AGENTS 中引用固定路径；已在 `sources/` 中的重复附件不重复复制。

**引用核验（硬要求）**：`references-list.txt` 的 venue 标注——尤其是标 📄 的 arXiv 条目与 workshop 级条目——写入稿件前必须逐条核验正式发表状态与版本，核验不了标 `[待核实]`。
**核验状态（本项目已完成一次全量核验）**：30 条已在 `audit/第一次组会/05-citations.md` 逐条核验，发现 **17 处清单错误（含 3 处链接/编号指向另一篇论文）**。**引用库一律以 `sources/references-list-verified.txt` 为准**，原 `references-list.txt` 仅作历史留存。
**P2 定位句（2026-10-13 由联网+文献核验后改写，**不得再用旧措辞**）**：
- ~~"Drive× 家族多为预印本，可用'首个经过同行评议的 OTF 条件世界模型'类措辞定位"~~（DriveDreamer 已是 ECCV 2024 正式论文，该差异不成立）
- **现行措辞（推荐版）**："首个以交通流社会压力场（OTF）作为**显式**结构条件模态的驾驶世界模型——既有驾驶世界模型的结构条件为 HDMap / 3D Box 等**几何布局**条件，交互信息一律以**隐空间或注意力权重**隐式编码。"
- **核验依据**：`literature/p2/P2-novelty-check.md`（253 行，2026-10-13）。三节 18 条**全部完成条件模态判定，0 条**以力场/势场/社会力为世界模型的结构条件模态；定向检索（OpenAlex 8 式 / arXiv 8 式 / S2 / Web）未发现以 OTF 为条件的世界模型。
- **⚠️ 但必须处理三个先例**：① **SPDiff**（AAAI 2024, [10.1609/aaai.v38i1.27802](https://doi.org/10.1609/aaai.v38i1.27802)）——**最危险**：把 Social Force 显式用于**条件扩散去噪引导**，但其"力"是去噪器**内部量/输出**（生成加速度）、面向**行人**，**不是输入型结构条件**；② StreamForce（力作视频生成控制信号，非驾驶）；③ NIFTY（CVPR 2024，交互场引导采样）。**区分点在"场放的位置"，不在"用没用场"。**
- **✅ 脆弱点已消解（2026-10-13 复核 AAAI 正式版）**：正式版摘要写 "we design a crowd interaction **encoder** to guide the denoising process"（arXiv v1 用 module），**措辞变了但条件来源的定义未变**——条件输入仍是 "both the **interactive and historical information of crowds**"，**社会力不是 `c_t` 的成员**，仍是 encoder 输出的内部力向量 `f_ped`。**⇒ 区分成立，P2 无需降级措辞，保留"显式"二字以自证区分。** 残留风险低（正式版 PDF 无法解析，核验基于摘要 + arXiv v1 正文）。
- **✅ 引用网络反向检索已执行（2026-10-13）**：从 DriveDreamer（OpenAlex `W4386876077`）取引用者，**独立于关键词通道**——15 篇引用中，题名含"力场/社会力/势场/交互场"的 **0 篇**、含"interaction/social + 驾驶类"的 **0 篇**。**双通道方向一致**。**限制**：OpenAlex 对该文只记 15 条引用（明显低于实际），**覆盖不完整，"15 条"不是全集**；且只筛题名。原始结果见 `literature/p2/_cite-net.json`。
- **★ 文献图不能作新颖性证据**：`literature/p2/文献需求-50篇顶刊.md` 的 50 条**系统性排除会议论文**（OpenAlex `type:article`），而上述 3 篇先例（AAAI/CVPR/arXiv）**全部落在那 50 条之外**——该图的限制第 1 条已被实测证实。
其余两条建议仍有效：① 优先引正式发表版本（如 DiLu→ICLR 2024、DriveGPT4→RA-L 2024、DriveDreamer→ECCV 2024）；② 五篇论文可共享约 70% 引用库（修正后仍成立，但共享库必须同源，避免同一错误复现五次）。
