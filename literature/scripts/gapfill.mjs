// gapfill.mjs — Crossref lookup for a plain title list (one JSON array of {key,title,year,note}).
// Usage: node gapfill.mjs gap_titles.json --out gapfill_out.json
import fs from 'node:fs';
const inPath = process.argv[2];
const arg = (k, d) => (process.argv.includes(k) ? process.argv[process.argv.indexOf(k) + 1] : d);
const OUT = arg('--out', 'gapfill_out.json');
const items = JSON.parse(fs.readFileSync(inPath, 'utf8'));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const STOP = new Set(['a', 'an', 'the', 'of', 'for', 'and', 'in', 'on', 'to', 'with', 'via', 'using', 'from', 'by', 'at', 'is', 'are', 'as', 'into', 'its', 'their', 'based']);
const toks = (s) => new Set((s || '').toLowerCase().replace(/[^a-z0-9\s-]/g, ' ').split(/\s+/).filter((w) => w.length > 1 && !STOP.has(w)));
const jac = (a, b) => { const A = toks(a), B = toks(b); if (!A.size || !B.size) return 0; let i = 0; for (const x of A) if (B.has(x)) i++; return i / (A.size + B.size - i); };

async function get(url, tries = 4) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url, { headers: { 'User-Agent': 'dsh-citation-verify/1.0 (mailto:research@example.org)' } });
      if (r.status === 429 || r.status >= 500) { await sleep(3000 * (i + 1)); continue; }
      if (!r.ok) return { error: `HTTP ${r.status}` };
      return { json: await r.json() };
    } catch (e) { if (i === tries - 1) return { error: e.message }; await sleep(2000 * (i + 1)); }
  }
  return { error: 'retries exhausted' };
}

const out = [];
for (const it of items) {
  const url = `https://api.crossref.org/works?query.bibliographic=${encodeURIComponent(it.title)}&rows=5&select=DOI,title,author,issued,container-title,type,volume,issue,page,is-referenced-by-count,publisher&mailto=research@example.org`;
  const r = await get(url);
  let best = null, alts = [];
  if (r.json && r.json.message && r.json.message.items) {
    const rows = r.json.message.items.map((x) => ({
      doi: x.DOI, title: (x.title && x.title[0]) || '',
      year: (x.issued && x.issued['date-parts'] && x.issued['date-parts'][0] && x.issued['date-parts'][0][0]) || null,
      venue: (x['container-title'] && x['container-title'][0]) || null,
      type: x.type, volume: x.volume || null, issue: x.issue || null, page: x.page || null,
      publisher: x.publisher || null,
      authors: (x.author || []).map((a) => [a.given, a.family].filter(Boolean).join(' ')),
      cited_by: x['is-referenced-by-count'] || 0,
      jaccard: Number(jac(it.title, (x.title && x.title[0]) || '').toFixed(3)),
    })).sort((a, b) => b.jaccard - a.jaccard);
    best = rows[0] || null; alts = rows.slice(1, 3);
  }
  out.push({ key: it.key, note: it.note || null, query_title: it.title, best, alts, error: r.error || null });
  console.log(`${it.key} | jac=${best ? best.jaccard : 'NA'} | ${best ? best.doi : 'NONE'} | ${best ? best.year : ''} | ${best ? (best.venue || '').slice(0, 40) : ''} | ${best ? best.title.slice(0, 60) : ''}`);
  await sleep(900);
}
fs.writeFileSync(OUT, JSON.stringify(out, null, 2), 'utf8');
console.error(`wrote ${OUT} (${out.length})`);
