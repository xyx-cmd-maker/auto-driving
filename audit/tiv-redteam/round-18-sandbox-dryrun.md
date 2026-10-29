# Round 18 — 沙盒试跑两套补丁：**可安全批准**（并修好了一个漏改）

> 目标文件：`C:\Users\本手\Downloads\TIV_RedTeam_Review_and_DSH_Goal.md`
> 执行日期：2026-10-29 ｜ 基线 commit：`81e2478`
> 本轮范围：在不碰真实稿件的前提下，把两套补丁（Round 10 的 E1–E7 与 Round 17 的 R1–R3）**一起应用并完整构建**。

---

## 9.1 结论

| 项 | 判定 |
|---|---|
| 当前状态 | **MAJOR REWORK**（决策未到；但补丁已证明可用） |
| 是否达到 T-IV 强贡献门槛 | **否（证据不足）** |

**三个最关键理由**

1. **沙盒全流程通过**：两套补丁同时应用 → 重拼装 → 重转换 → pdflatex ×2 → **8 页、0 错误** → 合规检查 **exit=0**。
2. **发现并修好一个"漏改"**：R1 原本只改 `01-abstract-final.md` 的标题，**LaTeX 标题是 `to_latex.py` 里硬编码的**，所以 PDF 仍会是旧标题。已加 **R1b** 同步修改，并在沙盒里验证 PDF 标题确实变了。
3. **所有 9 处改动在沙盒里逐条确认存在**（见 §9.3），摘要 **233 词**（≤250）、**无缩写 OTF**、关键数字保留。

---

## 9.2 沙盒配置与结果

| 项 | 值 |
|---|---|
| 沙盒 | `%TEMP%\p1_sandbox_r18b`（已清理） |
| 复制内容 | `scripts/`、`papers/`、`configs/`、`_check_manuscript.mjs` |
| 应用顺序 | `apply_pending_edits.py --apply --with-dv-result` → `apply_retarget.py --apply` |
| 两次应用 | 均 `exit=0`，锚点各命中 1 次 |
| pdflatex | **8 页，0 错误** |
| `_check_manuscript.mjs` | **exit=0**（0 em-dash / 0 禁用词 / 0 overclaim / 最长句 35 词） |
| 参考文献 | 8 条（补引的 Sensors 与 JAT 仍在 [1][2]） |

---

## 9.3 九处改动的逐条确认（沙盒内实测）

| 补丁 | 检查项 | 结果 |
|---|---|---|
| E1 | 摘要含 "0.084 to 0.168" | ✅ |
| E3 | 正文含 "seventeen runs"（原写 sixteen） | ✅ |
| E4 | 含 "control cycles with a non-zero net" | ✅ |
| E5 | 含 "averaged over ten runs" | ✅ |
| E6 | 含无 Δv 结果（+1.26 / p=0.375） | ✅ |
| E7 | 含 "about 1400 vehicles per hour" | ✅ |
| R1 / R1b | PDF 的 `\title{}` 已换成新标题 | ✅ |
| R2 | 摘要开头为 "A scalar summary of the traffic around a vehicle…" | ✅ |
| R3 | 含 "ordered from measurement to inference" | ✅ |
| — | 摘要 233 词、无 "OTF" | ✅ |

---

## 9.4 本轮修的那个漏改（记录在案）

| 环节 | 现象 | 根因 | 修法 |
|---|---|---|---|
| R1 | 改完 markdown，PDF 标题不变 | `to_latex.py` 里 `\title{...}` 是**硬编码**，不读 markdown 的 Title 段 | 新增 **R1b**：同时改 `scripts/to_latex.py` 的 title 行 |

**教训**：凡是"改标题/改作者/改摘要"这类**元信息**，都要同时检查 `to_latex.py` 里的硬编码模板——它是第二个真相来源。
已在 `apply_retarget.py` 的注释里写明：`PDF 标题来自 to_latex.py 的硬编码 \title{}；只改 markdown 不会改 PDF`。

---

## 9.5 现在的状态：三条路径都已验证可行

| 路径 | 命令 | 验证状态 |
|---|---|---|
| **只修错、保留 T-IV** | `py -3.12 scripts/apply_pending_edits.py --apply --with-dv-result` | ✅ 沙盒 8 页 / checker 0 |
| **改投 T-ITS** | 上面 + `py -3.12 scripts/apply_retarget.py --apply` | ✅ 沙盒 8 页 / checker 0 / 标题已换 |
| **改投 OJ-ITS** | 只改 cover letter + 一句定位（无需补丁） | — |
| **补实验（Route A）** | `routeA-prereg-draft.md` + 14 局 | ⏳ 需你批准算力 |

---

## 9.6 最小下一步

| # | 任务 | 需授权 |
|---|---|---|
| 1 | **批准 E1–E7**（修错，与选刊无关，**建议无条件执行**） | **需要你** |
| 2 | 选 T-ITS（追加 R1–R3）/ OJ-ITS / 先做 Route A | **需要你** |
| 3 | P0-1 与 P1-M 的口径决策 | **需要你** |
| 4 | CARLA 换道探针（关闭 Round 13 的 U） | **需要你** |

---

## 9.7 变更记录

| 文件 | 性质 | 说明 |
|---|---|---|
| `scripts/apply_retarget.py` | 改 | 新增 R1b（同步 LaTeX 标题）；支持 `base="scripts"` |
| `audit/tiv-redteam/round-18-sandbox-dryrun.md` | 新增 | 本报告 |

**未修改**：真实稿件、图、`results/`。沙盒已删除。

---

## 9.8 诚实声明

1. 沙盒只复制了 `scripts/`、`papers/`、`configs/`，**没有** `results/`、`runs/`；因此沙盒内**跑不了**数字审计脚本，本轮只验证"构建 + 合规"。
2. 沙盒 `pdflatex` 用的是同一台机器的 MiKTeX，**不排除**换环境后字体/宏包差异。
3. R1b 修的是**我上一轮补丁自身的缺陷**，不是论文的问题。
4. 本轮**没有**应用任何改动到真实仓库的稿件；真实稿件仍是 8 页、8 条参考文献的 Round 06 状态。
