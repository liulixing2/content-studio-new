import type { ArticleRecord, Direction, DraftArticle, RenderedArticle } from '../types/article'
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

export function saveArticleToLibrary(draft: DraftArticle, keywords: string) {
  return postJson<{ ok: boolean; article: ArticleRecord }>('/articles/save/', { draft, keywords })
}

export function fetchSavedArticles() {
  return getJson<{ articles: ArticleRecord[] }>('/articles/')
}
