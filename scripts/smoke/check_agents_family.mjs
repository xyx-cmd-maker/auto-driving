// check_agents_family.mjs — AGENTS 文件族完整性校验
// 用法：node scripts/smoke/check_agents_family.mjs
// 退出码：0 全部通过；1 有任一不符
//
// 校验项：
//   1. 文件族成员都存在（**自动发现**所有 AGENTS-*.md，不硬编码——新增子文件自动纳入校验）
//   2. 主文件引用了每个子文件（相对 markdown 链接）
//   3. 子文件都声明了与主文件等效
//   4. 主文件行数不超过阈值（默认 300；环境变量 AGENTS_MAX_LINES 可覆盖）
//   5. 子文件在主文件的分支 watch-paths 或文件族表中被登记
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(import.meta.dirname, "..", "..");
const MAIN = "AGENTS.md";
// 自动发现：根目录下所有 AGENTS-*.md（含未来新增的）
const SUBS = fs.readdirSync(ROOT)
  .filter((f) => /^AGENTS-.+\.md$/.test(f))
  .sort();
if (SUBS.length === 0) {
  console.error("[agents-family] 未发现任何 AGENTS-*.md 子文件——这本身说明校验失效");
  process.exit(1);
}
const MAX_LINES = Number(process.env.AGENTS_MAX_LINES || 300);

const results = [];
const ok = (name, detail) => results.push({ ok: true, name, detail });
const bad = (name, detail) => results.push({ ok: false, name, detail });

function read(rel) {
  const p = path.join(ROOT, rel);
  if (!fs.existsSync(p)) return null;
  return fs.readFileSync(p, "utf8");
}

function lineCount(text) {
  return text.split(/\r?\n/).length;
}

// 1. 存在性
const main = read(MAIN);
if (main === null) {
  bad("main-exists", `${MAIN} 不存在`);
} else {
  ok("main-exists", `${MAIN} 行数=${lineCount(main)}`);
}

for (const f of SUBS) {
  const t = read(f);
  if (t === null) bad(`sub-exists:${f}`, "缺失");
  else ok(`sub-exists:${f}`, `行数=${lineCount(t)}`);
}

// 2. 主文件引用子文件
if (main) {
  const missing = SUBS.filter((f) => !main.includes(`](${f})`) && !main.includes(f));
  if (missing.length) bad("main-references-subs", `未引用：${missing.join(", ")}`);
  else ok("main-references-subs", `已引用 ${SUBS.length} 个子文件`);
}

// 3. 子文件声明等效
for (const f of SUBS) {
  const t = read(f);
  if (!t) continue;
  const head = t.split(/\r?\n/).slice(0, 12).join("\n");
  if (/效力相同|同等效力/.test(head)) ok(`sub-declares-equivalence:${f}`, "已声明与主文件等效");
  else bad(`sub-declares-equivalence:${f}`, "开头 12 行内未声明与 AGENTS.md 效力相同");
}

// 4. 行数阈值
if (main) {
  const n = lineCount(main);
  if (n > MAX_LINES) bad("main-size", `${n} 行 > 阈值 ${MAX_LINES} → 按 AGENTS-NORMS.md §3 拆到新的 AGENTS-<主题>.md`);
  else ok("main-size", `${n} 行 ≤ 阈值 ${MAX_LINES}`);
}

// 5. watch-paths 登记（子文件变更也应被分支新鲜度覆盖）
if (main) {
  const m = main.match(/branch-watch:([\s\S]*?)```/);
  if (!m) bad("watch-paths-block", "主文件缺少 branch-watch 代码块");
  else {
    const watched = m[1];
    // 期望：每个子文件都在 watch 列表里出现
    const absent = SUBS.filter((f) => !watched.includes(f));
    if (absent.length) bad("watch-paths-covers-subs", `watch 路径未覆盖：${absent.join(", ")}（建议把根级 *.md 纳入主支 watch）`);
    else ok("watch-paths-covers-subs", `${SUBS.length} 个子文件均已被 watch`);
  }
}

// 输出
console.log(`AGENTS 文件族校验  root=${ROOT}  max-lines=${MAX_LINES}`);
console.log("");
for (const r of results) {
  console.log(`  ${r.ok ? "OK  " : "FAIL"} ${r.name}`);
  console.log(`        ${r.detail}`);
}
const failed = results.filter((r) => !r.ok).length;
console.log("");
console.log(`[agents-family] ${failed === 0 ? "全部通过" : failed + " 项不符"}：${results.length - failed}/${results.length}`);
process.exit(failed === 0 ? 0 : 1);
