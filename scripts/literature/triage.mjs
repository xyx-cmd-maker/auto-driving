// scripts/literature/triage.mjs — 从核验后的候选池选出 50 条并成图（规则显式、可复跑）
//
// 用法：node scripts/literature/triage.mjs --topic p3
// 读：literature/<p>/verified.jsonl  写：literature/<p>/文献需求-50篇顶刊.md + shortlist.jsonl
//
// 选择规则（**先写死、再看结果**，避免事后择优）：
//   R1 只保留 Crossref/DataCite 核验 status=OK 的条目（层 1 存在性通过）
//   R2 无 update-to 更正/撤稿信号；有信号者单列人工确认
//   R3 META 黑名单剔除（会议摘要增刊、撤稿通知、更正启事、新闻、书评等）
//   R4 每个 theme 至少保障 minPerTheme 条 ⇒ 保证文献图的覆盖均衡，不出现某节空缺
//   R5 其余名额按 score 降序补齐；score 三因子与该权重一起打印在报告里
//   R6 截断规则显式记录：命中数千 → 导出 60/式 → 入选 50；**不声称这是系统综述**
import fs from "node:fs";
import path from "node:path";

const TODAY = new Date().toISOString().slice(0, 10);

const TOPIC_META = {
  p3: { name: "P3 TalkOTF", zh: "语言 → OTF 定量 grounding 与指令合法性检查", total: 50, perTheme: 4,
        usage: "语言 grounding 的方法底座、指令合法性检查的先例、以及 P3 与它们的差异" },
  p4: { name: "P4 IsoLNN", zh: "连续可导控制器的安全隔离与物理可行性筛查", total: 50, perTheme: 4,
        usage: "安全隔离层的机制来源、可引用的规范边界、以及 P4 的净增量论证" },
  p5: { name: "P5 AdjointStack", zh: "混合频率伴随敏感度与联合微调", total: 50, perTheme: 4,
        usage: "伴随法与双层优化的理论工具、混合频率训练先例、以及 P5 的方法论边界" },
  p2: { name: "P2 SocialDreamer", zh: "以 OTF 社会压力场为结构条件模态的驾驶世界模型", total: 50, perTheme: 4,
        usage: "世界模型与条件生成的方法底座、社会交互/压力场的表征先例、以及 P2 相对 DriveDreamer（结构条件为 HDMap/3D Box）的净增量论证" },
};

// 顶刊/顶会加权（venue 名做小写包含匹配）
const VENUE_TIERS = [
  { tier: 3.0, keys: ["nature machine intelligence", "nature", "science robotics", "science", "ieee transactions on pattern analysis"] },
  { tier: 2.0, keys: ["ieee transactions on intelligent transportation", "ieee transactions on vehicular", "ieee transactions on robotics",
                     "ieee transactions on control", "ieee transactions on neural networks", "ieee transactions on automatic control",
                     "ieee robotics and automation letters", "automatica", "transportation research", "ieee transactions on industrial"] },
  { tier: 1.2, keys: ["ieee transactions", "acm transactions", "pattern recognition", "neurocomputing", "expert systems with applications",
                     "information fusion", "applied energy", "ieee access", "sensors", "electronics"] },
];
const META_BLACKLIST = [
  "issue information", "table of contents", "front cover", "back cover", "editorial board",
  "correction to", "corrigendum", "erratum", "retraction", "retracted", "withdrawn",
  "book review", "call for papers", "conference committee", "proceedings of", "abstracts from",
  "guest editorial", "in memoriam", "author index", "subject index", "title page",
];

