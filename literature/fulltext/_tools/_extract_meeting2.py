import os, re, hashlib
import fitz

BASE = r"D:\Deepseek Harness\auto-driving\audit\第二次组会"
OUT = r"D:\Deepseek Harness\auto-driving\literature\fulltext\meeting2"
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith(".txt"):
        os.remove(os.path.join(OUT, f))

def slug(name):
    s = re.sub(r"\.pdf$", "", name, flags=re.I)
    s = re.sub(r"[^0-9A-Za-z]+", "-", s).strip("-").lower()
    return s[:60]

for root, dirs, files in os.walk(BASE):
    dirs.sort()
    for f in sorted(files):
        if not f.lower().endswith(".pdf"):
            continue
        p = os.path.join(root, f)
        h = hashlib.md5(open(p, "rb").read()).hexdigest()
        rel = os.path.relpath(p, BASE).replace("\\", "/")
        doc = fitz.open(p)
        parts = []
        for i, page in enumerate(doc):
            parts.append("\n\n===== PAGE %d =====\n\n" % (i + 1))
            parts.append(page.get_text("text"))
        text = "".join(parts)
        text = re.sub(r"[ \t\u00a0]+", " ", text)
        text = re.sub(r" ?\n ?", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        pages = doc.page_count
        doc.close()
        name = "%s__%s" % (slug(f), h[:8])
        with open(os.path.join(OUT, name + ".txt"), "w", encoding="utf-8") as fh:
            fh.write("SOURCE_PDF: %s\nMD5: %s\nPAGES: %d\n\n" % (rel, h, pages))
            fh.write(text)
        print("%-72s pages=%-3d chars=%d" % (name, pages, len(text)))
