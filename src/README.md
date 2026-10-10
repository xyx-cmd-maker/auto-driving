# 模块实现（src/）

**谁生成数字写在这里。** `src/` 不写数字（数字只落 `results/`），`results/` 不出结论。

| 模块 | 职责 | 输出 | 状态 |
|---|---|---|---|
| `otf/` | OTF 事件判定、真值校验、P1 场景驱动 | `results/p1/*.json` | **部分已建**：`sumo_otf_smoke.py`（冒烟链路）、`check_otf_counting.py`（真值校验，两遍重算 72=72）、`run_p1_scenarios.py`（**四类工况 + 探测车速扫描**，五档窗口 × 5 种子，输出分箱占比分布）。**正式 OTF 库（固定窗 + 动态窗函数）仍待建（W1–W2）** |
| `eval/` | 分层递阶评估：安全层 TTC/THW → 效率层 OTF 适宜性分级 | 分级标签 | 待建（W3） |
| `ctrl/` | PID / MPC / TD3（`cited` 或 `reproduced`）/ OTF-CfC 控制器 | 控制指令 | 待建（W13+，需算力） |
| `envs/` | CARLA 场景封装、实车数据**回放器**；SUMO 场景生成 | 环境接口 | **部分已建**：`sumo_highway_scenario.py`（高速主线路网 + 元数据）。CARLA 与回放器待建（W12+） |
| `metrics/` | 指标口径的**唯一实现**：跟车 RMSE、a²积分、Jerk 峰值、车道居中偏差、前轮转角方差、延迟、内存 | 指标字典 | 待建（W16） |
| `stats/` | 种子聚合、mean±std / 95% CI、Wilson 与 Clopper-Pearson、等价/非劣检验、**种子独立性自检** | 聚合结果 + 自检报告 | **部分已建**：`check_seed_independence.py`（按 `scripts/smoke/check_seed_independence.SPEC.md` 实现 CHECK-1..4，含随机划分零分布）；聚合/区间估计仍待建（W3） |
| `plots/` | 出图脚本（每图一个脚本，保证可从 json 重生成） | 图 | 待建 |

## 命名护栏（硬约束）

- `envs/` 中回放相关的一切命名**必须含 `replay`**；禁止出现 `real_*`、`vehicle_*` 之类暗示实车的命名——对外措辞上限是"在 CARLA 与真实数据回放中"（`AGENTS.md` §1）。
- `ctrl/` 中的 TD3 必须显式标注来源：`cited`（学位论文实现，原样引用）或 `reproduced`（我们复现，附协议与差异清单）。**不得混称。**
- `metrics/` 是唯一口径实现；其他模块不得自行计算指标。
