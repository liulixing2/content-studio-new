from html import escape


def render_article_template(article):
    title = escape(article.get("title") or "")
    summary = escape(article.get("summary") or "")
    html_parts = [
        '<article class="wechat-article">',
        "<h1>%s</h1>" % title,
        '<p class="summary">%s</p>' % summary,
    ]
    text_parts = ["摘要：%s" % (article.get("summary") or "")]
    for section in article.get("sections", []):
        heading = section.get("heading") or ""
        html_parts.append("<h2>%s</h2>" % escape(heading))
        text_parts.extend(["", heading])
        for paragraph in section.get("paragraphs", []):
            html_parts.append("<p>%s</p>" % escape(paragraph))
            text_parts.append(paragraph)
        if section.get("image_hint"):
            hint = "配图建议：%s" % section["image_hint"]
            html_parts.append('<blockquote class="image-hint">%s</blockquote>' % escape(hint))
            text_parts.append(hint)
    if article.get("interaction"):
        html_parts.append('<p class="interaction">%s</p>' % escape(article["interaction"]))
        text_parts.extend(["", "互动引导：%s" % article["interaction"]])
    html_parts.append("</article>")
    return {"html": "\n".join(html_parts), "text": "\n".join(text_parts)}
