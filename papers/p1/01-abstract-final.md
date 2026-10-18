# P1 标题与摘要（定稿草案，2026-10-18，数字来自 20 局全量）

> 数字来源：`audit/第一次组会/15-a1-full-results.md` 与 `15-a1-full-results.data.md`（20 局）。
> 语言纪律：`science-top-journal-writing`（强度匹配）+ `academic-humanizer`（去 AI 味、不改数字）。
> **本文件在投稿前不得再改数字**；若重跑实验，须同步更新并在此注明日期。

---

## Title

**Overtaking Pressure on Multi-Lane Highways as a Control Input for Continuous-Time Car-Following**

*Assumption to check:* if the final framing shifts to "when is a traffic-flow scalar usable", the
alternative title is **"When Does Overtaking Frequency Help? A Closed-Loop Equivalence Study of a
Traffic-Flow Scalar in Highway Car-Following"**. Choose after the discussion section is written.

---

## Abstract (~205 words)

Multi-lane highways produce a continuous stream of lane changes around any given vehicle, and drivers
routinely trade longitudinal gap for lateral opportunity. Whether this aggregate pressure carries
usable information for a low-level controller remains unclear: prior work reports gains from
overtaking-frequency (OTF) features in classification settings, but has not tested them inside a
closed control loop. We therefore treat the OTF scalar as a fourth input to a closed-form
continuous-time controller, adopting the definition of Huang (2023). We ablate it against an otherwise
identical controller that sees only gap, relative speed, and ego speed. Both arms share the same search
budget, the same seeds, and the same traffic stream. Across four highway scenarios in CARLA with five seeds
each, the composite driving cost changed by +0.26 (95% CI [−2.32, +2.83]) without a lead vehicle and
by −0.05 ([−1.97, +1.87]) in the lead-exit scenario. Both lie inside a pre-registered ±10% equivalence
margin (TOST p = 0.020 and 0.006). The other two scenarios were inconclusive. Following RMSE and the
acceleration-squared integral showed no detectable difference, and neither arm collided. With five
seeds the exact paired test cannot reach significance after multiplicity correction, so we target
equivalence rather than superiority. A traffic-pressure scalar thus buys interpretability at no
additional sensing cost, not closed-loop performance.

---

## Keywords

overtaking frequency; traffic-flow scalar; continuous-time neural control; closed-loop ablation;
equivalence testing; highway mixed traffic

---

## 主张 → 证据 映射（每句都能指到字段）

| 摘要中的句子 | 证据位置 | 等级 |
|---|---|---|
| "prior work reports gains … in classification settings" | 黄梦圆 2023（分类器准确率 +1.0~+5.5 个百分点，**文献报告值，未复现**） | C（引用） |
| "adopted as defined by Huang (2023)" | `sources/thesis-huang2023.pdf`；代码 `src/otf/otf_core.py` | — |
| "across four scenarios … five seeds each" | 20 份 `runs/p1/cases/case_*.json`，指纹一致 | — |
| "+0.26 (95% CI [−2.32, +2.83])" | `--analyze` 的 `delta_cost` / none 行 | C |
| "−0.05 ([−1.97, +1.87])" | 同上，lead-exit 行 | C |
| "TOST p = 0.020 and 0.006" | 同上，`p(TOST)` 列 | C |
| "The other two scenarios were inconclusive" | cutin（+0.33，CI 上界 +3.12 > 界 3.03）、lead-brake（+0.86，上界 +3.81 > 界 3.09） | C |
| "no detectable difference" (RMSE / accel) | 8 个检验全部"未定"，TOST p 0.12–0.66 | C |
| "neither arm collided" | 20 局 `delta_collision` 全为 0 | — |
| "cannot reach significance after multiplicity correction" | n=5 精确检验最小 p=0.0625 > 0.05/4=0.0125（`15-` §3） | — |

**强度自查**：全文最高只用到 "we read … as evidence" 与 "we target equivalence"，
**未出现** prove / demonstrate / establish / significantly / outperforms。

---

## 合规自查（脚本化，2026-10-18）

| 检查项 | 结果 |
|---|---|
| em-dash（`—`、`--`） | 0 |
| 禁用词（novel / first / state-of-the-art / delve / underscore / pivotal / seamless / leverage / realm / showcase / foster / pave the way / shed light） | 0 |
| 公式化开头（In recent years / With the rapid development） | 0 |
| over-claiming 动词（prove / demonstrate / establish） | 0 |
| 每个实证数字是否有证据映射 | 是（见上表） |
| 是否有占位符残留 | 0 |
| 最长句词数 | 34（"Across four highway scenarios … six."）—— 已拆分过一次，仍偏长，**投稿前再审一次** |

---

## 与旧版的关系

- `00-title-abstract-fig1.md` 里的"结局 A / 结局 B"是**预注册时的两支假设**，用于防止事后挑口径；
  现在结果落在"等价 + 未定"，**故本文件的版本生效**，旧文件的 A/B 仅作历史记录。
- **不得**因为负性结果而修改 title 的"as a Control Input"表述——它陈述的是方法而非效果。
