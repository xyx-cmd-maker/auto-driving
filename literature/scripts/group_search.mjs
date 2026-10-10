// group_search.mjs — 追黄梦圆/李世武课题组的 2024+ 产出 + OTF 主题补检
import fs from "node:fs";
const DIR = "D:/Deepseek Harness/auto-driving/literature/fresh2024";
const MAILTO = "research@example.org";
const UA = `dsh-p1-fresh/1.0 (mailto:${MAILTO})`;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const pick = (s, t) => { const o = s.indexOf(`<${t}`); if (o < 0) return null; const g = s.indexOf(">", o); const c = s.indexOf(`</${t}>`, g); return c < 0 ? null : s.slice(g + 1, c).replace(/\s+/g, " ").trim(); };

const out = { run_utc: new Date().toISOString(), openalex: [], crossref: [], arxiv: [] };

// --- OpenAlex：按作者 + 主题 ---
const OA = [
  ["G1", 'https://api.openalex.org/works?filter=raw_author_name.search:Mengyuan%20Huang,from_publication_date:2023-01-01&sort=publication_date:desc&per-page=25&select=doi,title,display_name,publication_year,publication_date,cited_by_count,primary_location,authorships&mailto=' + MAILTO],
  ["G2", 'https://api.openalex.org/works?filter=raw_author_name.search:Shiwu%20Li,from_publication_date:2023-01-01&sort=publication_date:desc&per-page=25&select=doi,title,display_name,publication_year,publication_date,cited_by_count,primary_location,authorships&mailto=' + MAILTO],
  ["G3", 'https://api.openalex.org/works?search=' + encodeURIComponent('overtaking frequency autonomous vehicle behavior decision') + '&filter=from_publication_date:2023-01-01&sort=relevance_score:desc&per-page=15&select=doi,title,display_name,publication_year,cited_by_count,primary_location&mailto=' + MAILTO],
  ["G4", 'https://api.openalex.org/works?search=' + encodeURIComponent('dynamic time window overtaking frequency') + '&filter=from_publication_date:2020-01-01&sort=relevance_score:desc&per-page=15&select=doi,title,display_name,publication_year,cited_by_count,primary_location&mailto=' + MAILTO],
];
for (const [id, url] of OA) {
  try {
    const j = await (await fetch(url, { headers: { "User-Agent": UA } })).json();
    const rows = (j.results || []).map((w) => ({
      year: w.publication_year, date: w.publication_date, cited: w.cited_by_count,
      venue: (w.primary_location && w.primary_location.source && w.primary_location.source.display_name) || "-",
      title: w.display_name || "(no title)",
      doi: (w.doi || "").replace(/^https?:\/\/doi\.org\//, ""),
      authors: (w.authorships || []).map((a) => a.author.display_name).slice(0, 8),
    }));
    out.openalex.push({ id, total: j.meta && j.meta.count, rows });
    console.log(`\n### ${id}  total=${j.meta && j.meta.count}`);
    rows.forEach((x) => console.log(`   [${x.date}] c=${String(x.cited).padStart(4)} ${String(x.venue).slice(0, 34).padEnd(34)} | ${String(x.title).slice(0, 92)} | ${x.doi}\n        ${x.authors.join("; ").slice(0, 150)}`));
  } catch (e) { console.log(id, "ERR", e.message); out.openalex.push({ id, error: e.message }); }
  await sleep(400);
}

// --- Crossref：按作者名精确式 ---
const CR = [
  ["R1", '"overtaking frequency" autonomous vehicle'],
  ["R2", '"dynamic time window" overtaking'],
  ["R3", 'Huang Mengyuan Li Shiwu overtaking'],
];
for (const [id, q] of CR) {
  try {
    const url = `https://api.crossref.org/works?query.bibliographic=${encodeURIComponent(q)}&filter=from-pub-date:2020-01-01&sort=is-referenced-by-count&order=desc&rows=15&select=DOI,title,author,issued,container-title,type,is-referenced-by-count&mailto=${MAILTO}`;
    const j = await (await fetch(url, { headers: { "User-Agent": UA } })).json();
    const rows = (j.message.items || []).map((it) => ({
      year: it.issued && it.issued["date-parts"] && it.issued["date-parts"][0] ? it.issued["date-parts"][0][0] : null,
      cited: it["is-referenced-by-count"],
      venue: (it["container-title"] && it["container-title"][0]) || "-",
      title: (it.title && it.title[0]) || "(no title)",
      doi: it.DOI,
      authors: (it.author || []).map((a) => [a.given, a.family].filter(Boolean).join(" ")).join("; ").slice(0, 150),
    }));
    out.crossref.push({ id, q, total: j.message["total-results"], rows });
    console.log(`\n### ${id} "${q}"  total=${j.message["total-results"]}`);
    rows.forEach((x) => console.log(`   [${x.year}] c=${String(x.cited).padStart(4)} ${String(x.venue).slice(0, 34).padEnd(34)} | ${String(x.title).slice(0, 92)} | ${x.doi}\n        ${x.authors}`));
  } catch (e) { console.log(id, "ERR", e.message); out.crossref.push({ id, q, error: e.message }); }
  await sleep(3000);
}

// --- arXiv：OTF / 超车频次 ---
const AX = [["Y1", 'all:"overtaking frequency"'], ["Y2", 'all:"overtaking" AND all:"frequency" AND all:"traffic"']];
for (const [id, q] of AX) {
  const url = `https://export.arxiv.org/api/query?search_query=${encodeURIComponent(q)}&start=0&max_results=40&sortBy=submittedDate&sortOrder=descending`;
  const txt = await (await fetch(url, { headers: { "User-Agent": UA } })).text();
  const rows = []; let p = 0;
  while ((p = txt.indexOf("<entry>", p)) >= 0) {
    const e = txt.slice(p, txt.indexOf("</entry>", p));
    rows.push({ date: (pick(e, "published") || "").slice(0, 10), arxiv: (pick(e, "id") || "").replace(/https?:\/\/arxiv\.org\/abs\//, ""), title: pick(e, "title"), jr: pick(e, "arxiv:journal_ref") });
    p += 8;
  }
  out.arxiv.push({ id, q, total: pick(txt, "opensearch:totalResults"), rows });
  console.log(`\n### ${id} "${q}"  total=${pick(txt, "opensearch:totalResults")}`);
  rows.filter((r) => r.date >= "2023-01-01").forEach((r) => console.log(`   [${r.date}] ${String(r.title).slice(0, 96)} | ${r.arxiv} | jr:${r.jr || "-"}`));
  await sleep(3600);
}
fs.writeFileSync(`${DIR}/group_search.json`, JSON.stringify(out, null, 2), "utf8");
console.log(`\nWROTE ${DIR}/group_search.json`);
