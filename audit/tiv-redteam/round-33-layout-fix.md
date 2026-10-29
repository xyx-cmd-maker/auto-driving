# Round 33 — 修掉一处真实排版缺陷：Table IV 超宽 75 pt

> 日期：2026-10-29 ｜ 基线 commit：`21b6332` ｜ 修复 commit：`df48146`

## 9.1 结论

| 项 | 判定 |
|---|---|
| Overfull hbox | **1 → 0** |
| 页数 | 8（未变） |
| 写作检查 | checker exit=0 |
| 分组信息 | **未丢失**（移入表题） |

## 9.2 问题

`manuscript.log` 报告 **1 处 Overfull hbox（75 pt ≈ 2.6 cm）**，位置在附录 Table IV（逐局结果表，8 列）。
该表放在双栏 IEEE 文档的**单栏**里，8 列（含 `lead-brake`/`lead-exit` 与 `valid off/on`）**装不下**，
内容溢出到栏外——打印版会明显越界。

## 9.3 修法（三步，均不删信息）

| 步骤 | 做法 |
|---|---|
| 1 | 去掉 `Group` 列（29 行受影响），把该信息**移入表题**："The first twenty rows form the main group; the last five repeat the lead-brake scenario with relative speed removed from the observation." |
| 2 | 表头缩短：`Scenario→Scen.`、`off cost→off`、`on cost→on`、`Phi (on)→Phi`、`valid off/on→n off/on` |
| 3 | 场景名缩短：`lead-brake→brake`、`lead-exit→exit` |

**验证**：
- `Overfull \hbox` 计数 **0**；
- PDF 同时含 "first twenty rows" 与 "relative speed removed"（说明信息确实进了表题）；
- 8 页、checker exit=0。

## 9.4 为什么这值得单独一轮

排版溢出是**唯一一类机器能发现、但所有内容审计都会漏掉**的缺陷：
数字全对、逻辑全对，印出来还是有一行飘到栏外。它属于"必须看一眼 PDF"才能收口的问题。

我此前 32 轮只做过一次目视（Round 32 第 4 页），**没有检查 LaTeX 日志的 Overfull 计数**——这是本轮补上的检查项。

## 9.5 新增的常规检查（已纳入后续流程）

```powershell
# 每次重编译后必查
Select-String -Path manuscript.log -Pattern 'Overfull \\hbox' | Measure-Object   # 期望 0
```

## 9.6 诚实声明

1. 修法**改变了表的呈现**（少一列、场景名缩写），**没有删任何数据行**；分组信息改由表题承载。
2. 我只检查了 **Overfull hbox**；**Underfull hbox（5 处）未处理**——它只影响词间距美观，不影响正确性。
3. 本轮未改任何数字、结论或统计方法。
4. 其余页面仍未逐页目视。
