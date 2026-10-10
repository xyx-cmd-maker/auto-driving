// axsearch.mjs — arXiv incremental search (2024+) for P1-relevant topics.
// arXiv export API only; >=3 s between requests.
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const pick = (s, tag) => {
  const open = s.indexOf(`<${tag}`);
  if (open < 0) return null;
  const gt = s.indexOf('>', open);
  const close = s.indexOf(`</${tag}>`, gt);
  if (close < 0) return null;
  return s.slice(gt + 1, close).replace(/\s+/g, ' ').trim();
};
const QUERIES = [
  { id: 'A1', q: 'all:"liquid neural network"' },
  { id: 'A2', q: 'all:"liquid time-constant"' },
  { id: 'A3', q: 'all:"closed-form continuous-time"' },
  { id: 'A4', q: 'all:"neural ordinary differential equation" AND all:control' },
  { id: 'A5', q: 'all:"string stability" AND all:"mixed traffic"' },
  { id: 'A6', q: 'all:"car-following" AND all:"reinforcement learning"' },
  { id: 'A7', q: 'all:"TinyML"' },
  { id: 'A8', q: 'all:"microcontroller" AND all:"neural network" AND all:inference' },
];
const all = [];
for (const t of QUERIES) {
  const url = `https://export.arxiv.org/api/query?search_query=${encodeURIComponent(t.q)}`
    + `&start=0&max_results=30&sortBy=submittedDate&sortOrder=descending`;
  let txt = '';
  for (let k = 0; k < 4; k++) {
    txt = await (await fetch(url)).text();
    if (txt.includes('<entry>') || txt.includes('totalResults')) break;
    await sleep(5000 * (k + 1));
  }
  const total = pick(txt, 'opensearch:totalResults');
  const rows = [];
  let p = 0;
  while ((p = txt.indexOf('<entry>', p)) >= 0) {
    const e = txt.slice(p, txt.indexOf('</entry>', p));
    rows.push({
      query_id: t.id,
      arxiv: (pick(e, 'id') || '').replace(/https?:\/\/arxiv\.org\/abs\//, ''),
      title: pick(e, 'title'),
      published: (pick(e, 'published') || '').slice(0, 10),
      updated: (pick(e, 'updated') || '').slice(0, 10),
      journal_ref: pick(e, 'arxiv:journal_ref'),
      comment: (pick(e, 'arxiv:comment') || '').slice(0, 120),
    });
    p += 8;
  }
  // incremental only: 2024+
  const inc = rows.filter((r) => r.published >= '2024-01-01');
  all.push(...inc);
  console.error(`[${t.id}] total=${total} fetched=${rows.length} since2024=${inc.length}`);
  await sleep(3600);
}
const seen = new Set();
const dedup = all.filter((r) => (seen.has(r.arxiv) ? false : (seen.add(r.arxiv), true)));
console.log(`total_since2024=${all.length} unique=${dedup.length}`);
for (const r of dedup) console.log([r.published, r.arxiv, '|', (r.title || '').slice(0, 96), '| jr:', r.journal_ref || '-', '|', r.comment || '-'].join(' '));
const fs = await import('node:fs');
fs.writeFileSync('gap_recent_arxiv.jsonl', dedup.map((r) => JSON.stringify(r)).join('\n') + '\n', 'utf8');
