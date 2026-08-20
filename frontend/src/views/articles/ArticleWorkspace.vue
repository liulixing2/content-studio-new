<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import {
  checkDraftQuality,
  exportDraftWord,
  exportSavedArticleWord,
  fetchSavedArticles,
  generateArticleDirections,
  generateManualPrompt,
  generateManualHotspotDirections,
  generateArticleTitles,
  generateTemporaryArticleDraft,
  importDraftFromPaste,
  saveArticleToLibrary,
} from '../../api/articles'
import type {
  ArticleRecord,
  Direction,
  DraftArticle,
  ManualPrompt,
  QualityReport,
  RenderedArticle,
} from '../../types/article'
import ArticleLibrary from './components/ArticleLibrary.vue'
import DirectionPanel from './components/DirectionPanel.vue'
import DraftPreview from './components/DraftPreview.vue'
import ManualAiPanel from './components/ManualAiPanel.vue'
import ManualHotspotPanel from './components/ManualHotspotPanel.vue'
import QualityPanel from './components/QualityPanel.vue'
import TitlePanel from './components/TitlePanel.vue'

const keywords = ref('90后 动漫 龙珠')
const directions = ref<Direction[]>([])
const titles = ref<string[]>([])
const selectedDirection = ref<Direction | null>(null)
const selectedTitle = ref('')
const draft = ref<DraftArticle | null>(null)
const rendered = ref<RenderedArticle | null>(null)
const manualPrompt = ref<ManualPrompt | null>(null)
const pastedText = ref('')
const manualHotspotText = ref('')
const qualityReport = ref<QualityReport | null>(null)
const articles = ref<ArticleRecord[]>([])
const statusText = ref('当前为本地 mock 流程，不会自动调用 DeepSeek。')
const isLoading = ref(false)
const hasUnsavedTemporaryResult = ref(false)

const canCreateTitles = computed(() => Boolean(selectedDirection.value))
const canCreateDraft = computed(() => Boolean(selectedTitle.value))
const canSaveDraft = computed(() => Boolean(draft.value))
const canImportPastedDraft = computed(() => Boolean(selectedTitle.value && pastedText.value.trim()))
const canCheckDraft = computed(() => Boolean(draft.value))
const canImportManualHotspots = computed(() => Boolean(keywords.value.trim() && manualHotspotText.value.trim()))

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

function confirmTemporaryOverwrite() {
  if (!hasUnsavedTemporaryResult.value) return true
  return window.confirm('当前有未保存的临时结果，继续会覆盖页面里的临时内容。是否继续？')
}

function markTemporaryChanged() {
  hasUnsavedTemporaryResult.value = true
  qualityReport.value = null
}

async function loadDirections() {
  if (!confirmTemporaryOverwrite()) return
  await runAction(async () => {
    const result = await generateArticleDirections(keywords.value)
    directions.value = result.directions
    titles.value = []
    selectedDirection.value = result.directions[0] ?? null
    selectedTitle.value = ''
    draft.value = null
    rendered.value = null
    manualPrompt.value = null
    pastedText.value = ''
    qualityReport.value = null
    hasUnsavedTemporaryResult.value = true
  }, '已生成选题方向。')
}

async function loadTitles() {
  if (!selectedDirection.value) return
  if (!confirmTemporaryOverwrite()) return
  await runAction(async () => {
    const result = await generateArticleTitles(selectedDirection.value as Direction)
    titles.value = result.titles
    selectedTitle.value = result.titles[0] ?? ''
    draft.value = null
    rendered.value = null
    qualityReport.value = null
    hasUnsavedTemporaryResult.value = true
  }, '已生成标题候选。')
}

async function importManualHotspots() {
  if (!canImportManualHotspots.value) return
  if (!confirmTemporaryOverwrite()) return
  await runAction(async () => {
    const result = await generateManualHotspotDirections(keywords.value, manualHotspotText.value)
    directions.value = result.directions
    selectedDirection.value = result.directions[0] ?? null
    titles.value = []
    selectedTitle.value = ''
    draft.value = null
    rendered.value = null
    qualityReport.value = null
    hasUnsavedTemporaryResult.value = true
  }, '已将手动粘贴热点整理为临时方向。')
}

