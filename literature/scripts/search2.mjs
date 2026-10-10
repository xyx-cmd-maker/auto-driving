// paper-discovery probe v2: theme x venue-cluster, OpenAlex.
// Usage: node search2.mjs [--per-page N] [--topk N] [--out path]
// Writes candidates_v2.jsonl (raw) + search2.log.json (per-query hits/exported).
import fs from 'node:fs';

const arg = (k, d) => (process.argv.includes(k) ? process.argv[process.argv.indexOf(k) + 1] : d);
const PER_PAGE = Number(arg('--per-page', 8));
const TOPK = Number(arg('--topk', 10));
const OUT = arg('--out', 'candidates_v2.jsonl');
const MAILTO = 'research@example.org';

// Venue clusters: ISSN-L verified via OpenAlex /sources on 2026-04-16 (see venues.mjs output).
const CLUSTERS = {
  transport: {
    label: 'Transportation / ITS / vehicular',
    issns: ['1524-9050', '2379-8858', '0968-090X', '0191-2615', '0018-9545', '0041-1655', '0965-8564'],
  },
  control: {
    label: 'Control / robotics',
    issns: ['1063-6536', '0018-9286', '0005-1098', '2377-3766', '1556-4959', '2470-9476', '2573-5144'],
  },
  ml: {
    label: 'ML / AI flagship journals',
    issns: ['2522-5839', '0162-8828', '2162-237X', '1532-4435', '2041-1723', '2471-285X', '0925-2312'],
  },
};

const THEMES = [
  { id: 'K01', q: '"liquid neural network" OR "liquid time-constant"', note: 'LNN origin/family' },
  { id: 'K02', q: '"closed-form continuous-time" OR "continuous-time recurrent"', note: 'CfC controller' },
  { id: 'K03', q: '"neural ordinary differential equation" OR "neural ODE"', note: 'NODE + adjoint' },
  { id: 'K04', q: '"ordinary differential equation" AND "deep learning" AND control', note: 'ODE-based control' },
  { id: 'K05', q: '"car-following" OR "car following"', note: 'car-following core' },
  { id: 'K06', q: '"string stability" OR "platoon" OR "vehicle platoon"', note: 'platoon/string stability' },
  { id: 'K07', q: '"mixed traffic" OR "mixed autonomy"', note: 'mixed traffic ODD' },
  { id: 'K08', q: '"lane change" OR "lane-changing" OR overtaking', note: 'lane change/overtaking (OTF)' },
  { id: 'K09', q: '"traffic oscillation" OR "traffic flow" AND stability', note: 'traffic flow stability' },
  { id: 'K10', q: '"reinforcement learning" AND ("autonomous driving" OR "autonomous vehicle")', note: 'RL driving baseline' },
  { id: 'K11', q: '"model predictive control" AND (vehicle OR "autonomous driving")', note: 'MPC baseline' },
  { id: 'K12', q: '"control barrier function" OR "safety filter"', note: 'safety layer' },
  { id: 'K13', q: '"formal verification" AND ("neural network" OR controller)', note: 'verification' },
  { id: 'K14', q: '"embedded" OR "microcontroller" AND ("neural network" OR inference) AND "real-time"', note: 'MCU deployment' },
  { id: 'K15', q: '"quantization" OR "knowledge distillation" OR "model compression" AND "edge"', note: 'compression' },
  { id: 'K16', q: '"end-to-end" AND ("autonomous driving" OR "self-driving")', note: 'end-to-end AD' },
  { id: 'K17', q: '"trajectory prediction" AND ("autonomous driving" OR "road agents")', note: 'prediction (P2 bridge)' },
  { id: 'K18', q: '"world model" AND (driving OR "autonomous driving")', note: 'world model (P2 bridge)' },
  { id: 'K19', q: '"sim-to-real" OR "domain randomization" OR "CARLA"', note: 'sim2real + simulator' },
  { id: 'K20', q: '"physics-informed" OR "structure-preserving" OR "Hamiltonian"', note: 'physics-structured learning' },
  { id: 'K21', q: '"driver behaviour" OR "driver behavior" AND (heterogeneity OR aggressive)', note: 'driver heterogeneity' },
  { id: 'K22', q: '"sensitivity analysis" AND ("adjoint" OR "backpropagation")', note: 'adjoint sensitivity' },
];

