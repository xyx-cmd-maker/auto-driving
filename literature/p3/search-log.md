# 检索日志：P3 TalkOTF —— 语言 → OTF 定量 grounding 与指令合法性检查

执行日期：2026-10-11｜执行者：`scripts/literature/discover.mjs`（自动化）｜通道：OpenAlex
时间窗：2016-01-01 起｜文献类型：article｜语言：en｜排序：relevance_score 降序｜每式截断：前 60 条

## 逐查询命中与导出

| query_id | 主题 | 检索式 | 命中 | 导出 | 新增 |
|---|---|---|---|---|---|
| P3-T1 | LLM 用于自动驾驶决策 | `"large language model" AND "autonomous driving"` | 3077 | 60 | 60 |
| P3-T2 | VLA / 视觉-语言-动作模型 | `"vision-language-action" OR "vision language action"` | 709 | 60 | 60 |
| P3-T3 | 语言条件轨迹规划 | `"language" AND "trajectory" AND ("planning" OR "generation") AND vehicle` | 50368 | 60 | 59 |
| P3-T4 | 人类驾驶行为建模与自然语言 | `"driving behavior" AND ("natural language" OR "language model")` | 1458 | 60 | 57 |
| P3-T5 | 语言 grounding 到物理量 | `"grounding" AND ("physical" OR "quantitative" OR "scalar") AND (language OR text)` | 77618 | 60 | 60 |
| P3-T6 | 可解释驾驶与自然语言接口 | `"explainable" AND "autonomous driving" AND ("language" OR "explanation")` | 12309 | 60 | 53 |
| P3-T7 | 端到端驾驶的大模型 | `"end-to-end" AND "autonomous driving" AND ("foundation model" OR "large model")` | 1724 | 60 | 53 |
| P3-T8 | 语言交互式车辆决策 | `"human-like" AND ("interaction" OR "interface") AND ("autonomous vehicle" OR "driving")` | 14072 | 60 | 58 |

## 完整检索式（可原样复制）

- P3-T1: https://api.openalex.org/works?search=%22large+language+model%22+AND+%22autonomous+driving%22&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P3-T2: https://api.openalex.org/works?search=%22vision-language-action%22+OR+%22vision+language+action%22&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P3-T3: https://api.openalex.org/works?search=%22language%22+AND+%22trajectory%22+AND+%28%22planning%22+OR+%22generation%22%29+AND+vehicle&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P3-T4: https://api.openalex.org/works?search=%22driving+behavior%22+AND+%28%22natural+language%22+OR+%22language+model%22%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P3-T5: https://api.openalex.org/works?search=%22grounding%22+AND+%28%22physical%22+OR+%22quantitative%22+OR+%22scalar%22%29+AND+%28language+OR+text%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P3-T6: https://api.openalex.org/works?search=%22explainable%22+AND+%22autonomous+driving%22+AND+%28%22language%22+OR+%22explanation%22%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P3-T7: https://api.openalex.org/works?search=%22end-to-end%22+AND+%22autonomous+driving%22+AND+%28%22foundation+model%22+OR+%22large+model%22%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P3-T8: https://api.openalex.org/works?search=%22human-like%22+AND+%28%22interaction%22+OR+%22interface%22%29+AND+%28%22autonomous+vehicle%22+OR+%22driving%22%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2016-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
