<script setup lang="ts">
import type { ManualPrompt } from '../../../types/article'

defineProps<{
  prompt: ManualPrompt | null
  canImport: boolean
  canBuildFromDraft: boolean
  isLoading: boolean
}>()

const pastedText = defineModel<string>('pastedText', { required: true })

defineEmits<{
  generatePrompt: [stage: string]
  copyPrompt: []
  importDraft: []
}>()
</script>

<template>
  <section class="panel manual-panel">
    <h3>4. 手动 DeepSeek</h3>
    <p class="hint">这里只生成 Prompt，不会自动调用 DeepSeek。复制到免费版，结果粘回来再导入。</p>

    <div class="button-row">
      <button type="button" :disabled="isLoading" @click="$emit('generatePrompt', 'hotspots')">热点方向 Prompt</button>
      <button type="button" :disabled="isLoading" @click="$emit('generatePrompt', 'titles')">标题 Prompt</button>
      <button type="button" :disabled="isLoading" @click="$emit('generatePrompt', 'outline')">大纲 Prompt</button>
      <button type="button" :disabled="isLoading" @click="$emit('generatePrompt', 'draft')">正文 Prompt</button>
      <button type="button" :disabled="isLoading || !canBuildFromDraft" @click="$emit('generatePrompt', 'image')">
        配图 Prompt
      </button>
    </div>

    <div v-if="prompt" class="prompt-box">
      <div class="preview-head">
        <strong>{{ prompt.stage_name }}</strong>
        <button type="button" @click="$emit('copyPrompt')">复制 Prompt</button>
      </div>
      <pre>{{ prompt.prompt }}</pre>
      <small>{{ prompt.usage_note }}</small>
    </div>

    <label>
      粘贴 DeepSeek 返回正文
      <textarea v-model="pastedText" rows="8" placeholder="把 DeepSeek 生成的公众号正文粘贴到这里"></textarea>
    </label>
    <div class="actions">
      <button type="button" :disabled="isLoading || !canImport" @click="$emit('importDraft')">导入为临时草稿</button>
    </div>
  </section>
</template>
