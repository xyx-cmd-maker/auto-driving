#!/usr/bin/env node
/**
 * check_branch_freshness.mjs —— 校验 `AGENTS.md` §0「分支对话登记」表的新鲜度
 *
 * 为什么存在：会话开工协议要求分支改动产出后"当场更新登记行"，但那条规则只靠自觉。
 * 本脚本读 §0 表里的 `最后更新` 列，与下表 ```text branch-watch 派生的 watch paths
 * 的**最新文件 mtime** 比对：登记落后超过容忍天数即报 stale（退出码 1）。
 *
 * 校验项：
 *   1. branch-table-parse   —— §0 表可解析（分支名 / 最后更新 列）
 *   2. branch-watch-parse   —— ```text branch-watch 块可解析
 *   3. branch-coverage      —— 表里每个分支都有 watch paths（除显式豁免：非分支）
 *   4. branch-date-valid    —— 日期格式可解析（YYYY-MM-DD 或 —）
 *   5. freshness:<分支>     —— 登记日期 ≥ watch paths 最新 mtime − 容忍天数
 *   6. watch-path-exists    —— watch path 在磁盘上存在（防路径写错静默通过）
 *
 * 关键设计：默认把 `scripts/smoke/` 加入每个分支的忽略集，否则本脚本自身
 * 一落盘就会把主支的落点"变新"，导致永远不报 stale —— 自我实现的新鲜。
 *
 * 用法：
 *   node scripts/smoke/check_branch_freshness.mjs
 *   node ... --tolerance 5        # 容忍天数（默认 3）
 *   node ... --json / --quiet / --root <项目根>
 * 退出码：0 全部新鲜；1 有 stale 或解析失败；2 用法错误。
 * 依赖：仅 Node 内置模块。
 */

import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import process from 'node:process';

const argv = process.argv.slice(2);
const getArg = (n) => { const i = argv.indexOf(n); return i >= 0 && argv[i + 1] ? argv[i + 1] : null; };
const AS_JSON = argv.includes('--json');
const QUIET = argv.includes('--quiet');
const TOLERANCE = Number(getArg('--tolerance') ?? 3);
if (!Number.isFinite(TOLERANCE) || TOLERANCE < 0) {
  console.error('[freshness] --tolerance 必须是非负数字');
  process.exit(2);
}

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(getArg('--root') || path.resolve(SCRIPT_DIR, '..', '..'));
const AGENTS_MD = path.join(ROOT, 'AGENTS.md');

// 忽略集：生成物 + 缓存 + 本脚本自身所在目录（见文件头说明）
const IGNORE_DIRS = new Set(['node_modules', '.git', '__pycache__', '.venv', 'runs']);
const IGNORE_PATH_FRAGMENTS = [path.join('scripts', 'smoke')];

const results = [];
const record = (id, ok, expected, actual, hint) => results.push({ id, ok, expected, actual, hint });

const toDay = (d) => Math.floor(new Date(d).getTime() / 86400000);
// 本地日期（不能用 toISOString：它会转 UTC，跨时区把本地 10-07 算成 10-08）
const localDate = (d) => {
  const x = new Date(d);
  const p = (n) => String(n).padStart(2, '0');
  return `${x.getFullYear()}-${p(x.getMonth() + 1)}-${p(x.getDate())}`;
};
// 表里的分支名可能带括号后缀（"主支（本对话）"），branch-watch 的键是短名 → 归一到短名
const normBranch = (n) => n.replace(/（[^）]*）/g, '').replace(/\([^)]*\)/g, '').trim();

function latestMtime(target, seen = { skipped: 0 }) {
  if (!existsSync(target)) return null;
  const st = statSync(target);
  if (st.isFile()) return { ms: st.mtimeMs, file: target };
  let best = null;
  const stack = [target];
  while (stack.length) {
    const cur = stack.pop();
    let entries;
    try { entries = readdirSync(cur, { withFileTypes: true }); } catch { continue; }
    for (const e of entries) {
      const full = path.join(cur, e.name);
      if (IGNORE_PATH_FRAGMENTS.some((frag) => full.includes(frag))) { seen.skipped += 1; continue; }
      if (e.isDirectory()) {
        if (IGNORE_DIRS.has(e.name)) { seen.skipped += 1; continue; }
        stack.push(full);
      } else if (e.isFile()) {
        try {
          const m = statSync(full).mtimeMs;
          if (!best || m > best.ms) best = { ms: m, file: full };
        } catch { /* 文件可能刚被删 */ }
      }
    }
  }
  return best;
}

// ---------- 解析 AGENTS.md ----------
if (!existsSync(AGENTS_MD)) {
  const payload = { root: ROOT, ok: false, error: `找不到 ${AGENTS_MD}`, checks: [] };
  if (AS_JSON) console.log(JSON.stringify(payload, null, 2));
  else console.error(`[freshness] 找不到 ${AGENTS_MD}`);
  process.exit(1);
}
const md = readFileSync(AGENTS_MD, 'utf8');

