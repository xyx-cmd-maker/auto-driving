// check_lnn_recent.mjs — does any 2024+ LNN application paper have a published version?
const TITLES = [
  'LNN-powered Fluid Antenna Multiple Access',
  'Liquid Fourier Latent Dynamics Networks for fast GPU-based numerical simulations in computational cardiology',
  'Exploring Liquid Neural Networks on Loihi-2',
  'Liquid-Graph Time-Constant Network for Multi-Agent Systems Control',
  'Continuous Cross-Domain Traffic State Prediction via Memory-Augmented Graph Liquid Time-Constant Networks',
];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
for (const t of TITLES) {
  const url = 'https://api.crossref.org/works?query.bibliographic=' + encodeURIComponent(t)
    + '&rows=2&select=DOI,title,issued,container-title,is-referenced-by-count&mailto=research@example.org';
  try {
    const r = await fetch(url, { headers: { 'User-Agent': 'dsh-verify/1.0 (mailto:research@example.org)' } });
    if (!r.ok) { console.log(`${t.slice(0, 50)} | HTTP ${r.status}`); await sleep(5000); continue; }
    const j = await r.json();
    const it = (j.message.items || [])[0];
    console.log(it
      ? `${(it.issued && it.issued['date-parts'][0][0])} | ${((it['container-title'] || [''])[0] || '-').slice(0, 46)} | ${(it.title || [''])[0].slice(0, 66)} | ${it.DOI}`
      : `${t.slice(0, 50)} | NO MATCH`);
  } catch (e) { console.log(`${t.slice(0, 50)} | ERR ${e.message}`); }
  await sleep(5000);
}
