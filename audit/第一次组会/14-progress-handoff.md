# 进度交接记录（2026-10-18 12:35，用户要求"先停一下"时落盘）

> **用途**：任何新对话/新会话读这一页就能接上，不依赖对话记忆。
> **权威来源**：本页数字全部来自命令输出（`git rev-parse`、文件 mtime、JSON 字段），不来自记忆。
> **配套**：[`AGENTS-PROJECT.md`](../../AGENTS-PROJECT.md) §4 快照、[`AGENTS-LESSONS.md`](../../AGENTS-LESSONS.md) §4。

> **★ 2026-10-18 15:00 更新：全量 20/20 已完成，结果见 [`15-a1-full-results.md`](15-a1-full-results.md)。**
> 本节以下的"全量实验：已按用户要求停止"是**当时**的状态记录，保留作历史。
---

## 1. 项目六要素（一眼看全）

| 要素 | 当前内容 |
|---|---|
| **目的** | 回答一个问题：把**超车频次（OTF）**作为控制器的第 4 维输入，**在闭环里**是否比不带它更好 |
| **要得到的结果** | ① 一篇投 **IEEE T-IV** 的英文论文（第一作者：用户；通讯作者：黄梦圆）② 可复现代码与结果 JSON ③ highD 真实轨迹上的 OTF 稀疏性与回放验证 |
| **目标期刊** | **T-IV（已定案，JCR Q1）**；备选 T-ITS；时间硬约束时 OJ-ITS。取证见 [`08-venue-decision.md`](08-venue-decision.md) |
| **当前阶段** | **阶段四（消融与撰写）起步**：全量 A1 闭环消融跑到 **13/20 局**（2026-10-18 12:40 按用户要求停止，可续跑）；摘要骨架已写；真实数据层改走 highD（申请中） |
| **阻塞项** | ① highD **许可（EULA）未核实** → 未拿到前不得使用数据；② NGSIM 官方门户对本机 **403**；③ 全量未跑完，claim 不能定 |
| **下一步** | 全量跑完 → 出 `15-a1-full-results.md`（逐场景三态 + claim 选择 + 摘要填数）→ highD 到手后算 OTF 稀疏性曲线 |

---

## 2. 全量实验：**已按用户要求停止（2026-10-18 12:40）**

| 项 | 值 |
|---|---|
| 命令（续跑用同一条） | `py -3.12 src/ctrl/train_cfc.py --scenarios none,cutin,lead-brake,lead-exit --seeds 0,1,2,3,4 --episode-s 60 --traffic 16 --resume` |
| **状态** | **已停止**（用户要求"先停一下"） |
| 已完成 | **13 / 20 局**：none×5、cutin×5、lead-brake×3（s0–s2） |
| **剩余 7 局** | `lead-brake` s3、s4 ＋ `lead-exit` s0–s4 |
| 单局耗时 | 约 **11–12 min** ⇒ 续跑约需 **80–90 min** |
| 停机后核查 | ✓ 无 python 进程 ｜ ✓ 无 CARLA 进程 ｜ ✓ 端口 2000 已释放 ｜ ✓ **无 `.tmp` 残留**（说明没有写一半的文件） |
| 产物 | `runs/p1/cases/case_<scenario>_s<seed>.json`（13 份，各 9–10 KB，含 `exec` 执行指纹） |

**续跑只需一条命令**（`--resume` 会按 `exec` 指纹校验档位一致才跳过，**不会混档位**）：
```powershell
cd "D:\Deepseek Harness\auto-driving"
Start-Process -FilePath 'D:\CARLA\CarlaUE4.exe' -ArgumentList '-quality-level=Low','-windowed','-carla-port=2000' -WorkingDirectory 'D:\CARLA'
# 等端口 2000 就绪（约 25 s）后：
$env:OPENBLAS_NUM_THREADS='1'; $env:OMP_NUM_THREADS='1'
py -3.12 src\ctrl\train_cfc.py --scenarios none,cutin,lead-brake,lead-exit --seeds 0,1,2,3,4 --episode-s 60 --traffic 16 --resume
```

> ⚠️ **续跑前必须先重启 CARLA**（P9 教训：同代码不同结果时第一步是重启被控环境）。
> ⚠️ **CARLA 的相机跟随已默认开启**（`CARLA_FOLLOW=0` 可关），续跑时窗口里能直接看到 ego 在动——这是本轮修的可观测性缺陷。

---

## 3. 已完成并推送的东西（46 次提交，HEAD `4d0f095`）

### 3.1 实验与代码
| 文件 | 状态 |
|---|---|
`src/envs/carla_town04.py` | 闭环环境；含 **脚本化 cut-in 注入**（使 OTF 真激活 8–13%）、**相机跟随默认开启**（`CARLA_FOLLOW=0` 可关） |
`src/ctrl/train_cfc.py` | 执行器；含 `exec` 指纹、`phi_nonzero_ratio` 强制落盘、`--analyze`（精确符号翻转 + TOST + Holm + 三态结论） |
`src/otf/otf_core.py` | OTF 的**唯一**实现（`_crossed`：车辆跨越 ego 车道才计数） |
`src/eval/metrics.py` | 指标；无数据返回 `None` 而非 0 |
`configs/p1/a1_execution_freeze.yaml` | **预注册冻结**（主口径 `Δcost(best)`、TOST margin 10%、Holm、三态） |

