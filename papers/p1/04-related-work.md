<!-- BEGIN-MANUSCRIPT -->

# 3. Related work

## 3.1 Traffic-flow descriptors as controller inputs

Car-following models describe the longitudinal response to a lead vehicle, and the classical families
differ in how much memory they carry. String-stability analysis then asks whether a perturbation
amplifies along a platoon [string-stability]. That line of work treats the lead vehicle as the relevant
input. Everything behind and beside the ego enters, if at all, through aggregate parameters such as
density or wave speed [wave-dissipation].

A second line feeds traffic-level information to the controller explicitly. Cooperative control schemes
share planned trajectories and solve a joint optimization over a rolling horizon [DeeP-LCC]. These
methods work with rich per-vehicle messages rather than one scalar, and they assume connectivity. Our
question is narrower: whether one scalar computed from unconnected traffic carries enough information
to change a low-level command.

## 3.2 Overtaking frequency and social pressure

The OTF scalar comes from the behavior-decision literature. Huang (2023) defined it as the rate at which
surrounding vehicles cross the ego lane and reported accuracy gains of 1.0 to 5.5 percentage points when
OTF features are added to classifiers. Those results are reported for classification, on a dataset that
is not available to us, and we do not reproduce them here.

The idea that surrounding traffic exerts a pressure that can be summarized is older than OTF. Social-force
formulations describe the same intuition for pedestrians, and variants have been adapted to vehicles
[social-force]. Our contribution is not the notion of pressure but a closed-loop test of whether one
particular scalarization of it changes a control command.

## 3.3 Continuous-time and closed-form recurrent models

Liquid time-constant and closed-form continuous-time networks replace discrete recurrence with a
continuous ODE-like update and report large speedups over conventional recurrent cells [CfC]. The
claimed advantage is compute per step rather than sample efficiency. We use a CfC cell precisely because
it is cheap enough to evaluate twelve candidates per arm inside a 60 s episode, which is what makes an
equal-budget ablation affordable on a laptop GPU.

The same literature motivates our architecture choice. A pure ODE state integrates its input and
responds slowly, so a controller that relies on it alone cannot react to an instantaneous gap change. We
add a direct linear path from the observation to the command, and we report both parameter counts.

## 3.4 Physics-informed and structure-informed priors

A large body of work injects physical structure into learning. Physics-informed neural networks add a
residual of a governing equation to the loss [PINC]. That approach requires an equation whose residual
can be evaluated, and it succeeds when the residual is meaningful.

OTF does not provide such a residual. It is a heuristic aggregate with no governing equation, so a
soft physics loss would not be well posed. We therefore treat it as an additional input and as an
inductive bias, and we describe it as structure-informed rather than physics-informed. The distinction
matters because it determines what evidence would count as success: a physics-informed claim can be
checked against the residual, whereas our claim can only be checked in closed loop.

## 3.5 What is missing

Three gaps follow from the above. Closed-loop evidence for OTF is absent, because the reported results
are classification accuracies. Equivalence is rarely reported, because ablation studies usually test
for a difference and stop when none is found. And the operating point is rarely characterized, because
availability of a traffic-level signal depends on density in a way that is easy to leave implicit. This
paper addresses the three together.

<!-- END-MANUSCRIPT -->

---

## 引用槽位映射（作者/年份须从已核验库填，**不得凭记忆写**）

| 槽位 | 必须支持的论断 | 来源（已核验库条目） | 状态 |
|---|---|---|---|
| `[string-stability]` | 跟驰模型的弦稳定性分析传统 | `literature/library/P1-library.jsonl` 中"弦稳定/Lp"条目；限定语见 `literature/notes/citation-qualifiers.md` #33 | 待填 author-year |
| `[wave-dissipation]` | 用密度/波速等宏观量描述交通 | 同上库"波消散"条目（qualifier #43） | 待填 |
| `[DeeP-LCC]` | 连通条件下滚动时域协同控制 | 同上库 DeeP-LCC 条目（qualifier #45） | 待填 |
| `[CfC]` | 闭式连续时间网络及其速度优势 | NMI 2022，参数量口径见 `AGENTS.md` §1（4 184 / 230 828） | 待填 |
| `[PINC]` | 物理残差作为软损失项 | Neurocomputing 2024（qualifier #7）；**该文从未做 λ=0 消融** | 待填 |
| `[social-force]` | 社会力用于行人、并被移植到车辆 | 需在库内确认具体条目 | **未确认，须先核** |
| Huang (2023) | OTF 定义与分类增益 1.0–5.5 pp | `sources/thesis-huang2023.pdf`（全文可 grep） | 已核 |

**纪律**：上表 7 项中只有 Huang (2023) 是已逐字核验的；其余 6 项**必须先按
`literature/library/P1-library.jsonl` 的字段填 author-year 与 DOI，核不到就整句删除**，
不得留占位符进投稿版。
