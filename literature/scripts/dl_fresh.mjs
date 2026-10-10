// dl_fresh.mjs — 下载 2024+ 增量批次的全文（只下 OA 可得的）
import fs from "node:fs";
import { join } from "node:path";
const OUT = "D:/Deepseek Harness/auto-driving/literature/fulltext/_raw";
fs.mkdirSync(OUT, { recursive: true });
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36";
const ITEMS = [
  ["natcommun2025-platoon", "https://www.nature.com/articles/s41467-025-62597-x.pdf"],
  ["tiv2024-safe-rl-platoon", "https://arxiv.org/pdf/2401.11148"],
  ["robotics2024-cfc-smc", "https://www.mdpi.com/2218-6581/13/9/126/pdf"],
  ["trc2024-robust-cf-drl", "https://www.sciencedirect.com/science/article/pii/S0968090X24001641/pdfft"],
  ["tits2024-overtaking-feasibility", "https://napier-repository.worktribe.com/file/3636737/1/Overtaking%20Feasibility%20Prediction%20For%20Mixed%20Connected%20And%20Connectionless%20Vehicles%20%28accepted%20version%29"],
  ["tcst2024-physaug-deeplcc", "https://arxiv.org/pdf/2306.01387"],
  ["arxiv2026-lateral-string-stability", "https://arxiv.org/pdf/2605.01731"],
  ["inffus2026-platoon-knowledge-data", "https://arxiv.org/pdf/2502.08658"],
  ["tcst2025-async-string-stability", "https://centralesupelec.hal.science/hal-04794550v1/file/TCST24%20-%20Asynchronous%20sampled-data%20String%20Stability%20%20for%20a%20platoon%20of%20heterogeneous%20vehicles%20%20via%20a%20mesoscopic%20approach.pdf"],
  ["sensors2025-tinyml-survey", "https://www.mdpi.com/1424-8220/25/10/3191/pdf"],
  ["electronics2026-overtaking-hrl", "https://www.mdpi.com/2079-9292/15/8/1711/pdf"],
  ["trf2025-overtaking-truck-platoon", "https://eprints.whiterose.ac.uk/222778/2/2025.1-Revised%20manuscript-ZL.pdf"],
  ["trc2024-stopandgo-learning-cf", "https://www.osti.gov/servlets/purl/2438666"],
];
for (const [name, url] of ITEMS) {
  try {
    const r = await fetch(url, { redirect: "follow", headers: { "User-Agent": UA, Accept: "application/pdf,*/*" } });
    const buf = Buffer.from(await r.arrayBuffer());
    const ct = r.headers.get("content-type") || "";
    const isPdf = buf.subarray(0, 5).toString("latin1") === "%PDF-";
    const ext = isPdf ? ".pdf" : ".bin";
    fs.writeFileSync(join(OUT, name + ext), buf);
    console.log(`${isPdf ? "PDF " : "HTML"} ${name.padEnd(38)} status=${r.status} ${buf.length} B  ${ct.split(";")[0]}`);
  } catch (e) { console.log(`ERR  ${name.padEnd(38)} ${e.message}`); }
  await new Promise((s) => setTimeout(s, 900));
}