async function loadDraft() {
  if (!selectedTitle.value) return
  if (!confirmTemporaryOverwrite()) return
  await runAction(async () => {
    const result = await generateTemporaryArticleDraft(selectedTitle.value, keywords.value)
    draft.value = result.draft
    rendered.value = result.rendered
    markTemporaryChanged()
  }, '已生成临时草稿，刷新前请确认是否保存。')
}

async function buildPrompt(stage: string) {
  await runAction(async () => {
    const result = await generateManualPrompt(stage, {
      keywords: keywords.value,
      title: selectedTitle.value,
      direction: selectedDirection.value,
      draft_text: rendered.value?.text ?? '',
    })
    manualPrompt.value = result.prompt
    hasUnsavedTemporaryResult.value = true
  }, '已生成手动 DeepSeek Prompt。')
}

async function copyPrompt() {
  if (!manualPrompt.value) return
  await navigator.clipboard.writeText(manualPrompt.value.prompt)
  statusText.value = 'Prompt 已复制。'
}

async function importPastedDraft() {
  if (!selectedTitle.value || !pastedText.value.trim()) return
  if (!confirmTemporaryOverwrite()) return
  await runAction(async () => {
    const result = await importDraftFromPaste(selectedTitle.value, keywords.value, pastedText.value)
    draft.value = result.draft
    rendered.value = result.rendered
    markTemporaryChanged()
  }, '已导入为临时草稿，尚未保存。')
}

async function checkCurrentDraft() {
  if (!draft.value) return
  await runAction(async () => {
    const result = await checkDraftQuality(draft.value as DraftArticle)
    qualityReport.value = result.report
    hasUnsavedTemporaryResult.value = true
  }, '已完成发布检测。')
}

async function saveDraft() {
  if (!draft.value) return
  if (!window.confirm('确认保存当前草稿到作品库？保存后会生成文章记录和版本记录。')) return
  await runAction(async () => {
    await saveArticleToLibrary(draft.value as DraftArticle, keywords.value)
    await loadLibrary()
    hasUnsavedTemporaryResult.value = false
  }, '已保存到作品库。')
}

function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}

async function exportCurrentDraftWord() {
  if (!draft.value) return
  await runAction(async () => {
    const blob = await exportDraftWord(draft.value as DraftArticle)
    downloadBlob(blob, 'wechat-draft.docx')
  }, '已导出当前临时草稿 Word。')
}

async function exportSavedWord(articleId: number) {
  await runAction(async () => {
    const blob = await exportSavedArticleWord(articleId)
    downloadBlob(blob, `wechat-article-${articleId}.docx`)
  }, '已导出作品库文章 Word。')
}

async function loadLibrary() {
  const result = await fetchSavedArticles()
  articles.value = result.articles
}

function warnBeforeUnload(event: BeforeUnloadEvent) {
  if (!hasUnsavedTemporaryResult.value) return
  event.preventDefault()
  event.returnValue = ''
}

onMounted(() => {
  loadLibrary()
  window.addEventListener('beforeunload', warnBeforeUnload)
})

onBeforeUnmount(() => {
  window.removeEventListener('beforeunload', warnBeforeUnload)
})
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

        <ManualHotspotPanel
          v-model:manual-hotspot-text="manualHotspotText"
          :keywords="keywords"
          :can-import="canImportManualHotspots"
          :is-loading="isLoading"
          @import-hotspots="importManualHotspots"
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

        <ManualAiPanel
          v-model:pasted-text="pastedText"
          :prompt="manualPrompt"
          :can-import="canImportPastedDraft"
          :can-build-from-draft="canCheckDraft"
          :is-loading="isLoading"
          @generate-prompt="buildPrompt"
          @copy-prompt="copyPrompt"
          @import-draft="importPastedDraft"
        />

        <DraftPreview
          :draft="draft"
          :rendered="rendered"
          :can-save="canSaveDraft"
          :is-loading="isLoading"
          @save="saveDraft"
          @export-word="exportCurrentDraftWord"
        />

        <QualityPanel :report="qualityReport" :can-check="canCheckDraft" :is-loading="isLoading" @check="checkCurrentDraft" />

        <ArticleLibrary :articles="articles" @refresh="loadLibrary" @export-word="exportSavedWord" />
      </section>
    </main>
  </div>
</template>
