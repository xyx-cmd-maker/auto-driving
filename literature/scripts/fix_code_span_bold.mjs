// 检出/修复：行内 code span 内含 ** 的情况（在 code span 内 ** 会被原样渲染）
import fs from 'node:fs';
const files = [
  'D:/Deepseek Harness/auto-driving/literature/fresh2024/notes/arxiv2025-platoon-risk-potential-field.md',
  'D:/Deepseek Harness/auto-driving/literature/fresh2024/notes/arxiv2026-lnn-edge-compression.md',
];
const APPLY = process.argv.includes('--apply');
for (const f of files) {
  const t = fs.readFileSync(f, 'utf8');
  const re = /`[^`\n]*`/g;
  const hits = [];
  const out = t.replace(re, (m) => {
    if (!m.includes('**')) return m;
    hits.push(m);
    return m.replace(/\*\*/g, '');
  });
  console.log(`\n== ${f.split('/').pop()} : ${hits.length} 个 code span 内含 ** ==`);
  for (const h of hits) console.log('   ' + h.slice(0, 160));
  if (APPLY && hits.length) { fs.writeFileSync(f, out, 'utf8'); console.log('   -> 已修复'); }
  else if (hits.length) console.log('   -> 干跑，未写入（加 --apply 执行）');
}
