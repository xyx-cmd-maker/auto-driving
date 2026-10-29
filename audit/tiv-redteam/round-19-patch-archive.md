# Round 19 — 补丁的 before/after 存档（并再抓一个文字重复）

> 目标文件：`C:\Users\本手\Downloads\TIV_RedTeam_Review_and_DSH_Goal.md`
> 执行日期：2026-10-29 ｜ 基线 commit：`4ca64c5`
> 本轮范围：把两套补丁的实际改动导成 diff 存档，供作者**批准前逐行审查**。

---

## 9.1 结论

| 项 | 判定 |
|---|---|
| 当前状态 | **MAJOR REWORK**（决策未到；补丁已存档且修好一处瑕疵） |
| 是否达到 T-IV 强贡献门槛 | **否（证据不足）** |

**三个最关键理由**

1. **改动已可逐行审查**：三份 diff 存档在 `audit/tiv-redteam/patch-diffs/`——`pending.patch`（6.2 KB）、`retarget.patch`（4.9 KB）、`combined.patch`（10.1 KB，两者叠加后的总改动）。
2. **diff 目视又抓到一个瑕疵**：E6 的锚点只截到 "…two ranges overlap"，而原文下一行是 "almost exactly."，替换后会**重复一次该短语**。已把锚点延伸到 "almost exactly."，重新生成 combined.patch 并复验。
3. **修后仍 8 页、checker exit=0**，且 §5.2 段落读通无重复。

---

## 9.2 存档清单

| 文件 | 大小 | 内容 |
|---|---|---|
| `patch-diffs/pending.patch` | 6.2 KB | 仅 E1–E7（修错：口径、局数、0.32、帧/窗口） |
| `patch-diffs/retarget.patch` | 4.9 KB | 仅 R1/R1b/R2/R3（改投 T-ITS 的重定位） |
| `patch-diffs/combined.patch` | 10.1 KB | 两者叠加（= 若选"改投 T-ITS"时的全部改动） |

**总改动规模（combined，按文件计）**：

| 文件 | 变更行 |
|---|---|
| `papers/p1/01-abstract-final.md` | 12 |
| `papers/p1/02-introduction-discussion.md` | 25 |
| `papers/p1/_results-fragment.md` | 5 |
| `papers/p1/05-figures.md` | 2 |
| `scripts/to_latex.py` | 2 |
| **合计** | **46 行**（diff 全文 142 行含上下文） |

---

## 9.3 本轮修的那处重复（记录在案）

| 项 | 内容 |
|---|---|
| 现象 | 应用 E6 后，§5.2 出现 "…the two ranges overlap **almost exactly.** Removing the input… p of 0.375. **almost exactly.** The recurrent state…" |
| 根因 | E6 的 `old` 只截到 "overlap"，没有包含原文下一行的 "almost exactly." |
| 修法 | `old` 延伸为 "…overlap\n almost exactly."；`new` 保留一次该短语 |
| 验证 | 修后沙盒：8 页、checker exit=0、"almost exactly. almost" **不存在**、§5.2 段落连贯 |

**这说明**：沙盒编译 + 合规检查**不能**替代**逐行 diff 目视**——重复短语既不影响编译，也不触发任何规则。

---

## 9.4 当前三条路径的状态（全部已存档、已验证）

| 路径 | 应用命令 | diff | 沙盒验证 |
|---|---|---|---|
| 只修错（保留 T-IV） | `apply_pending_edits.py --apply --with-dv-result` | `pending.patch` | ✅ 8 页 / checker 0 |
| 改投 T-ITS | 上面 + `apply_retarget.py --apply` | `combined.patch` | ✅ 8 页 / checker 0 |
| 改投 OJ-ITS | 仅 cover letter + 一句定位 | 无补丁 | — |
| 补实验（Route A） | `routeA-prereg-draft.md` + 14 局 | — | ⏳ 需算力批准 |

---

## 9.5 最小下一步

| # | 任务 | 需授权 |
|---|---|---|
| 1 | **读 `combined.patch`（10 KB，10 分钟）后批准** | **需要你** |
| 2 | 选 T-ITS / OJ-ITS / Route A | **需要你** |
| 3 | P0-1（OTF 定义）与 P1-M（Fig.2 口径） | **需要你** |
| 4 | CARLA 换道探针（关闭 Round 13 的 U） | **需要你** |

---

## 9.6 变更记录

| 文件 | 性质 | 说明 |
|---|---|---|
| `scripts/apply_pending_edits.py` | 改 | E6 锚点延伸到 "almost exactly."，避免重复 |
| `audit/tiv-redteam/patch-diffs/pending.patch` | 新增 | E1–E7 的 diff |
| `audit/tiv-redteam/patch-diffs/retarget.patch` | 新增 | R1–R3 的 diff |
| `audit/tiv-redteam/patch-diffs/combined.patch` | 新增/更新 | 两者叠加（修重复后重生成） |
| `audit/tiv-redteam/round-19-patch-archive.md` | 新增 | 本报告 |

**未修改**：真实稿件、图、`results/`。两个沙盒均已删除。

---

## 9.7 诚实声明

1. diff 是在**临时 git 仓库**里生成的（`git init` → baseline → 应用 → `git diff`），不是真实仓库的历史。
2. `pending.patch` 与 `retarget.patch` 是**分别**生成的；`combined.patch` 是两者在同一沙盒里**先后**应用后的总 diff。若你只应用其中一套，请以对应文件为准。
3. 生成的 `manuscript-*.md/tex/pdf` **未纳入 diff**（它们是产物，可由补丁重生成）。
4. 本轮**没有**应用任何改动到真实稿件；稿件仍是 8 页、8 条参考文献。
5. `combined.patch` 的 46 行改动里，**没有一行**触及数字、表格、图、统计方法。
