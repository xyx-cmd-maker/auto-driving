// verify_new.mjs — 核验 2024+ 新命中的题录（Crossref 权威字段）+ 记录 OA 状态
import fs from "node:fs";
const DIR = "D:/Deepseek Harness/auto-driving/literature/fresh2024";
const MAILTO = "research@example.org";
const UA = `dsh-p1-fresh/1.0 (mailto:${MAILTO})`;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const DOIS = [
  "10.1109/icssas66150.2025.11081318",
  "10.1016/j.isatra.2026.06.027",
  "10.3390/robotics13090126",
  "10.1007/978-3-032-20963-4_21",
  "10.1109/tits.2024.3398602",
  "10.1016/j.trf.2025.01.026",
  "10.1016/j.trc.2024.104578",
  "10.1007/s11063-024-11640-x",
  "10.1007/978-3-031-92741-6_24",
  "10.1016/j.chaos.2025.117116",
  "10.1038/s41467-025-62597-x",
  "10.1016/j.trc.2024.104486",
  "10.1109/tcst.2024.3505036",
  "10.1109/tcst.2024.3361393",
  "10.1109/tiv.2024.3373512",
  "10.1016/j.inffus.2025.103622",
  "10.1109/tac.2024.3401082",
];
const out = [];
console.log("=== Crossref 权威字段 ===");
for (const d of DOIS) {
  let rec = { doi: d };
  for (let k = 0; k < 5; k++) {
    try {
      const r = await fetch(`https://api.crossref.org/works/${d}`, { headers: { "User-Agent": UA } });
      if (r.status === 429) { await sleep(8000 * (k + 1)); continue; }
      if (r.status === 404) { rec.error = "404 not found in Crossref"; break; }
      if (!r.ok) throw new Error("HTTP " + r.status);
      const m = (await r.json()).message;
      rec = {
        doi: d,
        title: (m.title && m.title[0]) || "",
        container: (m["container-title"] && m["container-title"][0]) || "",
        short: (m["short-container-title"] && m["short-container-title"][0]) || "",
        type: m.type,
        year: m.issued && m.issued["date-parts"] && m.issued["date-parts"][0] ? m.issued["date-parts"][0][0] : null,
        vol: m.volume, issue: m.issue, page: m.page, article: m["article-number"],
        cited: m["is-referenced-by-count"],
        authors: (m.author || []).map((a) => [a.given, a.family].filter(Boolean).join(" ")),
        n_authors: (m.author || []).length,
        license: (m.license || []).map((l) => l.URL).join(" | ") || null,
        abstract: (m.abstract || "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim().slice(0, 900) || null,
        update_to: m["update-to"] || null,
        publisher: m.publisher,
      };
      break;
    } catch (e) { rec.error = e.message; await sleep(6000 * (k + 1)); }
  }
  out.push(rec);
  const ok = rec.title ? "OK " : "!! ";
  console.log(`${ok}${d}`);
  if (rec.title) {
    console.log(`     ${rec.year} | ${String(rec.container).slice(0, 56)} | ${String(rec.vol || "")}(${rec.issue || ""}):${rec.page || rec.article || ""} | cited=${rec.cited} | ${rec.type}`);
    console.log(`     ${rec.title.slice(0, 150)}`);
    if (rec.n_authors) console.log(`     作者: ${rec.authors.slice(0, 4).join("; ")}${rec.n_authors > 4 ? " et al. (n=" + rec.n_authors + ")" : ""}`);
    if (rec.update_to) console.log(`     ⚠ update-to: ${JSON.stringify(rec.update_to)}`);
    if (!rec.license) console.log(`     license: (none/closed)`);
  } else console.log(`     ERR ${rec.error}`);
  await sleep(1500);
}
fs.writeFileSync(`${DIR}/crossref_new.json`, JSON.stringify(out, null, 2), "utf8");
console.log(`\nWROTE ${DIR}/crossref_new.json  n=${out.length}  matched=${out.filter((r) => r.title).length}`);
