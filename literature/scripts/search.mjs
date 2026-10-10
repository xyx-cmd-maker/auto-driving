// paper-discovery probe: OpenAlex + Crossref, Node fetch only (no Invoke-WebRequest).
// Usage: node search.mjs [--out <path>] [--per-page N] [--only QID]
// Writes raw candidate records as JSONL. Does NOT filter/curate.

const MAILTO = 'research@example.org';
const OUT = process.argv.includes('--out')
  ? process.argv[process.argv.indexOf('--out') + 1]
  : 'candidates_raw.jsonl';
const PER_PAGE = process.argv.includes('--per-page')
  ? Number(process.argv[process.argv.indexOf('--per-page') + 1])
  : 25;
const ONLY = process.argv.includes('--only')
  ? process.argv[process.argv.indexOf('--only') + 1]
  : null;

// Thematic queries. T = theme id, q = OpenAlex search string, note = why it matters for P1 (OTF-CfC).
const QUERIES = [
  { id: 'T01', theme: 'LNN / continuous-time NN foundations',
    q: '"liquid neural network" OR "liquid time-constant" OR "liquid time constant"',
    note: 'P1 controller family origin' },
  { id: 'T02', theme: 'Neural ODE / continuous-depth',
    q: '"neural ordinary differential equation" OR "continuous-depth" OR "ODE network"',
    note: 'P1/P5 adjoint training theory' },
  { id: 'T03', theme: 'Adaptive ODE solvers / stiff dynamics',
    q: '"adaptive step size" OR "Dormand-Prince" OR "Dopri5" OR "stiff neural"',
    note: 'P1 Dopri5 ablation A3' },
  { id: 'T04', theme: 'LNN applied to robotics / UAV / driving control',
    q: '"liquid neural network" AND (robot OR drone OR UAV OR vehicle OR control)',
    note: 'P1 closest prior art' },
  { id: 'T05', theme: 'Car-following / platoon / string stability',
    q: '"car-following" OR "platoon" OR "string stability"',
    note: 'P1 ODD and evaluation protocol' },
  { id: 'T06', theme: 'Mixed traffic with automated vehicles',
    q: '"mixed traffic" AND (autonomous OR "connected automated" OR "automated vehicle")',
    note: 'P1 mixed-traffic narrative' },
  { id: 'T07', theme: 'Lane change / overtaking behaviour + social pressure',
    q: '"lane-changing" OR "overtaking" OR "lane change"',
    note: 'OTF construct external validity' },
  { id: 'T08', theme: 'Dynamics-aware / differentiable motion planning for AV',
    q: '"differentiable" AND (planning OR "motion planning") AND (driving OR vehicle OR autonomous)',
    note: 'P1 baseline vs MPC' },
  { id: 'T09', theme: 'RL for autonomous driving (TD3 baseline lineage)',
    q: '"deep reinforcement learning" AND ("autonomous driving" OR "autonomous vehicle")',
    note: 'Thesis TD3 baseline' },
  { id: 'T10', theme: 'Control barrier functions / safety filters',
    q: '"control barrier function"',
    note: 'P4 safety layer, P1 comparison' },
  { id: 'T11', theme: 'Real-time / embedded NN deployment on MCU',
    q: '"microcontroller" AND ("neural network" OR "deep learning") AND (deployment OR "real-time" OR embedded)',
    note: 'P1 Cortex-M7 <1ms claim' },
  { id: 'T12', theme: 'Model compression / quantization for embedded inference',
    q: '"model compression" OR "post-training quantization" OR "network pruning"',
    note: 'P1 <500KB parameter budget' },
  { id: 'T13', theme: 'Formal verification of neural network controllers',
    q: '"formal verification" AND ("neural network" OR "neural controller")',
    note: 'P4 isolation layer' },
  { id: 'T14', theme: 'Intelligent driver model / traffic flow stability',
    q: '"intelligent driver model" OR "traffic flow stability" OR "microscopic traffic flow"',
    note: 'P1 IDM disturbance model' },
  { id: 'T15', theme: 'Model predictive control for AV trajectory tracking',
    q: '"model predictive control" AND (vehicle OR driving OR autonomous)',
    note: 'P1 baseline 2' },
  { id: 'T16', theme: 'Physics-informed / structure-preserving learning for dynamics',
    q: '"physics-informed" OR "structure-preserving" OR "Hamiltonian neural network"',
    note: 'P1/P2 potential-field theory anchor' },
];

