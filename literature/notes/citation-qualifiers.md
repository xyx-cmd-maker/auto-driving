# P1 核心六篇：`citation_qualifier` 单行字段汇总（层 3 核验用）

> 生成：2026-10-02 ｜ 用途：`citation-and-related-work` **层 3（主张一致性）** 的限定语基准，以及 `paper-experiment-analyzer` 断言强度校准的输入。
> 契约：本文件每条的 `citation_qualifier:` 为**逐字**取自对应精读笔记的机器可读字段；**任何改写都会让"这句话到底在什么条件下成立"失去唯一答案**（`citation-and-related-work` §2 层 3 硬规则）。
> 笔记位置：`literature/notes/<id>.md`（六份均由 `deep-paper-reader` 规范产出，包含作用域声明、主张—证据台账（内部等级 + 外部复现两列）、方法可复现性清单、关键数字表、统计旗标、缺失信息 ≥3 条、红队三条、限制 ≥3 条）。

---

## 速查：六篇的"引用时必须带上"的限定语（结论表）

| # | 论文 | 一句话限定语（**完整单行见下**） | 对 P1 的直接后果 |
|---|---|---|---|
| #1 | CfC (NMI 2022) | 5 个任务；**真车闭环零量化指标**；硬件未报告；参数量只有车道保持模型 | P1 **不能**把 CfC 的建模优势当控制优势；`<500 KB` 须按 **230,828** 参数算（fp32 ≈ 902 KiB 超标） |
| #7 | PINC (Neurocomputing 2024) | 两个低维 ODE 基准、**零实测数据**、单次运行、基线是"神谕" NMPC | PINC 是**模型**不是控制器；P1 不宜自称 "physics-informed"，宜用 structure-/prior-informed |
| #15 | Human-like CF (TR-C 2018) | SH-NDS 2,000 段/827 min；**单次训练、无种子无 CI**；开环回放 | "类人"被完全操作化为轨迹 RMSPE；图 7 的 "lowest SD on spacing" **不成立**（矢量反算） |
| #33 | Lp String Stability (TCST 2014) | **实车** 6 车 CACC；判据**仅对 LTI 成立**；关键数值来自**单次实验** | 判据**不能**直接套到非线性 CfC；RMSE 小 ≠ 弦稳定，须报逐车误差传播曲线 |
| #43 | Stop-and-go dissipation (TR-C 2018) | 单车道封闭环道 21–22 辆、**恰好 1 辆受控**、每条件**单次运行**、无 CI | 只能作**动机锚点**；其百分比**禁止**进入 P1 性能对比表；IRB/里程/接管分母**六项全无** |
| #45 | DeeP-LCC (TCST 2023) | OVM 单车道混行 n=8 + m=2 CAV；数据是**仿真生成的 40 s 轨迹**；**无弦稳定性结果** | 不得写"需采集足量混行轨迹"；无任何设置显示它优于 MPC |

---

## 逐条（逐字字段）

### #1 CfC — Closed-form continuous-time neural networks
`文献`：Hasani R, Lechner M, Amini A, Liebenwein L, Ray A, Tschaikowski M, Teschl G, Rus D. Nature Machine Intelligence 2022;4(11):992–1003. DOI 10.1038/s42256-022-00556-7
`笔记`：`notes/p01-cfc-nmi2022.md` ｜ `全文来源`：arXiv HTML 2106.13898（**未核 NMI 正式版**）

citation_qualifier: 5 settings (bit-stream XOR with equidistant+event-based encodings; PhysioNet 2012 8000 ICU patients; IMDB 25k/25k; MuJoCo Walker2d-v2; real-vehicle lane keeping on a Lexus RX450H over 1 km private road at 30 km/hr), accuracy/error as mean ± SD with n=5 but no seeds, no CI and no significance tests, speed as single per-epoch values with no hardware/precision/batch size/repetition reported (only 3x–220x is traceable although the Abstract claims one to five orders of magnitude), most baseline numbers copied from [7]/[9]/[40]/[42]/[44] rather than re-run, parameter counts available only for the lane-keeping model (CfC 4,184 RNN-only vs 230,828 including the CNN head), all figures/tables cited from the arXiv HTML version 2106.13898 and not verified against the published Nature Machine Intelligence 2022 version, and no closed-loop control performance metric is reported for the real-vehicle experiment

