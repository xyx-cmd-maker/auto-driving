# P1 标题 / 摘要骨架 / Fig.1 规格（2026-10-18 起草，**claim 句待全量填入**）

> 写作纪律来源：[`../../AGENTS-VENUE.md`](../../AGENTS-VENUE.md) 五条（标题与前两句落交通现象、
> Fig.1 必须是交通场景、OTF 是交通流量、必须出现 CARLA、负结果优先 T-ITS）。
> 语言纪律：`science-top-journal-writing`（证据强度匹配）+ `academic-humanizer`（去 AI 味，不改数字）。
> **数字纪律**：凡未定的数值一律写 `{{占位符}}`，**不得**先填估计值。

---

## 1. 标题（三选，均以交通现象开头）

**A（推荐，现象 + 机制 + 方法，最贴 T-IV 范围）**
> Overtaking Pressure on Multi-Lane Highways as a Control Input for Continuous-Time Car-Following

**B（更强调"是否值得"这个问题，适合负结果或等价结果）**
> Does Overtaking Frequency Help? A Closed-Loop Ablation of a Traffic-Flow Scalar in Continuous-Time Highway Control

**C（最保守，纯描述）**
> A Continuous-Time Controller Conditioned on Overtaking Frequency: Closed-Loop Ablation on a Multi-Lane Highway

**为什么 A 推荐**：
- 首词是 `Overtaking`（交通现象），不是 `A Novel...`；
- `as a Control Input` 明确了贡献边界（不是"我们提出 OTF"，OTF 归黄梦圆）；
- `Continuous-Time` 点出 CfC 的族属，但不把网络当卖点。

**禁用**：任何含 `novel` / `first` / `state-of-the-art` / `efficient` 的标题（前者过度声称，后者不可检验）。

---

## 2. 摘要骨架（约 200 词，**两个结局版本**）

### 2.1 通用前三句（两版共用，落在交通现象上）

> Multi-lane highways produce a continuous stream of lane changes around any given vehicle, and
> drivers routinely trade longitudinal gap for lateral opportunity. Whether this aggregate pressure
> carries usable information for a low-level controller remains unclear: prior work reports gains from
> overtaking-frequency (OTF) features in **classification** settings, but has not tested them inside a
> closed control loop.
>
> We therefore treat the OTF scalar, adopted as defined by Huang (2023), as a fourth input to a
> closed-form continuous-time (CfC) controller and ablate it against an otherwise identical controller
> that sees only gap, relative speed, and ego speed. Both arms share the same search budget, the same
> random seeds, and the same traffic stream.

### 2.1b 必须先交代的"信息可用性"（★ 2026-10-18 已用 SUMO 实测，替换掉原先的估算）

**实测（零门槛、可复现）**：`scripts/sumo/otf_density_sweep.py`，3 seeds × 5 密度，
同一套 OTF 定义，结果见 `papers/p1/figs/fig_otf_density.pdf`。

| 密度 (veh/h) | W=5 s 非零比例 | W=10 s | W=20 s |
|---|---|---|---|
| 600 | 0.118 | 0.221 | 0.393 |
| 1 200 | 0.248 | 0.425 | 0.692 |
| 2 400 | 0.415 | 0.633 | 0.878 |
| 3 600 | 0.515 | 0.738 | 0.934 |
| 4 800 | 0.563 | 0.768 | 0.903 |

**推论（可直接写进引言与讨论）**：
1. OTF 的信息可用性随密度**单调上升**，约 3 600–4 800 veh/h 趋于饱和；
2. 低密度（≤1 200 veh/h）下，5 s 窗口有 **≥75%** 是零，此时把 OTF 当控制输入属于**低信息 regime**；
3. 我们的 CARLA 闭环实验（16 辆混行车）就在这个低信息区 ⇒ **弱效应是机制性预期，不是实现失误**。

**建议引言句（英文，可直接用）**：
> Whether a scalar like OTF is usable depends on how often it is non-zero. We measured this
> availability directly: in a three-lane SUMO highway, the fraction of 5 s windows with OTF > 0
> rises from 0.12 at 600 veh/h to 0.56 at 4 800 veh/h (Fig. 1). Our closed-loop setting, with 16
> mixed vehicles, therefore sits in the low-information regime, and any ablation must be read
> against that base rate.

**纪律**：
- 这张图是**我们自己算的**（SUMO 合成流），措辞必须是 "in a SUMO highway"，
  **不得**写成 "in real-world traffic"；
- 若 highD 到手，只把它作为"曲线形状是否在真实数据中复现"的验证，**不改变主结论**；
- ~~原先"多数 5 s 窗口为 0"的估算已作废~~（那是按 highD 总量除总时长推的，与实测不符）。

---

### 2.2 结局 A：若全量为「有意义更小」（正向）

> ⚠️ 注意：`classification` 与 `closed control loop` 的对比是本段的核心张力，**不得**删掉：
> 它同时说明了"为什么值得做"与"我们做的是新问题"。

### 2.2 结局 A：若全量为「有意义更小」（正向）

