# P1 主张—数据—摘要 对齐检查（2026-10-18）

> 用户第 10 问：**"现在我们的数据和我们的主张和摘要都对的上吗？"**
> 答案分三层：**摘要还不存在**；**主张上限已写死但与当前数据方向不符**；**方法描述有 4 处与实际实现不符**（这些是最容易被审稿人一查就崩的地方）。

---

## 0. 一句话结论

**现在还不能写"OTF 提升控制性能"——数据不支持；能写的只有 C 级的中性/负结果 + 可解释性价值。**
而且**没有任何摘要或稿件存在**（`papers/` 下只有台账 `portfolio.md`），所以"对得上"目前是"没有摘要可对"。

---

## 1. 摘要与稿件：**不存在**

| 检查 | 结果 |
|---|---|
| 是否有 P1 摘要草稿 | **无**（仓库内无 `paper/`、`manuscript/`、`draft/` 目录） |
| 是否有 P1 正文 | **无** |
| 是否有图表 | **无**（连 Fig.1 都没有） |
| 现有的是什么 | 实验基础设施 + 协议 + 结果 JSON + 审计文档 |

**⇒ 所以现在谈"摘要是否对得上"是空转。但可以先把"摘要被允许写什么"锁死，这就是下面 §2。**

---

## 2. 主张 vs 数据：**当前对不上（方向相反）**

`AGENTS.md` §1 已写死 P1 红线：**不得预先声称"OTF 势场带来 X% 性能提升"**。这是对的方向。但还要看数据实际说什么：

| 证据 | 等级 | 结果 | 支持的措辞 | **不支持的措辞** |
|---|---|---|---|---|
| A1 信息量版（开环，36 份算例） | C | **负结果**：logistic AUC 0.7435 / rf 0.8649 / hgb 0.8456，12 组配置 \|ΔAUC\| ≤ 0.0045；rf 4/4 偏负 | "OTF 未显示增量预测力" | "OTF 能预测他车行为" |
| A1 闭环中量（n=4） | C（样本不足） | Δcost **2 对半**；**Δ加速度积分 4/4 为正**（OTF 更不平顺，均值 +87.2）；OTF 臂无效候选更多（50–58% vs 33–42%） | "未观察到一致改善；观察到更不平顺与更难搜索" | "OTF 改善闭环控制" |
| A1 闭环全量（20 局） | — | **进行中（1/20）** | **暂无** | **任何结论** |

**⇒ 若今天写摘要，"OTF 提升性能"这句一定对不上。**
**可写的初稿句（C 级，且需全量确认）：**

> "On a CARLA highway with mixed traffic, adding the overtaking-frequency scalar as a fourth input
> did **not** yield a consistent improvement in closed-loop following performance
> (paired per-scenario estimates; see Table X); we observed **larger acceleration-squared integrals**
> and a **higher fraction of failed policy-search candidates**, and we report both as findings rather
> than limitations."

**若全量出现"有意义更小"**，则改成正向句，但强度上限仍是 **B/C 级**（仿真、单地图、单车型）。

---

## 3. 方法描述 vs 实际实现：**4 处必须对上**（审稿人一查就崩）

| # | 若照"蓝图/直觉"写 | **实际实现** | 后果 | 必须怎么写 |
|---|---|---|---|---|
| 1 | "100 Hz 控制器" | **实际 20 Hz**（仿真 50 Hz，控制降频 1/2.5） | 审稿人复现不了，或质疑实时性主张 | 全文写 **20 Hz**，并在 Limitations 说明未达 100 Hz 的原因 |
| 2 | "natural lane changes / mixed traffic" | **脚本化 cut-in（直接置位）**，周期 4 s | 被认定为"人为制造信号" | 明确写 **scripted cut-in injection**，并讨论"事件过于规律"这一局限 |
| 3 | "we train a CfC controller" | **随机策略搜索**（12 候选/臂 + 精英保留），非 RL 训练 | 被质疑"这不是训练" | 写 **policy search with a fixed budget of 12 candidates**，不写 "trained" |
| 4 | "validated on real-world data" | **无实车数据**（唯一外部缺口） | 直接退稿级问题 | 只能写 **"in CARLA"**；实车数据到手前**不得**出现 real-world validation |

**另有一处已有纪律**：TD3 基线只写**文献报告值**（`mode: cited`），**不得**写"我们复现"。

---

## 4. 已对齐的部分（可以放心用）

| 项 | 状态 |
|---|---|
| 数字来源 | 全部结果在 `runs/p1/cases/*.json`（含 `exec` 指纹）与 `results/p1/*.json`，可指到字段 |
| 统计规范 | 种子 5、精确符号翻转 + TOST + Holm，已代码化（`--analyze`） |
| 处理变量可判定性 | `phi_nonzero_ratio` 强制落盘，实测 **8.4%–12.6%**（已激活） |
| 公平性 | 两臂共用同一组随机种子、同 12 候选预算、同代价权重 |
| OTF 术语 | 定义归属黄梦圆（学位论文），本作只做"接进控制回路"的增量 |

---

## 5. 结论与下一步

1. **现在不能写摘要正文**（没有稿件，且全量未出）。
2. **可以现在写的是"摘要的骨架 + 禁止清单"**：即上面 §2 的 C 级中性句 + §3 的 4 处订正。
3. **等全量 20 局出来**（预计 2026-10-18 下午），按 `configs/p1/a1_execution_freeze.yaml` 的结局矩阵选 claim，再写摘要。
4. **绝不能做的事**：先写"OTF 提升 X%"，再去找数据支持；或在全量里挑一个有利口径（已用预注册堵住）。
