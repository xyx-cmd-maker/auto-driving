import re, html, json, os

SRC = r"D:\Deepseek Harness\auto-driving\literature\fulltext\_raw\deeponet-nmi2021-VoR-try1.bin"
OUTDIR = r"D:\Deepseek Harness\auto-driving\literature\fulltext"

t = open(SRC, encoding="utf-8", errors="replace").read()

def strip(x):
    x = re.sub(r"<[^>]+>", " ", x)
    x = html.unescape(x)
    x = re.sub(r"\s+", " ", x)
    return x.strip()

# 1) 官方摘要
m = re.search(r'id="Abs1-content">(.*?)</div></section>', t, re.S)
abstract = strip(m.group(1)) if m else "NOT FOUND"

# 2) 图注
figs = []
for fm in re.finditer(r'<figure[^>]*>(.*?)</figure>', t, re.S):
    blk = fm.group(1)
    cap = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', blk, re.S)
    label = re.search(r'c-article-figure__label[^>]*>(.*?)<', blk, re.S)
    txt = strip(cap.group(1)) if cap else strip(blk)[:300]
    lab = strip(label.group(1)) if label else ""
    figs.append((lab, txt))

# 3) 章节标题
secs = [strip(x) for x in re.findall(r'<h2[^>]*class="c-article-section__title[^"]*"[^>]*>(.*?)</h2>', t, re.S)]

# 4) 参考文献条数
refs = re.findall(r'<meta name="citation_reference"', t)
# 5) 元数据
def meta(name):
    mm = re.search(r'<meta name="%s" content="([^"]*)"' % re.escape(name), t)
    return html.unescape(mm.group(1)) if mm else None
authors = re.findall(r'<meta name="citation_author" content="([^"]*)"', t)

rep = []
rep.append("SOURCE_URL: https://www.nature.com/articles/s42256-021-00302-5 (VoR landing page)")
rep.append("FETCH_DATE: 2026-10-04")
rep.append("NOTE: VoR full text is NOT open access (Crossref license = Springer Nature TDM only; Europe PMC hitCount=0; OpenAlex oa_status=green points to the arXiv v3 preprint). This file contains ONLY the publicly served landing-page content: official abstract, figure captions, section headings, reference list and metadata.")
rep.append("")
rep.append("== METADATA ==")
rep.append("title: " + str(meta("citation_title")))
rep.append("journal: %s %s(%s):%s-%s (%s)" % (meta("citation_journal_title"), meta("citation_volume"), meta("citation_issue"), meta("citation_firstpage"), meta("citation_lastpage"), meta("citation_publication_date")))
rep.append("doi: " + str(meta("citation_doi")))
rep.append("article_type: " + str(meta("citation_article_type")))
rep.append("online_date: " + str(meta("citation_online_date")))
rep.append("n_authors: %d" % len(authors))
for a in authors:
    rep.append("  author: " + html.unescape(a))
rep.append("n_references_citation_meta: %d" % len(refs))
rep.append("")
rep.append("== OFFICIAL ABSTRACT (VoR) ==")
rep.append(abstract)
rep.append("")
rep.append("== SECTION HEADINGS ==")
for s in secs:
    rep.append("- " + s)
rep.append("")
rep.append("== FIGURE CAPTIONS (%d) ==" % len(figs))
for lab, txt in figs:
    rep.append("[%s] %s" % (lab, txt[:600]))
rep.append("")
rep.append("== REFERENCES (citation_reference meta, first 60) ==")
for i, rm in enumerate(re.finditer(r'<meta name="citation_reference" content="([^"]*)"', t), 1):
    rep.append("%d. %s" % (i, html.unescape(rm.group(1))[:300]))
    if i >= 60:
        break

out = os.path.join(OUTDIR, "deeponet-nmi2021-VoR-landingpage.txt")
open(out, "w", encoding="utf-8").write("\n".join(rep))
print("WROTE", out, len("\n".join(rep)), "chars")
print()
print("authors:", len(authors), "| refs:", len(refs), "| figures:", len(figs), "| sections:", len(secs))
print("ABSTRACT[:300]:", abstract[:300])
print()
for lab, txt in figs[:6]:
    print("[%s] %s" % (lab, txt[:160]))
