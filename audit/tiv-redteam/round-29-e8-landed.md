# Round 29 — E8 落地：margin 敏感性已进补丁集（沙盒 8 页 / checker exit=0）

> 日期：2026-10-29 ｜ 基线 commit：`c08667e`

## 9.1 结论

| 项 | 判定 |
|---|---|
| E8 | **已加入补丁集并沙盒验证通过** |
| 补丁集 | E1–E8 + 可选 E6（8 处），dry-run **8/8 锚点唯一** |
| 沙盒 | **8 页、0 编译错误、checker exit=0**（最长句 35 词） |

## 9.2 先修了一个我自己造成的破坏

**发现**：`scripts/apply_pending_edits.py` 在 Round 28 被我的一条失败命令 `Set-Content` **清空为 0 行**；
Round 28 我报告的 "dry-run exit=0" 实际是**跑空文件**的结果（空模块退出码也是 0），**那是误判**。

**处置**：
1. `git checkout 65d92ea -- scripts/apply_pending_edits.py` 从上一个完好提交恢复（**139 行**，compile=0）；
2. 重新跑 dry-run：**7/7 锚点唯一**，确认恢复成功；
3. 用 `edit` 工具（而非 PowerShell 内联）插入 E8，避免引号转义。

**教训**：`py_compile` 对**空文件**也返回 0；用"退出码"当验证会漏掉"文件被清空"这种事故。已记入错题本。

## 9.3 E8 的内容（拆成 5 句，最长 24 词）

> These verdicts sit close to the margin. For no lead vehicle, equivalence would still hold at a margin of
> 2.577, which is 85 percent of the pre-registered 3.048. For cutin the corresponding value is 2.800, or
> 92 percent of 3.031. For lead exit it is 1.918, or 63 percent of 3.062. A margin of 8.5 percent rather
> than 10 percent would leave none of the four equivalent. We therefore read the equivalence as
> conditional on the margin rather than as a robust absence of effect.

**它不改变任何数字**，只把 Round 27 的敏感性分析写进 §4。

## 9.4 补丁集现状（8 处）

| id | 位置 | 作用 |
|---|---|---|
| E1 | 摘要 | 0.084 → 0.084–0.168 |
| E2 | Fig.2 图注 | 声明三来源统计量不同 |
| E3 | §4.1 | 16/4 → 17/3 + 定义帧 |
| E4 | §5.2 | windows → control cycles |
| E5 | §5.3 | 0.53 加"10 次 run 均值" |
| E6（可选） | §5.2 | 写入无 Δv 结果 |
| E7 | §5.3 | 0.32 写明插值依据 |
| **E8** | §4 等价段 | **margin 敏感性披露** |

## 9.5 下一步（需你）

1. **批准 E1–E8**（`py -3.12 scripts/apply_pending_edits.py --apply`）——修错 + 披露，均与选刊无关；
2. 定叙事方向（R1 重构 / R2 加 172 局 / 换刊）。

## 9.6 诚实声明

1. Round 28 的 "dry-run exit=0" 是**误判**（空文件），本轮已更正并修复。
2. E8 只加披露，**不改变任何数字与结论**。
3. 真实稿件仍未改动。
