// 学术写作合规自查（脚本化，不靠自觉）。用完即弃。
// 用法：node check_writing_compliance.mjs <file.md>
import fs from "node:fs";

const path = process.argv[2];
if (!path) { console.log("用法: node check_writing_compliance.mjs <file.md>"); process.exit(2); }
const raw = fs.readFileSync(path, "utf8");

// 只取 "Abstract" 段之后的英文正文，一直到下一个 "---"，避免把元文本/中文说明算进去
const startIdx = raw.indexOf("## Abstract");
const endIdx = raw.indexOf("\n---", startIdx);
const body = (startIdx >= 0 && endIdx > startIdx) ? raw.slice(startIdx, endIdx) : raw;

const checks = [];
const em = (body.match(/\u2014|--/g) || []).length;
checks.push(["em-dash / double-hyphen", em, em === 0]);

const banned = ["novel", "first", "state-of-the-art", "delve", "underscore", "pivotal",
                "seamless", "leverage", "realm", "showcase", "foster", "pave the way", "shed light"];
const hitBanned = banned.filter(w => new RegExp("\\b" + w + "\\b", "i").test(body));
checks.push(["banned words", hitBanned.length, hitBanned.length === 0]);

const overclaim = ["prove", "proves", "proved", "demonstrate", "demonstrates", "demonstrated",
                   "establish", "establishes", "established", "significantly", "outperform", "outperforms"];
const hitOver = overclaim.filter(w => new RegExp("\\b" + w + "\\b", "i").test(body));
checks.push(["over-claiming verbs", hitOver.length, hitOver.length === 0]);

const formulaic = ["In recent years", "With the rapid development", "It is worth noting"];
const hitForm = formulaic.filter(w => body.toLowerCase().includes(w.toLowerCase()));
checks.push(["formulaic openers", hitForm.length, hitForm.length === 0]);

const placeholders = (body.match(/\{\{[^}]+\}\}/g) || []).length;
checks.push(["leftover placeholders", placeholders, placeholders === 0]);

const sentences = body.replace(/\s+/g, " ").split(/(?<=[.!?])\s+/).filter(s => s.split(" ").length > 3);
const lens = sentences.map(s => s.split(" ").length);
const longest = Math.max(...lens);
checks.push(["longest sentence (words)", longest, longest <= 35]);

let ok = true;
for (const [name, val, pass] of checks) {
  if (!pass) ok = false;
  console.log(`  ${pass ? "OK  " : "FAIL"}  ${name}: ${val}`);
}
if (hitBanned.length) console.log("        命中: " + hitBanned.join(", "));
if (hitOver.length) console.log("        命中: " + hitOver.join(", "));
if (hitForm.length) console.log("        命中: " + hitForm.join(", "));
console.log(`  词数(Abstract 段) ≈ ${body.split(/\s+/).filter(Boolean).length}`);
process.exit(ok ? 0 : 1);