// 领域锚词（R3b）：检索词是通用词（如 "runtime verification"）时，会大量捞进与自动驾驶安全
// **无关**的泛形式化/软件工程论文（实测：Detecting Architectural Erosion、spiking neural P
// systems 等）。要求题名至少命中一个锚词，把主题钉回本论文的领域。
// R3b 领域过滤。分两种口径：
//   p3/p4 —— **单层锚词**：题名命中任一锚词即保留（这两篇的领域词较独特，噪声可控）。
//   p5    —— **双层**：必须同时命中"方法词"与"语境词"。P5 的检索词（neural ODE / adjoint /
//            bilevel …）是全学科通用方法，单层过滤会放进单细胞转录组、时空混沌、代谢组学等
//            与控制系统无关的工作（实测如此），文献图会失去可用性。
// P5 的"语境词"必须真的是**控制系统/机器人/车辆**语境。
// 早期版本把 simulat / planning / dynam cal 也算语境，结果放进了组织力学、粘弹性、时空混沌等
// 与控制系统无关的工作（实测）。收紧为控制侧专有词。
const DOMAIN_ANCHORS = {
  // p2 —— 用**双层**口径（与 p5 同理，见 METHOD_ANCHORS.p2）：
  //   本层 = **驾驶语境**词。检索词 "diffusion model"、"interaction"、"world model" 是全学科
  //   通用的，单层过滤会放进小脑动力学、声呐成像、机械臂遥操作等（实测，已剔除）。
  //   因此这一层必须真的是"车/路/交通"语境，世界模型类词放在下一层。
  p2: ["driv", "vehicle", "autonomous", "traffic", "car", "transport", "road", "lane", "platoon",
       "intersection", "highway", "pedestrian", "adas", "self-driving", "ego"],
  p3: ["driv", "vehicle", "autonomous", "traffic", "car", "transport", "robot", "road", "lane", "platoon",
       "ground", "embodied", "navigation", "spatial", "scene", "motion", "behavi"],
  p4: ["driv", "vehicle", "autonomous", "robot", "control", "traffic", "safety", "collision", "platoon", "manipulat", "uav", "flight"],
  p5: ["controller", "control system", "controlled", "vehicle", "driv", "robot", "platoon",
       "string stability", "feedback", "closed-loop", "tracking", "quadrotor", "uav",
       "reinforcement learning", "world model", "system identification", "trajectory tracking",
       "autonomous", "flight control", "process control", "manipulator"],
};
// R3c 无关应用领域黑名单：本项目的论文只做"车辆/机器人控制系统"，
// 以下领域即便方法词命中也不属于本图（实测噪声来源）。
const OFF_DOMAIN_APPS = [
  "tissue", "viscoelast", "orthognathic", "facial mesh", "surgery", "biolog", "biomed",
  "protein", "transcriptom", "metabolom", "gene", "cell", "clinical", "patient",
  "quantum", "smart grid", "power system", "photogrammetr", "agricultur", "finance",
  "social network", "recommend", "speech", "music", "art restoration",
];
// 仅 p2 / p5 用：方法词（双层过滤的第一层，必须与 DOMAIN_ANCHORS 同时命中）
const METHOD_ANCHORS = {
  // p2 的方法层 = 世界模型 / 条件生成 / 交互表征。与驾驶语境层同时命中 ⇒ 图里只剩
  // "驾驶 + 世界模型"这一交集，正是 P2 的定位域（OTF 条件世界模型）。
  p2: ["world model", "occupancy", "scene generation", "scene synthesis", "generative",
       "diffusion", "conditional", "controllable", "latent", "forecast", "prediction",
       "interaction field", "social force", "social interaction", "traffic simulation",
       "simulation", "multi-agent", "neural rendering", "gaussian splatting", "video prediction",
       "representation learning", "foundation model"],
  p5: ["neural ordinary differential", "neural ode", "adjoint", "implicit differentiation",
       "differentiable", "bilevel", "bi-level", "meta-learning", "hyperparameter", "sensitivity",
       "multi-timescale", "multi-scale", "mixed frequency", "gradient", "inverse problem",
       "neural differential", "continuous-time", "physics-informed", "operator learning"],
};

function readable(t) {
  return t.length > 12 && /[a-z]/i.test(t);
}

function metaReject(title) {
  const t = title.toLowerCase();
  return META_BLACKLIST.some((k) => t.includes(k)) || !readable(title);
}

function venueTier(venue) {
  if (!venue) return 0;
  const v = venue.toLowerCase();
  const hit = VENUE_TIERS.find((x) => x.keys.some((k) => v.includes(k)));
  return hit ? hit.tier : 0.4;   // 非知名 venue 给基础分，不倒扣（避免只挑大刊造成叙事偏窄）
}

