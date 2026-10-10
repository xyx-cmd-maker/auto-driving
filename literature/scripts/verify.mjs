// verify.mjs — layer-1/layer-2 citation verification.
// For each candidate: (a) Crossref bibliographic query -> DOI + metadata; (b) optional arXiv id_list existence check.
// Cross-source agreement (title token Jaccard) computed between the seed title and Crossref/arXiv titles.
// Usage: node verify.mjs seeds.json --out verify_out.json
import fs from 'node:fs';

const inPath = process.argv[2];
const arg = (k, d) => (process.argv.includes(k) ? process.argv[process.argv.indexOf(k) + 1] : d);
const OUT = arg('--out', 'verify_out.json');
const seeds = JSON.parse(fs.readFileSync(inPath, 'utf8'));

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const STOP = new Set(['a', 'an', 'the', 'of', 'for', 'and', 'in', 'on', 'to', 'with', 'via', 'using',
  'from', 'by', 'at', 'is', 'are', 'as', 'into', 'its', 'their', 'based']);
const toks = (s) => new Set(
  (s || '').toLowerCase().replace(/[^a-z0-9\s-]/g, ' ').split(/\s+/)
    .filter((w) => w.length > 1 && !STOP.has(w))
);
const jac = (a, b) => {
  const A = toks(a), B = toks(b);
  if (!A.size || !B.size) return 0;
  let inter = 0;
  for (const x of A) if (B.has(x)) inter++;
  return inter / (A.size + B.size - inter);
};

async function jget(url, tries = 4) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url, { headers: { 'User-Agent': 'dsh-citation-verify/1.0 (mailto:research@example.org)' } });
      if (r.status === 429 || r.status >= 500) { await sleep(1500 * (i + 1)); continue; }
      if (r.status === 404) return { status: 404 };
      if (!r.ok) return { error: `HTTP ${r.status}` };
      return { json: await r.json() };
    } catch (e) {
      if (i === tries - 1) return { error: e.message };
      await sleep(1000 * (i + 1));
    }
  }
  return { error: 'retries exhausted' };
}

const out = [];
for (const s of seeds) {
  const rec = { key: s.key, group: s.group || null, seed_title: s.title, seed_year: s.year || null, arxiv: s.arxiv || null };

  // --- arXiv existence check (if id given)
  if (s.arxiv) {
    const u = `https://export.arxiv.org/api/query?id_list=${encodeURIComponent(s.arxiv)}&max_results=1`;
    const r = await jget(u);
    if (r.json) {
      const entry = r.json.match(/<entry>([\s\S]*?)<\/entry>/);
      if (entry) {
        const t = (entry[1].match(/<title>([\s\S]*?)<\/title>/) || [])[1];
        const pub = (entry[1].match(/<published>([\s\S]*?)<\/published>/) || [])[1];
        rec.arxiv_title = t ? t.replace(/\s+/g, ' ').trim() : null;
        rec.arxiv_published = pub ? pub.slice(0, 10) : null;
        rec.arxiv_title_jaccard = jac(s.title, rec.arxiv_title);
      } else {
        rec.arxiv_error = 'no entry in feed';
      }
    } else rec.arxiv_error = r.error || `HTTP ${r.status}`;
    await sleep(3200); // arXiv: >=3s interval
  }

  // --- Crossref title query
  const q = encodeURIComponent(s.title);
  const crUrl = `https://api.crossref.org/works?query.bibliographic=${q}&rows=5&select=DOI,title,author,issued,container-title,type,volume,issue,page,is-referenced-by-count,publisher,short-container-title`;
  const cr = await jget(crUrl);
  if (cr.json && cr.json.message && cr.json.message.items) {
    const items = cr.json.message.items.map((it) => ({
      doi: it.DOI,
      title: (it.title && it.title[0]) || '',
      year: (it.issued && it.issued['date-parts'] && it.issued['date-parts'][0] && it.issued['date-parts'][0][0]) || null,
      venue: (it['container-title'] && it['container-title'][0]) || null,
      type: it.type,
      volume: it.volume || null,
      issue: it.issue || null,
      page: it.page || null,
      authors: (it.author || []).map((a) => [a.given, a.family].filter(Boolean).join(' ')).slice(0, 8),
      cited_by: it['is-referenced-by-count'] || 0,
      jaccard: jac(s.title, (it.title && it.title[0]) || ''),
    })).sort((a, b) => b.jaccard - a.jaccard);
    rec.crossref_top = items[0] || null;
    rec.crossref_alternatives = items.slice(1, 4).map((i) => ({ doi: i.doi, title: i.title, year: i.year, jaccard: Number(i.jaccard.toFixed(3)) }));
    rec.best_jaccard = items[0] ? Number(items[0].jaccard.toFixed(3)) : 0;
  } else {
    rec.crossref_error = cr.error || `HTTP ${cr.status}`;
  }
  out.push(rec);
  const v = rec.crossref_top;
  console.log(`${s.key} | jac=${rec.best_jaccard ?? 'NA'} | ${v ? v.doi : 'NO-DOI'} | ${v ? v.year : ''} | ${v ? (v.venue || '').slice(0, 40) : ''} | ${rec.arxiv ? `arxiv_jac=${rec.arxiv_title_jaccard?.toFixed?.(3)}` : ''}`);
  await sleep(700);
}

fs.writeFileSync(OUT, JSON.stringify(out, null, 2), 'utf8');
console.error(`\nwrote ${OUT} (${out.length} records)`);
