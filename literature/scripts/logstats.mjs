// logstats.mjs — summarize per-channel hit/export counts for the search log.
import fs from 'node:fs';
const files = process.argv.slice(2);
let grandHits = 0, grandExp = 0, n = 0;
for (const f of files) {
  if (!fs.existsSync(f)) { console.log(`(missing) ${f}`); continue; }
  const log = JSON.parse(fs.readFileSync(f, 'utf8'));
  const ok = log.filter((l) => l.status === '200');
  const fail = log.filter((l) => l.status !== '200');
  const h = ok.reduce((s, l) => s + (l.hits || 0), 0);
  const e = ok.reduce((s, l) => s + (l.exported || 0), 0);
  grandHits += h; grandExp += e; n += ok.length;
  console.log(`${f}: queries_ok=${ok.length} queries_failed=${fail.length} sum_hits=${h} sum_exported=${e}`);
  if (fail.length) console.log(`   failed: ${fail.map((x) => `${x.theme}/${x.cluster || '-'}:${x.status.slice(0, 28)}`).join(' | ')}`);
}
console.log(`TOTAL ok_queries=${n} sum_hits=${grandHits} sum_exported=${grandExp}`);
