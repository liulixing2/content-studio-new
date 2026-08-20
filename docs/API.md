# API 说明

基础地址：

```text
http://127.0.0.1:8000/api
```

当前接口均为 mock 或本地保存，不调用 DeepSeek。

## 健康检查

```http
GET /api/health/
```

返回：

```json
{
  "ok": true,
  "service": "content-studio-backend"
}
```

## 生成公众号方向

```http
POST /api/articles/directions/
```

请求：

```json
{
  "keywords": "90后 动漫 龙珠"
}
```

返回：

```json
{
  "mode": "mock",
  "directions": []
}
```

## 生成标题

```http
POST /api/articles/titles/
```

请求：

```json
{
  "direction": {
    "title": "方向名称",
    "keywords": ["龙珠"]
  }
}
```

返回：

```json
{
  "mode": "mock",
  "titles": ["标题1", "标题2"]
}
```

## 生成临时草稿

```http
POST /api/articles/draft/
```

请求：

```json
{
  "title": "文章标题",
  "keywords": "90后 动漫 龙珠"
}
```

返回：

```json
{
  "mode": "mock",
  "draft": {},
  "rendered": {
    "html": "...",
    "text": "..."
  },
  "saved": false
}
```

注意：此接口不保存数据。

## 生成手动 DeepSeek Prompt

```http
POST /api/articles/manual-prompt/
```

请求：

```json
{
  "stage": "draft",
  "context": {
    "keywords": "90后 动漫 龙珠",
    "title": "文章标题",
    "direction": {},
    "draft_text": "已有正文"
  }
}
```

`stage` 可选：`hotspots`、`titles`、`outline`、`draft`、`quality`、`image`。

注意：此接口只生成可复制的 Prompt，不调用 DeepSeek，也不保存。

## 导入粘贴正文为临时草稿

```http
POST /api/articles/import-draft/
```

请求：

```json
{
  "title": "文章标题",
  "keywords": "90后 动漫 龙珠",
  "pasted_text": "从 DeepSeek 粘贴回来的正文"
}
```

返回：

```json
{
  "draft": {},
  "rendered": {
    "html": "...",
    "text": "..."
  },
  "saved": false
}
```

注意：导入结果仍然是临时草稿，不保存。

## 发布前质检

```http
POST /api/articles/quality-check/
```

请求：

```json
{
  "draft": {}
}
```

返回：

```json
{
  "report": {
    "publishable": false,
    "score": 70,
    "issues": [],
    "suggestions": [],
    "saved": false
  },
  "saved": false
}
```

注意：质检报告也是临时结果，不保存。

## 渲染公众号模板

```http
POST /api/articles/render/
```

请求：

```json
{
  "draft": {
    "title": "文章标题",
    "summary": "摘要",
    "sections": []
  }
}
```

返回：

```json
{
  "rendered": {
    "html": "...",
    "text": "..."
  }
}
```

用途：

- AI 返回结构化内容后，由项目统一套公众号模板。
- 后续配图、标题、段落样式都应在模板层处理。

## 保存文章

```http
POST /api/articles/save/
```

请求：

```json
{
  "keywords": "90后 动漫 龙珠",
  "draft": {
    "title": "文章标题",
    "summary": "摘要",
    "sections": []
  }
}
```

返回：

```json
{
  "ok": true,
  "article": {}
}
```

注意：只有这个接口会写入作品库。

## 作品库列表

```http
GET /api/articles/
```

返回：

```json
{
  "articles": []
}
```

## 文章详情

```http
GET /api/articles/{id}/
```

## 当前接口约束

- 当前接口全部是 mock 或本地数据库操作。
- 不调用 DeepSeek。
- 不抓取百度、微博、B站。
- 草稿接口不保存，保存接口才写库。
- 手动 Prompt、粘贴导入、质检报告也都不保存。