### 3.2 审计与决策文档（`audit/第一次组会/`）
| 文件 | 内容 |
|---|---|
`08-venue-decision.md` | T-IV vs T-ITS 取证；**T-IV 已定案（Q1，用户确认）** |
`09-a1-medium-validation.md` | n=4 管线验证（**不作结论**），暴露"候选池不等"与"Phi=0"两个问题 |
`10-a1-protocol-freeze.md` | 5 件事的**预注册**与理由（含为什么主口径选 best 而非等 K） |
`11-claim-data-abstract-alignment.md` | **主张 vs 数据 vs 方法描述**的对齐审计（4 处"写法与实现不符"清单） |
`12-authorship-and-contribution.md` | 署名（用户第一 / 黄梦圆通讯）、**CRediT 全部由第一作者主导**、OTF 术语归黄梦圆、数据使用 5 条 |
`13-public-dataset-strategy.md` | highD 主 / NGSIM 备 / exiD 补充；**§8 已用原文核实规模**并推出 **OTF 稀疏性**；NGSIM 403 实测 |
本文件 | 进度交接

### 3.3 写作
`papers/p1/00-title-abstract-fig1.md` | 3 个标题候选（推荐 A）、**两版摘要骨架**（正向/中性）、**Fig.1 三分面规格**、合规自查（em-dash 0、禁用词 0、over-claim 0）、**12 个占位符的填数来源**、§2.1b **稀疏性陈述**

### 3.4 规则文件族（6 份，效力相同，校验 14/14 通过）
`AGENTS.md`（300 行）/ `AGENTS-PROJECT.md` / `AGENTS-NORMS.md` / `AGENTS-LESSONS.md` / `AGENTS-VENUE.md` / `AGENTS-WORKFLOW.md`
其中 `AGENTS.md §0.0.1` 是**数据前提覆盖块**：实车数据不可得 → 公开数据集；全文不得写 real-world validation。

---

## 4. 关键决策（已冻结，新对话不得推翻）

1. **venue = T-IV**（JCR Q1，用户 2026-10-18 确认；距毕业两年 → 不走 OJ-ITS）。
2. **主指标 = `Δcost(best)`**；等 K 只作敏感性分析（理由见 `10-` §2）。
3. **无效候选**（ego 位移 <20 m）保留在 12 候选中、标记失败、不补跑不删。
4. **统计**：精确符号翻转 + 95% CI + **TOST(10%)** + Holm + **三态结论**（有意义差异/实际等价/未定）。
5. **实车数据不可得** → highD（主）/ NGSIM（备）/ exiD（补充）；**回放不是实车闭环**，证据等级仍 **C**。
6. **ODD 改称**"高速多车道**人工**混行"（highD 无自动驾驶车，未覆盖人机混行）。
7. **署名**：用户第一作者、黄梦圆通讯；**CRediT 全部用户主导**；**OTF 术语归黄梦圆**（首现须引 Huang 2023）。

---

## 5. 下一步的确切命令（复制即可）

```powershell
cd "D:\Deepseek Harness\auto-driving"

# 1) 确认 20 局齐了
(Get-ChildItem runs\p1\cases\case_*.json).Count    # 应为 20

# 2) 出统计（按冻结协议：逐场景三态 + Holm + 等K敏感性 + Phi 激活率 + 无效比例）
$env:OPENBLAS_NUM_THREADS='1'; $env:OMP_NUM_THREADS='1'
py -3.12 src\ctrl\train_cfc.py --analyze --scenarios none,cutin,lead-brake,lead-exit --seeds 0,1,2,3,4

# 3) 三条自检
node scripts\smoke\check_agents_family.mjs
node scripts\smoke\check_progress_snapshot.mjs
node scripts\smoke\check_branch_freshness.mjs
```

然后按冻结的**结局矩阵**（`configs/p1/a1_execution_freeze.yaml` 的 `outcome_matrix`）选 claim，
写 `audit/第一次组会/15-a1-full-results.md`，并把 `papers/p1/00-title-abstract-fig1.md` 的占位符填成真实数字。

---

## 6. 未完成的 4 件事（按优先级）

| # | 事项 | 谁 | 为什么排这个位置 |
|---|---|---|---|
| 1 | **出全量统计 + 选 claim** | 我 | 决定论文类型（正向 vs 边界条件），其他写作都依赖它 |
| 2 | **highD EULA 核实 → 算 OTF 稀疏性曲线** | 用户（EULA）/ 我（脚本） | 稀疏性决定论证方式；且不需要训练，成本低 |
| 3 | **决定 NGSIM 弃或取** | 用户 | 403 未解；**宁可放弃也不要用来源不明的数据** |
| 4 | 摘要填数 + Fig.1 绘制（调 `scientific-visualization`） | 我 | 依赖 1 |

---

## 7. 已知风险（诚实清单）

1. **全量结果可能仍是"未定"**（n=20，单地图、单车型）。届时按预注册只能写"未检出差异"，不能写"无差异"（需 TOST 通过）。
2. **OTF 稀疏性**意味着效应量本就小；若结果全为"未定"，论文必须转成"边界条件 + 可解释性"叙事——**这已在预注册的结局矩阵里**，不属于事后改口。
3. **highD 许可**若限制商业使用或禁止再分发，需相应调整（只发表统计量、不发布原始轨迹）。
4. **控制频率只有 20 Hz**（协议原写 100 Hz），必须在方法里如实写。
5. **脚本化 cut-in 是人为构造**，不是自然换道；稿件不得称 natural lane changes。
