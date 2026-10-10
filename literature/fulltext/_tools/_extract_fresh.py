
import os, re, hashlib, fitz
RAW = r"D:/Deepseek Harness/auto-driving/literature/fulltext/_raw"
OUT = r"D:/Deepseek Harness/auto-driving/literature/fulltext/fresh2024"
names = [f for f in os.listdir(RAW) if f.endswith('.pdf')]
for f in sorted(names):
    p = os.path.join(RAW, f)
    d = fitz.open(p); parts = []
    for i, pg in enumerate(d):
        parts.append("\n\n===== PAGE %d =====\n\n" % (i + 1)); parts.append(pg.get_text("text"))
    t = "".join(parts)
    t = re.sub(r"[ \t\u00a0]+", " ", t); t = re.sub(r" ?\n ?", "\n", t); t = re.sub(r"\n{3,}", "\n\n", t).strip()
    h = hashlib.md5(open(p,'rb').read()).hexdigest()
    op = os.path.join(OUT, f[:-4] + "__" + h[:8] + ".txt")
    open(op, "w", encoding="utf-8").write("SOURCE_PDF: %s\nMD5: %s\nPAGES: %d\n\n" % (f, h, d.page_count) + t)
    print("%-46s pages=%-3d chars=%d" % (f, d.page_count, len(t)))
    d.close()
