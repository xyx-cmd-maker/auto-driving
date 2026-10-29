# Round 10 — 事实纠错（P1-N）+ 一键补丁集（待批准）

> 目标文件：`C:\Users\本手\Downloads\TIV_RedTeam_Review_and_DSH_Goal.md`
> 执行日期：2026-10-29 ｜ 基线 commit：`5338936`
> 本轮范围：把前九轮攒下的文字/口径问题做成**可一键应用的补丁**（默认 dry-run，未改稿）。

---

## 9.1 结论

| 项 | 判定 |
|---|---|
| 当前状态 | **MAJOR REWORK**（四项待决策；本轮新增 1 处事实错误） |
| 是否达到 T-IV 强贡献门槛 | **否（证据不足）** |

**三个最关键理由**

1. **新增事实错误 P1-N**：§4.1 写"0.084 **in sixteen runs** and 0.167 **in four**"，而**预注册 20 局的实际分布是 17 局 0.084 / 3 局 0.168**（逐局可数）。这是**可被审稿人逐局核对**的错误。
2. **P0-1 的不一致从四处升到五处**：§4.1 说 "control cycles"（帧），§5.2 说 "windows"（窗口）——同一个 `phi_nonzero_ratio` 被两个不同单位描述。
3. **补丁已就绪**：`scripts/apply_pending_edits.py` 把 6 处编辑写成 old→new 对，**dry-run 全部锚点唯一（6/6）**，一条命令即可应用；本轮**未应用**，等你批准。

---

## 9.2 新证据：P1-N 局数错误

| 项 | 论文 §4.1 | 数据 |
|---|---|---|
| Φ = 0.084 的局数 | **十六** | **十七** |
| Φ = 0.168 的局数 | **四** | **三** |
| 合计 | 20 | 20 |

逐局明细（预注册 20 局，`results/p1/cases/main`，seeds 0–4）：

| 场景 | Φ 值 |
|---|---|
| none（5 局） | 全 0.084 |
| cutin（5 局） | 全 0.084 |
| lead-brake（5 局） | 全 0.084 |
| lead-exit（5 局） | 0.084 ×2、0.167 ×2、0.168 ×1 |

⇒ 0.084 × **17**，非 0.084 × **3**。论文的 16/4 无法由任何分组方式复现。

**为什么重要**：这是**"论文与自身数据不符"**的实例，属 §2.2 的 E 级反证；审稿人若拿附录逐局数，会直接质疑数据核对流程。

---

## 9.3 P0-1 现状：五处不一致（截至本轮）

| # | 不一致 | 位置 | 证据 |
|---|---|---|---|
| a | 文字"进入 +1/离开 −1" ≠ 实现（驶出返回 0） | 方法节 vs `otf_core._crossed` | 探针用例 B/C/D |
| b | 三来源三种估计量 | Fig.2 | 三段代码 |
| c | CARLA Φ 未持久化 | 逐局 JSON | 字段清单 |
| d | `crossed` 两份实现 | `otf_core.py` / `otf_sparsity_sumo.py` | 逐行比对 |
| **e** | **同一统计量被写成"control cycles"（§4.1）与"windows"（§5.2）** | 两节 | 文本对照 |

---

## 9.4 待批准补丁集（dry-run 已通过）

```powershell
# 只看能不能改（默认 dry-run，不写盘）
py -3.12 scripts/apply_pending_edits.py

# 真改（自动重拼装 + 重转换 + 重生成 tex；PDF 需再跑 pdflatex ×2）
py -3.12 scripts/apply_pending_edits.py --apply

# 连带把"无 Δv 组 OTF 仍无效"写进 §5.2
py -3.12 scripts/apply_pending_edits.py --apply --with-dv-result
```

| id | 改哪里 | 改什么 | 属哪条 |
|---|---|---|---|
| **E1** | 摘要 | "reaches only 0.084" → **"only 0.084 to 0.168"**（+2 词，仍在 250 内） | P1-M |
| **E2** | Fig.2 图注 | 追加："Each source uses its own statistic… descriptive rather than like-for-like." | P1-M |
| **E3** | §4.1 | **16/4 → 17/3**，并定义"control cycle = 20 Hz 观测步" | **P1-N** + P0-1e |
| **E4** | §5.2 | "fraction of windows with OTF > 0" → **"fraction of control cycles with a non-zero net crossing"** | P0-1e |
| **E5** | §5.3 | TGSIM 的 0.53 补上 "averaged over ten runs" | P1-M |
| **E6**（可选） | §5.2 | 追加无 Δv 结果：**+1.26，95% CI [−2.17, +4.68]，exact p = 0.375** | Round 09 新分析 |

**dry-run 结果**：6/6 锚点**唯一命中**，`exit=0`（含 E6）。应用后我会自动重跑 `assemble → to_ieee_citations → to_latex`，再由我执行 pdflatex 与合规检查。

---

## 9.5 最小下一步

| # | 任务 | 需授权 |
|---|---|---|
| 1 | **批准应用补丁**（是否含 E6） | **需要你** |
| 2 | **P0-1 路线 1/2/3**（Round 09） | **需要你** |
| 3 | **P1-M 方案 1/2/3**（Round 08） | **需要你** |
| 4 | **P0-4 路线 A/B/C/D**（Round 09） | **需要你** |

> 说明：E1–E5 与 P0-1 路线 2、P1-M 方案 2 是**同一套**动作。你若选"路线 2 + 方案 2"，**就等于批准 E1–E5**。

---

## 9.6 变更记录

| 文件 | 性质 | 说明 |
|---|---|---|
| `scripts/apply_pending_edits.py` | 新增 | 6 处待批准编辑；默认 dry-run |
| `audit/tiv-redteam/round-10-pending-edits.md` | 新增 | 本报告 |

**未修改**：论文任何源文件、图、`results/`。

---

## 9.7 诚实声明

1. 本轮**没有应用**任何编辑；稿件仍是 Round 06 的状态（8 页、8 条参考文献）。
2. P1-N 的"17/3"由逐局数据数出（E 级）；**我未追查论文的 16/4 从何而来**（可能是早期 n 或手工计数），属未验证推断。
3. E1 把摘要改成范围后，摘要词数会从 245 增至 **247**，仍在 250 内；应用后我会重新跑合规检查确认。
4. E3 修正了一个**事实数字**，属"根据审计发现修正错误"（§6 允许），不是改结论。
5. E6 的分析是 n=5、单场景，**不能外推**；写入正文时我保留 p 值与区间，不写"证明无效"。
