// repair_library.mjs — final, correct merge.
// Rule: P1 顶刊清单的 68 行是主记录（primary）；旧引用库只做"附加证据"，绝不替换主记录。
import fs from 'node:fs';
const LIB = 'library/P1-library.jsonl';
const finalJsonl = fs.readFileSync('final_list.jsonl', 'utf8').trim().split('\n').filter(Boolean).map((l) => JSON.parse(l));
const current = fs.readFileSync(LIB, 'utf8').trim().split('\n').filter(Boolean).map((l) => JSON.parse(l));

const STOP = new Set(['a', 'an', 'the', 'of', 'for', 'and', 'in', 'on', 'to', 'with', 'via', 'using', 'from', 'by', 'at', 'is', 'are', 'as', 'into', 'its', 'their']);
const toks = (s) => [...new Set((s || '').toLowerCase().replace(/[^a-z0-9\s]/g, ' ').split(/\s+/).filter((w) => w.length > 2 && !STOP.has(w)))];
const jac = (a, b) => { const A = new Set(toks(a)), B = new Set(toks(b)); if (!A.size || !B.size) return 0; let i = 0; for (const x of A) if (B.has(x)) i++; return i / (A.size + B.size - i); };

// 1) primary records = the 68 P1 rows (rebuilt from final_list.jsonl, keeping project fields)
const primaries = finalJsonl.map((p) => ({
  id: `p1:${p.n}`,
  n_p1: p.n,
  doi: p.doi || null,
  arxiv: p.doi && p.doi.startsWith('10.48550/arXiv.') ? p.doi.replace('10.48550/arXiv.', '') : null,
  title: p.title, authors: p.authors, year: p.year, venue: p.venue,
  volume: p.volume, issue: p.issue, page: p.page, url: p.url,
  crossref_cited_by: p.crossref_cited_by,
  sources: ['literature/final_list.jsonl (Crossref+arXiv 核验 2026-10-02)'],
  verification: p.verification, project_refs: [`literature/final_list.jsonl#${p.n}`],
  groups: p.group ? [p.group] : [], why: p.why || null, status: 'candidate',
}));

// 2) old-library-only records = current entries that are NOT a P1 primary and NOT matched by a primary
const oldRecords = current.filter((r) => !r.n_p1);
const kept = [];
const attachLog = [];
for (const o of oldRecords) {
  let best = null, bj = 0;
  for (const p of primaries) { const j = jac(o.title, p.title); if (j > bj) { bj = j; best = p; } }
  const doiHit = o.doi ? primaries.find((p) => p.doi && p.doi === o.doi) : null;
  const target = doiHit || (bj >= 0.7 ? best : null);
  if (target) {
    target.sources.push(...o.sources.filter((s) => !target.sources.includes(s)));
    target.project_refs.push(...(o.project_refs || []).filter((s) => !target.project_refs.includes(s)));
    target.old_citation = o.citation || o.title;
    target.old_note = o.note || null;
    target.groups = [...new Set([...(target.groups || []), ...(o.groups || [])])];
    attachLog.push({ src_id: o.src_id, into_n: target.n_p1, into: target.title, how: doiHit ? 'doi' : `title j=${bj.toFixed(3)}` });
  } else {
    kept.push(o);
    attachLog.push({ src_id: o.src_id, into_n: null, into: o.title, how: `kept (best j=${bj.toFixed(3)})` });
  }
}

const out = [...primaries, ...kept];
fs.writeFileSync(LIB, out.map((r) => JSON.stringify(r)).join('\n') + '\n', 'utf8');
fs.writeFileSync('library/attach-log.json', JSON.stringify(attachLog, null, 2), 'utf8');

const ids = out.map((r) => r.id);
console.log(`primaries=${primaries.length} old_kept=${kept.length} total=${out.length} dup_ids=${ids.filter((x, i) => ids.indexOf(x) !== i).length}`);
console.log(`attached_to_primary=${attachLog.filter((a) => a.into_n).length}`);
console.log('P1 nums present:', primaries.length === 68 ? 'all 68 ✓' : 'MISSING: ' + finalJsonl.map((p) => p.n).filter((n) => !primaries.some((p) => p.n_p1 === n)));
console.log('\nattached pairs:');
for (const a of attachLog.filter((x) => x.into_n)) console.log(`  ${a.src_id || '(old)'} -> #${a.into_n} ${String(a.into).slice(0, 58)} [${a.how}]`);
console.log('\nold-only kept:');
for (const a of attachLog.filter((x) => !x.into_n)) console.log(`  ${a.src_id || '(old)'} | ${String(a.into).slice(0, 66)}`);
