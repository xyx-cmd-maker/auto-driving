import { readFileSync } from 'node:fs';
import { join } from 'node:path';
const OUT = 'D:\\Deepseek Harness\\auto-driving\\literature\\fulltext';
const g = (f) => readFileSync(join(OUT, f + '.txt'), 'utf8');

console.log('=== p01 markdown headings ===');
console.log(g('p01-cfc-nmi2022').split('\n').filter(l => /^#{1,4} /.test(l)).slice(0, 30).join('\n'));

console.log('\n=== p33 lines that look like IEEE section headings ===');
console.log(g('p33-lpstring-tcst2014').split('\n').filter(l => /^\s*([IVX]+\.|[A-Z]\.|\d+\.)\s+[A-Z]/.test(l)).slice(0, 40).join('\n'));

console.log('\n=== p33 occurrences of "Fig." / "Table" (case-sensitive) ===');
const p33 = g('p33-lpstring-tcst2014');
console.log('Fig. count:', (p33.match(/Fig\./g) || []).length, '| Table count:', (p33.match(/Table/g) || []).length, '| TABLE count:', (p33.match(/TABLE/g) || []).length);
console.log(p33.split('\n').filter(l => /Fig\.\s*\d/.test(l)).slice(0, 10).join('\n'));

console.log('\n=== p15 all lines containing "Figure" or "Fig." (first 25) ===');
const p15 = g('p15-humanlike-cf-trc2018');
console.log(p15.split('\n').filter(l => /(Figure|Fig\.)\s*\d/.test(l)).slice(0, 25).map(l => l.slice(0, 130)).join('\n'));

console.log('\n=== p15 TABLE captions ===');
console.log(p15.split('\n').filter(l => /TABLE\s*\d/i.test(l)).join('\n'));
