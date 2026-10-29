# 检索日志（T-IV 红队，2026-10-29）

> 用途：为目标文件 §5.1（文献新颖性审计）提供**可复现**的检索记录。
> 纪律：每条记录通道、查询、日期、命中数与相关性判定；**不把"没搜到"写成"不存在"**。

---

## L1｜OTF 本身

| 项 | 内容 |
|---|---|
| 通道 | OpenAlex API（经 domain_search） |
| 查询 | `overtaking frequency autonomous vehicle control input` |
| 日期 | 2026-10-29 |
| 命中 | 3 |
| 相关 | **1**：Sensors 2021（10.3390/s21020371） |
| 判定 | OTF 已被用作实车评估模型的输入 |

## L2｜同一术语的第二次检索

| 项 | 内容 |
|---|---|
| 通道 | OpenAlex |
| 查询 | `"overtaking frequency" OTF traffic flow state lane evaluation` |
| 日期 | 2026-10-29 |
| 命中 | 2 |
| 相关 | **2**：Sensors 2021、J. Adv. Transp. 2021（10.1155/2021/5948971） |
| 判定 | **两篇均未引用于本稿**（Round 05 发现，Round 06 已补引） |

## L3｜"可用性/稀疏性"角度

| 项 | 内容 |
|---|---|
| 通道 | OpenAlex |
| 查询 | `sparsity of lane change events in driving simulation traffic density realism` |
| 日期 | 2026-10-29 |
| 命中 | 3 |
| 相关 | **0**（元胞自动机、交通灯仿真、SUMO 标定——均不涉及"特征可用性"） |
| 判定 | 未发现"先测可用性再消融"的先例 |

## L4｜闭环消融角度

| 项 | 内容 |
|---|---|
| 通道 | OpenAlex |
| 查询 | `closed-loop ablation traffic interaction feature autonomous driving controller input necessity` |
| 日期 | 2026-10-29 |
| 命中 | 3 |
| 相关 | **0**（LMDrive、端到端综述、多模态 LLM 综述） |
| 判定 | 未发现同类闭环消融研究 |

## L5｜负结果角度

| 项 | 内容 |
|---|---|
| 通道 | arXiv |
| 查询 | `ablation extra input car following controller no benefit negative result` |
| 日期 | 2026-10-29 |
| 命中 | 3 |
| 相关 | **1（弱）**：RACER（2312.07003）——跟驰模型，非消融 |
| 判定 | 未发现"交通标量作为控制输入的负结果" |

## L6｜两次 work 直取（元数据核验）

| 项 | 内容 |
|---|---|
| 通道 | OpenAlex work API |
| 查询 | `doi:10.3390/s21020371`、`doi:10.1155/2021/5948971` |
| 日期 | 2026-10-29 |
| 结果 | 作者、年份、卷期页、摘要（倒排索引）均取到；**未读全文** |

---

## 覆盖度声明（必须写进论文与回复）

1. 上述 5 条检索**只覆盖英文标题/摘要**，不含中文文献（除已知的学位论文）。
2. **只用了 OpenAlex 与 arXiv 两个通道**，未用 Web of Science / Scopus（无权限）与 Google Scholar（不可编程）。
3. 因此结论只能是"**在本次检索范围内未发现同类工作**"，**不能**写成"首次"或"尚无研究"。
4. 本地 98 条文献库**原先不含**这两篇 OTF 先例，说明库的构建范围有盲区；已在 Round 06 补入（现 100 条，含 `G-OTF-precedent` 标签）。

---

## 结论（供 §5.1 使用）

| 主张 | 是否被文献支持 | 证据 |
|---|---|---|
| OTF 作为交通压力标量 | **是**（他人已提出） | Sensors 2021 / JAT 2021 |
| OTF 用作评估/决策模型的输入 | **是** | 同上 |
| OTF 用作**闭环控制器输入的因果检验** | **未发现在先例** | L3–L5 均无相关命中 |
| **先测可用性再消融** 这一做法 | **未发现在先例** | L3–L5 均无相关命中 |
