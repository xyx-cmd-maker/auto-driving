// Targeted novelty search: is there any work using a force/potential/social field
// as the *conditioning modality* of a (driving) world model / generative model?
// Channels: OpenAlex search (abstract-level), arXiv API.
const MAILTO = "research@example.org";

const OA_QUERIES = [
  { id: "N1", q: `"social force" AND ("world model" OR "generative" OR diffusion)` },
  { id: "N2", q: `"potential field" AND ("world model" OR condition AND generation) AND driving` },
  { id: "N3", q: `"social force model" AND (conditioning OR "conditional" OR "as input")` },
  { id: "N4", q: `("force field" OR "potential field" OR "interaction field") AND ("scene generation" OR "trajectory generation" OR "world model")` },
  { id: "N5", q: `"social pressure" AND traffic AND (field OR model)` },
  { id: "N6", q: `"driving world model" AND (condition OR conditional OR controllable)` },
  { id: "N7", q: `"social value orientation" AND ("diffusion model" OR "world model")` },
  { id: "N8", q: `"repulsive force" AND ("diffusion" OR "generative model") AND (pedestrian OR vehicle OR traffic)` },
];

const ARXIV_QUERIES = [
  { id: "A1", q: `all:"social force" AND all:"world model"` },
  { id: "A2", q: `all:"social force" AND all:"diffusion model"` },
  { id: "A3", q: `all:"potential field" AND all:"driving world model"` },
  { id: "A4", q: `all:"interaction field" AND all:"trajectory"` },
  { id: "A5", q: `abs:"force field" AND abs:"scene generation"` },
  { id: "A6", q: `all:"social pressure field"` },
  { id: "A7", q: `all:"driving world model" AND all:"condition"` },
  { id: "A8", q: `all:"social force" AND all:"conditional"` },
];

function invert(idx) {
  if (!idx) return null;
  const arr = [];
  for (const [w, poss] of Object.entries(idx)) for (const p of poss) arr[p] = w;
  return arr.filter(Boolean).join(" ");
}

async function get(url) {
  const r = await fetch(url, { headers: { "User-Agent": `novelty-check/1.0 (mailto:${MAILTO})` } });
  return { status: r.status, text: r.status === 200 ? await r.text() : "" };
}

const results = { openalex: [], arxiv: [] };

for (const { id, q } of OA_QUERIES) {
  const url =
    `https://api.openalex.org/works?search=${encodeURIComponent(q)}` +
    `&filter=from_publication_date:2019-01-01&sort=relevance_score:desc&per-page=25` +
    `&select=id,doi,display_name,publication_year,type,cited_by_count,primary_location,abstract_inverted_index` +
    `&mailto=${MAILTO}`;
  const { status, text } = await get(url);
  if (status !== 200) {
    results.openalex.push({ id, q, status, error: true });
    continue;
  }
  const j = JSON.parse(text);
  results.openalex.push({
    id,
    q,
    status,
    count: j.meta?.count,
    items: (j.results ?? []).map((w) => ({
      doi: w.doi,
      title: w.display_name,
      year: w.publication_year,
      venue: w.primary_location?.source?.display_name ?? null,
      cited: w.cited_by_count,
      abs: (invert(w.abstract_inverted_index) ?? "").slice(0, 700),
    })),
  });
  process.stderr.write(`OA ${id} count=${j.meta?.count}\n`);
}

for (const { id, q } of ARXIV_QUERIES) {
  const url = `http://export.arxiv.org/api/query?search_query=${encodeURIComponent(q)}&start=0&max_results=15&sortBy=relevance`;
  const { status, text } = await get(url);
  const entries = [...text.matchAll(/<entry>([\s\S]*?)<\/entry>/g)].map((m) => {
    const e = m[1];
    const pick = (tag) => (e.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`)) ?? [])[1]?.replace(/\s+/g, " ").trim();
    return {
      id: pick("id"),
      title: pick("title"),
      published: pick("published"),
      summary: (pick("summary") ?? "").slice(0, 700),
    };
  });
  results.arxiv.push({ id, q, status, count: entries.length, entries });
  process.stderr.write(`arXiv ${id} n=${entries.length}\n`);
}

const { writeFileSync } = await import("node:fs");
writeFileSync(new URL("./novelty_search.json", import.meta.url), JSON.stringify(results, null, 2), "utf8");
console.log("done");