// 1) 分支表：| 分支 | 角色 | 主要产出/落点 | 状态 | 最后更新 |
const tableRows = [];
for (const line of md.split(/\r?\n/)) {
  if (!/^\|\s*\*\*/.test(line) && !/^\|\s*[^|\s]/.test(line)) continue;
  const cells = line.split('|').map((c) => c.trim());
  if (cells.length < 7) continue;
  const name = cells[1];
  if (!name || /^-+$/.test(name) || name === '分支') continue;
  if (!/最后更新/.test(line) && cells.length < 7) continue;
  // 只取 §0 那段的分支表：要求第 5 格（最后更新）是日期或 —
  const lastUpdated = cells[5];
  if (!/^(\d{4}-\d{2}-\d{2}|—|-)$/.test(lastUpdated)) continue;
  tableRows.push({ name: name.replace(/\*\*/g, '').trim(), key: normBranch(name.replace(/\*\*/g, '').trim()), lastUpdated });
}
record(
  'branch-table-parse',
  tableRows.length >= 3,
  '≥3 行（分支 | 角色 | 落点 | 状态 | 最后更新）',
  `解析到 ${tableRows.length} 行：${tableRows.map((r) => r.name).join(' / ') || '无'}`,
  '检查 §0 表是否仍为 5 列，且「最后更新」列存在'
);

// 2) branch-watch 块
const watchBlock = md.match(/```text([\s\S]*?)```/g)?.find((b) => b.includes('branch-watch'));
const watch = new Map();
if (!watchBlock) {
  record('branch-watch-parse', false, '```text branch-watch 块', '未找到', '在 §0 表下方补 branch-watch 块');
} else {
  for (const raw of watchBlock.split(/\r?\n/)) {
    const line = raw.replace(/^\s*>\s?/, '').trim();
    if (!line || line.startsWith('```') || line === 'branch-watch:') continue;
    const m = line.match(/^(.+?):\s*(.+)$/);
    if (!m) continue;
    const branch = m[1].trim();
    const paths = m[2].split(',').map((s) => s.trim()).filter(Boolean);
    watch.set(branch, paths);
  }
  record('branch-watch-parse', watch.size >= 3, '≥3 个分支的 watch paths', `${watch.size} 个：${[...watch.keys()].join(' / ')}`, '检查 branch-watch 块的缩进与冒号格式');
}

// 3) 覆盖性：表里每个分支都要有 watch paths（豁免：含"非分支"）
if (watch.size > 0) {
  const exempt = (n) => n.includes('非分支');
  const missing = tableRows.filter((r) => !watch.has(r.key) && !exempt(r.name)).map((r) => r.name);
  record('branch-coverage', missing.length === 0, '表内每个分支都有 watch paths', missing.length ? `缺：${missing.join('、')}` : '全覆盖', '为该分支在 branch-watch 块补一行，或在表中标为"非分支"');
}

// 4–6) 逐分支新鲜度
for (const row of tableRows) {
  const paths = watch.get(row.key);
  if (!paths) continue; // 已由 coverage 报出

  if (row.lastUpdated === '—' || row.lastUpdated === '-') {
    record(`freshness:${row.name}`, true, '登记为非追踪（—）', '跳过新鲜度比对', null);
    continue;
  }
  if (!/^\d{4}-\d{2}-\d{2}$/.test(row.lastUpdated)) {
    record(`freshness:${row.name}`, false, 'YYYY-MM-DD 或 —', `无法解析：${row.lastUpdated}`, '统一日期格式');
    continue;
  }

  // watch path 存在性
  const absent = paths.filter((p) => !existsSync(path.join(ROOT, p)));
  if (absent.length) {
    record(`watch-path-exists:${row.name}`, false, '全部存在', `不存在：${absent.join('、')}`, '修正 branch-watch 里的路径');
    continue;
  }
  record(`watch-path-exists:${row.name}`, true, '全部存在', `${paths.length} 条路径均存在`, null);

  // 最新 mtime
  let best = null;
  for (const p of paths) {
    const got = latestMtime(path.join(ROOT, p));
    if (got && (!best || got.ms > best.ms)) best = got;
  }
  if (!best) {
    record(`freshness:${row.name}`, true, 'watch paths 内无文件', '无可比对文件（跳过）', null);
    continue;
  }
  const newestDay = toDay(best.ms);
  const registeredDay = toDay(`${row.lastUpdated}T00:00:00`);
  const lagDays = newestDay - registeredDay;
  const ok = lagDays <= TOLERANCE;
  record(
    `freshness:${row.name}`, ok,
    `登记 ${row.lastUpdated}（容忍 ${TOLERANCE} 天）`,
    `最新改动 ${localDate(best.ms)}（${path.relative(ROOT, best.file)}），落后 ${lagDays} 天`,
    `产出已更新但登记行未更新：把 §0 表里「${row.name}」的「最后更新」改为 ${localDate(best.ms)}`
  );
}

// ---------- 输出 ----------
const failed = results.filter((r) => !r.ok);
const payload = {
  root: ROOT,
  ok: failed.length === 0,
  failedCount: failed.length,
  toleranceDays: TOLERANCE,
  today: localDate(new Date()),
  branches: tableRows.length,
  checks: results,
};

if (AS_JSON) {
  console.log(JSON.stringify(payload, null, 2));
} else {
  if (!QUIET) {
    console.log(`分支登记新鲜度校验  root=${ROOT}  容忍=${TOLERANCE} 天`);
    console.log('');
    for (const r of results) {
      console.log(`${r.ok ? '  OK  ' : ' FAIL '} ${r.id}`);
      console.log(`        期望: ${r.expected}`);
      console.log(`        实测: ${r.actual}`);
      if (!r.ok && r.hint) console.log(`        处置: ${r.hint}`);
    }
    console.log('');
  }
  console.log(failed.length === 0
    ? `[freshness] 全部新鲜：${results.length}/${results.length} 项通过`
    : `[freshness] 有过期/错误：${failed.length}/${results.length} 项未通过 → ${failed.map((r) => r.id).join(', ')}`);
}

process.exit(failed.length === 0 ? 0 : 1);
