# 逐局结果（外审可复核副本）

> 本目录是**脱敏副本**，原文件在作者机器的 `runs/` 下（体积大、未入库）。
> 复制时间：2026-10-29 ｜ 内容：每局一个 JSON，字段含 `scenario`、`seed`、`arms`、`paired`、`guards`、`exec`。
> 已检查：**不含**本地绝对路径、用户名、邮箱。

## 目录含义

| 子目录 | 是什么 | 局数 |
|---|---|---|
| `main/` | 主实验：四场景 × seeds 0–4；**另加 lead-brake 的 seeds 5–9（窗口 5 s）** | 25 |
| `window10/` | 窗口 10 s 的 lead-brake，seeds 0–9 | 20 |
| `window20/` | 窗口 20 s 的 lead-brake，seeds 0–9 | 10 |
| `degraded/` | **删掉相对速度**（Δv）的 lead-brake，seeds 0–4，窗口 5 s | 5 |

**注意**：`main/case_lead-brake_s*.json` 有 **10 个**，因为 2026-10-19 把 lead-brake 补到了 n=10；
其余三个场景仍是 5 个。论文 Table I 用的是 **seeds 0–4**，窗口标准差那一节用的是 **n=10**。

## 一键复核

```powershell
py -3.12 scripts/verify_from_published_cases.py
```

预期输出（2026-10-29 实测，exit=0）：

```
  窗口           n    Δcost 均值  Δcost SD
  main        10      +0.409     1.718
  window10    10      +0.587     1.809
  window20    10      +0.558     1.926

  机制检验（删掉相对速度）：off 臂复合代价
    有 Δv（main 全部）     n=10  均值 30.82
    无 Δv（degraded）     n=5  均值 30.96
    差值 +0.14

  主实验四场景的配对差（main 组，seeds 0-4）
  none                5      +0.256
  cutin               5      +0.326
  lead-brake         10      +0.409
  lead-exit           5      -0.051
```

若你算出的数与上面不同，说明数据与稿件不一致——请直接告知作者。

---

## 2026-10-29 追加：Table III 与 Fig.2 补充组的逐局数据

原先 Table III 的 A 组与 Fig.2 的 W=20 s 另两场景**只有作者机器上的 `runs/` 副本**，
公开仓库无法复核。本轮已把 15 个文件补入（同样脱敏：无本地路径、无用户名、无邮箱）：

| 子目录 | 是什么 | 局数 | 执行参数 |
|---|---|---|---|
| `highdensity/` | **A 组**：交通车辆 32（其余同主实验），lead-brake | 5 | 32 辆 / 5 s 窗口 / 60 s |
| `window20extra/` | **B2 组**：20 s 窗口下的另两个场景 | 10 | 16 辆 / 20 s 窗口（cutin 5 + lead-exit 5） |

复核命令：

```powershell
py -3.12 scripts/audit_table3_supplementary.py
```

预期（2026-10-29 实测，exit=0）：

```
  Main         n=5  Δ=+0.858  CI[-2.092, 3.808]  宽 5.90  Φ=0.084
  A, density   n=5  Δ=+1.371  CI[-2.326, 5.069]  宽 7.40  Φ=0.084
  B, window    n=5  Δ=+0.707  CI[-2.709, 4.122]  宽 6.83  Φ=0.334
  W=20 s 三场景 Φ 最大值：0.334 / 0.334 / 0.497
```

> 注意：`highdensity/` 与 `window20extra/` 是**补充实验组**，不是预注册主分析的一部分；
> 引用它们时必须写明"补充组"，不得与主实验合并报告。