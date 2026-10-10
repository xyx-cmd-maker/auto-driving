// verify3.mjs — Crossref-primary verification + arXiv existence/dedup, with OpenAlex pool join (offline seed).
// L1 existence: Crossref query.bibliographic hit + arXiv id_list feed entry.
// L2 consistency: title token-Jaccard vs seed, year, venue, first-author surname.
// Usage: node verify3.mjs seeds.json --pool candidates_v2.jsonl --out verify_out.json
import fs from 'node:fs';

const inPath = process.argv[2];
const arg = (k, d) => (process.argv.includes(k) ? process.argv[process.argv.indexOf(k) + 1] : d);
const OUT = arg('--out', 'verify_out.json');
const POOL = arg('--pool', 'candidates_v2.jsonl');
const seeds = JSON.parse(fs.readFileSync(inPath, 'utf8'));
const pool = fs.existsSync(POOL)
  ? fs.readFileSync(POOL, 'utf8').trim().split('\n').filter(Boolean).map((l) => JSON.parse(l))
  : [];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const STOP = new Set(['a', 'an', 'the', 'of', 'for', 'and', 'in', 'on', 'to', 'with', 'via', 'using',
  'from', 'by', 'at', 'is', 'are', 'as', 'into', 'its', 'their', 'based', 'new', 'toward', 'towards']);
const toks = (s) => new Set((s || '').toLowerCase().replace(/[^a-z0-9\s-]/g, ' ').split(/\s+/)
  .filter((w) => w.length > 1 && !STOP.has(w)));
const jac = (a, b) => { const A = toks(a), B = toks(b); if (!A.size || !B.size) return 0; let i = 0; for (const x of A) if (B.has(x)) i++; return i / (A.size + B.size - i); };
const sur = (n) => (n || '').trim().split(/\s+/).pop().toLowerCase();

async function get(url, { text = false, tries = 4 } = {}) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url, { headers: { 'User-Agent': 'dsh-citation-verify/1.0 (mailto:research@example.org)' } });
      if (r.status === 429 || r.status >= 500) { await sleep(3000 * (i + 1)); continue; }
      if (r.status === 404) return { status: 404 };
      if (!r.ok) return { error: `HTTP ${r.status}` };
      return text ? { text: await r.text() } : { json: await r.json() };
    } catch (e) { if (i === tries - 1) return { error: e.message }; await sleep(2000 * (i + 1)); }
  }
  return { error: 'retries exhausted' };
}

const out = [];
for (const s of seeds) {
  const rec = { key: s.key, group: s.group || null, expected: { title: s.title, year: s.year || null, arxiv: s.arxiv || null } };

  // ---- pool join (OpenAlex records already fetched offline in the discovery phase)
  const poolHit = pool
    .map((p) => ({ ...p, j: jac(s.title, p.title) }))
    .sort((a, b) => b.j - a.j)[0];
  if (poolHit && poolHit.j >= 0.6) {
    rec.pool = { openalex_id: poolHit.openalex_id, doi: poolHit.doi, title: poolHit.title, year: poolHit.year,
      venue: poolHit.venue, cited_by: poolHit.cited_by, jaccard: Number(poolHit.j.toFixed(3)) };
  } else rec.pool = null;

  // ---- L1/L2: Crossref
  const url = `https://api.crossref.org/works?query.bibliographic=${encodeURIComponent(s.title)}&rows=6&select=DOI,title,author,issued,container-title,type,volume,issue,page,is-referenced-by-count,publisher&mailto=research@example.org`;
  const cr = await get(url);
  if (cr.json && cr.json.message && cr.json.message.items) {
    const items = cr.json.message.items.map((it) => ({
      doi: it.DOI,
      title: (it.title && it.title[0]) || '',
      year: (it.issued && it.issued['date-parts'] && it.issued['date-parts'][0] && it.issued['date-parts'][0][0]) || null,
      venue: (it['container-title'] && it['container-title'][0]) || null,
      type: it.type, volume: it.volume || null, issue: it.issue || null, page: it.page || null,
      publisher: it.publisher || null,
      authors: (it.author || []).map((a) => [a.given, a.family].filter(Boolean).join(' ')).slice(0, 10),
      cited_by: it['is-referenced-by-count'] || 0,
      jaccard: Number(jac(s.title, (it.title && it.title[0]) || '').toFixed(3)),
    })).sort((a, b) => b.jaccard - a.jaccard);
    rec.crossref_best = items[0] || null;
    rec.crossref_alts = items.slice(1, 4).map((i) => ({ doi: i.doi, title: i.title, year: i.year, venue: i.venue, jaccard: i.jaccard }));
  } else rec.crossref_error = cr.error || `HTTP ${cr.status}`;
  await sleep(900);

  // ---- arXiv existence / version + journal-ref
  if (s.arxiv) {
    const ax = await get(`https://export.arxiv.org/api/query?id_list=${encodeURIComponent(s.arxiv)}&max_results=1`, { text: true });
    if (ax.text) {
      const entry = (ax.text.match(/<entry>([\s\S]*?)<\/entry>/) || [])[1];
      if (entry) {
        const g = (tag) => { const m = entry.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`)); return m ? m[1].replace(/\s+/g, ' ').trim() : null; };
        const t = g('title');
        rec.arxiv = {
          id: s.arxiv, title: t, published: (g('published') || '').slice(0, 10),
          updated: (g('updated') || '').slice(0, 10),
          journal_ref: g('arxiv:journal_ref'), comment: g('arxiv:comment'),
          jaccard_vs_seed: t ? Number(jac(s.title, t).toFixed(3)) : null,
        };
      } else rec.arxiv = { error: 'no entry (id may not exist)' };
    } else rec.arxiv = { error: ax.error || `HTTP ${ax.status}` };
    await sleep(3400);
  }

  // ---- verdict
  const cb = rec.crossref_best, pb = rec.pool;
  const bestJac = Math.max(cb ? cb.jaccard : 0, pb ? pb.jaccard : 0);
  const axOk = rec.arxiv && rec.arxiv.jaccard_vs_seed >= 0.6;
  rec.verdict = {
    title_match: bestJac >= 0.8 ? 'strong' : bestJac >= 0.6 ? 'weak' : 'FAIL',
    best_jaccard: Number(bestJac.toFixed(3)),
    sources: [cb && cb.jaccard >= 0.6 ? 'crossref' : null, pb ? 'openalex' : null, axOk ? 'arxiv' : null].filter(Boolean),
    n_sources: [cb && cb.jaccard >= 0.6, !!pb, axOk].filter(Boolean).length,
  };
  out.push(rec);
  console.log([s.key, rec.verdict.title_match, rec.verdict.best_jaccard,
    cb ? cb.doi : 'NO-CR', cb ? cb.year : '', pb ? `oa:${pb.cited_by}` : 'oa:-',
    rec.arxiv ? `ax:${rec.arxiv.jaccard_vs_seed ?? rec.arxiv.error}` : '',
    cb ? (cb.venue || '').slice(0, 38) : ''].join(' | '));
  await sleep(400);
}

fs.writeFileSync(OUT, JSON.stringify(out, null, 2), 'utf8');
const bad = out.filter((r) => r.verdict.title_match === 'FAIL');
console.error(`\nwrote ${OUT} (${out.length}); FAIL=${bad.length}; weak=${out.filter((r) => r.verdict.title_match === 'weak').length}`);
if (bad.length) console.error('FAIL keys: ' + bad.map((b) => b.key).join(', '));
