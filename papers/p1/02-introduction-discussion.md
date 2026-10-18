<!-- BEGIN-MANUSCRIPT -->

# 1. Introduction

On a multi-lane highway, a driver's longitudinal decision is shaped by what happens in the adjacent
lanes. A vehicle that closes on a slower lead may either slow down or move over, and the choice
depends on how much lateral opportunity the surrounding traffic offers. Over a few seconds these
individual choices aggregate into a measurable rate at which vehicles cross a given lane.

Huang (2023) proposed to summarize this aggregate as the overtaking frequency (OTF): the number of
lane crossings observed in a sliding window around the ego vehicle, divided by the window length.
OTF is attractive for three reasons. It is a single scalar. It is defined on traffic rather than on a
particular sensor suite. And it can be estimated from radar and camera streams that production
vehicles already carry, so it adds no sensing cost.

Evidence for OTF so far comes from classification. The reported gains are 1.0 to 5.5 percentage
points of classifier accuracy over baselines without OTF features, across three classifier families
(Huang, 2023, as reported; not reproduced here). Classification and control ask different questions.
A feature can improve an offline label prediction and still add nothing to a feedback loop that
already observes gap and relative speed. Those results are classification accuracies, and none of them
closes the loop.

We test it directly. We treat OTF as a fourth input to a closed-form continuous-time (CfC) controller
and compare it against an otherwise identical controller that sees only lead gap, relative speed, and
ego speed. Both arms share one twelve-candidate search budget, the same five seeds, and the same
traffic stream, so any difference must come from the fourth input.

A scalar can only help if it is non-zero often enough, so we measured availability before measuring
effect. In a three-lane SUMO highway, the fraction of 5 s windows with OTF > 0 rises from 0.12 at
600 veh/h to 0.56 at 4800 veh/h. A 20 s window reaches 0.93 at 3600 veh/h. In the CARLA setting used
for the closed-loop experiment, with sixteen mixed vehicles, the measured fraction was 0.084 to 0.167.
That setting therefore sits in the low-information regime, and the closed-loop result has to be read
against this base rate rather than as a verdict on OTF in general.

This paper makes three contributions.

1. A closed-loop ablation of OTF under an equal search budget, reported per scenario with an
   equivalence test that was registered before the data were collected. Two of four scenarios are
   statistically equivalent on composite driving cost within a 10% margin (TOST p = 0.020 and 0.006);
   the other two are inconclusive.
2. A measured map of OTF availability as a function of traffic flow and window length, obtained with
   the same OTF definition used by the controller. The map shows that availability is governed by
   density and window jointly, and that our closed-loop setting is in its lower region.
3. An explicit account of why the experiment cannot support a superiority claim even if a difference exists:
   with five seeds the exact paired test cannot reach significance after multiplicity correction. We
   therefore target equivalence, and we report the equal-K sensitivity analysis that reverses the sign
   of the effect estimate.

Section 2 describes the controller, the OTF definition, and the two environments. Section 3 gives the
protocol and the pre-registered analysis. Section 4 reports results. Section 5 discusses what the
results do and do not imply. Section 6 lists limitations.

# 5. Discussion

## 5.1 What the experiment shows

Across four highway scenarios with five seeds each, conditioning the controller on OTF changed the
composite driving cost by +0.26 (95% CI [−2.32, +2.83]) without a lead vehicle. In the lead-exit
scenario the change was −0.05 ([−1.97, +1.87]). Both intervals lie inside the pre-registered 10%
equivalence margin, with TOST p = 0.020 and 0.006. The cutin and lead-brake scenarios were
inconclusive, because their intervals crossed the margin. Following RMSE and the acceleration-squared
integral showed no detectable difference in any scenario, and neither arm collided.

We read this as evidence that OTF buys interpretability at no additional sensing cost, not closed-loop
performance. The wording matters. Equivalence within a 10%
margin is a positive statement about practical similarity, and it is stronger than a failure to
reject. It is also weaker than a claim of no effect: a difference smaller than the margin, or one
confined to a regime we did not reach, remains compatible with our data.

## 5.2 Why no gain, and why that is not surprising

Two mechanisms are consistent with the result, and they are not mutually exclusive.

One mechanism is redundancy at the controller input. A longitudinal controller that already observes lead
gap and relative speed has most of what a one-dimensional traffic aggregate can say. OTF summarizes
the behaviour of vehicles that are not the lead vehicle. When those vehicles do not constrain the ego,
their aggregate contributes little to the instantaneous decision.

The other mechanism is signal availability. The measured fraction of windows with OTF > 0 was 0.084 to 0.167
in our setting. In more than four fifths of control cycles the fourth input was exactly zero, so the
two controllers were driven by identical observations for most of every episode. An ablation in that
regime cannot detect much, whatever the underlying mechanism.

