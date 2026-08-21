# 文档 / 规范需求模板

## 目标

```text
例如：更新 AGENTS.md，加入新的防漂移规则。
```

## 要修改的文件

```text
例如：
AGENTS.md
docs/DEVELOPMENT_RULES.md
docs/IMPLEMENTATION.md
```

## 要加入的规则

```text
这里逐条写新规则。
```

## 要删除或改写的旧规则

```text
这里写旧规则问题。如果没有，写“无”。
```

## 本次边界

- 只改文档。
- 不改前端。
- 不改后端。
- 不改 Git 配置。

## 验收标准

- 文档里能直接看懂规则。
- 不和现有 AGENTS.md 冲突。
- `git diff --check` 通过。
