# 环境配置说明

## 当前目标

本项目优先面向本地运行，也可以后续打包给别人使用。

第一阶段只搭建公众号文章框架和公共基础能力，不接真实 DeepSeek，不做视频剪辑，不做小说生成。

## 推荐技术栈

前端：

- Vue 3
- Vite
- TypeScript

后端：

- Python
- Django
- Django REST Framework

数据库：

- 第一阶段默认 SQLite
- 后续可选 MySQL

缓存 / 队列：

- 第一阶段不依赖 Redis
- 后续可选 Redis + Celery

文件存储：

- 本地 `storage/` 目录
- 上传素材、生成图片、导出文件都存本地

AI：

- DeepSeek API 模式：用户填写自己的 API Key
- 手动免费模式：项目生成 Prompt，用户复制到 DeepSeek 网页/App，再粘贴结果

## 为什么第一阶段不用 MySQL 和 Redis

第一阶段目标是本地可运行、低配置、低维护成本。

SQLite 足够支持：

- 公众号草稿
- 作品库
- 版本记录
- AI 调用记录
- 基础模板数据

MySQL 和 Redis 适合后续多人协作、云端部署、长任务队列和大量数据场景。

## 计划目录结构

```text
content_studio_new
├─ frontend             # Vue3 + Vite 前端
├─ backend              # Django + DRF 后端
├─ docs                 # 产品和开发文档
├─ templates            # 公众号/视频/小说模板
├─ storage              # 本地文件存储，不提交 Git
├─ data                 # SQLite 数据库，不提交 Git
├─ scripts              # 本地启动脚本
├─ REQUIREMENTS.md
├─ ENVIRONMENT.md
├─ VERSION.md
├─ DEVELOPMENT_RULES.md
└─ README.md
```

## 本地运行方式目标

后续应提供：

- `scripts/start_backend.bat`
- `scripts/start_frontend.bat`
- `scripts/start_all.bat`

用户使用方式：

```text
双击启动脚本
  ↓
浏览器打开本地地址
  ↓
使用项目
```

## Git 注意事项

不能提交：

- `.env`
- DeepSeek API Key
- SQLite 数据库文件
- 上传素材
- 生成文章
- 生成图片
- 生成视频
- 临时缓存
- 日志文件

应提交：

- 源代码
- 模板
- 文档
- 示例配置
- 启动脚本

## 后续可选升级

当项目需要多人使用或部署到服务器时，再加入：

- MySQL
- Redis
- Celery
- Nginx
- Docker
- 用户权限系统
