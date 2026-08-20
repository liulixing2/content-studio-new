import re


HEADING_PATTERN = re.compile(r"^([一二三四五六七八九十]+[、.．]|[0-9]+[、.．])\s*(.+)")


def import_pasted_article(title, pasted_text, keywords):
    lines = [line.strip() for line in str(pasted_text or "").splitlines()]
    lines = [line for line in lines if line]
    summary = ""
    sections = []
    current_section = None

    for line in lines:
        if line.startswith("摘要：") or line.startswith("摘要:"):
            summary = line.split("：", 1)[-1] if "：" in line else line.split(":", 1)[-1]
            continue

        heading_match = HEADING_PATTERN.match(line)
        if heading_match:
            if current_section:
                sections.append(current_section)
            current_section = {
                "heading": line,
                "paragraphs": [],
                "image_hint": "根据本段内容生成原创信息图或氛围插图，避免未授权素材。",
            }
            continue

        if current_section is None:
            current_section = {
                "heading": "一、正文开头",
                "paragraphs": [],
                "image_hint": "根据开头主题生成原创封面或信息图，避免未授权素材。",
            }
        current_section["paragraphs"].append(line)

    if current_section:
        sections.append(current_section)

    if not summary:
        summary = sections[0]["paragraphs"][0][:120] if sections and sections[0]["paragraphs"] else ""

    return {
        "title": title or "未命名公众号文章",
        "summary": summary,
        "sections": sections,
        "interaction": "你对这个话题怎么看？欢迎在评论区聊聊。",
        "copyright_notes": [
            "正文为用户粘贴导入的临时内容，保存前请人工确认事实和版权。",
            "配图默认使用原创生成图或自有授权素材。",
        ],
        "source_keywords": keywords,
    }
