import { readFileSync } from "node:fs";
import { join } from "node:path";
const OUT = "D:\\Deepseek Harness\\auto-driving\\literature\\fulltext";
for (const f of ["p01-cfc-nmi2022","p07-pinn-ctrl-neucom2024","p15-humanlike-cf-trc2018","p33-lpstring-tcst2014","p43-dissipation-trc2018","p45-deeplcc-tcst2023"]) {
  const buf = readFileSync(join(OUT, f + ".txt"));
  const s = buf.toString("utf8");
  const footer = (s.match(/\n\nSOURCE_URL: [\s\S]*$/) || [""])[0].length;
  console.log(f.padEnd(30), "bytes=" + buf.length, "chars=" + s.length, "bodyChars=" + (s.length - footer), "footerChars=" + footer);
}
