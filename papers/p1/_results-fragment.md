# 4. Results

## 4.1 Validity checks

All twenty paired runs completed. The execution fingerprint is identical across runs: 60 s episodes,
sixteen traffic vehicles in the main experiment, 50 Hz simulation, 20 Hz control, 24 hidden units, and
twelve candidate controllers per arm. The three runtime guards reported no empty episodes, no actor
leaks, and no deadlocked episodes.

The treatment variable was active in every run. The fraction of control cycles with OTF > 0 was 0.084
in sixteen runs and 0.167 in four. Neither arm collided in any run, so collision counts are zero
throughout and we do not use them as evidence of a difference.

## 4.2 Primary endpoint

Table 1 reports the paired difference in composite driving cost for each scenario, with the
pre-registered equivalence margin of 10% of the off-arm mean.

**Table 1.** Paired difference in composite cost (negative favours the OTF arm).

| Scenario | n | Mean Δ | off mean | 95% CI | 90% CI | exact p | TOST p | Conclusion |
|---|---|---|---|---|---|---|---|---|
| none | 5 | +0.256 | 30.481 | [−2.321, +2.832] | [−1.723, +2.234] | 0.8125 | 0.0198 | equivalent |
| cutin | 5 | +0.326 | 30.314 | [−2.467, +3.119] | [−1.818, +2.471] | 0.8750 | 0.0273 | inconclusive |
| lead-brake | 5 | +0.858 | 30.947 | [−2.092, +3.808] | [−1.407, +3.123] | 0.4375 | 0.0515 | inconclusive |
| lead-exit | 5 | −0.051 | 30.623 | [−1.968, +1.867] | [−1.523, +1.422] | 1.0000 | 0.0060 | equivalent |

Two scenarios, no lead vehicle and lead exit, have both interval bounds inside the margin under the
pre-registered 95% criterion. The cutin scenario would also qualify under the conventional 90%
interval, where its upper bound is +2.471 against a margin of 3.031. The lead-brake scenario does not
qualify under either criterion. We report the stricter criterion as primary.

The exact sign-flip test returns no value below 0.4375 for this endpoint. Neither scenario reaches
significance, and Section 4.5 explains why that was impossible by design rather than by data.

## 4.3 Secondary endpoints

**Table 2.** Paired differences in the two performance endpoints.

| Scenario | Δ following RMSE (m) | 95% CI | TOST p | Δ accel. integral | 95% CI | TOST p |
|---|---|---|---|---|---|---|
| none | −4.361 | [−26.629, +17.908] | 0.3184 | +34.47 | [−6.004, +74.934] | 0.5786 |
| cutin | −4.767 | [−27.421, +17.888] | 0.3432 | +40.13 | [−13.938, +94.190] | 0.6637 |
| lead-brake | −0.761 | [−18.849, +17.327] | 0.1484 | +46.89 | [−49.977, +143.762] | 0.6435 |
| lead-exit | −2.317 | [−14.851, +10.217] | 0.1161 | +8.98 | [−79.179, +97.131] | 0.2630 |

All eight tests are inconclusive. The point estimates have consistent signs across scenarios: following
error is lower in the OTF arm in all four, and the acceleration-squared integral is higher in all four,
with off-arm means between 310 and 331. The intervals are wide enough that neither pattern supports an
inference, and we report the signs only as directions.

## 4.4 Sensitivity to the search budget

The primary metric takes the best valid candidate in each arm. The number of valid candidates differs
between arms in several runs, so we repeated the comparison with K fixed at the smaller of the two
counts and the top K averaged. Under this equal-K rule the mean difference is −1.066, against +0.347
under the primary metric. The sign reverses.

The reversal is mechanical. Equalizing K discards good candidates from whichever arm ran more, and in
these runs that arm was usually the off arm. We report both figures because the direction of the effect
estimate depends on which accounting of the budget a reader accepts.

## 4.5 Multiplicity and power

Each scenario contributes one test per endpoint, and we correct within endpoint families using Holm's
method. No test survives correction at alpha = 0.05.

The reason is structural. The exact sign-flip test enumerates all 32 sign assignments with five seeds,
so its smallest attainable two-sided p-value is 0.0625. Holm correction across four scenarios requires
0.0125 for the smallest p-value. No dataset of this size could have produced a significant result.

The invalid-candidate rate carries the same caveat. Between 25% and 67% of the twelve candidates per arm
failed the 20 m displacement criterion, and the rate was not consistently higher in either arm (off arm
mean 48%, on arm 47%). Training difficulty therefore does not separate the arms in this dataset.

<!-- END-MANUSCRIPT -->

---

## 图注（作图时逐条核过：数字来自结果 JSON，参数来自代码）

**Figure 1.** Overtaking pressure and its measurement. **A**, three-lane highway with the ego vehicle
(blue), the lead vehicle, and vehicles in the adjacent lanes. The arrow marks one crossing of the ego
lane, which the counting rule scores as +1. The front-vehicle search used by the controller extends
150 m ahead in the ego lane, and commanded speed is bounded at 30 m/s. **B**, the counting rule on a
time–lane plane. A vehicle entering the ego lane from an adjacent lane scores +1; a vehicle leaving it
scores −1. Crossings are counted inside a sliding window W, which is 5 s in the main experiment and
20 s in the supplementary group. **C**, availability of the signal, measured in SUMO with the same OTF
definition: the fraction of sliding windows with OTF > 0 as a function of traffic flow and window
length, over three seeds. White contours mark 0.25, 0.50 and 0.75. The hatched band marks the
equivalent flow of the CARLA setting, estimated from sixteen vehicles on a 420 m three-lane segment;
the star marks the value measured there, 0.084 at W = 5 s.

**Figure 2.** Same data as panel C, drawn for a single-column layout with window length as separate
series. Values are means over three SUMO seeds; the shaded band is not shown because the seed spread is
below 0.02 in every cell.

**Table 1 and Table 2.** Intervals are Student t intervals on five paired differences. The exact p-value
comes from enumerating all 32 sign assignments. TOST uses a margin of 10% of the off-arm mean.
Equivalence is declared when the 95% interval lies inside the margin. The 90% interval, which
corresponds to the conventional two one-sided tests at alpha = 0.05, is reported alongside.
