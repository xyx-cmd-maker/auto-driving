# 检索日志：P5 AdjointStack —— 混合频率伴随敏感度与联合微调

执行日期：2026-10-11｜执行者：`scripts/literature/discover.mjs`（自动化）｜通道：OpenAlex
时间窗：2016-01-01 起｜文献类型：article｜语言：en｜排序：relevance_score 降序｜每式截断：前 60 条

## 逐查询命中与导出

| query_id | 主题 | 检索式 | 命中 | 导出 | 新增 |
|---|---|---|---|---|---|
| P5-T1 | 神经 ODE 与伴随法 | `"neural ordinary differential equation" OR "adjoint sensitivity"` | 5248 | 60 | 60 |
| P5-T2 | 隐式微分与可微优化 | `"implicit differentiation" OR "differentiable optimization"` | 2749 | 60 | 60 |
| P5-T3 | 双层优化与元学习 | `"bilevel optimization" AND ("machine learning" OR "deep learning")` | 1953 | 60 | 60 |
| P5-T4 | 基于梯度的超参数敏感度 | `"hyperparameter" AND "gradient" AND ("optimization" OR "sensitivity")` | 153873 | 60 | 60 |
| P5-T5 | 世界模型与基于模型的 RL | `"world model" AND ("model-based reinforcement learning" OR "planning")` | 6615 | 60 | 60 |
| P5-T6 | 可微仿真与物理先验 | `"differentiable simulation" OR "differentiable physics"` | 1408 | 60 | 60 |
| P5-T7 | 混合频率 / 多时间尺度训练 | `"multi-timescale" OR "mixed frequency" OR "temporal hierarchy" AND learning` | 1454 | 60 | 60 |
| P5-T8 | 端到端可微驾驶栈 | `"end-to-end" AND "differentiable" AND (driving OR "autonomous driving")` | 18719 | 60 | 60 |
| P5-T9 | 闭环联合训练与端到端微调 | `"closed-loop" AND ("joint training" OR "fine-tuning" OR "finetuning") AND (control OR driving OR robot)` | 15755 | 60 | 60 |
| P5-T10 | 可微模型预测控制 | `"differentiable model predictive control" OR "differentiable MPC"` | 191 | 60 | 59 |
| P5-T11 | 控制器敏感度与梯度整定 | `"sensitivity analysis" AND ("controller tuning" OR "control parameter") AND (gradient OR automatic differentiation)` | 2265 | 60 | 59 |
| P5-T12 | 学习控制器与世界模型的联合优化 | `("world model" OR "dynamics model") AND ("controller" OR "policy") AND ("joint" OR "end-to-end") AND optimization` | 12537 | 60 | 49 |

## 完整检索式（可原样复制）

- P5-T1: https://api.openalex.org/works?search=%22neural+ordinary+differential+equation%22+OR+%22adjoint+sensitivity%22&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P5-T2: https://api.openalex.org/works?search=%22implicit+differentiation%22+OR+%22differentiable+optimization%22&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P5-T3: https://api.openalex.org/works?search=%22bilevel+optimization%22+AND+%28%22machine+learning%22+OR+%22deep+learning%22%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P5-T4: https://api.openalex.org/works?search=%22hyperparameter%22+AND+%22gradient%22+AND+%28%22optimization%22+OR+%22sensitivity%22%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P5-T5: https://api.openalex.org/works?search=%22world+model%22+AND+%28%22model-based+reinforcement+learning%22+OR+%22planning%22%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P5-T6: https://api.openalex.org/works?search=%22differentiable+simulation%22+OR+%22differentiable+physics%22&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P5-T7: https://api.openalex.org/works?search=%22multi-timescale%22+OR+%22mixed+frequency%22+OR+%22temporal+hierarchy%22+AND+learning&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P5-T8: https://api.openalex.org/works?search=%22end-to-end%22+AND+%22differentiable%22+AND+%28driving+OR+%22autonomous+driving%22%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P5-T9: https://api.openalex.org/works?search=%22closed-loop%22+AND+%28%22joint+training%22+OR+%22fine-tuning%22+OR+%22finetuning%22%29+AND+%28control+OR+driving+OR+robot%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P5-T10: https://api.openalex.org/works?search=%22differentiable+model+predictive+control%22+OR+%22differentiable+MPC%22&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P5-T11: https://api.openalex.org/works?search=%22sensitivity+analysis%22+AND+%28%22controller+tuning%22+OR+%22control+parameter%22%29+AND+%28gradient+OR+automatic+differentiation%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P5-T12: https://api.openalex.org/works?search=%28%22world+model%22+OR+%22dynamics+model%22%29+AND+%28%22controller%22+OR+%22policy%22%29+AND+%28%22joint%22+OR+%22end-to-end%22%29+AND+optimization&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
