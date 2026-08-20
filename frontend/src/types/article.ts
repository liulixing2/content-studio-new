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
