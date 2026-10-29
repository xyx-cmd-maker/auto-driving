<!-- BEGIN-MANUSCRIPT -->

# 1. Introduction

On a multi-lane highway, a driver's longitudinal decision is shaped by what happens in the adjacent
lanes. A vehicle that closes on a slower lead may either slow down or move over, and the choice
depends on how much lateral opportunity the surrounding traffic offers. Over a few seconds these
individual choices aggregate into a measurable rate at which vehicles cross a given lane.

Huang et al. (2021a) proposed to summarize this aggregate as the overtaking frequency (OTF): the number of
lane crossings observed in a sliding window around the ego vehicle, divided by the window length.
OTF is attractive for three reasons. It is a single scalar. It is defined on traffic rather than on a
particular sensor suite. And it can be estimated from radar and camera streams that production
vehicles already carry, so it adds no sensing cost.

Evidence for OTF so far comes from evaluation and decision models rather than from control. One line
feeds it to a long short-term memory network that judges whether the current speed suits the traffic
state, and reports 93 percent agreement in an on-road test (Huang et al., 2021a). A second line embeds
it in a deep deterministic policy gradient decision model evaluated in four simulated three-lane
highway scenarios (Huang et al., 2021b). Neither reports how often the scalar is non-zero. Evaluation
and control ask different questions. A feature can improve an offline judgement and still add nothing
to a feedback loop that already observes gap and relative speed. Neither line closes the loop.

We test it directly. We treat OTF as a fourth input to a closed-form continuous-time (CfC) controller
and compare it against an otherwise identical controller that sees only lead gap, relative speed, and
ego speed. Both arms share one twelve-candidate search budget, the same five seeds, and the same
traffic stream, so any difference must come from the fourth input.

A scalar can only help if it is non-zero often enough, so we measured availability before measuring
effect. In a three-lane SUMO highway, the fraction of 5 s windows with OTF > 0 rises from 0.12 at
600 veh/h to 0.56 at 4800 veh/h. A 20 s window reaches 0.93 at 3600 veh/h. In the CARLA setting used
for the closed-loop experiment, with sixteen mixed vehicles, the measured fraction was 0.084 to 0.167.
That setting therefore sits in the low-information regime. We do not treat that as an excuse for the
result. Section 5.2 reports a supplementary group that raises availability fourfold and tests whether
scarcity is what limits the conclusion.

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

## 5.2 Why no gain

The result is consistent with redundancy at the controller input, and we tested that reading directly.
We removed relative speed from the observation, so that both arms saw only gap and ego speed. The
off-arm cost moved by 0.14, from 30.82 with ten runs to 30.96 with five, and the two ranges overlap
almost exactly. Removing the input did not make OTF useful either: in the same five runs the paired
difference between the two arms was +1.26, with a 95 percent interval of -2.17 to +4.68 and an exact
p of 0.375. The recurrent state therefore rebuilds the missing rate from the history of the gap.

That matters for the interpretation. A controller that can reconstruct one of its own inputs has little
left to gain from a fourth scalar that summarizes vehicles other than the lead. OTF describes traffic
that does not constrain the ego at the moment of decision. When those vehicles are unconstrained, their
aggregate adds nothing to the instantaneous command.

Signal scarcity is the obvious competing explanation, and we tested it rather than assuming it. In the
main experiment the fraction of control cycles with a non-zero net crossing was 0.084 to 0.168, so
the fourth input was zero for most of every episode. We therefore raised that fraction fourfold in every scenario, by widening the
window to 20 s while holding everything else fixed. Availability rose to 0.334 in two scenarios and to
between 0.334 and 0.497 in the third.

No scenario sharpened. The interval width grew rather than shrank in all three: 5.90 to 6.83, 5.59 to
6.73, and 3.84 to 4.92. A second supplementary group tripled the background traffic without moving
availability, and also left the conclusion unchanged.

