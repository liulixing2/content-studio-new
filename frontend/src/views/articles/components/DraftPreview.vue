<script setup lang="ts">
import type { DraftArticle, RenderedArticle } from '../../../types/article'

defineProps<{
  draft: DraftArticle | null
  rendered: RenderedArticle | null
  canSave: boolean
  isLoading: boolean
}>()

defineEmits<{
  copyHtml: []
  copyText: []
  save: []
  exportWord: []
}>()
</script>

<template>
  <section class="panel preview-panel">
    <div class="preview-head">
      <h3>正文预览</h3>
      <div class="button-row compact">
        <button type="button" :disabled="isLoading || !canSave" @click="$emit('copyHtml')">复制富文本</button>
        <button type="button" :disabled="isLoading || !canSave" @click="$emit('copyText')">复制纯文本</button>
        <button type="button" :disabled="isLoading || !canSave" @click="$emit('exportWord')">导出 Word</button>
        <button type="button" :disabled="isLoading || !canSave" @click="$emit('save')">保存到作品库</button>
      </div>
    </div>

    <p v-if="!draft" class="empty">粘贴正文导入后，会自动套公众号模板显示在这里。未保存前刷新会丢失。</p>
    <div v-else>
      <div class="article-preview" v-html="rendered?.html"></div>
      <h4>复制用纯文本</h4>
      <pre>{{ rendered?.text }}</pre>
    </div>
  </section>
</template>
