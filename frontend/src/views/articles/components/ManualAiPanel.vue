<script setup lang="ts">
import { ref } from 'vue'
import type { ManualPrompt } from '../../../types/article'

const props = defineProps<{
  keywords: string
  prompt: ManualPrompt | null
  canImport: boolean
  canImportHotspots: boolean
  canBuildFromDraft: boolean
  isLoading: boolean
}>()

const pastedText = defineModel<string>('pastedText', { required: true })
const manualHotspotText = defineModel<string>('manualHotspotText', { required: true })
const draftMode = ref<'direct' | 'outline'>('direct')
const selectedTemplate = ref('情绪共鸣文')

const templateOptions = ['情绪共鸣文', '清单盘点文', '单作品深聊', '对比观点文']

defineEmits<{
  generatePrompt: [stage: string, extraContext?: Record<string, unknown>]
  copyPrompt: []
  importDraft: []
  importHotspots: []
}>()

function searchUrl(platform: 'baidu' | 'weibo' | 'bilibili') {
  const query = encodeURIComponent(props.keywords || '')
  if (platform === 'baidu') return `https://www.baidu.com/s?wd=${query}`
  if (platform === 'weibo') return `https://s.weibo.com/weibo?q=${query}`
  return `https://search.bilibili.com/all?keyword=${query}`
}

function promptContext() {
  return {
    manual_hotspots: manualHotspotText.value,
    template_type: selectedTemplate.value,
  }
}

</script>

<template>
  <section class="panel manual-panel">
    <h3>生成设置</h3>
    <p class="hint">按顺序准备方向、热词、大纲和模板。这里不自动调用 DeepSeek，只生成可复制的 Prompt。</p>

    <div class="workflow-card">
      <div class="workflow-step">
        <div>
          <strong>1. 方向 / 分类</strong>
          <p class="hint">先确定写什么类型，再让 AI 帮你找可写切口。</p>
        </div>
        <button type="button" :disabled="isLoading || !keywords.trim()" @click="$emit('generatePrompt', 'hotspots', promptContext())">
          AI 方向
        </button>
      </div>

      <div class="search-row">
        <a :href="searchUrl('baidu')" target="_blank" rel="noreferrer">百度</a>
        <a :href="searchUrl('weibo')" target="_blank" rel="noreferrer">微博</a>
        <a :href="searchUrl('bilibili')" target="_blank" rel="noreferrer">B站</a>
      </div>

      <label>
        热词 / 素材
        <textarea
          v-model="manualHotspotText"
          rows="5"
          placeholder="可以粘贴平台热词、评论切口、标题，也可以粘贴 DeepSeek 返回的方向；每行一条更好整理"
        ></textarea>
      </label>

      <button type="button" :disabled="isLoading || !canImportHotspots" @click="$emit('importHotspots')">
        整理为可选方向
      </button>
    </div>

    <div class="workflow-card">
      <div class="workflow-step">
        <div>
          <strong>2. 标题 / 大纲</strong>
          <p class="hint">标题可以直接生成；大纲是可选项，复杂文章再走。</p>
        </div>
        <div class="button-row compact">
          <button type="button" :disabled="isLoading" @click="$emit('generatePrompt', 'titles', promptContext())">AI 标题</button>
          <button type="button" :disabled="isLoading" @click="$emit('generatePrompt', 'outline', promptContext())">AI 大纲</button>
        </div>
      </div>

      <label>
        模板
        <select v-model="selectedTemplate">
          <option v-for="option in templateOptions" :key="option" :value="option">{{ option }}</option>
        </select>
      </label>
    </div>

    <div class="workflow-card">
      <div class="workflow-step">
        <div>
          <strong>3. 正文 / 配图</strong>
          <p class="hint">可以跳过大纲直接生成正文，正文稳定后再生成配图建议。</p>
        </div>
      </div>
      <div class="choice-row">
        <label>
          <input v-model="draftMode" type="radio" value="direct" />
          直接正文
        </label>
        <label>
          <input v-model="draftMode" type="radio" value="outline" />
          基于大纲
        </label>
      </div>
      <div class="button-row compact">
        <button type="button" :disabled="isLoading" @click="$emit('generatePrompt', draftMode === 'direct' ? 'draft_direct' : 'draft', promptContext())">
          AI 正文
        </button>
        <button type="button" :disabled="isLoading || !canBuildFromDraft" @click="$emit('generatePrompt', 'image', promptContext())">
          AI 配图
        </button>
      </div>
    </div>

    <div v-if="prompt" class="prompt-box">
      <div class="preview-head">
        <strong>待复制给 DeepSeek：{{ prompt.stage_name }}</strong>
        <button type="button" @click="$emit('copyPrompt')">复制 Prompt</button>
      </div>
      <pre>{{ prompt.prompt }}</pre>
      <small>{{ prompt.usage_note }}</small>
    </div>

    <label>
      粘贴 DeepSeek 返回正文
      <textarea v-model="pastedText" rows="8" placeholder="把 DeepSeek 生成的公众号正文粘贴到这里；没选标题时会尝试用第一行作为标题"></textarea>
    </label>
    <div class="actions">
      <button type="button" :disabled="isLoading || !canImport" @click="$emit('importDraft')">导入为临时草稿</button>
    </div>
  </section>
</template>
