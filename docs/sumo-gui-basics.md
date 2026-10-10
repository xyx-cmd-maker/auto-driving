# SUMO GUI 操作路径（给人照着点）

> 定位：这是 [sumo-basics.md](sumo-basics.md) 的**图形界面视角**配套文档。前者覆盖命令行 / TraCI / OTF 采集链路，本文覆盖"在 GUI 里点哪里"。
> 适用版本：本机实测 **SUMO 1.27.1**（`D:\SUMO\sumo-1.27.1`）。菜单名以英文界面为准。
> 本文所有路径与参数均在 2026-10-08 实机验证。

---

## 0. 三个可用的入口（桌面快捷方式）

| 图标 | 作用 | 说明 |
|---|---|---|
| **SUMO GUI (sumo-gui)** | 直接开仿真界面 | **空白启动**，需自己载入 `net` / `sumocfg` |
| **SUMO NetEdit (netedit)** | 直接开路网编辑器 | **空白启动**，需自己载入或新建路网 |
| **SUMO 示例 · 打开编辑器** | 双击即载入 `demo.net.xml` | 想看东西先用这个 |
| **SUMO 示例 · 跑仿真** | 双击即跑 `demo.sumocfg`（带 `--delay 100`） | 约 1 分钟看到车辆动画 |

> ⚠️ **空白启动是正常的**，不是没装好。netedit / sumo-gui 不加载文件时就是一块灰色画布（见 `sumo-basics.md` §4 的坑与实测记录）。

---

## 1. 在 netedit 里造一个路网

**路径**：`File > Generate Network`（`Ctrl+Shift+N`）

弹窗里填：

| 字段 | 含义 | 建议值（本项目 ODD） |
|---|---|---|
| `Grid` | 是否生成网格 | **取消勾选**（我们要的是一条直的高速主线） |
| `Number of junctions` | 节点数 | 2（直路两端） |
| `Edge length` | 路段长度 | **3000**（3 km，够跑 300 s） |
| `Number of lanes` | 车道数 | **3**（单向三车道） |
| `Speed` | 限速 (m/s) | **30**（≈108 km/h，高速主线量级） |

点 `OK` → 立刻出现路网。**注意**：这样生成的是**双向**边（对向车道也在一起），对向流在后面用 `departLane` 与方向区分。

**保存**：`File > Save Network As...` → 存成 `*.net.xml`（例：`configs/p1/sumo_highway.net.xml`）。

> 命令行等价物（更快、可脚本化）：
> ```
> netgenerate --grid --grid.number=2 --grid.length=3000 --default.lanenumber=3 ^
>             --default.speed=30 --no-turnarounds true --output-file sumo_highway.net.xml
> ```

---

## 2. 手工编辑（netedit 的三种模式）

netedit 顶部工具栏有模式切换：**Network / Demand / Data**（快捷键 `F2` / `F3` / `F4`）。

| 模式 | 能做什么 | 本项目常用动作 |
|---|---|---|
| **Network** | 画/改道路、车道、连接、信号 | 车道数不对时选中边改 `numLanes`；加/删连接 |
| **Demand** | 定义车辆类型、车流、路线 | 加 `vType`、加 `flow`、画路线 |
| **Data** | 编辑附加文件（检测器、公交站等） | 目前不用 |

**检查拓扑**：`Network` 模式下把鼠标悬停在边上，状态栏会显示 edge id / 车道数 / 限速。**连接关系**可用 `Locate > Junctions` 或直接把视图放大看交叉口的连线。

---

## 3. 载入车流并跑起来（sumo-gui）

**最省事的做法**：不要一个个文件载，直接写一个 `.sumocfg` 把路网与车流都指进去，然后：

1. 双击 **SUMO 示例 · 跑仿真**（或命令行 `sumo-gui -c demo.sumocfg`）
2. sumo-gui 启动后**不会自动播放**，需要点顶部工具栏的**播放按钮**（▶）

