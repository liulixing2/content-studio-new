import re


HEADING_PATTERN = re.compile(r"^(#{1,3}\s*)?(([一二三四五六七八九十]+|[0-9]+)[、.．、]\s*)?(.{2,48})$")
LABEL_PATTERN = re.compile(r"^(标题|摘要|导语|互动引导|互动|评论引导|素材说明|图片说明|版权提示|版权说明|参考来源)[:：]\s*(.*)$")


def _clean_line(value):
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text.strip("-*# ")


def _is_heading(line):
    if len(line) > 52:
        return False
    if line.startswith(("一、", "二、", "三、", "四、", "五、", "六、", "七、", "八、", "九、", "十、")):
        return True
    if re.match(r"^[0-9]+[、.．]\s*\S+", line):
        return True
    if line.startswith(("## ", "### ")):
        return True
    return False


def _strip_heading_marker(line):
    text = line.lstrip("#").strip()
    return text


def _fallback_sections(paragraphs):
    if not paragraphs:
        return []

    if len(paragraphs) <= 2:
        groups = [paragraphs]
        headings = ["一、正文"]
    else:
        first = max(1, len(paragraphs) // 3)
        second = max(first + 1, (len(paragraphs) * 2) // 3)
        groups = [paragraphs[:first], paragraphs[first:second], paragraphs[second:]]
        headings = ["一、开头切入", "二、正文展开", "三、结尾收束"]

    sections = []
    for heading, group in zip(headings, groups):
        if not group:
            continue
        sections.append({"heading": heading, "paragraphs": group, "image_hint": ""})
    return sections


def import_pasted_article(title, pasted_text, keywords):
    lines = [_clean_line(line) for line in str(pasted_text or "").splitlines()]
    lines = [line for line in lines if line]
    summary = ""
    detected_title = ""
    interaction = ""
    copyright_notes = []
    sections = []
    current_section = None
    leading_paragraphs = []

    for line in lines:
        label_match = LABEL_PATTERN.match(line)
        if label_match:
            label, value = label_match.groups()
            value = value.strip()
            if label == "标题" and value:
                detected_title = value
            elif label in ["摘要", "导语"] and value:
                summary = value
            elif label in ["互动引导", "互动", "评论引导"] and value:
                interaction = value
            elif value:
                copyright_notes.append(value if label in ["素材说明", "图片说明"] else "%s：%s" % (label, value))
            continue

        if not detected_title and not title and len(line) <= 42 and not _is_heading(line):
            detected_title = line
            continue

        if title and line == title:
            continue

        if _is_heading(line):
            if current_section:
                sections.append(current_section)
            current_section = {
                "heading": _strip_heading_marker(line),
                "paragraphs": [],
                "image_hint": "",
            }
            continue

        if current_section is None:
            leading_paragraphs.append(line)
        else:
            current_section["paragraphs"].append(line)

    if leading_paragraphs:
        if sections or current_section:
            sections.insert(0, {"heading": "一、开头切入", "paragraphs": leading_paragraphs, "image_hint": ""})
        else:
            sections.extend(_fallback_sections(leading_paragraphs))

    if current_section:
        sections.append(current_section)

    if not summary:
        summary = sections[0]["paragraphs"][0][:120] if sections and sections[0]["paragraphs"] else ""

    if not interaction:
        interaction = "你对这个话题怎么看？欢迎在评论区聊聊。"

    if not copyright_notes:
        copyright_notes = [
            "正文为用户粘贴导入的临时内容，保存前请人工确认事实和版权。",
            "配图默认使用原创生成图或自有授权素材。",
        ]

    return {
        "title": title or detected_title or "未命名公众号文章",
        "summary": summary,
        "sections": sections,
        "interaction": interaction,
        "copyright_notes": copyright_notes,
        "source_keywords": keywords,
    }
