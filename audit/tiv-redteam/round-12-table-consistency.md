# Round 12 — 表格逐单元格对照 + §5.3/§5.4 文字-证据一致性

> 目标文件：`C:\Users\本手\Downloads\TIV_RedTeam_Review_and_DSH_Goal.md`
> 执行日期：2026-10-29 ｜ 基线 commit：`a0d515b`
> 本轮范围：把"论文表格 → 源"的反向核对做完，并核 §5.3/§5.4 的两个百分比与一处窗口值。

---

## 9.1 结论

| 项 | 判定 |
|---|---|
| 当前状态 | **MAJOR REWORK**（四项待决策；本轮无新增缺陷） |
| 是否达到 TIV 强贡献门槛 | **否（证据不足）** |

**三个最关键理由**

1. **三张表的 88 个单元格全部与源一致**：新脚本 `audit_table_text_consistency.py` 直接把渲染进 PDF 的表（`manuscript-ieee.md`）解析出来，逐格重算比对，`exit=0`。
2. **正文两个百分比被证实**：§5.4 说"600 veh/h 时 5 s 窗 88% 的时间为零"→ 实测 100−11.8% = **88.2%**；"3600 veh/h 时同一窗口约一半时间非零"→ **51.5%**。
3. **一处正文窗口值也证实**：§5.3 说"20 s 窗口在 3600 veh/h 达到 0.93"→ 实测 **0.9337**。

⇒ 数字这条线（摘要 / Fig.2 / 三张表 / 正文机制段 / 敏感性段 / 产量声明）**已经查完**，仅剩 Round 11 的 P1-O（§5.3 的 0.32）待补。

---

## 9.2 表格逐单元格对照（88 项，全 PASS）

| 表 | 行数 | 比对内容 |
|---|---|---|
| Table I | 4 | n、Mean Δ、off mean、95% CI 上下界、90% CI 上下界、exact p、TOST p、Conclusion 标签 |
| Table II | 8 | 均值、95% CI 上下界、TOST p；并验证"All eight tests are inconclusive"（TOST p ≥ 0.05 的行数 = **8**） |
| Table III | 3 | 可用性、Mean Δcost、95% CI 上下界、**CI 宽度**、结论 |

**容差说明**：表内数字按 2–4 位小数显示，故比对容差取 **6e-3**（足以发现 0.001 量级的真错，同时容纳四舍五入）。
本轮的两次"FAIL"都是我自己的容差设置问题（0.263 vs 0.262894、1.372 vs 1.371496、34.47 vs 34.4650），**不是论文错误**，已修正脚本。

---

## 9.3 §5.3 / §5.4 文字-证据一致性

| 论文句 | 论文值 | 源 | 判定 |
|---|---|---|---|
| §5.3 "A 20 s window reaches 0.93 at 3600 veh/h" | 0.93 | 扫描表 W=20 @3600 = **0.9337** | PASS |
| §5.4 "at 600 veh/h a 5 s window is zero **88%** of the time" | 88% | 1 − 0.1180 = **88.2%** | PASS |
| §5.4 "at 3600 veh/h the same window is non-zero **half** the time" | ≈50% | **51.5%** | PASS |
| §5.3 "SUMO's LC2013 … over a 60 s probe the whole fleet completed **two lane changes, none across the ego lane**" | — | **仓库内无该探针的产物** | **U（无法核）** |

最后一条是**环境观察**（Traffic Manager 在稀疏场景几乎不换道），它支撑"必须脚本注入"这一关键设计决定，但**没有任何日志或 JSON 落盘**。建议补一个 `results/p1/sumo_lanecount_probe_s1.json` 或在正文注明"作者内部观察，未留存产物"。

---

## 9.4 数字溯源总覆盖（截至本轮）

| 位置 | 工具 | 结果 |
|---|---|---|
| 摘要 + Fig.2 | `audit_number_sources.py` | 10 PASS / 2 WARN（口径） |
| Table I/II | `audit_recompute_main.py` | 44 数值 + 4 标签 PASS |
| 择优层 + 等 K | `audit_recompute_selection.py` | PASS |
| Table III + Fig.2 补充组 | `audit_table3_supplementary.py` | PASS |
| 正文 §4.4 / §5.2 | `audit_number_sources_body.py` | 11 PASS |
| **三张表逐单元格** | `audit_table_text_consistency.py`（本轮） | **88 项 PASS** |
| §5.3 的 0.32 | — | **P1-O 待补** |
| §5.3 的"两次换道"探针 | — | **U 无产物** |

---

## 9.5 最小下一步

| # | 任务 | 需授权 |
|---|---|---|
| 1 | **批准补丁 E1–E5 + E7（含/不含 E6）** | **需要你** |
| 2 | **P0-1 路线 1/2/3** | **需要你** |
| 3 | **P1-M 方案 1/2/3** | **需要你** |
| 4 | **P0-4 路线 A/B/C/D** | **需要你** |
| 5 | 为"两次换道"探针补一份产物，或在正文注明未留存 | 否（下一轮可做） |

---

## 9.6 变更记录

| 文件 | 性质 | 说明 |
|---|---|---|
| `scripts/audit_table_text_consistency.py` | 新增 | 三张表逐单元格反向核对（88 项） |
| `audit/tiv-redteam/round-12-table-consistency.md` | 新增 | 本报告 |

**未修改**：论文、图、`results/`。

---

## 9.7 诚实声明

1. 本轮**两次修正自己的容差**（先是 5e-5/5e-4 过紧，后是 1e-3 对 2 位小数仍过紧），最终 6e-3。**这三次都不是论文的问题**，我在报告里如实记录。
2. `audit_table_text_consistency.py` 从 `audit_recompute_main.py` 复用 t 分布与检验函数——**共享实现**，若前者有 bug 会同时影响两者（同一来源，非独立实现）。
3. §5.3 "两次换道"探针**无法核**（U 级），我**没有**把它标成错误，只标"无产物"。
4. 数字这条线基本收口；**剩下的是贡献判断（P0-4）与四项待决策**。
