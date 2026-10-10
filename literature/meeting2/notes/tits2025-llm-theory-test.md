# LLM 驾驶理论考试基准（英国 DVSA）｜Methodology and Benchmark for Automated Driving Theory Test of Large Language Models

- **出处**：IEEE Transactions on Intelligent Transportation Systems, vol. 26, no. 10, pp. 17013–17026, October 2025 ｜ **类型**：期刊论文（评测方法与基准；作者自述为 MobiArch 2024 会议论文 [13] 的扩展版，新增内容 >50%）
- **作者**：Dashuai Pei et al.（Dashuai Pei, Yiwen Wu, Jianhua He, Kezhong Liu, Mozi Chen, Xuedou Xiao, Shengkai Zhang, Jiawei Zheng）
- **DOI**：10.1109/TITS.2025.3571213
- **全文来源**：`literature/fulltext/meeting2/methodology-and-benchmark-for-automated-driving-theory-test-__000c83f0.txt`
- **分组**：TITS
- **证据等级初判**：C 级 — 有对照（16 个模型、固定通过线、三层评价协议）且代码数据开源，但准确率为 Temperature=0 单次采样、全文无置信区间与统计检验、无人类实测基线，属相关/测量型证据，非干预或闭环证据
- **档位建议**：D 排除 — 命中排除词表「语言模型评测」（LLM driving theory test / LLM benchmark：全文即"LLM 驾驶理论考试基准"，与 P1 控制器无接口）；加权分照常算出为 8
- **五维打分**：D1=0 D2=1 D3=0 D4=2 D5=2 → 加权 = 3·D1+2·D2+2·D3+1·D4+2·D5 = 3·0+2·1+2·0+1·2+2·2 = 8

## 1. 标题

Methodology and Benchmark for Automated Driving Theory Test of Large Language Models｜面向大语言模型的自动驾驶理论考试方法与基准

## 2. 摘要（≤400 字中文，保留关键数字与结论成立条件）

作者提出首个面向 LLM 的驾驶理论考试框架与基准，仿英国 DVSA 官方考试，含 MCQ 与危险感知两段。去重后 726 道 MCQ（DS-Text 617 题纯文本、DS-Image 109 题含图），另加 DVSA 两套标准化 50 题；危险感知用 54 段官方危险视频（官方考试 14 段），按 0.2 s 切帧、标注危险起止与递减得分。评测 16 个 LLM（11 专有 + 5 开源：GPT-4o、Claude、Gemini、Ernie、glm、Qwen、DeepSeek、MiniCPM），prompt 设「资深驾驶员」角色、只要选项字母或 0/1。GPT-4o 平均 88.21%，为唯一通过 MCQ 线（43/50=86%）者；Claude-3.5-sonnet 85.21% 未过；含图题普遍下降（GPT-4o 79.82%）。危险感知无人通过：GPT-4o 帧级 precision 19.16%、FP 1139。成立条件：仅英国题库、T=0 单次采样、纯问答无闭环。

## 3. 结论（≤350 字中文：作者结论节要点 + 关键数字 + 作者自承的局限）

通用 LLM 尚不足以承担自动驾驶辅助的全部环节：完整 MCQ 测试中只有 GPT-4o 达到通过线（88.21%），多数模型在纯文本 MCQ 上超过 86% 门槛，说明感知（含图理解）是主要瓶颈；危险感知中即便 GPT-4o 也 precision 低、误报高。作者称该框架可作为 LLM 接入关键系统前的可复现前置基准，并扩展到端侧部署与更广 AD 流水线评估。

自承局限：① 基准仅基于英国考试，全球泛化性受限；② 只测通用 LLM，未纳入领域专用模型（GPT-Driver、DriveGPT4、DriveLM）；③ 危险视频首尾无风险事件、危险时间窗受 LLM 输入长度限制（GPT-4o 为 128k tokens），可能低估对迫近危险的响应能力；④ 过保守判定归因于三点：缺驾驶专用训练、RLHF 安全偏置过罚、prompt 框架诱导过度谨慎。

## 4. 方法一句话（≤60 字，必须含「输入 → 模型 → 输出」三要素）

输入 DVSA 理论 MCQ 与危险感知视频帧 → 两段式 prompt 送 16 个 LLM → 输出选项字母、危险 0/1 判定与递减得分

## 5. 图表清单（占位符）

