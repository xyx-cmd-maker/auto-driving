# A1 闭环消融：全量结果（20 局，2026-10-18）

> **性质**：按 [`configs/p1/a1_execution_freeze.yaml`](../../configs/p1/a1_execution_freeze.yaml)
> 预注册协议执行完毕的结果。**结论范围为"本协议下"**，不外推到别的密度/窗口/基线。
> 逐局明细：[`15-a1-full-results.data.md`](15-a1-full-results.data.md)（自动生成）
> 原始产物：`runs/p1/cases/case_<scenario>_s<seed>.json`（20 份，含 `exec` 执行指纹）
> 统计命令：`py -3.12 src/ctrl/train_cfc.py --analyze --scenarios none,cutin,lead-brake,lead-exit --seeds 0,1,2,3,4`

---

## 0. 三句话结论

1. **没有证据表明 OTF 输入改善了闭环控制**：3 个端点 × 4 个场景共 12 个检验，**无一显著**。
2. **但有 2/4 场景达到了"实际等价"**（composite cost 的 95% CI 完全落在 ±10% 等价界内）：
   `none`（p=0.0198）与 `lead-exit`（p=0.0060）。这比"未定"强，也比"无差异"诚实。
3. **一个必须先讲清的效力缺陷**：n=5 的精确符号翻转检验**最小可能 p = 2/32 = 0.0625**，
   而 Holm 校正（4 个场景）要求首个 p ≤ 0.0125 ⇒ **按构造， superiority 结论在本设计下不可能成立**。
   因此本文的正确推断目标是**等价性（TOST）**，而不是显著性——这与预注册一致。

---

## 1. 数据与可判定性

| 项 | 值 |
|---|---|
| 完成局数 | **20 / 20**（4 场景 × 5 种子） |
| 执行指纹 | **20 局完全一致**（`episode_s=60, traffic=16, sim_hz=50, control_hz=20, hidden=24, candidates=12, elite=3`）|
| 看护 | G0 无效择优 **0** ｜ G1 空 episode **0** ｜ G3 拥塞/死锁 **0** |
| **处理变量激活率 Φ_OTF>0** | **0.084 / 0.167**（两种取值；**全部 20 局均 >0**，满足"可判定"前提） |
| 碰撞 | **两臂全 0，20 局 Δ 均为 0** |
| 单局耗时 | 约 9.5–10.7 min |

> **这一栏是本轮最重要的前提**：早期版本的 A1 里 Φ 恒为 0（等于没测），
> 现在 20/20 局都真正激活，才谈得上"比较"。

---

## 2. 主结果（逐场景三态，冻结协议）

### 2.1 决策指标 `Δcost`（主口径：各取最好有效候选，负值 = OTF 臂更好）

| 场景 | n | 均值Δ | off 均值 | 95% CI | 精确 p | TOST p | **三态** | 等价界(±10%) |
|---|---|---|---|---|---|---|---|---|
| none | 5 | **+0.256** | 30.481 | [−2.321, +2.832] | 0.8125 | **0.0198** | **实际等价** | ±3.048 |
| cutin | 5 | +0.326 | 30.314 | [−2.467, +3.119] | 0.8750 | 0.0273 | 未定 | ±3.031 |
| lead-brake | 5 | +0.858 | 30.947 | [−2.092, +3.808] | 0.4375 | 0.0515 | 未定 | ±3.095 |
| lead-exit | 5 | **−0.051** | 30.623 | [−1.968, +1.867] | 1.0000 | **0.0060** | **实际等价** | ±3.062 |

**读法**：
- `none` / `lead-exit`：CI 完全落在等价界内 ⇒ **"两臂在 cost 上实际等价"成立**（这是可写进摘要的强陈述）。
- `cutin` / `lead-brake`：CI 上界（+3.12 / +3.81）**略超**等价界，且均值为正 ⇒ **只能说"未定"**。
  注意两者均值都偏正（OTF 臂 cost 略高），但**不能**据此说有差异。
- **Holm 校正后全部不显著**（最小 p=0.4375 ≫ 0.0125）。

### 2.2 性能端点 1：`Δfollowing_rmse`

| 场景 | 均值Δ | 95% CI | 精确 p | TOST p | 三态 |
|---|---|---|---|---|---|
| none | −4.361 | [−26.629, +17.908] | 0.6250 | 0.3184 | 未定 |
| cutin | −4.767 | [−27.421, +17.888] | 0.6250 | 0.3432 | 未定 |
| lead-brake | −0.761 | [−18.849, +17.327] | 0.8125 | 0.1484 | 未定 |
| lead-exit | −2.317 | [−14.851, +10.217] | 0.6250 | 0.1161 | 未定 |

