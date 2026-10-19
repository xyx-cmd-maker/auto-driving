# 投稿材料（T-IV）— 2026-10-19

> 纪律：**不确定的期刊要求标【需核实】，作者背景不编造、留 [待填]**。

---

## 1. 参考文献核验的一条结论：**Swaroop 1996 不能用**

§3.1 首句"String-stability analysis then asks whether a perturbation amplifies along a platoon"
现在只引 **Ploeg et al., 2014**（库内 `verification=OK`）。

曾考虑追加经典的 Swaroop & Hedrick（1996）。核查 `literature/library/P1-library.jsonl` 后发现：

| 字段 | 库内值 | 判断 |
|---|---|---|
| title | String stability of interconnected systems | 与目标文献同名 |
| authors | **A.S. Morse** | **与 Swaroop & Hedrick 不符** |
| year / venue | 1996 / IEEE TAC | 同年同刊，易混 |
| `verification` | **MISMATCH** | **不合格** |

⇒ **不引**。若审稿人要求补经典出处，须先拿到正确条目（Swaroop & Hedrick, IEEE TAC 1996）
并重新核验，**不得**用这条 MISMATCH 记录充数。

---

## 2. Graphical abstract（可直接按此绘制）

**尺寸**：T-IV 要求待核【需核实】；通用安全值 **宽 ≥ 1300 px、300 dpi、PNG/TIFF**。

**内容（三块横向排布，复用 Fig.1 的视觉语言）**：
1. **左**：三车道示意（ego 蓝、邻道车灰），一支橙色箭头跨入 ego 车道，标 `OTF +1`；
2. **中**：一张小相图（密度 × 窗口），标出"真实 0.53 / SUMO 0.39 / 我们的闭环 0.084"三个点；
3. **右**：一句话结论条 —— **"same cost, one fewer sensor to trust"**（≤8 词，字号最大）。

**配色**：Okabe–Ito（蓝 `#0072B2`、橙 `#D55E00`、绿 `#009E73`），灰度下用箭头/文字冗余编码。

**禁止**：把 `0.084` 画成"性能提升"；不得出现 real-world validation 字样。

---

## 3. Author biographies（**个人信息留空待填，不得代填**）

> IEEE 终稿阶段要求每位作者提供 100–150 词小传 + 照片。以下为结构模板，
> **学历/职位/研究方向必须由本人填写**——我不能编造。

**Xia Yuxuan**（first author）
> Xia Yuxuan received the [待填: 学位] degree in [待填: 专业] from [待填: 学校] in [待填: 年份].
> [他/她] is currently [待填: 职位] with Shenzhen Polytechnic University, Shenzhen, China.
> [他/她] research interests include [待填: 方向].
> Contact: xiayuxuan@mail.szpu.edu.cn

**Huang Mengyuan**（corresponding author）
> Huang Mengyuan received the Ph.D. degree from Jilin University, Changchun, China, in 2023.
> [他/她] is currently [待填: 职位] with Shenzhen Polytechnic University, Shenzhen, China.
> [他/她] research interests include [待填: 方向].
> Contact: huangmy2215@szpu.edu.cn

**已知可写的部分**：黄梦圆的博士学位来自吉林大学（2023），依据 `sources/thesis-huang2023.pdf`；
其余一律待填。

---

## 4. Highlights：**T-IV 不使用这一项**

"Highlights"（3–5 条 ≤85 字符）是 **Elsevier** 的投稿要求；**IEEE 期刊没有这一项**。
⇒ **不准备**，以免在投稿系统里放错材料。

若被要求提供"key points"，可从下面这段压缩（已从摘要提炼，均为已测数字）：

- Paired closed-loop ablation of an overtaking-frequency input, 20 runs, equal budget.
- Two of four scenarios equivalent within a pre-registered 10% margin.
- Availability rises with density and window; our loop sits at 0.08–0.33.
- Quadrupling availability sharpened no estimate in three scenarios.
- Conclusion: interpretability and no extra sensing cost, not performance.

---

## 5. 定稿前最后一张检查表

| 项 | 状态 |
|---|---|
| 正文（IEEE 编号制） | ✅ `manuscript-ieee.md`，4407 词，7 条引用全有出处 |
| 参考文献清单 | ✅ `references-ieee.md`（7 条，全部 Crossref 核验 OK，除 CfC 之外都在库内） |
| Cover letter | ✅ `06-cover-letter.md`，合规全过 |
| Fig.1 / Fig.2 | ✅ 178 mm / 173 mm，300 dpi，PDF 矢量 |
| 图注 | ✅ `05-figures.md`（含三条限制） |
| 作者信息 | ⚠️ 姓名与单位已记录；**小传待本人填写** |
| Graphical abstract | ⏸ 方案已给，待绘制 |
| Suggested reviewers | ⏸ **需真实姓名与单位，不得编造** |
| T-IV 具体要求 | ⚠️ **【需核实】**：建议投前去期刊 Author Information 页核对（页数上限、graphical abstract 是否强制） |
