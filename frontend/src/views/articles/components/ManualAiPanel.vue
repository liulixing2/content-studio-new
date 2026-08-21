<script setup lang="ts">
import { ref } from 'vue'
import type { ManualPrompt } from '../../../types/article'

defineProps<{
  prompt: ManualPrompt | null
  canImport: boolean
  canBuildFromDraft: boolean
  isLoading: boolean
}>()

const pastedText = defineModel<string>('pastedText', { required: true })
const activeStep = ref<'hotspots' | 'titles' | 'outline' | 'draft' | 'image'>('titles')
const draftMode = ref<'direct' | 'outline'>('direct')

const steps = [
  {
    key: 'hotspots',
    title: '热点',
    note: '根据关键词找可写切口。已有手动粘贴热点时，可以跳过。',
  },
  {
    key: 'titles',
    title: '标题',
    note: '根据方向生成多个标题，选一个继续。',
  },
  {
    key: 'outline',
    title: '大纲',
    note: '可选步骤。复杂文章建议先走大纲，短文可以跳过。',
  },
  {
    key: 'draft',
    title: '正文',
    note: '可以按标题直接生成，也可以基于大纲生成。',
  },
  {
    key: 'image',
    title: '配图',
    note: '正文稳定后再生成配图方案。',
  },
] as const

defineEmits<{
  generatePrompt: [stage: string]
  copyPrompt: []
  importDraft: []
}>()

function generateDraftPrompt(emit: (event: 'generatePrompt', stage: string) => void) {
  emit('generatePrompt', draftMode.value === 'direct' ? 'draft_direct' : 'draft')
}
</script>

<template>
  <section class="panel manual-panel">
    <h3>4. 手动 DeepSeek</h3>
    <p class="hint">这里只生成 Prompt，不会自动调用 DeepSeek。复制到免费版，结果粘回来再导入。</p>

    <div class="step-tabs">
      <button
        v-for="step in steps"
        :key="step.key"
        class="step-tab"
        :class="{ active: activeStep === step.key }"
        type="button"
        @click="activeStep = step.key"
      >
        {{ step.title }}
      </button>
    </div>

    <div v-for="step in steps" v-show="activeStep === step.key" :key="step.key" class="step-panel">
      <div class="preview-head">
        <div>
          <strong>{{ step.title }}</strong>
          <p class="hint">{{ step.note }}</p>
        </div>
      </div>

      <template v-if="step.key === 'hotspots'">
        <button type="button" :disabled="isLoading" @click="$emit('generatePrompt', 'hotspots')">生成热点 Prompt</button>
      </template>

      <template v-if="step.key === 'titles'">
        <button type="button" :disabled="isLoading" @click="$emit('generatePrompt', 'titles')">生成标题 Prompt</button>
      </template>

      <template v-if="step.key === 'outline'">
        <button type="button" :disabled="isLoading" @click="$emit('generatePrompt', 'outline')">生成大纲 Prompt</button>
      </template>

      <template v-if="step.key === 'draft'">
        <div class="choice-row">
          <label>
            <input v-model="draftMode" type="radio" value="direct" />
            按标题直接生成正文
          </label>
          <label>
            <input v-model="draftMode" type="radio" value="outline" />
            基于大纲生成正文
          </label>
        </div>
        <button type="button" :disabled="isLoading" @click="generateDraftPrompt($emit)">生成正文 Prompt</button>
      </template>

      <template v-if="step.key === 'image'">
        <button type="button" :disabled="isLoading || !canBuildFromDraft" @click="$emit('generatePrompt', 'image')">
          生成配图 Prompt
        </button>
      </template>
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
