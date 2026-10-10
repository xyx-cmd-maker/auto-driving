// fix_table.mjs — rewrite citation counts in the deliverable markdown from the authoritative JSON.
import fs from 'node:fs';
const MD = '文献需求-50篇顶刊.md';
const rows = JSON.parse(fs.readFileSync('final_list.json', 'utf8'));
const cite = new Map(rows.map((r) => [r.n, r.crossref_cited_by]));
let md = fs.readFileSync(MD, 'utf8');
const lines = md.split('\n');
let fixed = 0;
const out = lines.map((ln) => {
  const m = ln.match(/^\| (\d+) \| /);
  if (!m) return ln;
  const n = Number(m[1]);
  if (!cite.has(n)) return ln;
  const want = cite.get(n);
  const cells = ln.split('|');
  // table row: ['', ' # ', ' title ', ' authors ', ' venue ', ' year ', ' vol ', ' link ', ' cited ', ' why ', '']
  if (cells.length < 10) return ln;
  const idx = 8; // citation count cell
  const cur = cells[idx].trim();
  if (cur === String(want)) return ln;
  cells[idx] = ` ${want === null ? '—' : want} `;
  fixed++;
  return cells.join('|');
});
fs.writeFileSync(MD, out.join('\n'), 'utf8');
console.log(`rows_corrected=${fixed}`);
