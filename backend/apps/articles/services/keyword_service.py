def split_keywords(value):
    text = str(value or "").replace("，", ",").replace("、", ",")
    return [item.strip() for item in text.split(",") if item.strip()]
