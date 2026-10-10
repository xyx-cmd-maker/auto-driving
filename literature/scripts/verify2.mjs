// verify2.mjs — cross-source citation verification (OpenAlex title-search -> DOI -> Crossref confirm; arXiv id check).
// Layers: L1 existence (OpenAlex work id + Crossref DOI resolve), L2 consistency (title jaccard, year, venue, authors).
// Usage: node verify2.mjs seeds.json --out verify_out.json
import fs from 'node:fs';

const inPath = process.argv[2];
const arg = (k, d) => (process.argv.includes(k) ? process.argv[process.argv.indexOf(k) + 1] : d);
const OUT = arg('--out', 'verify_out.json');
const seeds = JSON.parse(fs.readFileSync(inPath, 'utf8'));
const MAILTO = 'research@example.org';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const STOP = new Set(['a', 'an', 'the', 'of', 'for', 'and', 'in', 'on', 'to', 'with', 'via', 'using',
  'from', 'by', 'at', 'is', 'are', 'as', 'into', 'its', 'their', 'based', 'new', 'toward', 'towards']);
const toks = (s) => new Set((s || '').toLowerCase().replace(/[^a-z0-9\s-]/g, ' ').split(/\s+/)
  .filter((w) => w.length > 1 && !STOP.has(w)));
const jac = (a, b) => {
  const A = toks(a), B = toks(b);
  if (!A.size || !B.size) return 0;
  let inter = 0; for (const x of A) if (B.has(x)) inter++;
  return inter / (A.size + B.size - inter);
};

async function jget(url, tries = 4) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url, { headers: { 'User-Agent': 'dsh-citation-verify/1.0 (mailto:research@example.org)' } });
      if (r.status === 429 || r.status >= 500) { await sleep(2500 * (i + 1)); continue; }
      if (r.status === 404) return { status: 404 };
      if (!r.ok) return { error: `HTTP ${r.status}` };
      return { json: await r.json() };
    } catch (e) { if (i === tries - 1) return { error: e.message }; await sleep(1500 * (i + 1)); }
  }
  return { error: 'retries exhausted' };
}

const OA_SELECT = 'id,doi,display_name,publication_year,publication_date,type,cited_by_count,authorships,primary_location,language';