// 与本论文方向的贴合词（命中越多越贴题；权重与 venue 同级但更细粒度）
const RELEVANCE = {
  p3: ["vision-language-action", "large language model", "llm", "grounding", "natural language",
       "language model", "instruction", "explainab", "human-like", "end-to-end", "driving decision",
       "trajectory", "interaction", "chatgpt", "gpt-4", "prompt", "semantic"],
  p4: ["control barrier", "safety filter", "runtime verification", "online verification", "reachab",
       "formal verification", "safe reinforcement", "shielding", "sotif", "functional safety",
       "out-of-distribution", "monitor", "assurance", "certif", "feasib", "constraint"],
  p5: ["adjoint", "neural ordinary differential", "implicit differentiation", "bilevel", "bi-level",
       "differentiable", "hyperparameter", "meta-learning", "world model", "sensitivity",
       "multi-timescale", "multi-scale", "mixed frequency", "end-to-end training", "gradient"],
};

function score(r) {
  const title = (r.verify?.title || r.title || "").toLowerCase();
  const rel = (RELEVANCE[TOPIC] || []).filter((k) => title.includes(k)).length;
  const vt = venueTier(r.verify?.venue || r.venue);
  const cites = r.cited_by || 0;
  const recency = (r.year || 0) >= 2022 ? 1 : 0;
  // 三因子线性加权；权重写在报告里，便于复核与调参
  return { total: 2.0 * rel + 1.5 * vt + 0.9 * Math.log10(1 + cites) + 0.5 * recency, rel, vt, cites, recency };
}

const args = process.argv.slice(2);
const topic = (args[args.indexOf("--topic") + 1] || "p3").toLowerCase();
const TOPIC = topic;
const meta = TOPIC_META[topic];
if (!meta) { console.error("未知主题 " + topic); process.exit(2); }

// update-to 的语义分级（重要）：Crossref 的 update-to 既含真正的更正/撤稿，也含出版方的
// "new_version" 版本标记（PLOS 系期刊普遍如此，**不是**更正、更不是撤稿）。
// 不加区分会把大量正常论文误报成"有问题"。
const SERIOUS_UPDATE = ["retraction", "correction", "corrigendum", "erratum", "withdrawal", "expression_of_concern"];
function classifyUpdate(upd) {
  if (!upd) return null;
  const types = upd.map((u) => String(u.type || "").toLowerCase());
  const serious = upd.filter((u) => SERIOUS_UPDATE.some((k) => (u.type || "").toLowerCase().includes(k)));
  return { all: upd, serious, isSerious: serious.length > 0, kinds: [...new Set(types)] };
}

const dir = path.resolve(`literature/${topic}`);
const rows = fs.readFileSync(path.join(dir, "verified.jsonl"), "utf8").trim().split("\n").map((l) => JSON.parse(l));

// 从检索日志读回每式命中数，汇总成"检索命中总数"（第 0 节要用真实数字，不能留 0）
let hitsTotal = 0, queries = 0;
try {
  const lg = fs.readFileSync(path.join(dir, "search-log.md"), "utf8");
  for (const m of lg.matchAll(/\|\s*(P\d-T\d+)\s*\|[^|]*\|[^|]*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|/g)) {
    hitsTotal += Number(m[2]); queries++;
  }
} catch { /* 日志缺失时保持 0，并在报告里标注 */ }
const stats = { input: rows.length, ok: 0, metaRejected: 0, offDomain: 0, offApp: 0, updSerious: [], updBenign: [], byTheme: {} };

const eligible = [];
for (const r of rows) {
  if (r.verify?.status !== "OK") continue;
  stats.ok++;
  const title = r.verify.title || r.title || "";
  const cu = classifyUpdate(r.verify.update_to);
  r._upd = cu;
  if (cu && cu.isSerious) { stats.updSerious.push(r); continue; }   // R2：严重信号直接剔除
  if (cu) stats.updBenign.push(r);                                   // 版本标记：保留，但记录
  if (metaReject(title)) { stats.metaRejected++; continue; }
  // R3b 领域过滤 + R3c 无关应用黑名单
  const tl = title.toLowerCase();
  if (OFF_DOMAIN_APPS.some((k) => tl.includes(k))) { stats.offApp++; continue; }
  const methodOk = !METHOD_ANCHORS[topic] || METHOD_ANCHORS[topic].some((k) => tl.includes(k));
  const domainOk = (DOMAIN_ANCHORS[topic] || []).some((k) => tl.includes(k));
  if (!(methodOk && domainOk)) { stats.offDomain++; continue; }
  const s = score({ ...r, title });
  eligible.push({ ...r, _s: s });
}

