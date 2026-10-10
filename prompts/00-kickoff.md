# 立项启动（Kickoff）—— 可执行指令

> 触发：`读 @auto-driving/prompts/00-kickoff.md 并执行`
> 前置：已装载技能 `science-top-journal-writing`；已读 `auto-driving/AGENTS.md` 与 `papers/portfolio.md`。
> 本文件是**任务指令**，不是常驻约定；硬约束以 `auto-driving/AGENTS.md` 为准。

## 0. 先复述，后提问

用 ≤6 行复述硬约束（P1 主张上限 / 开环≠闭环 / TD3 基线标注 / 他人数字不可直接对比 / ODD / 统计口径），
然后问我最多 3 个必要问题：① 学位论文数据与 TD3 代码是否可得、在哪；② CARLA 环境与 GPU 现状；③ 本轮优先级（P1 还是先补资产）。
**在我回答前只做第 1 步，不得撰写正文。**

## 1. 资产盘点表（先做）

`资产｜出处（学位论文/公开数据/自建）｜本机是否已有｜可用性 A–D｜缺口｜最小补法`

覆盖：OTF 定义与动态时间窗函数（第三章）、分层递阶评估分级标签（第四章）、TD3 模型与权重、实车数据（毫米波雷达+GPS、CAN、高速/城市双工况）、四类工况场景库、CARLA 环境与 Town04 改造地图、nuScenes/Waymo 访问、GPU 算力。
学位论文细节可从 `sources/thesis-huang2023.fulltext.txt` 用 grep 检索（**不要整篇读入**，133 页 / 30 万字符）。
另外读 `sources/references-list.txt`，核对清单里 30 篇文献的 venue 标注（📄 的 arXiv 条目与 workshop 条目必须逐条核验正式发表状态），产出**"待核验引用清单"**（论文｜清单标注｜核验结论｜建议引用版本｜依据）。
两篇锚点原文在 `sources/drivedreamer-2023.fulltext.txt` 与 `sources/drive-as-you-speak-2023.fulltext.txt`（已提取全文，可 grep），需要时再读。
我没提供的资产一律标 `[待确认]`，不要替我假设。

## 2. P1 二十四周计划

每周一行：`周次｜目标｜交付物｜判据｜依赖｜风险`。必须覆盖：环境与基线（PID/MPC/TD3）、Φ_OTF(t) 实现、CfC 控制器、A1–A5 消融、长尾四项、MCU 部署验证、论文撰写与投稿。
标出关键路径，并单独给"**第 1 周就能开始的 5 件事**"（每件 ≤1 天可见结果）。

## 3. 仓库骨架建议

目录｜放什么｜谁生成数字。命名遵守 `results/<paper>/<experiment>_<scenario>_<seedset>.json`。
只给目录与 README 规划，**不要写实现代码**。

## 4. P2 隐性关键路径预告

给出 OTF 自动标注流水线的启动时点（第 2 个月）与最小可行版本范围，避免 P2 因标注卡住。

## 5. 风险登记表

`风险｜触发条件｜影响｜早期信号｜缓解｜降级方案`。至少含蓝图三条（P1 增益复现、P2 标注成本、P5 野心控制），并补充你在盘点中发现的新风险。

## 6. 产出

写入并声明：`auto-driving/audit/00-asset-inventory.md`、`01-p1-plan.md`、`02-repo-skeleton.md`、`03-risk-register.md`；
若状态有变，先更新 `papers/portfolio.md` 再改稿。
结尾给 3 个下一步（推荐在前）与最低成本路径。
