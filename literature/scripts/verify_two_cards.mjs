// 一次性核验脚本：为 fresh2024 两张精读卡做「正式版核验」（arXiv API + Crossref）
// 用法：node verify_two_cards.mjs
// 输出：literature/fresh2024/verify_two_cards.json（原始返回留档，作为取用证据）
const OUT = 'D:/Deepseek Harness/auto-driving/literature/fresh2024/verify_two_cards.json';
const UA = 'otf-p1-litcheck/1.0 (mailto:research@example.org)';

const ids = ['2506.16311', '2601.06227'];
const titles = [
  'Towards Emergency Scenarios: An Integrated Decision-making Framework of Multi-lane Platoon Reorganization',
  'When Smaller Wins: Dual-Stage Distillation and Pareto-Guided Compression of Liquid Neural Networks for Edge Battery Prognostics',
];

const log = [];
async function get(url) {
  try {
    const r = await fetch(url, { headers: { 'User-Agent': UA, Accept: 'application/json, application/atom+xml, */*' } });
    const t = await r.text();
    return { url, status: r.status, len: t.length, body: t };
  } catch (e) {
    return { url, status: 'ERR', error: String(e) };
  }
}

// 1) arXiv API：取 comment / journal_ref / version 历史
for (const id of ids) {
  const r = await get(`http://export.arxiv.org/api/query?id_list=${id}&max_results=1`);
  log.push({ kind: 'arxiv', id, status: r.status, len: r.len, body: r.body });
}

// 2) Crossref 题名匹配（卡片模板要求的那一次查询）
for (const t of titles) {
  const u = `https://api.crossref.org/works?query.bibliographic=${encodeURIComponent(t)}&rows=3&select=DOI,title,container-title,type,issued,published,created,author,event,ISBN,page,publisher,abstract`;
  const r = await get(u);
  let items = null;
  try { items = JSON.parse(r.body).message.items; } catch { items = null; }
  log.push({ kind: 'crossref', query: t, status: r.status, items });
}

// 3) Crossref 精确短语查询（补充：看 ICPR 2026 论文集的收录情况）
{
  const u = `https://api.crossref.org/works?query.bibliographic=${encodeURIComponent('Dual-Stage Distillation Pareto-Guided Compression Liquid Neural Networks Battery')}&rows=5&select=DOI,title,container-title,type,issued,published,created`;
  const r = await get(u);
  let items = null;
  try { items = JSON.parse(r.body).message.items; } catch { items = null; }
  log.push({ kind: 'crossref', query: 'Dual-Stage Distillation Pareto-Guided Compression Liquid Neural Networks Battery', status: r.status, items });
}

// 4) ICPR 2026 会议论文集检索（Crossref container-title 含 ICPR）
for (const q of ['ICPR 2026 International Conference on Pattern Recognition', 'Pattern Recognition ICPR 2026 proceedings']) {
  const u = `https://api.crossref.org/works?query.container-title=${encodeURIComponent(q)}&rows=3&select=DOI,title,container-title,type,issued`;
  const r = await get(u);
  let items = null;
  try { items = JSON.parse(r.body).message.items; } catch { items = null; }
  log.push({ kind: 'crossref-container', query: q, status: r.status, items });
}

const fs = await import('node:fs');
fs.writeFileSync(OUT, JSON.stringify({ run_at_utc: new Date().toISOString(), channel: 'arXiv API + Crossref REST (api.crossref.org/works?query.bibliographic=...)', log }, null, 1), 'utf8');
console.log('written', OUT);

// 摘要打印
for (const e of log) {
  if (e.kind === 'arxiv') {
    const m = /<entry>[\s\S]*?<\/entry>/.exec(e.body || '');
    const g = (re) => { const x = re.exec(e.body || ''); return x ? x[1].replace(/\s+/g, ' ').trim() : null; };
    console.log('\n=== arXiv', e.id, 'status', e.status, '===');
    console.log(' title      :', g(/<title>([\s\S]*?)<\/title>/));
    console.log(' published  :', g(/<published>(.*?)<\/published>/));
    console.log(' updated    :', g(/<updated>(.*?)<\/updated>/));
    console.log(' comment    :', g(/<arxiv:comment[^>]*>([\s\S]*?)<\/arxiv:comment>/));
    console.log(' journal_ref:', g(/<arxiv:journal_ref[^>]*>([\s\S]*?)<\/arxiv:journal_ref>/));
    console.log(' doi        :', g(/<arxiv:doi[^>]*>([\s\S]*?)<\/arxiv:doi>/));
    console.log(' primary    :', g(/<arxiv:primary_category[^>]*term="([^"]+)"/));
    console.log(' entry-len  :', m ? m[0].length : 0);
  } else {
    console.log('\n===', e.kind, '|', e.query, '| status', e.status, '===');
    for (const it of (e.items || [])) {
      console.log('  -', it.DOI, '|', (it.title && it.title[0] || '').slice(0, 110), '|', (it['container-title'] && it['container-title'][0]) || '', '|', it.type, '|', JSON.stringify(it.issued || it.published || it.created || ''));
    }
    if (!e.items) console.log('  (parse failed)');
  }
}
