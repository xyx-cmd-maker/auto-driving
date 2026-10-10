// fresh2024.mjs — P1 增量检索：只收 2024-01-01 之后的工作
// 通道：OpenAlex（主题 + venue 锚定）｜Crossref（短语精确式）｜arXiv（submittedDate 降序）
// 输出：candidates_2024.jsonl + candidates_2024.log.json
import fs from "node:fs";

const MAILTO = "research@example.org";
const FROM = "2024-01-01";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const UA = `dsh-p1-fresh/1.0 (mailto:${MAILTO})`;

const log = { run_utc: new Date().toISOString(), from: FROM, channels: [], queries: [] };
const pool = [];
const push = (rec) => pool.push(rec);

// ---------- OpenAlex 主题检索 ----------
const TOPIC = [
  ["T01", "liquid neural network"],
  ["T02", "liquid time-constant network"],
  ["T03", "closed-form continuous-time neural network"],
  ["T04", "neural ordinary differential equation control"],
  ["T05", "continuous-time neural network controller"],
  ["T06", "car-following reinforcement learning"],
  ["T07", "string stability mixed traffic"],
  ["T08", "vehicle platoon learning-based control"],
  ["T09", "overtaking behaviour traffic flow"],
  ["T10", "social pressure field traffic flow model"],
  ["T11", "interpretable end-to-end autonomous driving"],
  ["T12", "microcontroller deployment neural network inference"],
];
// ---------- OpenAlex venue 锚定（ISSN 经项目既有核验） ----------
const VENUE = [
  ["K01", "1524-9050", "liquid neural network OR continuous-time neural network"],
  ["K02", "1524-9050", "car-following OR platoon OR mixed traffic control"],
  ["K03", "2379-8858", "continuous-time control OR neural ODE"],
  ["K04", "0968-090X", "car-following deep learning OR reinforcement learning"],
  ["K05", "1063-6536", "platoon string stability"],
  ["K06", "2522-5839", "continuous-time neural network"],
  ["K07", "2377-3766", "liquid neural network OR neural circuit policy"],
  ["K08", "0018-9286", "mixed traffic platoon OR string stability"],
];

const oaSelect = "id,doi,title,display_name,publication_year,publication_date,type,cited_by_count,authorships,primary_location,language";

