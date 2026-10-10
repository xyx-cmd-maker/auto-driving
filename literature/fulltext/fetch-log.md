# fetch-log.md — 全文抓取日志

任务：为引用核验下载 6 篇论文全文纯文本
目录：`D:\Deepseek Harness\auto-driving\literature\fulltext\`
日期：2026-10-02

---

## 1. 汇总表（每篇一行）

| 编号 | 状态 | 实际 URL | 正文字符数 |
|---|---|---|---|
| p01-cfc-nmi2022 | OK（全文） | https://arxiv.org/html/2106.13898 | 65041（正文 64970） |
| p07-pinn-ctrl-neucom2024 | OK（全文） | https://arxiv.org/html/2104.02556 | 80712（正文 80641） |
| p15-humanlike-cf-trc2018 | OK（全文，PDF 提取） | https://arxiv.org/pdf/1901.00569 | 64825（正文 64755） |
| p33-lpstring-tcst2014 | OK（全文，PDF 提取） | https://pure.tue.nl/ws/files/73899014/Ploeg_2014_Lp_String_Stability_of_Cascaded_Systems_Application_to_Vehicle_Platooning.pdf | 48146（正文 47982） |
| p43-dissipation-trc2018 | OK（全文） | https://arxiv.org/html/1705.01693 | 72483（正文 72412） |
| p45-deeplcc-tcst2023 | OK（全文） | https://arxiv.org/html/2203.10639 | 97265（正文 97194） |

- **ABSTRACT-ONLY：0 篇。FAILED：0 篇。** 6 篇均拿到全文。
- 字符数定义：以 Node `readFileSync(path,'utf8').length` 统一测量。**总字符数** = 整个 `.txt`；**正文** = 扣除末尾 `SOURCE_URL:` / `FETCH_DATE:` 两行（p33 因 TU/e URL 较长，页脚为 164 字符，其余约 70 字符）。
- 复现命令：`node "_tools\_final.mjs"`。

---

## 2. 逐篇：尝试过的全部 URL 与结果

### p01-cfc-nmi2022
| URL | 结果 |
|---|---|
| https://export.arxiv.org/api/query?id_list=2106.13898 | 200，题名 "Closed-form Continuous-time Neural Models"，journal_ref = Nature Machine Intelligence 4, 992--1003 (2022)，DOI 10.1038/s42256-022-00556-7 → **与任务书目完全匹配** |
| https://arxiv.org/html/2106.13898 | **200，346633 bytes HTML → 采用** |
| https://ar5iv.labs.arxiv.org/html/2106.13898 | 200，333970 bytes（未使用，主 URL 已成功） |

### p07-pinn-ctrl-neucom2024
| URL | 结果 |
|---|---|
| https://export.arxiv.org/api/query?id_list=2109.07153 | 200，但题名 = "Refined fundamental parameters of Canopus from combined near-IR interferometry and spectral energy distribution"（天体物理）→ **编号不匹配，任务给的 arXiv 编号有误** |
| https://export.arxiv.org/api/query?search_query=ti:%22Physics-informed%20neural%20nets%20for%20control%20of%20dynamical%20systems%22 | 200，命中 **arXiv:2104.02556v3**，题名 "Physics-Informed Neural Nets for Control of Dynamical Systems"，DOI 10.1016/j.neucom.2024.127419 → **与 Neurocomputing 579:127419 (2024) 完全匹配** |
| https://arxiv.org/html/2104.02556 | **200，354630 bytes HTML → 采用** |
| https://ar5iv.labs.arxiv.org/html/2104.02556 | 200，332909 bytes（未使用） |

### p15-humanlike-cf-trc2018
| URL | 结果 |
|---|---|
| https://export.arxiv.org/api/query?id_list=1801.02433 | 200，但题名 = "Arbitrary digital pulse sequence generator with delay-loop timing"（仪器仪表）→ **编号不匹配，任务给的 arXiv 编号有误** |
| https://export.arxiv.org/api/query?search_query=ti:%22Human-like%20autonomous%20car-following%20model%22 | 200，命中 **arXiv:1901.00569v1**，"Human-Like Autonomous Car-Following Model with Deep Reinforcement Learning"，journal_ref = Transportation Research Part C: Emerging Technologies 2018 |
| https://arxiv.org/html/1901.00569 | **404**（该文无 arXiv LaTeXML HTML 版） |
| https://ar5iv.labs.arxiv.org/html/1901.00569 | 200 但为 **跨域重定向到 arxiv.org 的占位页，非论文 HTML**（`web_fetch` 明确报 `cross-origin redirect to https://arxiv.org is not followed automatically`）→ 判定 ar5iv 无此渲染 |
| https://arxiv.org/pdf/1901.00569 | **200，1897150 bytes application/pdf → 采用（PyMuPDF 提取，34 页）** |
| https://api.crossref.org/works?query.bibliographic=Human-like+autonomous+car-following+model+with+deep+reinforcement+learning | 200，DOI 10.1016/j.trc.2018.10.024，TR-C vol 97, pp. 348-368, 2018-12 → **卷/页/年匹配** |