| 占位符 | 图/表号 | 原文图注（逐字，可截断到 100 字符） | 读图要点 |
|---|---|---|---|
| {FIG-llmtt-1} | Fig. 1 | Remote or local deployment of LLMs for V2X-assisted deci- | 部署示意图（非实验）：LLM 置于 RSU 或云端，经 V2V/V2I 为 CAV 提供 OOD 场景决策；仅支撑"理论考试应作部署前置门"的动机 |
| {FIG-llmtt-2} | Fig. 2 | Example of two multiple-choice questions from the driving theory test. | DS-Text 与 DS-Image 各一题示例，正确项标绿、错误项标红；可用于核对该基准的题型（4 选项，1 个或多个正确项） |
| {FIG-llmtt-3} | Fig. 3 | Key frames from two hazard perception test video clips. (Top row) The first set of frames shows | 两段危险感知视频关键帧（支路汇入主路前停车让行；人行横道前等待行人）；说明"developing hazard"如何界定 |
| {FIG-llmtt-4} | Fig. 4 | Comparison of openai model accuracy across different parameter | DS-Text 上 GPT-4/GPT-4o/GPT-4o-mini/GPT-3.5-turbo 的准确率—温度（Top-p=1）与准确率—Top-p（T=0）曲线；文本题波动小 |
| {TAB-llmtt-1} | TABLE I | PERFORMANCE COMPARISON OF DIFFERENT LLMS ON THE DS-TEXT | DS-Text（617 题）各模型 accuracy 与耗时；**txt 中仅存表题，表格内容未抽取** |
| {TAB-llmtt-2} | TABLE II | PERFORMANCE COMPARISON OF DIFFERENT LLMS ON THE DS-IMAGE | DS-Image（109 题）同上；**txt 中仅存表题，表格内容未抽取** |
| {FIG-llmtt-5} | Fig. 5 | Comparison of openai model accuracy across different parameter | DS-Image 上同一组扫描；Claude 与 glm-4v-plus 随温度升高下降，GPT-4o-mini 稳定 |
| {FIG-llmtt-6} | Fig. 6 | The effect of temperature and Top_p on model accuracy in MCQ | 标准化 50 题集上 Temperature×Top_p 联合影响（GPT-4o、GPT-4o-mini、Gemini-1.5-pro、Gemini-2.0-flash）；作者称差异不显著但未做统计检验 |
| {FIG-llmtt-7} | Fig. 7 | Evaluation of real-time performance and computational efficiency | (a) 吞吐：GPT-4o 2.21、GPT-4o-mini 2.22、Claude-3.5-Sonnet 0.89 题/秒；(b) 推理成本—速度权衡，GPT-4 TPT/CPT 最高 |
| {FIG-llmtt-8} | Fig. 8 | Accuracy of different LLMs on two sets of UK standardized driving | 两套 DVSA 标准化 50 题上的准确率；GPT-4o 两套均最高（0.98 / 0.96），Gemini 两套间波动较大 |
| {FIG-llmtt-9} | Fig. 9 | Frame-level confusion matrix for GPT-4o and GPT-4o-mini models. | 帧级混淆矩阵：GPT-4o 270 TP/84 TN/2 FN/1139 FP，mini 265/261/7/962；两者均严重过判为正 |
| {FIG-llmtt-10} | Fig. 10 | Frame-level performance metrics for GPT-4o and GPT-4o-mini | 帧级 accuracy/precision/recall/F1；recall 97.43%–99.26% 而 precision 19.16%–21.6%，典型"全判为正"退化 |
| {FIG-llmtt-11} | Fig. 11 | Event-level evaluation results for GPT-4o and GPT-4o-mini models at different thresholds. | 事件级混淆矩阵，IoU 阈值 0.5（a）与 0.7（b）；阈值越严，检出越少 |
| {FIG-llmtt-12} | Fig. 12 | Comparison of metrics between GPT-4o and GPT-4o-mini models across various event detection | 各阈值下的 accuracy/precision/recall/F1；阈值 0.2→0.85 时 GPT-4o 准确率由 52.43% 崩到 0.64% |
| {FIG-llmtt-13} | Fig. 13 | Comparison of hazard perception scores and score percentages | 危险感知总分与得分率随阈值变化；阈值 0.2 时 GPT-4o 270/270（100%），0.5 时降到约 130–135（48–50%） |
| {FIG-llmtt-14} | Fig. 14 | Example of LLM-based hazard perception in a driving scenario. | 过保守判定案例：邻侧非机动车道上的行人（动或静）被判为潜在危险，导致不必要的减速 |

