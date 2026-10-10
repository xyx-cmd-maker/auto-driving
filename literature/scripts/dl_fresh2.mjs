// dl_fresh2.mjs — 补下 4 个失败的，并把全部 PDF 提为 txt
import fs from "node:fs";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
const RAW = "D:/Deepseek Harness/auto-driving/literature/fulltext/_raw";
const OUT = "D:/Deepseek Harness/auto-driving/literature/fulltext/fresh2024";
fs.mkdirSync(OUT, { recursive: true });
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36";
const RETRY = [
  ["robotics2024-cfc-smc", "https://www.mdpi.com/2218-6581/13/9/126/pdf?version=1724411538"],
  ["tcst2025-async-string-stability", "https://centralesupelec.hal.science/hal-04794550/document"],
  ["trc2024-robust-cf-drl", "https://arxiv.org/pdf/2305.02063"],
  ["tits2024-overtaking-feasibility", "https://www.researchgate.net/profile/x/publication"],
];
for (const [name, url] of RETRY.slice(0, 3)) {
  try {
    const r = await fetch(url, { redirect: "follow", headers: { "User-Agent": UA, Accept: "application/pdf,*/*" } });
    const buf = Buffer.from(await r.arrayBuffer());
    const isPdf = buf.subarray(0, 5).toString("latin1") === "%PDF-";
    if (isPdf) { fs.writeFileSync(join(RAW, name + ".pdf"), buf); console.log(`PDF  ${name} ${buf.length} B`); }
    else console.log(`HTML ${name} status=${r.status} ${buf.length} B (未保存)`);
  } catch (e) { console.log(`ERR  ${name} ${e.message}`); }
  await new Promise((s) => setTimeout(s, 900));
}

// 提取全部 PDF → txt（PyMuPDF）
const py = `
import os, re, hashlib, fitz
RAW = r"D:/Deepseek Harness/auto-driving/literature/fulltext/_raw"
OUT = r"D:/Deepseek Harness/auto-driving/literature/fulltext/fresh2024"
names = [f for f in os.listdir(RAW) if f.endswith('.pdf')]
for f in sorted(names):
    p = os.path.join(RAW, f)
    d = fitz.open(p); parts = []
    for i, pg in enumerate(d):
        parts.append("\\n\\n===== PAGE %d =====\\n\\n" % (i + 1)); parts.append(pg.get_text("text"))
    t = "".join(parts)
    t = re.sub(r"[ \\t\\u00a0]+", " ", t); t = re.sub(r" ?\\n ?", "\\n", t); t = re.sub(r"\\n{3,}", "\\n\\n", t).strip()
    h = hashlib.md5(open(p,'rb').read()).hexdigest()
    op = os.path.join(OUT, f[:-4] + "__" + h[:8] + ".txt")
    open(op, "w", encoding="utf-8").write("SOURCE_PDF: %s\\nMD5: %s\\nPAGES: %d\\n\\n" % (f, h, d.page_count) + t)
    print("%-46s pages=%-3d chars=%d" % (f, d.page_count, len(t)))
    d.close()
`;
fs.writeFileSync("D:/Deepseek Harness/auto-driving/literature/fulltext/_tools/_extract_fresh.py", py, "utf8");
console.log("\n--- extracting ---");
console.log(execFileSync("python", ["D:/Deepseek Harness/auto-driving/literature/fulltext/_tools/_extract_fresh.py"], { encoding: "utf8" }));
