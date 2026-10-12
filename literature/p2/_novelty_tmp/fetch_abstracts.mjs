// Temporary helper: fetch OpenAlex/Crossref/DataCite abstracts for the 18 P2 entries.
// Channel: OpenAlex abstract_inverted_index -> reconstructed text.
const DOIS = [
  // 驾驶世界模型（预测/规划）
  "10.3390/app15168986",
  "10.1109/lra.2020.2966414",
  "10.1109/lra.2025.3608656",
  "10.1016/j.trc.2025.105456",
  "10.1109/tiv.2024.3398357",
  "10.1016/j.inffus.2024.102671",
  "10.1109/tiv.2024.3408830",
  "10.1561/2300000078",
  // 条件模态与可控 rollout
  "10.26599/commtr.2026.9640042",
  "10.1088/1742-5468/ad292b",
  "10.1016/j.compind.2026.104442",
  // 多智能体交通流仿真与生成
  "10.1016/j.ijtst.2025.07.011",
  "10.1109/tits.2022.3220961",
  "10.1016/j.trpro.2024.12.122",
  "10.3390/s23052373",
  "10.1109/tits.2025.3602664",
  "10.1016/j.trc.2026.106054",
  "10.1109/tvcg.2024.3392587",
];

const MAILTO = "research@example.org";

function invert(idx) {
  if (!idx) return null;
  const arr = [];
  for (const [w, poss] of Object.entries(idx)) for (const p of poss) arr[p] = w;
  return arr.filter(Boolean).join(" ");
}

async function j(url) {
  const r = await fetch(url, { headers: { "User-Agent": "novelty-check/1.0 (mailto:" + MAILTO + ")" } });
  return { status: r.status, body: r.status === 200 ? await r.json() : await r.text() };
}

const out = [];
for (const doi of DOIS) {
  const rec = { doi };
  const oa = await j(`https://api.openalex.org/works/doi:${doi}?mailto=${MAILTO}`);
  if (oa.status === 200) {
    rec.title = oa.body.display_name;
    rec.year = oa.body.publication_year;
    rec.venue = oa.body.primary_location?.source?.display_name ?? null;
    rec.type = oa.body.type;
    rec.cited = oa.body.cited_by_count;
    rec.abstract = invert(oa.body.abstract_inverted_index);
    rec.oa_id = oa.body.id;
    rec.concepts = (oa.body.concepts ?? []).slice(0, 5).map((c) => c.display_name);
  } else {
    rec.openalex_error = `${oa.status}`;
  }
  if (!rec.abstract) {
    const cr = await j(`https://api.crossref.org/works/${doi}`);
    if (cr.status === 200) {
      rec.crossref_abstract = cr.body.message?.abstract ?? null;
      rec.crossref_title = cr.body.message?.title?.[0] ?? null;
    } else {
      rec.crossref_error = `${cr.status}`;
    }
  }
  out.push(rec);
  process.stderr.write(`done ${doi}\n`);
}

import { writeFileSync } from "node:fs";
writeFileSync(new URL("./abstracts.json", import.meta.url), JSON.stringify(out, null, 2), "utf8");

// Human-readable dump too
import { appendFileSync, writeFileSync as wfs } from "node:fs";
const lines = [];
for (const r of out) {
  const a = r.abstract || (r.crossref_abstract || "").replace(/<[^>]+>/g, " ");
  lines.push("=".repeat(100));
  lines.push(`DOI: ${r.doi}`);
  lines.push(`TITLE: ${r.title || r.crossref_title || "(none)"}`);
  lines.push(`VENUE: ${r.venue} | YEAR: ${r.year} | TYPE: ${r.type} | CITED: ${r.cited}`);
  lines.push(`ABS: ${a || "(NO ABSTRACT oa=" + r.openalex_error + " cr=" + r.crossref_error + ")"}`);
}
wfs(new URL("./abstracts.txt", import.meta.url), lines.join("\n"), "utf8");
console.log("wrote abstracts.json and abstracts.txt");
