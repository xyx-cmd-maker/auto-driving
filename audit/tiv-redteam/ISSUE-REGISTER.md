| F4 | **等价结论依赖 jerk 常数放大的 margin：扣常数后 2/4 等价 → 0/4** | **P0（核心结论）** | **NEW（R25）** | `audit_jerk_sensitivity.py`：off 均值 30.48→14.77，margin 3.05→1.48，none 与 lead-exit 均翻为 inconclusive |# 问题登记册（T-IV 红队，Round 01–20）
| F5 | **路线 C：在 RMSE 与 accel² 上 8/8 端点全为「未定」，0 个「等价」** | **P0（核心结论）** | **NEW（R26）** | `audit_endpoint_states.py`；「2/4 等价」只在含 jerk 常数的复合代价上成立；达到等价需 8–43 种子/场景 |
| F6 | **等价判定卡在 margin 阈值上：none 的临界 margin 仅为现值的 85%，cutin 为 92%** | **P1（判据敏感）** | **NEW（R27）** | 单变量敏感性；把 margin 从 10% 降到 8.5%，none 即不再等价；lead-brake 的 TOST p=0.0515 距等价只差 0.0015 |> 目标文件：`C:\Users\本手\Downloads\TIV_RedTeam_Review_and_DSH_Goal.md`
> 更新：2026-10-29（Round 20）
> 规则：每条给**严重度 / 状态 / 证据 / 动作**；状态只有四种——
> `OPEN`（未处理）、`FIX-READY`（补丁写好待批准）、`FIXED`（已落盘并验证）、`DECIDE`（需作者裁决）。

---

## A. 数据与统计（P0-2 / P0-3 线）——全部关闭

| # | 问题 | 严重度 | 状态 | 证据 |
|---|---|---|---|---|
| A1 | 主分析（均值/CI/精确 p/TOST/三态）是否可复现 | P0 | **FIXED** | `audit_recompute_main.py` exit=0；44 数值 + 4 标签 |
| A2 | 择优层与等 K 敏感性是否可复现 | P0 | **FIXED** | `audit_recompute_selection.py` exit=0；+0.347 / −1.066 |
| A3 | Table III 与 Fig.2 补充组数据未公开 | P1 | **FIXED** | 发布 `highdensity/`(5) + `window20extra/`(10)，`audit_table3_supplementary.py` exit=0 |
| A4 | 三张表逐单元格是否与源一致 | P1 | **FIXED** | `audit_table_text_consistency.py` 88 项 exit=0 |
| A5 | 正文 §4.4/§5.2 数字是否可溯源 | P1 | **FIXED** | `audit_number_sources_body.py` 11 项 exit=0 |
| A6 | 冻结协议是否被执行 | P0 | **FIXED** | `audit_protocol_conformance.py` 21 条 exit=0 |
| A7 | 副本与 `runs/` 原件是否一致 | P0 | **FIXED** | 75 个文件 SHA256 全等 |

---

## B. 定义与口径（P0-1 / P1-M 线）——**未关闭，需裁决**

| # | 问题 | 严重度 | 状态 | 证据 / 动作 |
|---|---|---|---|---|
| B1 | `_crossed` 对"正常驶出"返回 0，与论文文字"离开 −1"冲突 | **P0** | **DECIDE** | 探针用例 B/C/D；(a) 改实现 / (b) 改文字 |
| B2 | 三来源三种估计量（对称计数 / 净>0 / \|净\|>0）却写成 "the same quantity" | **P0** | **DECIDE** | Fig.2 + 三段代码；路线 1/2/3 |
| B3 | CARLA 的 Φ 序列未持久化，改定义必须重跑 40 局 | **P0** | **DECIDE** | 逐局 JSON 仅存比例 |
| B4 | `crossed` 有两份实现（`otf_core` / `otf_sparsity_sumo`） | P1 | **DECIDE**（低风险修复） | 逐行比对等价；加单测即可 |
| B5 | 同一统计量在 §4.1 写作 "control cycles"、§5.2 写作 "windows" | P1 | **FIX-READY**（E4） | 文本对照 |
| B6 | Fig.2 的 CARLA 点取"跨场景最小值"，TGSIM/SUMO 取"均值" | **P1** | **DECIDE** | 0.084 vs 合并均值 0.096；方案 1/2/3 |

---

## C. 事实错误——**补丁已写好**