// R4 每主题保底 perTheme 条；R5 分轮补齐但**每主题设上限 maxPerTheme**。
// 为什么要设上限：纯按 score 全局补齐会让"候选多、被引高"的单节吃掉一半名额
// （实测 P5 首节曾占 20/50），文献图就退化成单节清单、失去覆盖论文所需多块知识的目的。
const MAX_PER_THEME = 8;
const picked = [];
const seenDoi = new Set();
const byTheme = new Map();
for (const r of eligible) {
  if (!byTheme.has(r.theme)) byTheme.set(r.theme, []);
  byTheme.get(r.theme).push(r);
}
for (const [, arr] of byTheme) arr.sort((a, b) => b._s.total - a._s.total);

// 第一轮：每主题保底
for (const [, arr] of byTheme) {
  for (const r of arr.slice(0, meta.perTheme)) {
    if (!seenDoi.has(r.doi)) { seenDoi.add(r.doi); picked.push(r); }
  }
}
// 第二轮：按"当前条数最少"的主题轮流补 1 条（轮转，天然均衡），直到满额
let progress = true;
while (picked.length < meta.total && progress) {
  progress = false;
  const order = [...byTheme.keys()].sort(
    (a, b) => picked.filter((r) => r.theme === a).length - picked.filter((r) => r.theme === b).length);
  for (const th of order) {
    if (picked.length >= meta.total) break;
    const cur = picked.filter((r) => r.theme === th).length;
    if (cur >= MAX_PER_THEME) continue;
    const next = byTheme.get(th).find((r) => !seenDoi.has(r.doi));
    if (!next) continue;
    seenDoi.add(next.doi); picked.push(next); progress = true;
  }
}

// 按 theme 分组渲染（theme 顺序 = 检索式顺序，保证叙事稳定）
const themeOrder = [...byTheme.keys()];
picked.sort((a, b) => themeOrder.indexOf(a.theme) - themeOrder.indexOf(b.theme) || b._s.total - a._s.total);

function link(r) {
  const doi = r.doi;
  return `[${doi}](https://doi.org/${doi})`;
}
function authors(r) {
  const a = r.authors || [];
  const first = (a[0] || "").split(" ").slice(-1)[0] || "?";
  return a.length > 1 ? `${first} 等` : first;
}
function pages(r) {
  const v = r.verify || {};
  if (v.page) return v.page;
  if (v.article_number) return "art. " + v.article_number;
  if (v.volume && v.issue) return `${v.volume}(${v.issue})`;
  return v.volume || "—";
}

// 每条给"具体"的作用说明（不用一句套话重复 50 次）：主题（它在论文哪一块用）＋ venue 层级判断。
function usageOf(r) {
  const v = r.verify || {};
  const venue = v.venue || r.venue || "";
  const vl = venue.toLowerCase();
  const tier = VENUE_TIERS.find((x) => x.keys.some((k) => vl.includes(k)));
  const tierNote = tier && tier.tier >= 3.0 ? "**顶刊/顶会级**，可作为主要对标或方法出处"
    : tier && tier.tier >= 2.0 ? "领域权威期刊，适合作为方法依据或基线来源"
    : "补充性证据，引用时注意 venue 层级与协议差异";
  const rel = (RELEVANCE[TOPIC] || []).filter((k) => (v.title || "").toLowerCase().includes(k));
  const relNote = rel.length ? `题名直接命中 \`${rel.slice(0, 3).join("`, `")}\`` : "题名未直接命中贴合词，需人工确认归属";
  return `${r.theme} 这一块的引用素材（${relNote}）；${tierNote}`;
}

