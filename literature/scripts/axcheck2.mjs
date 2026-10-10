// axcheck2.mjs — arXiv existence/version check for many IDs in ONE request (id_list limit ~ 100).
const ids = process.argv.slice(2);
const pick = (s, tag) => {
  const open = s.indexOf(`<${tag}`);
  if (open < 0) return null;
  const gt = s.indexOf('>', open);
  const close = s.indexOf(`</${tag}>`, gt);
  if (close < 0) return null;
  return s.slice(gt + 1, close).replace(/\s+/g, ' ').trim();
};
const url = `https://export.arxiv.org/api/query?id_list=${ids.map(encodeURIComponent).join(',')}&max_results=100`;
const t = await (await fetch(url)).text();
const total = pick(t, 'opensearch:totalResults');
console.log(`requested=${ids.length} totalResults=${total} feed_bytes=${t.length}`);
const entries = [];
let i = 0;
while ((i = t.indexOf('<entry>', i)) >= 0) {
  const e = t.slice(i, t.indexOf('</entry>', i));
  const idUrl = pick(e, 'id') || '';
  entries.push({
    id: idUrl.replace('http://arxiv.org/abs/', '').replace('https://arxiv.org/abs/', ''),
    title: pick(e, 'title'),
    published: (pick(e, 'published') || '').slice(0, 10),
    updated: (pick(e, 'updated') || '').slice(0, 10),
    journal_ref: pick(e, 'arxiv:journal_ref'),
    comment: pick(e, 'arxiv:comment'),
  });
  i += 8;
}
for (const e of entries) console.log([e.id, '|', e.published, '| upd', e.updated, '|', e.title, '| jr:', e.journal_ref || '-', '| cm:', (e.comment || '-').slice(0, 70)].join(' '));
const got = new Set(entries.map((e) => e.id.split('v')[0]));
const missing = ids.filter((x) => !got.has(x));
if (missing.length) console.log('MISSING: ' + missing.join(', '));
