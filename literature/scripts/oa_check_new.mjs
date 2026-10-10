// oa_check_new.mjs — 对 2024+ 短名单查 OA 状态（Unpaywall），决定哪些能做全文卡
import fs from "node:fs";
const DIR = "D:/Deepseek Harness/auto-driving/literature/fresh2024";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const LIST = [
  ["OTF 2026（Huang/Li 课题组）", "10.1007/978-3-032-20963-4_21"],
  ["ISA Trans 2026 CfC+KF 车辆状态估计", "10.1016/j.isatra.2026.06.027"],
  ["Robotics 2024 CfC 滑模控制", "10.3390/robotics13090126"],
  ["Nat Commun 2025 混行编队知识引导自学习", "10.1038/s41467-025-62597-x"],
  ["T-ITS 2024 超车可行性预测（混行）", "10.1109/tits.2024.3398602"],
  ["TCST 2024 Physics-augmented DeeP-LCC", "10.1109/tcst.2024.3361393"],
  ["T-IV 2024 混行编队安全 RL", "10.1109/tiv.2024.3373512"],
  ["TCST 2025 异步采样弦稳定", "10.1109/tcst.2024.3505036"],
  ["TAC 2024 抗社会驾驶员 cut-in", "10.1109/tac.2024.3401082"],
  ["TR-C 2024 鲁棒跟驰 DRL", "10.1016/j.trc.2024.104486"],
  ["TR-C 2026 混行交织区 V2I（李世武组）", "10.1016/j.trc.2026.106020"],
  ["TR-F 2025 超车卡车编队", "10.1016/j.trf.2025.01.026"],
  ["TR-C 2024 停走波与学习型跟驰", "10.1016/j.trc.2024.104578"],
  ["Inf Fusion 2026 知识-数据融合编队建模", "10.1016/j.inffus.2025.103622"],
  ["Sensors 2025 TinyML 综述", "10.3390/s25103191"],
  ["Electronics 2026 超车分层 RL", "10.3390/electronics15081711"],
  ["ICSSAS 2025 LTC 自动驾驶控制", "10.1109/icssas66150.2025.11081318"],
  ["Chaos Solitons Fractals 2025 跟驰 PD 抑制超车", "10.1016/j.chaos.2025.117116"],
];
const out = [];
for (const [name, doi] of LIST) {
  let rec = { name, doi };
  try {
    const r = await fetch(`https://api.unpaywall.org/v2/${doi}?email=research@example.org`);
    if (r.ok) {
      const j = await r.json();
      rec.is_oa = j.is_oa; rec.status = j.oa_status; rec.journal = j.journal_name;
      const b = j.best_oa_location;
      rec.best = b ? { version: b.version, host: b.host_type, license: b.license, url: b.url_for_pdf || b.url } : null;
      rec.locs = (j.oa_locations || []).map((l) => `${l.version}|${l.host_type}|${l.license || "-"}|${l.url_for_pdf || l.url}`);
    } else rec.err = "HTTP " + r.status;
  } catch (e) { rec.err = e.message; }
  out.push(rec);
  const flag = rec.is_oa ? (rec.best && rec.best.version === "publishedVersion" ? "★VoR-OA" : " OA:" + rec.status) : " ✗CLOSED";
  console.log(`${String(name).slice(0, 40).padEnd(40)} ${flag}`);
  if (rec.best) console.log(`     best: ${rec.best.version} | ${rec.best.host} | ${rec.best.license || "-"} | ${rec.best.url}`);
  if (rec.locs && rec.locs.length > 1) rec.locs.slice(1, 4).forEach((l) => console.log(`     loc : ${l}`));
  await sleep(600);
}
fs.writeFileSync(`${DIR}/oa_new.json`, JSON.stringify(out, null, 2), "utf8");
console.log(`\nWROTE ${DIR}/oa_new.json`);
