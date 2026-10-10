// final_table.mjs — merge curated numbers with verified Crossref metadata.
import fs from 'node:fs';
const A = JSON.parse(fs.readFileSync('dois_checked.json', 'utf8'));
const B = JSON.parse(fs.readFileSync('dois_appendix_checked.json', 'utf8'));
const rows = [...A, ...B].filter((r) => r.check && r.check.exists);
rows.sort((a, b) => a.n - b.n);
for (const r of rows) {
  const c = r.check;
  console.log([
    String(r.n).padStart(3), c.verdict.padEnd(5),
    String(c.year).padEnd(4), (c.volume ? `v${c.volume}` : 'v-').padEnd(7), (c.issue ? `n${c.issue}` : 'n-').padEnd(6),
    (c.page || '-').padEnd(14), (c.venue || '').slice(0, 40).padEnd(40),
    (c.authors[0] || '?').padEnd(18), '|', c.title.slice(0, 70),
  ].join(' '));
}
console.error(`rows=${rows.length}`);
