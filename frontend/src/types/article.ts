export interface Direction {
  title: string
  reader_question: string
  angle: string
  keywords: string[]
  article_type: string
  avoid: string[]
}

export interface DraftArticleSection {
  heading: string
  paragraphs: string[]
  image_hint: string
}

export interface DraftArticle {
  title: string
  summary: string
  sections: DraftArticleSection[]
  interaction: string
  copyright_notes: string[]
}

export interface RenderedArticle {
  html: string
  text: string
}

export interface ManualPrompt {
  stage: string
  stage_name: string
  prompt: string
  saved: boolean
  usage_note: string
}

export interface QualityIssue {
  level: 'high' | 'medium' | 'low'
  message: string
}

export interface QualityReport {
  publishable: boolean
  score: number
  issues: QualityIssue[]
  suggestions: string[]
  saved: boolean
}

export interface ArticleRecord {
  id: number
  title: string
  summary: string
  keywords: string
  article_type: string
  status: string
  body_json: DraftArticle
  rendered_html: string
  rendered_text: string
  created_at: string
  updated_at: string
}
