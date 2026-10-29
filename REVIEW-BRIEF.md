# 外审说明 / Reviewer Brief

**稿件**：*When Is Overtaking Frequency Informative? A Pre-Registered Closed-Loop Ablation and an Availability Map*
**状态**：**尚未投稿**（pre-submission），目标期刊 IEEE Transactions on Intelligent Vehicles (T-IV)
**稿件文件**：`papers/p1/manuscript.pdf`（8 页，IEEEtran 双栏，参考文献 7 条）
**仓库**：https://github.com/xyx-cmd-maker/auto-driving
**送审日期**：2026-10-29

---

## English summary (for an international reviewer)

This is a **pre-submission** manuscript, shared with one external reviewer before it goes to IEEE T-IV. It reports a **pre-registered closed-loop ablation** of a traffic-pressure scalar (overtaking frequency, OTF) as a fourth input to a continuous-time neural car-following controller, together with a **measured availability map** of that scalar in SUMO, in the public TGSIM corpus, and in our own closed loop. The headline is a **null/equivalence** result: in two of four scenarios the two arms are statistically equivalent within a pre-registered 10 % margin, and two are inconclusive. We ask for a **hostile methodological read**, not encouragement: the paper's main risk is that it is a negative result whose only defence is design discipline. Section 6 below lists the weaknesses we already know about, and Section 7 lists the specific questions we want attacked.

---

## 1. 请你做什么（三类意见，按优先级）

| 优先级 | 类型 | 具体问题 |
|---|---|---|
| **P0** | **能不能投** | 以现在这个形态投 T-IV，是否会被 desk-reject 或一审即拒？若会，缺的是什么 |
| **P1** | **统计与推断** | 等价性框架用得对不对；n=5 的功效上限处理是否诚实；"未定"的两场景是否应该报 |
| **P2** | **表述与证据边界** | 摘要/结论是否有超出证据的措辞；哪一句最容易被审稿人抓住 |

**不需要**你做的：语言润色（我们自己过）、格式检查（T-IV 模板已套）、引用补齐（7 条已逐条 DOI 核验）。

> **你是团队内部成员，全部材料对你开放。**
> 除了稿件，最值得你看的是我们自己写的那几份"丑话先说"的文档：
> - `audit/第一次组会/20-strategy-after-downgrade.md` —— 我们对本文弱点的自评，以及**改投 T-ITS 的备选路线**；
> - `audit/第一次组会/10-a1-protocol-freeze.md` —— 收数据前冻结的 margin / α / 判定规则；
> - `audit/第一次组会/15-a1-full-results.md` —— 全量结果（含双 CI、TOST、功效分析）；
> - `audit/第一次组会/18-window-scan.md` —— 窗口扫描（n=5 与 n=10 两版，含我们自己推翻自己的那一版）；
> - `audit/第三次组会/组会汇报-分批计划-2026-10-28.md` —— 汇报节奏与"要老师拍板的三件事"。
> 这些文档里的话比稿子更直白，**审稿意见不必照顾我们的面子**。

---

## 2. 一句话结论与三条贡献

> **一句话**：我们先测这个交通标量"到底存不存在"，再做消融；在它稀缺的区间里，加上它没有可分辨的性能差异。

| # | 贡献 | 证据强度 |
|---|---|---|
| C1 | **可用性测量**：真实交通里该标量 53 % 时间非零，我们自己的闭环只有 8.4 %（约 1/6） | 强（真实公开数据开环 + 闭环仿真） |
| C2 | **预注册等价性消融**：四场景 20 局，2/4 等价（TOST p = 0.020、0.006），2/4 未定 | 强（设计层面），但功效受 n=5 限制 |
| C3 | **机制证据**：删掉观测里的相对速度，代价仅 0.14（30.82 → 30.96）→ 递推状态可从间距历史重建它 | 中（单场景 5 局 + 10 局对照） |