> 注：**共 14 个 Figure + 2 个 Table（合计 16 项 > 12），此处全部覆盖**（grep 确认全文无 Fig. 15、无 Table III）。图注栏均逐字摘自全文 PDF 文本的对应行，未改写、未翻译、未跨行拼接；条目在该行原文的固定列宽断行处结束。TABLE I / TABLE II 在 txt 中只抽到表题，表格数值缺失。

## 6. 对 P1 的用处

- **与 P1 的关系**：不同问题（也非相邻）。本文是纯文本/视频问答的 LLM 能力基准，测的是"交通法规知识与危险感知的答题正确率"，既无车辆纵横向控制接口，也无同 ODD（高速主线多车道混行）的闭环评价协议；其题库场景含支路汇入、人行横道等城市要素。
- **可迁移**：
  1. **"资格门"式评测协议的形式**：先定官方通过线（43/50 = 86%）再判合格，并把评价拆成三层——帧级/事件级（IoU 0.5、0.7 匹配）与时间敏感评分（越早检出得分越高、误报与漏检都罚）。P1 若要给编队控制器设"准入指标门"，可借用这种"门槛 + 分层 + 时间加权"的结构（结构借鉴，非数字复用）。
  2. **速度—成本双轴报告法**：Throughput（题/秒）、TPT（每 token 时间）、CPT（每 token 成本）三件套 + 散点图（Fig. 7）。P1 的"端到端延迟 / MCU 内存"可参照其"主指标 + 资源轴"并列报告的方式；其"网络抖动用多次测量取均值"的处理思路可移植为 P1 的"多次推理取均值并标注编译器档位"。
  3. **失败样例归类**：作者用失败题目反推能力缺口（Fig. 14 的过保守判定三因）。P1 的失败模式分析（长尾四类 + 激进车流扰动）可参照"逐场景 + 归因三分"的写法。
- **不可迁移 / 陷阱**：
  1. **跨 ODD**：题库与视频基于英国道路（含汇入路口、人行横道、行人互动），P1 的 ODD 是高速主线多车道混行；按项目 AGENTS.md §5，其结论不可作为 P1 的证据。
  2. **无控制接口**：模型输出是选项字母、0/1 危险判定与文字建议，不含转向/加速度量，不能充当 P1 的 PID / MPC / TD3 / OTF-CfC 之外的任何基线，也不能替代闭环评价。
  3. **结论绑定 prompt 与通过线**：成绩依赖"资深驾驶员"系统提示与"只回字母"的输出约束，以及英国官方 86% 通过线；换 prompt 框架或换辖区即失效（作者自承仅英国、跨地区留作未来工作）。
  4. **数字不同量纲**：88.21% 等数字是问答准确率/得分率，与 P1 的跟车 RMSE、jerk 峰值、车道居中偏差等不可比。**文献报告值，协议不同，不可直接比较**。
- **引用时必须带的限定语**：本文结果来自 2025 年英国 DVSA 驾驶理论（726 道 MCQ + 54 段危险感知视频）的 LLM 闭卷问答评测，覆盖 16 个通用 LLM，为 Temperature=0 单次采样、无置信区间、无人类实测基线，且不含任何车辆纵横向闭环控制验证——文献报告值，协议不同，不可与 P1 结果直接比较。

## 7. 缺失信息（≥3 条，写成可执行动作）

