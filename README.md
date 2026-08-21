# Content Studio New

本地内容创作工作台。当前阶段只做公众号文章框架，不接真实 DeepSeek，不做视频和小说实现。

## 当前范围

- Vue3 + Vite 前端骨架
- Django + DRF 后端骨架
- SQLite 默认数据库
- 公众号文章 mock 流程
- 临时预览，不自动保存
- 用户点击后保存到作品库
- 手动 DeepSeek 正文 Prompt 大输入框
- 粘贴 DeepSeek 返回正文并导入，自动套公众号内联富文本模板
- 本地发布前质检
- 手动热点粘贴整理
- 临时草稿和作品库文章导出 Word
- 草稿富文本复制和纯文本复制
- 作品库删除
- 作品库文章打开回临时预览区
- 作品库最多保留 20 篇
- 安全重置本地测试数据脚本
- 关键词结构化配置和手动输入
- 公众号页面按“当前文章主区 + 右侧工具箱”组织，避免功能块平铺
- 公众号发布闭环：粘贴正文、模板预览、发布检查、复制富文本、手动保存
- Prompt 可插入方向、标题、热词、大纲和正文结构模板，再手动编辑复制

## 文档

- `docs/REQUIREMENTS.md`
- `docs/ENVIRONMENT.md`
- `docs/VERSION.md`
- `docs/DEVELOPMENT_RULES.md`
- `docs/IMPLEMENTATION.md`
- `docs/API.md`
- `docs/AI_CODE_REVIEW.md`

## 本地启动目标

首次安装依赖：

```bat
C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m venv backend\.venv
backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
cd frontend
npm install
```

启动：

```bat
scripts\start_backend.bat
scripts\start_frontend.bat
```

当前骨架不会自动调用 DeepSeek。

重置本地测试数据：

```bat
scripts\reset_local_data.bat
```

脚本需要手动输入 `RESET` 才会删除本地 SQLite 数据库。
