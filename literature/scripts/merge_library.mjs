// merge_library.mjs — build the P1 candidate citation library from
//   (a) sources/references-list-verified.txt  (30 items, project-verified, 5 groups)
//   (b) literature/final_list.jsonl           (68 items, Crossref-verified)
// Output: literature/library/P1-library.jsonl  +  P1-library.md  + merge-report.md
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve('..');                     // auto-driving/
const LIT = path.resolve('.');                       // auto-driving/literature/
const LIB = path.join(LIT, 'library');
fs.mkdirSync(LIB, { recursive: true });

const verifiedTxt = fs.readFileSync(path.join(ROOT, 'sources', 'references-list-verified.txt'), 'utf8');
const finalJsonl = fs.readFileSync(path.join(LIT, 'final_list.jsonl'), 'utf8').trim().split('\n').filter(Boolean).map((l) => JSON.parse(l));

// ---------- (a) parse references-list-verified.txt ----------
// Entries start with "**<ID> <mark> <Title-rest>" and continue with indented bullet lines.
const lines = verifiedTxt.split(/\r?\n/);
const entries = [];
let cur = null;
const groupRe = /^##\s+(.+)$/;
let group = '(核心锚点)';
for (const ln of lines) {
  const g = ln.match(groupRe);
  if (g) { group = g[1].trim(); continue; }
  const start = ln.match(/^\*\*([A-F]\d+|A\d)\s+(✅|🔶|📄|🔧)\s*(.*)$/);
  if (start) {
    if (cur) entries.push(cur);
    cur = { src_id: start[1], mark: start[2], group, head: start[3].trim(), bullets: [] };
    continue;
  }
  if (cur && /^-\s+/.test(ln)) cur.bullets.push(ln.replace(/^-\s+/, '').trim());
}
if (cur) entries.push(cur);

const cleanMd = (s) => (s || '')
  .replace(/\*\*/g, '').replace(/`/g, '').replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
  .replace(/\s+/g, ' ').trim();

// The old list stores full citation strings ("Authors. Title. *Venue* year;vol:pp").
// Extract the paper title so that dedup against the P1 list can work on titles.
function extractTitle(citRaw) {
  let s = (citRaw || '').replace(/\*\*/g, '').replace(/`/g, '').trim();
  s = s.replace(/^（[^）]*）\s*/, '');                       // leading Chinese parenthesis notes
  s = s.replace(/^\[[^\]]*\]\s*/, '');                       // leading bracket notes
  // cut at the first venue-ish marker
  const cut = s.search(/\*\s|\*[A-Z]|\bProc\.|\bIn:\s|\bIEEE\b|\bAdvances in\b|\barXiv:|\bDOI\b|\bComputer Vision –|\bFirst Conference\b|\bNature\b|\bPhysical Review\b/);
  let head = cut > 0 ? s.slice(0, cut) : s;
  head = head.replace(/\*+$/, '').trim();
  // drop a leading author list: find the sentence boundary that precedes the title
  const m = head.match(/^(.{0,400}?\.)\s*([A-Z0-9(\[].*)$/);
  if (m && m[2] && m[2].replace(/[^A-Za-z]/g, '').length > 12) head = m[2];
  return head.replace(/\s*\*\s*$/, '').replace(/\.$/, '').trim();
}

const parsed = entries.map((e) => {
  const citation = cleanMd(e.head);                      // "Authors. Title. Venue year;vol:pp"
  const title = extractTitle(citation);
  const yearM = (e.bullets.join(' ') + ' ' + e.head).match(/\b(19|20)\d{2}\b/);
  const doiM = e.bullets.join(' ').match(/10\.\d{4,9}\/[^\s)]+/);
  const doi = doiM ? doiM[0].replace(/[.,;]$/, '').toLowerCase() : null;
  const links = [...e.bullets.join(' ').matchAll(/\[([^\]]+)\]\((https?:[^)]+)\)/g)].map((m) => ({ label: m[1], url: m[2] }));
  return {
    src_id: e.src_id, mark: e.mark, group: e.group,
    head: citation, title, bullets: e.bullets.map(cleanMd),
    year: yearM ? Number(yearM[0]) : null, doi, links,
  };
});

// ---------- ids / keys ----------
const keyOf = (doi, title) => doi ? `doi:${doi}` : `title:${(title || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 70)}`;

const library = [];
const ledger = [];

for (const p of finalJsonl) {
  library.push({
    id: keyOf(p.doi && !p.doi.startsWith('10.48550/') ? p.doi : null, p.title),
    doi: p.doi || null,
    arxiv: p.doi && p.doi.startsWith('10.48550/arXiv.') ? p.doi.replace('10.48550/arXiv.', '') : null,
    title: p.title, authors: p.authors, year: p.year, venue: p.venue,
    volume: p.volume, issue: p.issue, page: p.page, url: p.url,
    crossref_cited_by: p.crossref_cited_by,
    sources: ['crossref+arXiv (2026-10-02 P1 顶刊清单)'],
    verification: p.verification,
    project_refs: [`literature/final_list.jsonl#${p.n}`],
    groups: p.group ? [p.group] : [],
    why: p.why || null,
    status: 'candidate',
    n_p1: p.n,
  });
  ledger.push({ action: 'add', n_p1: p.n, title: p.title, doi: p.doi, reason: 'P1 顶刊清单新增' });
}

