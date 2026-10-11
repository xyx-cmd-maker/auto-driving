# 检索日志：P4 IsoLNN —— 连续可导控制器的安全隔离与物理可行性筛查

执行日期：2026-10-11｜执行者：`scripts/literature/discover.mjs`（自动化）｜通道：OpenAlex
时间窗：2015-01-01 起｜文献类型：article｜语言：en｜排序：relevance_score 降序｜每式截断：前 60 条

## 逐查询命中与导出

| query_id | 主题 | 检索式 | 命中 | 导出 | 新增 |
|---|---|---|---|---|---|
| P4-T1 | 控制障碍函数 / 安全滤波器 | `"control barrier function"` | 2890 | 60 | 60 |
| P4-T2 | 运行时验证 / 在线验证 | `"runtime verification" OR "online verification"` | 3215 | 60 | 60 |
| P4-T3 | 神经网络控制器的形式化验证 | `"formal verification" AND ("neural network" OR "neural controller")` | 3468 | 60 | 60 |
| P4-T4 | 可达性分析与安全包络 | `"reachability analysis" AND (safety OR control)` | 3554 | 60 | 59 |
| P4-T5 | 安全强化学习与屏蔽机制 | `"safe reinforcement learning" OR "shielding"` | 762798 | 60 | 57 |
| P4-T6 | SOTIF / 预期功能安全 | `"SOTIF" OR "functional safety" AND "autonomous driving"` | 1219 | 60 | 60 |
| P4-T7 | OOD 检测与失效预测 | `"out-of-distribution" AND ("detection" OR "monitoring") AND (driving OR robot)` | 4167 | 60 | 60 |
| P4-T8 | 学习控制器的可行性与约束满足 | `"learned controller" AND ("feasibility" OR "constraint satisfaction")` | 232 | 60 | 58 |
| P4-T9 | 自动驾驶安全保证与论证 | `"safety assurance" OR "safety case" AND autonomous` | 972 | 60 | 59 |

## 完整检索式（可原样复制）

- P4-T1: https://api.openalex.org/works?search=%22control+barrier+function%22&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2015-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P4-T2: https://api.openalex.org/works?search=%22runtime+verification%22+OR+%22online+verification%22&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2015-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P4-T3: https://api.openalex.org/works?search=%22formal+verification%22+AND+%28%22neural+network%22+OR+%22neural+controller%22%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2015-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P4-T4: https://api.openalex.org/works?search=%22reachability+analysis%22+AND+%28safety+OR+control%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2015-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P4-T5: https://api.openalex.org/works?search=%22safe+reinforcement+learning%22+OR+%22shielding%22&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2015-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P4-T6: https://api.openalex.org/works?search=%22SOTIF%22+OR+%22functional+safety%22+AND+%22autonomous+driving%22&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2015-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P4-T7: https://api.openalex.org/works?search=%22out-of-distribution%22+AND+%28%22detection%22+OR+%22monitoring%22%29+AND+%28driving+OR+robot%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2015-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P4-T8: https://api.openalex.org/works?search=%22learned+controller%22+AND+%28%22feasibility%22+OR+%22constraint+satisfaction%22%29&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2015-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
- P4-T9: https://api.openalex.org/works?search=%22safety+assurance%22+OR+%22safety+case%22+AND+autonomous&filter=type%3Aarticle%2Clanguage%3Aen%2Cfrom_publication_date%3A2015-01-01&sort=relevance_score%3Adesc&per-page=60&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Ccited_by_count%2Cauthorships%2Cprimary_location%2Clanguage&mailto=research%40example.org
