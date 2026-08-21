# Codex Project Rules

This file is the project-level anchor for Codex work in this repository. Read it before changing code.

## Current Scope

- Work only in the new project: `F:\codex\project\content_studio_new`.
- Do not modify or revive the old project under `_legacy_disabled`.
- Current active module is WeChat public-account articles only.
- Do not implement video packages, novel generation, image generation, real hotspot scraping, or automatic DeepSeek calls unless the user explicitly starts that phase.

## Product Flow Lock

The current article flow is:

```text
requirements prompt -> copy to DeepSeek manually -> paste returned article -> apply WeChat template -> quality check -> copy rich text -> user confirms save
```

UI rule for the article page:

- Keep the left navigation.
- Keep the main article workspace in the center column.
- The main workspace must show requirements above returned正文.
- The requirement prompt must support these editable modules: base rules, direction/category, title, hotwords, outline, template.
- Do not restore the right-side generation toolbox unless the user explicitly asks.
- Auxiliary settings and library may be folded or secondary, but must remain usable.

## Hard Prohibitions

- Do not call DeepSeek, scrape the web, generate images, or run batch tasks automatically.
- Do not make hidden loops or background retries.
- Do not auto-save generated content. Save only after the user clicks save and confirms.
- Do not hard-code topic words such as a specific anime, person, movie, era, or title into general prompts.
- Do not reintroduce old template phrases or fallback text that looks like a system note.
- Do not output default interaction text or material/copyright notes unless the user provided them or explicitly wants them.
- Do not let repeated prompt-module clicks append unlimited duplicate blocks; update the relevant block instead.
- Do not treat mock/local data as real web trends.

## Acceptance Checklist

For article changes, verify the relevant items before final response:

- Direction/category can be edited manually.
- Title can be edited manually and does not become a fake default title.
- Requirement module buttons update or insert the matching block without duplicate stacking.
- The copied DeepSeek prompt contains title, direction/category, outline, template, and hard rules when synced.
- Pasted正文 imports into the WeChat template without adding default interaction or default material notes.
- Empty headings such as `一、` become readable headings or are rejected.
- Obvious test content such as repeated digits is not publishable.
- Rich text copy, plain text copy, quality check, save, open, delete, and Word export are not broken by layout changes.

## Engineering Rules

- Read the real target files before editing.
- Keep diffs narrow. Do not refactor unrelated files.
- Prefer existing Vue, DRF, and service patterns already in this repo.
- Do not add dependencies, change lockfiles, change build config, or change data storage unless the user explicitly asks.
- If the same problem fails 3 times, stop and report the latest error instead of continuing.
- For code changes, run the smallest relevant checks. At minimum for frontend/article work:

```powershell
npm run build
backend\.venv\Scripts\python.exe backend\manage.py check
git diff --check
```

## Git

- Work on `dev` unless the user explicitly asks otherwise.
- Important completed changes should be pushed to both remotes:

```powershell
git push github dev
git push gitee dev
```
