# AGENTS-PROJECT.md — 项目进程同步（目的 · 成果形态 · venue · 进度）

> **本文件与 `AGENTS.md` 效力相同**（文件族规则见 `AGENTS.md` 开头的表；方法类规则见 `AGENTS-NORMS.md`）。
> 建立：2026-10-11（用户指定：每隔一段对话同步一次项目进程，防止长对话遗忘与局部最优）。
> **每轮收工必须更新第 4 节的快照**；数字必须来自文件或命令输出，**不来自记忆**。

---

## 1. 项目目的（一句话与三层展开）

**一句话**：以黄梦圆（2023）提出的**超车频次（Overtaking Frequency, OTF）**为锚点，把"交通社会压力"这一**可解释标量**推入现代自动驾驶栈的三条赛道，产出五篇论文。

| 展开 | 内容 |
|---|---|
| 要解决的问题 | 端到端模型缺可解释的交通流社会压力表征；OTF 在学位论文里止步于**事后分类评估**，未进入控制；语言指令缺可定量 grounding 的物理量 |
| 方法主张 | OTF **升维**（势场化、预测化）＋**下沉**（注入 ODE 边界条件）；"**大胆决策、小心修正**"（VLA 阶梯指令 10 Hz ＋ LNN 连续积分 100 Hz ＋ 安全隔离层） |
| 不做什么 | **不训练统一大模型**；LNN 与 Transformer **不用直接 BP 串联**；不声称车规合规；不把仿真/回放写成实车 |

## 2. 要得到的结果（成果形态）

### 2.1 五篇论文（台账 `papers/portfolio.md` 是唯一状态来源）

| # | 代号 | 层 / 定位 | 周期（相对周） | 当前状态 |
|---|---|---|---|---|
| P1 | **OTF-CfC** | LNN 控制（MVP 首发）：OTF 势场作 ODE 边界条件 ＋ CfC 100 Hz 控制器 | 0–6 月 | 蓝图完成；**前提部分满足**（GPU 有；缺实车数据、CARLA、CUDA torch）；已有 36 份 SUMO 合成算例，含 A1 信息量版 |
| P2 | **SocialDreamer** | WLA 预测：OTF 标量 → BEV 连续标量场（新**条件模态**） | 3–9 月 | 蓝图完成；定位句已修正 |
| P3 | **TalkOTF** | VLA 决策：语言 → OTF 定量 grounding ＋ 指令合法性检查器 | 6–12 月 | 蓝图完成；需自建 500–1000 条配对数据 |
| P4 | **IsoLNN** | 安全隔离（横贯）：连续可导控制器的物理可行性筛查 | 9–15 月 | 蓝图完成；依赖 P1 控制器 |
| P5 | **AdjointStack** | 全栈训练（旗舰）：混合频率伴随敏感度联合微调 | 9–18 月 | 蓝图完成；推导受阻时降级为"两两模块联合微调" |

### 2.2 投稿材料（每篇论文的完整交付集）

稿件（英文）｜cover letter｜rebuttal / response letter｜**Data & Code Availability 声明**（含"原始数据不可再分发"的表述）｜AI 使用披露｜图表源文件（可由 `results/` 重生成）

### 2.3 可复用资产（论文之外的交付）

`results/<paper>/*.json`（数字唯一来源）｜`configs/**`（可复现配置与结果 schema）｜`literature/**`（检索日志＋引用库＋精读笔记＋`refs.bib`）｜`audit/**`（盘点、风险、引用核验、组会材料）｜SUMO→OTF 采集链路与文档（`docs/sumo-*.md`、`docs/otf-distribution-and-paper-comparison.md`）

## 3. venue 策略（多轮自查后的决定）

> **依据**：蓝图 `sources/blueprint-papers-v1.1.txt`（L79–108）＋ `papers/portfolio.md` ＋ 本库已核验的 venue 事实（`audit/第一次组会/05-citations.md`）。
> **标注置信度**：目标期刊的**范围与影响因子为【需核实】**——本轮取 IEEE Xplore 被拦（HTTP 202 无正文），**投稿前必须逐刊核对官方 Aims & Scope 与作者指南**，不得凭记忆写进 cover letter。

