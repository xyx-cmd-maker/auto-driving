// 抽取 MANUSCRIPT 标记之间的英文正文并做合规检查（用完即弃）
// 用法：node _check_manuscript.mjs <file.md>
import fs from "node:fs";

const p = process.argv[2];
const raw = fs.readFileSync(p, "utf8");
const a = raw.indexOf("<!-- BEGIN-MANUSCRIPT -->");
const b = raw.indexOf("<!-- END-MANUSCRIPT -->");
if (a < 0 || b <= a) { console.log("未找到 MANUSCRIPT 标记"); process.exit(2); }
// 先剥掉 HTML 注释：否则 `<!--` 与 `-->` 里的 `--` 会被误判成双连字符
const body = raw.slice(a, b).replace(/<!--[\s\S]*?-->/g, "");

const checks = [];
const em = (body.match(/\u2014|--/g) || []).length;
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

// 句子长度：按 . ! ? 切，忽略标题行、列表编号、以及**4 空格缩进的公式/代码块**
// （公式块不是散文，混进来会把 "a(t) = 3.0 * tanh(...)" 拼成 50+ 词的假长句）
const prose = body.split(/\r?\n/)
  .filter(l => l.trim() && !l.startsWith("#") && !/^\d+\.\s/.test(l.trim()) && !/^\s{4,}/.test(l))
  .join(" ").replace(/\s+/g, " ");
const sents = prose.split(/(?<=[.!?])\s+/).filter(s => s.split(" ").length > 4);
const lens = sents.map(s => s.split(" ").length);
const longest = Math.max(...lens);
checks.push(["longest sentence (words)", longest, longest <= 35]);
checks.push(["sentences >35 words", lens.filter(n => n > 35).length, lens.filter(n => n > 35).length === 0]);

let ok = true;
for (const [n, v, pass] of checks) { if (!pass) ok = false; console.log(`  ${pass ? "OK  " : "FAIL"}  ${n}: ${v}`); }
if (hitBanned.length) console.log("        banned: " + hitBanned.join(", "));
if (hitOver.length) console.log("        overclaim: " + hitOver.join(", "));
if (hitForm.length) console.log("        formulaic: " + hitForm.join(", "));
console.log(`  正文词数 ≈ ${prose.split(/\s+/).filter(Boolean).length}`);
if (lens.length) {
  const idx = lens.indexOf(longest);
  console.log(`  最长句（${longest} 词）：${sents[idx].slice(0, 140)}...`);
}
process.exit(ok ? 0 : 1);
