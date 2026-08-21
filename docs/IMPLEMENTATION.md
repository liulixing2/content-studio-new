# 公众号框架实现说明

## 当前实现范围

当前只实现公众号文章框架 MVP，不接真实 DeepSeek。

已实现：

- 后端 Django / DRF 骨架。
- 前端 Vue3 / Vite 骨架。
- 公众号 mock 流程。
- 临时预览。
- 用户手动保存到作品库。
- 文章版本初始记录。
- 手动 DeepSeek Prompt 生成。
- DeepSeek 返回正文粘贴导入。
- 本地发布前质检。
- 未保存临时结果离开页面提示。
- 手动热点粘贴整理。
- 临时草稿和作品库文章导出 Word。
- 草稿富文本复制和纯文本复制。
- 作品库删除。
- 作品库文章打开回临时预览区。
- 作品库最多保留 20 篇。
- 公众号页面按“当前文章主区 + 右侧工具箱”组织。

未实现：

- 真实 DeepSeek API。
- 图片生成。
- 富文本剪贴板。
- 视频包。
- 小说。

## 目录说明

```text
backend/
  content_studio_backend/       # Django 项目配置
  apps/articles/                # 公众号文章模块
    models.py                   # Article / ArticleVersion / AiTask
    views.py                    # API 入口，只做请求编排
    serializers.py              # DRF 序列化
    services/                   # 业务服务拆分
      keyword_service.py        # 关键词清洗
      direction_service.py      # 选题方向生成
      title_service.py          # 标题生成
      draft_service.py          # 草稿生成
      manual_hotspot_service.py # 手动热点粘贴整理
      word_export_service.py    # Word 文件导出
      template_service.py       # 公众号 HTML / Text 模板渲染

frontend/
  src/App.vue                   # 挂载工作台入口
  src/api/http.ts               # GET / POST / PUT / PATCH / DELETE 封装
  src/api/articles.ts           # 公众号接口方法
  src/types/article.ts          # 公众号相关类型
  src/views/articles/           # 公众号页面
    ArticleWorkspace.vue        # 公众号工作台主页面
    components/                 # 页面局部组件
      DirectionPanel.vue        # 关键词和方向
      TitlePanel.vue            # 标题和生成草稿
      ManualAiPanel.vue         # 生成设置、手动热点、DeepSeek Prompt 和粘贴导入
      DraftPreview.vue          # 临时草稿预览
      QualityPanel.vue          # 发布前质检
      ArticleLibrary.vue        # 已保存作品库
  src/styles.css                # 页面样式

scripts/
  start_backend.bat             # 后端启动脚本
  start_frontend.bat            # 前端启动脚本

docs/
  API.md                        # 接口说明
  AI_CODE_REVIEW.md             # AI 生成代码审查说明
```

## 核心业务规则

生成草稿不会保存。

```text
生成方向
  ↓
手动粘贴热点整理方向（可选）
  ↓
生成标题
  ↓
生成临时草稿 / 生成手动 DeepSeek Prompt
  ↓
粘贴 DeepSeek 返回内容并导入为临时草稿
  ↓
发布前质检
  ↓
用户确认
  ↓
保存到作品库
```

相关代码：

- `backend/apps/articles/views.py`
- `backend/apps/articles/services/`
- `frontend/src/views/articles/ArticleWorkspace.vue`
- `frontend/src/api/articles.ts`

## 主要数据模型

`Article`

- 已保存文章。
- 保存渲染后的 HTML / Text。
- 保存结构化正文 JSON。

`ArticleVersion`

- 文章版本记录。
- 第一版保存时自动生成 `version = 1`。

`AiTask`

- AI 调用记录占位表。
- 当前 mock 阶段暂未实际写入。

## 命名原则

函数名尽量表达动作：

- `generateArticleDirections`
- `generateManualHotspotDirections`
- `generateArticleTitles`
- `generateTemporaryArticleDraft`
- `generateManualPrompt`
- `importDraftFromPaste`
- `checkDraftQuality`
- `exportDraftWord`
- `exportSavedArticleWord`
- `saveArticleToLibrary`
- `render_article_template`

后续继续保持：看函数名能知道业务意图。

## 当前前端工作台

当前启用模块：

- 公众号文章

预留模块：

- 视频包
- 小说章节

预留模块只显示入口，不实现业务，避免半成品功能误导使用。

公众号页面布局：

- 左侧导航：区分公众号文章、视频包、小说章节。
- 中间主区：围绕当前文章展示标题状态、标题候选、正文预览和发布检查。
- 右侧工具箱：放选题设置、生成设置和作品库。

这样页面主线是“当前这篇稿子能不能发布”，工具区只负责提供关键词配置、手动素材、DeepSeek Prompt 和历史文章。

## 关键词输入规则

关键词支持两种方式：

- 直接输入，例如 `90后 动漫 怀旧 龙珠 童年回忆 名场面`。
- 展开结构化配置，选择年代、内容类型、写作方向，再填写指定作品/人物和补充关键词。

结构化配置只负责生成关键词文本，不自动调用 AI，不自动保存。

## 生成设置

生成设置面板把原来的手动热点和 DeepSeek Prompt 合并到一张卡里，按实际使用顺序组织：

- 方向 / 分类：确认关键词后，可以生成 DeepSeek 方向 Prompt。
- 热词 / 素材：用户可从百度、微博、B站或其他来源手动复制，也可以粘贴 DeepSeek 返回方向。
- 标题 / 大纲：可以只生成标题，也可以为复杂文章生成大纲。
- 模板：可选择情绪共鸣文、清单盘点文、单作品深聊、对比观点文。
- 正文 / 配图：可直接生成正文，也可基于大纲生成；正文稳定后再生成配图 Prompt。

这些按钮只是生成可复制 Prompt，不自动调用 DeepSeek，不自动保存结果。

## 方向来源

可写方向有两种来源：

- 本地生成方向：根据关键词本地 mock 生成，不调用 DeepSeek。
- 生成设置粘贴整理：用户从百度、微博、B站或 DeepSeek 复制内容，粘贴回来整理成临时方向。

系统不能把粘贴来源伪装成自动抓取，也不能把本地生成方向伪装成网络热点。

## 后续扩展接口边界

接真实 DeepSeek 时，优先新增独立服务，不把 AI 调用写进 `views.py`。

建议新增：

- `ai_provider_service.py`：统一封装 DeepSeek 或手动 Prompt 模式。
- `quality_service.py`：检测是否可发布。
- `image_prompt_service.py`：根据文章生成配图提示词。
- `quota_service.py`：限制单次点击和自动修稿次数。

所有真实 AI 调用都必须由前端按钮触发，不能页面加载自动触发。

## 临时结果规则

以下结果默认只存在当前页面，刷新会丢失：

- 方向结果。
- 标题候选。
- 手动 Prompt。
- 粘贴导入后的草稿。
- 发布检测报告。
- mock 草稿。
- Word 导出结果。

只有点击“保存到作品库”才写入 `Article` 和 `ArticleVersion`。

页面会在有未保存临时结果时提示用户，避免误刷新丢稿。

## 作品库规则

作品库最多保留 20 篇公众号文章。

保存新文章后，如果超过 20 篇，系统会按更新时间删除最旧文章。

删除文章必须由用户点击删除按钮并确认，不自动删除当前可见文章。

导出 Word、复制富文本、复制纯文本都不改变保存状态。

打开作品库文章会把已保存内容放回临时预览区，方便继续复制、导出 Word 或重新质检；这个动作不会创建新版本，也不会自动保存。
