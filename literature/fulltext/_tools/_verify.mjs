// Coverage verification: sections, captions, table labels, key numbers.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
const OUT = 'D:\\Deepseek Harness\\auto-driving\\literature\\fulltext';
const files = ['p01-cfc-nmi2022', 'p07-pinn-ctrl-neucom2024', 'p15-humanlike-cf-trc2018', 'p33-lpstring-tcst2014', 'p43-dissipation-trc2018', 'p45-deeplcc-tcst2023'];
const want = ['Abstract', 'Introduction', 'Conclusion'];
for (const f of files) {
  const s = readFileSync(join(OUT, f + '.txt'), 'utf8');
  const hit = want.map(w => w + '=' + (new RegExp(w, 'i').test(s) ? 'Y' : 'N')).join(' ');
  const figCap = (s.match(/(?:Fig\.|Figure)\s*\d+\s*[:.]/g) || []).length;
  const tabLab = (s.match(/(?:TABLE|Table)\s+[IVX0-9]+\s*[:.]?/g) || []).length;
  const refs = /References|REFERENCES|Bibliography/.test(s) ? 'Y' : 'N';
  const digits = (s.match(/\d/g) || []).length;
  console.log(`${f.padEnd(30)} ${hit}  figCap=${String(figCap).padStart(3)}  tabLabels=${String(tabLab).padStart(3)}  refs=${refs}  digits=${digits}`);
}
console.log('\n--- p33 explicit TABLE search ---');
const p33 = readFileSync(join(OUT, 'p33-lpstring-tcst2014.txt'), 'utf8');
console.log('has "TABLE I":', /TABLE\s+I\b/.test(p33), '| has "TABLE":', /TABLE/.test(p33));
console.log('\n--- p33 first 900 chars ---');
console.log(p33.slice(0, 900));
console.log('\n--- p15 section-ish lines ---');
const p15 = readFileSync(join(OUT, 'p15-humanlike-cf-trc2018.txt'), 'utf8');
console.log(p15.split('\n').filter(l => /^\s*\d+(\.\d+)*\s+[A-Z]/.test(l)).slice(0, 18).join('\n'));
