# Round 31 — P1-S 已修：控制频率 20 Hz → **25 Hz**（并修掉自相矛盾的 "2.5 步"）

> 日期：2026-10-29 ｜ 基线 commit：`3610150`

## 9.1 结论

| 项 | 判定 |
|---|---|
| P1-S（频率事实错误） | **已修复并核验** |
| PDF | 8 页、0 编译错误 |
| 写作检查 | **checker exit=0**（最长句 35 词） |
| 源码残留 "20 Hz" | **0** |
| 源码 "25 Hz" | 4 处 |

## 9.2 改了什么

| 位置 | 原文 | 现文 |
|---|---|---|
| Methods §2.2 | "the controller runs at 20 Hz, so the observation is updated every **2.5** simulation steps" | "the controller runs **every second simulation step, that is at 25 Hz**, so the observation is updated every **2** simulation steps" |
| §4.1 执行指纹 | "50 Hz simulation, **20 Hz** control" | "50 Hz simulation, **25 Hz** control" |
| §4.1 定义句 | "one **20 Hz** observation step" | "one **25 Hz** observation step" |
| §5.5 Limitation 5 | "a control rate of **20 Hz** rather than the 100 Hz" | "a control rate of **25 Hz** rather than the 100 Hz" |

**顺带修掉一个自相矛盾**：原文说"20 Hz，所以每 **2.5** 个仿真步更新一次"——2.5 步在物理上不可能，
实际是每 **2** 步（25 Hz）。这正是 `round(2.5)=2` 造成的事实与文字脱节。

## 9.3 为什么这处必须改而不是"保留原文"

- 若读者按 20 Hz 复现，每局是 1200 步；实际是 1500 步（60 s × 25 Hz），**结果不可比**；
- "2.5 步"这句话本身就是错的，任何细心的审稿人都会停在这里；
- 改文字**不影响任何数字与结论**（两端同频），只需 4 处替换。

## 9.4 累计状态（Round 30 + 31）

| 轮次 | 内容 | 状态 |
|---|---|---|
| R30 | E1–E8（局数、术语、0.32 出处、无 Δv 结果、margin 敏感性、摘要范围、图注口径） | 已应用 |
| **R31** | **P1-S：20→25 Hz（含 2.5 步的矛盾）** | **已应用** |

稿件现为：**8 页、8 条参考文献、checker exit=0、229 词摘要**。

## 9.5 仍未解决（需你）

| 项 | 内容 |
|---|---|
| R1/R2 | "2/4 等价"是否改为"未检出 + 不可判定性"；或加种子到 43/场景 |
| 选刊 | T-IV / T-ITS / OJ-ITS |

## 9.6 诚实声明

1. 频率改动的依据是**实测**（平均控制周期 0.0400 s、每局 1501 帧）与**代码**（`round(2.5)=2`），非推断。
2. 本轮**未改任何数值结果**；九个数字审计脚本的输入未变。
3. 回退：`git checkout 3610150 -- papers/p1`。