| # | 问题 | 严重度 | 状态 | 证据 / 动作 |
|---|---|---|---|---|
| C1 | §4.1 写 "0.084 in sixteen runs and 0.167 in four"，数据是 **17 / 3** | **P1（事实）** | **FIX-READY**（E3） | 逐局可数 |
| C2 | §5.3 的 "near 0.32" 在扫描表里无对应行，且与 Fig.2 的 0.39 冲突 | P1（事实） | **FIX-READY**（E7） | 扫描表 8 行 |
| C3 | 论文 OTF 出处指向 2023 学位论文，未引两篇期刊版先例 | **P0（引用完整性）** | **FIXED** | Round 06；[1][2] 已就位 |

---

## D. 贡献与证据强度——**结构性，需决策**

| # | 问题 | 严重度 | 状态 | 证据 / 动作 |
|---|---|---|---|---|
| D1 | **全文没有任何外部基线**（无 PID / MPC / 参照控制器），只有 OTF 开/关两臂 | **P0（门槛）** | **FIX-READY（Round 21：代码就绪，运行待授权）** | 稿件 grep `PID/MPC/baseline` = 0 命中；`src/` 无基线实现；`configs/p1/baseline_{pid,mpc,td3}.yaml` **三个配置都在但均为 `runnable: false`**，理由是"CARLA 未建"——该阻碍已过期（CARLA 已打通） |
| D2 | 贡献强度不足以支撑 T-IV Regular | **P0（门槛）** | **DECIDE** | Round 15 九行对照 + 判断矩阵；路线 A/B/C/D |
| D3 | C3（"重建 Δv"）是间接证据，非直接观测 | P1 | **OPEN** | Round 09 无 Δv 组仍无效；Route C 可补 |
| D4 | 无外部/真实闭环（TGSIM 仅开环） | P1 | **已披露**（Limitations 6） | — |
| D5 | "两次换道"的 CARLA 探针无产物 | P2 | **U** | Round 13；SUMO 探针不能替代 |

---

## E. 工具与流程——已修复

| # | 问题 | 状态 | 证据 |
|---|---|---|---|
| E1 | 转换器不幂等（重跑丢引用） | 部分修复（补了 `Huang` 条目；幂等未做） | Round 06 |
| E2 | R1 只改 markdown 标题，PDF 标题不变 | **FIXED**（R1b） | Round 18 |
| E3 | E6 会重复 "almost exactly." | **FIXED**（锚点延伸） | Round 19 |
| E4 | 我自己三次误设比较容差 | **FIXED** | Round 12 |
| E5 | 我用相关系数错误论证"场景无关" | **FIXED**（改配对统计） | Round 03 |
| E6 | 我在给出实验建议前没算功效下界 | **FIXED**（`audit_design_power.py`） | Round 16 |

---

## 统计口径（截至 Round 20）

| 状态 | 条数 |
|---|---|
| **FIXED**（已落盘并验证） | 13 |
| **FIX-READY**（补丁待批准） | 3（B5、C1、C2 — 均在 E1–E7 内） |
| **DECIDE**（需作者裁决） | 6（B1、B2、B3、B4、B6、D2） |
| **OPEN / NEW** | 3（D1、D3、D5） |

**结论**：数据与统计线（A 组）**已全部关闭**；剩余 9 条中有 6 条是**选刊/定义决策**，
真正新发现的实质问题是 **D1（无外部基线）**。

---

## F. 指标与执行真实性（Round 23–24 新增）

| # | 问题 | 严重度 | 状态 | 证据 / 动作 |
|---|---|---|---|---|
| F1 | `jerk_peak` 恒为 **1571.18**（150/150 臂-局），在代价中贡献 15.71 = 均值的 51.1% | **P1** | **CONFIRMED（E）** | 实机探针：第 4 帧 accel +19.6 → −43.25，/0.04 s = 1571.2；属开局伪迹，配对差中抵消 |
| F2 | 稳态车距 ≈130 m vs 参考 47 m（`gap − (1.5v+5)`） | P1 | **CORRECTED** | 上轮称『跟踪失效』过重；实为工况与参考车头时距错配 |
| F3 | **实际控制 25 Hz**（`round(2.5)=2`），论文写 20 Hz | **P1（事实）** | **FIXED（R31）** | 实测平均控制周期 0.0400 s；1500 步/局；源码 4 处已改 25 Hz，PDF 无 20 Hz 残留 |