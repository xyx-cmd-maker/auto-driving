// Best-of-cluster: show top-cited candidates per venue from the venue-anchored pool.
import fs from 'node:fs';
const IN = process.argv[2] || 'candidates_v2.jsonl';
const MIN = Number(process.argv[3] || 40);
const PER_VENUE = Number(process.argv[4] || 12);
const rows = fs.readFileSync(IN, 'utf8').trim().split('\n').filter(Boolean).map((l) => JSON.parse(l))
  .filter((r) => (r.cited_by || 0) >= MIN);
const byVenue = new Map();
for (const r of rows) {
  const v = r.venue || 'NA';
  if (!byVenue.has(v)) byVenue.set(v, []);
  byVenue.get(v).push(r);
}
for (const [v, list] of [...byVenue.entries()].sort((a, b) => b[1].length - a[1].length)) {
  console.log(`\n=== ${v} (n>=${MIN}: ${list.length}) ===`);
  for (const r of list.sort((a, b) => b.cited_by - a.cited_by).slice(0, PER_VENUE)) {
    console.log(`  ${String(r.cited_by).padStart(5)} | ${r.year} | ${(r.theme_ids || []).join(',')} | ${r.doi} | ${r.title.slice(0, 108)}`);
  }
}
