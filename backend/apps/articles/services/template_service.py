from html import escape


ARTICLE_STYLE = "margin:0 auto;padding:8px 0 24px;max-width:677px;color:#1f2937;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Microsoft YaHei',Arial,sans-serif;line-height:1.85;font-size:16px;"
TITLE_STYLE = "margin:0 0 18px;color:#111827;font-size:24px;line-height:1.35;font-weight:700;text-align:left;"
SUMMARY_STYLE = "margin:0 0 22px;padding:12px 14px;border-left:4px solid #2563eb;background:#f8fafc;color:#475569;font-size:15px;line-height:1.8;"
HEADING_STYLE = "margin:28px 0 14px;padding:0 0 0 10px;border-left:4px solid #2563eb;color:#111827;font-size:19px;line-height:1.5;font-weight:700;"
PARAGRAPH_STYLE = "margin:0 0 16px;color:#1f2937;font-size:16px;line-height:1.9;text-align:justify;"
INTERACTION_STYLE = "margin:26px 0 18px;padding:14px 16px;border-radius:6px;background:#eff6ff;color:#1d4ed8;font-size:16px;line-height:1.8;font-weight:700;"
NOTES_STYLE = "margin:22px 0 0;padding-top:12px;border-top:1px solid #e5e7eb;color:#6b7280;font-size:13px;line-height:1.7;"


def render_article_template(article):
    title = escape(article.get("title") or "")
    summary = escape(article.get("summary") or "")
    html_parts = [
        '<article class="wechat-article" style="%s">' % ARTICLE_STYLE,
        '<h1 style="%s">%s</h1>' % (TITLE_STYLE, title),
    ]
    text_parts = [article.get("title") or ""]
    if summary:
        html_parts.append('<p class="summary" style="%s"><strong>摘要：</strong>%s</p>' % (SUMMARY_STYLE, summary))
        text_parts.extend(["", "摘要：%s" % (article.get("summary") or "")])

    for section in article.get("sections", []):
        heading = section.get("heading") or ""
        if not section.get("paragraphs"):
            continue
        html_parts.append('<h2 style="%s">%s</h2>' % (HEADING_STYLE, escape(heading)))
        text_parts.extend(["", heading])
        for paragraph in section.get("paragraphs", []):
            html_parts.append('<p style="%s">%s</p>' % (PARAGRAPH_STYLE, escape(paragraph)))
            text_parts.append(paragraph)

    if article.get("interaction"):
        html_parts.append('<p class="interaction" style="%s">%s</p>' % (INTERACTION_STYLE, escape(article["interaction"])))
        text_parts.extend(["", "互动引导：%s" % article["interaction"]])

    copyright_notes = [note for note in article.get("copyright_notes", []) if note]
    if copyright_notes:
        note_text = " ".join(copyright_notes)
        html_parts.append('<p class="copyright-notes" style="%s">素材说明：%s</p>' % (NOTES_STYLE, escape(note_text)))
        text_parts.extend(["", "素材说明：%s" % note_text])

    html_parts.append("</article>")
    return {"html": "\n".join(html_parts), "text": "\n".join(text_parts)}