### 3.1 分层与理由

| 论文 | **首选** | **备选** | **会议轨** | 为什么这样排 |
|---|---|---|---|---|
| P1 | **IEEE T-ITS** | **IEEE T-IV**（更贴"智能车"） | **IEEE IV**（可先投会议再扩刊）／ICRA | T-ITS 覆盖交通流＋控制＋安全，与"混行编队＋OTF 交通流度量"最贴；ICRA 偏机器人本体，P1 的贡献不在机械 |
| P2 | **IEEE TPAMI** | **IEEE T-ITS** | **CVPR-W / ICCV-W**（先占位） | 世界模型＋生成属 CV 主流；TPAMI 容得下方法＋大规模实验；workshop 用来抢时间窗 |
| P3 | **IEEE TVT** | **IEEE T-ITS** | **IROS** | TVT 收车辆层面的语言/决策集成；IROS 收机器人交互 |
| P4 | **IEEE T-ITS**（安全/可靠性专栏） | **DASC** | DASC | 与"独立隔离＋SOTIF 思路"最贴；DASC 是 AD 安全社区主场 |
| P5 | **NeurIPS** | **RSS**（系统/机器人视角） | RSS／ICLR | 伴随法与混合系统训练属 ML 方法论；RSS 收系统级贡献 |

### 3.2 venue 纪律（硬要求，写稿前逐条过）

1. **workshop ≠ 正式发表**：CVPR-W/ICCV-W 只能表述为"在 … Workshop"，**不得**写成主会（本项目已因 Drive as You Speak 的 venue 定性吃过一次教训）。
2. **同一工作不得重复发表**：会议版 → 期刊版必须**实质扩展**（新增实验/理论/系统），并在 cover letter 中说明扩展点。
3. **预印本策略**：发布 arXiv **前**先查目标刊政策与专利公开时序（多数法域要求**申请先于公开**）——【需核实：IEEE 预印本政策原文，本轮 PDF 抓取失败，投稿前查官方页】。
4. **引用格式**：IEEE 格式优先引正式发表版（如 DriveDreamer→ECCV 2024、DriveGPT4→RA-L 2024、DiLu→ICLR 2024）。
5. **投稿前必做**：`audit/第一次组会/05-citations.md` 的 `[待核实]` 字段清零；`AGENTS.md` §1 的参数量/术语口径复核；数据许可与致谢确认。

## 4. 进度快照（每轮收工更新；取数方式必须写明）

> 快照日期：**2026-10-11** ｜ 取数：读 `papers/portfolio.md` ＋ 扫描 `results/`、`src/`、`configs/` ＋ `git log`

| 类别 | 已完成 | 未完成 |
|---|---|---|
| 立项与契约 | 资产盘点、仓库骨架、结果 schema、环境锁、风险登记 12 条、24 周逐周计划；**`configs/p1/` 已冻结**（6 份：params.frozen / main_otf_cfc / 三基线含 `baseline_td3: mode: cited` / ablation_a1） | `src/eval|ctrl|metrics` 正式实现；CfC 控制器（需算力） |
| 文献 | 30 条 venue 全量核验（17 处修正）；`literature/**` 文献图＋逐字限定语；第二次组会精读 23 篇；**P3/P4/P5 三张文献图已补齐**（各 50/50/28 条，DOI 逐条 Crossref 核验，见 `literature/p3|p4|p5/`） | P2 文献图（唯一缺口）；OpenAlex 引文展开（额度耗尽，"外部复现"列仍为"未检"）；P5 图仅 28 条——**已证实是该交叉方向文献稀缺，非检索不足** |
| 环境 | **环境前提已全部清空**：GPU（RTX 5060 8 GB / sm_120）＋ **torch 2.11.0+cu128**（11/11、6.7×）＋ **CARLA 0.9.16 装于 `D:\CARLA`**（服务端 25 s 就绪；Python 3.12.10 并装；客户端冒烟 8/8；**闭环环境 `src/envs/carla_town04.py` 自检 8/8**：前车 50.9 m、场景注入 500 样本、实时倍率 2.27×）＋ **SUMO 1.27.1** | **学位论文实车数据**（唯一实质缺口，申请函待发）；**闭环 A1 的 `train_cfc.py` 训练循环**（环境、CfC 单元、指标三件已就位） |
| 工具与数据 | `src/ctrl/cfc.py`（CfC 单元，自检 11/11）、`src/eval/metrics.py`（七项指标，自检 8/8）、`src/envs/carla_town04.py`（Town04 闭环环境，自检 8/8）、`src/otf/otf_core.py`（OTF 唯一实现）；`results/p1/` **36 份算例**；**A1 信息量版负结果已落盘**（见 §8） | 实车数据（申请函待发，条款已补）、TD3 代码/权重、`train_cfc.py`、与论文的严格对拍 |
| 版本管理 | **git 已落地并已推送**：私有仓库 `github.com/xyx-cmd-maker/auto-driving`（本地/远程同 SHA，10 次提交） | GitHub 归属的**登录态确认**（用户 2026-10-11 已确认无误）；推送偶发被重置，见 §9 |
| 组会材料 | 第一次组会 docx＋PDF；第二次组会 docx＋PDF；**A1 结论文件 `audit/第一次组会/06-a1-otf-information-bound.md`** | 第二次组会正文两处 `【待填】` |

