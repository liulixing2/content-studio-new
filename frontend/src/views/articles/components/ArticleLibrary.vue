<script setup lang="ts">
import type { ArticleRecord } from '../../../types/article'

defineProps<{
  articles: ArticleRecord[]
}>()

defineEmits<{
  refresh: []
}>()
</script>

<template>
  <section class="panel saved">
    <div class="preview-head">
      <h3>4. 作品库</h3>
      <button type="button" @click="$emit('refresh')">刷新</button>
    </div>

    <p v-if="!articles.length" class="empty">还没有保存文章。</p>
    <div v-for="article in articles" :key="article.id" class="library-item">
      <strong>{{ article.title }}</strong>
      <span>{{ article.summary }}</span>
      <small>{{ article.updated_at }}</small>
    </div>
  </section>
</template>
