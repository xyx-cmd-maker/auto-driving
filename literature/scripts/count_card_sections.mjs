// 字数实测：抽出 §2 摘要 / §3 结论 / §4 方法一句话，按"去除空白后的字符数"与"中日韩字符数"两种口径计数
const fs = await import('node:fs');
const files = process.argv.slice(2);
for (const f of files) {
  const t = fs.readFileSync(f, 'utf8');
  const pick = (startRe, endRe) => {
    const s = t.search(startRe); if (s < 0) return null;
    const rest = t.slice(s);
    const lineEnd = rest.indexOf('\n');
    const body = rest.slice(lineEnd + 1);
    const e = body.search(endRe);
    return (e < 0 ? body : body.slice(0, e)).trim();
  };
  const secs = {
    '§2 摘要(<=400)': pick(/^## 2\. 摘要/m, /^---\s*$/m),
    '§3 结论(<=350)': pick(/^## 3\. 结论/m, /^---\s*$/m),
    '§4 方法一句话(<=60)': pick(/^## 4\. 方法一句话/m, /^---\s*$/m),
  };
  console.log('\n===== ' + f.split(/[\\/]/).pop() + ' =====');
  for (const [k, v] of Object.entries(secs)) {
    if (v == null) { console.log(k, '-> NOT FOUND'); continue; }
    const noWs = v.replace(/\s+/g, '');
    const cjk = (v.match(/[\u3400-\u9fff\u3000-\u303f\uff00-\uffef]/g) || []).length;
    const cjkAlnum = (v.match(/[\u3400-\u9fff\u3000-\u303f\uff00-\uffefA-Za-z0-9]/g) || []).length;
    const noMd = noWs.replace(/[`*>|#]/g, '');
    console.log(`${k}: 去空白=${noWs.length} 去空白去MD=${noMd.length} CJK=${cjk} CJK+字母数字=${cjkAlnum}`);
  }
}