### p33-lpstring-tcst2014
| URL | 结果 |
|---|---|
| https://export.arxiv.org/api/query?id_list=1304.5986 | 200，但题名 = "A little scholium on Hilbert-Rohn via the total reality of M-curves…"（代数几何）→ **编号不匹配，任务给的备选 arXiv 编号有误** |
| https://export.arxiv.org/api/query?search_query=all:%22String%20Stability%20of%20Cascaded%20Systems%22%20AND%20all:%22Vehicle%20Platooning%22 | 200，**totalResults = 0** → arXiv 上无此文 |
| https://research.tue.nl/en/publications/lp-string-stability-of-cascaded-systems-application-to-vehicle-plo | 404（slug 被截断） |
| https://research.tue.nl/en/publications/lp-string-stability-of-cascaded-systems-application-to-vehicle-pl/ | 200（机构库条目页，用于定位 PDF） |
| https://pure.tue.nl/ws/files/73899014/Ploeg_2014_Lp_String_Stability_of_Cascaded_Systems_Application_to_Vehicle_Ploating.pdf | ERR（fetch failed；拼写错误 "Ploating"，非真实文件） |
| https://pure.tue.nl/ws/files/73899014/Ploeg_2014_Lp_String_Stability_of_Cascaded_Systems_Application_to_Vehicle_Platooning.pdf | **200，411291 bytes application/pdf → 采用（PyMuPDF 提取，10 页；TU/e 机构库 accepted manuscript）** |
| https://api.crossref.org/works/10.1109/TCST.2013.2258346 | 200，题名 "Lp String Stability of Cascaded Systems: Application to Vehicle Platooning"，Jeroen Ploeg / Nathan van de Wouw / Henk Nijmeijer，IEEE TCST 22(2):786-793, 2014-03 → **完全匹配** |

### p43-dissipation-trc2018
| URL | 结果 |
|---|---|
| https://export.arxiv.org/api/query?id_list=1705.01693 | 200，题名 "Dissipation of stop-and-go waves via control of autonomous vehicles: Field experiments"，journal_ref = TR-C 89:205-221, 2018，DOI 10.1016/j.trc.2018.02.005 → **完全匹配** |
| https://arxiv.org/html/1705.01693 | **200，245477 bytes HTML → 采用** |
| https://ar5iv.labs.arxiv.org/html/1705.01693 | 200，226723 bytes（未使用） |

### p45-deeplcc-tcst2023
| URL | 结果 |
|---|---|
| https://export.arxiv.org/api/query?id_list=2203.10639 | 200，题名 "DeeP-LCC: Data-EnablEd Predictive Leading Cruise Control in Mixed Traffic Flow"（含 "DeeP-LCC" ✓），DOI 10.1109/TCST.2023.3288636 → **完全匹配** |
| https://arxiv.org/html/2203.10639 | **200，515957 bytes HTML → 采用** |
| https://ar5iv.labs.arxiv.org/html/2203.10639 | 200，491699 bytes（未使用） |

---

## 3. 方法说明（含一处对任务指令的必要偏离，请复核）

**核验环节**：全部 arXiv 编号/题名/DOI 核验、Crossref 书目核验均使用 **`web_fetch`**（任务指定的工具），见 §2 各表。

**正文抓取环节**：**未**使用 `web_fetch`，改用 Node `fetch` 落盘 + 确定性转换（HTML：`_tools/_fetch_html.mjs`；PDF：`_tools/_pdf.py` + PyMuPDF）。原因：

1. `web_fetch` 只能把内容**返回进模型上下文**，没有落盘通道；要把 ~6 篇（单篇 HTML 245–516 KB，转文本 6.5–9.7 万字符）全文写进文件，只能由模型经 `write` **二次转写**，必然发生截断／改写／数字丢失——直接违反任务"**不要总结、不要改写、不要删数字**"的硬要求。
2. 单篇 HTML 转文本约 2–3 万 token，6 篇约 15 万 token 上下文，不可行。
3. 任务禁用 `Invoke-WebRequest` 的**真实原因是**"本机部分域名会触发凭据提示而报假错"；Node `fetch` 同样规避该问题，且是全局 `AGENTS.md` §2.1 硬约束 2 指定的本机标准做法。**约束的意图（拿到真实全文）被完整满足。**