const FIELDS = [
  'id', 'doi', 'title', 'display_name', 'publication_year', 'publication_date',
  'type', 'cited_by_count', 'authorships', 'primary_location', 'language',
].join(',');

function openalexUrl(q) {
  const params = new URLSearchParams({
    search: q,
    filter: 'type:article,language:en',
    sort: 'cited_by_count:desc',
    'per-page': String(PER_PAGE),
    select: FIELDS,
    mailto: MAILTO,
  });
  return `https://api.openalex.org/works?${params.toString()}`;
}

async function getJson(url, tries = 3) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url, { headers: { 'User-Agent': 'dsh-paper-discovery/1.0 (mailto:research@example.org)' } });
      if (r.status === 429 || r.status >= 500) {
        await sleep(1500 * (i + 1));
        continue;
      }
      if (!r.ok) return { error: `HTTP ${r.status}` };
      return { json: await r.json() };
    } catch (e) {
      await sleep(1000 * (i + 1));
      if (i === tries - 1) return { error: e.message };
    }
  }
  return { error: 'exhausted retries' };
}

const sleep = (ms) => new Promise((res) => setTimeout(res, ms));

function norm(rec, qid, theme) {
  const loc = rec.primary_location || {};
  const src = loc.source || {};
  return {
    openalex_id: (rec.id || '').replace('https://openalex.org/', ''),
    doi: rec.doi ? rec.doi.replace('https://doi.org/', '').toLowerCase() : null,
    title: rec.display_name || rec.title || '',
    year: rec.publication_year,
    date: rec.publication_date,
    venue: src.display_name || null,
    venue_type: src.type || null,
    issn_l: src.issn_l || null,
    type: rec.type,
    cited_by: rec.cited_by_count,
    authors: (rec.authorships || []).slice(0, 12).map((a) => (a.author && a.author.display_name) || ''),
    n_authors: (rec.authorships || []).length,
    query_ids: [qid],
    theme,
  };
}

const results = [];
const log = [];
const targets = ONLY ? QUERIES.filter((q) => q.id === ONLY) : QUERIES;

for (const t of targets) {
  const url = openalexUrl(t.q);
  const { json, error } = await getJson(url);
  if (error) {
    log.push({ qid: t.id, theme: t.theme, q: t.q, url, status: error, hits: null, exported: 0 });
    console.error(`[${t.id}] FAIL ${error}`);
    await sleep(600);
    continue;
  }
  const recs = (json.results || []).map((r) => norm(r, t.id, t.theme));
  results.push(...recs);
  log.push({ qid: t.id, theme: t.theme, q: t.q, url, status: '200', hits: json.meta && json.meta.count, exported: recs.length });
  console.error(`[${t.id}] hits=${json.meta && json.meta.count} exported=${recs.length}`);
  await sleep(600);
}

// de-dup within this run: DOI (lowercased) > openalex_id
const byKey = new Map();
let merged = 0;
for (const r of results) {
  const key = r.doi || r.openalex_id;
  if (byKey.has(key)) {
    const prev = byKey.get(key);
    for (const q of r.query_ids) if (!prev.query_ids.includes(q)) prev.query_ids.push(q);
    merged++;
  } else {
    byKey.set(key, r);
  }
}

const fs = await import('node:fs');
const lines = [...byKey.values()].map((r) => JSON.stringify(r));
fs.writeFileSync(OUT, lines.join('\n') + '\n', 'utf8');
fs.writeFileSync(OUT.replace(/\.jsonl$/, '.log.json'), JSON.stringify(log, null, 2), 'utf8');
console.error(`\nbefore_dedup=${results.length} after_dedup=${byKey.size} merged_pairs=${merged}`);
console.error(`wrote ${OUT}`);
