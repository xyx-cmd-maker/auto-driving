// build_library.mjs — final consolidated library builder (P1 primary rows + old verified list attached).
// Inputs : literature/final_list.jsonl                (75 rows, Crossref/arXiv-verified, n 1..53 & 101..125)
//          auto-driving/sources/references-list-verified.txt (35 parsed entries, project-audited)
// Outputs: literature/library/P1-library.jsonl | P1-library.md | merge-report.md
import fs from 'node:fs';
import path from 'node:path';

const LIT = path.resolve('.');
const ROOT = path.resolve('..');
const LIB = path.join(LIT, 'library');
fs.mkdirSync(LIB, { recursive: true });

const finalRows = fs.readFileSync(path.join(LIT, 'final_list.jsonl'), 'utf8').trim().split('\n').filter(Boolean).map((l) => JSON.parse(l));
const verifiedTxt = fs.readFileSync(path.join(ROOT, 'sources', 'references-list-verified.txt'), 'utf8');

// ---------- parse the project-verified list ----------
const cleanMd = (s) => (s || '').replace(/\*\*/g, '').replace(/`/g, '').replace(/\[([^\]]+)\]\([^)]+\)/g, '$1').replace(/\s+/g, ' ').trim();
function extractTitle(citRaw) {
  let s = (citRaw || '').replace(/\*\*/g, '').replace(/`/g, '').trim();
  s = s.replace(/^（[^）]*）\s*/, '').replace(/^\[[^\]]*\]\s*/, '');
  const cut = s.search(/\*\s|\*[A-Z]|\bProc\.|\bIn:\s|\bIEEE\b|\bAdvances in\b|\barXiv:|\bDOI\b|\bComputer Vision –|\bFirst Conference\b|\bNature\b|\bPhysical Review\b/);
  let head = cut > 0 ? s.slice(0, cut) : s;
  head = head.replace(/\*+$/, '').trim();
  const m = head.match(/^(.{0,400}?\.)\s*([A-Z0-9(\[].*)$/);
  if (m && m[2] && m[2].replace(/[^A-Za-z]/g, '').length > 12) head = m[2];
  return head.replace(/\s*\*\s*$/, '').replace(/\.$/, '').trim();
}
const lines = verifiedTxt.split(/\r?\n/);
const parsed = [];
let cur = null, group = '(核心锚点)';
for (const ln of lines) {
  const g = ln.match(/^##\s+(.+)$/);
  if (g) { group = g[1].trim(); continue; }
  const start = ln.match(/^\*\*([A-F]\d+|A\d)\s+(✅|🔶|📄|🔧)\s*(.*)$/);
  if (start) { if (cur) parsed.push(cur); cur = { src_id: start[1], mark: start[2], group, head: start[3].trim(), bullets: [] }; continue; }
  if (cur && /^-\s+/.test(ln)) cur.bullets.push(ln.replace(/^-\s+/, '').trim());
}
if (cur) parsed.push(cur);

// ---------- helpers (declared before use) ----------
const STOP = new Set(['a', 'an', 'the', 'of', 'for', 'and', 'in', 'on', 'to', 'with', 'via', 'using', 'from', 'by', 'at', 'is', 'are', 'as', 'into', 'its', 'their']);
const toks = (s) => [...new Set((s || '').toLowerCase().replace(/[^a-z0-9\s]/g, ' ').split(/\s+/).filter((w) => w.length > 2 && !STOP.has(w)))];
const jac = (a, b) => { const A = new Set(toks(a)), B = new Set(toks(b)); if (!A.size || !B.size) return 0; let i = 0; for (const x of A) if (B.has(x)) i++; return i / (A.size + B.size - i); };
const titleToks = (s) => toks(s).filter((w) => !(w.length <= 3 && /^[a-z]+$/.test(w)) && !/^\d+$/.test(w));
const jacTitle = (a, b) => {
  const A = new Set(titleToks(a)), B = new Set(titleToks(b));
  if (!A.size || !B.size) return 0;
  let i = 0; for (const x of A) if (B.has(x)) i++;
  return i / (A.size + B.size - i);
};
// Containment fallback: the old list's "title" often still carries a leading author list,
// so check whether the clean title occurs *inside* the noisy one.
const normChars = (s) => (s || '').toLowerCase().replace(/[^a-z0-9]+/g, '');
const containsTitle = (noisy, clean) => {
  const N = normChars(noisy), C = normChars(clean);
  if (!N || !C) return 0;
  return N.includes(C) ? C.length / N.length : 0;
};
const matchScore = (noisy, clean) => Math.max(jacTitle(noisy, clean), containsTitle(noisy, clean));
// Split glued DOI + CJK text, e.g. "10.23919/ECC.2019.8796030）｜arXiv" -> "10.23919/ecc.2019.8796030"
const cleanDoi = (d) => (d || '').split(/[^\x20-\x7E]/)[0].replace(/[.,;)\]}]+$/, '').toLowerCase();

