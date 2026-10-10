// search4.mjs — targeted gap search (OpenAlex). Tries multiple hosts; degrades gracefully.
import fs from 'node:fs';
const arg = (k, d) => (process.argv.includes(k) ? process.argv[process.argv.indexOf(k) + 1] : d);
const OUT = arg('--out', 'candidates_gap.jsonl');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// G1 deployment/compression/edge-TinyML ; G2 vehicle longitudinal+lateral control & AV control journals
const QUERIES = [
  { id: 'D01', q: '("microcontroller" OR "TinyML" OR "edge inference" OR "embedded deep learning") AND ("neural network" OR inference)' },
  { id: 'D02', q: '("model compression" OR quantization OR pruning OR "knowledge distillation") AND ("edge" OR "embedded" OR "mobile")' },
  { id: 'D03', q: '("real-time" OR latency) AND ("neural network" OR controller) AND ("autonomous driving" OR vehicle)' },
  { id: 'D04', q: '("neural network" OR "deep learning") AND ("model predictive control" OR "control barrier") AND vehicle' },
  { id: 'D05', q: '("adaptive cruise control" OR "cooperative adaptive cruise") ' },
  { id: 'D06', q: '("lateral control" OR "path tracking" OR "trajectory tracking") AND ("autonomous vehicle" OR "automated driving")' },
  { id: 'D07', q: '("energy-efficient" OR "eco-driving") AND ("platoon" OR "connected automated")' },
  { id: 'D08', q: '("event-triggered" OR "sampled-data" OR "networked control") AND vehicle' },
  { id: 'D09', q: '("driver behaviour" OR "driving style" OR "human driver") AND ("car-following" OR "lane change" OR heterogeneity)' },
  { id: 'D10', q: '("irregularly sampled" OR "irregular sampling" OR "continuous-time") AND ("time series" OR "control")' },
  { id: 'D11', q: '("overtaking" OR "cut-in" OR "surrogate safety") AND ("safety" OR "risk")' },
  { id: 'D12', q: '("traffic pressure" OR "social force" OR "potential field") AND (traffic OR vehicle OR driving)' },
];

const CLUSTERS = {
  transport: ['1524-9050', '2379-8858', '0968-090X', '0191-2615', '0018-9545', '0965-8564', '2046-0430'],
  control: ['1063-6536', '0018-9286', '0005-1098', '2377-3766', '1556-4959', '2470-9476'],
  ml: ['2522-5839', '0162-8828', '2162-237X', '0018-9219', '2327-4662', '1536-1233', '0925-2312', '2471-285X'],
};
const FIELDS = ['id', 'doi', 'display_name', 'publication_year', 'publication_date', 'type', 'cited_by_count', 'authorships', 'primary_location'].join(',');
const MAILTO = 'research@example.org';

async function get(url, tries = 3) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url, { headers: { 'User-Agent': 'dsh-paper-discovery/1.0' } });
      if (r.status === 429 || r.status >= 500) { await sleep(4000 * (i + 1)); continue; }
      if (!r.ok) return { error: `HTTP ${r.status}` };
      return { json: await r.json() };
    } catch (e) { if (i === tries - 1) return { error: e.message }; await sleep(3000 * (i + 1)); }
  }
  return { error: 'retries exhausted' };
}

const rows = []; const log = [];
for (const [ck, issns] of Object.entries(CLUSTERS)) {
  for (const t of QUERIES) {
    const p = new URLSearchParams({
      search: t.q,
      filter: `primary_location.source.issn:${issns.join('|')},from_publication_date:2012-01-01,language:en`,
      sort: 'cited_by_count:desc', 'per-page': '10', select: FIELDS, mailto: MAILTO,
    });
    const u = `https://api.openalex.org/works?${p}`;
    const { json, error } = await get(u);
    if (error) { log.push({ theme: t.id, cluster: ck, q: t.q, url: u, status: error, hits: null, exported: 0 }); console.error(`[${t.id}/${ck}] ${error}`); await sleep(2500); continue; }
    const res = json.results || [];
    for (const r of res) {
      const src = (r.primary_location && r.primary_location.source) || {};
      rows.push({ openalex_id: (r.id || '').replace('https://openalex.org/', ''), doi: r.doi ? r.doi.replace('https://doi.org/', '').toLowerCase() : null,
        title: r.display_name || '', year: r.publication_year, date: r.publication_date, venue: src.display_name || null,
        issn_l: src.issn_l || null, type: r.type, cited_by: r.cited_by_count,
        authors: (r.authorships || []).slice(0, 8).map((a) => (a.author && a.author.display_name) || ''), theme_ids: [t.id], cluster: ck });
    }
    log.push({ theme: t.id, cluster: ck, q: t.q, url: u, status: '200', hits: json.meta && json.meta.count, exported: res.length });
    console.error(`[${t.id}/${ck}] hits=${(json.meta && json.meta.count) || 0} exported=${res.length}`);
    await sleep(2500);
  }
}
const byKey = new Map();
for (const r of rows) { const k = r.doi || r.openalex_id; if (!byKey.has(k)) byKey.set(k, r); }
fs.writeFileSync(OUT, [...byKey.values()].map((r) => JSON.stringify(r)).join('\n') + '\n', 'utf8');
fs.writeFileSync(OUT.replace(/\.jsonl$/, '.log.json'), JSON.stringify(log, null, 2), 'utf8');
console.error(`after_dedup=${byKey.size} -> ${OUT}`);
