# -*- coding: utf-8 -*-
"""生成第二次组会汇报 Word 文档（P1 文献底座与三条硬约束）。

依赖：本机已有 python-docx 1.2.0 与 Microsoft Word COM，不安装任何新包。
用法：python make_meeting2_docx.py
产物：auto-driving/audit/第二次组会/组会汇报-第二次-P1文献底座与三条硬约束.docx
"""
import os
import sys
import tempfile
import zipfile

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audit", "第二次组会")
OUT_PATH = os.path.abspath(os.path.join(OUT_DIR, "组会汇报-第二次-P1文献底座与三条硬约束.docx"))

MINIMAL = {
    "[Content_Types].xml": (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        '</Types>'
    ),
    "_rels/.rels": (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        '</Relationships>'
    ),
    "word/_rels/document.xml.rels": (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
        '</Relationships>'
    ),
    "word/document.xml": (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:body><w:p/><w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1440" w:right="1418" w:bottom="1440" w:left="1418" w:header="851" w:footer="992" w:gutter="0"/>'
        '</w:sectPr></w:body></w:document>'
    ),
    "word/styles.xml": (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:docDefaults><w:rPrDefault><w:rPr>'
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="\u5b8b\u4f53" w:cs="Times New Roman"/>'
        '<w:sz w:val="21"/></w:rPr></w:rPrDefault></w:docDefaults>'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>'
        '<w:pPr><w:outlineLvl w:val="0"/></w:pPr>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="\u9ed1\u4f53"/>'
        '<w:b/><w:sz w:val="30"/></w:rPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>'
        '<w:pPr><w:outlineLvl w:val="1"/></w:pPr>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="\u9ed1\u4f53"/>'
        '<w:b/><w:sz w:val="24"/></w:rPr></w:style>'
        '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/>'
        '<w:tblPr><w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '</w:tblBorders></w:tblPr></w:style>'
        '</w:styles>'
    ),
    "word/settings.xml": (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:defaultTabStop w:val="420"/><w:compat/></w:settings>'
    ),
    "docProps/core.xml": (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/">'
        '<dc:title>\u7b2c\u4e8c\u6b21\u7ec4\u4f1a\u6c47\u62a5</dc:title>'
        '</cp:coreProperties>'
    ),
    "docProps/app.xml": (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
        '<Application>Python</Application></Properties>'
    ),
}


