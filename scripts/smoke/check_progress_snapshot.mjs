#!/usr/bin/env node
/**
 * check_progress_snapshot.mjs —— 校验 `AGENTS.md` §0.1「进度快照」与磁盘实况是否一致
 *
 * 为什么存在：会话开工协议（AGENTS.md §0）要求"实时更新进度"，但那条规矩只靠自觉。
 * 长对话里模型记忆会与磁盘事实分叉（用户 2026-10-08 提出的风险）。本脚本把其中
 * 四条**可机器判定的硬事实**变成可校验项，不一致即退出码 1。
 *
 * 校验项（四项，均取自 AGENTS.md §0.1 的 ```text 常量块）：
 *   1. results-json-count      —— results/ 下 .json 文件数
 *   2. src-code-file-count     —— src/ 下实现代码文件数（.py/.m/.cpp/.h/.hpp/.ipynb）
 *   3. portfolio-check         —— papers/portfolio.md 中 P1–P5 的「当前状态」列可解析且非空
 *   4. env:sumo-version        —— 环境锁里的 SUMO 版本 与 二进制实测版本（及注册表路径）一致
 *
 * 用法：
 *   node auto-driving/scripts/smoke/check_progress_snapshot.mjs
 *   node ... --root "D:\Deepseek Harness\auto-driving"    # 显式指定项目根
 *   node ... --json                                       # 机器可读输出
 *   node ... --quiet                                       # 只输出结论行
 *
 * 退出码：0 = 全部一致；1 = 有项不一致（或输入缺失）；2 = 用法/环境错误。
 * 约束：只用 Node 内置模块（node:fs / path / child_process），不装任何依赖。
 */

import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import process from 'node:process';

// ---------- 参数 ----------
const argv = process.argv.slice(2);
const getArg = (name) => {
  const i = argv.indexOf(name);
  return i >= 0 && argv[i + 1] ? argv[i + 1] : null;
};
const AS_JSON = argv.includes('--json');
const QUIET = argv.includes('--quiet');
// 注意：必须用 fileURLToPath，不能用 new URL(...).pathname —— 后者会把路径中的空格编码成 %20，
// 在 "D:\Deepseek Harness\..." 这类含空格的路径下会直接失效（本脚本首次运行即踩到）。
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_ROOT = path.resolve(SCRIPT_DIR, '..', '..'); // scripts/smoke -> 项目根
const ROOT = path.resolve(getArg('--root') || DEFAULT_ROOT);

const AGENTS_MD = path.join(ROOT, 'AGENTS.md');
const PORTFOLIO_MD = path.join(ROOT, 'papers', 'portfolio.md');
const ENV_LOCK = path.join(ROOT, 'configs', 'env', 'local-cpu.lock.yaml');

const CODE_EXT = new Set(['.py', '.m', '.cpp', '.h', '.hpp', '.ipynb']);
const results = [];

function record(id, ok, expected, actual, hint) {
  results.push({ id, ok, expected, actual, hint });
}

function readUtf8(p) {
  return readFileSync(p, 'utf8');
}

function walkFiles(dir, filter) {
  if (!existsSync(dir)) return null;
  const out = [];
  const stack = [dir];
  while (stack.length) {
    const cur = stack.pop();
    for (const entry of readdirSync(cur, { withFileTypes: true })) {
      const full = path.join(cur, entry.name);
      if (entry.isDirectory()) stack.push(full);
      else if (entry.isFile() && filter(entry.name)) out.push(full);
    }
  }
  return out;
}

// ---------- 0) 读取快照常量块 ----------
let snapshot = null;
let snapshotError = null;
if (!existsSync(AGENTS_MD)) {
  snapshotError = `找不到 ${AGENTS_MD}`;
} else {
  const md = readUtf8(AGENTS_MD);
  const section = md.split('### 0.1')[1] || '';
  const fence = section.match(/```text([\s\S]*?)```/);
  if (!fence) {
    snapshotError = 'AGENTS.md §0.1 里找不到 ```text 常量块';
  } else {
    snapshot = {};
    for (const raw of fence[1].split(/\r?\n/)) {
      // 常量块位于引用块（blockquote）内，每行带 "> " 前缀，必须先剥掉
      const line = raw.replace(/^\s*>\s?/, '');
      if (!line.trim()) continue;
      const m = line.match(/^\s*([A-Za-z0-9:_-]+)\s*:\s*(.+?)\s*$/);
      if (m) snapshot[m[1]] = m[2];
    }
  }
}