**转换保真度**：
- HTML→文本：保留章节标题（`#` 分级）、全部表格（含表号+表题+单元格数值，以 `|` 分隔）、图题（原样式 `Fig. N:` / `Figure N:`）、公式（LaTeXML `alttext` LaTeX 源）、参考文献表；丢弃导航栏、脚本样式、页眉页脚。
- PDF→文本：PyMuPDF 逐页文本提取，保留 `===== PAGE n =====` 页码标记以利溯源；IEEE 双栏阅读顺序正确。
- **参考文献列表予以保留**（任务表述"去掉导航栏、参考文献列表之外的样板文字"按"保留参考文献表"理解）——引用核验需要它。如需删除请告知。

---

## 4. 保真度自查（可复现）

| 检查项 | 结果 |
|---|---|
| UTF-8 完整性 | 6 文件全部 `cjk=0`、`replacement-char=0`（无乱码；控制台显示的 `鈥搒tep` 系 PowerShell 显示编码，文件本身正确） |
| 章节覆盖 | 6/6 含 Abstract；5/6 含 Introduction（p01 为 Nature Machine Intelligence 版式，正文首节无 "Introduction" 标题，属原刊格式）；6/6 含 Conclusion |
| 图题 | p01=9、p07=26、p15=10（`FIGURE N …`）、p33=7（`Fig. N.`）、p43=6、p45=19 |
| 表格 | p01=13、p07=3、p15=8、p43=13、p45=4 处表号；**p33 = 0 表**——已核实该文原文即无表格（纯图 + 正文内联参数 τ=0.1 s, φ=0.2 s, kp=0.2, kd=0.7, θ≈0.15 s, h=0.7 s），**非提取失败** |
| 数值抽查 | p45 `TABLE I` 数值完整（HDV 1: α=0.45, β=0.60, s_go=38）；p15 `TABLE 1` 数值完整（Aggressive: 15.90 / 0.16 / 96.77 / 10.50 …）；p01 `Table 1` 时间复杂度表达式完整 |

---

## 5. 需提请注意的书目出入（与任务描述不一致）

1. **p15 作者列表**：任务写 "Zhu, Wang, **Pu, Li**"。Crossref（DOI 10.1016/j.trc.2018.10.024）与 arXiv:1901.00569 一致显示作者为 **Meixin Zhu, Xuesong Wang, Yinhai Wang**（3 人，无 Pu、无 Li）。**题名、期刊、卷 97、页 348-368、年 2018 全部匹配**，故确认是同一篇；作者列表需更正。
2. **p07 arXiv 编号**：任务给的 `2109.07153` 是 Canopus 天体物理论文；正确编号为 **`2104.02556`**（v3）。
3. **p15 arXiv 编号**：任务给的 `1801.02433` 是数字脉冲序列发生器论文；正确编号为 **`1901.00569`**。
4. **p33 备选 arXiv 编号**：任务给的 `1304.5986` 是代数几何论文，且 arXiv 检索此文 totalResults=0，**该文不在 arXiv 上**；最终采用 TU/e 机构库 accepted manuscript。
5. **p01 题名**：arXiv 条目题名为 "Closed-form Continuous-time Neural **Models**"，而所抓 HTML（NMI 正式版式）首页题名为 "Closed-form Continuous-time Neural **Networks**" —— 与任务给的 NMI 2022 题名一致。

---

## 6. 目录内其他文件

- `_raw/` — 原始抓取件（4 个 HTML + 2 个 PDF），作为提取结果的溯源证据，可复核/重跑。
- `_tools/` — 抓取与转换脚本（`_fetch_html.mjs`、`_dl.mjs`、`_pdf.py`、`_probe.mjs`、`_diag*.mjs`、`_verify.mjs`、`_norm.mjs`），可删除，不影响交付物。

**证据等级（A–D）**：本次交付为**原文全文转录**，属 **A 级**（一手来源直接抓取，未经过二次转述）；但 p15/p33 经 PDF 文本层提取，图表版式退化为线性文本，**表格结构（行列对齐）为 B 级**——数值本身完整，但若需精确复现表格排版应回看 `_raw/*.pdf`。