1. **TABLE I / TABLE II 的完整数值缺失**：txt 只抽到两个表题，GPT-4、GPT-3.5-turbo、GPT-4o-mini、Ernie-4.0-turbo-8k、Qwen-turbo、Gemini 两个型号在 DS-Text/DS-Image 上的 accuracy/precision/recall/F1 与耗时都取不到。→ 动作：回原 PDF 逐行抄录两表，或从 GitHub 仓库读取评测输出文件。
2. **无不确定度与重复采样**：全文无 CI、无 p 值、无多 seed；准确率在 T=0 下只跑一次（仅对受网络影响的吞吐/成本做"多次测量取均值"）。→ 动作：若要引用其准确率，必须写明"单次采样、无 CI"；若需误差棒，须自行重跑。
3. **题库许可与仓库 LICENSE 未说明**：正文只说题目来自 DVSA 公开模拟题 [29] 与 DriverInstructor 网站 [30]，致谢网站"分享题目"，但未见许可条款；仓库 LICENSE 未在正文出现。→ 动作：访问 https://github.com/PeiDashuai/DVSA-test-for-LLMs 核对 LICENSE 与再分发条款；未确认前不得转引题目原文。
4. **prompt 全文缺失**：只有 prompt 设计描述，无逐字 system/user prompt 与危险感知"危险类型—视觉特征—威胁评估—建议动作"四段模板。→ 动作：从仓库取 prompt 文本，才能判定成绩对措辞的敏感度（现只有 Temperature/Top_p 敏感性，无 prompt 变体对照）。
5. **视频编辑规则未量化**：作者称"appropriately edited"了官方视频长度而未说明裁掉多少、是否改动危险起止帧。→ 动作：索取帧级标注文件与剪辑脚本，核对危险起始帧与得分序列的对应关系。
6. **人类基线只有通过线、没有实测分布**：仅有官方标准（MCQ 43/50=86%；危险感知 44/75、67/100），无人类考生准确率/得分分布。→ 动作：另找 DVSA 官方统计或人类被试研究，才能计算"LLM 距人类"的效应量。
7. **版本关系**：本文是 MobiArch 2024 会议论文 [13] 的扩展版（作者称新增 >50%），但未给出扩展边界。→ 动作：引用时说明版本关系，避免与会议版数字混用。

## 8. 关键数字（只抄论文明确印出的表格/正文，**不得目测估读**）

