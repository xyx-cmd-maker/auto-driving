// Render venue-anchored candidates grouped by theme (for curation).
import fs from 'node:fs';
const IN = process.argv[2] || '../candidates_v2.jsonl';
const rows = fs.readFileSync(IN, 'utf8').trim().split('\n').filter(Boolean).map((l) => JSON.parse(l));
const byTheme = new Map();
for (const r of rows) {
  for (const t of r.theme_ids || ['?']) {
    if (!byTheme.has(t)) byTheme.set(t, []);
    byTheme.get(t).push(r);
  }
}
const keys = [...byTheme.keys()].sort();
for (const k of keys) {
  const list = byTheme.get(k).sort((a, b) => (b.cited_by || 0) - (a.cited_by || 0));
  console.log(`\n=== ${k} (n=${list.length}) ===`);
  for (const r of list) {
    console.log(`  ${String(r.cited_by).padStart(5)} | ${r.year} | ${(r.venue || 'NA').slice(0, 44).padEnd(44)} | ${r.doi || r.openalex_id} | ${r.title.slice(0, 100)}`);
  }
}
