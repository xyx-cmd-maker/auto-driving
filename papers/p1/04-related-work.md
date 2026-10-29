<!-- BEGIN-MANUSCRIPT -->

# 3. Related work

## 3.1 Traffic-flow descriptors as controller inputs

Car-following models describe the longitudinal response to a lead vehicle, and the classical families
differ in how much memory they carry. String-stability analysis then asks whether a perturbation
amplifies along a platoon (Ploeg et al., 2014). That line of work treats the lead vehicle as the
relevant input. Everything behind and beside the ego enters, if at all, through aggregate parameters
such as density or wave speed.

A second line feeds traffic-level information to the controller explicitly. One field experiment
showed that a small number of controlled vehicles can dissipate stop-and-go waves in the surrounding
flow (Stern et al., 2018). Cooperative schemes go further and share planned trajectories, solving a
joint optimization over a rolling horizon (Wang et al., 2023). Those methods work with rich per-vehicle
messages rather than one scalar, and they assume connectivity. Our question is narrower: whether one
scalar computed from unconnected traffic carries enough information to change a low-level command.

## 3.2 Overtaking frequency and social pressure

The OTF scalar comes from the behavior-decision literature. Huang et al. (2021a) defined it as the rate
at which surrounding vehicles cross the ego lane. They use it as the primary input to a long short-term
memory model that judges speed suitability, and they report 93 percent agreement in an on-road test. A
companion study embeds OTF in a deep deterministic policy gradient decision model, evaluated in four
simulated three-lane highway scenarios (Huang et al., 2021b). Both are evaluation or decision models, and
neither closes the loop. We do not reproduce them, and the dataset behind them is not available to us.

The idea that surrounding traffic exerts a pressure that can be summarized is older than OTF.
Social-force formulations describe the same intuition for pedestrians (Helbing and Molnár, 1995). That
formulation targets pedestrians, and we do not assume it transfers to vehicles. Our contribution is
not the notion of pressure but a closed-loop test of whether one particular scalarization of it
changes a control command.

## 3.3 Continuous-time and closed-form recurrent models

Liquid time-constant and closed-form continuous-time networks replace discrete recurrence with a
continuous ODE-like update and report large speedups over conventional recurrent cells (Hasani et al.,
2022). The claimed advantage is compute per step rather than sample efficiency. We use a CfC cell
precisely because it is cheap enough to evaluate twelve candidates per arm inside a 60 s episode. That
cost is what makes an equal-budget ablation affordable on a laptop GPU.

The same literature motivates our architecture choice. A pure ODE state integrates its input and
responds slowly, so a controller that relies on it alone cannot react to an instantaneous gap change.
We add a direct linear path from the observation to the command, and we report both parameter counts.

## 3.4 Physics-informed and structure-informed priors

A large body of work injects physical structure into learning. Physics-informed neural networks add a
residual of a governing equation to the loss (Antonelo et al., 2024). That approach requires an
equation whose residual can be evaluated, and it succeeds when the residual is meaningful.

OTF does not provide such a residual. It is a heuristic aggregate with no governing equation, so a
soft physics loss would not be well posed. We therefore treat it as an additional input and as an
inductive bias, and we describe it as structure-informed rather than physics-informed. The distinction
matters because it determines what evidence would count as success. A physics-informed claim can be
checked against the residual, whereas our claim can only be checked in closed loop.

## 3.5 What is missing

Three gaps follow from the above. Closed-loop evidence for OTF is absent, because the reported results
are classification accuracies. Equivalence is rarely reported, because ablation studies usually test
for a difference and stop when none is found. And the operating point is rarely characterized, because
availability of a traffic-level signal depends on density in a way that is easy to leave implicit. This
paper addresses the three together.

<!-- END-MANUSCRIPT -->

---

## References（6 条，全部 Crossref `verdict=OK`；投稿时转 IEEE 编号制）

| # | 文献 | DOI | 库内核验 |
|---|---|---|---|
| 1 | Ploeg J., van de Wouw N., Nijmeijer H. Lp string stability of cascaded systems: application to vehicle platooning. *IEEE Trans. Control Syst. Technol.*, 2014, 22(2): 786–793. | `10.1109/TCST.2013.2258346` | crossref, jaccard=1, OK |
| 2 | Stern R.E., Cui S., Delle Monache M.L., et al. Dissipation of stop-and-go waves via control of autonomous vehicles: field experiments. *Transp. Res. Part C*, 2018, 89: 205–221. | `10.1016/j.trc.2018.02.005` | crossref, jaccard=1, OK |
| 3 | Wang J., Zheng Y., Li K., Xu Q. DeeP-LCC: data-enabled predictive leading cruise control in mixed traffic flow. *IEEE Trans. Control Syst. Technol.*, 2023, 31(6): 2760–2776. | `10.1109/TCST.2023.3288636` | crossref, jaccard=1, OK |
| 4 | Hasani R., Lechner M., Amini A., et al. Closed-form continuous-time neural networks. *Nature Machine Intelligence*, 2022, 4(11): 992–1003. | `10.1038/s42256-022-00556-7` | crossref, jaccard=1, OK |
| 5 | Antonelo E.A., Camponogara E., Seman L.O., et al. Physics-informed neural nets for control of dynamical systems. *Neurocomputing*, 2024, 579: 127419. | `10.1016/j.neucom.2024.127419` | crossref, jaccard=1, OK |
| 6 | Helbing D., Molnár P. Social force model for pedestrian dynamics. *Phys. Rev. E*, 1995, 51(5): 4282–4286. | `10.1103/PhysRevE.51.4282` | crossref, jaccard=1, OK |
| — | Huang M. 基于超车频次的自动驾驶车辆行为决策研究. 吉林大学博士学位论文, 2023. | — | `sources/thesis-huang2023.pdf` 全文可 grep |

**填写说明（2026-10-18）**：6 个槽位全部由 `literature/library/P1-library.jsonl` 填入，
每条均带 `verification.verdict = OK`（Crossref 标题 Jaccard = 1）。**没有任何一条来自记忆。**
