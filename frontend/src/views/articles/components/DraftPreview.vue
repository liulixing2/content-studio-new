<script setup lang="ts">
import type { DraftArticle, RenderedArticle } from '../../../types/article'

defineProps<{
  draft: DraftArticle | null
  rendered: RenderedArticle | null
  canSave: boolean
  isLoading: boolean
}>()

defineEmits<{
  save: []
}>()
</script>

<template>
  <section class="panel preview-panel">
    <div class="preview-head">
      <h3>3. 临时预览</h3>
      <button type="button" :disabled="isLoading || !canSave" @click="$emit('save')">保存到作品库</button>
    </div>

    <p v-if="!draft" class="empty">草稿生成后会显示在这里。未保存前刷新会丢失。</p>
    <div v-else>
      <div class="article-preview" v-html="rendered?.html"></div>
      <h4>复制用纯文本</h4>
      <pre>{{ rendered?.text }}</pre>
    </div>
  </section>
</template>
