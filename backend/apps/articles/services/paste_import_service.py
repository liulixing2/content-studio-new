import re


HEADING_PATTERN = re.compile(r"^(#{1,3}\s*)?(([一二三四五六七八九十]+|[0-9]+)[、.．、]\s*)?(.{2,48})$")
MARKER_ONLY_PATTERN = re.compile(r"^([一二三四五六七八九十]+|[0-9]+)[、.．、]\s*$")
LABEL_PATTERN = re.compile(r"^(标题|摘要|导语|互动话题|互动引导|互动|评论引导|素材说明|图片说明|版权提示|版权说明|参考来源)[:：]\s*(.*)$")
CHINESE_NUMBERS = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
DEFAULT_HEADING_TAILS = ["具体场景", "核心观点", "重看理解", "读者互动"]


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


def _strip_heading_marker(line, index=0):
    text = line.lstrip("#").strip()
    marker_match = MARKER_ONLY_PATTERN.match(text)
    if marker_match:
        marker = CHINESE_NUMBERS[index] if index < len(CHINESE_NUMBERS) else str(index + 1)
        tail = DEFAULT_HEADING_TAILS[index] if index < len(DEFAULT_HEADING_TAILS) else "正文"
        return "%s、%s" % (marker, tail)
    return text


def _renumber_heading(heading, index):
    marker = CHINESE_NUMBERS[index] if index < len(CHINESE_NUMBERS) else str(index + 1)
    clean = re.sub(r"^(#{1,3}\s*)?(([一二三四五六七八九十]+|[0-9]+)[、.．、]\s*)", "", str(heading or "")).strip()
    if not clean:
        clean = DEFAULT_HEADING_TAILS[index] if index < len(DEFAULT_HEADING_TAILS) else "正文"
    return "%s、%s" % (marker, clean)


def _renumber_sections(sections):
    cleaned = []
    for section in sections:
        paragraphs = [paragraph for paragraph in section.get("paragraphs", []) if paragraph]
        if not paragraphs:
            continue
        cleaned.append(
            {
                "heading": _renumber_heading(section.get("heading"), len(cleaned)),
                "paragraphs": paragraphs,
                "image_hint": section.get("image_hint", ""),
            }
        )
    return cleaned


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
        headings = ["一、具体场景", "二、核心观点", "三、读者互动"]

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
            elif label in ["互动话题", "互动引导", "互动", "评论引导"] and value:
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
                "heading": _strip_heading_marker(line, len(sections)),
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
            sections.insert(0, {"heading": "一、具体场景", "paragraphs": leading_paragraphs, "image_hint": ""})
        else:
            sections.extend(_fallback_sections(leading_paragraphs))

    if current_section:
        sections.append(current_section)

    sections = _renumber_sections(sections)

    if not summary:
        summary = sections[0]["paragraphs"][0][:120] if sections and sections[0]["paragraphs"] else ""

    return {
        "title": title or detected_title or "未命名公众号文章",
        "summary": summary,
        "sections": sections,
        "interaction": interaction,
        "copyright_notes": copyright_notes,
        "source_keywords": keywords,
    }
