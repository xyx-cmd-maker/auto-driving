// UTF-8 integrity diagnostic: distinguishes real file corruption from console-display mojibake.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
const OUT = 'D:\\Deepseek Harness\\auto-driving\\literature\\fulltext';
const files = ['p01-cfc-nmi2022', 'p07-pinn-ctrl-neucom2024', 'p15-humanlike-cf-trc2018', 'p33-lpstring-tcst2014', 'p43-dissipation-trc2018', 'p45-deeplcc-tcst2023'];
const rows = [];
for (const f of files) {
  const buf = readFileSync(join(OUT, f + '.txt'));
  const s = buf.toString('utf8');
  const cjk = (s.match(/[\u3000-\u9fff\uf900-\ufaff]/g) || []).length;
  const repl = (s.match(/\ufffd/g) || []).length;
  const greek = (s.match(/[\u0370-\u03ff]/g) || []).length;
  const dash = (s.match(/[\u2013\u2014]/g) || []).length;
  const math = (s.match(/[+\-<=>]/g) || []).length;
  rows.push({ file: f, bytes: buf.length, chars: s.length, cjk, repl, greek, dash, mathish: math });
}
for (const r of rows) console.log(JSON.stringify(r));
// targeted probe: the exact spot that looked corrupted
const p01 = readFileSync(join(OUT, 'p01-cfc-nmi2022.txt'), 'utf8');
const m = /adaptive.{0,6}step solver/.exec(p01);
console.log('PROBE p01:', m ? JSON.stringify(m[0]) + ' codepoints=' + [...m[0]].map(c => c.codePointAt(0).toString(16)).join(',') : 'not found');
const p45 = readFileSync(join(OUT, 'p45-deeplcc-tcst2023.txt'), 'utf8');
const i = p45.indexOf('Heterogeneous Parameter Setup');
console.log('PROBE p45:', JSON.stringify(p45.slice(i, i + 160)));
const p33 = readFileSync(join(OUT, 'p33-lpstring-tcst2014.txt'), 'utf8');
const j = p33.indexOf('interconnected system is considered string stable');
console.log('PROBE p33:', JSON.stringify(p33.slice(j, j + 120)));