const old = parsed.map((e) => {
  const citation = cleanMd(e.head);
  const allDois = [...(e.bullets.join(' ') + ' ' + e.head).matchAll(/10\.[0-9]{4,9}\/[^\s\]|]+/g)]
    .map((m) => cleanDoi(m[0])).filter(Boolean);
  const yearM = (e.bullets.join(' ') + ' ' + e.head).match(/\b(19|20)\d{2}\b/);
  return {
    src_id: e.src_id, mark: e.mark, group: e.group, citation,
    title: extractTitle(citation), dois: [...new Set(allDois)], doi: allDois[0] || null,
    year: yearM ? Number(yearM[0]) : null,
    links: [...e.bullets.join(' ').matchAll(/\[([^\]]+)\]\((https?:[^)]+)\)/g)].map((m) => m.url),
    note: e.bullets.map(cleanMd).join(' | '),
  };
});

// ---------- primaries ----------
// ---------- primaries ----------

const primaries = finalRows.map((p) => ({
  id: `p1:${p.n}`, n_p1: p.n, doi: p.doi || null,
  arxiv: p.doi && p.doi.startsWith('10.48550/arXiv.') ? p.doi.replace('10.48550/arXiv.', '') : null,
  title: p.title, authors: p.authors, year: p.year, venue: p.venue,
  volume: p.volume, issue: p.issue, page: p.page, url: p.url,
  cited_by_crossref: p.crossref_cited_by,
  group_p1: p.group, why_p1: p.why,
  verification: p.verification, note_verification: p.year_note || null,
  sources: ['literature/final_list.jsonl (Crossref/arXiv 逐条核验, 2026-10-02)'],
  project_refs: [`literature/final_list.jsonl#${p.n}`],
  status: 'candidate',
}));

// ---------- attach old records ----------
// Curated cross-list links that string matching alone cannot prove (verified by the reader, 2026-10-02):
//   F5 (nuScenes, CVF pages 11621–11631) == P1 #114 (nuScenes, IEEE pages 11618–11628): same paper, two page ranges
//   E1 (CBF tutorial, ECC 2019)          == P1 #111: identical paper; the old row's DOI was glued to CJK text
const CURATED = { F5: 114, E1: 111 };
const kept = [];
const attach = [];
for (const o of old) {
  let best = null, bj = 0;
  for (const p of primaries) { const j = matchScore(o.title, p.title); if (j > bj) { bj = j; best = p; } }
  const doiHit = o.dois && o.dois.length ? primaries.find((p) => p.doi && o.dois.includes(p.doi)) : null;
  const curatedHit = CURATED[o.src_id] ? primaries.find((p) => p.n_p1 === CURATED[o.src_id]) : null;
  const target = doiHit || curatedHit || (bj >= 0.7 ? best : null);
  if (target) {
    target.sources = [...new Set([...target.sources, `sources/references-list-verified.txt#${o.src_id} (${o.mark})`])];
    target.project_refs = [...new Set([...target.project_refs, `sources/references-list-verified.txt#${o.src_id}`])];
    target.old_citation = o.citation;
    target.old_note = o.note || null;
    attach.push({ src_id: o.src_id, into_n: target.n_p1, into: target.title, how: doiHit ? 'doi' : curatedHit ? 'curated-cross-list' : `title j=${bj.toFixed(3)}` });
  } else {
    kept.push({
      id: `old:${o.src_id}`, n_p1: null, doi: o.doi, arxiv: (o.links.find((u) => /arxiv\.org/.test(u)) || null),
      title: o.title || o.citation.slice(0, 80), authors: [], year: o.year, venue: null,
      url: o.links[0] || (o.doi ? `https://doi.org/${o.doi}` : null),
      cited_by_crossref: null, group_p1: null, why_p1: null,
      verification: { source: 'project audit/05-citations.md', verdict: o.mark },
      note_verification: null,
      sources: [`sources/references-list-verified.txt#${o.src_id} (${o.mark})`],
      project_refs: [`sources/references-list-verified.txt#${o.src_id}`],
      status: 'candidate', citation: o.citation, old_note: o.note || null,
    });
    attach.push({ src_id: o.src_id, into_n: null, into: o.title, how: `kept as old-only (best j=${bj.toFixed(3)})` });
  }
}

const library = [...primaries, ...kept];
fs.writeFileSync(path.join(LIB, 'P1-library.jsonl'), library.map((r) => JSON.stringify(r)).join('\n') + '\n', 'utf8');
fs.writeFileSync(path.join(LIB, 'attach-log.json'), JSON.stringify(attach, null, 2), 'utf8');

