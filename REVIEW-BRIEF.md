# 外审说明（单文件版）

| 项 | 内容 |
|---|---|
| **稿件** | *When Is Overtaking Frequency Informative? A Pre-Registered Closed-Loop Ablation and an Availability Map* |
| **PDF** | `papers/p1/manuscript.pdf` —— 8 页，IEEEtran 双栏，参考文献 7 条 |
| **状态** | **尚未投稿**（目标 IEEE T-IV） |
| **仓库** | https://github.com/xyx-cmd-maker/auto-driving |
| **审稿人** | **团队内部成员**：仓库内一切（含 `audit/` 内部策略、`AGENTS*.md` 纪律文件）对你开放，不必回避 |
| **日期** | 2026-10-29 |

---

## 0. English summary

A **pre-submission** manuscript shared for internal review before submission to IEEE T-IV. It reports a **pre-registered closed-loop ablation** of a traffic-pressure scalar (overtaking frequency, OTF) as a fourth input to a continuous-time neural car-following controller, plus a **measured availability map** of that scalar in SUMO, in the public TGSIM corpus, and in our own closed loop. The headline is a **null/equivalence** result: two of four scenarios are statistically equivalent within a pre-registered 10 % margin; two are inconclusive. We ask for a **hostile methodological read**: the paper's only defence is design discipline, so tell us whether that defence holds.

---

## 1. 一句话结论与三条贡献

> 我们先测这个交通标量**到底存不存在**，再做消融；在它稀疏的区间里，加上它没有可分辨的性能差异。

| # | 贡献 | 强度 | 一句话证据 |
|---|---|---|---|
| C1 | **可用性测量**：真实交通 53 % 时间非零，我们闭环只有 8.4 %（约 1/6） | 强 | TGSIM 开环 + 闭环仿真 |
| C2 | **预注册等价性消融**：四场景 20 局，2/4 等价（TOST p=0.020、0.006），2/4 未定 | 强（设计） | 同预算、同种子、同交通 |
| C3 | **机制证据**：删掉观测里的相对速度，代价仅 0.14 | 中 | 30.82 → 30.96 |

**卖点不是性能，是「测量 + 不撒谎的统计协议」。**

---

## 2. 关键数字（一张表看完）

| 量 | 值 | 出处 |
|---|---|---|
| 真实交通 OTF 非零比例 | **0.53**（TGSIM，估 1800–2400 veh/h） | `results/p1/otf_real_tgsim_s1.json` |
| SUMO 合成（同流量段） | **0.39** | 同上 |
| 我们闭环 | **0.084** | `audit/第一次组会/15-a1-full-results.md` |
| 可用性随密度 | 0.12（600 veh/h）→ **0.56**（4800 veh/h） | `results/p1/otf_density_sweep_sumo_s1-2-3_fine.json` |
| 操纵检验 Φ（窗口 5/10/20 s） | **0.084 / 0.167 / 0.334**，组内零方差 | `audit/第一次组会/17-three-scenario-highinfo.md` |
| 主实验 Δcost（none/cutin/brake/exit） | **+0.256 / +0.326 / +0.858 / −0.051** | `15-a1-full-results.md` |
| 等价判定 | none 与 lead-exit **等价**；另两个**未定** | 同上（含双 CI） |
| 窗口扫描 SD（n=10） | **1.718 / 1.809 / 1.926**，增量 0.09/0.12 小于抽样误差 ≈0.4 → **不可区分** | `18-window-scan.md` §n10 |
| 删 Δv 的代价 | off 臂 30.82（10 局）→ **30.96**（5 局），差 **+0.14** | `20-strategy-after-downgrade.md` §6 |

> 两处我们**刻意压低**的措辞：不写“OTF 无用”，写“**不可分辨**”；不写“真实交通验证”，写“**recorded traffic**”（仅开环）。

---

## 3. 一分钟验数（请务必跑一次）

```powershell
py -3.12 scripts/verify_from_published_cases.py
```

**预期输出（2026-10-29 实测，exit=0）**：