if (snapshotError) {
  const payload = { root: ROOT, ok: false, error: snapshotError, checks: [] };
  if (AS_JSON) console.log(JSON.stringify(payload, null, 2));
  else console.error(`[snapshot] 无法读取快照：${snapshotError}`);
  process.exit(1);
}

const want = (key) => snapshot[key];

// ---------- 1) results/ 下 .json 文件数 ----------
{
  const dir = path.join(ROOT, 'results');
  const files = walkFiles(dir, (n) => n.toLowerCase().endsWith('.json'));
  const actual = files === null ? null : files.length;
  const expected = Number(want('results-json-count'));
  const ok = actual !== null && Number.isInteger(expected) && actual === expected;
  record(
    'results-json-count', ok, want('results-json-count'),
    actual === null ? '(results/ 目录不存在)' : String(actual),
    '数字变化时：若确有真实算例 → 更新快照常量；若只是调试产物 → 移出 results/（AGENTS.md §2）'
  );
}

// ---------- 2) src/ 下实现代码文件数 ----------
{
  const dir = path.join(ROOT, 'src');
  const files = walkFiles(dir, (n) => CODE_EXT.has(path.extname(n).toLowerCase()));
  const actual = files === null ? null : files.length;
  const expected = Number(want('src-code-file-count'));
  const ok = actual !== null && Number.isInteger(expected) && actual === expected;
  record(
    'src-code-file-count', ok, want('src-code-file-count'),
    actual === null ? '(src/ 目录不存在)' : String(actual),
    'W1 起 src/otf、src/eval 会有实现文件；那时必须同步快照常量'
  );
}

// ---------- 3) portfolio 状态列可解析 ----------
{
  const expected = want('portfolio-check');
  if (!existsSync(PORTFOLIO_MD)) {
    record('portfolio-check', false, expected, '(papers/portfolio.md 不存在)', '台账是唯一状态来源，缺失即无法校验');
  } else {
    const md = readUtf8(PORTFOLIO_MD);
    const rows = md.split(/\r?\n/).filter((l) => /^\|\s*P[1-5]\s*\|/.test(l));
    const parsed = rows.map((l) => {
      const cells = l.split('|').map((c) => c.trim());
      // | P1 | 代号 | 架构层 | 落地场景 | venue | 周期 | 当前状态 | 关键风险 |
      const id = cells[1];
      const status = cells[7] || '';
      return { id, status };
    });
    const missing = parsed.filter((r) => !r.status || r.status.length < 4).map((r) => r.id);
    const ok = parsed.length === 5 && missing.length === 0;
    record(
      'portfolio-check', ok, expected,
      `解析到 ${parsed.length}/5 行；状态列空或过短：${missing.length ? missing.join(',') : '无'}`,
      '每篇论文的「当前状态」列必须存在且非空；状态变更先改台账（AGENTS.md §6）'
    );
  }
}

