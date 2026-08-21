STAGE_NAMES = {
    "hotspots": "热点与选题方向",
    "titles": "标题候选",
    "outline": "文章大纲",
    "draft_direct": "按标题生成正文",
    "draft": "公众号正文",
    "quality": "发布前质检",
    "image": "配图提示词",
}


def build_manual_prompt(stage, context):
    stage_name = STAGE_NAMES.get(stage, "公众号内容辅助")
    keywords = context.get("keywords") or ""
    title = context.get("title") or ""
    direction = context.get("direction") or {}
    draft_text = context.get("draft_text") or ""
    manual_hotspots = context.get("manual_hotspots") or ""
    template_type = context.get("template_type") or ""

    common_rules = [
        "请使用中文输出。",
        "不要编造来源，不要把本地素材伪装成网络热点。",
        "不要使用未授权剧照、海报、明星照片或高度还原角色脸的配图建议。",
        "内容要具体，避免套话、空话和重复句式。",
    ]

    if stage == "hotspots":
        task = [
            "请根据关键词整理可以写公众号文章的近期讨论切口。",
            "输出 6 个热点方向，每个方向包含：方向标题、读者会关心的问题、可写角度、相关关键词、需要避开的风险。",
            "如果无法确认是真实热点，请明确标注为待核实，不要伪装成热点。",
        ]
    elif stage == "titles":
        task = [
            "请基于选题方向生成 10 个公众号标题。",
            "标题要有差异：问题型、对比型、情绪型、观点型、清单型都要覆盖。",
            "每个标题后给一句适合的人群或点击理由。",
        ]
    elif stage == "outline":
        task = [
            "请基于标题生成一份公众号文章大纲。",
            "大纲要包含摘要、开头切口、3-5 个正文段落、结尾互动。",
            "每段说明要回答什么问题，不能只写泛泛的小标题。",
        ]
    elif stage == "draft":
        task = [
            "请基于标题和大纲生成一篇可发布公众号正文。",
            "要求段落自然，不要像模板填空；每段都要有具体画面、判断或信息增量。",
            "输出格式：标题、摘要、正文分段、互动引导、版权/配图注意事项。",
        ]
    elif stage == "draft_direct":
        task = [
            "请基于标题直接生成一篇可发布公众号正文，不需要先生成大纲。",
            "正文要围绕标题里的核心问题展开，避免泛泛盘点和模板句式。",
            "输出格式：标题、摘要、正文分段、互动引导、版权/配图注意事项。",
        ]
    elif stage == "quality":
        task = [
            "请检查这篇公众号文章是否可以直接发布。",
            "重点检查：标题和正文是否一致、是否空泛重复、是否像模板、是否有事实风险、是否有版权风险、配图建议是否合规。",
            "输出：结论、主要问题、修改建议、是否建议发布。",
        ]
    elif stage == "image":
        task = [
            "请根据正文生成公众号配图方案。",
            "不要建议使用未授权影视截图、动漫截图、官方海报、明星照片或高度还原角色脸。",
            "输出封面图提示词、正文插图提示词、版式建议、版权注意事项。",
        ]
    else:
        task = ["请根据上下文完成公众号内容辅助任务。"]

    prompt_lines = [
        "你是公众号内容编辑，请完成任务：%s。" % stage_name,
        "",
        "【关键词】",
        keywords or "无",
        "",
        "【已选标题】",
        title or "无",
        "",
        "【已选方向】",
        direction.get("title", "") if isinstance(direction, dict) else "",
        direction.get("angle", "") if isinstance(direction, dict) else "",
        "",
        "【已有正文】",
        draft_text or "无",
        "",
        "【手动素材/热词】",
        manual_hotspots or "无",
        "",
        "【期望模板】",
        template_type or "无",
        "",
        "【任务要求】",
    ]
    prompt_lines.extend(["- %s" % item for item in task])
    prompt_lines.extend(["", "【通用规则】"])
    prompt_lines.extend(["- %s" % item for item in common_rules])

    return {
        "stage": stage,
        "stage_name": stage_name,
        "prompt": "\n".join(prompt_lines).strip(),
        "saved": False,
        "usage_note": "当前只是生成手动 Prompt，不会调用 DeepSeek，也不会保存结果。",
    }
