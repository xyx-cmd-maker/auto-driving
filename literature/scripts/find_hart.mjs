// find_hart.mjs — 找 Hart/Okhrin/Treiber 的 TR-C 2024 跟驰 DRL 论文的可获取版本
const UA = "dsh/1.0";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const pick = (s, t) => { const o = s.indexOf("<" + t); if (o < 0) return null; const g = s.indexOf(">", o); const c = s.indexOf("</" + t + ">", g); return c < 0 ? null : s.slice(g + 1, c).replace(/\s+/g, " ").trim(); };

const Q = [
  ['all:"car-following" AND all:"reinforcement learning" AND au:Treiber', "Treiber + CF + RL"],
  ['ti:"robust car-following"', "题名精确"],
  ['all:"deep reinforcement learning" AND all:"car-following" AND all:"string stability"', "CF+RL+弦稳定"],
];
for (const [q, tag] of Q) {
  const url = `https://export.arxiv.org/api/query?search_query=${encodeURIComponent(q)}&start=0&max_results=12&sortBy=relevance`;
  const t = await (await fetch(url, { headers: { "User-Agent": UA } })).text();
  console.log(`\n### ${tag}  total=${pick(t, "opensearch:totalResults")}`);
  let p = 0;
  while ((p = t.indexOf("<entry>", p)) >= 0) {
    const e = t.slice(p, t.indexOf("</entry>", p));
    const id = (pick(e, "id") || "").replace(/https?:\/\/arxiv\.org\/abs\//, "");
    const pub = (pick(e, "published") || "").slice(0, 10);
    console.log(`   ${id} | ${pub} | jr:${pick(e, "arxiv:journal_ref") || "-"} | doi:${pick(e, "arxiv:doi") || "-"}`);
    console.log(`      ${(pick(e, "title") || "").slice(0, 120)}`);
    p += 8;
  }
  await sleep(3600);
}
// 另试 MDPI Robotics 的 HTML 全文
console.log("\n=== 试 MDPI Robotics 2024 全文（HTML） ===");
try {
  const r = await fetch("https://www.mdpi.com/2218-6581/13/9/126", { headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0" } });
  const h = await r.text();
  console.log("HTTP", r.status, "bytes", h.length, "| title:", (h.match(/<title[^>]*>([^<]{0,120})/i) || [, ""])[1].trim());
  if (h.length > 50000) { (await import("node:fs")).writeFileSync("D:/Deepseek Harness/auto-driving/literature/fulltext/_raw/robotics2024-cfc-smc.html", h, "utf8"); console.log("saved HTML"); }
} catch (e) { console.log("ERR", e.message); }
