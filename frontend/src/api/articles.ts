import type {
  ArticleRecord,
  Direction,
  DraftArticle,
  ManualPrompt,
  QualityReport,
  RenderedArticle,
} from '../types/article'
import { getJson, postJson } from './http'

export function generateArticleDirections(keywords: string) {
  return postJson<{ mode: string; directions: Direction[] }>('/articles/directions/', { keywords })
}

export function generateArticleTitles(direction: Direction) {
  return postJson<{ mode: string; titles: string[] }>('/articles/titles/', { direction })
}

export function generateTemporaryArticleDraft(title: string, keywords: string) {
  return postJson<{ mode: string; draft: DraftArticle; rendered: RenderedArticle; saved: boolean }>('/articles/draft/', {
    title,
    keywords,
  })
}

export function generateManualPrompt(stage: string, context: Record<string, unknown>) {
  return postJson<{ prompt: ManualPrompt }>('/articles/manual-prompt/', { stage, context })
}

export function importDraftFromPaste(title: string, keywords: string, pastedText: string) {
  return postJson<{ draft: DraftArticle; rendered: RenderedArticle; saved: boolean }>('/articles/import-draft/', {
    title,
    keywords,
    pasted_text: pastedText,
  })
}

export function checkDraftQuality(draft: DraftArticle) {
  return postJson<{ report: QualityReport; saved: boolean }>('/articles/quality-check/', { draft })
}

export function saveArticleToLibrary(draft: DraftArticle, keywords: string) {
  return postJson<{ ok: boolean; article: ArticleRecord }>('/articles/save/', { draft, keywords })
}

export function fetchSavedArticles() {
  return getJson<{ articles: ArticleRecord[] }>('/articles/')
}
