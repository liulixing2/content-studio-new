<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import {
  fetchSavedArticles,
  generateArticleDirections,
  generateArticleTitles,
  generateTemporaryArticleDraft,
  saveArticleToLibrary,
} from '../../api/articles'
import type { ArticleRecord, Direction, DraftArticle, RenderedArticle } from '../../types/article'
import ArticleLibrary from './components/ArticleLibrary.vue'
import DirectionPanel from './components/DirectionPanel.vue'
import DraftPreview from './components/DraftPreview.vue'
import TitlePanel from './components/TitlePanel.vue'

const keywords = ref('90后 动漫 龙珠')
const directions = ref<Direction[]>([])
const titles = ref<string[]>([])
const selectedDirection = ref<Direction | null>(null)
const selectedTitle = ref('')
const draft = ref<DraftArticle | null>(null)
const rendered = ref<RenderedArticle | null>(null)
const articles = ref<ArticleRecord[]>([])
const statusText = ref('当前为本地 mock 流程，不会自动调用 DeepSeek。')
const isLoading = ref(false)

const canCreateTitles = computed(() => Boolean(selectedDirection.value))
const canCreateDraft = computed(() => Boolean(selectedTitle.value))
const canSaveDraft = computed(() => Boolean(draft.value))

async function runAction(action: () => Promise<void>, successText: string) {
  isLoading.value = true
  try {
    await action()
    statusText.value = successText
  } catch (error) {
    statusText.value = error instanceof Error ? error.message : '操作失败，请检查后端是否已启动。'
  } finally {
    isLoading.value = false
  }
}

async function loadDirections() {
  await runAction(async () => {
    const result = await generateArticleDirections(keywords.value)
    directions.value = result.directions
    titles.value = []
    selectedDirection.value = result.directions[0] ?? null
    selectedTitle.value = ''
    draft.value = null
    rendered.value = null
  }, '已生成选题方向。')
}

async function loadTitles() {
  if (!selectedDirection.value) return
  await runAction(async () => {
    const result = await generateArticleTitles(selectedDirection.value as Direction)
    titles.value = result.titles
    selectedTitle.value = result.titles[0] ?? ''
    draft.value = null
    rendered.value = null
  }, '已生成标题候选。')
}

async function loadDraft() {
  if (!selectedTitle.value) return
  await runAction(async () => {
    const result = await generateTemporaryArticleDraft(selectedTitle.value, keywords.value)
    draft.value = result.draft
    rendered.value = result.rendered
  }, '已生成临时草稿，刷新前请确认是否保存。')
}

async function saveDraft() {
  if (!draft.value) return
  await runAction(async () => {
    await saveArticleToLibrary(draft.value as DraftArticle, keywords.value)
    await loadLibrary()
  }, '已保存到作品库。')
}

async function loadLibrary() {
  const result = await fetchSavedArticles()
  articles.value = result.articles
}

onMounted(loadLibrary)
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <h1>内容工作台</h1>
      <button class="active" type="button">公众号文章</button>
      <button disabled type="button">视频包</button>
      <button disabled type="button">小说章节</button>
      <p>先打通公众号主流程，视频和小说保留入口。</p>
    </aside>

    <main class="workspace">
      <header class="topbar">
        <div>
          <h2>公众号文章生成</h2>
          <p>关键词生成方向、标题、临时草稿；确认后再保存作品库。</p>
        </div>
        <div class="status">{{ statusText }}</div>
      </header>

      <section class="grid">
        <DirectionPanel
          v-model:keywords="keywords"
          v-model:selected-direction="selectedDirection"
          :directions="directions"
          :is-loading="isLoading"
          @generate="loadDirections"
        />

        <TitlePanel
          v-model:selected-title="selectedTitle"
          :titles="titles"
          :can-create-titles="canCreateTitles"
          :can-create-draft="canCreateDraft"
          :is-loading="isLoading"
          @generate-titles="loadTitles"
          @generate-draft="loadDraft"
        />

        <DraftPreview
          :draft="draft"
          :rendered="rendered"
          :can-save="canSaveDraft"
          :is-loading="isLoading"
          @save="saveDraft"
        />

        <ArticleLibrary :articles="articles" @refresh="loadLibrary" />
      </section>
    </main>
  </div>
</template>