for (const p of parsed) {
  const id = keyOf(p.doi, p.title);
  const norm = (s) => (s || '').toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 40);
  const exist = library.find((x) => (x.doi && p.doi && x.doi === p.doi) ||
    (x.title && p.title && norm(x.title) && norm(x.title) === norm(p.title)));
  if (exist) {
    exist.sources.push(`references-list-verified.txt (${p.src_id}, ${p.mark})`);
    exist.project_refs.push(`sources/references-list-verified.txt#${p.src_id}`);
    exist.verified_note = p.bullets.join(' | ');
    ledger.push({ action: 'merge', src_id: p.src_id, into: exist.title, doi: exist.doi, reason: '同一文献，两份清单都收录' });
  } else {
    library.push({
      id, doi: p.doi, arxiv: (p.links.find((l) => /arxiv\.org/.test(l.url)) || {}).url || null,
      title: p.title, citation: p.head, authors: [], year: p.year, venue: null,
      url: p.doi ? `https://doi.org/${p.doi}` : (p.links[0] ? p.links[0].url : null),
      crossref_cited_by: null,
      sources: [`references-list-verified.txt (${p.src_id}, ${p.mark})`],
      verification: { source: 'project-audit/05-citations.md', verdict: p.mark },
      project_refs: [`sources/references-list-verified.txt#${p.src_id}`],
      groups: [p.group],
      why: null, status: 'candidate', n_p1: null,
      note: p.bullets.join(' | '),
    });
    ledger.push({ action: 'keep', src_id: p.src_id, title: p.title, doi: p.doi, reason: '仅旧库收录（不在 P1 顶刊清单内）' });
  }
}

// dedup by id
const byId = new Map();
for (const r of library) {
  if (byId.has(r.id)) {
    const prev = byId.get(r.id);
    prev.sources = [...new Set([...prev.sources, ...r.sources])];
    prev.project_refs = [...new Set([...prev.project_refs, ...r.project_refs])];
    prev.groups = [...new Set([...(prev.groups || []), ...(r.groups || [])])];
  } else byId.set(r.id, r);
}
const out = [...byId.values()];

fs.writeFileSync(path.join(LIB, 'P1-library.jsonl'), out.map((r) => JSON.stringify(r)).join('\n') + '\n', 'utf8');

// markdown view
let md = `# P1 候选引用库（唯一来源）\n\n> 生成：2026-10-02 ｜ 条目 ${out.length} 条\n> 合并自：\`literature/final_list.jsonl\`（68，Crossref 逐条核验）＋ \`sources/references-list-verified.txt\`（30，项目审计已核验）\n> 规则：**任何一条修正只改本文件**；原两份来源保留作历史留存（见 \`merge-report.md\`）。\n> 每一行都可指回来源：\`project_refs\` 字段给出文件与编号/序号。\n\n| id | 标题 | 年 | 期刊/会议 | DOI / 链接 | 来源 | 分组 | 状态 |\n|---|---|---|---|---|---|---|---|\n`;
for (const r of out.sort((a, b) => (a.year || 0) - (b.year || 0))) {
  md += `| ${r.id} | ${(r.title || '').replace(/\|/g, '\\|')} | ${r.year || '—'} | ${(r.venue || '').replace(/\|/g, '\\|')} | ${r.url ? `[${r.doi || 'link'}](${r.url})` : '—'} | ${r.sources.length} | ${(r.groups || []).join('/')} | ${r.status} |\n`;
}
fs.writeFileSync(path.join(LIB, 'P1-library.md'), md, 'utf8');

// merge report
const merges = ledger.filter((l) => l.action === 'merge');
const adds = ledger.filter((l) => l.action === 'add');
const keeps = ledger.filter((l) => l.action === 'keep');
let rep = `# 合表报告（final_list.jsonl × references-list-verified.txt）\n\n生成：2026-10-02\n\n## 计数\n\n| 项 | 数 |\n|---|---|\n| P1 顶刊清单输入 | ${finalJsonl.length} |\n| 旧引用库输入（references-list-verified.txt 条目） | ${parsed.length} |\n| **合并后唯一条目** | **${out.length}** |\n| 其中：两份清单都收录（去重合并） | ${merges.length} |\n| 其中：仅 P1 顶刊清单（新增） | ${adds.length} |\n| 其中：仅旧库（保留待用） | ${keeps.length} |\n\n## 两份清单都收录的条目（已去重）\n\n| 旧库编号 | 标题 | DOI |\n|---|---|---|\n`;
for (const m of merges) rep += `| ${m.src_id} | ${(m.into || '').replace(/\|/g, '\\|')} | ${m.doi || '—'} |\n`;
rep += `\n## 仅旧库收录（P1 清单未含，保留在库中待 P2–P5 使用）\n\n| 旧库编号 | 标题 | DOI |\n|---|---|---|\n`;
for (const k of keeps) rep += `| ${k.src_id} | ${(k.title || '').replace(/\|/g, '\\|')} | ${k.doi || '—'} |\n`;
fs.writeFileSync(path.join(LIB, 'merge-report.md'), rep, 'utf8');

console.log(`parsed_old=${parsed.length} from_p1=${finalJsonl.length} merged_unique=${out.length} dedup_merges=${merges.length} new_only=${adds.length} old_only=${keeps.length}`);
