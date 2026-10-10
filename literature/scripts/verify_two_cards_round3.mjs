// 第三轮：为「缺失信息（可执行动作）」提供取用证据
// (a) 正式版获取路径：Unpaywall OA 状态
// (b) 风险场参数标定出处 [30] 是否可查
const UA = 'otf-p1-litcheck/1.0 (mailto:research@example.org)';
async function get(url) {
  try { const r = await fetch(url, { headers: { 'User-Agent': UA, Accept: 'application/json' } }); return { url, status: r.status, text: await r.text() }; }
  catch (e) { return { url, status: 'ERR', text: String(e) }; }
}
const out = {};
for (const doi of ['10.1109/tce.2025.3612821', '10.1007/978-3-032-31441-3_28']) {
  const r = await get(`https://api.unpaywall.org/v2/${encodeURIComponent(doi)}?email=research@example.org`);
  try { const j = JSON.parse(r.text); out['unpaywall:' + doi] = { status: r.status, is_oa: j.is_oa, oa_status: j.oa_status, best: j.best_oa_location && { url: j.best_oa_location.url, host: j.best_oa_location.host_type, version: j.best_oa_location.version, license: j.best_oa_location.license }, journal: j.journal_name, publisher: j.publisher, year: j.year }; }
  catch { out['unpaywall:' + doi] = { status: r.status, raw: r.text.slice(0, 300) }; }
}
{
  const u = `https://api.crossref.org/works?query.bibliographic=${encodeURIComponent('Concept principle and modeling of driving risk field based on driver-vehicle-road interaction')}&rows=3&select=DOI,title,container-title,type,issued,author`;
  const r = await get(u);
  try { out['crossref:ref30'] = JSON.parse(r.text).message.items; } catch { out['crossref:ref30'] = { status: r.status, raw: r.text.slice(0, 300) }; }
}
{
  const u = `https://api.crossref.org/works?query.bibliographic=${encodeURIComponent('China Journal of Highway and Transport driving risk field')}&rows=3&select=DOI,title,container-title,type,issued`;
  const r = await get(u);
  try { out['crossref:cjht'] = JSON.parse(r.text).message.items; } catch { out['crossref:cjht'] = { status: r.status, raw: r.text.slice(0, 300) }; }
}
const fs = await import('node:fs');
fs.writeFileSync('D:/Deepseek Harness/auto-driving/literature/fresh2024/verify_two_cards_round3.json', JSON.stringify({ run_at_utc: new Date().toISOString(), out }, null, 1), 'utf8');
console.log(JSON.stringify(out, null, 1).slice(0, 4000));
