<script setup lang="ts">
import type { ArticleRecord } from '../../../types/article'

defineProps<{
  articles: ArticleRecord[]
}>()

defineEmits<{
  openArticle: [article: ArticleRecord]
  refresh: []
  exportWord: [articleId: number]
  deleteArticle: [articleId: number]
}>()
</script>

<template>
  <section class="panel saved">
    <div class="preview-head">
      <h3>7. 作品库</h3>
      <button type="button" @click="$emit('refresh')">刷新</button>
    </div>

    <p v-if="!articles.length" class="empty">还没有保存文章。</p>
    <div v-for="article in articles" :key="article.id" class="library-item">
      <div class="library-row">
        <strong>{{ article.title }}</strong>
        <div class="button-row compact">
          <button type="button" @click="$emit('openArticle', article)">打开</button>
          <button type="button" @click="$emit('exportWord', article.id)">导出 Word</button>
          <button type="button" @click="$emit('deleteArticle', article.id)">删除</button>
        </div>
      </div>
      <span>{{ article.summary }}</span>
      <small>{{ article.updated_at }}</small>
    </div>
  </section>
</template>