四个场景均值方向一致为**负**（OTF 臂跟车误差略低），但 CI 极宽（±18–27 m，off 均值约 84–87 m）
⇒ **只能描述方向，不能作推断**。

### 2.3 性能端点 2：`Δaccel_sq_integral`（舒适性）

| 场景 | 均值Δ | 95% CI | 精确 p | TOST p | 三态 |
|---|---|---|---|---|---|
| none | **+34.47** | [−6.004, +74.934] | 0.1250 | 0.5786 | 未定 |
| cutin | **+40.13** | [−13.938, +94.190] | 0.0625 | 0.6637 | 未定 |
| lead-brake | **+46.89** | [−49.977, +143.762] | 0.2500 | 0.6435 | 未定 |
| lead-exit | **+8.98** | [−79.179, +97.131] | 0.8125 | 0.2630 | 未定 |

**四个场景均值全为正**（OTF 臂更不平顺，off 均值约 310–331）。
`cutin` 的精确 p=0.0625 已是 n=5 的**最小可能值**（即"全部同号"），
但**仍达不到显著**，且 TOST p=0.66 ⇒ **既不能说更差，也不能说等价**。
**写作纪律：这条只能写成"方向一致但不显著的方向性观察"，不得写成"OTF 使车辆更不平顺"。**

---

## 3. ★ 必须写进 Limitations 的效力缺陷（本轮新发现）

n=5 的双侧精确符号翻转检验，p 只能取 {2/32, 4/32, …, 1} 的离散值，**最小 0.0625**。
预注册用 Holm-Bonferroni 控制 4 个场景，首个阈值 = 0.05/4 = **0.0125**：
**0.0625 > 0.0125 ⇒ 本设计在任何数据下都不可能拒绝零假设。**

**这不是"结果不好"，而是"设计选了错误的推断目标"。** 正确的处理是：
1. **主推断改为等价性（TOST）**——已在预注册里写明 margin=10%，因此**不是事后改口**；
2. 显著性检验**照实报告为"无显著差异"**，并说明其**不可达**，避免读者误以为是"数据弱"；
3. 在 Limitations 明确写："with five seeds, the exact paired test cannot reach conventional
   significance after multiplicity correction; we therefore target equivalence."

---

## 4. 敏感性分析：等 K 口径**方向相反**（必须双报）

| 口径 | 均值 Δcost | 中位 | 范围 |
|---|---|---|---|
| **主口径**（各取最好有效候选） | **+0.347** | +0.612 | [−2.959, +3.193] |
| **等 K**（K = min(有效候选数)，取前 K 均值） | **−1.066** | −0.684 | [−11.590, +12.414] |

**方向翻转**：主口径（OTF 略差）与等 K（OTF 略好）符号相反。
**原因**：有效候选数在臂间不等（部分局 off 8 / on 5），等 K 会**丢弃 off 臂的部分好候选**，
等于给 OTF 臂"减压"。

**处理（已在预注册中写死）**：
- 主口径仍为 best-of-budget（因为实验问题就是"固定 12 次候选预算下哪个臂更好"）；
- **等 K 必须在稿件中同时给出**，并如实说明"结论依赖候选池大小"；
- **不得**只报对自己有利的那个。

---

## 5. 训练难度（按纪律不隐去）

| 场景 | off 无效率（5 seeds） | on 无效率 |
|---|---|---|
| none | 33/42/58/50/58 % | 58/50/42/25/58 % |
| cutin | 33/42/58/50/58 % | 58/50/42/25/58 % |
| lead-brake | 33/42/58/50/58 % | 58/42/42/25/58 % |
| lead-exit | 33/42/58/50/58 % | 58/42/42/25/67 % |

**两臂的无效率互有高低**（全量 20 局里 off 平均约 48%，on 约 47%）——
**与中量验证（n=4）时"on 臂系统性更高"的印象不同**。
⇒ 中量验证的那个"OTF 更难训"的观察**在 n=20 上没有复现**，**不得**写进稿件。

---

## 6. 按冻结结局矩阵选 claim

预注册的矩阵（`configs/p1/a1_execution_freeze.yaml` → `outcome_matrix`）：