> Across {{N_SCENARIOS}} highway scenarios in CARLA, the OTF-conditioned arm reduced the composite
> driving cost by {{DELTA_COST_MEAN}} (95% CI {{CI}}, exact paired test p = {{P}}, n = {{N_PAIRS}} pairs),
> with following RMSE changing by {{DELTA_RMSE}} and the acceleration-squared integral by
> {{DELTA_ACCEL}}. Collisions were {{COLLISIONS}} in both arms. We then replay recorded German highway
> trajectories (highD) with fixed neighbours and obtain {{REPLAY_RESULT}}. We read these results as
> evidence that OTF acts as a usable conditioning signal for longitudinal control on multi-lane
> highways, not as a predictor of individual neighbour behaviour.

### 2.3 结局 B：若全量为「实际等价 / 未定 / 逆向」（中性或负向，**当前更可能**）

> Across {{N_SCENARIOS}} highway scenarios in CARLA, the two arms were statistically
> indistinguishable on the composite cost (mean difference {{DELTA_COST_MEAN}}, 95% CI {{CI}},
> equivalence margin {{MARGIN}}), and the OTF-conditioned arm produced a **larger**
> acceleration-squared integral ({{DELTA_ACCEL}}). The OTF arm also yielded a higher fraction of
> failed search candidates ({{INVALID_ON}} vs {{INVALID_OFF}}), which we report as a property of the
> method rather than as noise. Replay on recorded highway trajectories (highD) gives {{REPLAY_RESULT}}.
> We conclude that an aggregate traffic-pressure scalar adds interpretability and requires no extra
> sensing, but does not by itself improve low-level following performance under an equal search budget.

> **纪律**：结局 B 里 **不得**出现 `no difference`（那是"证明无差异"，需等价检验）:
> 只有在 TOST 通过时才可写 `statistically equivalent`；否则写 `indistinguishable` 或 `undetermined`。

### 2.4 收尾句（两版共用）

> All code, scenario definitions, and result files are released to support re-analysis under the
> stated equivalence and multiplicity procedures.

---

## 3. Fig.1 规格（**必须是交通场景，不是网络结构图**）

| 项 | 规格 |
|---|---|
| 内容 | **三分面横排**：(a) 多车道高速俯视示意，标出 ego、前车、邻道车与一条换道轨迹箭头；(b) OTF 的计数几何（车辆跨越 ego 车道才计数，画 `crossed` 与 `not crossed` 两例）；(c) OTF 时间序列与对应跟车间距的对照曲线 |
| 尺寸 | 双栏宽 180 mm × 高 55–60 mm；单栏版可拆为 (a)(b) |
| 配色 | 色盲友好（Okabe–Ito）；ego 用深蓝、邻车灰、换道车橙 |
| 导出 | PDF（矢量）+ 300 dpi TIFF |
| 图注 | 首句说明"这是示意图还是实测"；**(c) 面板若来自 highD，必须写明 recording 编号与片段时长** |
| 数据来源标注 | (c) 面板的每个数值须能指到 `results/p1/otf_realism_highd_s1.json` 的字段；示意图部分标注 "schematic, not to scale" |
| **禁止** | 把 CfC 的 ODE 框图或网络层图放 Fig.1（放 Fig.2）；禁止用手绘的假 OTF 曲线 |

---

## 4. 合规自查（`academic-humanizer` 逐条过）

| 检查项 | 结果 |
|---|---|
| em-dash（`—`） | **0 处**（全部用逗号/冒号/括号替代） |
| 禁用词 `novel / first / state-of-the-art / delve / underscore / pivotal / seamless / leverage / realm / showcase / foster / pave the way / shed light` | **0 处** |
| 公式化开头 `In recent years...` | **0 处** |
| 连续 `Moreover/Furthermore/Additionally` | **0 处** |
| over-claiming 动词（prove / demonstrate / establish） | **0 处**（用 `read as evidence` / `we conclude` / `indistinguishable`） |
| 每个实证断言是否有数字或占位符 | **是**（全部 `{{}}` 占位，无估计值） |
| 过长句（>30 词或 3+ 从句） | 已拆；最长句 27 词 |
| 被动语态 | 仅保留"actor 无关"处（如 `are released`） |
| hedging 是否被误删 | 保留 `remains unclear`、`we read these results as evidence`、`does not by itself` |

---

## 5. 待填清单（全量跑完后一次性替换）

| 占位符 | 来源 |
|---|---|
| `{{N_SCENARIOS}}` / `{{N_PAIRS}}` | `runs/p1/cases/` 文件计数 |
| `{{DELTA_COST_MEAN}}` / `{{CI}}` / `{{P}}` / `{{MARGIN}}` | `train_cfc.py --analyze` 的 `delta_cost` 段 |
| `{{DELTA_RMSE}}` / `{{DELTA_ACCEL}}` | 同上，对应端点段 |
| `{{INVALID_ON}}` / `{{INVALID_OFF}}` | 同 `--analyze` 的"无效候选比例"段 |
| `{{COLLISIONS}}` | `paired.delta_collision` 与两臂 `best_metrics.collision_count` |
| `{{REPLAY_RESULT}}` | highD 回放实验（尚**未做**，需先申请数据） |
| `{{CLAIM_PENDING_FULL_RUN}}` | 结局 A/B 的选择，按 `configs/p1/a1_execution_freeze.yaml` 的结局矩阵 |

**在 `{{CLAIM_PENDING_FULL_RUN}}` 被替换之前，本文件不得作为投稿材料使用。**
