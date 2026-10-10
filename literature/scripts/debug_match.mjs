// debug_match.mjs
import fs from 'node:fs';
const lib = fs.readFileSync('library/P1-library.jsonl', 'utf8').trim().split('\n').map((l) => JSON.parse(l));
for (const sid of ['E1', 'F5']) {
  const r = lib.find((x) => x.id === `old:${sid}`);
  console.log(`=== ${sid} ===`);
  console.log('title:', JSON.stringify(r.title));
  console.log('doi:', r.doi, '| dois:', JSON.stringify(r.dois));
  console.log('citation:', JSON.stringify((r.citation || '').slice(0, 260)));
}
const primaryCBF = lib.find((x) => x.n_p1 === 111);
const primaryNu = lib.find((x) => x.n_p1 === 114);
console.log('\n#111:', JSON.stringify({ doi: primaryCBF.doi, t: primaryCBF.title }));
console.log('#114:', JSON.stringify({ doi: primaryNu.doi, t: primaryNu.title }));
const STOP = new Set(['a', 'an', 'the', 'of', 'for', 'and', 'in', 'on', 'to', 'with', 'via', 'using', 'from', 'by', 'at', 'is', 'are', 'as', 'into', 'its', 'their']);
const toks = (s) => [...new Set((s || '').toLowerCase().replace(/[^a-z0-9\s]/g, ' ').split(/\s+/).filter((w) => w.length > 2 && !STOP.has(w)))];
const titleToks = (s) => toks(s).filter((w) => !(w.length <= 3 && /^[a-z]+$/.test(w)) && !/^\d+$/.test(w));
const jacTitle = (a, b) => { const A = new Set(titleToks(a)), B = new Set(titleToks(b)); let i = 0; for (const x of A) if (B.has(x)) i++; return i / (A.size + B.size - i); };
console.log('\njacTitle(E1,#111) =', jacTitle(lib.find((x) => x.id === 'old:E1').title, primaryCBF.title).toFixed(3));
console.log('jacTitle(F5,#114) =', jacTitle(lib.find((x) => x.id === 'old:F5').title, primaryNu.title).toFixed(3));
console.log('tokens E1:', titleToks(lib.find((x) => x.id === 'old:E1').title).join(','));
console.log('tokens #111:', titleToks(primaryCBF.title).join(','));
console.log('tokens F5:', titleToks(lib.find((x) => x.id === 'old:F5').title).join(','));
console.log('tokens #114:', titleToks(primaryNu.title).join(','));
