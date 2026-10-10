# 合表报告：P1 顶刊清单 × 项目引用库

生成：2026-10-02

## 一、计数（可复核）

| 项 | 数 |
|---|---|
| P1 顶刊清单输入行（final_list.jsonl） | 75 |
| 旧引用库输入条目（references-list-verified.txt） | 35 |
| **合并后唯一记录** | **98** |
| ↳ P1 主记录 | 75 |
| ↳ 旧库独有（P2–P5 用） | 23 |
| ↳ 两份清单都收录 → 已去重并入主记录 | 12 |

## 二、两份清单都收录（去重明细）

| 旧库编号 | 合入 P1 编号 | 标题 | 匹配方式 |
|---|---|---|---|
| B1 | #101 | Neural Ordinary Differential Equations | title j=1.000 |
| B2 | #102 | Liquid Time-constant Networks | doi |
| B3 | #1 | Closed-form continuous-time neural networks | doi |
| B4 | #103 | Neural circuit policies enabling auditable autonomy | doi |
| C3 | #49 | World Models for Autonomous Driving: An Initial Survey | title j=1.000 |
| D3 | #121 | DriveGPT4: Interpretable End-to-End Autonomous Driving Via Large Language Model | title j=1.000 |
| E1 | #111 | Control Barrier Functions: Theory and Applications | curated-cross-list |
| F1 | #116 | Planning-oriented Autonomous Driving | title j=1.000 |
| F3 | #117 | End-to-End Autonomous Driving: Challenges and Frontiers | title j=1.000 |
| F4 | #12 | Addressing Function Approximation Error in Actor-Critic Methods | title j=1.000 |
| F5 | #114 | nuScenes: A Multimodal Dataset for Autonomous Driving | curated-cross-list |
| F7 | #115 | CARLA: An Open Urban Driving Simulator | title j=1.000 |

## 三、旧库独有（保留）

| 旧库编号 | 标题 | 匹配到的最近 P1 条目相似度 |
|---|---|---|
| A1 | DriveDreamer [版本+1] | (best j=0.125) |
| A2 | Drive as You Speak [版本+1] | (best j=0.111) |
| B5 | 2018. https://github.com/rtqichen/torchdiffeq | (best j=0.000) |
| C1 | DriveDreamer-2: LLM-Enhanced World Models for Diverse Driving Video Generation | (best j=0.333) |
| C2 | GAIA-1: A Generative World Model for Autonomous Driving | (best j=0.333) |
| C4 | Wayformer: Motion Forecasting via Simple & Efficient Attention Networks. *2023 | (best j=0.100) |
| C5 | Motion Transformer with Global Intention Localization and Local Movement Refinement | (best j=0.125) |
| C6 | Scene Transformer: A unified architecture for predicting future trajectories of multiple agents | (best j=0.067) |
| D1 | DiLu: A Knowledge-Driven Approach to Autonomous Driving with Large Language Models | (best j=0.333) |
| D2 | GPT-Driver: Learning to Drive with GPT | (best j=0.125) |
| D4 | LanguageMPC: Large Language Models as Decision Makers for Autonomous Driving | (best j=0.364) |
| D5 | A Language Agent for Autonomous Driving | (best j=0.400) |
| D6 | Driving with LLMs: Fusing Object-Level Vector Modality for Explainable Autonomous Driving. *2024 | (best j=0.200) |
| D7 | DriveVLM: The Convergence of Autonomous Driving and Large Vision-Language Models | (best j=0.364) |
| D8 | DriveLM: Driving with Graph Visual Question Answering | (best j=0.125) |
| D9 | Talk2BEV: Language-enhanced Bird's-eye View Maps for Autonomous Driving. *2024 | (best j=0.250) |
| E2 | ISO 26262-1:2018, | (best j=0.000) |
| F2 | BEVFormer: Learning Bird's-Eye-View Representation from Multi-Camera Images via Spatiotemporal Transformers | (best j=0.067) |
| F6 |  | (best j=0.000) |
| F8 | OpenVLA: An Open-Source Vision-Language-Action Model | (best j=0.167) |
| F9 | Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond | (best j=0.133) |
| F10 | Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution | (best j=0.154) |
| F11 | DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning | (best j=0.182) |

## 四、已知口径问题（写入稿件前必须处理）

1. 旧库条目的题名/年份为**解析结果**（原文是整串引文），个别条目（如 ISO 26262-1、torchdiffeq）不是论文，已按原样保留并标 mark。
2. `refs.bib` 与 `P1-library.jsonl` 中的 P1 主记录字段一律来自 Crossref；Crossref 未注册的 4 条（#101/#104/#115/#120）与 1 条 DOI 指向他文的（#105）已显式标注，**不得直接引用其 DOI**。
3. 被引数为 Crossref 口径快照（2026-10-02），与 OpenAlex/Google Scholar 不可比。
