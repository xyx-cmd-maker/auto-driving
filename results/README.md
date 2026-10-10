# 结果目录（results/）——数字唯一来源

```
results/<paper>/<experiment>_<scenario>_<seedset>.json
```

| 规则 | 说明 |
|---|---|
| 写入者 | **只有 `scripts/run/`**；手工创建的文件一律视为不可引用 |
| 结构 | 必须通过 [`configs/schema/results.schema.json`](../configs/schema/results.schema.json) |
| 可引用条件 | `mode: "real"` ＋ `config_path`/`config_hash` 可追溯 ＋ `seeds` ≥5 ＋ `notes.seed_independence.verified: true`（任一检查 `not-run` 时必须为 false） |
| 禁引用 | `mode: "smoke"`（自检/调试/降级档位）；`runs/smoke/` 下的一切 |
| 版本管理 | 靠 git，不靠在文件名里写 v2/final/日期 |
| 未运行的数字 | 写 `{{占位符}}`，**绝不编造** |

## 写入者例外（2026-10-08）

上表写"只有 `scripts/run/` 写入"。**当前实际写入者是 [`src/otf/run_p1_scenarios.py`](../src/otf/run_p1_scenarios.py)**——因为 P1 的 SUMO 合成数据链路属于 W1–W10 的 CPU 线，尚未按最终形态收进 `scripts/run/`。这是**有意的临时安排**，不是契约失效：脚本同样产出符合 schema 的 JSON，且 `config_path`/`config_hash` 可追溯。**W11 之后应把入口迁到 `scripts/run/`**（记在 `audit/第一次组会/01-p1-plan.md`）。

## 当前内容

| 文件 | 内容 |
|---|---|
| `p1/main_otf_cfc_{cutin,none,lead-brake,lead-exit}_highway-mixed_s1.json` | **四类工况**的合成 OTF 真值，每个文件含**全部 5 个种子**的逐种子明细 + 跨种子**分箱占比分布**（对应论文表 3.3–3.7 的口径） |
| `p1/main_otf_cfc_speed-sweep_highway-mixed_s1.json` | 探测车速扫描（12 / 19 / 23 / 29 m/s），用于检验 OTF **符号**是否随"自车与邻车相对车速"变号 |

**聚合量口径（重要）**：报的是**分箱占比**（bin width 0.2，与论文一致），**不是均值**。原因：单辆自车在任意窗口内的 `N_ot − N_otn` 均值恒趋于 0（窗口内配平），报均值等于报噪声；**OTF 只能在每个窗口内取值，得到序列/分布**。

> ⚠️ 全部为 **SUMO 合成交通流**（证据等级 **C**），**不是** CARLA、更不是实车；任何引用必须写成"在 SUMO 合成交通流中"（`AGENTS.md` §1/§2）。

命名的取值域见 [`../docs/README.md`](../docs/README.md)。
