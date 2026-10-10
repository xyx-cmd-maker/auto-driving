import sys, re, fitz

OUT = r"D:\Deepseek Harness\auto-driving\literature\fulltext"


def extract(pdf_path, name, source_url):
    doc = fitz.open(pdf_path)
    parts = []
    for i, page in enumerate(doc):
        parts.append("\n\n===== PAGE %d =====\n\n" % (i + 1))
        parts.append(page.get_text("text"))
    text = "".join(parts)
    text = re.sub(r"[ \t\u00a0]+", " ", text)
    text = re.sub(r" ?\n ?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    footer = "SOURCE_URL: %s\nFETCH_DATE: 2026-10-02\n" % source_url
    with open(OUT + "\\" + name + ".txt", "w", encoding="utf-8") as f:
        f.write(text + "\n\n" + footer)
    print("OK %s pages=%d chars=%d" % (name, doc.page_count, len(text)))
    print("   HEAD: " + text[:220].replace("\n", " | "))
    doc.close()


extract(
    OUT + r"\_raw\p15-humanlike-cf-trc2018.pdf",
    "p15-humanlike-cf-trc2018",
    "https://arxiv.org/pdf/1901.00569",
)
extract(
    OUT + r"\_raw\p33-lpstring-tcst2014.pdf",
    "p33-lpstring-tcst2014",
    "https://pure.tue.nl/ws/files/73899014/Ploeg_2014_Lp_String_Stability_of_Cascaded_Systems_Application_to_Vehicle_Platooning.pdf",
)