### #7 PINC — Physics-informed neural nets for control of dynamical systems
`文献`：Antonelo EA, Camponogara E, Seman LO, Jordanou JP, de Souza ER, Hübner JF. Neurocomputing 2024;579:127419. DOI 10.1016/j.neucom.2024.127419
`笔记`：`notes/p07-pinn-ctrl-neucom2024.md` ｜ `全文来源`：arXiv HTML 2104.02556（**arXiv 版 48 条参考文献 vs VoR 57 条，未核 VoR**）

citation_qualifier: two low-dimensional ODE benchmarks only (Van der Pol oscillator, 2-state; Johansson four-tank, 4-state/2-input, non-minimum-phase parameters), plant simulated by RK4 of the very same ODE used for physics-informed training with zero measured data, PINC used as MPC prediction model vs oracle ODE/RK NMPC with identical Q=10I, R=I, N1=1, N2=5, Nu=N2, RMSE/IAE from a single run per system (no seeds, no variance, no significance or equivalence test), +/- reported only for wall-clock over 10 runs with SD/SE undefined, speed-up 23.3% on four-tank only (2.6% on Van der Pol, within run-to-run scatter) while the discussion's "up to 30%" conflicts with Table 1, all values from the arXiv 2104.02556 HTML version rather than the Neurocomputing 579:127419 VoR

### #15 Human-like car-following with DRL
`文献`：Zhu M, Wang X, Wang Y. Transportation Research Part C 2018;97:348–368. DOI 10.1016/j.trc.2018.10.024
`笔记`：`notes/p15-humanlike-cf-trc2018.md` ｜ `全文来源`：arXiv PDF 1901.00569

citation_qualifier: SH-NDS（2015 上海自然驾驶研究，限速封闭快速路/高速、单车道跟驰、纵向动力学）20 名驾驶员 × 100 个跟驰时段 = 2,000 段 / 827 min，逐驾驶员标定、70/30 划分、两级验证（intra-driver 与 inter-driver 20×20）；最高结果 DDPGvRT 的 18%/5% 指 intra-driver 验证 RMSPE（inter-driver 为 21.94%/6.66%，表 4 的 0.1984 为同指标分数口径 = 19.84%）；单一训练运行、未报告随机种子与运行间方差、无任何显著性检验或置信区间，且最佳 agent 以"训练+测试误差之和最小"选出（含测试集信息）；结果为开环回放 + 运动学质点模型仿真，非实车、非闭环

### #33 Lp String Stability of Cascaded Systems
`文献`：Ploeg J, van de Wouw N, Nijmeijer H. IEEE Transactions on Control Systems Technology 2014;22(2):786–793. DOI 10.1109/TCST.2013.2258346
`笔记`：`notes/p33-lpstring-tcst2014.md` ｜ `全文来源`：TU/e 机构库 accepted manuscript PDF

citation_qualifier: 6-vehicle homogeneous platoon (real passenger cars, CACC over IEEE 802.11p at 10 Hz; linear LTI platoon model with tau=0.1 s, phi=0.2 s, theta~0.15 s, kp=0.2/kd=0.7/kdd=0, constant-time-headway spacing policy d_r,i=r_i+h*v_i, one-vehicle look-ahead unidirectional topology, no uncertainty modelling) — NOT simulation; Theorem 1/2 conditions apply only to linear unidirectionally interconnected systems, and the h=0.7 s / 0.3 s / 15.5 s / 8.5 s figures come from a SINGLE experimental run with no repetitions, no variance and no confidence intervals reported (0.3 s is a model prediction only, never tested).

### #43 Dissipation of stop-and-go waves via control of autonomous vehicles
`文献`：Stern RE 等 14 人. Transportation Research Part C 2018;89:205–221. DOI 10.1016/j.trc.2018.02.005
`笔记`：`notes/p43-dissipation-trc2018.md` ｜ `全文来源`：arXiv HTML 1705.01693

