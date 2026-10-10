// rank_candidates.mjs — rank Crossref gap-search candidates for manual triage.
import fs from 'node:fs';
const files = process.argv.slice(2);
const rows = [];
for (const f of files) {
  if (!fs.existsSync(f)) continue;
  for (const l of fs.readFileSync(f, 'utf8').trim().split('\n').filter(Boolean)) rows.push(JSON.parse(l));
}
const seen = new Set();
const uniq = rows.filter((r) => (seen.has(r.doi) ? false : (seen.add(r.doi), true)));
// Journal-quality filter: keep records whose venue looks like a journal/transactions/letters,
// drop book chapters, conference proceedings and megajournals that add noise here.
const VENUE_OK = /transactions|journal|letters|review|automatica|nature|science|robot|vehicular|computing|systems|neurocomputing|access|magazine|intelligence|survey|tutorials/i;
const VENUE_BAD = /proceedings|conference|congress|symposium|workshop|lecture notes|book|encyclopedia|e3s|iop conf/i;
const scored = uniq.map((r) => {
  let s = 0;
  if (r.venue && VENUE_OK.test(r.venue)) s += 2;
  if (r.venue && VENUE_BAD.test(r.venue)) s -= 3;
  if ((r.cited_by || 0) >= 100) s += 2;
  else if ((r.cited_by || 0) >= 30) s += 1;
  if ((r.title || '').length > 15) s += 1;
  return { ...r, score: s };
}).sort((a, b) => b.score - a.score || (b.cited_by || 0) - (a.cited_by || 0));

const top = scored.filter((r) => r.score >= 1);
console.log(`unique=${uniq.length} kept_for_triage=${top.length}\n`);
for (const r of top.slice(0, 60)) {
  console.log([String(r.cited_by).padStart(5), String(r.year || ''), (r.venue || 'NA').slice(0, 40).padEnd(40), r.doi, r.title.slice(0, 96)].join(' | '));
}
fs.writeFileSync('gap_candidates_ranked.jsonl', top.map((r) => JSON.stringify(r)).join('\n') + '\n', 'utf8');
