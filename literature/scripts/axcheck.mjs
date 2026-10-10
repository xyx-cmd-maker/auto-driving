// axcheck.mjs — arXiv existence/version check via export API (plain text parsing).
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
for (const id of ids) {
  try {
    const t = await (await fetch(`https://export.arxiv.org/api/query?id_list=${encodeURIComponent(id)}&max_results=1`)).text();
    const s = t.indexOf('<entry>');
    if (s < 0) { console.log(`${id} | NO-ENTRY`); continue; }
    const e = t.slice(s, t.indexOf('</entry>', s));
    console.log([
      id, '|', pick(e, 'title'), '|', (pick(e, 'published') || '').slice(0, 10), '| upd', (pick(e, 'updated') || '').slice(0, 10),
      '| jr:', pick(e, 'arxiv:journal_ref') || '-', '| cm:', (pick(e, 'arxiv:comment') || '-').slice(0, 80),
    ].join(' '));
  } catch (err) { console.log(`${id} | ERR ${err.message}`); }
  await sleep(3300);
}
