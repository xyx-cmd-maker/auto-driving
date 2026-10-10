// paper-discovery probe v3: single theme x single cluster, mergeable, long backoff.
// Usage: node search3.mjs [--per-page 8] [--out candidates_v2.jsonl] [--gap 1500]
import fs from 'node:fs';

const arg = (k, d) => (process.argv.includes(k) ? process.argv[process.argv.indexOf(k) + 1] : d);
const PER_PAGE = Number(arg('--per-page', 8));
const OUT = arg('--out', 'candidates_v2.jsonl');
const GAP = Number(arg('--gap', 1500));
const MAILTO = 'research@example.org';

const CLUSTERS = {
  transport: { issns: ['1524-9050', '2379-8858', '0968-090X', '0191-2615', '0018-9545', '0041-1655', '0965-8564'] },
  control: { issns: ['1063-6536', '0018-9286', '0005-1098', '2377-3766', '1556-4959', '2470-9476', '2573-5144'] },
  ml: { issns: ['2522-5839', '0162-8828', '2162-237X', '1532-4435', '2041-1723', '2471-285X', '0925-2312'] },
};

const THEMES = [
  { id: 'K01', q: '"liquid neural network" OR "liquid time-constant"' },
  { id: 'K02', q: '"closed-form continuous-time" OR "continuous-time recurrent"' },
  { id: 'K03', q: '"neural ordinary differential equation" OR "neural ODE"' },
  { id: 'K04', q: '"ordinary differential equation" AND "deep learning" AND control' },
  { id: 'K05', q: '"car-following" OR "car following"' },
  { id: 'K06', q: '"string stability" OR "platoon" OR "vehicle platoon"' },
  { id: 'K07', q: '"mixed traffic" OR "mixed autonomy"' },
  { id: 'K08', q: '"lane change" OR "lane-changing" OR overtaking' },
  { id: 'K09', q: '"traffic oscillation" OR ("traffic flow" AND stability)' },
  { id: 'K10', q: '"reinforcement learning" AND ("autonomous driving" OR "autonomous vehicle")' },
  { id: 'K11', q: '"model predictive control" AND (vehicle OR "autonomous driving")' },
  { id: 'K12', q: '"control barrier function" OR "safety filter"' },
  { id: 'K13', q: '"formal verification" AND ("neural network" OR controller)' },
  { id: 'K14', q: '("embedded" OR "microcontroller") AND ("neural network" OR inference)' },
  { id: 'K15', q: '"quantization" OR "knowledge distillation" OR "model compression"' },
  { id: 'K16', q: '"end-to-end" AND ("autonomous driving" OR "self-driving")' },
  { id: 'K17', q: '"trajectory prediction" AND ("autonomous driving" OR "road agents" OR "road users")' },
  { id: 'K18', q: '"world model" AND (driving OR "autonomous driving")' },
  { id: 'K19', q: '"sim-to-real" OR "domain randomization" OR "CARLA"' },
  { id: 'K20', q: '"physics-informed" OR "structure-preserving" OR "Hamiltonian"' },
  { id: 'K21', q: '"driver behaviour" OR "driver behavior" OR "driving style"' },
  { id: 'K22', q: '"adjoint" AND ("sensitivity" OR "gradient")' },
];

const FIELDS = ['id', 'doi', 'display_name', 'publication_year', 'publication_date', 'type',
  'cited_by_count', 'authorships', 'primary_location', 'language'].join(',');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function getJson(url, tries = 6) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url, { headers: { 'User-Agent': 'dsh-paper-discovery/1.0 (mailto:research@example.org)' } });
      if (r.status === 429 || r.status >= 500) { await sleep(4000 * (i + 1)); continue; }
      if (!r.ok) return { error: `HTTP ${r.status}` };
      return { json: await r.json() };
    } catch (e) {
      if (i === tries - 1) return { error: e.message };
      await sleep(3000 * (i + 1));
    }
  }
  return { error: 'retries exhausted' };
}

function buildUrl(q, issns) {
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

// load existing pool for merge
const existing = fs.existsSync(OUT)
  ? fs.readFileSync(OUT, 'utf8').trim().split('\n').filter(Boolean).map((l) => JSON.parse(l))
  : [];
const logPath = OUT.replace(/\.jsonl$/, '.log.json');
const log = fs.existsSync(logPath) ? JSON.parse(fs.readFileSync(logPath, 'utf8')) : [];
const done = new Set(log.filter((l) => l.status === '200').map((l) => `${l.theme}|${l.cluster}`));

let fetched = 0;
for (const [cKey, c] of Object.entries(CLUSTERS)) {
  for (const t of THEMES) {
    const key = `${t.id}|${cKey}`;
    if (done.has(key)) continue;
    const u = buildUrl(t.q, c.issns);
    const { json, error } = await getJson(u);
    if (error) {
      log.push({ theme: t.id, cluster: cKey, q: t.q, url: u, status: error, hits: null, exported: 0 });
      console.error(`[${key}] FAIL ${error}`);
    } else {
      const res = json.results || [];
      for (const r of res) {
        const src = (r.primary_location && r.primary_location.source) || {};
        existing.push({
          openalex_id: (r.id || '').replace('https://openalex.org/', ''),
          doi: r.doi ? r.doi.replace('https://doi.org/', '').toLowerCase() : null,
          title: r.display_name || '', year: r.publication_year, date: r.publication_date,
          venue: src.display_name || null, issn_l: src.issn_l || null, type: r.type,
          cited_by: r.cited_by_count,
          authors: (r.authorships || []).slice(0, 10).map((a) => (a.author && a.author.display_name) || ''),
          n_authors: (r.authorships || []).length,
          theme_ids: [t.id], cluster: cKey,
        });
      }
      log.push({ theme: t.id, cluster: cKey, q: t.q, url: u, status: '200', hits: json.meta && json.meta.count, exported: res.length });
      console.error(`[${key}] hits=${(json.meta && json.meta.count) || 0} exported=${res.length}`);
      fetched++;
    }
    await sleep(GAP);
  }
}

const byKey = new Map();
let merged = 0;
for (const r of existing) {
  const k = r.doi || r.openalex_id;
  if (byKey.has(k)) {
    const p = byKey.get(k);
    for (const t of r.theme_ids) if (!p.theme_ids.includes(t)) p.theme_ids.push(t);
    merged++;
  } else byKey.set(k, r);
}
const all = [...byKey.values()].sort((a, b) => (b.cited_by || 0) - (a.cited_by || 0));
fs.writeFileSync(OUT, all.map((r) => JSON.stringify(r)).join('\n') + '\n', 'utf8');
fs.writeFileSync(logPath, JSON.stringify(log, null, 2), 'utf8');
console.error(`\nfetched_this_run=${fetched} before_dedup=${existing.length} after_dedup=${all.length} merged=${merged}`);
