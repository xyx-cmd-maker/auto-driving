// confirm2024.mjs — 定向确认查询 + 候选摘要拉取
import fs from "node:fs";
const DIR = "D:/Deepseek Harness/auto-driving/literature/fresh2024";
const MAILTO = "research@example.org";
const UA = `dsh-p1-fresh/1.0 (mailto:${MAILTO})`;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const out = { run_utc: new Date().toISOString(), confirm: [], records: [] };

// ---------- 1) 定向确认：LNN/CfC 在「车辆控制」方向 2024+ 到底有没有 ----------
const CONFIRM = [
  ["C1", 'https://api.openalex.org/works?search=' + encodeURIComponent('liquid neural network autonomous driving vehicle control') + '&filter=from_publication_date:2024-01-01&sort=relevance_score:desc&per-page=15&select=id,doi,title,publication_year,cited_by_count,primary_location&mailto=' + MAILTO, 'LNN × 驾驶/车辆控制'],
  ["C2", 'https://api.openalex.org/works?search=' + encodeURIComponent('closed-form continuous-time network control robotics') + '&filter=from_publication_date:2024-01-01&sort=relevance_score:desc&per-page=15&select=id,doi,title,publication_year,cited_by_count,primary_location&mailto=' + MAILTO, 'CfC × 控制/机器人'],
  ["C3", 'https://api.openalex.org/works?search=' + encodeURIComponent('overtaking frequency traffic') + '&filter=from_publication_date:2024-01-01&sort=relevance_score:desc&per-page=15&select=id,doi,title,publication_year,cited_by_count,primary_location&mailto=' + MAILTO, 'Overtaking frequency (OTF 本体)'],
  ["C4", 'https://api.openalex.org/works?search=' + encodeURIComponent('liquid time-constant network vehicle platoon car following') + '&filter=from_publication_date:2024-01-01&sort=relevance_score:desc&per-page=15&select=id,doi,title,publication_year,cited_by_count,primary_location&mailto=' + MAILTO, 'LTC × 编队/跟驰'],
];
for (const [id, url, tag] of CONFIRM) {
  try {
    const r = await fetch(url, { headers: { "User-Agent": UA } });
    const j = await r.json();
    const rows = (j.results || []).map((w) => ({
      year: w.publication_year,
      cited: w.cited_by_count,
      venue: (w.primary_location && w.primary_location.source && w.primary_location.source.display_name) || null,
      title: w.display_name,
      doi: (w.doi || "").replace(/^https?:\/\/doi\.org\//, ""),
    }));
    out.confirm.push({ id, tag, total: j.meta && j.meta.count, rows });
    console.log(`\n### ${id} ${tag} | total=${j.meta && j.meta.count}`);
    rows.forEach((x) => console.log(`   [${x.year}] c=${x.cited} ${(x.venue || "-").slice(0, 34).padEnd(34)} | ${x.title.slice(0, 100)} | ${x.doi}`));
  } catch (e) { out.confirm.push({ id, tag, error: e.message }); console.log(id, "ERR", e.message); }
  await sleep(400);
}

// ---------- 2) 候选摘要拉取 ----------
const DOIS = [
  "10.1038/s41467-025-62597-x", "10.1016/j.trc.2024.104486", "10.1109/tac.2024.3401082",
  "10.1109/tcst.2024.3505036", "10.1109/tcst.2024.3361393", "10.1109/tiv.2024.3373512",
  "10.1016/j.trc.2024.104941", "10.1016/j.inffus.2025.103622", "10.1109/tcst.2024.3478475",
  "10.1109/tcst.2025.3587878", "10.1109/tits.2024.3512784", "10.1109/tiv.2024.3352180",
  "10.3390/s25103191", "10.1109/lra.2024.3440097",
];
const AXIV = [
  "2605.01731", "2609.33892", "2606.20648", "2502.16466", "2506.16311",
  "2609.00385", "2604.01790", "2403.19637", "2401.01425",
  "2606.15807", "2603.27058", "2601.06227", "2510.07578", "2407.20590",
];
const inv2abs = (inv) => { if (!inv) return null; const a = []; for (const w in inv) for (const i of inv[w]) a[i] = w; return a.join(" "); };

console.log("\n=== abstracts: OpenAlex by DOI ===");
for (const d of DOIS) {
  try {
    const r = await fetch(`https://api.openalex.org/works/doi:${d}?mailto=${MAILTO}`, { headers: { "User-Agent": UA } });
    if (!r.ok) { out.records.push({ doi: d, error: "HTTP " + r.status }); console.log(`${d} HTTP ${r.status}`); await sleep(400); continue; }
    const j = await r.json();
    out.records.push({
      kind: "doi", doi: d, title: j.title, year: j.publication_year,
      venue: j.primary_location && j.primary_location.source && j.primary_location.source.display_name,
      vol: j.biblio && j.biblio.volume, issue: j.biblio && j.biblio.issue,
      first: j.biblio && j.biblio.first_page, last: j.biblio && j.biblio.last_page,
      cited: j.cited_by_count, type: j.type, oa: j.open_access && j.open_access.oa_status,
      authors: (j.authorships || []).map((a) => a.author.display_name).slice(0, 12),
      n_authors: (j.authorships || []).length,
      abstract: inv2abs(j.abstract_inverted_index),
    });
    console.log(`${d} OK  ${j.publication_year} ${(j.primary_location && j.primary_location.source && j.primary_location.source.display_name || "-").slice(0, 40)} cited=${j.cited_by_count}`);
  } catch (e) { out.records.push({ doi: d, error: e.message }); console.log(d, "ERR", e.message); }
  await sleep(400);
}

console.log("\n=== abstracts: arXiv ===");
for (let i = 0; i < AXIV.length; i += 5) {
  const batch = AXIV.slice(i, i + 5);
  const url = `https://export.arxiv.org/api/query?id_list=${batch.join(",")}&max_results=10`;
  try {
    const txt = await (await fetch(url, { headers: { "User-Agent": UA } })).text();
    let p = 0;
    while ((p = txt.indexOf("<entry>", p)) >= 0) {
      const e = txt.slice(p, txt.indexOf("</entry>", p));
      const g = (tag) => { const o = e.indexOf(`<${tag}`); if (o < 0) return null; const gt = e.indexOf(">", o); const c = e.indexOf(`</${tag}>`, gt); return c < 0 ? null : e.slice(gt + 1, c).replace(/\s+/g, " ").trim(); };
      const id = (g("id") || "").replace(/https?:\/\/arxiv\.org\/abs\//, "");
      out.records.push({
        kind: "arxiv", arxiv: id, title: g("title"), date: (g("published") || "").slice(0, 10),
        updated: (g("updated") || "").slice(0, 10),
        authors: [...e.matchAll(/<name>([^<]+)<\/name>/g)].map((m) => m[1]),
        journal_ref: g("arxiv:journal_ref"), doi: g("arxiv:doi"),
        comment: (g("arxiv:comment") || "").slice(0, 160),
        abstract: g("summary"),
      });
      console.log(`${id}  ${(g("title") || "").slice(0, 90)} | jr:${g("arxiv:journal_ref") || "-"}`);
      p += 8;
    }
  } catch (err) { console.log("batch ERR", err.message); }
  await sleep(3600);
}
fs.writeFileSync(`${DIR}/confirm2024.json`, JSON.stringify(out, null, 2), "utf8");
console.log("\nWROTE", `${DIR}/confirm2024.json`, "records=", out.records.length);
