from .keyword_service import split_keywords


def mock_article(title, keywords):
    words = split_keywords(keywords)
    first = words[0] if words else title
    sections = [
        {
            "heading": "一、先回答标题里的问题",
            "paragraphs": [
                "这篇文章先不急着堆资料，而是从读者为什么会点开这个标题开始。",
                "%s能被重新提起，往往不是因为它只有一个标签，而是因为它还能带出具体记忆和讨论。" % first,
            ],
            "image_hint": "标题问题信息图，避免使用未授权截图。",
        },
        {
            "heading": "二、正文要围绕具体切口展开",
            "paragraphs": [
                "项目会把 AI 返回的结构化正文套入公众号模板，段落、标题和配图位置由项目控制。",
                "当前内容只是 mock 预览，不会自动保存。只有用户确认后，才会写入作品库。",
            ],
            "image_hint": "段落关键词文字卡或信息图。",
        },
    ]
    return {
        "title": title,
        "summary": "围绕“%s”生成一篇公众号文章草稿，当前仅用于框架预览。" % first,
        "sections": sections,
        "interaction": "你觉得这个选题最值得展开的是哪一点？",
        "copyright_notes": ["默认不使用未授权截图、剧照、海报或明星照片。"],
    }