citation_qualifier: single-lane closed circular test track (lane-centre radius 41.4 m, 260 m circumference, no lane changes/merges/intersections), 21 vehicles (Exp A, B) or 22 vehicles (Exp C) at ~81-85 veh/km, exactly ONE vehicle under wave-damping control (4.5-4.8% of the fleet; the abstract's "less than 5%" is extrapolated from a single actuator, not a penetration sweep); 3 experiments - A FollowerStopper with an externally supplied set point, B trained human driver reproducing it, C PI-with-saturation fully automatic using a 38 s self-average - ONE RUN EACH, no repetition, no randomisation of control on/off order; no CI/SE/significance test anywhere, Table 3's "control active" values are the post-hoc BEST interval, wave onset uses a 2.5 m/s instantaneous velocity-std-dev threshold while tables report interval-average std dev, braking threshold tau is recomputed per experiment so braking rates are not comparable across experiments, throughput is defined as density times mean speed (not an independent count); drivers were university employees with safe-driver training, a trained driver held the steering wheel at all times, but NO IRB/consent/permit/insurance statement and NO mileage, exposure or takeover/intervention denominator is reported

### #45 DeeP-LCC
`文献`：**Wang J, Zheng Y, Li K, Xu Q**（⚠ 本次核验更正：不是 8 作者串）. IEEE Transactions on Control Systems Technology 2023;31(6):2760–2776. DOI 10.1109/TCST.2023.3288636
`笔记`：`notes/p45-deeplcc-tcst2023.md` ｜ `全文来源`：arXiv HTML 2203.10639

citation_qualifier: OVM single-lane pure-longitudinal mixed traffic, n=8 vehicles behind 1 head vehicle with m=2 CAVs at S={3,6} (=25% CAV penetration using denominator n=8, excluding the head vehicle; 22.2% if the head vehicle is counted), simulation-only with no vehicle/hardware test in this paper (the referenced real-world miniature experiments are a separate follow-up [47]), pre-collected data = 1 simulated trajectory of T=800 samples at dt=0.05 s (=40 s; theoretical lower bound 257 samples = 12.85 s) generated by an OVM pre-designed CAV controller with uniform noise and used for ALL experiments, 100 trajectories used only for the Experiment A cost statistics, single equilibrium v*=15 m/s during data collection whereas the simulated equilibrium is time-varying under the unverified assumption that HDV behaviour is similar across equilibria, performance numbers are single-run or mean-only with NO significance test, NO seeds and NO confidence intervals (only Fig. 4 reports mean +/- SD), the reported SDs differ by ~25.7x between MPC and DeeP-LCC, baselines are all-HDV (OVM) and a self-implemented output-feedback MPC only (no ACC/CACC/CCC/LCC baseline), the 'up to X%' values are per-Phase maxima over the NEDC phases without multiplicity correction, the 'collision-free' claim holds only conditional on constraint feasibility because recursive feasibility is explicitly left to future work, and NO string-stability result is reported.

---

## 使用规则（写入稿件前必做）

1. **逐字引用**：稿中每处引用上述六篇的句子，其限定语必须能逐字回到本文件；缺项要补，冲突以本文件为准并记录分歧。
2. **禁止删除限定语**：目标 venue 要求精简时，把限定语前移或在首次提及时交代，**不得删除**（限定语是方法学事实，不是文风）。
3. **不得把 C/D 级断言写进 Abstract/Conclusion**：六篇中 #1（CfC 控制优势）、#7（物理项降数据需求）、#15（类人）、#45（优于 MPC）在精读台账里均为 C_int 或 D_int 级，P1 引用时措辞不得超过该等级。
4. **待补动作**：#1 与 #7 的笔记基于 arXiv 版，**写入稿件前须取正式版（NMI / Neurocomputing VoR）逐条复核表号与数值**；本文件已把该缺口写进各自限定语末尾。
5. **外部复现列一律为"未检"**：本次未做引文方向检索；若要升 A 级，须按 `deep-paper-reader` §3.1.1 的核验动作补做（OpenAlex `cites:` 展开，额度 00:00 UTC 重置后）。
