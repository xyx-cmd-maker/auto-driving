# Round 32 — 应用后复验：11 个审计脚本 + 第 4 页目视

> 日期：2026-10-29 ｜ 基线 commit：`6ac71da`

## 9.1 结论

| 项 | 判定 |
|---|---|
| 数字审计（11 个脚本） | **10 个 exit=0，1 个 exit=2（按设计）** |
| 第 4 页目视 | **通过**：25 Hz、十七局、E8 段落全部正确渲染，无溢出 |
| 稿件 | 8 页、8 条参考文献、checker exit=0 |

## 9.2 审计复跑结果

| 脚本 | 结果 |
|---|---|
| recompute_main / selection / table3 / number_sources / number_sources_body | exit=0 |
| protocol_conformance / table_text_consistency / limitations_evidence / future_work_claims / endpoint_states | exit=0 |
| **jerk_sensitivity** | **exit=2（按设计）** |

**关于 exit=2**：该脚本在"扣常数后等价判定翻转"时**故意返回非零**，用于让 CI/批处理注意到结论敏感。
它不是失败——把它当失败会把"发现重大问题"误报成"脚本坏了"。
**建议**：后续统一改名为 `--expect-change` 语义，或在 README 里登记这个非零码。

## 9.3 第 4 页目视（PDF 渲染实拍）

确认以下五处在**同页正确渲染**、无溢出、双栏未断：

1. "50 Hz simulation, **25 Hz control**, 24 hidden units" ✓
2. "A control cycle is one **25 Hz** observation step" ✓
3. "0.084 in **seventeen** runs and **0.168 in three**" ✓
4. E8 全段（2.577 / 2.800 / 1.918；"8.5 percent rather than 10 percent would leave none of the four equivalent"）✓
5. "so the observation is updated **every 2 simulation steps**" ✓

## 9.4 登记册更新

| 条目 | 变化 |
|---|---|
| F3（实际 25 Hz vs 论文 20 Hz） | **FIXED（R31）** |
| E1–E8（纠错与披露） | 已应用（R30） |

## 9.5 仍未解决（需你）

| 项 | 内容 |
|---|---|
| R1 / R2 | 把"2/4 等价"改为"未检出 + 不可判定性"（2–3 h）；或加种子 172 局（30 h） |
| 选刊 | T-IV / T-ITS / OJ-ITS |

## 9.6 诚实声明

1. 目视只覆盖**第 4 页**（新段落集中于此）；其余页未逐页目视。
2. `jerk_sensitivity` 的 exit=2 是**设计语义**，不是回归；我在报告里写明，避免下一轮误判。
3. 本轮未改稿件任何内容，只做复验与登记。
