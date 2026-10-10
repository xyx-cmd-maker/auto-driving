import { readFileSync } from 'node:fs';
import { join } from 'node:path';
const OUT = 'D:\\Deepseek Harness\\auto-driving\\literature\\fulltext';
const g = (f) => readFileSync(join(OUT, f + '.txt'), 'utf8');
const p15 = g('p15-humanlike-cf-trc2018');
const p33 = g('p33-lpstring-tcst2014');

console.log('=== p15: uppercase FIGURE / Fig occurrences ===');
console.log('FIGURE:', (p15.match(/FIGURE/g) || []).length, '| "Fig.":', (p15.match(/Fig\./g) || []).length);
const cand = p15.split('\n').filter(l => /^\s*(FIGURE|Figure|Fig\.?)\s*\d+\s*[.:]?\s*\S/.test(l));
console.log('lines STARTING with a figure label:', cand.length);
console.log(cand.slice(0, 20).map(l => '  ' + l.slice(0, 140)).join('\n'));

console.log('\n=== p15: PAGE 12 raw slice (looking for figure captions) ===');
const p12 = p15.split('===== PAGE 12 =====')[1] || '';
console.log(p12.split('\n').filter(l => l.trim()).slice(0, 45).map(l => '  ' + l.slice(0, 130)).join('\n'));

console.log('\n=== p33: table-like numeric lines (3+ numbers separated by 2+ spaces) ===');
const t = p33.split('\n').filter(l => ((l.match(/\d+(\.\d+)?/g) || []).length >= 4) && /\s{2,}/.test(l));
console.log('count:', t.length);
console.log(t.slice(0, 15).map(l => '  ' + l.slice(0, 150)).join('\n'));

console.log('\n=== p33: VI. EXPERIMENTAL VALIDATION slice ===');
const ei = p33.indexOf('VI. EXPERIMENTAL VALIDATION');
console.log(JSON.stringify(p33.slice(ei, ei + 1300)));
