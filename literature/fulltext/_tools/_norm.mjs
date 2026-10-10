// Normalize CRLF -> LF in PDF-derived outputs (cosmetic consistency).
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
const OUT = 'D:\\Deepseek Harness\\auto-driving\\literature\\fulltext';
for (const f of ['p15-humanlike-cf-trc2018', 'p33-lpstring-tcst2014']) {
  const p = join(OUT, f + '.txt');
  const s = readFileSync(p, 'utf8');
  const n = s.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
  writeFileSync(p, n, 'utf8');
  console.log(`${f}: crlf=${(s.match(/\r\n/g) || []).length} -> chars=${n.length}`);
}