| 若结果 | 允许的 claim | 本次落在哪 |
|---|---|---|
| cost 有意义更小，且性能端点不显著变差 | "OTF 改善闭环控制"（B/C 级） | ✗ |
| cost **实际等价** | 改为「**可解释性 + 零额外传感器成本**」；**不得**写"OTF 提升性能" | **✓ 部分成立（2/4 场景）** |
| cost 有意义更大 | 诚实报告负结果 | ✗ |
| 未定 | 扩种子/场景后重跑 | ✓ 部分成立（2/4 场景） |

**因此 P1 的 claim 定为**（不得越界）：

> 在 CARLA 高速多车道混行、`Φ_OTF>0` 占 8–17% 的低信息 regime 下，
> 把 OTF 作为第 4 维输入的控制器与不带它的控制器，在**复合代价上统计等价**（2/4 场景，
> TOST 10% 界），在跟车误差与加速度积分上**无可检出差异**；
> 因此 OTF 的价值不在"性能提升"，而在**可解释性**与**零额外传感器成本**（只用已有雷达/视觉即可估计）。
> `cutin` 与 `lead-brake` 两个场景**未定**，需扩样本。

---

## 7. 英文摘要可用句（数字已填，待 `academic-humanizer` 复核）

> Across four highway scenarios in CARLA with five seeds each (20 paired runs, 12 controller
> candidates per arm), conditioning a closed-form continuous-time controller on the
> overtaking-frequency (OTF) scalar changed the composite driving cost by +0.26 (95% CI
> [−2.32, +2.83]) in the no-lead vehicle scenario and by −0.05 ([−1.97, +1.87]) in the lead-exit
> scenario, both within a pre-registered ±10% equivalence margin (TOST p = 0.020 and 0.006).
> The remaining two scenarios were inconclusive because their confidence intervals crossed the
> margin. Following RMSE and the acceleration-squared integral showed no detectable difference in
> any scenario, and no collisions occurred in either arm. With five seeds the exact paired test
> cannot reach significance after multiplicity correction, so we target equivalence rather than
> superiority. We read these results as evidence that an aggregate traffic-pressure scalar buys
> interpretability at no additional sensing cost, not closed-loop performance.

**写作纪律**（`academic-humanizer`）：
- 无 em-dash；无 `novel/first/state-of-the-art/delve/underscore/pivotal/seamless/leverage`；
- 不用 `prove/demonstrate/establish`；用 `we read these results as evidence`；
- "inconclusive" 不得写成 "no difference"；"equivalent" 只在 TOST 通过处使用；
- `+0.26` 等数字必须能指到 `15-a1-full-results.data.md` 与 `--analyze` 输出。

---

## 8. 限制（≥3 条，必须进稿件）

1. **效力**：n=5 的精确检验在 Holm 校正后**不可达显著**；本文推断以等价性为主，结论为"无优势"，不是"优于"。
2. **口径依赖**：主口径与等 K 口径**方向相反**（+0.35 vs −1.07）；稿件必须双报。
3. **低信息 regime**：Φ_OTF>0 仅 8–17%，且密度远低于相图的饱和区（见 [`13` §11](13-public-dataset-strategy.md)）；结论**不外推到高密度**。
4. **构造性交通**：OTF 激活依赖**脚本化 cut-in**（直接置位），不是自然换道；不得写 natural lane changes。
5. **仿真与频率**：单地图（Town04）、单车型（Tesla Model3）、控制频率 **20 Hz**（协议原写 100 Hz）。
6. **无真实数据**：highD/exiD 未到手；真实数据回放列为 Future Work。

---

## 9. 什么会改变这个结论

| 变化 | 预期影响 | 成本 |
|---|---|---|
| 种子 5 → 20（n=20/场景） | 精确检验最小 p 降到 2/2²⁰ ≈ 2e-6，**可做 superiority**；CI 宽度约减半 | 约 4× 时长（~5 h/场景集） |
| 提高密度到 ≥3 600 veh/h 等效（更多混行车） | Φ 升到 ≥0.5，进入相图的高信息区，**最有可能看到真实效应** | 需改 env 的交通生成 + 重跑 |
| 窗口 5 s → 20–30 s | 低密度下 Φ 从 0.08 升到 0.8（相图），信号更可用 | 改 OTF 窗口 + 重跑 |
| 真实数据（highD）回放 | 提升外部效度，但不改变"低信息 regime"的判断 | 需审批 |

**建议下一步（按性价比）**：**先做"提高密度 + 加长窗口"两组的各 5 局**（约 2 h），
因为相图明确指向"当前设定在低信息区"——这是最可能改变结论、且**零门槛**的一步。
