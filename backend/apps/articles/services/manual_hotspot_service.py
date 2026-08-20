import re

from .keyword_service import split_keywords


def _clean_hotspot_line(line):
    text = re.sub(r"\s+", " ", str(line or "")).strip()
    text = re.sub(r"^[#\-*0-9.、\s]+", "", text)
    return text[:80]


def build_directions_from_manual_hotspots(keywords, pasted_text):
    base_keywords = split_keywords(keywords)
    lines = [_clean_hotspot_line(line) for line in str(pasted_text or "").splitlines()]
    lines = [line for line in lines if len(line) >= 4]
    unique_lines = list(dict.fromkeys(lines))[:8]

    directions = []
    for index, line in enumerate(unique_lines, start=1):
        related_keywords = list(dict.fromkeys(base_keywords + split_keywords(line)))[:8]
        directions.append(
            {
                "title": "手动热点 %s：%s" % (index, line[:28]),
                "reader_question": "读者为什么会关注“%s”？" % line[:32],
                "angle": "基于用户从平台手动复制的热点文本整理，后续需要人工确认来源和时效。",
                "keywords": related_keywords,
                "article_type": "manual_hotspot",
                "avoid": ["不要伪装成自动抓取热点", "不要引用未核实来源", "不要使用未授权素材"],
                "source_text": line,
            }
        )

    return {
        "directions": directions,
        "saved": False,
        "source": "manual_paste",
        "message": "手动粘贴内容已整理为临时方向，尚未保存。",
    }
