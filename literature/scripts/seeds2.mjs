// seeds2.mjs — Crossref-only discovery lookup for a title list, with cross-check against the OpenAlex pool.
// Usage: node seeds2.mjs seeds_v3.json gap_titles.json --pool candidates_v2.jsonl --out seeds_lookup.json
import fs from 'node:fs';
const A = process.argv[2], B = process.argv[3];
const arg = (k, d) => (process.argv.includes(k) ? process.argv[process.argv.indexOf(k) + 1] : d);
const OUT = arg('--out', 'seeds_lookup.json');
const POOL = arg('--pool', 'candidates_v2.jsonl');
const seeds = JSON.parse(fs.readFileSync(A, 'utf8'));
const gaps = B && fs.existsSync(B) ? JSON.parse(fs.readFileSync(B, 'utf8')) : [];
const pool = fs.existsSync(POOL) ? fs.readFileSync(POOL, 'utf8').trim().split('\n').filter(Boolean).map((l) => JSON.parse(l)) : [];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const STOP = new Set(['a', 'an', 'the', 'of', 'for', 'and', 'in', 'on', 'to', 'with', 'via', 'using', 'from', 'by', 'at', 'is', 'are', 'as', 'into', 'its', 'their', 'based', 'new']);
const toks = (s) => new Set((s || '').toLowerCase().replace(/[^a-z0-9\s-]/g, ' ').split(/\s+/).filter((w) => w.length > 1 && !STOP.has(w)));
const jac = (a, b) => { const A2 = toks(a), B2 = toks(b); if (!A2.size || !B2.size) return 0; let i = 0; for (const x of A2) if (B2.has(x)) i++; return i / (A2.size + B2.size - i); };

async function get(url, tries = 5) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url, { headers: { 'User-Agent': 'dsh-citation-verify/1.0 (mailto:research@example.org)' } });
      if (r.status === 429 || r.status >= 500) { await sleep(2500 * (i + 1)); continue; }
      if (r.status === 404) return { status: 404 };
      if (!r.ok) return { error: `HTTP ${r.status}` };
      return { json: await r.json() };
    } catch (e) { if (i === tries - 1) return { error: e.message }; await sleep(2000 * (i + 1)); }
  }
  return { error: 'retries exhausted' };
}

// unified title list: seeds (with group/arxiv) + gaps
const list = [
  ...seeds.map((s) => ({ key: s.key, group: s.group, title: s.title, arxiv: s.arxiv || null, kind: 'seed' })),
  ...gaps.filter((g) => !seeds.some((s) => s.key === g.key)).map((g) => ({ key: g.key, group: 'GAP', title: g.title, arxiv: null, kind: 'gap', note: g.note })),
];

const out = [];
for (const it of list) {
  const rec = { key: it.key, group: it.group, kind: it.kind, note: it.note || null, expected_title: it.title };

  // pool join (OpenAlex metadata captured earlier, pre-budget-exhaustion)
  const best = pool.map((p) => ({ p, j: jac(it.title, p.title) })).sort((a, b) => b.j - a.j)[0];
  if (best && best.j >= 0.7) {
    rec.openalex = { id: best.p.openalex_id, doi: best.p.doi, title: best.p.title, year: best.p.year, venue: best.p.venue,
      cited_by: best.p.cited_by, jaccard: Number(best.j.toFixed(3)) };
  } else rec.openalex = null;

  // Crossref
  const u = `https://api.crossref.org/works?query.bibliographic=${encodeURIComponent(it.title)}&rows=5&select=DOI,title,author,issued,container-title,type,volume,issue,page,is-referenced-by-count,publisher&mailto=research@example.org`;
  const r = await get(u);
  if (r.json && r.json.message && r.json.message.items) {
    const rows = r.json.message.items.map((x) => ({
      doi: x.DOI, title: (x.title && x.title[0]) || '',
      year: (x.issued && x.issued['date-parts'] && x.issued['date-parts'][0] && x.issued['date-parts'][0][0]) || null,
      venue: (x['container-title'] && x['container-title'][0]) || null, type: x.type,
      volume: x.volume || null, issue: x.issue || null, page: x.page || null, publisher: x.publisher || null,
      authors: (x.author || []).map((a) => [a.given, a.family].filter(Boolean).join(' ')),
      cited_by: x['is-referenced-by-count'] || 0,
      jaccard: Number(jac(it.title, (x.title && x.title[0]) || '').toFixed(3)),
    })).sort((a, b) => b.jaccard - a.jaccard);
    rec.crossref_best = rows[0] || null;
    rec.crossref_alts = rows.slice(1, 4).map((z) => ({ doi: z.doi, title: z.title, year: z.year, venue: z.venue, jaccard: z.jaccard }));
  } else rec.crossref_error = r.error || `HTTP ${r.status}`;
  await sleep(800);

  // arXiv (only when an id is supplied)
  if (it.arxiv) {
    const ax = await get(`https://export.arxiv.org/api/query?id_list=${encodeURIComponent(it.arxiv)}&max_results=1`);
    if (ax.json !== undefined) {
      const txt = await (await fetch(`https://export.arxiv.org/api/query?id_list=${it.arxiv}&max_results=1`)).text();
      const entry = (txt.match(/<entry>([\s\S]*?)<\/entry>/) || [])[1];
      if (entry) {
        const g = (tag) => { const m = entry.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`)); return m ? m[1].replace(/\s+/g, ' ').trim() : null; };
        rec.arxiv = { id: it.arxiv, title: g('title'), published: (g('published') || '').slice(0, 10), journal_ref: g('arxiv:journal_ref'), comment: g('arxiv:comment'), jaccard: g('title') ? Number(jac(it.title, g('title')).toFixed(3)) : null };
      } else rec.arxiv = { error: 'no entry' };
    }
    await sleep(3300);
  }

  const cb = rec.crossref_best;
  rec.verdict = {
    best_jaccard: Math.max(cb ? cb.jaccard : 0, rec.openalex ? rec.openalex.jaccard : 0),
    sources: [cb && cb.jaccard >= 0.6 ? 'crossref' : null, rec.openalex ? 'openalex' : null, rec.arxiv && rec.arxiv.jaccard >= 0.6 ? 'arxiv' : null].filter(Boolean),
  };
  rec.verdict.n_sources = rec.verdict.sources.length;
  rec.verdict.title_match = rec.verdict.best_jaccard >= 0.8 ? 'strong' : rec.verdict.best_jaccard >= 0.6 ? 'weak' : 'FAIL';
  out.push(rec);
  console.log([it.key.padEnd(22), rec.verdict.title_match.padEnd(6), String(rec.verdict.best_jaccard).padEnd(5),
    (cb ? cb.doi : 'NO-CR').padEnd(36), String(cb ? cb.year : '').padEnd(5),
    rec.openalex ? `oa:${rec.openalex.cited_by}` : 'oa:-',
    ((cb ? cb.venue : (rec.openalex ? rec.openalex.venue : '')) || '').slice(0, 40)].join(' | '));
  await sleep(300);
}
fs.writeFileSync(OUT, JSON.stringify(out, null, 2), 'utf8');
console.error(`\nwrote ${OUT} (${out.length}); FAIL=${out.filter((o) => o.verdict.title_match === 'FAIL').length}`);
