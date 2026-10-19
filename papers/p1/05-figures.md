# P1 图表清单与图注（2026-10-18）

> 纪律：图注里的每个数字必须能指到 `results/` 或 `runs/` 的具体文件；限制必须写进图注，不只写正文。

## Figure 1: `figs/fig1_scenario.pdf`

**Overtaking pressure and its measurement.** **A**, three-lane highway with the ego vehicle (blue), the
lead vehicle, and vehicles in the adjacent lanes. The arrow marks one crossing of the ego lane, which
the counting rule scores as +1. The controller searches for a lead vehicle 150 m ahead in the ego lane,
and commanded speed is bounded at 30 m/s. **B**, the counting rule on a time–lane plane. A vehicle
entering the ego lane from an adjacent lane scores +1; a vehicle leaving it scores −1. Crossings are
counted inside a sliding window W, set to 5 s in the main experiment and 20 s in the supplementary
group. **C**, availability of the signal, computed in SUMO with the same OTF definition: the fraction of
sliding windows with OTF > 0 against traffic flow and window length, over three seeds. White contours
mark 0.25, 0.50 and 0.75. The hatched band marks the equivalent flow of the CARLA setting, estimated
from sixteen vehicles on a 420 m three-lane segment; the star marks the value measured there, 0.084 at
W = 5 s. The map describes where the signal exists. It is not offered as an explanation for the
closed-loop result, which Section 5.2 attributes to redundancy rather than to scarcity.

## Figure 2: `figs/fig2_availability_real.pdf`

**Availability in synthetic and recorded traffic.** **A**, the SUMO map of Fig. 1C with the CARLA
operating point. **B**, the same quantity at three window lengths for three sources. SUMO synthetic
traffic at 1800 to 2400 veh/h is drawn in blue. Recorded TGSIM traffic is drawn as orange squares: the
mean over ten runs, with the observed range as an error bar. Our CARLA closed loop is drawn as stars.
The closed-loop value at
W = 5 s is 0.084 from the main experiment and at W = 10 s is 0.167. At W = 20 s the supplementary
groups reach 0.334 in two scenarios and between 0.334 and 0.497 in the third, because lead-exit
produces crossings of the ego lane without any injection. The star is drawn at 0.334, the value shared
by two of the three scenarios. At a 5 s window the fractions are 0.39, 0.53 and 0.084.

**Three limitations of this panel, stated here because they bound its interpretation.**
1. The TGSIM horizontal placement is an **estimate** (unique vehicles divided by run duration). The
   public trajectory file uses per-run normalised coordinates spanning a fixed box, so absolute
   station flow cannot be recomputed from it without the centreline geometry files.
2. The error bars are the **minimum and maximum across ten runs**, not a confidence interval.
3. The three sources differ in density. The comparison therefore shows that recorded traffic exposes
   the controller to a non-zero OTF far more often than our closed loop does. It does not isolate
   density from lane-change behaviour as the cause.

## Table 1 / Table 2: see `audit/第一次组会/15-a1-full-results.md`

Intervals are Student t intervals on five paired differences. The exact p-value comes from enumerating
all 32 sign assignments. TOST uses a margin of 10% of the off-arm mean and is judged on the 95%
interval, as registered; the 90% interval is reported alongside because the two criteria disagree for
one scenario.
