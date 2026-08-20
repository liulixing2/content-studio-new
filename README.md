# Content Studio New

本地内容创作工作台。当前阶段只做公众号文章框架，不接真实 DeepSeek，不做视频和小说实现。

## 当前范围

- Vue3 + Vite 前端骨架
- Django + DRF 后端骨架
- SQLite 默认数据库
- 公众号文章 mock 流程
- 临时预览，不自动保存
- 用户点击后保存到作品库
- 手动 DeepSeek Prompt 生成
- 粘贴 DeepSeek 返回正文并导入为临时草稿
- 本地发布前质检
- 手动热点粘贴整理
- 临时草稿和作品库文章导出 Word

## 文档

- `docs/REQUIREMENTS.md`
- `docs/ENVIRONMENT.md`
- `docs/VERSION.md`
- `docs/DEVELOPMENT_RULES.md`
- `docs/IMPLEMENTATION.md`
- `docs/API.md`
- `docs/AI_CODE_REVIEW.md`

## 本地启动目标

后续安装依赖后：

```bat
scripts\start_backend.bat
scripts\start_frontend.bat
```

当前骨架不会自动调用 DeepSeek。
