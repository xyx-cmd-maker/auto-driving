// scripts/literature/discover.mjs — P3/P4/P5 主题化检索 + Crossref 权威核验
//
// 与 literature/scripts/search.mjs 的关系：**同模式、同通道、同字段纪律**，但把检索式
// 外置为"主题 → 若干查询"，以支持 P3/P4/P5 三篇论文（原脚本的查询是 P1 专用的、写死的）。
//
// 用法：
//   node scripts/literature/discover.mjs --topic p3 --out literature/p3        # 检索
//   node scripts/literature/discover.mjs --verify literature/p3/candidates.jsonl  # Crossref 核验
//   node scripts/literature/discover.mjs --topic p5 --dry                       # 只打印检索式
//
// 纪律（paper-discovery 技能 §2/§7）：
//   - 记"命中数"与"导出数"两栏，不混用
//   - 排序与截断规则显式写出（relevance_score 前 N）
//   - 时效：每条查询随附取用日期（T1）；核验含撤稿/更正检查（T5，按 DOI 前缀分流）
import fs from "node:fs";
import path from "node:path";

const MAILTO = process.env.OPENALEX_MAILTO || "research@example.org";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const TODAY = new Date().toISOString().slice(0, 10);

// ── 每篇论文的检索主题（theme 即最终文献图的分节）──
const TOPICS = {
  p2: {
    name: "P2 SocialDreamer",
    title: "以 OTF 社会压力场为结构条件模态的驾驶世界模型",
    from: "2019-01-01",
    // 检索式设计依据（写在此处以便复核，而不是事后猜）：
    //   P2 的定位是"**首个以交通流社会压力场（OTF 场）为结构条件模态**的世界模型"，
    //   对标对象 DriveDreamer（ECCV 2024）的结构条件是 HDMap / 3D Box。
    //   主题分四组：世界模型本体、条件模态与可控生成、社会交互/压力场、交通流与多智能体。
    //   **不得**把"是否已有 OTF 条件世界模型"当作已知——这正是本检索要回答的空缺。
    queries: [
      { id: "P2-T1", theme: "驾驶世界模型（预测/规划）", q: '"world model" AND ("autonomous driving" OR "driving")' },
      { id: "P2-T2", theme: "驾驶场景生成与合成", q: '"driving scene" AND ("generation" OR "synthesis") AND ("world model" OR "diffusion")' },
      { id: "P2-T3", theme: "条件模态与可控 rollout", q: '"conditional" AND "world model" AND ("controllable" OR "conditioning")' },
      { id: "P2-T4", theme: "社会交互与压力场建模", q: '("social force" OR "social interaction" OR "interaction field") AND (driving OR vehicle OR traffic)' },
      { id: "P2-T5", theme: "交互感知的行为/轨迹预测", q: '"interaction-aware" AND ("trajectory prediction" OR "behavior prediction") AND vehicle' },
      { id: "P2-T6", theme: "多智能体交通流仿真与生成", q: '"multi-agent" AND ("traffic simulation" OR "traffic flow") AND ("learning" OR "generative")' },
      { id: "P2-T7", theme: "占用/潜空间世界模型", q: '("occupancy" OR "latent") AND "world model" AND driving' },
      { id: "P2-T8", theme: "扩散模型用于轨迹与场景生成", q: '"diffusion model" AND ("trajectory" OR "scene") AND ("prediction" OR "generation") AND driving' },
    ],
  },
  p3: {
    name: "P3 TalkOTF",
    title: "语言 → OTF 定量 grounding 与指令合法性检查",
    from: "2016-01-01",
    queries: [
      { id: "P3-T1", theme: "LLM 用于自动驾驶决策", q: '"large language model" AND "autonomous driving"' },
      { id: "P3-T2", theme: "VLA / 视觉-语言-动作模型", q: '"vision-language-action" OR "vision language action"' },
      { id: "P3-T3", theme: "语言条件轨迹规划", q: '"language" AND "trajectory" AND ("planning" OR "generation") AND vehicle' },
      { id: "P3-T4", theme: "人类驾驶行为建模与自然语言", q: '"driving behavior" AND ("natural language" OR "language model")' },
      { id: "P3-T5", theme: "语言 grounding 到物理量", q: '"grounding" AND ("physical" OR "quantitative" OR "scalar") AND (language OR text)' },
      { id: "P3-T6", theme: "可解释驾驶与自然语言接口", q: '"explainable" AND "autonomous driving" AND ("language" OR "explanation")' },
      { id: "P3-T7", theme: "端到端驾驶的大模型", q: '"end-to-end" AND "autonomous driving" AND ("foundation model" OR "large model")' },
      { id: "P3-T8", theme: "语言交互式车辆决策", q: '"human-like" AND ("interaction" OR "interface") AND ("autonomous vehicle" OR "driving")' },
    ],
  },
  p4: {
    name: "P4 IsoLNN",
    title: "连续可导控制器的安全隔离与物理可行性筛查",
    from: "2015-01-01",
    queries: [
      { id: "P4-T1", theme: "控制障碍函数 / 安全滤波器", q: '"control barrier function"' },
      { id: "P4-T2", theme: "运行时验证 / 在线验证", q: '"runtime verification" OR "online verification"' },
      { id: "P4-T3", theme: "神经网络控制器的形式化验证", q: '"formal verification" AND ("neural network" OR "neural controller")' },
      { id: "P4-T4", theme: "可达性分析与安全包络", q: '"reachability analysis" AND (safety OR control)' },
      { id: "P4-T5", theme: "安全强化学习与屏蔽机制", q: '"safe reinforcement learning" OR "shielding"' },
      { id: "P4-T6", theme: "SOTIF / 预期功能安全", q: '"SOTIF" OR "functional safety" AND "autonomous driving"' },
      { id: "P4-T7", theme: "OOD 检测与失效预测", q: '"out-of-distribution" AND ("detection" OR "monitoring") AND (driving OR robot)' },
      { id: "P4-T8", theme: "学习控制器的可行性与约束满足", q: '"learned controller" AND ("feasibility" OR "constraint satisfaction")' },
      { id: "P4-T9", theme: "自动驾驶安全保证与论证", q: '"safety assurance" OR "safety case" AND autonomous' },
    ],
  },
  p5: {
    name: "P5 AdjointStack",
    title: "混合频率伴随敏感度与联合微调",
    from: "2016-01-01",
    queries: [
      { id: "P5-T1", theme: "神经 ODE 与伴随法", q: '"neural ordinary differential equation" OR "adjoint sensitivity"' },
      { id: "P5-T2", theme: "隐式微分与可微优化", q: '"implicit differentiation" OR "differentiable optimization"' },
      { id: "P5-T3", theme: "双层优化与元学习", q: '"bilevel optimization" AND ("machine learning" OR "deep learning")' },
      { id: "P5-T4", theme: "基于梯度的超参数敏感度", q: '"hyperparameter" AND "gradient" AND ("optimization" OR "sensitivity")' },
      { id: "P5-T5", theme: "世界模型与基于模型的 RL", q: '"world model" AND ("model-based reinforcement learning" OR "planning")' },
      { id: "P5-T6", theme: "可微仿真与物理先验", q: '"differentiable simulation" OR "differentiable physics"' },
      { id: "P5-T7", theme: "混合频率 / 多时间尺度训练", q: '"multi-timescale" OR "mixed frequency" OR "temporal hierarchy" AND learning' },
      { id: "P5-T8", theme: "端到端可微驾驶栈", q: '"end-to-end" AND "differentiable" AND (driving OR "autonomous driving")' },
      // T9–T12：补检（2026-10-11）。起因：T1–T8 的初检经"方法词＋控制语境词"双层过滤后
      // 只剩 26 条可用，怀疑是检索式未覆盖 P5 真正的近邻语汇（闭环联合训练、可微 MPC、
      // 控制器敏感度整定），而非文献真的稀缺。补检用于区分这两种解释。
      { id: "P5-T9", theme: "闭环联合训练与端到端微调", q: '"closed-loop" AND ("joint training" OR "fine-tuning" OR "finetuning") AND (control OR driving OR robot)' },
      { id: "P5-T10", theme: "可微模型预测控制", q: '"differentiable model predictive control" OR "differentiable MPC"' },
      { id: "P5-T11", theme: "控制器敏感度与梯度整定", q: '"sensitivity analysis" AND ("controller tuning" OR "control parameter") AND (gradient OR automatic differentiation)' },
      { id: "P5-T12", theme: "学习控制器与世界模型的联合优化", q: '("world model" OR "dynamics model") AND ("controller" OR "policy") AND ("joint" OR "end-to-end") AND optimization' },
    ],
  },
};

