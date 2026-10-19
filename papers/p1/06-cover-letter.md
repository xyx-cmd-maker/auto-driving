<!-- BEGIN-MANUSCRIPT -->

# Cover letter

Dear Editor-in-Chief,

We submit the manuscript "Overtaking Pressure on Multi-Lane Highways as a Control Input for
Continuous-Time Car-Following" for consideration in *IEEE Transactions on Intelligent Vehicles*.

The manuscript asks a narrow question with a pre-registered answer. A scalar that summarizes how often
neighbouring vehicles cross the ego lane has been reported to improve classification accuracy. Whether it
helps a closed-loop controller had not been tested. We test it by ablating a fourth input to a
closed-form continuous-time controller while holding the search budget, the seeds, and the traffic fixed.

Across four highway scenarios with five seeds each, two are statistically equivalent on composite cost
within a pre-registered 10% margin, and two are inconclusive. No endpoint shows a difference, and the
interval widths are reported in full. We then report two further steps that a reader would otherwise
ask for. First, we measure how often the scalar is non-zero, in a SUMO map and in the public TGSIM
trajectory corpus, and locate our operating point in the sparse region of that map. Second, we
manipulate availability directly in three scenarios and show that a fourfold increase in informative
control cycles sharpens none of the estimates.

We read the result as evidence that an aggregate traffic-pressure scalar buys interpretability at no
additional sensing cost, not closed-loop performance. The manuscript states this limit explicitly, and
it reports the equal-K sensitivity analysis that reverses the sign of the effect estimate. It also
states why superiority was untestable by construction: with five seeds the exact paired test cannot
reach significance after multiplicity correction.

We believe the work fits *IEEE Transactions on Intelligent Vehicles* because it concerns a vehicle-level
decision input, it uses a real public trajectory corpus for an open-loop check, and its contribution is
a boundary condition that other groups can reuse when deciding whether to add a traffic-level signal.

The manuscript is original, is not under consideration elsewhere, and all authors have approved the
submission. The authors declare no competing interests. Data and code are available as described in the
manuscript; the TGSIM corpus is public domain, and we redistribute none of it.

Yours sincerely,

Xia Yuxuan (first author) and Huang Mengyuan (corresponding author)
Shenzhen Polytechnic University

<!-- END-MANUSCRIPT -->

---

## 起草说明（不属于投稿信）

| 项 | 状态 |
|---|---|
| 数字来源 | 摘要与 `audit/第一次组会/15`–`19`；**未引入任何新数字** |
| 合规 | `node _check_manuscript.mjs papers/p1/06-cover-letter.md`（跑过：见下） |
| 待补 | 投稿系统里的 suggested reviewers（需真实姓名与单位，**不得编造**） |
| 待核 | T-IV 现任主编姓名（**未联网核实，故用 "Dear Editor-in-Chief"**，核实后可替换） |
