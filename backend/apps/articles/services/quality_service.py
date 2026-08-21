TEMPLATE_PHRASES = [
    "标题讨论点、观看现场、重看后劲",
    "它的价值不只是“发生过”",
    "它的价值不只是发生过",
    "更像一个时代入口",
    "能被读者接住的问题",
    "一听到这个词就能补出声音、画面和当时的心情",
]

GENERIC_PHRASES = [
    "片头、角色出场和某个一眼能认出的瞬间",
    "它怎样进入过一代人的日常",
    "不是资料，而是后劲",
]


def check_article_quality(article):
    issues = []
    suggestions = []
    title = article.get("title") or ""
    summary = article.get("summary") or ""
    sections = article.get("sections") or []
    full_text = "\n".join(
        [title, summary]
        + [section.get("heading", "") for section in sections]
        + [paragraph for section in sections for paragraph in section.get("paragraphs", [])]
    )

    if len(title) < 8:
        issues.append({"level": "high", "message": "标题太短，缺少明确讨论点。"})
        suggestions.append("标题需要包含对象、矛盾或读者关心的问题。")

    if not summary or len(summary) < 30:
        issues.append({"level": "medium", "message": "摘要偏弱，不能快速说明文章价值。"})
        suggestions.append("摘要建议用 1 句话说明对象、角度和读者收益。")

    if len(sections) < 2:
        issues.append({"level": "high", "message": "正文段落层次不足，容易像半成品。"})
        suggestions.append("正文至少拆成开头和主体两个层次，结尾可以放在互动引导里。")
    elif len(sections) == 2:
        issues.append({"level": "low", "message": "正文层次偏短，如果是长文建议再增加一个展开段。"})
        suggestions.append("短文可以发布；如果要做深度稿，建议增加一个转折或观点段。")

    for phrase in TEMPLATE_PHRASES:
        if phrase in full_text:
            issues.append({"level": "high", "message": "检测到模板化残留：%s" % phrase})

    for phrase in GENERIC_PHRASES:
        if phrase in full_text:
            issues.append({"level": "medium", "message": "检测到偏空泛表达：%s" % phrase})

    repeated_count = full_text.count("很多人")
    if repeated_count >= 8:
        issues.append({"level": "medium", "message": "“很多人”出现过多，语气容易重复。"})
        suggestions.append("替换为更具体的观看场景、读者问题或事实信息。")

    if "未授权" not in full_text and "版权" not in full_text:
        issues.append({"level": "low", "message": "缺少版权或配图风险提示。"})
        suggestions.append("发布前补充配图来源和授权说明。")

    high_count = len([issue for issue in issues if issue["level"] == "high"])
    publishable = high_count == 0 and len(sections) >= 2

    return {
        "publishable": publishable,
        "score": max(0, 100 - high_count * 30 - (len(issues) - high_count) * 10),
        "issues": issues,
        "suggestions": suggestions,
        "saved": False,
    }