const FIELDS = ["id", "doi", "title", "display_name", "publication_year", "publication_date",
  "type", "cited_by_count", "authorships", "primary_location", "language"].join(",");

function openalexUrl(q, fromDate, perPage) {
  const params = new URLSearchParams({
    search: q,
    filter: `type:article,language:en,from_publication_date:${fromDate}`,
    sort: "relevance_score:desc",     // 显式排序：相关度优先，不用 cited_by（避免只看老文）
    "per-page": String(perPage),
    select: FIELDS,
    mailto: MAILTO,
  });
  return `https://api.openalex.org/works?${params.toString()}`;
}

async function getJson(url, tries = 3) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url, { headers: { "User-Agent": "dsh-paper-discovery/1.0 (mailto:research@example.org)" } });
      if (r.status === 429 || r.status >= 500) { await sleep(1500 * (i + 1)); continue; }
      if (!r.ok) return { error: `HTTP ${r.status}` };
      return { json: await r.json() };
    } catch (e) {
      await sleep(1000 * (i + 1));
      if (i === tries - 1) return { error: e.message };
    }
  }
  return { error: "exhausted retries" };
}

function norm(rec, qid, theme) {
  const src = (rec.primary_location || {}).source || {};
  return {
    openalex_id: (rec.id || "").replace("https://openalex.org/", ""),
    doi: rec.doi ? rec.doi.replace("https://doi.org/", "").toLowerCase() : null,
    title: rec.display_name || rec.title || "",
    year: rec.publication_year, date: rec.publication_date,
    venue: src.display_name || null, venue_type: src.type || null,
    type: rec.type, cited_by: rec.cited_by_count,
    authors: (rec.authorships || []).slice(0, 12).map((a) => (a.author && a.author.display_name) || ""),
    n_authors: (rec.authorships || []).length,
    query_ids: [qid], theme,
    found_on: TODAY, last_seen: TODAY,
  };
}

