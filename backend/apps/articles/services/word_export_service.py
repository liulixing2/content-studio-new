from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile
from xml.sax.saxutils import escape


def _paragraph(text, style=None):
    style_xml = ""
    if style:
        style_xml = '<w:pPr><w:pStyle w:val="%s"/></w:pPr>' % escape(style)
    return "<w:p>%s<w:r><w:t>%s</w:t></w:r></w:p>" % (style_xml, escape(str(text or "")))


def _document_xml(article):
    title = article.get("title") or "未命名公众号文章"
    summary = article.get("summary") or ""
    sections = article.get("sections") or []
    copyright_notes = article.get("copyright_notes") or []

    body = [_paragraph(title, "Title")]
    if summary:
        body.append(_paragraph("摘要：%s" % summary))

    for section in sections:
        heading = section.get("heading") or ""
        if heading:
            body.append(_paragraph(heading, "Heading1"))
        for paragraph in section.get("paragraphs", []):
            body.append(_paragraph(paragraph))
        if section.get("image_hint"):
            body.append(_paragraph("配图建议：%s" % section["image_hint"]))

    if article.get("interaction"):
        body.append(_paragraph("互动引导：%s" % article["interaction"]))

    if copyright_notes:
        body.append(_paragraph("版权说明", "Heading1"))
        for note in copyright_notes:
            body.append(_paragraph(note))

    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    %s
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>""" % "\n".join(body)


def build_article_docx(article):
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as docx:
        docx.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>""",
        )
        docx.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>""",
        )
        docx.writestr("word/document.xml", _document_xml(article))
    return buffer.getvalue()
