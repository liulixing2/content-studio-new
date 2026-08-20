import type {
  ArticleRecord,
  Direction,
  DraftArticle,
  ManualPrompt,
  QualityReport,
  RenderedArticle,
} from '../types/article'
import { API_BASE, getJson, postJson } from './http'

export function generateArticleDirections(keywords: string) {
  return postJson<{ mode: string; directions: Direction[] }>('/articles/directions/', { keywords })
}

export function generateManualHotspotDirections(keywords: string, pastedText: string) {
  return postJson<{ directions: Direction[]; saved: boolean; source: string; message: string }>('/articles/manual-hotspots/', {
    keywords,
    pasted_text: pastedText,
  })
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

async function downloadWord(path: string, body?: unknown) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: body ? 'POST' : 'GET',
    headers: body ? { 'Content-Type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  })
  if (!response.ok) throw new Error(await response.text())
  return response.blob()
}

export function exportDraftWord(draft: DraftArticle) {
  return downloadWord('/articles/draft/export-word/', { draft })
}

export function exportSavedArticleWord(articleId: number) {
  return downloadWord(`/articles/${articleId}/export-word/`)
}
