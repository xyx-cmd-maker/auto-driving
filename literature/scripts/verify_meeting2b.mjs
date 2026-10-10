// 第二次组会 19 篇候选：Crossref 题录核验（第二轮，仅补未命中项，长退避）
import fs from "node:fs";

const MAILTO = "research@example.org";
const OUT = "D:/Deepseek Harness/auto-driving/literature/meeting2/crossref_verify.jsonl";

const jac = (a, b) => {
  const tok = (s) => new Set(s.toLowerCase().replace(/[^a-z0-9 ]/g, " ").split(/\s+/).filter((x) => x.length > 2));
  const A = tok(a), B = tok(b);
  const inter = [...A].filter((x) => B.has(x)).length;
  const uni = new Set([...A, ...B]).size;
  return uni ? inter / uni : 0;
};

const existing = fs.readFileSync(OUT, "utf-8").split("\n").filter(Boolean).map((l) => JSON.parse(l));
const todo = existing.filter((r) => !r.ok);
console.log("RETRY n=" + todo.length);

const sleep = (ms) => new Promise((s) => setTimeout(s, ms));

for (const rec of todo) {
  const t = rec.query;
  const url = `https://api.crossref.org/works?query.bibliographic=${encodeURIComponent(t)}&rows=4&select=DOI,title,author,issued,container-title,volume,issue,page,type,is-referenced-by-count,publisher&mailto=${MAILTO}`;
  rec.error = null;
  for (let attempt = 0; attempt < 6; attempt++) {
    try {
      const r = await fetch(url, { headers: { "User-Agent": `dsh-meeting2-verify/1.0 (mailto:${MAILTO})` } });
      if (r.status === 429) throw new Error("HTTP 429");
      if (!r.ok) throw new Error("HTTP " + r.status);
      const j = await r.json();
      const items = j.message.items || [];
      rec.candidates = items.map((it) => ({
        j: +jac(t, (it.title && it.title[0]) || "").toFixed(3),
        doi: it.DOI,
        title: (it.title && it.title[0]) || "",
        container: (it["container-title"] && it["container-title"][0]) || "",
        year: it.issued && it.issued["date-parts"] && it.issued["date-parts"][0] ? it.issued["date-parts"][0][0] : null,
        vol: it.volume || null, issue: it.issue || null, page: it.page || null,
        type: it.type, cited: it["is-referenced-by-count"],
        firstAuthor: it.author && it.author[0] ? [it.author[0].given, it.author[0].family].filter(Boolean).join(" ") : null,
        nAuthors: it.author ? it.author.length : null,
      }));
      rec.candidates.sort((a, b) => b.j - a.j);
      rec.best = rec.candidates[0] || null;
      rec.ok = !!(rec.best && rec.best.j >= 0.85);
      break;
    } catch (e) {
      rec.error = String(e.message || e);
      await sleep(5000 + attempt * 3000);
    }
  }
  console.log(`${rec.ok ? "OK  " : "FAIL"} J=${rec.best ? rec.best.j : "-"}  ${rec.best ? rec.best.doi + " | " + rec.best.container + " " + (rec.best.vol || "") + "(" + (rec.best.issue || "") + ") " + (rec.best.year || "") + ":" + (rec.best.page || "") + " cited=" + rec.best.cited : rec.error}`);
  console.log(`      Q: ${t}`);
  if (rec.best) console.log(`      A: ${rec.best.title} [${rec.best.firstAuthor} et al., n=${rec.best.nAuthors}]`);
  await sleep(4000);
}

fs.writeFileSync(OUT, existing.map((r) => JSON.stringify(r)).join("\n"), "utf-8");
console.log("\nUPDATED " + OUT + "  matched=" + existing.filter((r) => r.ok).length + "/" + existing.length);