```
  窗口           n    Δcost 均值  Δcost SD
  main        10      +0.409     1.718
  window10    10      +0.587     1.809
  window20    10      +0.558     1.926
  机制检验：有 Δv n=10 均值 30.82 ｜ 无 Δv n=5 均值 30.96 ｜ 差 +0.14
  四场景：none +0.256 ｜ cutin +0.326 ｜ lead-brake +0.409 ｜ lead-exit −0.051
```

数据在 `results/p1/cases/`（**60 个逐局 JSON，575 KB，已脱敏**：无本地路径、无用户名、无邮箱）。
说明：`main/` 的 lead-brake 有 10 个种子（2026-10-19 补到 n=10），其余场景各 5 个；Table I 用 seeds 0–4，窗口标准差那一节用 n=10。

**若任何一位数与上面不符，说明数据与稿件不一致——请直接告知，这比文字意见更重要。**

---

## 4. 先读这五份（比稿子更直白）

1. `audit/第一次组会/10-a1-protocol-freeze.md` —— 收数据前冻结的 margin / α / 判定规则（评统计必读）
2. `audit/第一次组会/20-strategy-after-downgrade.md` —— 我们自写的弱点清单 + **改投 T-ITS 的备选路线**
3. `audit/第一次组会/15-a1-full-results.md` —— 全量结果（双 CI、TOST、功效分析）
4. `audit/第一次组会/18-window-scan.md` —— 窗口扫描，含**我们自己推翻自己**的那一版
5. `audit/第三次组会/组会汇报-分批计划-2026-10-28.md` —— 汇报节奏与“要老师拍板的三件事”

**审稿意见不必照顾我们的面子。**

---

## 5. 我们已知的七条弱点（先说，免得你重复发现）

1. **这是负结果**，全部防御来自设计纪律，没有正效应支撑。
2. **n=5 的功效上限**：符号翻转检验最小双侧 p = 0.0625，Holm 校正后需 ≤0.0125 → **数学上不可能显著**，所以我们改主张等价。
3. **单地图、单车型、单控制器架构**（CARLA Town04 + Model 3 + CfC），外部效度未验证。
4. **OTF 由脚本注入**（每 4 s 一次定向切入），非背景交通自然产生；有阴性对照（背景车 +60 % 不改变 Φ），但仍是弱点。
5. **控制频率 20 Hz**，不是 100 Hz（主机限制）。
6. **真实数据只做开环**（TGSIM 无闭环接口），不能称“实车验证”。
7. **C3 只在一个场景**：只能证明“代价不敏感”，不等于“重建 Δv”被直接观测。

---

## 6. 请重点攻击的八个问题

1. **“测可用性”这个动作够不够撑起一篇 T-IV**？还是审稿人会当成“没做出来”的包装？
2. **margin 取偏离臂均值的 10 %**，是否可辩护？有没有更标准的做法？
3. **2/4 未定的两个场景**：报“未定”，还是扩种子到 20 再判（约 4 h/场景）？
4. **C3 的因果性**：+0.14 能支撑“控制器重建了 Δv”，还是只能说“代价不敏感”？
5. **OTF 注入**是否构成“操纵非自然现象”，削弱外部效度？
6. **0.084 vs 0.53**：真实数据流量是估计值，这个对比可信度几何？
7. **摘要第 2 句**（“rarely measured before it is ablated”）是否属于对文献的强断言？我们只核了 7 条引用。
8. **若你是审稿人，Major Revision 还是 Reject？** 一句话理由即可。

---

## 7. 边界

- **未投稿**：未向任何期刊提交；仓库含内部过程材料，**仅团队内使用**，不外传、不引用。
- **数据**：TGSIM 为美国政府公有领域数据，未入库（体积）；`runs/`、`data/` 在 `.gitignore`。
- **他人材料**：仓库**当前版本不含**任何他人论文全文或 PDF；`literature/` 仅保留元数据与 DOI。
- **AI 使用**：写作与代码有 AI 辅助（润色、脚本、排版）；若期刊要求披露，我们如实申报——本说明不为规避披露而设。

---

**反馈方式**：直接在本文档批注，或按 §6 八问逐条回复。收到后我们出“逐条处置表”（改稿 / 补实验 / 改主张），并同步更新仓库。
