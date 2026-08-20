from .keyword_service import split_keywords


def mock_directions(keywords):
    words = split_keywords(keywords)
    first = words[0] if words else "这个选题"
    return [
        {
            "title": "%s为什么值得重新写" % first,
            "reader_question": "读者为什么现在还会关心%s？" % first,
            "angle": "从读者记忆和当下讨论切入，避免资料复述。",
            "keywords": words[:5],
            "article_type": "hot_comment",
            "avoid": ["不要写成百科", "不要使用未授权图片"],
        },
        {
            "title": "把%s写成一篇可讨论文章" % first,
            "reader_question": "评论区能接住的问题是什么？",
            "angle": "先提出问题，再用具体段落回答。",
            "keywords": words[:5],
            "article_type": "wechat",
            "avoid": ["不要自动保存半成品", "不要使用未授权素材"],
        },
    ]