**关键参数：`Delay (ms)`**（工具栏中间那个框）

| Delay (ms) | 300 s 场景大约播多久 | 适用 |
|---|---|---|
| 0 | 瞬间播完（**看不到车动**） | 只想要结果文件 |
| 50 | 约 30 秒 | 快速过一遍 |
| **100** | **约 60 秒** | ← 默认，适合看动画 |
| 200 | 约 120 秒 | 逐步观察某个交互 |

命令行等价物：`sumo-gui -c demo.sumocfg --delay 100`

**缩放/定位**：滚轮缩放；`Locate > Vehicles` 可按 id 定位某辆车（调试探测车很有用）；`View > Vehicle Color` 可按类型/速度着色。

**结束时的弹窗**：`Simulation ended at time: ...` 是**正常结束**，不是错误。点 `No` 保留画面（可回看最后一步），点 `Yes` 关闭所有视图。

---

## 4. 导出记录（供事后分析）

两条路：

**路 A：写在 `.sumocfg` 里（推荐，可复现）**

```xml
<output>
    <tripinfo-output value="tripinfo.xml"/>   <!-- 每辆车一次行程的统计 -->
    <summary-output  value="summary.xml"/>    <!-- 每个时间步的全局汇总 -->
    <fcd-output      value="fcd.xml"/>        <!-- ★ 逐帧每车位置：OTF 分析要用这个 -->
</output>
```

> **★ `fcd-output` 是本项目最关键的输出**：它给出每 0.1/0.5 s 每辆车的 `(id, x, y, lane, speed)`，是与 TraCI 在线采集等价的**离线证据**。OTF 的离线复算、真值校验、以及"人工核事件"都应该基于它。

**路 B：GUI 里临时点**
`Simulation > Output` 里可勾选要写的输出；或在运行前用 `Settings > Save Configuration` 把当前设置（含输出）存成 `.sumocfg`。

**注意**：`fcd.xml` 体积很大（每车每步一行）。300 s × 数百车会到几十 MB 量级，建议只在需要复核的子场景开启。

---

## 5. 常用 GUI 快捷键（省得找菜单）

| 快捷键 | 作用 |
|---|---|
| `Ctrl+Shift+N` | 新建/生成路网（netedit） |
| `Ctrl+O` | 打开路网 |
| `Ctrl+M` | 打开 SUMO 配置 |
| `Ctrl+S` | 保存 |
| `F2` / `F3` / `F4` | netedit 切 Network / Demand / Data 模式 |
| `Ctrl+R` | netedit 重载当前路网 |
| `Space` | sumo-gui 播放/暂停（焦点在视图上时） |

---

## 6. 出问题时先查这三处

1. **底部状态栏**（sumo-gui / netedit 最下方）——错误信息在这里，比弹窗详细。
2. **`Error: Loading of network '<路径>' failed`**：多半是**把目录当文件**了，检查路径是否以 `.net.xml` 结尾（本机真实踩过，见 `sumo-basics.md` §4 坑 7 附近）。
3. **窗口标题**：`xxx.sumocfg - SUMO 1.27.1` 表示配置已载入；只显示 `SUMO 1.27.1` 表示**什么都没载**（空白态）。

---

## 7. 与 OTF 采集链路的关系（别搞混职责）

| 用途 | 用哪个 | 说明 |
|---|---|---|
| 快速看场景长什么样 | **GUI**（本文） | 交互、直观，但不产出可引用数字 |
| 批量跑五档窗口 × 5 种子 | **命令行 / TraCI**（`sumo-basics.md`） | 产 `results/p1/*.json`，唯一可引用的来源 |
| 复核某个超车事件 | **`fcd.xml` + 离线复算** | 与 TraCI 在线采集互为独立证据 |

**硬规则**：GUI 里看到的画面**不是证据**；能进稿件的数字只能来自 `results/p1/*.json`（`AGENTS.md` §2）。