**待用户裁决（阻塞）**：① 起始日（相对周起算点）与各论文投稿截止；② P1 是否补报振荡阻尼比 g_p 与交通流稳定性 f_flow；③ P2 是否因 §8 的负结果调整定位（是否继续假设"OTF 可升维为可预测势场"）；④ **是否并装 Python 3.12 以启用 CARLA Python 客户端**（官方 wheel 仅 cp312，本机 3.14/3.13 实测不可用）。

**当前最关键的一件事**：**据 §8 的 A1 边界结论重排 P1 的 claim 与 P2 的假设**——不是继续补实验。P1 的卖点须改为"可解释性 + 零额外传感器成本"，P2 必须为"势场比标量更可预测"给出机制性理由。

## 5. 术语表（写稿必须一致）

> ⚠️ **2026-10-11 叙事修正（由 A1 负结果触发，见 §8）**：P1 的卖点**不得**建立在"OTF 提供前瞻性/预测增益"上。"可解释性 + 零额外传感器成本"由"备选退路"**升为第一顺位卖点**。

| 术语 | 本项目定义 | 禁止用法 |
|---|---|---|
| **OTF** | 固定时间窗内自车相邻车道**超车数 − 被超车数**（黄梦圆 2023 第 3 章） | 不得写成预测量；不得省略"窗内已发生事件"这一定性 |
| **动态时间窗** | 窗长随车速、速度差、流量变化（论文第 3.2.2 节，**模拟器** 40 名驾驶人称定） | 不得说成实车拟合 |
| **分层递阶评估** | 安全层 TTC/THW → 效率层 OTF 适宜性分级 | 不得只写"OTF 分级" |
| **Φ_OTF(t)** | 把 OTF 推广为时间连续势场，作 ODE 的边界条件 | **不宜**自称 physics-informed（用 structure-/prior-informed 或 boundary-conditioned） |
| **ODD** | 高速公路主线 · 多车道 · 人工与自动混行 · **晴天** | 跨 ODD 结论无效 |
| OTF 增益 | **+1.0~+5.5 个百分点（分类器准确率，论文报告值，未经我们复现）** | 不得写"1.0–1.7%"；不得写成控制性能 |

## 6. 风险与未完成项索引

- 风险登记（12 条，含 R20 指标无可对标物）：`audit/第一次组会/03-risk-register.md`
- 资产与缺口：`audit/第一次组会/00-asset-inventory.md`
- 引用待核实项：`audit/第一次组会/05-citations.md` §4
- 已知坏链 2 条（`literature/meeting2/03-链接清单.md` → `../../scripts/check_links.mjs` 不存在）
- 数据申请与伦理：`audit/第一次组会/04-data-request-and-ethics.md`

## 7. 同步检查清单（每轮收工前逐条打勾）

