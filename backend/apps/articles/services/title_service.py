def mock_titles(direction):
    title = direction.get("title") or "公众号选题"
    keywords = direction.get("keywords") or []
    first = keywords[0] if keywords else title
    return [
        "%s：为什么现在还值得重新讨论" % first,
        "重看%s，真正留下来的不只是热闹" % first,
        "%s背后，读者真正想聊的是什么" % first,
        "从%s开始，重新整理一篇可发布的公众号文章" % first,
    ]
