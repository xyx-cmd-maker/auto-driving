// 抽取 MANUSCRIPT 标记之间的英文正文并做合规检查（用完即弃）
// 用法：node _check_manuscript.mjs <file.md>
import fs from "node:fs";

const p = process.argv[2];
const raw = fs.readFileSync(p, "utf8");
const a = raw.indexOf("<!-- BEGIN-MANUSCRIPT -->");
const b = raw.indexOf("<!-- END-MANUSCRIPT -->");
// 先剥掉 HTML 注释：否则 `<!--` 与 `-->` 里的 `--` 会被误判成双连字符
// 再剥掉 Markdown 水平线 `---`：它不是排版里的破折号（2026-10-18 假阳性，19 处）
let rawBody;
if (a >= 0 && b > a) {
  rawBody = raw.slice(a, b).replace(/<!--[\s\S]*?-->/g, "");
} else {
  // ★ 无 MANUSCRIPT 标记的文件（如 05-figures.md 这类图注/清单）也要能检查。
  // 2026-10-19 自审发现：这类文件此前直接 exit 2，等于**没被检查过**——
  // 结果 05-figures.md 里积了 3 处 em-dash 没人发现。
  // 退化策略：扫整文件，但剔除含中日韩字符的行（那是元信息，不是稿件正文）。
  rawBody = raw.replace(/<!--[\s\S]*?-->/g, "")
               .split(/\r?\n/)
               // 中文字符、中文标点（\u3000-\u303F）、全角符号（\uFF00-\uFFEF）都算元信息行
               .filter(l => !/[\u3000-\u303f\u3040-\u30ff\u4e00-\u9fff\uff00-\uffef]/.test(l))
               .join("\n");
  console.log("  （无 MANUSCRIPT 标记，已退化为整文件扫描并剔除中文行）");
}
const body = rawBody.replace(/^[ \t]*-{3,}[ \t]*$/gm, "");

const checks = [];
// 表格对齐行（|---|---|）里的连字符不是破折号，先剥掉再数
const noSep = body.replace(/^[ \t]*\|[\s\-:|]+\|[ \t]*$/gm, "");
const em = (noSep.match(/\u2014|--/g) || []).length;
checks.push(["em-dash / double-hyphen", em, em === 0]);

const banned = ["novel", "first", "state-of-the-art", "delve", "underscore", "pivotal",
                "seamless", "leverage", "realm", "showcase", "foster", "pave the way", "shed light"];
const hitBanned = banned.filter(w => new RegExp("\\b" + w + "\\b", "i").test(body));
checks.push(["banned words", hitBanned.length, hitBanned.length === 0]);

const over = ["prove", "proves", "proved", "demonstrate", "demonstrates", "demonstrated",
              "establish", "establishes", "established", "significantly", "outperform", "outperforms"];
const hitOver = over.filter(w => new RegExp("\\b" + w + "\\b", "i").test(body));
checks.push(["over-claiming verbs", hitOver.length, hitOver.length === 0]);

const formulaic = ["In recent years", "With the rapid development", "It is worth noting"];
const hitForm = formulaic.filter(w => body.toLowerCase().includes(w.toLowerCase()));
checks.push(["formulaic openers", hitForm.length, hitForm.length === 0]);

const ph = (body.match(/\{\{[^}]+\}\}/g) || []).length;
checks.push(["leftover placeholders", ph, ph === 0]);

// 句子长度：按 . ! ? 切，忽略标题行、列表编号、4 空格缩进的公式/代码块、以及**表格行**
// （表格不是散文：把表行拼起来会得到 100+ 词的假长句）
// ★ 无标记文件（图注/清单）跳过句长检查：它们的标题块与说明行会被拼成假长句，
//   而真正的句子长度由拼装后的 manuscript-draft.md 负责把关（那个文件有标记）。
const hasMarkers = (a >= 0 && b > a);
const prose = body.split(/\r?\n/)
  .filter(l => l.trim() && !l.startsWith("#") && !/^\d+\.\s/.test(l.trim())
            && !/^\s{4,}/.test(l) && !/^\s*\|/.test(l))
  .join(" ").replace(/\s+/g, " ");
const sents = prose.split(/(?<=[.!?])\s+/).filter(s => s.split(" ").length > 4);
const lens = sents.map(s => s.split(" ").length);
if (hasMarkers && lens.length) {
  const longest = Math.max(...lens);
  checks.push(["longest sentence (words)", longest, longest <= 35]);
  checks.push(["sentences >35 words", lens.filter(n => n > 35).length, lens.filter(n => n > 35).length === 0]);
} else {
  console.log("  SKIP  句长检查（无 MANUSCRIPT 标记：图注/清单文件，句长以 manuscript-draft.md 为准）");
}

let ok = true;
for (const [n, v, pass] of checks) { if (!pass) ok = false; console.log(`  ${pass ? "OK  " : "FAIL"}  ${n}: ${v}`); }
if (hitBanned.length) console.log("        banned: " + hitBanned.join(", "));
if (hitOver.length) console.log("        overclaim: " + hitOver.join(", "));
if (hitForm.length) console.log("        formulaic: " + hitForm.join(", "));
console.log(`  正文词数 ≈ ${prose.split(/\s+/).filter(Boolean).length}`);
if (hasMarkers && lens.length) {
  const longestV = Math.max(...lens);
  const idx = lens.indexOf(longestV);
  console.log(`  最长句（${longestV} 词）：${sents[idx].slice(0, 140)}...`);
}
process.exit(ok ? 0 : 1);
