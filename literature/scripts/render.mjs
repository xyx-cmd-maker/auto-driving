// Render candidates_raw.jsonl into a compact human-readable table for curation.
import fs from 'node:fs';
const IN = process.argv[2] || '../candidates_raw.jsonl';
const MIN_CITES = Number(process.argv[3] || 0);
const rows = fs.readFileSync(IN, 'utf8').trim().split('\n').map((l) => JSON.parse(l))
  .filter((r) => (r.cited_by || 0) >= MIN_CITES)
  .sort((a, b) => (b.cited_by || 0) - (a.cited_by || 0));
const out = rows.map((r) =>
  `${String(r.cited_by).padStart(6)} | ${r.year} | ${(r.venue || 'NA').slice(0, 52).padEnd(52)} | ${r.query_ids.join(',')} | ${r.doi || r.openalex_id} | ${r.title.slice(0, 110)}`
);
console.log(out.join('\n'));
console.error(`rows=${rows.length}`);