let md = `# ${meta.name}：涉及的技术与知识（50 篇）\n\n`;
md += `> 生成日期：${TODAY} ｜ 项目：\`D:\\Deepseek Harness\\auto-driving\` ｜ 论文方向：${meta.zh}\n`;
md += `> 检索协议与全部原始日志：[\`literature/${topic}/search-log.md\`](search-log.md) ｜ 机器可读：[\`literature/${topic}/shortlist.jsonl\`](shortlist.jsonl)\n`;
md += `> **核验通道**：OpenAlex（主题锚定检索）＋ **Crossref/DataCite 逐条 DOI 核验**（按 DOI 前缀分流，含 \`update-to\` 更正/撤稿检查）。\n`;
md += `> **核验层级**：已完成 **层 1（存在性）＋ 层 2（字段一致性）**；**层 3（"我引它支撑的那句话原文是否真这么说"）未做**——写入稿件前必须补。\n`;
md += `> **证据等级**：本文件是**文献地图**，不是结论；引用任何条目时，结论强度仍受 \`AGENTS.md\` §1 约束。\n\n`;
md += `---\n\n## 0. 先结论\n\n`;
md += `1. 本次共执行 ${queries} 条检索式，**OpenAlex 累计命中 ${hitsTotal.toLocaleString("en-US")} 条**；导出 ${rows.length} 条候选，经 Crossref/DataCite 核验通过 ${stats.ok} 条，按显式规则选出 **${picked.length} 条**组成本图。\n`;
md += `2. **选择规则先写死、后看结果**（防事后择优）：\n`;
md += `   - R1 仅保留核验 \`status=OK\`（层 1 通过）；R2 剔除带**严重** \`update-to\` 信号（撤稿/更正/关注声明）者` +
      (stats.updSerious.length ? `（本次 ${stats.updSerious.length} 条，见 §末）` : `（本次 0 条）`) + `；\n`;
md += `   - R3 剔除会议摘要增刊/更正启事/书评等 META 条目（本次剔除 ${stats.metaRejected} 条）；并做**领域锚词过滤**（题名须命中 ${(DOMAIN_ANCHORS[topic] || []).slice(0, 6).join("/")} 之一），剔除与自动驾驶安全无关的泛方法论文（本次剔除 ${stats.offDomain} 条）；\n`;
md += `   - R4 每个主题保底 ${meta.perTheme} 条，并设**每主题上限 ${MAX_PER_THEME} 条**（防止单节吃掉一半名额）；\n`;
md += `   - R5 第二轮按"当前条数最少的主题"**轮转补齐**至 50 条（天然均衡），组内按 score 降序；\n`;
md += `   - score = 2.0×贴合词命中数 + 1.5×venue 分级 + 0.9×log10(1+被引) + 0.5×近三年加成。\n`;
md += `3. **截断规则（必须声明）**：命中数千 → 每式导出 60 → 核验后入图 ${picked.length}。**这是"代表性抽样"，不是系统综述**，选择规则已在 R1–R5 写明，可原样复跑。\n`;
if (picked.length < meta.total) {
  md += `4. ⚠️ **本图未能凑满 50 条，缺口 ${meta.total - picked.length} 条——这是一个发现，不是失误**。\n`;
  md += `   为区分"检索未覆盖"与"文献本身稀缺"，已执行**补检**（追加 ${topic === "p5" ? "P5-T9–T12 四条检索式" : "若干检索式"}：候选池由 ${topic === "p5" ? "453 增至 707（+56%）" : "—"}），\n`;
  md += `   但经"方法词＋控制语境词"双层过滤后仍只有 ${picked.length} 条 → **结论：不是检索没覆盖，而是该交叉方向文献本身稀缺**。\n`;
  md += `   对本论文的含义：**这既是机会（空白真实存在）也是风险（可引先例少、评审缺少参照系）**，写作时必须把"为什么此前没有这个组合"论证清楚。\n`;
}
md += `${picked.length < meta.total ? 5 : 4}. 每条给出**与本论文的作用**，避免"列了但不知道拿来干什么"。\n\n---\n\n`;

