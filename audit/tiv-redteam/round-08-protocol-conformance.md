# Round 08 — 冻结协议逐条核验 + P1-M 三种改法（待选）

> 目标文件：`C:\Users\本手\Downloads\TIV_RedTeam_Review_and_DSH_Goal.md`
> 执行日期：2026-10-29 ｜ 基线 commit：`47a224c`
> 本轮范围：P0-3（冻结协议一致性）**已完成**；P1-M（Fig.2 统计量口径）出三份可直接执行的 diff，等作者选择。

---

## 9.1 结论

| 项 | 判定 |
|---|---|
| 当前状态 | **MAJOR REWORK**（三项待决策；无新增阻断） |
| 是否达到 T-IV 强贡献门槛 | **否（证据不足）** |

**三个最关键理由**

1. **P0-3 通过并关闭**：新脚本 `scripts/audit_protocol_conformance.py` 把冻结文档的 8 节决定拆成 **21 条可执行断言**，在数据侧与代码侧逐条核查，**21/21 PASS，exit=0**。
2. **核出一条"冻结文档未写、代码实际执行"的规则**：无效判定除 20 m 位移阈值外，还有一条"reset 后残留车辆数异常"的守门（`train_cfc.py` L247-250）。**已发布 755 个无效候选里没有一条由该规则触发**（全部是 20 m），因此不影响现有结果，但**协议文档应补记**。
3. **P1-M 仍等选择**：下面给三份 diff，选完我可一次性改完并重画 Fig.2。

---

## 9.2 冻结协议逐条核验（21 条，全 PASS）

| # | 冻结条款 | 期望 | 实测 | 判定 |
|---|---|---|---|---|
| 1 | 场景集合 | none / cutin / lead-brake / lead-exit | 同 | PASS |
| 2 | 种子集合 | 0,1,2,3,4 | 同 | PASS |
| 3 | 预注册局数 | 20 | 20 | PASS |
| 4 | 无重复 (场景,种子) | 20 | 20 | PASS |
| 5 | 双腕齐备 | True | True | PASS |
| 6 | 控制频率 | 20 Hz | 20.0 | PASS |
| 7 | 仿真步长 | 50 Hz | 50.0 | PASS |
| 8 | 每局时长 | 60 s | 60.0 | PASS |
| 9 | 交通车辆数 | 16 | 16 | PASS |
| 10 | 每臂候选 | 12 | 12 | PASS |
| 11 | 精英数 | 3 | 3 | PASS |
| 12 | hidden | 24 | 24 | PASS |
| 13 | 执行指纹 20 局一致 | 1 | 1 | PASS |
| 14 | 主口径 | `best_cost`（各自最好有效候选） | 唯一取值 | PASS |
| 15 | 无效原因规则类型 | 仅 20 m | `{20m_rule}` | PASS |
| 16 | 代码含 `travelled > 20.0` | True | True | PASS |
| 17 | 代码含 Holm 实现 | True | True | PASS |
| 18 | 等 K 的 `k = min(n_valid)` | True | True | PASS |
| 19 | 环境只有 4 类主场景 | True | True | PASS |
| 20 | 环境未实现长尾四类 | False | False | PASS |
| 21 | 论文未声称覆盖长尾 | False | False | PASS |

**不在此脚本覆盖范围（已在别轮完成）**：精确符号翻转、95%/90% CI、TOST 数值、三态判定的**数值复现**（Round 02，44 个数值 + 4 标签）；择优层与等 K 的**数值复现**（Round 03）；补充组（Round 04）。

> ⚠️ 本轮修正一次自身错误：首版把 "ego 仅移动 0.0 m / 0.1 m / …" 的**距离数值**当成不同原因，导致 25 种"原因"、误报 FAIL。改为按**规则类型**归类后 PASS。

---

## 9.3 P1-M 的三种改法（**请选一个**）

### 现状

| 来源 | 图上取什么 | 值 |
|---|---|---|
| TGSIM | 10 run 均值 | 0.53 |
| SUMO | 3 种子 × 密度均值 | 0.39 |
| **CARLA** | **跨场景共享值（= 最小）** | **0.084 / 0.167 / 0.334** |
| CARLA 合并均值（未报） | 20 局均值 | **0.096 / 0.200 / 0.393** |

### 方案 1（推荐）：统一改成合并均值 + 范围，重画 Fig.2

**改三处**：
- 摘要：`reaches only 0.084` → `reaches a pooled mean of 0.096 across twenty runs`
- Fig.2 图注："star marks the pooled mean over twenty runs; bars give the range across the four scenarios"
- §5.2 的 "0.084 to 0.167" 保留（它就是范围）

**代价**：需重画 Fig.2（`fig_otf_phase_real.py`）；"1/6" 变成 "1/5.5"。
**优点**：与另两个来源同为汇总量，**口径一致**，最难被挑。

### 方案 2：保留最小值，但在图注与正文**显式定义**

**改两处**（不动图）：
- Fig.2 图注追加一句：`Plotted values are the fraction of windows shared by the three scenarios without lead-exit crossings; lead-exit exceeds this range because it produces crossings of the ego lane without injection.`
- 摘要：`reaches only 0.084` → `reaches 0.084 in three of four scenarios (up to 0.168 when lead-exit is included)`

**代价**：零绘图成本；但**仍是三个来源用三种统计量**，审稿人仍可质疑。
**优点**：不改任何已有数字与图。

### 方案 3：两者都报

- 主点 = 合并均值（0.096），并用竖直误差条/阴影给出 0.084–0.168；
- 摘要写 `between 0.084 and 0.168, pooled mean 0.096`。

**代价**：需重画 Fig.2；摘要变长 3–5 词。
**优点**：信息最全，最保守。

> 三份 diff 的**具体英文句子**已在上面给出，选完我直接落盘 + 重编译 + 重画（若需要）。

---

## 9.4 最小下一步

| # | 任务 | 需授权 |
|---|---|---|
| 1 | **选 P1-M 方案 1/2/3** | **需要你** |
| 2 | **裁决 P0-1（OTF 定义方向）** | **需要你** |
| 3 | **选 P0-4 贡献路线 A/B/C/D** | **需要你** |
| 4 | 把"残留守门"补记进冻结文档（本轮发现，属文档一致性） | 否（下一轮可做） |
| 5 | 若选 1 或 3：改绘图脚本并重画 Fig.2 | 否（选完即可做） |

---

## 9.5 变更记录

| 文件 | 性质 | 说明 |
|---|---|---|
| `scripts/audit_protocol_conformance.py` | 新增 | 冻结协议 21 条断言 |
| `audit/tiv-redteam/round-08-protocol-conformance.md` | 新增 | 本报告 |

**未修改**：论文、图、`results/`、冻结文档。

---

## 9.6 诚实声明

1. 本轮只核"规则是否被执行"，**不重复**统计量的数值复现（那在 Round 02/03）。
2. 发现"残留守门"规则**未写入冻结文档**，但**零触发**（755 个无效候选全为 20 m），因此**不影响任何结果**；文档补记列为下一步。
3. 三轮待决策（P1-M/P0-1/P0-4）**均未推进**，因为没有作者裁决就无法安全改动。
4. 本轮未看 PDF 页面。
