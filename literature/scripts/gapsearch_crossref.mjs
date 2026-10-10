// gapsearch_crossref.mjs — Crossref-only gap search (OpenAlex anonymous budget exhausted, resets 00:00 UTC).
// Purpose A: 嵌入式/TinyML/MCU 部署主题（本次会话未覆盖）
// Purpose B: 近 2 年（2024+）新工作增量，按 publication_date 排序
// Output: gap_crossref.jsonl (+ log)
import fs from 'node:fs';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const MAILTO = 'research@example.org';

const MODE = process.argv.includes('--recent') ? 'recent' : 'embedded';

const QUERIES = MODE === 'embedded' ? [
  { id: 'E1', q: '"TinyML" "microcontroller"', from: '2017-01-01' },
  { id: 'E2', q: '"tiny machine learning" survey', from: '2017-01-01' },
  { id: 'E3', q: '"post-training quantization"', from: '2017-01-01' },
  { id: 'E4', q: '"quantization" "neural network inference" survey', from: '2017-01-01' },
  { id: 'E5', q: '"knowledge distillation" survey', from: '2017-01-01' },
  { id: 'E6', q: '"model compression" "deep neural network" survey', from: '2017-01-01' },
  { id: 'E7', q: '"edge intelligence" "deep learning" survey', from: '2017-01-01' },
  { id: 'E8', q: '"Cortex-M" neural network kernel', from: '2017-01-01' },
  { id: 'E9', q: '"on-device" inference latency microcontroller', from: '2017-01-01' },
] : [
  { id: 'R1', q: '"liquid neural network"', from: '2024-01-01' },
  { id: 'R2', q: '"liquid time-constant"', from: '2024-01-01' },
  { id: 'R3', q: '"closed-form continuous-time"', from: '2024-01-01' },
  { id: 'R4', q: '"neural ordinary differential equation" control', from: '2024-01-01' },
  { id: 'R5', q: '"string stability" "mixed traffic"', from: '2024-01-01' },
  { id: 'R6', q: '"car-following" "reinforcement learning"', from: '2024-01-01' },
  { id: 'R7', q: '"control barrier function" "learning-based control"', from: '2024-01-01' },
  { id: 'R8', q: '"vehicle platoon" "mixed traffic" control', from: '2024-01-01' },
  { id: 'R9', q: '"overtaking" "traffic flow" stability', from: '2024-01-01' },
];

const SELECT = 'DOI,title,author,issued,container-title,type,volume,issue,page,is-referenced-by-count,publisher,abstract';

async function get(url, tries = 5) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url, { headers: { 'User-Agent': 'dsh-gap-search/1.0 (mailto:research@example.org)' } });
      if (r.status === 429 || r.status >= 500) { await sleep(9000 * (i + 1)); continue; }
      if (!r.ok) return { error: `HTTP ${r.status}` };
      return { json: await r.json() };
    } catch (e) { if (i === tries - 1) return { error: e.message }; await sleep(6000 * (i + 1)); }
  }
  return { error: 'retries exhausted' };
}

const rows = [];
const log = [];
for (const t of QUERIES) {
  const sort = MODE === 'recent' ? 'published' : 'is-referenced-by-count';
  const url = `https://api.crossref.org/works?query.bibliographic=${encodeURIComponent(t.q)}`
    + `&filter=from-pub-date:${t.from},type:journal-article`
    + `&sort=${sort}&order=desc&rows=25&select=${SELECT}&mailto=${MAILTO}`;
  const r = await get(url, 8);
  if (r.json && r.json.message) {
    const items = r.json.message.items || [];
    rows.push(...items.map((x) => ({
      query_id: t.id, mode: MODE,
      doi: x.DOI,
      title: (x.title && x.title[0]) || '',
      year: (x.issued && x.issued['date-parts'] && x.issued['date-parts'][0] && x.issued['date-parts'][0][0]) || null,
      date: (x.issued && x.issued['date-parts'] && x.issued['date-parts'][0] || []).join('-'),
      venue: (x['container-title'] && x['container-title'][0]) || null,
      type: x.type, volume: x.volume || null, issue: x.issue || null, page: x.page || null,
      authors: (x.author || []).map((a) => [a.given, a.family].filter(Boolean).join(' ')).slice(0, 8),
      n_authors: (x.author || []).length,
      cited_by: x['is-referenced-by-count'] || 0,
      abstract: x.abstract ? x.abstract.replace(/<[^>]+>/g, '').slice(0, 600) : null,
    })));
    log.push({ id: t.id, mode: MODE, q: t.q, from: t.from, sort, url, status: '200', hits: r.json.message['total-results'], exported: items.length });
    console.error(`[${t.id}] hits=${r.json.message['total-results']} exported=${items.length}`);
  } else {
    log.push({ id: t.id, mode: MODE, q: t.q, from: t.from, sort, url, status: r.error || `HTTP ${r.status}`, hits: null, exported: 0 });
    console.error(`[${t.id}] FAIL ${r.error}`);
  }
  await sleep(8000);
}

const seen = new Set();
const dedup = rows.filter((r) => (seen.has(r.doi) ? false : (seen.add(r.doi), true)));
const out = `gap_${MODE}_crossref.jsonl`;
fs.writeFileSync(out, dedup.map((r) => JSON.stringify(r)).join('\n') + '\n', 'utf8');
fs.writeFileSync(`gap_${MODE}_crossref.log.json`, JSON.stringify(log, null, 2), 'utf8');
console.error(`\nbefore_dedup=${rows.length} after_dedup=${dedup.length} -> ${out}`);
