// Deterministic downloader. Usage: node _dl.mjs <name> <url> [<name> <url> ...]
import { writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const OUT = 'D:\\Deepseek Harness\\auto-driving\\literature\\fulltext';
const RAW = join(OUT, '_raw');
mkdirSync(RAW, { recursive: true });
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

const args = process.argv.slice(2);
for (let a = 0; a < args.length; a += 2) {
  const name = args[a];
  const url = args[a + 1];
  try {
    const r = await fetch(url, { redirect: 'follow', headers: { 'User-Agent': UA } });
    const buf = Buffer.from(await r.arrayBuffer());
    const ctype = r.headers.get('content-type') || '';
    const ext = /pdf/i.test(ctype) ? '.pdf' : '.bin';
    const p = join(RAW, name + ext);
    writeFileSync(p, buf);
    console.log(`OK   ${name} status=${r.status} bytes=${buf.length} type=${ctype} -> ${p}`);
  } catch (e) {
    console.log(`ERR  ${name} ${url} :: ${e.message}`);
  }
}
