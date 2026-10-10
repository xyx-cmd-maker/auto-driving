// ax_abs.mjs — 拉取 LNN 桶关键 arXiv 论文的摘要（用于分诊初判）
import fs from "node:fs";
const DIR = "D:/Deepseek Harness/auto-driving/literature/fresh2024";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const IDS = [
  "2601.06227", "2510.07578", "2603.27058", "2606.15807", "2407.20590",
  "2609.00385", "2604.01790", "2403.19637", "2401.01425",
  "2606.20648", "2609.33892", "2502.16466", "2506.16311", "2606.29677",
];
const pick = (s, t) => { const o = s.indexOf("<" + t); if (o < 0) return null; const g = s.indexOf(">", o); const c = s.indexOf("</" + t + ">", g); return c < 0 ? null : s.slice(g + 1, c).replace(/\s+/g, " ").trim(); };
const out = [];
for (let i = 0; i < IDS.length; i += 5) {
  const batch = IDS.slice(i, i + 5);
  const url = `https://export.arxiv.org/api/query?id_list=${batch.join(",")}&max_results=10`;
  const txt = await (await fetch(url, { headers: { "User-Agent": "dsh/1.0" } })).text();
  let p = 0;
  while ((p = txt.indexOf("<entry>", p)) >= 0) {
    const e = txt.slice(p, txt.indexOf("</entry>", p));
    const rec = {
      arxiv: (pick(e, "id") || "").replace(/https?:\/\/arxiv\.org\/abs\//, ""),
      title: pick(e, "title"), published: (pick(e, "published") || "").slice(0, 10),
      updated: (pick(e, "updated") || "").slice(0, 10),
      journal_ref: pick(e, "arxiv:journal_ref"), doi: pick(e, "arxiv:doi"),
      comment: (pick(e, "arxiv:comment") || "").slice(0, 150),
      authors: [...e.matchAll(/<name>([^<]+)<\/name>/g)].map((m) => m[1]),
      abstract: pick(e, "summary"),
    };
    out.push(rec);
    p += 8;
  }
  await sleep(3600);
}
fs.writeFileSync(`${DIR}/ax_abs.json`, JSON.stringify(out, null, 2), "utf8");
for (const r of out) {
  console.log("=".repeat(100));
  console.log(`${r.arxiv} | ${r.published} | jr:${r.journal_ref || "-"} | doi:${r.doi || "-"}`);
  console.log(`T: ${r.title}`);
  console.log(`A: ${(r.authors || []).slice(0, 6).join("; ")}${(r.authors || []).length > 6 ? " et al." : ""}`);
  console.log(`C: ${r.comment || "-"}`);
  console.log(`X: ${(r.abstract || "").slice(0, 700)}`);
}
console.log(`\nWROTE ${DIR}/ax_abs.json n=${out.length}`);
