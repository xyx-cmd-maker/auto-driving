// summarize.mjs — turn verify_out.json into a compact review table + flag rows needing manual work.
import fs from 'node:fs';
const IN = process.argv[2] || 'verify_out.json';
const rows = JSON.parse(fs.readFileSync(IN, 'utf8'));
const need = [];
console.log('key | match | jac | crJ | axJ | doi | year | venue | title(crossref)');
for (const r of rows) {
  const cb = r.crossref_best;
  const crJ = cb ? cb.jaccard : 0;
  const axJ = r.arxiv && typeof r.arxiv.jaccard_vs_seed === 'number' ? r.arxiv.jaccard_vs_seed : null;
  const flag = (r.verdict.title_match !== 'strong') || (r.verdict.n_sources < 2 && !r.expected.arxiv);
  if (flag) need.push(r.key);
  console.log([
    r.key.padEnd(22), r.verdict.title_match.padEnd(6), String(r.verdict.best_jaccard).padEnd(5),
    String(crJ).padEnd(5), axJ === null ? '-' : String(axJ).padEnd(5),
    (cb ? cb.doi : (r.pool ? r.pool.doi : 'NONE')).padEnd(38),
    (cb ? cb.year : (r.pool ? r.pool.year : '')).toString().padEnd(5),
    ((cb ? cb.venue : (r.pool ? r.pool.venue : '')) || '').slice(0, 42).padEnd(42),
    cb ? cb.title.slice(0, 70) : (r.pool ? r.pool.title.slice(0, 70) : ''),
  ].join(' | '));
}
console.error(`\ntotal=${rows.length} need_manual=${need.length}\n${need.join(', ')}`);