A window scan locates the cause more precisely. With a fixed number of seeds the interval width is
proportional to the sample standard deviation, so we report that quantity directly. For the lead-brake
scenario, run with ten seeds per window, the standard deviation is 1.72 at a 5 s window, 1.81 at 10 s,
and 1.93 at 20 s. The ordering is monotone, and no interior optimum appears.

The increments are small, however: 0.09 and 0.12, against a sampling error of about 0.4 on each standard
deviation at ten seeds. The three values are therefore not separated. We report the ordering and do not
claim a trend from it. The other two scenarios were run with five seeds only, and their ordering was
consistent with this one; with five seeds their standard deviations are inflated by roughly thirty
percent, so we do not use them as evidence.

Two mechanisms would both produce that monotone rise, and five seeds cannot separate them. A long window
spans fewer independent windows per episode. A long window also accumulates more crossings per window,
and a count with a larger mean carries a larger variance. We report the monotone rise as a fact and
leave the decomposition open.

We therefore read scarcity as a description of the regime rather than as the cause of the null. Had
availability been binding, a fourfold increase should have sharpened the estimate in at least one
scenario. It sharpened none.

The availability map still explains where the signal exists. Availability rises monotonically with flow
and with window length. The two trade against each other: the 0.5 contour is crossed near 1500 veh/h at
20 s, near 3400 veh/h at 10 s, and only beyond 4800 veh/h at 5 s. That map is what told us which
manipulation to try, and it is what a future study should use to choose an operating point deliberately
rather than inherit one from a simulator default.

## 5.3 A discrepancy worth reporting

At the flow equivalent of our CARLA setting, about 1400 vehicles per hour, the SUMO map predicts an
availability near 0.32 when interpolated between its 1200 and 1800 rows, while CARLA produced 0.084. Recorded traffic sits higher still: on the public TGSIM corpus, at an estimated
1800 to 2400 vehicles per hour, the measured fraction at a 5 s window was 0.53, averaged over ten runs. The gap is explained by
the lane-change model rather than by the OTF definition.
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
before deployment. The map locates the signal. It is not offered as an explanation for the closed-loop
result, which Section 5.2 attributes to redundancy.

## 5.5 Limitations

Six limitations bound the claims, and three of them are structural.

1. Power. With five seeds the exact paired test can return no value below 0.0625, while Holm
correction across four scenarios requires 0.0125. Superiority was therefore untestable by
construction, and our inference rests on equivalence.

2. Metric dependence. The primary metric takes the best valid candidate in each arm. The equal-K
sensitivity analysis equalizes the number of valid candidates and gives a mean of −1.07 against
+0.35 for the primary metric. The sign reverses. The direction of the effect estimate therefore
depends on how the search budget is accounted for, and both figures are reported.

3. Regime. Availability was 8% to 17% in the main experiment, far below the saturated region of the
map. One supplementary group reached 33%, and its estimate was no sharper. Even that level sits below
recorded traffic, where the same window gives 53%. Conclusions do not transfer to dense traffic.

4. Constructed traffic. OTF activation depends on scripted cut-ins placed by transform, not on
natural lane changes. The resulting events are more regular than real ones.

5. Platform. One map, one vehicle model, and a control rate of 25 Hz rather than the 100 Hz of the
original protocol. The controller under test is also modest. A tuned PID follows the lead with 17 m
of root-mean-square error against 85 m here, on all five seeds. Its composite cost is nevertheless 1.3
to 2.1 times ours across three scenarios, because a direct speed target trades comfort for tracking.
The ablation therefore tests the fourth input inside a weak carrier, not the best achievable controller.

6. Real trajectories, open loop only. The availability map comes from SUMO, and the closed loop from
CARLA. We also measured availability on the public TGSIM corpus, a US public-domain trajectory dataset
of a four-lane highway carrying three SAE L1 ACC vehicles per run, and obtained 0.53 at a 5 s window.
That comparison is open loop. No controller was run against the recorded trajectories, and we do not
claim closed-loop external validity.

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

