// 第二轮核验：取正式版 DOI 的完整题录 + T5 撤稿/更正检查（Crossref update-to）
const OUT = 'D:/Deepseek Harness/auto-driving/literature/fresh2024/verify_two_cards.json';
const UA = 'otf-p1-litcheck/1.0 (mailto:research@example.org)';
const dois = ['10.1109/tce.2025.3612821', '10.1007/978-3-032-31441-3_28'];

async function get(url) {
  try {
    const r = await fetch(url, { headers: { 'User-Agent': UA, Accept: 'application/json' } });
    return { url, status: r.status, text: await r.text() };
  } catch (e) { return { url, status: 'ERR', text: String(e) }; }
}

const out = [];
for (const d of dois) {
  const r = await get(`https://api.crossref.org/works/${encodeURIComponent(d)}`);
  let m = null;
  try { m = JSON.parse(r.text).message; } catch {}
  out.push({ doi: d, status: r.status, message: m ? {
    DOI: m.DOI, title: m.title, 'container-title': m['container-title'], type: m.type,
    issued: m.issued, published: m.published, created: m.created, deposited: m.deposited,
    page: m.page, volume: m.volume, issue: m.issue, ISBN: m.ISBN, publisher: m.publisher,
    event: m.event, author: (m.author || []).map(a => `${a.given || ''} ${a.family || ''}`.trim()),
    abstract_len: m.abstract ? m.abstract.length : 0,
    'update-to': m['update-to'] || null, 'updated-by': m['updated-by'] || null,
    relation: m.relation || null,
    reference_count: m['reference-count'], is_referenced_by_count: m['is-referenced-by-count'],
    license: (m.license || []).map(l => l.URL),
  } : null, raw_len: r.text.length });
}

// 反查：这两篇是否有被更正/撤稿的记录（Crossref 的 update-to 字段来自被查记录本身；
// 另用 query.bibliographic 找同题名的其他类型记录）
const fs = await import('node:fs');
fs.writeFileSync('D:/Deepseek Harness/auto-driving/literature/fresh2024/verify_two_cards_round2.json', JSON.stringify({ run_at_utc: new Date().toISOString(), out }, null, 1), 'utf8');
for (const e of out) {
  console.log('\n===', e.doi, 'status', e.status, '===');
  if (!e.message) { console.log(e.raw_len, 'bytes, parse failed'); continue; }
  const m = e.message;
  console.log(' title      :', (m.title || []).join(' | '));
  console.log(' container  :', (m['container-title'] || []).join(' | '));
  console.log(' type       :', m.type, '| page', m.page, '| vol', m.volume, '| issue', m.issue);
  console.log(' issued     :', JSON.stringify(m.issued), '| published', JSON.stringify(m.published));
  console.log(' published-online/print:', JSON.stringify(m.published));
  console.log(' ISBN       :', (m.ISBN || []).join(','));
  console.log(' publisher  :', m.publisher);
  console.log(' event      :', JSON.stringify(m.event));
  console.log(' authors    :', m.author.join(' ; '));
  console.log(' update-to  :', JSON.stringify(m['update-to']));
  console.log(' updated-by :', JSON.stringify(m['updated-by']));
  console.log(' relation   :', JSON.stringify(m.relation));
  console.log(' refs / cited-by:', m.reference_count, '/', m.is_referenced_by_count);
  console.log(' license    :', m.license.join(' , '));
}
