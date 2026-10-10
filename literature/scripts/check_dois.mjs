// check_dois.mjs — verify a curated DOI list against Crossref (existence + full metadata).
// Input: dois.json  [{ "n": 1, "key": "...", "doi": "10.xxxx/yyy", "claim": { title, year, venue } }]
// Output: dois_checked.json + console table.
import fs from 'node:fs';
const inPath = process.argv[2];
const arg = (k, d) => (process.argv.includes(k) ? process.argv[process.argv.indexOf(k) + 1] : d);
const OUT = arg('--out', 'dois_checked.json');
const items = JSON.parse(fs.readFileSync(inPath, 'utf8'));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const STOP = new Set(['a', 'an', 'the', 'of', 'for', 'and', 'in', 'on', 'to', 'with', 'via', 'using', 'from', 'by', 'at', 'is', 'are', 'as', 'into', 'its', 'their', 'based']);
const toks = (s) => new Set((s || '').toLowerCase().replace(/[^a-z0-9\s-]/g, ' ').split(/\s+/).filter((w) => w.length > 1 && !STOP.has(w)));
const jac = (a, b) => { const A = toks(a), B = toks(b); if (!A.size || !B.size) return 0; let i = 0; for (const x of A) if (B.has(x)) i++; return i / (A.size + B.size - i); };
const sur = (n) => (n || '').trim().split(/\s+/).pop().toLowerCase();

async function get(url, tries = 5) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url, { headers: { 'User-Agent': 'dsh-citation-verify/1.0 (mailto:research@example.org)' } });
      if (r.status === 429 || r.status >= 500) { await sleep(2200 * (i + 1)); continue; }
      if (r.status === 404) return { status: 404 };
      if (!r.ok) return { error: `HTTP ${r.status}` };
      return { json: await r.json() };
    } catch (e) { if (i === tries - 1) return { error: e.message }; await sleep(1800 * (i + 1)); }
  }
  return { error: 'retries exhausted' };
}

const out = [];
for (const it of items) {
  const rec = { ...it, check: {} };
  const r = await get(`https://api.crossref.org/works/${encodeURIComponent(it.doi)}`);
  if (r.status === 404) {
    rec.check = { exists: false, reason: 'DOI not registered in Crossref' };
    console.log(`${String(it.n).padStart(3)} | FAIL-NOT-REGISTERED | ${it.doi}`);
  } else if (r.json && r.json.message) {
    const m = r.json.message;
    const title = (m.title && m.title[0]) || '';
    rec.check = {
      exists: true,
      title, year: (m.issued && m.issued['date-parts'] && m.issued['date-parts'][0] && m.issued['date-parts'][0][0]) || null,
      venue: (m['container-title'] && m['container-title'][0]) || null,
      short_venue: (m['short-container-title'] && m['short-container-title'][0]) || null,
      volume: m.volume || null, issue: m.issue || null, page: m.page || null,
      type: m.type, publisher: m.publisher || null,
      authors: (m.author || []).map((a) => [a.given, a.family].filter(Boolean).join(' ')),
      crossref_cited_by: m['is-referenced-by-count'] || 0,
      jaccard_vs_claim: it.claim && it.claim.title ? Number(jac(it.claim.title, title).toFixed(3)) : null,
      year_ok: it.claim && it.claim.year ? Math.abs((it.claim.year) - ((m.issued && m.issued['date-parts'] && m.issued['date-parts'][0] && m.issued['date-parts'][0][0]) || 0)) <= 1 : null,
    };
    const j = rec.check.jaccard_vs_claim;
    const v = j === null ? 'noc' : j >= 0.8 ? 'OK' : j >= 0.6 ? 'WEAK' : 'MISMATCH';
    rec.check.verdict = v;
    console.log(`${String(it.n).padStart(3)} | ${v.padEnd(14)} | jac=${String(j).padEnd(5)} | ${it.doi.padEnd(34)} | ${String(rec.check.year).padEnd(4)} | ${(rec.check.venue || '').slice(0, 44).padEnd(44)} | ${title.slice(0, 62)}`);
  } else {
    rec.check = { exists: null, error: r.error || 'unknown' };
    console.log(`${String(it.n).padStart(3)} | ERROR          | ${r.error} | ${it.doi}`);
  }
  out.push(rec);
  await sleep(400);
}
fs.writeFileSync(OUT, JSON.stringify(out, null, 2), 'utf8');
const bad = out.filter((o) => o.check.verdict === 'MISMATCH' || o.check.exists === false || o.check.exists === null);
console.error(`\nwrote ${OUT} (${out.length}); problems=${bad.length}`);
if (bad.length) console.error('problem keys: ' + bad.map((b) => `${b.n}:${b.key}`).join(', '));