const results = [];
for (const s of seeds) {
  const rec = { key: s.key, group: s.group || null, expected: { title: s.title, year: s.year || null, arxiv: s.arxiv || null } };

  // ---- Step 1: OpenAlex title search (existence + metadata)
  const oaUrl = `https://api.openalex.org/works?filter=title.search:${encodeURIComponent(s.title)}&per-page=5&select=${OA_SELECT}&mailto=${MAILTO}`;
  const oa = await jget(oaUrl);
  if (oa.json && oa.json.results && oa.json.results.length) {
    const cands = oa.json.results.map((r) => ({
      openalex_id: (r.id || '').replace('https://openalex.org/', ''),
      doi: r.doi ? r.doi.replace('https://doi.org/', '').toLowerCase() : null,
      title: r.display_name, year: r.publication_year, date: r.publication_date,
      venue: (r.primary_location && r.primary_location.source && r.primary_location.source.display_name) || null,
      venue_type: (r.primary_location && r.primary_location.source && r.primary_location.source.type) || null,
      type: r.type, cited_by: r.cited_by_count,
      authors: (r.authorships || []).map((a) => (a.author && a.author.display_name) || ''),
      jaccard: Number(jac(s.title, r.display_name).toFixed(3)),
    })).sort((a, b) => b.jaccard - a.jaccard);
    rec.openalex_best = cands[0];
    rec.openalex_alts = cands.slice(1, 4);
  } else {
    rec.openalex_error = oa.error || 'no results';
  }
  await sleep(500);

  // ---- Step 2: Crossref cross-confirm of the matched DOI
  const doi = rec.openalex_best && rec.openalex_best.doi;
  if (doi) {
    const cr = await jget(`https://api.crossref.org/works/${encodeURIComponent(doi)}`);
    if (cr.json && cr.json.message) {
      const m = cr.json.message;
      rec.crossref = {
        doi: m.DOI,
        title: (m.title && m.title[0]) || '',
        year: (m.issued && m.issued['date-parts'] && m.issued['date-parts'][0] && m.issued['date-parts'][0][0]) || null,
        venue: (m['container-title'] && m['container-title'][0]) || null,
        volume: m.volume || null, issue: m.issue || null, page: m.page || null,
        type: m.type, publisher: m.publisher || null,
        authors: (m.author || []).map((a) => [a.given, a.family].filter(Boolean).join(' ')),
        cited_by: m['is-referenced-by-count'] || 0,
        jaccard_vs_seed: Number(jac(s.title, (m.title && m.title[0]) || '').toFixed(3)),
        jaccard_vs_openalex: Number(jac(rec.openalex_best.title, (m.title && m.title[0]) || '').toFixed(3)),
      };
      // author surname overlap between OpenAlex and Crossref
      const sur = (n) => (n || '').split(/\s+/).pop().toLowerCase();
      const oaSur = new Set((rec.openalex_best.authors || []).map(sur));
      const crSur = new Set((rec.crossref.authors || []).map(sur));
      let ov = 0; for (const x of oaSur) if (crSur.has(x)) ov++;
      rec.author_surname_overlap = oaSur.size ? Number((ov / oaSur.size).toFixed(2)) : null;
    } else if (cr.status === 404) {
      rec.crossref = { error: 'DOI not registered in Crossref' };
    } else {
      rec.crossref = { error: cr.error || `HTTP ${cr.status}` };
    }
    await sleep(500);
  }

  // ---- Step 3: arXiv existence check
  if (s.arxiv) {
    const ax = await jget(`https://export.arxiv.org/api/query?id_list=${encodeURIComponent(s.arxiv)}&max_results=1`);
    if (ax.json) {
      const entry = ax.json.match(/<entry>([\s\S]*?)<\/entry>/);
      if (entry) {
        const t = (entry[1].match(/<title>([\s\S]*?)<\/title>/) || [])[1];
        const pub = (entry[1].match(/<published>([\s\S]*?)<\/published>/) || [])[1];
        const upd = (entry[1].match(/<updated>([\s\S]*?)<\/updated>/) || [])[1];
        const jr = (entry[1].match(/<arxiv:journal_ref[^>]*>([\s\S]*?)<\/arxiv:journal_ref>/) || [])[1];
        const cm = (entry[1].match(/<arxiv:comment[^>]*>([\s\S]*?)<\/arxiv:comment>/) || [])[1];
        rec.arxiv = {
          id: s.arxiv,
          title: t ? t.replace(/\s+/g, ' ').trim() : null,
          published: pub ? pub.slice(0, 10) : null,
          updated: upd ? upd.slice(0, 10) : null,
          journal_ref: jr ? jr.replace(/\s+/g, ' ').trim() : null,
          comment: cm ? cm.replace(/\s+/g, ' ').trim() : null,
          jaccard_vs_seed: t ? Number(jac(s.title, t.replace(/\s+/g, ' ').trim()).toFixed(3)) : null,
        };
      } else rec.arxiv = { error: 'no entry returned (id may not exist)' };
    } else rec.arxiv = { error: ax.error || `HTTP ${ax.status}` };
    await sleep(3200);
  }

  const v = rec.openalex_best;
  console.log([s.key, `seed-jac=${v ? v.jaccard : 'NA'}`, v ? v.doi : 'NO-MATCH', v ? v.year : '',
    `cr-jac=${rec.crossref && rec.crossref.jaccard_vs_seed !== undefined ? rec.crossref.jaccard_vs_seed : 'NA'}`,
    rec.crossref && rec.crossref.error ? `CR:${rec.crossref.error}` : '',
    rec.arxiv && rec.arxiv.error ? `AX:${rec.arxiv.error}` : (rec.arxiv ? `AX-jac=${rec.arxiv.jaccard_vs_seed}` : ''),
    (v ? v.venue || '' : '').slice(0, 32)].join(' | '));
  results.push(rec);
  await sleep(400);
}

fs.writeFileSync(OUT, JSON.stringify(results, null, 2), 'utf8');
console.error(`\nwrote ${OUT} (${results.length})`);
