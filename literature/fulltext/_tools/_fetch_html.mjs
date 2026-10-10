// Deterministic HTML -> plain text extractor for arXiv/ar5iv (LaTeXML) pages.
// Usage: node _fetch_html.mjs <name> <url> [<name> <url> ...]
import { writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';

const OUT = 'D:\\Deepseek Harness\\auto-driving\\literature\\fulltext';
const RAW = join(OUT, '_raw');
mkdirSync(RAW, { recursive: true });

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

const SKIP_TAGS = new Set(['script', 'style', 'noscript', 'svg', 'head', 'nav', 'footer', 'header', 'iframe', 'button', 'form', 'select', 'input', 'textarea', 'link', 'meta']);
const SKIP_CLASS = /(^|\s)(ltx_page_nav|ltx_TOC|ltx_page_logo|ltx_role_navigation|ar5iv-menu|ar5iv-footer|ltx_navbar|ltx_page_footer|ltx_contact|ltx_role_author_note|ltx_author_notes|ltx_note_mark|ltx_bibliography--hide)(\s|$)/;
const VOID = new Set(['br', 'hr', 'img', 'input', 'meta', 'link', 'source', 'col']);
const BLOCK = new Set(['p', 'div', 'section', 'figure', 'table', 'ul', 'ol', 'blockquote', 'dl', 'dd', 'dt', 'article', 'aside', 'main', 'figcaption', 'thead', 'tbody', 'tfoot', 'tr']);

function decode(s) {
  return s.replace(/&(#x?[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]*);/g, (m, e) => {
    if (e[0] === '#') {
      const cp = e[1] === 'x' || e[1] === 'X' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
      return Number.isFinite(cp) && cp > 0 && cp <= 0x10ffff ? String.fromCodePoint(cp) : m;
    }
    const map = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', mdash: '\u2014', ndash: '\u2013', hellip: '\u2026', times: '\u00d7', minus: '\u2212', deg: '\u00b0', plusmn: '\u00b1', le: '\u2264', ge: '\u2265', ne: '\u2260', rarr: '\u2192', larr: '\u2190', harr: '\u2194', infin: '\u221e', sum: '\u2211', alpha: '\u03b1', beta: '\u03b2', gamma: '\u03b3', delta: '\u03b4', mu: '\u03bc', sigma: '\u03c3', tau: '\u03c4', phi: '\u03c6', omega: '\u03c9', Delta: '\u0394', Sigma: '\u03a3', Omega: '\u03a9' };
    return Object.prototype.hasOwnProperty.call(map, e) ? map[e] : m;
  });
}

function attr(tag, name) {
  const re = new RegExp('\\b' + name + '\\s*=\\s*("([^"]*)"|\'([^\']*)\'|([^\\s>]+))', 'i');
  const m = re.exec(tag);
  if (!m) return null;
  return decode(m[2] ?? m[3] ?? m[4] ?? '');
}

function htmlToText(html) {
  // keep only the article body when present (drops arXiv chrome entirely)
  let s = html.replace(/<!--[\s\S]*?-->/g, '');
  const artStart = s.search(/<article[\s>]/i);
  if (artStart > 0) {
    const artEnd = s.lastIndexOf('</article>');
    if (artEnd > artStart) s = s.slice(artStart, artEnd + 10);
  }
  const out = [];
  const stack = [];
  let skipDepth = 0;
  const push = (t) => { if (skipDepth === 0 && t) out.push(t); };
  const BLOCKNL = () => push('\n\n');
  let i = 0;
  const n = s.length;
  while (i < n) {
    const lt = s.indexOf('<', i);
    if (lt === -1) { push(decode(s.slice(i))); break; }
    if (lt > i) push(decode(s.slice(i, lt)));
    const gt = s.indexOf('>', lt);
    if (gt === -1) { push(decode(s.slice(lt))); break; }
    const tag = s.slice(lt + 1, gt);
    i = gt + 1;
    if (tag[0] === '!' || tag[0] === '?') continue;
    const closing = tag[0] === '/';
    const m = /^\/?\s*([a-zA-Z][a-zA-Z0-9:-]*)/.exec(tag);
    if (!m) continue;
    const name = m[1].toLowerCase();
    if (closing) {
      for (let k = stack.length - 1; k >= 0; k--) {
        if (stack[k].tag === name) {
          const removed = stack.splice(k);
          for (const r of removed) if (r.skip) skipDepth--;
          break;
        }
      }
      if (BLOCK.has(name)) BLOCKNL();
      if (name === 'td' || name === 'th') push(' | ');
      if (/^h[1-6]$/.test(name)) BLOCKNL();
      continue;
    }
    const selfClose = /\/\s*$/.test(tag) || VOID.has(name);
    const classVal = attr(tag, 'class') || '';
    let skip = SKIP_TAGS.has(name) || SKIP_CLASS.test(classVal);
    if (name === 'math') {
      const alt = attr(tag, 'alttext');
      if (alt) { push(' $' + alt + '$ '); skip = true; }
    }
    if (!selfClose) {
      if (BLOCK.has(name)) BLOCKNL();
      if (/^h[1-6]$/.test(name)) push('\n\n' + '#'.repeat(Number(name[1])) + ' ');
      if (name === 'li') push('\n- ');
      if (name === 'br') push('\n');
      stack.push({ tag: name, skip });
      if (skip) skipDepth++;
    } else if (name === 'br') {
      push('\n');
    }
  }
  let text = out.join('');
  text = text.replace(/[ \t\u00a0]+/g, ' ').replace(/ ?\n ?/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
  return text;
}

const args = process.argv.slice(2);
const report = [];
for (let a = 0; a < args.length; a += 2) {
  const name = args[a];
  const url = args[a + 1];
  try {
    const r = await fetch(url, { redirect: 'follow', headers: { 'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml' } });
    const html = await r.text();
    const ctype = r.headers.get('content-type') || '';
    writeFileSync(join(RAW, name + '.html'), html, 'utf8');
    if (!r.ok) { report.push(`FAIL ${name} HTTP ${r.status} ${url}`); continue; }
    if (!/html/i.test(ctype)) { report.push(`FAIL ${name} content-type=${ctype} ${url}`); continue; }
    const text = htmlToText(html);
    const body = `SOURCE_URL: ${url}\nFETCH_DATE: 2026-10-02\n`;
    writeFileSync(join(OUT, name + '.txt'), text + '\n\n' + body, 'utf8');
    report.push(`OK   ${name} status=${r.status} html=${html.length} text=${text.length}`);
  } catch (e) {
    report.push(`ERR  ${name} ${url} :: ${e.message}`);
  }
}
console.log(report.join('\n'));
