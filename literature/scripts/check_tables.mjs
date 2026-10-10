// 表格完整性检查：每个 markdown 表格块内各行的列数是否一致
import fs from 'node:fs';
for (const f of process.argv.slice(2)) {
  const lines = fs.readFileSync(f, 'utf8').split('\n');
  let i = 0, bad = 0, tables = 0;
  while (i < lines.length) {
    if (/^\s*\|/.test(lines[i])) {
      const start = i; const cols = [];
      while (i < lines.length && /^\s*\|/.test(lines[i])) {
        // 去掉行首行尾的 | 后按 | 切分（本文件表格内无转义竖线）
        const cells = lines[i].trim().replace(/^\|/, '').replace(/\|$/, '').split('|');
        cols.push(cells.length); i++;
      }
      tables++;
      const uniq = [...new Set(cols)];
      const ok = uniq.length === 1;
      if (!ok) { bad++; console.log(`  [列数不一致] ${f.split('/').pop()} 第 ${start + 1}–${i} 行, 列数集合 = ${uniq.join(',')}`); }
    } else i++;
  }
  console.log(`${f.split('/').pop()}: 表格块 ${tables} 个, 列数不一致 ${bad} 个`);
}
