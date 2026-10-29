# Round 38 — 载体偏弱已在 5 种子确认，并写入 Limitations（E9）

> 日期：2026-10-29 ｜ 基线 commit：`f2f1250`

## 9.1 结论

| 项 | 判定 |
|---|---|
| R37 的单种子结论 | **5 种子全部确认** |
| 披露 | **E9 已写入 §5.5 Limitation 5**，第 6 页目视通过 |

## 9.2 五种子实测（none 场景）

| 指标 | PID（调参后） | CfC off 臂 | 比值 |
|---|---|---|---|
| following RMSE | **16.88 m** | **84.53 m** | **0.20×** |
| accel² | 667 | 314 | 2.13× |
| composite cost | 41.13 | 30.48 | 1.35× |

**配对差（PID − CfC）RMSE = −71.1 / −68.8 / −66.2 / −81.1 / −51.0 m**——**五个种子无一例外**。

⇒ 不是单局噪声：一个十几行、零训练的 PID，跟车误差稳定只有被检验控制器的 1/5。

## 9.3 写入稿件的文字（E9，§5.5 Limitation 5）

> "The controller under test is also modest. A tuned PID follows the lead with 17 m of root-mean-square error against 85 m here, on all five seeds. The ablation therefore tests the fourth input inside a weak carrier, not the best achievable controller."

**为什么必须写**：审稿人只要拿一个 PID 比一比就会发现；与其被指出，不如自己先说，并明确它限制了结论的适用范围（"inside a weak carrier"）。

## 9.4 顺带修了补丁工具的三个隐患

| 隐患 | 修法 |
|---|---|
| 已应用的编辑会报 ANCHOR-MISSING（误报） | 判"新文是否已在"，标记 `ALREADY` |
| **追加式编辑会被重复插入**（old 是新文的前缀） | 先判 `new in txt`，再判锚点 |
| E3 的 new 文本因 R31 改成 25 Hz 而失配 | 同步更新 E3 的 new 字符串 |

**若无这次修复，再跑一次 `--apply` 会把 E2/E8/E6 各插入第二遍。**

## 9.5 验证

8 页、checker exit=0、Overfull = 0、E9 文本在 PDF 第 6 页正确渲染（跨栏续行正常）。

## 9.6 诚实声明

1. 五种子**只在 none 场景**；其余三个场景未跑 PID。
2. PID 参数是为压 accel² 而调（kp 0.04），**属"为达标调参"**，若进论文须报告调参过程。
3. E9 是**披露**，不改变任何结论强度。