// ── Crossref 逐条核验（层 1 存在性 + 层 2 字段一致性 + T5 撤稿/更正检查）──
async function verify(relPath) {
  const abs = path.resolve(relPath);
  const rows = fs.readFileSync(abs, "utf8").trim().split("\n").map((l) => JSON.parse(l));
  const withDoi = rows.filter((r) => r.doi);
  const out = [];
  let n = 0;
  for (const r of withDoi) {
    n++;
    const isArxivDoi = r.doi.startsWith("10.48550/");
    const reg = isArxivDoi ? "datacite" : "crossref";
    const url = isArxivDoi ? `https://api.datacite.org/dois/${r.doi}`
      : `https://api.crossref.org/works/${encodeURIComponent(r.doi)}`;
    const { json, error } = await getJson(url);
    const rec = { ...r, registry: reg };
    if (error) {
      rec.verify = { status: "FAIL", error, checked_on: TODAY };
    } else if (isArxivDoi) {
      const a = json.data?.attributes || {};
      rec.verify = {
        status: "OK", checked_on: TODAY,
        title: a.titles?.[0]?.title || null, year: a.publicationYear || null,
        venue: a.publisher || null, cited_by_registry: a.citationCount ?? null,
      };
    } else {
      const m = json.message || {};
      // 年份口径（重要）：Crossref 的 issued 常是**在线首发**年，而 IEEE 等期刊的**卷期正式年**
      // 在 published-print。P1 文献图已记录过这个坑（在线首发普遍早 1–2 年）。
      // 一律优先 published-print → published-online → issued。
      const pick = (k) => (m[k]?.["date-parts"]?.[0] || []);
      const printParts = pick("published-print");
      const onlineParts = pick("published-online");
      const issuedParts = pick("issued");
      const parts = printParts.length ? printParts : (onlineParts.length ? onlineParts : issuedParts);
      const upd = m["update-to"] || null;
      rec.verify = {
        status: "OK", checked_on: TODAY,
        title: (m.title || [])[0] || null,
        year: parts[0] || null, month: parts[1] || null,
        year_basis: printParts.length ? "published-print" : (onlineParts.length ? "published-online" : "issued"),
        year_issued: issuedParts[0] || null,
        year_online: onlineParts[0] || null,
        venue: (m["container-title"] || [])[0] || null,
        volume: m.volume || null, issue: m.issue || null, page: m.page || null,
        article_number: m["article-number"] || null,
        cited_by_registry: m["is-referenced-by-count"] ?? null,
        // T5：撤稿/更正信号（语义分级在 triage.mjs 里做）
        update_to: upd ? upd.map((u) => ({ type: u.type, doi: u.DOI, label: u.label })) : null,
      };
    }
    out.push(rec);
    if (n % 25 === 0) console.log(`  已核验 ${n}/${withDoi.length}`);
    await sleep(120);   // Crossref 礼貌间隔
  }
  const outPath = path.join(path.dirname(abs), "verified.jsonl");
  fs.writeFileSync(outPath, out.map((r) => JSON.stringify(r)).join("\n") + "\n", "utf8");
  const ok = out.filter((r) => r.verify.status === "OK").length;
  const upd = out.filter((r) => r.verify.update_to).length;
  console.log(`\n核验完成：${ok}/${out.length} 存在且字段可取；${upd} 条带 update-to（更正/撤稿信号）`);
  console.log(`写入 ${outPath}`);
  if (upd) {
    console.log("带 update-to 的条目（须人工确认）：");
    out.filter((r) => r.verify.update_to).forEach((r) =>
      console.log(`  ${r.doi}  ${r.title.slice(0, 70)}  → ${JSON.stringify(r.verify.update_to)}`));
  }
}