**一句话卖点**：不是性能，是「**测量 + 不撒谎的统计协议**」。

---

## 3. 主张—证据台账（每条都能点到文件）

| 主张 | 证据文件 | 等级 | 已知缺口 |
|---|---|---|---|
| 真实交通中 OTF 非零比例 ≈ 0.53 | `results/p1/otf_real_tgsim_s1.json`；`audit/第一次组会/18-real-data-otf.md` | B（开环、外部数据） | 流量为估计值（缺几何文件，无法算绝对流量） |
| 我们闭环中 ≈ 0.084 | `audit/第一次组会/15-a1-full-results.md` | A（我们自己的实验） | 单地图（Town04）、单车型 |
| 可用性随密度/窗口单调上升 | `results/p1/otf_density_sweep_sumo_s1-2-3_fine.json` | B（SUMO） | 三种子 |
| 窗口 5/10/20 s → Φ = 0.084 / 0.167 / 0.334，组内零方差 | `audit/第一次组会/17-three-scenario-highinfo.md` | A（操纵检验） | 剂量反应精确，但"有用性"未随之提高 |
| 2/4 场景在 10 % margin 内等价 | `audit/第一次组会/15-a1-full-results.md`（含双 CI） | A（预注册） | 其余 2 场景未定，不能写成"无效" |
| n=10 时三点标准差 1.718 / 1.809 / 1.926 且不可区分 | `audit/第一次组会/18-window-scan.md` §n10 | A（可复算） | 仅 lead-brake 扩到 n=10 |
| 删 Δv 代价 0.14 | `audit/第一次组会/20-strategy-after-downgrade.md` §6 | B（5 局 + 对照） | 仅一个场景；只证明"代价不敏感" |

---

## 4. 数字怎么自己复核（一条命令，1 分钟）

仓库里放了主实验的**逐局 JSON**（60 个文件、575 KB、已脱敏：无本地路径、无用户名、无邮箱），
路径 `results/p1/cases/`。请直接运行：

```powershell
py -3.12 scripts/verify_from_published_cases.py
```

**预期输出（2026-10-29 实测，exit=0）**：

```
  窗口           n    Δcost 均值  Δcost SD
  main        10      +0.409     1.718
  window10    10      +0.587     1.809
  window20    10      +0.558     1.926

  机制检验（删掉相对速度）：off 臂复合代价
    有 Δv（main 全部）     n=10  均值 30.82
    无 Δv（degraded）     n=5  均值 30.96
    差值 +0.14

  主实验四场景的配对差（main 组，seeds 0-4）
  none                5      +0.256
  cutin               5      +0.326
  lead-brake         10      +0.409
  lead-exit           5      -0.051
```

> 若你的输出与上面**任何一位数**不同，那就是我们数据与稿件不一致——请直接告知，这比文字意见更重要。
> 说明：`main/` 下 `lead-brake` 有 10 个种子（2026-10-19 补到 n=10），其余三个场景各 5 个；
> 论文 Table I 用 seeds 0–4，窗口标准差那一节用 n=10。
> 目录约定见 `results/p1/cases/README.md`。

---

## 5. 仓库导航（只看你需要的）

| 路径 | 是什么 | 建议 |
|---|---|---|
| `papers/p1/manuscript.pdf` | **要审的稿**（8 页） | 必读 |
| `papers/p1/manuscript.tex` / `manuscript-ieee.md` | LaTeX 源 / IEEE 编号版正文 | 想核原文时看 |
| `papers/p1/01-abstract-final.md` | 摘要与关键词（含逐句证据映射） | 必读 |
| `audit/第一次组会/15-a1-full-results.md` | 主实验全量结果（含双 CI、TOST、功效） | 必读 |
| `audit/第一次组会/10-a1-protocol-freeze.md` | **预注册冻结记录**（margin、α、判定规则） | 评统计时必读 |
| `audit/第一次组会/18-window-scan.md` | 窗口扫描（n=5 与 n=10 两版） | 评 C3 时看 |
| `audit/第一次组会/20-strategy-after-downgrade.md` | 我们自己写的"弱点与改投路线" | **建议读**，可省你重复发现 |
| `literature/library/P1-library.jsonl` | 98 条候选文献（66 条已核验） | 查引用覆盖时看 |
| `src/ctrl/`、`src/envs/`、`scripts/` | 控制器 / 环境 / 复算脚本 | 想复现时看 |
| `AGENTS*.md`、`audit/` | 工作纪律、逐次组会材料、策略自评、协议冻结 | **建议读**（内部成员）：先看 `audit/第一次组会/20-strategy-after-downgrade.md` 与 `10-a1-protocol-freeze.md` |

