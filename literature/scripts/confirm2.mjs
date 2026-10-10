// confirm2.mjs — 修复空标题后的定向确认
import fs from "node:fs";
const DIR = "D:/Deepseek Harness/auto-driving/literature/fresh2024";
const MAILTO = "research@example.org";
const UA = `dsh-p1-fresh/1.0 (mailto:${MAILTO})`;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const CONFIRM = [
  ["C1", 'liquid neural network autonomous driving vehicle control', 'LNN × 驾驶/车辆控制'],
  ["C2", 'closed-form continuous-time network control robotics', 'CfC × 控制/机器人'],
  ["C3", 'overtaking frequency traffic', 'Overtaking frequency（OTF 本体）'],
  ["C4", 'liquid time-constant network vehicle platoon car following', 'LTC × 编队/跟驰'],
  ["C5", 'neural circuit policy control', 'NCP × 控制'],
  ["C6", 'continuous-time recurrent network end-to-end driving', '连续时间网络 × 端到端驾驶'],
];
const out = [];
for (const [id, q, tag] of CONFIRM) {
  const url = `https://api.openalex.org/works?search=${encodeURIComponent(q)}`
    + `&filter=from_publication_date:2024-01-01&sort=relevance_score:desc&per-page=12`
    + `&select=id,doi,title,display_name,publication_year,cited_by_count,primary_location&mailto=${MAILTO}`;
  try {
    const r = await fetch(url, { headers: { "User-Agent": UA } });
    const j = await r.json();
    const rows = (j.results || []).map((w) => ({
      year: w.publication_year,
      cited: w.cited_by_count,
      venue: (w.primary_location && w.primary_location.source && w.primary_location.source.display_name) || "-",
      title: (w.display_name || w.title || "(no title)"),
      doi: (w.doi || "").replace(/^https?:\/\/doi\.org\//, ""),
    }));
    out.push({ id, tag, query: q, total: j.meta && j.meta.count, rows });
    console.log(`\n### ${id} ${tag}  |  命中总数=${j.meta && j.meta.count}  |  式: ${q}`);
    rows.forEach((x) => console.log(`   [${x.year}] c=${String(x.cited).padStart(5)} ${String(x.venue).slice(0, 32).padEnd(32)} | ${String(x.title).slice(0, 96)} | ${x.doi}`));
  } catch (e) { console.log(id, "ERR", e.message); out.push({ id, tag, query: q, error: e.message }); }
  await sleep(400);
}
fs.writeFileSync(`${DIR}/confirm_targeted.json`, JSON.stringify(out, null, 2), "utf8");
console.log("\nWROTE", `${DIR}/confirm_targeted.json`);
