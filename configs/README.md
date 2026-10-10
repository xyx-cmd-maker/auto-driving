# 实验配置（configs/）

**每个实验先有配置，`scripts/run/` 不接受手敲参数。**

| 路径 | 内容 |
|---|---|
| `env/local-cpu.lock.yaml` | 本机现状：CPU-only，用于自检与规则层复现 |
| `env/cloud-gpu.lock.yaml` | 云端算力：**未定供应商，字段留空** |
| `p1/*.yaml` | P1 的主实验、四个基线、A1–A5 消融 |
| `p2/`…`p5/` | 后续论文（暂空） |
| `seeds/seedset_s1.yaml` | 交通流 / 初始化种子集合，**≥5 个**（`AGENTS.md` §4） |
| `schema/results.schema.json` | `results/*.json` 的必填字段契约（**字段只增不改**）；`notes.seed_independence` 为新增必填项 |

## 种子独立性（R2 缺口，硬要求）

`seeds` 只要求"≥5 个"，**不保证独立**：若 5 个种子共用同一份训练/测试划分，统计上等价于 n=1。因此每份配置与每条结果都必须交代：

| 字段 | 取值 | 说明 |
|---|---|---|
| `split_policy` | `by-time` / `by-entity` / `by-seed-holdout` | 时序数据按时间切分；禁止随机打散 |
| `entity_group` | `vehicle` / `drive-run` / `scene` | 同一实体不得跨折 |
| `verified` | 布尔 | **只有 true 的结果可引用**；由 `scripts/smoke/check_seed_independence.py` 填写。**任一检查为 `not-run` 时必须为 `false`** |
| `partial_scope` | 数组 | 未执行的检查项（`CHECK-1`…`CHECK-4`）；非空时 `verified` 必须为 `false` |
| `check_script` | 路径 | 自检脚本位置，保证可复跑 |

**阈值不写死**：Jaccard 的通过线由**随机划分的零分布**按实体池大小 N 与每折实体数 k 计算（精确超几何或固定种子的蒙特卡洛），因为固定阈值在实体池小的时候几乎不触发、大的时候又过松。算法见规格 §4.2。

自检至少覆盖三条泄漏检查：实体跨折、特征含未来信息（**OTF 是滑动窗内已发生事件**，必须明确窗右端点相对预测时刻的位置）、预处理在划分之前完成。

**判定逻辑写在 [`../scripts/smoke/check_seed_independence.SPEC.md`](../scripts/smoke/check_seed_independence.SPEC.md)**（四项检查 + 退出码 + **稿件措辞对应表**：划分不随种子变化时只能写 "random initializations"，不得写 "independent partitions"）。实现属 W2。

## P1 配置清单（待填）

| 配置 | experiment 名 | 说明 |
|---|---|---|
| `baseline_pid.yaml` | `baseline_pid` | 基线① |
| `baseline_mpc.yaml` | `baseline_mpc` | 基线②（线性化车辆模型） |
| `baseline_td3.yaml` | `baseline_td3` | 基线③——**必须填 `mode: cited \| reproduced`**（`AGENTS.md` §1） |
| `main_otf_cfc.yaml` | `main_otf_cfc` | 本文方法 |
| `ablation_a1.yaml` … `a5.yaml` | `ablation_a1`…`a5` | 一次只改一个因素；须记录失败设定 |

## 公平性字段（写入每份配置）

同等可用信息（**不得给本方法特权输入**）＋ 同等调参预算与训练轮次 ＋ 同一 CARLA 地图版本 ＋ 同一组交通流随机种子。