// ---------- human-readable views ----------
const GNAME = { A: 'A 连续时间/流体神经网络', B: 'B 决策基线 RL', C: 'C 安全层 CBF/验证', D: 'D 跟驰-编队-混行', E: 'E 预测/规划/世界模型', F: 'F 结构保持学习', X: 'X 附录：奠基会议与经典' };
let md = `# P1 候选引用库（唯一来源）\n\n> 生成 2026-10-02 ｜ 条目 **${library.length}**＝P1 顶刊清单 ${primaries.length} 条（主记录）＋ 旧引用库独有 ${kept.length} 条\n> 合并自：\`literature/final_list.jsonl\`（Crossref/arXiv 逐条核验）＋ \`sources/references-list-verified.txt\`（项目审计已核验）\n> **规则：任何一条修正只改本文件**；\`project_refs\` 字段给出可追溯的文件与编号。\n\n## A. 主记录（P1 清单，n=1–53 与 101–125）\n\n| n | 组 | 标题 | 年 | 期刊/会议 | 卷(期):页 | 链接 | 被引 | 来源数 |\n|---|---|---|---|---|---|---|---|---|\n`;
for (const r of primaries.sort((a, b) => a.n_p1 - b.n_p1)) {
  md += `| ${r.n_p1} | ${r.group_p1 || ''} | ${(r.title || '').replace(/\|/g, '\\|')} | ${r.year || '—'} | ${(r.venue || '').replace(/\|/g, '\\|')} | ${r.volume ? r.volume : '—'}${r.issue ? `(${r.issue})` : ''}:${r.page || '—'} | ${r.url ? `[${r.doi || 'link'}](${r.url})` : '⚠ 无可解析标识'} | ${r.cited_by_crossref ?? '—'} | ${r.sources.length} |\n`;
}
md += `\n## B. 旧引用库独有（P1 清单未含；供 P2–P5 使用）\n\n| 旧库编号 | 标题 | 年 | DOI / 链接 |\n|---|---|---|---|\n`;
for (const r of kept) md += `| ${r.id.replace('old:', '')} | ${(r.title || '').replace(/\|/g, '\\|')} | ${r.year || '—'} | ${r.url ? `[${r.doi || 'link'}](${r.url})` : '—'} |\n`;
fs.writeFileSync(path.join(LIB, 'P1-library.md'), md, 'utf8');

let rep = `# 合表报告：P1 顶刊清单 × 项目引用库\n\n生成：2026-10-02\n\n## 一、计数（可复核）\n\n| 项 | 数 |\n|---|---|\n| P1 顶刊清单输入行（final_list.jsonl） | ${finalRows.length} |\n| 旧引用库输入条目（references-list-verified.txt） | ${old.length} |\n| **合并后唯一记录** | **${library.length}** |\n| ↳ P1 主记录 | ${primaries.length} |\n| ↳ 旧库独有（P2–P5 用） | ${kept.length} |\n| ↳ 两份清单都收录 → 已去重并入主记录 | ${attach.filter((a) => a.into_n).length} |\n\n## 二、两份清单都收录（去重明细）\n\n| 旧库编号 | 合入 P1 编号 | 标题 | 匹配方式 |\n|---|---|---|---|\n`;
for (const a of attach.filter((x) => x.into_n)) rep += `| ${a.src_id} | #${a.into_n} | ${(a.into || '').replace(/\|/g, '\\|')} | ${a.how} |\n`;
rep += `\n## 三、旧库独有（保留）\n\n| 旧库编号 | 标题 | 匹配到的最近 P1 条目相似度 |\n|---|---|---|\n`;
for (const a of attach.filter((x) => !x.into_n)) rep += `| ${a.src_id} | ${(a.into || '').replace(/\|/g, '\\|')} | ${a.how.replace('kept as old-only ', '')} |\n`;
rep += `\n## 四、已知口径问题（写入稿件前必须处理）\n\n1. 旧库条目的题名/年份为**解析结果**（原文是整串引文），个别条目（如 ISO 26262-1、torchdiffeq）不是论文，已按原样保留并标 mark。\n2. \`refs.bib\` 与 \`P1-library.jsonl\` 中的 P1 主记录字段一律来自 Crossref；Crossref 未注册的 4 条（#101/#104/#115/#120）与 1 条 DOI 指向他文的（#105）已显式标注，**不得直接引用其 DOI**。\n3. 被引数为 Crossref 口径快照（2026-10-02），与 OpenAlex/Google Scholar 不可比。\n`;
fs.writeFileSync(path.join(LIB, 'merge-report.md'), rep, 'utf8');

console.log(`primaries=${primaries.length} old_parsed=${old.length} attached=${attach.filter((a) => a.into_n).length} old_only=${kept.length} library_total=${library.length}`);