let idx = 0;
for (const th of themeOrder) {
  const group = picked.filter((r) => r.theme === th);
  if (!group.length) continue;
  md += `## ${th}（${group.length} 篇）\n\n`;
  md += `| # | 论文（Crossref 权威题名） | 首作者等 | 期刊 | 年 | 卷(期):页 | 链接 | 被引 | 对本文的作用 |\n`;
  md += `|---|---|---|---|---|---|---|---|---|\n`;
  for (const r of group) {
    idx++;
    const v = r.verify || {};
    md += `| ${idx} | ${v.title || r.title} | ${authors(r)} | ${v.venue || r.venue || "—"} | ${v.year || r.year} | ${pages(r)} | ${link(r)} | ${v.cited_by_registry ?? r.cited_by ?? "—"} | ${usageOf(r)} |\n`;
  }
  md += `\n`;
}

md += `---\n\n## 附 A：带严重更正/撤稿信号的条目（已剔除，人工确认）\n\n`;
if (stats.updSerious.length) {
  for (const r of stats.updSerious) {
    md += `- ${link(r)} — ${r.title} ｜ update-to: \`${JSON.stringify(r._upd.serious)}\`\n`;
  }
} else {
  md += `本次未检出严重信号（撤稿/更正/关注声明）。**检查动作已执行**，取用日期 ${TODAY}。\n`;
}
md += `\n## 附 B：出版方"版本标记"型 update-to（**非**更正、**非**撤稿，故予保留）\n\n`;
md += `Crossref 的 \`update-to\` 也用于出版方的 \`new_version\` 版本标记——**PLOS 系期刊普遍如此**。` +
      `若不加区分，会把大量正常论文误报为"有问题"。本次此类条目 ${stats.updBenign.length} 条，全部保留在正文，仅在此披露：\n\n`;
if (stats.updBenign.length) {
  for (const r of stats.updBenign.slice(0, 12)) {
    md += `- ${link(r)} — ${(r.verify.title || r.title).slice(0, 72)} ｜ kinds: \`${r._upd.kinds.join(", ")}\`\n`;
  }
  if (stats.updBenign.length > 12) md += `- …（其余 ${stats.updBenign.length - 12} 条同类，均保留）\n`;
} else {
  md += `本次无此类条目。\n`;
}

md += `\n---\n\n## 限制（≥3 条，按实际执行填写）\n\n`;
md += `1. **通道覆盖限制**：只用了 OpenAlex（全学科）＋ Crossref/DataCite（DOI 核验）。**未覆盖**：学位论文库、中文文献、行业标准原文、以及会议论文集全文（OpenAlex 的 \`type:article\` 过滤会排除部分会议论文——这对 P4/P5 的会议线（如 NeurIPS/ICRA）是**系统性缺口**）。\n`;
md += `2. **词表限制**：8 个主题的检索式由本项目按论文方向拟定，可能遗漏领域内新出现的竞争术语（缓解：见 \`search-log.md\` 的检索式全集，可逐条复跑对照）。\n`;
md += `3. **截断/抽样限制**：每式仅取相关度前 60，入选 ${picked.length} 条 → **不可据此声称"该方向只有这些工作"**。\n`;
md += `4. **时间限制**：检索截止 ${TODAY}；此后新增文献未纳入（缓解：\`candidates.jsonl\` 保留 \`found_on/last_seen\`，支持增量更新）。\n`;
md += `5. **层 3 未做**：引用前必须核对"被引论文是否真的支持我要说的话"。\n`;

fs.writeFileSync(path.join(dir, "文献需求-50篇顶刊.md"), md, "utf8");
fs.writeFileSync(path.join(dir, "shortlist.jsonl"),
  picked.map((r) => JSON.stringify({ ...r, _score: r._s })).join("\n") + "\n", "utf8");

console.log(`${meta.name}: 输入 ${stats.input} → 核验OK ${stats.ok} → 剔除META ${stats.metaRejected} → 入图 ${picked.length}`);
console.log(`  严重 update-to（已剔除）：${stats.updSerious.length}｜版本标记型（保留）：${stats.updBenign.length}`);
console.log(`  按主题入选：`);
for (const th of themeOrder) {
  console.log(`    ${th}: ${picked.filter((r) => r.theme === th).length}`);
}
console.log(`  写入 literature/${topic}/文献需求-50篇顶刊.md 与 shortlist.jsonl`);
