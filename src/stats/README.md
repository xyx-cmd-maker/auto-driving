# 统计模块（src/stats/）

职责：种子聚合、区间估计、等价与非劣检验、**以及种子独立性自检**。

## 必须实现的口径（`AGENTS.md` §4）

| 项 | 要求 |
|---|---|
| 聚合 | 报 mean ± std **或** 95% CI；禁用"只报最优运行" |
| 小样本 | 成功率/长尾类用 **Wilson** 或 **Clopper-Pearson**，不得用正态近似 |
| 无差异 | 必须用**等价检验（TOST）或非劣检验**，不得把 p>0.05 写成"无差异" |
| 多重比较 | 多场景/多指标并列时须校正 |
| 失败设定 | 与 `notes.abandoned_settings` 一致，不得只报成功配置 |

## 种子独立性自检（R2 缺口）

问题：`seeds` 列表有 5 个种子，不等于 5 次独立重复。若它们共用同一份数据划分，有效样本量仍是 1。

自检脚本（W2 交付，路径 `scripts/smoke/check_seed_independence.py`）必须验证三条：

> **判定逻辑已先行冻结**：见 [`../../scripts/smoke/check_seed_independence.SPEC.md`](../../scripts/smoke/check_seed_independence.SPEC.md)。其中 CHECK-1 要求判定"**划分是否随种子变化**"（成对 Jaccard），而不只是检查字段填没填——这是红队指出的关键分界线。

1. **实体不跨折**：同一 `entity_group`（vehicle / drive-run / scene）的样本不同时出现在训练与测试折；
2. **无未来信息**：OTF 是滑动窗口内**已发生**的超越事件计数，须明确窗右端点相对预测时刻的位置，否则构成标签泄漏（这与 P1 的"OTF 是否具备前瞻性"是同一个问题的两面）；
3. **划分先于预处理**：特征构造、标准化、特征选择均在划分之后。

跑通后把 `configs/seeds/seedset_s1.yaml` 的 `independence.verified` 与每条结果 JSON 的 `notes.seed_independence.verified` 置为 `true`；**未置 true 的结果不得被引用**。
