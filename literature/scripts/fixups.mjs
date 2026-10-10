// fixups.mjs — resolve two remaining metadata questions.
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function j(url, tries = 5) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url, { headers: { 'User-Agent': 'dsh-citation-verify/1.0 (mailto:research@example.org)' } });
      if (r.status === 429 || r.status >= 500) { await sleep(2500 * (i + 1)); continue; }
      if (!r.ok) return { error: `HTTP ${r.status}` };
      return { json: await r.json() };
    } catch (e) { if (i === tries - 1) return { error: e.message }; await sleep(2000 * (i + 1)); }
  }
  return { error: 'retries exhausted' };
}

console.log('=== A) search: Swaroop & Hedrick string stability 1996 ===');
const q = await j('https://api.crossref.org/works?query.bibliographic=' + encodeURIComponent('String stability of interconnected systems Swaroop Hedrick') + '&rows=6&select=DOI,title,author,issued,container-title,volume,page&mailto=research@example.org');
if (q.json) for (const it of q.json.message.items) {
  console.log([it.DOI, (it.issued && it.issued['date-parts'][0][0]), (it['container-title'] || [''])[0], 'v' + it.volume, 'p' + it.page,
    (it.author || []).map((a) => a.family).join(','), (it.title || [''])[0].slice(0, 90)].join(' | '));
}
await sleep(800);

console.log('\n=== B) full record 10.1109/TCST.2015.2437336 ===');
const d = await j('https://api.crossref.org/works/' + encodeURIComponent('10.1109/TCST.2015.2437336'));
if (d.json) {
  const m = d.json.message;
  console.log('title:', (m.title || [''])[0]);
  console.log('venue:', (m['container-title'] || [''])[0]);
  console.log('volume:', m.volume, 'issue:', m.issue, 'page:', m.page, 'year:', m.issued['date-parts'][0][0]);
  console.log('published-print:', JSON.stringify(m['published-print']), 'published-online:', JSON.stringify(m['published-online']));
  console.log('authors:', (m.author || []).map((a) => `${a.given} ${a.family}`).join('; '));
}
await sleep(800);

console.log('\n=== C) full record 10.1007/978-3-031-73195-2_4 (DriveDreamer ECCV) ===');
const e = await j('https://api.crossref.org/works/' + encodeURIComponent('10.1007/978-3-031-73195-2_4'));
if (e.json) {
  const m = e.json.message;
  console.log('title:', (m.title || [''])[0]);
  console.log('container:', (m['container-title'] || [''])[0], '| type:', m.type);
  console.log('page:', m.page, 'year:', m.issued['date-parts'][0][0], 'publisher:', m.publisher);
  console.log('authors:', (m.author || []).map((a) => `${a.given} ${a.family}`).join('; '));
}
