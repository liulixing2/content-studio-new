<script setup lang="ts">
import type { Direction } from '../../../types/article'

defineProps<{
  directions: Direction[]
  isLoading: boolean
}>()

const keywords = defineModel<string>('keywords', { required: true })
const selectedDirection = defineModel<Direction | null>('selectedDirection', { required: true })

defineEmits<{
  generate: []
}>()
</script>

<template>
  <section class="panel">
    <h3>1. 关键词与方向</h3>
    <label>
      关键词
      <textarea v-model="keywords" rows="4" placeholder="例如：90后 动漫 龙珠 热血"></textarea>
    </label>

    <div class="actions">
      <button type="button" :disabled="isLoading || !keywords.trim()" @click="$emit('generate')">
        抓取/生成方向
      </button>
    </div>

    <p v-if="!directions.length" class="empty">输入关键词后生成可写方向。</p>
    <button
      v-for="direction in directions"
      :key="direction.title"
      class="option"
      :class="{ selected: selectedDirection?.title === direction.title }"
      type="button"
      @click="selectedDirection = direction"
    >
      <strong>{{ direction.title }}</strong>
      <span>{{ direction.reader_question }}</span>
      <small>{{ direction.angle }}</small>
    </button>
  </section>
</template>