The availability map makes the second mechanism quantitative. Availability rises monotonically with
flow and with window length. The two trade against each other: the 0.5 contour is crossed near
1500 veh/h at 20 s, near 3400 veh/h at 10 s, and only beyond 4800 veh/h at 5 s. A study that wants to
test whether OTF can help should therefore choose its operating point deliberately, not inherit it
from a simulator default.

## 5.3 A discrepancy worth reporting

At the flow equivalent of our CARLA setting, the SUMO map predicts an availability near 0.32, while
CARLA produced 0.084. The gap is explained by the lane-change model rather than by the OTF definition.
SUMO's LC2013 changes lanes to overtake slower traffic. CARLA's Traffic Manager, in a sparse scene
without congestion pressure, rarely does: over a 60 s probe the whole fleet completed two lane
changes, none of them across the ego lane. We therefore injected scripted cut-ins to obtain a usable
signal. This is a property of the simulator, and it must be stated whenever a simulated OTF rate is
compared with a measured one.

## 5.4 Practical implications

For a vehicle engineer the result is a boundary, not a rejection. OTF is cheap, explainable, and
sensor-agnostic, which makes it a reasonable diagnostic input and a reasonable input for
higher-level decisions such as lane-change readiness. It is not, on this evidence, a way to improve
low-level car-following inside a fixed search budget.

For a traffic engineer the map is the more useful artifact. It says where the signal exists. At
600 veh/h a 5 s window is zero 88% of the time; at 3600 veh/h the same window is non-zero half the
time. Any deployment that feeds OTF to a controller should therefore check its own operating point
before deployment.

## 5.5 Limitations

Six limitations bound the claims, and three of them are structural.

1. Power. With five seeds the exact paired test can return no value below 0.0625, while Holm
correction across four scenarios requires 0.0125. Superiority was therefore untestable by
construction, and our inference rests on equivalence.

2. Metric dependence. The primary metric takes the best valid candidate in each arm. The equal-K
sensitivity analysis equalizes the number of valid candidates and gives a mean of −1.07 against
+0.35 for the primary metric. The sign reverses. The direction of the effect estimate therefore
depends on how the search budget is accounted for, and both figures are reported.

3. Regime. Availability was 8% to 17%, far below the saturated region of the map. Conclusions do
not transfer to dense traffic or to longer windows.

4. Constructed traffic. OTF activation depends on scripted cut-ins placed by transform, not on
natural lane changes. The resulting events are more regular than real ones.

5. Platform. One map, one vehicle model, and a control rate of 20 Hz rather than the 100 Hz of the
original protocol.

6. No recorded trajectories. The availability map comes from SUMO, and the closed loop from CARLA.
Replay on recorded highway trajectories remains future work, and we do not claim external validity
beyond the two simulators.

## 5.6 Future work

Three extensions follow directly. Increasing seeds to twenty would make the exact test informative and
halve the interval widths. Moving the operating point into the upper region of the map would test
whether the null result belongs to OTF or to our regime. Raising density or lengthening the window
both work, and the map predicts availability above 0.5 there. Replaying
recorded trajectories with fixed neighbours would then test whether the simulated availability matches
real traffic. Two of these require only compute; the third requires data access.

<!-- END-MANUSCRIPT -->

---

## 写作元信息（不属于稿件）

| 项 | 内容 |
|---|---|
| 数字来源 | `audit/第一次组会/15-a1-full-results.md`（20 局）；相图 `13` §11 |
| 图表引用 | Fig.1（交通场景）/ Fig.2（相图）/ Table 1（逐场景三态）待编号 |
| 合规检查 | `node _check_manuscript.mjs <本文件>`（剥 HTML 注释后扫 em-dash/禁用词/overclaim/长句） |
| 待补 | Related Work 段、Section 2/3/4 正文、Fig.1 绘制 |

### 待核实引用（**目前未写进正文**，核实后再插）

| 线索 | 状态 |
|---|---|
| *Beyond "non-significant" results: why and how to test for practical equivalence*, **PNAS**, DOI `10.1073/pnas.2611548123` | **【需核实】作者、年份、卷期**——PNAS 官网与 Oxford ORA 均被 Cloudflare 401/403 拦截，**无法核实**。它将是"等价性优先于不显著"这一推断策略的最佳方法学引用；**核实前不得写入参考文献** |
| eLife 关于等价/优越性检验报告规范的指引（eLife 92311 之类） | **【需核实】** 同上，仅见二手片段 |
| 说明 | 正文 §5.1 关于"equivalence 是正向陈述、比'未拒绝'更强"的表述属标准统计常识，**暂不引文**；核实到 PNAS 那篇后再补一句带引用的支撑。 |