1. `papers/portfolio.md` 的"当前状态"是否与本文件 §4 一致？
2. 新增/搬动/重命名文件是否已反映到 §4 与 `AGENTS.md` §0 分支登记（含"最后更新"列）？
3. `git status` 是否干净？本轮改动是否已提交？
4. 快照常量是否仍与实测一致？→ `node scripts/smoke/check_progress_snapshot.mjs`
5. 分支登记是否过期？→ `node scripts/smoke/check_branch_freshness.mjs`
6. 结论里是否标了 `【确定】/【推测】/【需核实】`？反证问是否回答？

---

## 8. A1 信息边界结论（2026-10-11，**影响 P1/P2 叙事**）

**完整结论与限制见 [`audit/第一次组会/06-a1-otf-information-bound.md`](audit/第一次组会/06-a1-otf-information-bound.md)。**

| 项 | 内容 |
|---|---|
| 实验 | `ablation_a1_otf-info`（合成版 A1 = OTF 的**预测信息增量**，非闭环控制版） |
| 来源 | `results/p1/ablation_a1_otf-info_highway-mixed_s1.json`（`mode: real`、`provenance: ours-reproduced`） |
| 结果 | 4 配置下 **\|ΔAUC\| ≤ 0.0016**，符号随跟驰模型/窗型**翻转** → 预注册判据（符号一致）**未通过** |
| 关键对照 | **跟驰模型**造成的 AUC 差异 **0.0749**，是 OTF 最大效应的 **49 倍** |
| 等级 | **C（仿真）**；措辞上限"在 SUMO 合成交通流中" |
| 对 P1 | 卖点改为可解释性 + 零额外传感器成本；**不得**声称前瞻性或预测增益 |
| 对 P2 | **风险上升**：P2 假设 OTF 可升维为可预测势场；若 OTF 自身不可预测，P2 须给出"势场比标量更可预测"的机制性理由 |
| 对 P4 | 不受影响（P4 用 OTF 做**后验**指令筛查，不依赖前瞻性） |
| 明确未测 | 闭环控制效用、真实数据、CARLA —— 前者因**无数据**、后者因**环境未建**；**注意：算力与 CUDA 工具链已就绪**（GPU 实测可用、torch 2.11.0+cu128 验证通过），不得再以"无 GPU／无算力"为由外推 |

---

## 9. 本机到 GitHub 的连通性（2026-10-11 实测，**推送失败时先看这里**）

**症状**：`github.com:443` 的 DNS 解析到境外 IP（如 `20.205.243.166`）会**连接超时**；即使钉到可达 IP，TLS 通道也会**间歇被重置**（`Recv failure: Connection was reset`）。`api.github.com` 一直可用（`web_fetch` 与 API 调用正常）。

**绕行方法（已验证可用，无需管理员、不改 hosts）**：

```powershell
# 1) 探测哪些 GitHub 边缘 IP 可达
foreach ($ip in '140.82.112.3','140.82.112.4','140.82.113.3','140.82.114.3','140.82.121.3','4.237.22.38','20.27.177.113') {
  $c = New-Object System.Net.Sockets.TcpClient
  try { $iar = $c.BeginConnect($ip,443,$null,$null)
        if ($iar.AsyncWaitHandle.WaitOne(3000) -and $c.Connected) { "$ip 可达" } else { "$ip 超时" } } finally { $c.Close() }
}

# 2) 用 http.curloptResolve 把主机名钉到可达 IP（保留 SNI/Host，TLS 校验正常）
git -c http.curloptResolve=github.com:443:140.82.114.3 push origin main

# 3) 成功后写回仓库 local 配置（仅本仓库，不动全局）
git config --local http.curloptResolve github.com:443:<可达IP>
```

**注意事项**
- **IP 会失效**：同一 IP 可能几分钟前可用、之后被重置 → 失败就换下一个 IP 重试；当前写入配置的 IP 记录于此：`140.82.114.3`（2026-10-11）。
- **本地提交不会丢**：推送失败只影响远程同步；`git log` 与工作区完好，网络恢复后 `git push` 即可。
- 若系统代理恢复监听（注册表配的是 `127.0.0.1:7897`，实测该端口**未监听**），改用代理更稳：`git -c http.proxy=http://127.0.0.1:7897 push origin main`。
- **不要**把这项工作当成常态：它只是网络绕行，与研究内容无关；**不要**据此改动任何研究口径。

