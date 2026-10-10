# 入口脚本（scripts/）

**薄壳，不含逻辑。** 逻辑在 `src/`。

| 目录 | 用途 | 产物落点 |
|---|---|---|
| `smoke/` | 冒烟与管线自检：验证契约连通（如"配置 → 跑通 → 产出符合 schema 的 JSON"） | `runs/smoke/`（**永不可引用**） |
| `run/` | 真实算例入口；**只接受 `configs/<paper>/*.yaml` 路径**，不接受手敲参数 | `runs/real/` + `results/` |

## 两条规则

1. `run/` 必须先校验配置存在且 hash 可算，否则拒绝启动。
2. 产物写 `results/` 前必须过 [`configs/schema/results.schema.json`](../configs/schema/results.schema.json)；`mode` 字段由脚本决定，**不允许手工改成 `real`**。

## smoke/ 下已有的规格与脚本

| 文件 | 内容 | 状态 |
|---|---|---|
| [`smoke/check_seed_independence.SPEC.md`](smoke/check_seed_independence.SPEC.md) | 种子独立性自检的**判定逻辑规格**（CHECK-1 划分是否随种子变化 / CHECK-2 实体跨折 / CHECK-3 预处理先于划分 / CHECK-4 OTF 窗是否含未来信息），含退出码与稿件措辞对应表 | 规格；实现属 W2 |
| [`smoke/check_progress_snapshot.mjs`](smoke/check_progress_snapshot.mjs) | **进度快照一致性校验**：比对 `AGENTS.md` §0.1 的 ```text 常量块与磁盘实况（`results/` json 数、`src/` 代码文件数、`portfolio.md` 状态列、环境锁 SUMO 版本 vs 二进制实测）。4 项全过 exit 0，任一不符 exit 1 | **已实现并实测**（2026-10-08） |
| [`smoke/check_branch_freshness.mjs`](smoke/check_branch_freshness.mjs) | **分支登记新鲜度校验**：读 `AGENTS.md` §0 表的「最后更新」列，与 `branch-watch` 块派生的产出路径**最新 mtime** 比对，落后 > 容忍天数即 stale。校验表解析、watch 解析、覆盖性、路径存在性、逐分支新鲜度 | **已实现并实测**（2026-10-08） |

`check_progress_snapshot.mjs` 用法与约定：

```bash
node scripts/smoke/check_progress_snapshot.mjs            # 人类可读
node scripts/smoke/check_progress_snapshot.mjs --json     # 机器可读
node scripts/smoke/check_progress_snapshot.mjs --quiet    # 只输出结论
node scripts/smoke/check_progress_snapshot.mjs --root <项目根>

node scripts/smoke/check_branch_freshness.mjs             # 默认容忍 3 天
node scripts/smoke/check_branch_freshness.mjs --tolerance 1
```

**`check_branch_freshness.mjs` 的一个内在张力（已用忽略集处理）**：主支与 SUMO 分支的 watch paths 里含 `scripts/`、`configs/env`，而这两个脚本自己就住在那——若不排除，脚本一落盘就把对应分支"变新"，导致**永远不报 stale（自我实现的新鲜）**。因此脚本默认把 `scripts/smoke/` 加入每个分支的忽略集，并在文件头注明。

- **只用 Node 内置模块**，不装依赖；已在本机 Node v24.15.0 实测。
- 退出码：`0` 一致 / `1` 不一致或输入缺失 / `2` 用法错误。
- 不一致时二选一：磁盘是对的 → 改 `AGENTS.md` §0.1 常量；快照是对的 → 把磁盘改回去。
- 已知坑（脚本内已修正并留注释）：`new URL(...).pathname` 会把路径空格编码成 `%20`，必须用 `fileURLToPath`。
