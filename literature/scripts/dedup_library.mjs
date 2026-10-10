// dedup_library.mjs — token-based dedup pass over the merged P1 library.
import fs from 'node:fs';
const P = 'library/P1-library.jsonl';
const rows = fs.readFileSync(P, 'utf8').trim().split('\n').map((l) => JSON.parse(l));
const STOP = new Set(['a', 'an', 'the', 'of', 'for', 'and', 'in', 'on', 'to', 'with', 'via', 'using', 'from', 'by', 'at', 'is', 'are', 'as', 'into', 'its', 'their']);
const toks = (s) => [...new Set((s || '').toLowerCase().replace(/[^a-z0-9\s]/g, ' ').split(/\s+/).filter((w) => w.length > 2 && !STOP.has(w)))];
const jac = (a, b) => { const A = new Set(toks(a)), B = new Set(toks(b)); if (!A.size || !B.size) return 0; let i = 0; for (const x of A) if (B.has(x)) i++; return i / (A.size + B.size - i); };

const p1 = rows.filter((r) => r.n_p1);
const old = rows.filter((r) => !r.n_p1);
const merged = [...p1];
const report = [];
for (const o of old) {
  let best = null, bj = 0;
  for (const p of merged) { const j = jac(o.title, p.title); if (j > bj) { bj = j; best = p; } }
  const doiHit = o.doi && merged.find((p) => p.doi && p.doi === o.doi);
  if (doiHit) {
    doiHit.sources = [...new Set([...doiHit.sources, ...o.sources])];
    doiHit.project_refs = [...new Set([...doiHit.project_refs, ...o.project_refs])];
    doiHit.groups = [...new Set([...(doiHit.groups || []), ...(o.groups || [])])];
    doiHit.old_citation = o.citation || o.title;
    doiHit.old_note = o.note || null;
    report.push({ kind: 'merge-doi', src_id: o.src_id, into: doiHit.title, j: 1 });
  } else if (best && bj >= 0.7) {
    best.sources = [...new Set([...best.sources, ...o.sources])];
    best.project_refs = [...new Set([...best.project_refs, ...o.project_refs])];
    best.groups = [...new Set([...(best.groups || []), ...(o.groups || [])])];
    best.old_citation = o.citation || o.title;
    best.old_note = o.note || null;
    report.push({ kind: 'merge-title', src_id: o.src_id, into: best.title, j: Number(bj.toFixed(3)) });
  } else {
    merged.push(o);
    report.push({ kind: 'keep-old', src_id: o.src_id, title: o.title, j: Number(bj.toFixed(3)) });
  }
}
const byId = new Map();
for (const r of merged) {
  const k = r.n_p1 ? `p1:${r.n_p1}` : r.id;
  if (!byId.has(k)) byId.set(k, r);
}
const out = [...byId.values()];
fs.writeFileSync(P, out.map((r) => JSON.stringify(r)).join('\n') + '\n', 'utf8');
fs.writeFileSync('library/dedup-report.json', JSON.stringify(report, null, 2), 'utf8');
console.log(`before=${rows.length} after=${out.length} merged_doi=${report.filter((r) => r.kind === 'merge-doi').length} merged_title=${report.filter((r) => r.kind === 'merge-title').length} old_only=${report.filter((r) => r.kind === 'keep-old').length}`);
console.log('\n--- merged ---');
for (const r of report.filter((x) => x.kind !== 'keep-old')) console.log(`  ${r.src_id} -> ${String(r.into).slice(0, 62)} (j=${r.j})`);
console.log('\n--- old-only kept ---');
for (const r of report.filter((x) => x.kind === 'keep-old')) console.log(`  ${r.src_id} | ${String(r.title).slice(0, 70)} (best j=${r.j})`);