const FIELDS = ['id', 'doi', 'display_name', 'publication_year', 'publication_date', 'type',
  'cited_by_count', 'authorships', 'primary_location', 'language'].join(',');

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function getJson(url, tries = 4) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url, { headers: { 'User-Agent': 'dsh-paper-discovery/1.0' } });
      if (r.status === 429 || r.status >= 500) { await sleep(2000 * (i + 1)); continue; }
      if (!r.ok) return { error: `HTTP ${r.status}` };
      return { json: await r.json() };
    } catch (e) {
      if (i === tries - 1) return { error: e.message };
      await sleep(1200 * (i + 1));
    }
  }
  return { error: 'retries exhausted' };
}

function url(q, issns) {
  const p = new URLSearchParams({
    search: q,
    filter: `primary_location.source.issn:${issns.join('|')},from_publication_date:2012-01-01,language:en`,
    sort: 'cited_by_count:desc',
    'per-page': String(PER_PAGE),
    select: FIELDS,
    mailto: MAILTO,
  });
  return `https://api.openalex.org/works?${p}`;
}

const rows = [];
const log = [];

for (const [cKey, c] of Object.entries(CLUSTERS)) {
  for (const t of THEMES) {
    const u = url(t.q, c.issns);
    const { json, error } = await getJson(u);
    if (error) {
      log.push({ theme: t.id, cluster: cKey, q: t.q, url: u, status: error, hits: null, exported: 0 });
      console.error(`[${t.id}/${cKey}] FAIL ${error}`);
      await sleep(700);
      continue;
    }
    const res = json.results || [];
    for (const r of res) {
      const src = (r.primary_location && r.primary_location.source) || {};
      rows.push({
        openalex_id: (r.id || '').replace('https://openalex.org/', ''),
        doi: r.doi ? r.doi.replace('https://doi.org/', '').toLowerCase() : null,
        title: r.display_name || '',
        year: r.publication_year,
        date: r.publication_date,
        venue: src.display_name || null,
        issn_l: src.issn_l || null,
        type: r.type,
        cited_by: r.cited_by_count,
        authors: (r.authorships || []).slice(0, 10).map((a) => (a.author && a.author.display_name) || ''),
        n_authors: (r.authorships || []).length,
        theme_ids: [t.id],
        theme_note: t.note,
        cluster: cKey,
      });
    }
    log.push({ theme: t.id, cluster: cKey, q: t.q, url: u, status: '200', hits: json.meta && json.meta.count, exported: res.length });
    console.error(`[${t.id}/${cKey}] hits=${(json.meta && json.meta.count) || 0} exported=${res.length}`);
    await sleep(700);
  }
}

// dedup: DOI > openalex_id ; keep best (max cited) venue record; merge theme ids
const byKey = new Map();
let merged = 0;
for (const r of rows) {
  const k = r.doi || r.openalex_id;
  if (byKey.has(k)) {
    const p = byKey.get(k);
    for (const t of r.theme_ids) if (!p.theme_ids.includes(t)) p.theme_ids.push(t);
    if ((r.cited_by || 0) > (p.cited_by || 0)) Object.assign(byKey.get(k), r, { theme_ids: p.theme_ids });
    merged++;
  } else byKey.set(k, r);
}

const all = [...byKey.values()].sort((a, b) => (b.cited_by || 0) - (a.cited_by || 0));
fs.writeFileSync(OUT, all.map((r) => JSON.stringify(r)).join('\n') + '\n', 'utf8');
fs.writeFileSync(OUT.replace(/\.jsonl$/, '.log.json'), JSON.stringify(log, null, 2), 'utf8');
console.error(`\nbefore_dedup=${rows.length} after_dedup=${all.length} merged=${merged} -> ${OUT}`);
