// bibtex.mjs — generate BibTeX from the verified final list.
import fs from 'node:fs';
const rows = JSON.parse(fs.readFileSync('final_list.json', 'utf8'));
const cur = { type: null, venue: null };
const out = [];

const surname = (full) => {
  const parts = (full || '').trim().split(/\s+/);
  if (parts.length === 1) return parts[0];
  return parts[parts.length - 1];
};
const bibAuthor = (full) => {
  const parts = (full || '').trim().split(/\s+/);
  if (parts.length === 1) return parts[0];
  const last = parts[parts.length - 1];
  const first = parts.slice(0, -1).join(' ');
  return `${last}, ${first}`;
};
const keyOf = (r) => `${surname(r.authors[0] || 'anon').toLowerCase().replace(/[^a-z]/g, '')}${r.year_crossref}${(r.key || '').replace(/[^a-z0-9]/gi, '').slice(0, 8)}`;

for (const r of rows) {
  const conf = /Conference|Symposium|Proceedings|Lecture Notes in Computer Science/i.test(r.venue || '');
  const type = conf ? 'inproceedings' : 'article';
  const authors = r.authors.map(bibAuthor).join(' and ');
  const lines = [`@${type}{${keyOf(r)},`, `  author    = {${authors}},`, `  title     = {{${r.crossref_title}}},`];
  if (conf) lines.push(`  booktitle = {${r.venue}},`);
  else lines.push(`  journal   = {${r.venue}},`);
  lines.push(`  year      = {${r.year_crossref}},`);
  if (r.volume) lines.push(`  volume    = {${r.volume}},`);
  if (r.issue) lines.push(`  number    = {${r.issue}},`);
  if (r.page) lines.push(`  pages     = {${String(r.page).replace('-', '--')}},`);
  if (r.publisher) lines.push(`  publisher = {${r.publisher}},`);
  if (r.doi && !r.doi.startsWith('10.48550/')) lines.push(`  doi       = {${r.doi}},`, `  url       = {https://doi.org/${r.doi}},`);
  else if (r.doi) lines.push(`  eprint    = {${r.doi.replace('10.48550/arXiv.', '')}},`, `  archivePrefix = {arXiv},`, `  url       = {https://arxiv.org/abs/${r.doi.replace('10.48550/arXiv.', '')}},`);
  lines.push(`  note      = {verified via Crossref ${r.verdict}; project P1-OTF-CfC},`, `}`);
  out.push(lines.join('\n'));
}
fs.writeFileSync('refs.bib', out.join('\n\n') + '\n', 'utf8');
console.log(`entries=${out.length}`);