async function openalex(id, url, tag) {
  for (let k = 0; k < 4; k++) {
    try {
      const r = await fetch(url, { headers: { "User-Agent": UA } });
      if (r.status === 429) { log.queries.push({ id, channel: "openalex", status: 429, attempt: k }); await sleep(8000 * (k + 1)); continue; }
      if (!r.ok) throw new Error("HTTP " + r.status);
      const j = await r.json();
      const rows = (j.results || []).map((w) => ({
        source: "openalex", query_id: id, query: tag,
        doi: (w.doi || "").replace(/^https?:\/\/doi\.org\//, "").toLowerCase() || null,
        title: w.display_name || (w.title || ""),
        year: w.publication_year, date: w.publication_date,
        venue: (w.primary_location && w.primary_location.source && w.primary_location.source.display_name) || null,
        issn: (w.primary_location && w.primary_location.source && w.primary_location.source.issn_l) || null,
        type: w.type, cited: w.cited_by_count,
        first_author: (w.authorships && w.authorships[0] && w.authorships[0].author && w.authorships[0].author.display_name) || null,
        n_authors: (w.authorships || []).length,
      }));
      log.queries.push({ id, channel: "openalex", status: 200, hits: rows.length, total: (j.meta && j.meta.count) || null });
      rows.forEach(push);
      return;
    } catch (e) { log.queries.push({ id, channel: "openalex", status: "ERR", err: e.message, attempt: k }); await sleep(4000 * (k + 1)); }
  }
}

console.log("=== OpenAlex topic + venue ===");
for (const [id, q] of TOPIC) {
  const url = `https://api.openalex.org/works?search=${encodeURIComponent(q)}`
    + `&filter=from_publication_date:${FROM},type:article,language:en`
    + `&sort=cited_by_count:desc&per-page=25&select=${oaSelect}&mailto=${MAILTO}`;
  await openalex(id, url, q);
  const last = log.queries[log.queries.length - 1];
  console.log(`${id} status=${last.status} hits=${last.hits ?? "-"} ${q}`);
  await sleep(350);
}
for (const [id, issn, q] of VENUE) {
  const url = `https://api.openalex.org/works?search=${encodeURIComponent(q)}`
    + `&filter=primary_location.source.issn:${issn},from_publication_date:${FROM},language:en`
    + `&sort=cited_by_count:desc&per-page=15&select=${oaSelect}&mailto=${MAILTO}`;
  await openalex(id, url, q);
  const last = log.queries[log.queries.length - 1];
  console.log(`${id} status=${last.status} hits=${last.hits ?? "-"} [${issn}] ${q}`);
  await sleep(350);
}

// ---------- Crossref 短语精确式（近两年） ----------
const CROSS = [
  ["X01", '"liquid neural network"'],
  ["X02", '"liquid time-constant"'],
  ["X03", '"closed-form continuous-time" neural'],
  ["X04", '"neural circuit policy" control'],
  ["X05", '"continuous-time" "car-following" control'],
  ["X06", '"string stability" "mixed traffic"'],
  ["X07", '"overtaking" "car-following" stability'],
  ["X08", '"physics-informed" "vehicle platoon"'],
  ["X09", '"microcontroller" "neural network" real-time control'],
  ["X10", '"interpretable" "end-to-end" driving policy'],
];
console.log("\n=== Crossref ===");
for (const [id, q] of CROSS) {
  const url = `https://api.crossref.org/works?query.bibliographic=${encodeURIComponent(q)}`
    + `&filter=from-pub-date:${FROM},type:journal-article`
    + `&sort=is-referenced-by-count&order=desc&rows=20`
    + `&select=DOI,title,author,issued,container-title,type,volume,issue,page,is-referenced-by-count&mailto=${MAILTO}`;
  let ok = false;
  for (let k = 0; k < 4 && !ok; k++) {
    try {
      const r = await fetch(url, { headers: { "User-Agent": UA } });
      if (r.status === 429) { await sleep(9000 * (k + 1)); continue; }
      if (!r.ok) throw new Error("HTTP " + r.status);
      const j = await r.json();
      const rows = (j.message.items || []).map((it) => ({
        source: "crossref", query_id: id, query: q,
        doi: (it.DOI || "").toLowerCase() || null,
        title: (it.title && it.title[0]) || "",
        year: it.issued && it.issued["date-parts"] && it.issued["date-parts"][0] ? it.issued["date-parts"][0][0] : null,
        venue: (it["container-title"] && it["container-title"][0]) || null,
        type: it.type, cited: it["is-referenced-by-count"],
        first_author: it.author && it.author[0] ? [it.author[0].given, it.author[0].family].filter(Boolean).join(" ") : null,
        n_authors: it.author ? it.author.length : null,
        vol: it.volume, issue: it.issue, page: it.page,
      }));
      log.queries.push({ id, channel: "crossref", status: 200, hits: rows.length, total: j.message["total-results"] });
      rows.forEach(push);
      console.log(`${id} hits=${rows.length} ${q}`);
      ok = true;
    } catch (e) { log.queries.push({ id, channel: "crossref", status: "ERR", err: e.message, attempt: k }); await sleep(6000 * (k + 1)); }
  }
  if (!ok) console.log(`${id} FAILED ${q}`);
  await sleep(1500);
}

// ---------- arXiv ----------
const AX = [
  ["A01", 'all:"liquid neural network"'],
  ["A02", 'all:"liquid time-constant"'],
  ["A03", 'all:"closed-form continuous-time"'],
  ["A04", 'all:"neural circuit policy"'],
  ["A05", 'all:"car-following" AND all:"neural ODE"'],
  ["A06", 'all:"string stability" AND all:"reinforcement learning"'],
  ["A07", 'all:"vehicle platoon" AND all:"learning"'],
  ["A08", 'all:"overtaking" AND all:"traffic"'],
  ["A09", 'all:"interpretable" AND all:"driving policy"'],
  ["A10", 'all:"continuous-time" AND all:"control" AND all:"neural network"'],
];
console.log("\n=== arXiv ===");
const pick = (s, tag) => { const o = s.indexOf(`<${tag}`); if (o < 0) return null; const g = s.indexOf(">", o); const c = s.indexOf(`</${tag}>`, g); return c < 0 ? null : s.slice(g + 1, c).replace(/\s+/g, " ").trim(); };
for (const [id, q] of AX) {
  const url = `https://export.arxiv.org/api/query?search_query=${encodeURIComponent(q)}&start=0&max_results=40&sortBy=submittedDate&sortOrder=descending`;
  let txt = "", ok = false;
  for (let k = 0; k < 4 && !ok; k++) {
    try { txt = await (await fetch(url, { headers: { "User-Agent": UA } })).text(); ok = txt.includes("totalResults"); }
    catch (e) { await sleep(5000 * (k + 1)); }
    if (!ok) await sleep(5000 * (k + 1));
  }
  let n = 0, since = 0;
  let p = 0;
  while ((p = txt.indexOf("<entry>", p)) >= 0) {
    const e = txt.slice(p, txt.indexOf("</entry>", p));
    const pub = (pick(e, "published") || "").slice(0, 10);
    if (pub >= FROM) {
      since++;
      push({
        source: "arxiv", query_id: id, query: q,
        doi: (pick(e, "arxiv:doi") || "").toLowerCase() || null,
        arxiv: (pick(e, "id") || "").replace(/https?:\/\/arxiv\.org\/abs\//, ""),
        title: pick(e, "title"), year: +pub.slice(0, 4), date: pub,
        venue: pick(e, "arxiv:journal_ref") || null,
        type: "preprint", cited: null,
        first_author: (e.match(/<name>([^<]+)<\/name>/) || [, null])[1],
        comment: (pick(e, "arxiv:comment") || "").slice(0, 120),
      });
    }
    n++; p += 8;
  }
  log.queries.push({ id, channel: "arxiv", status: ok ? 200 : "ERR", fetched: n, since_2024: since });
  console.log(`${id} fetched=${n} since2024=${since} ${q}`);
  await sleep(3600);
}

// ---------- 去重 + 落盘 ----------
const key = (r) => r.doi || r.arxiv || (r.title || "").toLowerCase().replace(/[^a-z0-9]/g, "").slice(0, 80);
const map = new Map();
for (const r of pool) {
  const k = key(r);
  if (!k) continue;
  if (!map.has(k)) map.set(k, { ...r, query_ids: [r.query_id] });
  else { const e = map.get(k); if (!e.query_ids.includes(r.query_id)) e.query_ids.push(r.query_id); if (!e.cited && r.cited) e.cited = r.cited; if (!e.venue && r.venue) e.venue = r.venue; }
}
const uniq = [...map.values()].sort((a, b) => (b.cited || 0) - (a.cited || 0));
const OUT = "D:/Deepseek Harness/auto-driving/literature/fresh2024";
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(`${OUT}/candidates_2024.jsonl`, uniq.map((r) => JSON.stringify(r)).join("\n") + "\n", "utf8");
log.totals = { raw: pool.length, unique: uniq.length, by_source: {} };
for (const r of uniq) log.totals.by_source[r.source] = (log.totals.by_source[r.source] || 0) + 1;
fs.writeFileSync(`${OUT}/candidates_2024.log.json`, JSON.stringify(log, null, 2), "utf8");
console.log(`\nRAW=${pool.length} UNIQUE=${uniq.length}`);
console.log("by_source=", JSON.stringify(log.totals.by_source));
console.log("WROTE", OUT);