// ---------- 4) SUMO 版本：环境锁 vs 二进制实测 vs 注册表路径 ----------
{
  const expectedKey = 'env:sumo-version';
  const expected = want(expectedKey);
  const notes = [];
  let ok = true;

  // 4a. 环境锁里的版本（必须限定在 sumo: 块内，否则会误读到 python: "3.14.4" 那类 version 行）
  let lockVersion = null;
  if (!existsSync(ENV_LOCK)) {
    notes.push('configs/env/local-cpu.lock.yaml 不存在');
    ok = false;
  } else {
    const lock = readUtf8(ENV_LOCK);
    const lines = lock.split(/\r?\n/);
    const start = lines.findIndex((l) => /^sumo:\s*$/.test(l));
    if (start < 0) {
      notes.push('环境锁里找不到顶格的 sumo: 行');
      ok = false;
    } else {
      // 从 sumo: 起，直到下一个顶格内容行为止
      const blockLines = [];
      for (let i = start + 1; i < lines.length; i += 1) {
        if (lines[i].trim() && !/^\s/.test(lines[i])) break;
        blockLines.push(lines[i]);
      }
      const vm = blockLines.join('\n').match(/^\s*version:\s*"?([^"#\r\n]+?)"?\s*(?:#.*)?$/m);
      lockVersion = vm ? vm[1].trim() : null;
      if (!lockVersion) { notes.push('sumo: 块里读不到 version'); ok = false; }
      else if (expected && lockVersion !== expected) {
        notes.push(`环境锁版本(${lockVersion}) ≠ 快照常量(${expected})`);
        ok = false;
      }
    }
  }

  // 4b. 二进制实测（用注册表 SUMO_HOME 或环境变量推导，不依赖 PATH）
  let binVersion = null;
  let binPath = null;
  const home = process.env.SUMO_HOME
    || (() => {
      try {
        const out = execFileSync('reg', ['query', 'HKCU\\Environment', '/v', 'SUMO_HOME'], { encoding: 'utf8' });
        const m = out.match(/SUMO_HOME\s+REG_\w+\s+(.+?)\s*$/m);
        return m ? m[1].trim() : null;
      } catch { return null; }
    })();
  if (!home) {
    notes.push('取不到 SUMO_HOME（环境变量与注册表均为空）');
    ok = false;
  } else {
    binPath = path.join(home, 'bin', 'sumo.exe');
    if (!existsSync(binPath)) {
      notes.push(`sumo.exe 不在 ${binPath}`);
      ok = false;
    } else {
      try {
        const out = execFileSync(binPath, ['--version'], { encoding: 'utf8' });
        const m = out.match(/sumo\s+([0-9][0-9.]*)/i);
        binVersion = m ? m[1] : null;
        if (!binVersion) { notes.push('sumo --version 输出中解析不到版本号'); ok = false; }
        else if (binVersion !== lockVersion) {
          notes.push(`二进制实测版本(${binVersion}) ≠ 环境锁(${lockVersion})`);
          ok = false;
        }
      } catch (e) {
        notes.push(`执行 sumo.exe 失败：${e.message.split('\n')[0]}`);
        ok = false;
      }
    }
  }

  record(
    expectedKey, ok, expected,
    `锁内=${lockVersion ?? '—'} / 实测=${binVersion ?? '—'} / 路径=${binPath ?? '—'}${notes.length ? ' | ' + notes.join('；') : ''}`,
    '装了新版本、或移动了 SUMO 目录时：更新 configs/env/local-cpu.lock.yaml 与快照常量'
  );
}

// ---------- 输出 ----------
const failed = results.filter((r) => !r.ok);
const payload = {
  root: ROOT,
  snapshotDate: want('snapshot-date') ?? null,
  ok: failed.length === 0,
  failedCount: failed.length,
  checks: results,
};

if (AS_JSON) {
  console.log(JSON.stringify(payload, null, 2));
} else {
  if (!QUIET) {
    console.log(`进度快照校验  root=${ROOT}`);
    console.log(`快照日期=${payload.snapshotDate ?? '未标注'}\n`);
    for (const r of results) {
      console.log(`${r.ok ? '  OK  ' : ' FAIL '} ${r.id}`);
      console.log(`        期望: ${r.expected}`);
      console.log(`        实测: ${r.actual}`);
      if (!r.ok && r.hint) console.log(`        处置: ${r.hint}`);
    }
    console.log('');
  }
  if (failed.length === 0) {
    console.log(`[snapshot] 一致：${results.length}/${results.length} 项通过`);
  } else {
    console.log(`[snapshot] 不一致：${failed.length}/${results.length} 项未通过 → ${failed.map((r) => r.id).join(', ')}`);
    console.log('[snapshot] 修法二选一：① 磁盘是对的 → 更新 AGENTS.md §0.1 常量；② 快照是对的 → 把磁盘状态改回去。');
  }
}

process.exit(failed.length === 0 ? 0 : 1);
