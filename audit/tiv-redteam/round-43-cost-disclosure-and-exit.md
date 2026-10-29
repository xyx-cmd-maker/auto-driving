# Round 43 — 补上代价侧披露（E10）+ lead-exit 批次跑通（换启动方式）

> 日期：2026-10-29 ｜ 基线 commit：`0bbb48c`

## 9.1 结论

| 项 | 判定 |
|---|---|
| E10（补代价侧） | **已写入并验证**（8 页、checker 0、Overfull 0） |
| lead-exit 批次 | **跑通 3 局**（此前两次失败是执行器派生进程失败，改用 .ps1 文件启动即正常） |
| lead-exit 稳定性 | **差**（44.2 / 52.2 / **124.3**，SD 44） |

## 9.2 E10：修正我上一轮的选择性披露

**改前**（E9）只说了 RMSE：
> "A tuned PID follows the lead with 17 m … against 85 m here, on all five seeds."

**改后**（E10）补上代价侧：
> "**Its composite cost is nevertheless 1.3 to 2.1 times ours across three scenarios, because a direct speed target trades comfort for tracking.**"

验证：PDF 含 "1.3 to 2.1 times ours" 与 "trades comfort for tracking"；8 页、checker exit=0、Overfull 0。

## 9.3 lead-exit 批次（3 局）

| seed | cost | travelled |
|---|---|---|
| 0 | 44.2 | 498.2 m |
| 1 | 52.2 | 415.3 m |
| 2 | **124.3** | 401.5 m |
| 均值 | **73.6** | — |
| SD | **44.1** | — |

CfC 的 lead-exit 均值是 29.5 ⇒ PID 约为 **2.5×**，且**方差极大**（此前单局还出现过 191.8）。

**解释（H 级）**：前车驶离后 `lead_gap` 跳回默认 200 m，PID 直接按 `kp(gap − d_des)` 给出大目标速度，
行为对该跳变极其敏感 ⇒ **lead-exit 上 PID 不能作为公平参照**。

## 9.4 PID 基线的最终定位（4 场景合并）

| 场景 | PID 均值 | SD | CfC 均值 | 比值 | 可用性 |
|---|---|---|---|---|---|
| none | 41.13 | 10.26 | 30.48 | 1.35× | 可用作参照 |
| cutin | 39.49 | 10.62 | 30.31 | 1.30× | 可用作参照 |
| lead-brake | 63.95 | 21.39 | 30.95 | 2.07× | 可用作参照 |
| lead-exit | 73.58 | 44.13 | 29.53 | 2.49× | **不稳定，不可用** |

**结论**：门槛 7（强基线）**从"代码就绪"升到"3/4 场景有参照数据"**，但**仍未达标**——
因为 (a) lead-exit 不稳定，(b) 该 PID 是**为压 accel² 调参**得到的，不是"调好的强基线"。

## 9.5 下一步

| # | 任务 | 需谁 |
|---|---|---|
| 1 | lead-exit 补到 5 局并写明"不稳定、不可作参照" | 我（0.2 h） |
| 2 | 若要真正的强基线：需 PID 在 gap 跳变时加保护逻辑 | 1–2 h |
| 3 | R1 / R2 / 换刊 | **需你** |

## 9.6 诚实声明

1. lead-exit **只有 3 局**，且其中一局是 124.3 的异常值；不构成稳定估计。
2. E10 的数字（1.3–2.1×）来自**3 个场景的 5 局均值**，不含 lead-exit；所以措辞是 "across three scenarios"。
3. 本轮未改实验设计，只改披露。
