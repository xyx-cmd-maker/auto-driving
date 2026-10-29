# 改投路线的可执行清单（T-ITS / OJ-ITS）+ 三处重定位补丁

> 目标文件：`C:\Users\本手\Downloads\TIV_RedTeam_Review_and_DSH_Goal.md`
> 执行日期：2026-10-29 ｜ 基线 commit：`1b9b21f`
> 状态：**补丁已就绪（dry-run 通过），未应用**；等作者定方向。

---

## 1. 三个去处怎么选（不含录用率预测）

| | **T-IV**（现目标） | **T-ITS** | **OJ-ITS** |
|---|---|---|---|
| 定位 | 智能车辆（车端为主） | 智能交通系统（系统与评估） | 开放获取，范围宽 |
| 对"负结果 + 测量方法"的容忍度 | 低 | **中** | **较高** |
| 本文要不要换叙事 | — | **要**（测量优先） | 可保留现叙事 |
| 要不要新实验 | 若想投 T-IV 强贡献，**要**（14 局起） | 不一定要 | 不要 |
| 风险 | 一审即拒或要求大改 | 可能要求"更贴近系统/部署" | 影响因子/声望低于前两者 |

**判断**：现稿的证据链（数字可复现、协议冻结、限制诚实）**足以支撑一篇"评估方法 + 负结果"的论文**；
它**不足以支撑** T-IV Regular 所要求的"新技术能力"。改投不是降级，是**让贡献强度与期刊定位匹配**。

---

## 2. 改投要动的三处（`scripts/apply_retarget.py`，dry-run 已通过）

| id | 位置 | 改什么 | 为什么 |
|---|---|---|---|
| **R1** | 标题 | 提问式 → 方法/实践式：`Measure the Signal Before You Ablate It: Availability of a Traffic-Level Scalar and a Pre-Registered Closed-Loop Equivalence Study` | T-ITS 偏系统/方法，不用问句当标题 |
| **R2** | 摘要开头两句 | 把"程序性缺口"提到最前：先承认标量便宜、再指出"没人先测它是否非零" | 让读者第一眼看到方法与结论，而不是一个待验证的现象 |
| **R3** | 贡献列表 | **把"可用性地图"提为第 1 条**，消融降为第 2 条；末尾加一句给实践者的建议 | 与 T-ITS 的"评估方法"定位对齐 |

**R3 新增的那句话**：

> "The recommendation for practice is procedural rather than numerical: measure availability before
> ablating a traffic-level signal, and report the operating point alongside the ablation."

---

## 3. 改投**不动**的东西（这一点最重要）

| 类别 | 是否改动 |
|---|---|
| 全部数字（0.084 / 0.167 / 0.334 / 0.53 / 0.39 / +0.256…） | **不动** |
| Table I / II / III、Fig.1 / Fig.2 | **不动** |
| 统计方法（精确检验、TOST、Holm、三态） | **不动** |
| 六条 Limitations | **不动** |
| §5.6 Future work | **不动** |
| 7 条参考文献 | **不动**（R1–R3 不新增引用） |

⇒ 改投是**换叙事入口**，不是换结果。这也意味着：**若以后想再投 T-IV，可以原样回退**。

---

## 4. 应用与回退

```powershell
# 只看锚点
py -3.12 scripts/apply_retarget.py

# 应用（自动重拼装/重转换/重生成 tex；PDF 需再跑 pdflatex ×2）
py -3.12 scripts/apply_retarget.py --apply

# 回退（改投决定撤销时）
git checkout -- papers/p1/01-abstract-final.md papers/p1/02-introduction-discussion.md
```

**已验证的副作用**（dry-run 期间算出，未写入）：

| 检查 | 结果 |
|---|---|
| 摘要词数 | 245 → **231**（仍 ≤250） |
| 摘要含缩写 OTF | **False**（T-IV 规则保留） |
| 摘要含 0.084 | **True**（关键数字未丢） |

---

## 5. 若选 OJ-ITS

不需要 R1–R3；只需：
1. 把 cover letter 的期刊名改掉；
2. 在 §1 末加一句定位（"a methodological and negative-result contribution"）；
3. 保留 T-IV 的格式要求（IEEEtran 双栏可直接用）。

---

## 6. 与"补实验投 T-IV"的对比

| 路线 | 成本 | 可能的结局 |
|---|---|---|
| 改投 T-ITS（R1–R3） | **0.5 h**（应用+重编译+通读） | 贡献与定位匹配，负结果可被接受 |
| 改投 OJ-ITS | 0.3 h | 更稳，但声望低 |
| Route A 14 局 + 仍投 T-IV | ≈3 h 实验 + 1–2 h 代码 + 改稿 | **可能有**正面结果；也可能仍"未定"，那时还得改投 |

---

## 7. 需要作者决定

1. 改投 **T-ITS**（应用 R1–R3）？
2. 改投 **OJ-ITS**（只改 cover letter + 一句定位）？
3. 还是先做 **Route A 14 局**、再决定投哪？
4. 若选 1/2：**是否同时应用 Round 10 的补丁 E1–E5 + E7**（口径与事实纠错）？
   —— 建议**是**：那些与选刊无关，属论文自身正确性。

> 未确认前，本文件不产生任何改动。
