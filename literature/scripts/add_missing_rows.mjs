// add_missing_rows.mjs — append the 7 incorrectly-dropped appendix rows into final_list.json,
// using the Crossref/arXiv-verified metadata already in dois_appendix_checked.json.
import fs from 'node:fs';
const APPX = 'dois_appendix_checked.json';
const rows = JSON.parse(fs.readFileSync('final_list.json', 'utf8'));
const have = new Set(rows.map((r) => r.n));
const B = JSON.parse(fs.readFileSync(APPX, 'utf8'));

const CUR = {
  102: 'LNN 原始论文（CfC 的前身），AAAI 2021 正式版；P1 控制器谱系的必引起点',
  103: 'NCP 可审计自主性；P1 的"小参数 + 可审计"论据。⚠ 项目原清单所附 arXiv:2003.08554 指向另一篇论文，不得附 arXiv 链接',
  106: 'IDM 的原始出处（PRE 2000）；P1 用 IDM 模拟前车加减速扰动的参数与方程来源',
  107: 'Gipps 跟驰模型（TR-B 1981）；安全距离型跟驰基线的经典参照',
  108: 'FVD 全速度差模型（PRE 2001）；跟驰模型谱系补全，用于说明 OTF 之外的既有"压力式"建模传统',
  115: 'CARLA 开源城市驾驶仿真器（CoRL 2017, PMLR 78:1–16）；P1/P2 的仿真平台（arXiv comments 已注明发表于 CoRL）',
  120: 'TransFuser（TPAMI 2023）：端到端传感器融合模仿学习对照。⚠ 本次核验未在 Crossref 取得该 DOI（10.1109/TPAMI.2022.3200242 返回未注册）→ 引用前必须复核，暂标 [待核实]',
};
const GROUP = { 102: 'X', 103: 'X', 106: 'X', 107: 'X', 108: 'X', 115: 'X', 120: 'X' };

for (const n of [102, 103, 106, 107, 108, 115, 120]) {
  if (have.has(n)) { console.log(`#${n} already present, skipped`); continue; }
  const b = B.find((r) => r.n === n);
  if (!b) { console.log(`#${n} NOT in appendix verification file`); continue; }
  const c = b.check || {};
  const conf = /Conference|Symposium|Proceedings|Lecture Notes/i.test(c.venue || '');
  rows.push({
    n, group: GROUP[n], why: CUR[n], key: b.key,
    crossref_title: c.title || b.claim.title,
    year_crossref: c.year || b.claim.year,
    year_note: null,
    venue: c.venue || b.claim.venue,
    short_venue: c.short_venue || null,
    volume: c.volume || null, issue: c.issue || null, page: c.page || null,
    authors: c.authors || [],
    publisher: c.publisher || null,
    doi: b.doi,
    url: b.doi.startsWith('10.48550/') ? `https://arxiv.org/abs/${b.doi.replace('10.48550/arXiv.', '')}` : `https://doi.org/${b.doi}`,
    crossref_cited_by: c.crossref_cited_by ?? null,
    verdict: c.verdict || (c.exists === false ? 'NOT-REGISTERED' : 'ARXIV-ONLY'),
    jaccard: c.jaccard_vs_claim ?? null,
    is_journal: !conf,
  });
  console.log(`added #${n} ${b.key} | ${c.title || b.claim.title} | ${b.doi} | verdict=${c.verdict || 'n/a'}`);
}
rows.sort((a, b) => a.n - b.n);
fs.writeFileSync('final_list.json', JSON.stringify(rows, null, 2), 'utf8');
console.log(`\nfinal_list.json now has ${rows.length} rows: ${rows.map((r) => r.n).join(',')}`);
