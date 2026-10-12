# 检索日志：P2 SocialDreamer —— 以 OTF 社会压力场为结构条件模态的驾驶世界模型

执行日期：2026-10-12｜执行者：`scripts/literature/discover.mjs`（自动化）｜通道：OpenAlex
时间窗：2019-01-01 起｜文献类型：article｜语言：en｜排序：relevance_score 降序｜每式截断：前 60 条

## 逐查询命中与导出

| query_id | 主题 | 检索式 | 命中 | 导出 | 新增 |
|---|---|---|---|---|---|
| P2-T1 | 驾驶世界模型（预测/规划） | `"world model" AND ("autonomous driving" OR "driving")` | 2738 | 60 | 60 |
| P2-T2 | 驾驶场景生成与合成 | `"driving scene" AND ("generation" OR "synthesis") AND ("world model" OR "diffusion")` | 299 | 60 | 53 |
| P2-T3 | 条件模态与可控 rollout | `"conditional" AND "world model" AND ("controllable" OR "conditioning")` | 1727 | 60 | 49 |
| P2-T4 | 社会交互与压力场建模 | `("social force" OR "social interaction" OR "interaction field") AND (driving OR vehicle OR traffic)` | 116266 | 60 | 59 |
| P2-T5 | 交互感知的行为/轨迹预测 | `"interaction-aware" AND ("trajectory prediction" OR "behavior prediction") AND vehicle` | 571 | 60 | 58 |
| P2-T6 | 多智能体交通流仿真与生成 | `"multi-agent" AND ("traffic simulation" OR "traffic flow") AND ("learning" OR "generative")` | 5734 | 60 | 59 |
| P2-T7 | 占用/潜空间世界模型 | `("occupancy" OR "latent") AND "world model" AND driving` | 1142 | 60 | 21 |
| P2-T8 | 扩散模型用于轨迹与场景生成 | `"diffusion model" AND ("trajectory" OR "scene") AND ("prediction" OR "generation") AND driving` | 4705 | 60 | 53 |

## 完整检索式（可原样复制）

- P2-T1: https://api.openalex.org/works?search=%22world+model%22+AND+%28%22autonomous+driving%22+OR+%22driving%22%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2019-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P2-T2: https://api.openalex.org/works?search=%22driving+scene%22+AND+%28%22generation%22+OR+%22synthesis%22%29+AND+%28%22world+model%22+OR+%22diffusion%22%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2019-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P2-T3: https://api.openalex.org/works?search=%22conditional%22+AND+%22world+model%22+AND+%28%22controllable%22+OR+%22conditioning%22%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2019-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P2-T4: https://api.openalex.org/works?search=%28%22social+force%22+OR+%22social+interaction%22+OR+%22interaction+field%22%29+AND+%28driving+OR+vehicle+OR+traffic%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2019-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P2-T5: https://api.openalex.org/works?search=%22interaction-aware%22+AND+%28%22trajectory+prediction%22+OR+%22behavior+prediction%22%29+AND+vehicle&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2019-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P2-T6: https://api.openalex.org/works?search=%22multi-agent%22+AND+%28%22traffic+simulation%22+OR+%22traffic+flow%22%29+AND+%28%22learning%22+OR+%22generative%22%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2019-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P2-T7: https://api.openalex.org/works?search=%28%22occupancy%22+OR+%22latent%22%29+AND+%22world+model%22+AND+driving&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2019-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P2-T8: https://api.openalex.org/works?search=%22diffusion+model%22+AND+%28%22trajectory%22+OR+%22scene%22%29+AND+%28%22prediction%22+OR+%22generation%22%29+AND+driving&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2019-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