async function discover(topicKey, outDir, perPage, dry) {
  const t = TOPICS[topicKey];
  if (!t) { console.error(`未知主题 ${topicKey}（可选 ${Object.keys(TOPICS).join(", ")}）`); process.exit(2); }
  if (dry) {
    console.log(`# ${t.name}：${t.title}`);
    for (const q of t.queries) console.log(`${q.id}  ${openalexUrl(q.q, t.from, perPage)}`);
    return;
  }
  const pool = new Map();
  const log = [];
  console.log(`# ${t.name} 检索｜执行日期 ${TODAY}｜时间窗 ${t.from} 起｜type=article,lang=en｜排序 relevance_score｜截断前 ${perPage}/式`);
  for (const q of t.queries) {
    const url = openalexUrl(q.q, t.from, perPage);
    const { json, error } = await getJson(url);
    if (error) {
      console.log(`  ${q.id}  FAIL ${error}`);
      log.push({ id: q.id, theme: q.theme, q: q.q, url, hits: null, exported: 0, added: 0, error });
      await sleep(700); continue;
    }
    const hits = json.meta?.count ?? 0;
    const recs = json.results || [];
    let added = 0;
    for (const rec of recs) {
      const r = norm(rec, q.id, q.theme);
      const key = r.doi ? `doi:${r.doi}` : `oa:${r.openalex_id}`;
      if (pool.has(key)) { pool.get(key).query_ids.push(q.id); continue; }
      pool.set(key, r); added++;
    }
    console.log(`  ${q.id}  OK  hits=${hits}  exported=${recs.length}  new=${added}  | ${q.theme}`);
    log.push({ id: q.id, theme: q.theme, q: q.q, url, hits, exported: recs.length, added });
    await sleep(700);
  }
  const rows = [...pool.values()];
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, "candidates.jsonl"), rows.map((r) => JSON.stringify(r)).join("\n") + "\n", "utf8");

  const logPath = path.join(outDir, "search-log.md");
  const head = `# 检索日志：${t.name} —— ${t.title}\n\n` +
    `执行日期：${TODAY}｜执行者：\`scripts/literature/discover.mjs\`（自动化）｜通道：OpenAlex\n` +
    `时间窗：${t.from} 起｜文献类型：article｜语言：en｜排序：relevance_score 降序｜每式截断：前 ${perPage} 条\n\n` +
    `## 逐查询命中与导出\n\n| query_id | 主题 | 检索式 | 命中 | 导出 | 新增 |\n|---|---|---|---|---|---|\n`;
  const body = log.map((l) =>
    `| ${l.id} | ${l.theme} | \`${l.q}\` | ${l.hits ?? "FAIL"} | ${l.exported} | ${l.added} |`).join("\n");
  const urls = log.map((l) => `- ${l.id}: ${l.url}`).join("\n");
  fs.writeFileSync(logPath, head + body + `\n\n## 完整检索式（可原样复制）\n\n${urls}\n`, "utf8");

  const withDoi = rows.filter((r) => r.doi).length;
  console.log(`\n候选池去重后 N=${rows.length}（带 DOI ${withDoi}，无 DOI ${rows.length - withDoi}）`);
  console.log(`写入 ${path.join(outDir, "candidates.jsonl")} 与 ${logPath}`);
  console.log(`下一步：node scripts/literature/discover.mjs --verify ${path.join(outDir, "candidates.jsonl")}`);
}

const args = process.argv.slice(2);
const get = (k, d) => (args.includes(k) ? args[args.indexOf(k) + 1] : d);
if (args.includes("--verify")) {
  await verify(get("--verify"));
} else {
  await discover((get("--topic", "p3")).toLowerCase(), get("--out", `literature/${get("--topic", "p3")}`),
    Number(get("--per-page", 60)), args.includes("--dry"));
}