def write_minimal_docx(path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in MINIMAL.items():
            z.writestr(name, data.encode("utf-8"))


def main():
    try:
        import docx
        from docx.shared import Pt, Cm
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.enum.table import WD_TABLE_ALIGNMENT
        from docx.oxml.ns import qn
    except ImportError as exc:
        print("MISSING python-docx: %s" % exc)
        return 2

    cn = "\u5b8b\u4f53"
    cn_head = "\u9ed1\u4f53"

    def style_run(run, size=10.5, bold=False, font=cn):
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.name = "Times New Roman"
        rpr = run._element.get_or_add_rPr()
        rf = rpr.find(qn("w:rFonts"))
        if rf is None:
            rf = rpr.makeelement(qn("w:rFonts"), {})
            rpr.insert(0, rf)
        rf.set(qn("w:ascii"), "Times New Roman")
        rf.set(qn("w:hAnsi"), "Times New Roman")
        rf.set(qn("w:eastAsia"), font)

    def para(doc, text, size=10.5, bold=False, indent=True, align=None, space_after=4, font=cn):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_after = Pt(space_after)
        pf.line_spacing = 1.25
        if indent:
            pf.first_line_indent = Pt(size * 2)
        if align is not None:
            p.alignment = align
        style_run(p.add_run(text), size=size, bold=bold, font=font)
        return p

    def heading(doc, text, level=1):
        h = doc.add_heading(level=level)
        h.paragraph_format.space_before = Pt(10 if level == 1 else 8)
        h.paragraph_format.space_after = Pt(4)
        style_run(h.add_run(text), size=14 if level == 1 else 12, bold=True, font=cn_head)
        return h

    def table(doc, header, rows, widths=None, size=9.5):
        t = doc.add_table(rows=1, cols=len(header))
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        hdr = t.rows[0].cells
        for i, htxt in enumerate(header):
            hdr[i].text = ""
            p = hdr[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            style_run(p.add_run(htxt), size=size, bold=True, font=cn_head)
        for row in rows:
            cells = t.add_row().cells
            for i, val in enumerate(row):
                cells[i].text = ""
                p = cells[i].paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                style_run(p.add_run(str(val)), size=size)
        if widths:
            for r in t.rows:
                for i, w in enumerate(widths):
                    r.cells[i].width = Cm(w)
        return t

    def caption(doc, text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(8)
        style_run(p.add_run(text), size=9, font=cn_head)
        return p

    tmpdir = tempfile.mkdtemp(prefix="mtg2_")
    seed = os.path.join(tmpdir, "seed.docx")
    write_minimal_docx(seed)

    doc = docx.Document(seed)
    try:
        doc.styles["Table Grid"]
    except KeyError:
        from docx.oxml import parse_xml
        doc.styles.element.append(parse_xml(
            '<w:style xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders>'
            '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
            '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
            '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
            '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
            '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
            '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
            '</w:tblBorders></w:tblPr></w:style>'
        ))
        patched = os.path.join(tmpdir, "patched.docx")
        doc.save(patched)
        doc = docx.Document(patched)

    # ===== 标题 =====
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style_run(t.add_run("\u7b2c\u4e8c\u6b21\u7ec4\u4f1a\u6c47\u62a5\uff1aP1 \u7684\u6587\u732e\u5e95\u5ea7\u4e0e\u4e09\u6761\u786c\u7ea6\u675f"), size=18, bold=True, font=cn_head)
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style_run(sub.add_run("\u2014\u2014 \u8fde\u7eed\u65f6\u95f4\u795e\u7ecf\u7f51\u7edc\u3001\u51b3\u7b56\u57fa\u7ebf\u4e0e T-ITS \u56de\u987e\uff1a\u5bf9\u7b2c\u4e00\u7bc7\u8bba\u6587\u65ad\u8a00\u8303\u56f4\u7684\u4fee\u6b63"), size=11, font=cn)
    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta.paragraph_format.space_after = Pt(14)
    style_run(meta.add_run("\u6c47\u62a5\u4eba\uff1a\u3010\u5f85\u586b\u3011\u3000\u65e5\u671f\uff1a\u3010\u5f85\u586b\u3011\u3000\u9879\u76ee\uff1aOTF \u8bba\u6587\u96c6\u7fa4\u00b7P1 OTF-CfC"), size=10, font=cn)

    heading(doc, "\u4e00\u3001\u672c\u6b21\u6c47\u62a5\u7684\u91cd\u5fc3\uff1a\u4ece\u201c\u505a\u4ec0\u4e48\u201d\u8f6c\u5230\u201c\u8bf4\u5230\u4ec0\u4e48\u7a0b\u5ea6\u201d", 1)
    para(doc, "\u4e0a\u6b21\u6c47\u62a5\u4ea4\u4ee3\u7684\u662f\u9879\u76ee\u5e95\u5b50\u4e0e\u7b2c\u4e00\u7bc7\u8bba\u6587\u7684\u6280\u672f\u524d\u7f6e\uff1a\u76d8\u4e86\u8d44\u4ea7\u3001\u6838\u4e86\u5f15\u7528\u5e93\u3001\u5b9a\u4e86\u5b9e\u9a8c\u5951\u7ea6\u3002\u8fd9\u6b21\u4e0d\u91cd\u590d\u90a3\u4e9b\uff0c\u800c\u662f\u628a\u6587\u732e\u8bfb\u5230\u4e00\u4e2a\u80fd\u56de\u7b54\u201c\u6211\u4eec\u5230\u5e95\u80fd\u8bf4\u4ec0\u4e48\u201d\u7684\u7a0b\u5ea6\u3002\u5de5\u4f5c\u5206\u4e09\u5757\uff1a\u7b2c\u4e00\u5757\u662f P1 \u63a7\u5236\u5668\u7684\u65b9\u6cd5\u5b66\u5e95\u5ea7\uff08\u8fde\u7eed\u65f6\u95f4\u4e0e\u6d41\u4f53\u795e\u7ecf\u7f51\u7edc\uff09\uff1b\u7b2c\u4e8c\u5757\u662f\u51b3\u7b56\u57fa\u7ebf\uff08\u5f3a\u5316\u5b66\u4e60\u4e0e\u5b89\u5168\u5f3a\u5316\u5b66\u4e60\uff09\uff1b\u7b2c\u4e09\u5757\u662f T-ITS \u8fd1\u5e74\u6587\u732e\u7684\u56de\u987e\u4e0e\u5b9a\u4f4d\u53c2\u7167\u3002\u4e09\u5757\u5171\u8ba1 30 \u4f59\u7bc7\u539f\u6587\u5df2\u5f52\u6863\u5230 audit/\u7b2c\u4e8c\u6b21\u7ec4\u4f1a/\uff0c\u5e76\u5bf9\u5176\u4e2d 23 \u7bc7\u505a\u4e86\u9010\u7bc7\u7cbe\u8bfb\u8bb0\u5f55\u3002")

    para(doc, "\u7ed3\u8bba\u5148\u8bf4\u3002\u8fd9\u8f6e\u9605\u8bfb\u6ca1\u6709\u63a8\u7ffb\u7b2c\u4e00\u7bc7\u8bba\u6587\u7684\u65b9\u5411\uff0c\u4f46\u4fee\u6b63\u4e86\u5b83\u7684\u65ad\u8a00\u8303\u56f4\u3002\u5177\u4f53\u662f\u4e09\u6761\u786c\u7ea6\u675f\uff1a\u53c2\u6570\u91cf\u4e0d\u80fd\u5199\u201c\u5c0f\u4e8e 500 KB\u201d\uff1b\u4e0d\u80fd\u81ea\u79f0 physics-informed\uff1b\u4e03\u9879\u6307\u6807\u91cc\u6709\u4e24\u9879\u5728\u540c\u7c7b\u6587\u732e\u4e2d\u627e\u4e0d\u5230\u5bf9\u6807\u7269\u3002\u4e09\u6761\u90fd\u5df2\u5199\u8fdb\u9879\u76ee\u4e0d\u53d8\u91cf\u4e0e\u98ce\u9669\u767b\u8bb0\u8868\u3002\u4e0b\u9762\u5206\u522b\u8bf4\u660e\u5b83\u4eec\u4ece\u54ea\u6765\u3001\u5f71\u54cd\u4ec0\u4e48\u3001\u600e\u4e48\u5e94\u5bf9\u3002")

    heading(doc, "\u4e8c\u3001\u63a7\u5236\u5668\u7684\u65b9\u6cd5\u5b66\u5e95\u5ea7\uff1a\u8fde\u7eed\u65f6\u95f4\u7f51\u7edc\u7a76\u7adf\u7ed9\u4e86\u6211\u4eec\u4ec0\u4e48", 1)
    para(doc, "P1 \u62df\u7528 CfC\uff08\u95ed\u5f0f\u8fde\u7eed\u65f6\u95f4\u7f51\u7edc\uff09\u505a 100 Hz \u63a7\u5236\u5668\u3002\u8fd9\u8f6e\u628a\u5b83\u7684\u539f\u6587\uff08Nature Machine Intelligence 2022\uff09\u8bfb\u5230\u53ef\u6838\u5bf9\u7ea7\u522b\uff0c\u7ed3\u8bba\u662f\u597d\u574f\u53c2\u534a\u3002")

    heading(doc, "2.1 \u5b83\u80fd\u652f\u6301\u4ec0\u4e48", 2)
    para(doc, "\u53c2\u6570\u6548\u7387\u5728\u540c\u7c7b\u6a21\u578b\u6a2a\u5411\u6bd4\u8f83\u4e0b\u6210\u7acb\uff1aCfC \u7684\u9012\u5f52\u5206\u91cf\u53ea\u6709 4 184 \u4e2a\u53c2\u6570\uff0c\u540c\u8868\u4e2d NCP \u662f 6 495\u3001LSTM \u662f 33 089\u3002\u5bf9\u4e0d\u89c4\u5219\u91c7\u6837\u7684\u9c81\u68d2\u6027\u4e5f\u6709\u6b63\u9762\u8bc1\u636e\uff083 \u4e2a\u4efb\u52a1\uff09\uff0c\u8fd9\u4e0e\u5b9e\u8f66\u56de\u653e\u65f6\u65f6\u95f4\u6233\u4e0d\u5747\u5300\u7684\u60c5\u51b5\u662f\u543b\u5408\u7684\u3002\u673a\u7406\u4e0a\u5b83\u4e0d\u9700\u8981\u6570\u503c ODE \u6c42\u89e3\u5668\uff0c\u63a8\u7406\u6210\u672c\u4e0e\u79bb\u6563 RNN \u540c\u9636\uff0c\u8fd9\u4e0e 100 Hz \u5b9a\u6b65\u957f\u63a7\u5236\u56de\u8def\u76f8\u5bb9\u3002")

    heading(doc, "2.2 \u5b83\u4e0d\u80fd\u652f\u6301\u4ec0\u4e48\uff08\u8fd9\u662f\u672c\u8282\u91cd\u70b9\uff09", 2)
    para(doc, "\u7b2c\u4e00\uff0c\u8fd9\u7bc7\u6587\u7ae0\u91cc\u7684 CfC \u662f\u4e00\u4e2a\u5e8f\u5217\u5efa\u6a21\u6a21\u578b\uff08\u56fe\u50cf\u8f93\u5165\u3001\u8f93\u51fa\u8f6c\u5411\u66f2\u7387\uff09\uff0c\u4e0d\u662f\u63a7\u5236\u5668\uff1a\u6ca1\u6709\u63a7\u5236\u4ee3\u4ef7\u3001\u6ca1\u6709\u72b6\u6001\u53cd\u9988\u7ed3\u6784\u3001\u6ca1\u6709\u7a33\u5b9a\u6027\u4e0e\u7ea6\u675f\u5904\u7406\u3002\u7b2c\u4e8c\uff0c\u5168\u6587\u6ca1\u6709\u4efb\u4f55\u786c\u4ef6\u4fe1\u606f\uff0c\u4e5f\u6ca1\u6709\u4e00\u9879\u95ed\u73af\u63a7\u5236\u6307\u6807\u3002\u7b2c\u4e09\uff0c\u811a\u672c\u91cc\u7684\u201c\u53ef\u4e0a MCU\u201d\u53ea\u662f\u4f5c\u8005\u5728\u9002\u7528\u573a\u666f\u91cc\u7684\u5efa\u8bae\u53e5\uff0c\u4e0d\u662f\u5b9e\u9a8c\u7ed3\u8bba\u3002")

    para(doc, "\u8fd9\u4e09\u70b9\u5408\u8d77\u6765\u76f4\u63a5\u51b3\u5b9a\u4e86\u4e00\u4ef6\u4e8b\uff1aP1 \u4e0d\u80fd\u628a CfC \u7684\u5efa\u6a21\u4f18\u52bf\u5f53\u6210\u63a7\u5236\u4f18\u52bf\u6765\u5199\u3002\u5f15\u7528\u65f6\u53ea\u80fd\u5199\u6210\u201cCfC \u5728\u5f00\u73af\u5e8f\u5217\u5efa\u6a21\u4efb\u52a1\u4e0a\u76f8\u5bf9\u7279\u5b9a ODE \u57fa\u7ebf\u62a5\u544a\u4e86\u8bad\u7ec3/\u63a8\u7406\u52a0\u901f\u4e0e\u76f8\u5f53\u6216\u66f4\u4f18\u7684\u7cbe\u5ea6\uff08\u6587\u732e\u62a5\u544a\u503c\uff0c\u672a\u62a5\u544a\u786c\u4ef6\uff0c\u4e0d\u53ef\u76f4\u63a5\u6bd4\u8f83\uff09\u201d\u3002")

    para(doc, "\u4e00\u4e2a\u5bf9\u6211\u4eec\u6bd4\u8f83\u5173\u952e\u7684\u8865\u5145\u53d1\u73b0\uff1a\u5728\u8fd9\u4e2a\u7cfb\u5217\u91cc\uff0c\u76ee\u524d\u552f\u4e00\u7684\u771f\u673a\u95ed\u73af\u8bc1\u636e\u6765\u81ea\u4e00\u7bc7\u56db\u65cb\u7ffc\u98de\u884c\u8bba\u6587\uff08Science Robotics 2023\uff09\uff0c\u5b83\u7684\u63a7\u5236\u5668\u6b63\u597d\u5c31\u662f CfC \u8840\u7edf\uff0c\u5728\u56db\u4e2a\u73af\u5883\u91cc\u5404 40 \u6b21\u673a\u8f7d\u95ed\u73af\u3002\u4f46\u5b83\u7684\u5e73\u53f0\u662f Jetson TX2\uff08\u5355\u677f\u673a\uff0c\u4e0d\u662f MCU\uff09\uff0c\u800c\u4e14\u540c\u6837\u6ca1\u6709\u53c2\u6570\u91cf\u3001\u6ca1\u6709\u63a7\u5236\u9891\u7387\u3001\u6ca1\u6709\u65f6\u5ef6\u3002\u6240\u4ee5\u5b83\u80fd\u652f\u6301\u201c\u8be5\u7c7b\u6a21\u578b\u53ef\u5728\u771f\u5b9e\u786c\u4ef6\u4e0a\u95ed\u73af\u201d\uff0c\u4e0d\u80fd\u652f\u6301\u4efb\u4f55\u5b9e\u65f6\u6027\u4e0e\u5185\u5b58\u65ad\u8a00\u3002")

    heading(doc, "\u4e09\u3001\u4e09\u6761\u786c\u7ea6\u675f\u53ca\u5176\u540e\u679c", 1)

    heading(doc, "3.1 \u53c2\u6570\u91cf\uff1a\u4e0d\u80fd\u5199\u201c\u5c0f\u4e8e 500 KB\u201d", 2)
    para(doc, "\u84dd\u56fe\u91cc\u5199\u7684\u662f\u63a7\u5236\u5668\u53c2\u6570\u91cf\u5c0f\u4e8e 500 KB\u3002\u539f\u6587\u53ea\u7ed9\u4e86\u4e00\u7ec4\u53c2\u6570\u91cf\uff0c\u800c\u4e14\u662f\u8f66\u9053\u4fdd\u6301\u6a21\u578b\u7684\uff1a\u9012\u5f52\u5206\u91cf 4 184\uff0c\u542b CNN \u611f\u77e5\u5934\u7684\u5168\u6a21\u578b 230 828\u3002\u6362\u7b97\u4e0b\u6765\uff0cfp32 \u7ea6 902 KiB\u3001\u8d85\u8fc7 500 KB\uff1bfp16 \u7ea6 451 KiB \u624d\u8fbe\u6807\u3002\u800c\u4e14\u8fd9\u4e2a\u6362\u7b97\u662f\u6211\u4eec\u505a\u7684\uff0c\u8bba\u6587\u53ea\u7ed9\u4e86\u53c2\u6570\u4e2a\u6570\uff0c\u6ca1\u63d0\u91cf\u5316\u7cbe\u5ea6\u4e0e KB\u3002")

    table(doc,
          ["\u53e3\u5f84", "\u53c2\u6570\u91cf", "fp32", "fp16", "\u80fd\u4e0d\u80fd\u5199 <500 KB"],
          [
              ["\u53ea\u7b97 RNN \u5206\u91cf", "4 184", "\u7ea6 16.3 KiB", "\u7ea6 8.2 KiB", "\u80fd\uff0c\u4f46\u9700\u81ea\u8bc1\u611f\u77e5\u524d\u7aef\u4e0d\u5360\u9884\u7b97\u6216\u53e6\u884c\u91cf\u5316"],
              ["\u5168\u6a21\u578b\uff08\u542b\u611f\u77e5\u5934\uff09", "230 828", "\u7ea6 902 KiB", "\u7ea6 451 KiB", "fp32 \u4e0d\u80fd\uff1bfp16 \u53ef\uff0c\u4f46\u987b\u62a5\u91cf\u5316\u540e\u7684\u7cbe\u5ea6\u635f\u5931"],
          ],
          widths=[4.4, 2.4, 2.4, 2.4, 5.6], size=9.5)
    caption(doc, "\u8868 1\u3000\u53c2\u6570\u91cf\u53e3\u5f84\u4e0e\u53ef\u5199\u8303\u56f4\uff08\u53c2\u6570\u4e3a\u539f\u6587\u503c\uff0cKiB \u6362\u7b97\u4e3a\u672c\u9879\u76ee\u6240\u505a\uff09")

    para(doc, "\u56e0\u6b64\u9879\u76ee\u5c42\u9762\u5df2\u5b9a\u7eaa\u5f8b\uff1a\u5728\u62ff\u5230\u672c\u9879\u76ee\u81ea\u5df1\u7684\u5b9e\u6d4b\u53c2\u6570\u91cf\u4e4b\u524d\uff0cP1 \u4e0d\u5f97\u5199\u201c\u5c0f\u4e8e 500 KB\u201d\uff1b\u82e5\u5fc5\u987b\u5199\uff0c\u5fc5\u987b\u540c\u65f6\u5199\u660e\u91cf\u5316\u7cbe\u5ea6\u4e0e\u662f\u5426\u542b\u611f\u77e5\u5934\u3002\u540c\u4e00\u6761\u7eaa\u5f8b\u4e5f\u9002\u7528\u4e8e\u201c\u5ef6\u8fdf\u5c0f\u4e8e 1 ms\u201d\u4e0e\u201c\u53ef\u4e0a MCU\u201d\u2014\u2014\u4e24\u8005\u76ee\u524d\u90fd\u6ca1\u6709\u4efb\u4f55\u652f\u6491\u7269\u3002")

    heading(doc, "3.2 \u672f\u8bed\uff1a\u4e0d\u5b9c\u81ea\u79f0 physics-informed", 2)
    para(doc, "\u6211\u4eec\u539f\u672c\u7684\u8bbe\u60f3\u662f\u628a OTF \u52bf\u573a\u4f5c\u4e3a ODE \u7684\u8fb9\u754c\u6761\u4ef6\uff0c\u8fd9\u5728\u53d9\u8ff0\u4e0a\u5f88\u5bb9\u6613\u88ab\u5199\u6210\u201c\u7269\u7406\u4fe1\u606f\u9a71\u52a8\uff08physics-informed\uff09\u201d\u3002\u4f46\u8fd9\u8f6e\u627e\u5230\u7684\u6700\u63a5\u8fd1\u5de5\u4f5c\uff08PINC\uff0cNeurocomputing 2024\uff09\u63d0\u4f9b\u4e86\u4e00\u4e2a\u53cd\u4f8b\uff1a\u5b83\u7528\u7684\u662f\u8f6f\u635f\u5931\u9879\uff0c\u4e14\u5176\u57fa\u51c6\u65b9\u7a0b\u6709\u53ef\u5224\u771f\u4f2a\u7684\u6b8b\u5dee\u3002\u800c OTF \u52bf\u573a\u662f\u542f\u53d1\u5f0f\u5148\u9a8c\uff0c\u4e0d\u5b58\u5728\u8fd9\u6837\u7684\u6b8b\u5dee\u2014\u2014\u6ca1\u6709\u4e00\u4e2a\u65b9\u7a0b\u53ef\u4ee5\u5224\u5b9a\u5b83\u5bf9\u4e0d\u5bf9\u3002\u786c\u8bf4 physics-informed \u4f1a\u88ab\u5ba1\u7a3f\u4eba\u4e00\u53e5\u95ee\u5012\u3002")

    para(doc, "\u5b9c\u7528\u7684\u8bf4\u6cd5\u662f structure-informed\u3001prior-informed \u6216 boundary-conditioned\uff0c\u5e76\u628a OTF \u5b9a\u4f4d\u4e3a\u5f15\u5bfc\u6027\u504f\u7f6e\uff08inductive bias\uff09\u3002\u8fd9\u91cc\u6709\u4e00\u4e2a\u5bf9\u6211\u4eec\u6709\u5229\u7684\u7ec6\u8282\uff1aPINC \u90a3\u7bc7\u6587\u7ae0\u4ece\u672a\u505a\u8fc7\u5173\u6389\u7269\u7406\u9879\u7684\u6d88\u878d\uff0c\u800c P1 \u7684 A1 \u6d88\u878d\u6b63\u662f OTF \u5f00/\u5173\u5bf9\u6bd4\u2014\u2014\u8fd9\u4e00\u6b65\u76f8\u5bf9\u5b83\u662f\u51c0\u589e\u91cf\u3002")

    heading(doc, "3.3 \u6307\u6807\uff1a\u4e24\u9879\u5728\u540c\u7c7b\u6587\u732e\u91cc\u627e\u4e0d\u5230\u5bf9\u6807\u7269", 2)
    para(doc, "\u6211\u4eec\u7ed9 P1 \u5b9a\u4e86\u4e03\u9879\u6307\u6807\u3002\u8fd9\u8f6e\u9010\u7bc7\u6838\u5bf9\u540c\u7c7b\u6587\u732e\u540e\u53d1\u73b0\uff1a\u7aef\u5230\u7aef\u5ef6\u8fdf\u4e0e MCU \u5185\u5b58\u5360\u7528\u8fd9\u4e24\u9879\uff0c\u5728\u5df2\u68c0\u7d22\u7684\u540c\u7c7b\u5de5\u4f5c\u91cc\u666e\u904d\u6ca1\u6709\u5bf9\u5e94\u7269\uff1b\u800c\u8ddf\u8f66\u8bef\u5dee RMSE\u3001\u52a0\u901f\u5ea6\u5e73\u65b9\u79ef\u5206\u3001Jerk \u5cf0\u503c\u8fd9\u4e09\u9879\u624d\u662f\u771f\u6b63\u53ef\u5bf9\u6807\u7684\u3002")

    table(doc,
          ["P1 \u6307\u6807", "\u540c\u7c7b\u6587\u732e\u53ef\u5bf9\u6807\u6027", "\u5904\u7406\u65b9\u5f0f"],
          [
              ["\u8ddf\u8f66\u8bef\u5dee RMSE", "\u53ef\u5bf9\u6807\uff08\u90e8\u5206\u9700\u5148\u7edf\u4e00\u53c2\u8003\u91cf\u4e0e\u5206\u6bcd\uff09", "\u8fdb\u5165\u4e3b\u5bf9\u6bd4\u8868"],
              ["\u52a0\u901f\u5ea6\u5e73\u65b9\u79ef\u5206\u3001Jerk \u5cf0\u503c", "\u53ef\u5bf9\u6807\uff08\u4e0e\u90e8\u5206\u6587\u732e\u7684\u52a0\u901f\u5ea6\u7ea6\u675f\u8fb9\u754c\u53ef\u6bd4\uff09", "\u8fdb\u5165\u4e3b\u5bf9\u6bd4\u8868"],
              ["\u8f66\u9053\u5c45\u4e2d\u504f\u5dee\u3001\u524d\u8f6e\u8f6c\u89d2\u65b9\u5dee", "\u90e8\u5206\u53ef\u5bf9\u6807", "\u8fdb\u5165\u4e3b\u5bf9\u6bd4\u8868\uff0c\u6807\u6ce8\u53e3\u5f84\u5dee\u5f02"],
              ["\u7aef\u5230\u7aef\u5ef6\u8fdf", "\u65e0\u5bf9\u6807\u7269\uff08\u6709\u6587\u732e\u62a5\u684c\u9762\u673a\u8ba1\u7b97\u65f6\u95f4\uff0c\u5e73\u53f0\u4e0d\u540c\uff09", "\u4e0d\u8fdb\u5165\u5bf9\u6bd4\u8868\uff1b\u82e5\u62a5\uff0c\u53ea\u62a5\u201c\u8ba1\u7b97\u65f6\u95f4 / \u91c7\u6837\u5468\u671f\u201d\u8fd9\u4e00\u76f8\u5bf9\u6bd4\u503c"],
              ["MCU \u5185\u5b58\u5360\u7528", "\u65e0\u5bf9\u6807\u7269", "\u5fc5\u987b\u81ea\u6d4b\uff1b\u4e14\u62c6\u6210 Flash\uff08\u6743\u91cd\uff09\u4e0e RAM\uff08\u6fc0\u6d3b/\u5cf0\u503c\uff09\u4e24\u9879\uff0c\u7ec4\u5408\u6210\u4e00\u4e2a\u6570\u4f1a\u88ab\u8d28\u7591"],
          ],
          widths=[4.2, 6.4, 7.0], size=9)
    caption(doc, "\u8868 2\u3000\u4e03\u9879\u6307\u6807\u7684\u53ef\u5bf9\u6807\u6027\u5206\u7c7b\uff08\u9010\u7bc7\u4f9d\u636e\u89c1 literature/notes/ \u4e0e literature/fresh2024/notes/ \u7684\u6838\u5bf9\u8bb0\u5f55\uff09")

    para(doc, "\u8fd9\u6761\u53d1\u73b0\u5e26\u6765\u4e24\u4e2a\u76f4\u63a5\u540e\u679c\u3002\u4e00\u662f\u5bf9\u6bd4\u8868\u5fc5\u987b\u53ea\u653e\u53ef\u6bd4\u9879\uff0c\u4e0d\u53ef\u6bd4\u7684\u5355\u5217\u5e76\u6ce8\u660e\u201c\u6587\u732e\u65e0\u5bf9\u5e94\u6307\u6807\u201d\u2014\u2014\u5426\u5219\u7b49\u4e8e\u62ff\u522b\u4eba\u6ca1\u6d4b\u7684\u4e1c\u897f\u8bf4\u81ea\u5df1\u66f4\u597d\u3002\u4e8c\u662f\u6211\u4eec\u53d1\u73b0\u4e86\u8be5\u8865\u800c\u6ca1\u8865\u7684\u6307\u6807\uff1a\u56e0\u4e3a P1 \u505a\u7684\u662f\u7f16\u961f\u63a7\u5236\uff0c\u800c\u5f26\u7a33\u5b9a\u6027\uff08string stability\uff09\u4e0d\u80fd\u7528 RMSE \u4ee3\u66ff\uff1b\u4e00\u7bc7\u76f8\u5173\u5de5\u4f5c\u7ed9\u51fa\u4e86\u53ef\u76f4\u63a5\u590d\u7528\u7684\u56db\u9879\u8bc4\u4ef7\u534f\u8bae\uff08\u632f\u8361\u963b\u5c3c\u6bd4\u3001\u8212\u9002\u6210\u672c\u3001\u80fd\u8017\u3001\u4ea4\u901a\u6d41\u7a33\u5b9a\u6027\uff09\uff0c\u5176\u4e2d\u632f\u8361\u963b\u5c3c\u6bd4\u4e0e\u4ea4\u901a\u6d41\u7a33\u5b9a\u6027\u6b63\u662f\u201c\u6df7\u884c\u7f16\u961f\u632f\u8361\u6291\u5236\u201d\u7684\u76f4\u63a5\u5ea6\u91cf\uff0c\u53ef\u4f5c\u4e3a P1 \u7684\u8865\u5145\u6307\u6807\u3002")

    heading(doc, "\u56db\u3001\u51b3\u7b56\u57fa\u7ebf\uff1a\u4e24\u4e2a TD3 \u4e0d\u80fd\u6df7", 1)
    para(doc, "P1 \u7684\u57fa\u7ebf\u91cc\u6709\u4e00\u6761\u662f\u5b66\u4f4d\u8bba\u6587\u7684 TD3 \u76f4\u63a7\u3002\u8fd9\u8f6e\u540c\u65f6\u8bfb\u4e86 TD3 \u539f\u6587\uff08ICML 2018\uff09\u4e0e\u5b66\u4f4d\u8bba\u6587\u7b2c\u4e94\u7ae0\u7684\u5b9e\u73b0\uff0c\u4e24\u8005\u5fc5\u987b\u5206\u5f00\u5bf9\u5f85\uff1a\u524d\u8005\u662f\u7b97\u6cd5\u51fa\u5904\u3001\u540e\u8005\u662f\u5177\u4f53\u5b9e\u73b0\uff08\u7f51\u7edc\u5c42\u6570\u3001\u5b66\u4e60\u7387\u3001\u5956\u52b1\u8bbe\u8ba1\u5747\u4e0d\u540c\uff09\u3002\u800c\u4e14 TD3 \u539f\u6587\u91cc\u6ca1\u6709\u7aef\u5230\u7aef\u5ef6\u8fdf\u4e0e\u5185\u5b58\u6307\u6807\uff0c\u8fd9\u4e24\u9879\u53ea\u80fd\u81ea\u91c7\u3002")

    para(doc, "\u5b89\u5168\u5f3a\u5316\u5b66\u4e60\u65b9\u5411\uff0c\u8fd9\u8f6e\u8bfb\u4e86\u4e09\u7bc7\u53ef\u76f4\u63a5\u4f7f\u7528\u7684\uff1a\u4e00\u7bc7\u662f T-ITS \u4e0a\u7684 Safety-Enhanced DRL\uff0c\u4e00\u7bc7\u662f Q-Advantage\uff08\u4eba\u5de5\u5f15\u5bfc\u7684\u5b89\u5168\u5f3a\u5316\u5b66\u4e60\uff09\uff0c\u4e00\u7bc7\u662f\u5e26\u5b89\u5168\u5c42\u7684\u7aef\u5230\u7aef\u65b9\u6cd5\u3002\u5b83\u4eec\u5171\u540c\u652f\u6491 P4\uff08\u5b89\u5168\u9694\u79bb\u5c42\uff09\u7684\u52a8\u673a\u53d9\u4e8b\u2014\u2014\u5373\u201c\u4e0a\u5c42\u667a\u80fd\u4f53\u4e0d\u53ef\u5b8c\u5168\u4fe1\u4efb\uff0c\u9700\u8981\u72ec\u7acb\u7684\u7269\u7406\u53ef\u884c\u6027\u7b5b\u67e5\u201d\u3002\u4f46\u540c\u6837\u5730\uff0c\u8fd9\u4e09\u7bc7\u90fd\u4e0d\u62a5 MCU \u7ea7\u8d44\u6e90\u6307\u6807\uff0c\u4e0d\u80fd\u62ff\u6765\u505a\u8d44\u6e90\u5bf9\u6bd4\u3002")

    heading(doc, "\u4e94\u3001\u6587\u732e\u5e95\u5ea7\u7684\u53ef\u590d\u73b0\u8bc1\u636e\u94fe", 1)
    para(doc, "\u4e3a\u907f\u514d\u201c\u8bfb\u4e86\u5f88\u591a\u4f46\u8bf4\u4e0d\u6e05\u8bfb\u4e86\u54ea\u4e9b\u201d\uff0c\u8fd9\u8f6e\u628a\u68c0\u7d22\u8fc7\u7a0b\u4e5f\u843d\u76d8\u4e86\u3002\u5173\u952e\u6570\u5b57\u5982\u4e0b\uff08\u5747\u53ef\u5728 literature/ \u4e0b\u56de\u67e5\uff09\uff1a")

    table(doc,
          ["\u4ea7\u51fa", "\u5185\u5bb9", "\u4f4d\u7f6e"],
          [
              ["\u68c0\u7d22\u65e5\u5fd7", "\u68c0\u7d22\u534f\u8bae\u4e03\u8981\u7d20\u3001\u5404\u8f6e\u547d\u4e2d\u4e0e\u53bb\u91cd\u8bb0\u5f55\uff08\u542b\u5931\u8d25\u7684\u68c0\u7d22\u5f0f\u4e0e\u9650\u989d\u539f\u56e0\uff09", "literature/search-log.md"],
              ["P1 \u5019\u9009\u5f15\u7528\u5e93", "98 \u6761\u552f\u4e00\u8bb0\u5f55\uff08= 75 \u4e3b\u8bb0\u5f55 + 23 \u65e7\u5e93\u72ec\u6709\uff09\uff0c\u5408\u8868\u62a5\u544a\u540c\u76ee\u5f55", "literature/library/P1-library.jsonl"],
              ["\u6587\u732e\u56fe", "50 \u7bc7\u671f\u520a + 18 \u6761\u9644\u5f55\uff0cDOI \u9010\u6761\u7ecf Crossref \u6838\u9a8c", "literature/\u6587\u732e\u9700\u6c42-50\u7bc7\u9876\u520a.md"],
              ["\u9010\u7bc7\u7cbe\u8bfb\u8bb0\u5f55", "\u7b2c\u4e8c\u6b21\u7ec4\u4f1a\u4e3b\u9898 23 \u7bc7 + 2024+ \u589e\u91cf\u5206\u8bca\u82e5\u5e72", "literature/meeting2/notes/"],
              ["\u6807\u51c6\u5316\u9650\u5b9a\u8bed", "6 \u7bc7\u6838\u5fc3\u6587\u732e\u7684\u9010\u5b57\u9650\u5b9a\u8bed\uff0c\u5199\u7a3f\u5f15\u7528\u65f6\u5fc5\u987b\u5e26\u4e0a", "literature/notes/citation-qualifiers.md"],
              ["\u53ef\u7f16\u8bd1\u5f15\u7528", "BibTeX\uff0c\u4f9b Zotero/\u6295\u7a3f\u6a21\u677f\u76f4\u63a5\u4f7f\u7528", "literature/refs.bib"],
          ],
          widths=[3.2, 9.6, 5.4], size=9)
    caption(doc, "\u8868 3\u3000\u6587\u732e\u5e95\u5ea7\u7684\u4ea7\u51fa\u4e0e\u4f4d\u7f6e")

    para(doc, "\u9700\u8981\u8bf4\u6e05\u695a\u4e24\u6761\u9650\u5236\u3002\u7b2c\u4e00\uff0c\u68c0\u7d22\u5e73\u53f0 OpenAlex \u7684\u533f\u540d\u989d\u5ea6\u5728\u524d\u4e24\u8f6e\u7528\u5c3d\uff0c\u5bfc\u81f4\u201c\u5f15\u6587\u5c55\u5f00\uff08\u8be5\u6587\u88ab\u8c01\u5f15\u7528\u3001\u662f\u5426\u88ab\u72ec\u7acb\u590d\u73b0\uff09\u201d\u8fd9\u4e00\u6b65\u672c\u6b21\u6ca1\u80fd\u505a\uff0c\u7cbe\u8bfb\u8bb0\u5f55\u91cc\u7684\u201c\u5916\u90e8\u590d\u73b0\u201d\u5217\u56e0\u6b64\u7edf\u4e00\u5199\u201c\u672a\u68c0\u201d\u2014\u2014\u8fd9\u662f\u4fe1\u606f\u7f3a\u5931\uff0c\u4e0d\u7b49\u4e8e\u201c\u65e0\u5916\u90e8\u8bc1\u636e\u201d\uff0c\u989d\u5ea6\u91cd\u7f6e\u540e\u5e94\u8865\u3002\u7b2c\u4e8c\uff0c\u7b2c\u56db\u8f6e\u7528 Crossref \u8865\u68c0\u5d4c\u5165\u5f0f\u90e8\u7f72\u4e3b\u9898\uff0c\u4f46 Crossref \u65e0\u6cd5\u5728\u4e3b\u9898\u5185\u6309\u88ab\u5f15\u6392\u5e8f\uff0c\u8be5\u8f6e\u5019\u9009\u7684\u7b5b\u9009\u5f3a\u5ea6\u4f4e\u4e8e\u539f 50 \u7bc7\uff0c\u56e0\u6b64\u8d44\u6e90\u7c7b\u6307\u6807\uff08\u5ef6\u8fdf\u3001\u5185\u5b58\uff09\u7684\u53ef\u884c\u6027\u7ed3\u8bba\u4e0d\u80fd\u53ea\u9760\u8fd9\u4e00\u8f6e\u4e0b\u5b9a\u8bba\u3002")

    heading(doc, "\u516d\u3001\u5bf9\u7b2c\u4e00\u7bc7\u8bba\u6587\u7684\u51c0\u5f71\u54cd", 1)
    para(doc, "\u628a\u4e0a\u9762\u4e09\u6761\u786c\u7ea6\u675f\u548c\u6307\u6807\u53d1\u73b0\u5408\u8d77\u6765\uff0cP1 \u7684\u65ad\u8a00\u8303\u56f4\u53d1\u751f\u4e86\u4ee5\u4e0b\u53d8\u5316\uff1a")

    table(doc,
          ["\u9879", "\u4fee\u6b63\u524d\uff08\u84dd\u56fe/\u521d\u7248\u9aa8\u67b6\uff09", "\u4fee\u6b63\u540e\uff08\u73b0\u884c\u53e3\u5f84\uff09", "\u4f9d\u636e"],
          [
              ["\u53c2\u6570\u91cf", "\u201c\u53c2\u6570\u91cf\u5c0f\u4e8e 500 KB\u201d", "\u672a\u5b9e\u6d4b\u524d\u4e0d\u5f97\u5199\uff1b\u82e5\u5199\u987b\u6807\u91cf\u5316\u7cbe\u5ea6\u4e0e\u662f\u5426\u542b\u611f\u77e5\u5934", "AGENTS.md \u00a71\u3001literature/notes/p01-cfc-nmi2022.md"],
              ["\u5ef6\u8fdf\u4e0e MCU", "\u201c\u5b9e\u6d4b\u5ef6\u8fdf <1 ms\uff0c\u7ed9\u51fa\u8f66\u89c4\u90e8\u7f72\u8def\u5f84\u201d", "\u672a\u62ff\u5230\u677f\u5b50\u524d\u53ea\u5199\u76ee\u6807\uff1b\u4e0d\u8fdb\u5165\u4e0e\u4ed6\u4eba\u7684\u5bf9\u6bd4\u8868", "AGENTS.md \u00a71/\u00a73\u3001\u98ce\u9669 R20"],
              ["\u672f\u8bed", "\u201c\u7269\u7406\u4fe1\u606f\u9a71\u52a8\u7684 ODE \u8fb9\u754c\u6761\u4ef6\u201d", "structure-informed / prior-informed / boundary-conditioned\uff1bOTF \u5b9a\u4f4d\u4e3a\u5f15\u5bfc\u6027\u504f\u7f6e", "AGENTS.md \u00a71\u3001literature/notes/p07-pinn-ctrl-neucom2024.md"],
              ["\u65f6\u95f4\u7a97\u51fd\u6570\u8bc1\u636e", "\u5f15\u5b66\u4f4d\u8bba\u6587\u7684\u52a8\u6001\u65f6\u95f4\u7a97\u51fd\u6570", "\u533a\u5206\u4e24\u7c7b\u8bc1\u636e\uff1a\u5b9e\u8f66 OTF \u5206\u5e03\uff08\u7b2c 3.2.1 \u8282\uff09vs \u6a21\u62df\u5668\u6807\u5b9a\u7684\u7a97\u51fd\u6570\uff08\u7b2c 3.2.2 \u8282\uff0c40 \u540d\u9a7e\u9a76\u4eba\uff09", "audit/\u7b2c\u4e00\u6b21\u7ec4\u4f1a/00-asset-inventory.md M2"],
              ["\u5206\u7c7b\u5668\u589e\u76ca\u53e3\u5f84", "\u201cOTF \u589e\u76ca 1.0\u20131.7%\u201d", "+1.0 ~ +5.5 \u4e2a\u767e\u5206\u70b9\uff08\u5206\u7c7b\u5668\u51c6\u786e\u7387\uff0c\u8bba\u6587\u62a5\u544a\u503c\uff0c\u672a\u7ecf\u6211\u4eec\u590d\u73b0\uff09", "AGENTS.md \u00a71\u3001\u8bba\u6587\u8868 4.2\u20134.4"],
              ["\u7a33\u5b9a\u6027\u8bba\u8bc1", "\uff08\u539f\u672c\u65e0\u6b64\u9879\uff09", "\u82e5\u58f0\u79f0\u7a33\u5b9a\u6027\uff0c\u987b\u62a5\u9010\u8f66\u8bef\u5dee\u4f20\u64ad\u66f2\u7ebf\uff1bRMSE \u5c0f \u2260 \u5f26\u7a33\u5b9a", "literature/notes/p33-lpstring-tcst2014.md"],
          ],
          widths=[2.8, 4.6, 6.6, 3.8], size=9)
    caption(doc, "\u8868 4\u3000P1 \u65ad\u8a00\u8303\u56f4\u7684\u4fee\u6b63\u5bf9\u7167")

    heading(doc, "\u4e03\u3001\u4e0b\u4e00\u6b65\u5b89\u6392", 1)
    table(doc,
          ["\u9636\u6bb5", "\u4efb\u52a1", "\u5b8c\u6210\u5224\u636e", "\u4f9d\u8d56"],
          [
              ["\u7b2c 1\u20132 \u5468", "\u628a\u4e09\u6761\u786c\u7ea6\u675f\u5199\u8fdb\u5199\u4f5c\u6a21\u677f\uff1b\u6309\u65b0\u53e3\u5f84\u91cd\u67e5\u7b2c\u4e00\u6b21\u7ec4\u4f1a\u6750\u6599\u4e0e\u9aa8\u67b6", "\u4efb\u4f55\u6587\u4ef6\u91cc\u4e0d\u518d\u51fa\u73b0\u201c<500 KB\u201d\u201c<1 ms\u201d\u201cphysics-informed\u201d\u65e0\u9650\u5b9a\u8bed\u7684\u7528\u6cd5", "\u65e0"],
              ["\u7b2c 3\u20134 \u5468", "\u8865 OpenAlex \u5f15\u6587\u5c55\u5f00\uff08\u6bcf\u65e5\u989d\u5ea6\u91cd\u7f6e\u540e\uff09\uff0c\u628a\u7cbe\u8bfb\u8bb0\u5f55\u7684\u201c\u5916\u90e8\u590d\u73b0\u201d\u5217\u4ece\u201c\u672a\u68c0\u201d\u5347\u7ea7", "\u6bcf\u7bc7\u7ed9\u51fa\u540c\u5411/\u53cd\u5411\u5f15\u7528\u6570\u4e0e\u4ee3\u8868\u4f5c", "OpenAlex \u989d\u5ea6"],
              ["\u7b2c 5\u20136 \u5468", "\u628a\u8868 2 \u7684\u4e0d\u53ef\u5bf9\u6807\u9879\u5199\u6210 P1 \u7684\u6307\u6807\u7ae0\u7a0b\uff1b\u786e\u5b9a\u662f\u5426\u8865\u632f\u8361\u963b\u5c3c\u6bd4\u4e0e\u4ea4\u901a\u6d41\u7a33\u5b9a\u6027", "\u6307\u6807\u6e05\u5355\u5b9a\u7a3f\uff0c\u4e0d\u53ef\u6bd4\u9879\u660e\u786e\u6807\u4e3a\u201c\u4e0d\u8fdb\u5165\u5bf9\u6bd4\u8868\u201d", "\u65e0"],
              ["\u7b2c 7\u20138 \u5468", "\u628a\u7b2c\u4e00\u6b21\u7ec4\u4f1a\u7684\u56db\u6bb5\u5f0f\u8ba1\u5212\u5347\u7ea7\u4e3a 24 \u5468\u9010\u5468\u8ba1\u5212", "\u6bcf\u5468\u4e00\u884c\uff08\u76ee\u6807/\u4ea4\u4ed8\u7269/\u5224\u636e/\u4f9d\u8d56/\u98ce\u9669\uff09\uff0c\u4e0e\u7b2c\u4e00\u6b21\u7ec4\u4f1a\u7684\u9636\u6bb5\u5212\u5206\u4e00\u81f4", "\u7b97\u529b\u4e0e TD3 \u8def\u7ebf\u5df2\u51b3"],
          ],
          widths=[2.4, 6.6, 5.6, 3.0], size=9)
    caption(doc, "\u8868 5\u3000\u672c\u8f6e\u4e4b\u540e\u7684\u56db\u6b65\u5b89\u6392")

    heading(doc, "\u516b\u3001\u9700\u8981\u8001\u5e08\u5b9a\u7684\u4e09\u4ef6\u4e8b", 1)
    para(doc, "\u4e00\u662f\u6307\u6807\u8865\u5145\uff1aP1 \u662f\u5426\u8865\u62a5\u632f\u8361\u963b\u5c3c\u6bd4\u4e0e\u4ea4\u901a\u6d41\u7a33\u5b9a\u6027\u8fd9\u4e24\u9879\uff1f\u5b83\u4eec\u6bd4 RMSE \u66f4\u8d34\u8fd1\u201c\u7f16\u961f\u63a7\u5236\u201d\u7684\u672c\u4f53\u3002\u4e8c\u662f\u53c2\u6570\u9884\u7b97\u53e3\u5f84\uff1a\u82e5\u5b9e\u6d4b\u540e\u5168\u6a21\u578b\u8d85\u4e86 500 KB\uff0c\u662f\u63a5\u53d7 fp16/\u91cf\u5316\uff08\u5e76\u62a5\u7cbe\u5ea6\u635f\u5931\uff09\uff0c\u8fd8\u662f\u6539\u53ea\u62a5\u9012\u5f52\u5206\u91cf\uff1f\u4e09\u662f\u7b97\u529b\u8def\u7ebf\uff1a\u4e91\u7aef\u79df\u7528\u8fd8\u662f\u5148\u964d\u7ea7\u4e3a\u5f00\u73af\u56de\u653e\u4e0e\u89c4\u5219\u5c42\u9a8c\u8bc1\u3002\u8fd9\u4e09\u4ef6\u5206\u522b\u51b3\u5b9a\u5bf9\u6bd4\u8868\u5f62\u6001\u3001\u5de5\u7a0b\u4e3b\u5f20\u7684\u5199\u6cd5\u548c\u65f6\u95f4\u8868\u3002")

    doc.add_page_break()
    heading(doc, "\u9644\u4ef6\uff1a\u672c\u6587\u6570\u636e\u4e0e\u4e8b\u5b9e\u7684\u6765\u6e90", 1)
    table(doc,
          ["\u6570\u636e\u6216\u4e8b\u5b9e", "\u6765\u6e90"],
          [
              ["CfC \u53c2\u6570\u91cf 4 184 / 230 828\u3001\u65e0\u786c\u4ef6\u4e0e\u65e0\u95ed\u73af\u6307\u6807", "literature/notes/p01-cfc-nmi2022.md\u3001literature/meeting2/notes/cfc-nmi2022.md"],
              ["Chahine \u56db\u65cb\u7ffc\u771f\u673a\u95ed\u73af\uff08CfC \u63a7\u5236\u5668\u3001Jetson TX2\u3001\u65e0\u53c2\u6570\u91cf/\u9891\u7387/\u65f6\u5ef6\uff09", "literature/meeting2/notes/scirebotics2023-chahine-lnn-flight.md"],
              ["PINC \u7528\u8f6f\u635f\u5931\u9879\u3001\u4e14\u672a\u505a\u7269\u7406\u9879\u5173\u95ed\u6d88\u878d", "literature/notes/p07-pinn-ctrl-neucom2024.md"],
              ["Lp \u5f26\u7a33\u5b9a\u5224\u636e\u4ec5\u5bf9 LTI \u6210\u7acb\u3001\u5173\u952e\u6570\u503c\u6765\u81ea\u5355\u6b21\u5b9e\u9a8c", "literature/notes/p33-lpstring-tcst2014.md"],
              ["\u7aef\u5230\u7aef\u5ef6\u8fdf\u4e0e MCU \u5185\u5b58\u5728\u540c\u7c7b\u6587\u732e\u4e2d\u65e0\u5bf9\u6807\u7269", "literature/notes/p45-deeplcc-tcst2023.md\u3001literature/fresh2024/notes/electronics2026-overtaking-hierarchical-rl.md"],
              ["\u56db\u9879\u8bc4\u4ef7\u534f\u8bae\uff08\u632f\u8361\u963b\u5c3c\u6bd4\u3001\u8212\u9002\u6210\u672c\u3001\u80fd\u8017\u3001\u4ea4\u901a\u6d41\u7a33\u5b9a\u6027\uff09\u53ef\u590d\u7528", "literature/fresh2024/notes/natcommun2025-platoon-knowledge-guided.md"],
              ["TD3 \u539f\u6587\u65e0\u5ef6\u8fdf\u4e0e\u5185\u5b58\u6307\u6807", "literature/meeting2/notes/icml2018-td3.md"],
              ["\u68c0\u7d22\u5404\u8f6e\u547d\u4e2d\u4e0e\u53bb\u91cd\u3001OpenAlex \u989d\u5ea6\u8017\u5c3d\u5bfc\u81f4\u5f15\u6587\u5c55\u5f00\u672a\u505a", "literature/search-log.md"],
              ["\u5b66\u4f4d\u8bba\u6587\u5206\u7c7b\u5668\u589e\u76ca\u4e0e\u52a8\u6001\u65f6\u95f4\u7a97\u6807\u5b9a\u6765\u6e90", "sources/thesis-huang2023.fulltext.txt\uff08\u884c\u53f7\u89c1 audit/\u7b2c\u4e00\u6b21\u7ec4\u4f1a/00-asset-inventory.md\uff09"],
          ],
          widths=[6.4, 11.2], size=9)
    caption(doc, "\u8868 6\u3000\u6570\u636e\u4e0e\u4e8b\u5b9e\u6765\u6e90\u5bf9\u7167")

    para(doc, "\u9700\u8981\u63d0\u9192\u4e00\u53e5\uff1a\u672c\u6587\u5f15\u7528\u7684\u6240\u6709\u4ed6\u4eba\u6570\u5b57\u90fd\u662f\u6587\u732e\u62a5\u544a\u503c\uff0c\u4e14\u591a\u6570\u672a\u7ecf\u72ec\u7acb\u590d\u7b97\uff08\u4ec5 CfC \u53c2\u6570\u91cf\u4e00\u5904\u505a\u4e86\u6b63\u5f0f\u7248\u8bfb\u56fe\u6838\u5bf9\uff09\uff1b\u6295\u7a3f\u65f6\u5fc5\u987b\u6309\u9879\u76ee\u7ea6\u5b9a\u6807\u201c\u6587\u732e\u62a5\u544a\u503c\uff0c\u534f\u8bae\u4e0d\u540c\uff0c\u4e0d\u53ef\u76f4\u63a5\u6bd4\u8f83\u201d\u3002")

    # 页脚页码
    try:
        from docx.oxml.ns import qn as _qn
        sec = doc.sections[0]
        footer = sec.footer
        fp = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = fp.add_run()
        style_run(run, size=9)
        fld = run._element.makeelement(_qn("w:fldSimple"), {_qn("w:instr"): "PAGE"})
        run._element.addnext(fld)
    except Exception as exc:
        print("footer skipped: %s" % exc)

    os.makedirs(OUT_DIR, exist_ok=True)
    doc.save(OUT_PATH)
    print("SAVED: %s" % OUT_PATH)
    print("size: %d bytes | paragraphs: %d | tables: %d" % (os.path.getsize(OUT_PATH), len(doc.paragraphs), len(doc.tables)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
