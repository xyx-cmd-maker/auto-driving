// axcheck3.mjs — arXiv check in small batches with spacing; writes JSON.
import fs from 'node:fs';
const ids = process.argv.slice(2);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const pick = (s, tag) => {
  const open = s.indexOf(`<${tag}`);
  if (open < 0) return null;
  const gt = s.indexOf('>', open);
  const close = s.indexOf(`</${tag}>`, gt);
  if (close < 0) return null;
  return s.slice(gt + 1, close).replace(/\s+/g, ' ').trim();
};
const out = [];
const B = 6;
for (let i = 0; i < ids.length; i += B) {
  const batch = ids.slice(i, i + B);
  const url = `https://export.arxiv.org/api/query?id_list=${batch.map(encodeURIComponent).join(',')}&max_results=20`;
  let t = '';
  for (let k = 0; k < 4; k++) {
    t = await (await fetch(url)).text();
    if (t.includes('<entry>')) break;
    await sleep(5000 * (k + 1));
  }
  const entries = [];
  let p = 0;
  while ((p = t.indexOf('<entry>', p)) >= 0) {
    const e = t.slice(p, t.indexOf('</entry>', p));
    entries.push({
      id: (pick(e, 'id') || '').replace(/https?:\/\/arxiv\.org\/abs\//, ''),
      title: pick(e, 'title'),
      published: (pick(e, 'published') || '').slice(0, 10),
      updated: (pick(e, 'updated') || '').slice(0, 10),
      journal_ref: pick(e, 'arxiv:journal_ref'),
      comment: pick(e, 'arxiv:comment'),
    });
    p += 8;
  }
  for (const b of batch) {
    const hit = entries.find((e) => e.id.split('v')[0] === b);
    out.push(hit ? { requested: b, ...hit } : { requested: b, error: 'NO-ENTRY' });
  }
  console.error(`batch ${i / B + 1}: requested=${batch.length} entries=${entries.length}`);
  await sleep(4000);
}
for (const r of out) {
  console.log(r.error ? `${r.requested} | MISSING` : `${r.requested} | ${r.published} | upd ${r.updated} | ${r.title} | jr:${r.journal_ref || '-'} | cm:${(r.comment || '-').slice(0, 60)}`);
}
fs.writeFileSync('arxiv_checked.json', JSON.stringify(out, null, 2), 'utf8');
console.error(`wrote arxiv_checked.json (${out.length}); missing=${out.filter((o) => o.error).length}`);