---

## 6. 我们已知的弱点（先说，免得你重复发现）

1. **这是负结果**。全部防御来自设计纪律（预注册、同预算、等价性），没有正效应支撑。
2. **n=5 的功效上限**：符号翻转检验最小双侧 p = 0.0625，Holm 校正后需 ≤0.0125 → **数学上不可能显著**。所以我们才主张等价而非优越。
3. **单地图、单车型、单控制器架构**（CARLA Town04 + Tesla Model 3 + CfC）。外部效度未验证。
4. **OTF 由脚本注入**（每 4 s 一次定向切入）而非背景交通自然产生。我们有阴性对照（背景车 +60 % 不改变 Φ），但审稿人可能仍质疑。
5. **控制频率 20 Hz**，不是 100 Hz（主机限制）。
6. **真实数据只做开环**（TGSIM 无闭环接口），不能称"实车验证"。
7. **机制证据（C3）只在一个场景**：删 Δv 后代价 +0.14，但只证明"代价不敏感"，不等于"重建"被直接观测。

---

## 7. 想请你重点攻击的八个问题

1. **"测可用性"这个动作，够不够撑起一篇 T-IV？** 还是说审稿人会认为这是"没做出来"的包装？
2. **等价性框架**：margin 取偏离臂均值的 10 %，这个选择是否可辩护？有没有更标准的做法（如基于最小效应量）？
3. **2/4 未定的两个场景**：应当报"未定"，还是应当扩种子到 20 再判？（扩种子约 4 h/场景）
4. **C3 的因果性**：删 Δv 代价 0.14，能否支撑"控制器重建了 Δv"这一说法？还是只能说"代价不敏感"？
5. **OTF 注入**是否构成"操纵了非自然现象"，从而削弱外部效度？
6. **0.084 vs 0.53 的对比**：真实数据流量是估计值，这个对比有多少可信度？
7. **摘要第 2 句**（"rarely measured before it is ablated"）是否属于对文献的强断言？我们只核了 7 条引用。
8. **若你是审稿人，你会给 Major Revision 还是 Reject？** 理由一句话即可。

---

## 8. 边界声明

- **未投稿**：本稿未向任何期刊提交。仓库含内部过程材料（`audit/`、`AGENTS*.md`），**请仅在团队内使用**，不要外传或引用。
- **他人材料**：仓库内**不包含**任何他人论文的全文或 PDF（已在下架清单中移除）；`citations/` 与 `literature/` 只保留**元数据与 DOI**。
- **数据**：TGSIM 为美国政府公有领域数据，未入库（体积）；`data/` 在 `.gitignore` 中。
- **代码**：`src/`、`scripts/` 可直接阅读；运行需 CARLA 0.9.16 + SUMO 1.27.1（见 `configs/env/`）。
- **AI 使用**：写作与代码中使用了 AI 辅助（润色、脚本、排版）。若期刊要求披露，我们会如实申报；本说明不为规避披露而设。

---

**反馈方式**：直接在本文档上批注，或按 §7 的八问逐条回复。收到后我们会把每一条转成可执行动作（改稿 / 补实验 / 改主张），并回一份"逐条处置表"。
