# 规范与清单（docs/）

**这些文件给人读，不是数字来源。** 数字只来自 `results/`。

| 文件 | 内容 | 状态 |
|---|---|---|
| `odd.md` | ODD 声明：道路类型、车道数、交通构成、天气、速度区间 | 待写（从学位论文第 2 章抽取） |
| `metrics.md` | 每个指标的定义、单位、采集平台与档位要求 | 待写 |
| `scenario-taxonomy.md` | 四类工况 + 长尾四类的判定规则（可执行伪代码级） | 待写 |
| `data-licenses.md` | 学位论文数据许可、nuScenes/Waymo 条款、可否再分发 | 待写 |

## 命名取值域（`results/` 文件名）

| 字段 | 取值域 |
|---|---|
| `<paper>` | `p1` … `p5` |
| `<experiment>` | `main_otf_cfc`／`baseline_pid`／`baseline_mpc`／`baseline_td3`／`ablation_a1`…`a5`（+ 变体后缀） |
| `<scenario>` | `highway-mixed`（主）；长尾 `lead-brake`／`cutin-hard`／`platoon-exit`／`aggressive-flow`；辅助 `city-expressway-replay` |
| `<seedset>` | `s1`…（指向 `configs/seeds/seedset_s1.yaml`） |

## ODD（当前口径，待 `odd.md` 细化）

高速公路主线 · 多车道 · 人工与自动混行 · **晴朗天气**（学位论文实车数据仅在晴天采集，见 `sources/thesis-huang2023.fulltext.txt` L1986、L2002）· 单向三车道为主、自车保持中间车道。

**跨 ODD（交叉口、城市普通道路、环形道路、恶劣天气）结论无效。**