| 指标 | 值 | 不确定度 | 出处（表/图/节） |
|---|---|---|---|
| MCQ 通过线（英国官方，轿车） | 50 题中至少答对 43 题 = 准确率 86% | — | §III-A（同句说明该标准也用于 LLM） |
| MCQ 官方题量与时长 | 50 题，每题 4 选项、1 个或多个正确项；57 分钟 | — | §III-A |
| 危险感知（轿车/摩托） | 14 段 1 分钟视频；满分 75；通过线 44 | — | §III-A |
| 危险感知（货车/客车） | 19 段视频；满分 100；通过线 67 | — | §III-A |
| 题库规模（去重后） | 726 道唯一 MCQ，其中约 109 道含图 | — | §III-B |
| 评测集划分 | DS-Text 617 题；DS-Image 109 题 | — | §III-B |
| 危险感知视频（作者收集） | 54 段含危险事件；帧切分 0.2 s | — | §III-B |
| 评测模型数 | 16（11 专有 + 5 开源） | — | §I、§III-C |
| 评测模型清单 | 专有：GPT-3.5-turbo、GPT-4、GPT-4o、GPT-4o-mini、Claude-3.5-sonnet、Gemini-1.5-Pro、Gemini-2.0-Flash、Ernie-4.0-turbo-8k、glm-4-plus、glm-4v-plus、Qwen-turbo；开源：DeepSeek-V3、DeepSeek-R1、MiniCPM3-4B、MiniCPM-V-2.6、MiniCPMLlama3-V2.5 | — | §I、§III-C |
| GPT-4o MCQ 平均准确率 | 88.21% | 未报告 CI/标准误；T=0 单次采样 | §IV-D（摘要同值） |
| GPT-4o DS-Text | 96.60%；617 题用时 279.65 s | 同上 | §IV-D（TABLE I） |
| GPT-4o DS-Image | 79.82%；用时 50.51 s | 同上 | §IV-D（TABLE II） |
| Claude-3.5-sonnet | DS-Text 93.35%（689.68 s）；DS-Image 77.06%（78.5 s）；平均 85.21% | 同上 | §IV-D |
| glm-4-plus / glm-4v-plus | DS-Text 89.47%（897.87 s）/ DS-Image 69.72%（199.7 s） | 同上 | §IV-D |
| DeepSeek-V3 / DeepSeek-R1 | DS-Text 93.68% / 95.69% | 同上；无图像能力，未测 DS-Image | §IV-D |
| MiniCPM-3-4B / V-2.6 / Llama3-V2.5 | 70.83%（文本）/ 57.80%（图）/ 55.96%（图） | 同上 | §IV-D |
| GPT-4o-mini MCQ 平均 | 77.49% | 同上 | §IV-D |
| DVSA 标准化 50 题（两套） | GPT-4o 0.98 与 0.96（最高） | 同上 | §IV-E（Fig. 8） |
| 吞吐 | GPT-4o 2.21、GPT-4o-mini 2.22、Claude-3.5-Sonnet 0.89 题/秒 | 多次测量取均值，未给标准差 | §IV-D（Fig. 7a） |
| TPT / CPT | GPT-4 0.00537 s / $2.18；GPT-4o 0.00401 s / $0.36；GPT-4o-mini 0.00399 s / $0.043；Claude-3.5-Sonnet 0.00947 s / $0.25 | 同上 | §IV-D（Fig. 7b） |
| 帧级（GPT-4o） | accuracy 0.3518；precision 19.16%；recall 0.9926；F1 32.12%；混淆矩阵 270 TP / 84 TN / 2 FN / 1139 FP | 单次；accuracy 与混淆矩阵不自洽（见文末 ⚠） | §IV-F-1（Fig. 9、Fig. 10） |
| 帧级（GPT-4o-mini） | accuracy 23.68%；precision 21.6%；recall 97.43%；F1 35.36%；混淆矩阵 265 TP / 261 TN / 7 FN / 962 FP | 单次；同上 | §IV-F-1 |
| 事件级（阈值 0.2） | GPT-4o 准确率 52.43%、precision 52.43%、recall 100%、F1 68.79%；GPT-4o-mini 38.93% / 39.84% / 94.44% / 56.04% | 单次 | §IV-F-2（Fig. 12） |
| 事件级（阈值 0.85） | GPT-4o 0.64% / 0.97% / 1.85% / 1.27%；GPT-4o-mini 1.11% / 1.56% / 3.70% / 2.20% | 单次 | §IV-F-2 |
| 危险感知得分 | 阈值 0.2：GPT-4o 270/270（100%）、mini 255（94.4%）；0.5：两者约 130–135（48–50%）；0.7：mini 40 分 vs GPT-4o 35 分；0.85：mini 10 分 vs GPT-4o 5 分 | 单次；满分口径为样本数×5 | §IV-F-2（Fig. 13） |
| 摘要层面的危险感知结论 | 危险事件检出 precision 低于 20%、最终得分率低于 60%，均未通过 | 与正文阈值 0.2 时 100% 得分率不一致（见文末 ⚠） | Abstract、§IV-F-2 |
| API 价格（参考） | GPT-3.5 $0.50/$1.50；GPT-4 $30/$120；GPT-4o $5/$15（每 1M tokens）＋ $0.001275/图 | — | §III-C |
| 题库来源与许可 | 来自 DVSA 公开模拟题 [29] 与 DriverInstructor 网站公开题 [30]，去重后 726 题；54 段视频取自 DVSA 公开考试资源 | 许可条款未说明（未见 LICENSE） | §III-B、ACKNOWLEDGMENT |
| 采样参数 | Temperature = 0，Top_p = 1 | — | §IV-A |
| 硬件 | MiniCPM 本地部署：RTX 4090 24 GB；API 调用：i9-13900H + RTX 4060 8 GB + 32 GB RAM 笔记本 | — | §IV-A |
| 可复现材料 | 数据与代码公开：https://github.com/PeiDashuai/DVSA-test-for-LLMs | 未见 LICENSE 说明，未见在线榜单 | §II 脚注 1 |

⚠内部不一致：① 帧级准确率疑似对调——正文称 GPT-4o 准确率 0.3518、GPT-4o-mini 为 23.68%，但按正文印出的混淆矩阵（GPT-4o：270 TP/84 TN/2 FN/1139 FP；GPT-4o-mini：265/261/7/962）自算应为 GPT-4o 23.68%、mini 35.18%（该换算为本卡按原文数字计算，非原文值），而 precision/recall/F1 三项与混淆矩阵一致；② 引言称 GPT-4o（88.21%）与 Claude-3.5-sonnet（85.21%）"both passing the multiple-choice test"，与通过线 86% 及摘要/结论"only GPT-4o achieved a passing score (88.21%)"矛盾；③ 同一组帧级混淆矩阵数字在帧级（§IV-F-1）与事件级（§IV-F-2）两小节重复出现，事件级未给出自己的混淆矩阵数值；④ 摘要称危险感知"final score rate was below 60%"，与正文阈值 0.2 时 GPT-4o 270/270（100%）、mini 255（94.4%）冲突。
