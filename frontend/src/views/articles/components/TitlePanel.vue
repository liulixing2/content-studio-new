<script setup lang="ts">
defineProps<{
  titles: string[]
  canCreateTitles: boolean
  canCreateDraft: boolean
  isLoading: boolean
}>()

const selectedTitle = defineModel<string>('selectedTitle', { required: true })

defineEmits<{
  generateTitles: []
  generateDraft: []
}>()
</script>

<template>
  <section class="panel">
    <h3>3. 标题与草稿</h3>
    <div class="actions">
      <button type="button" :disabled="isLoading || !canCreateTitles" @click="$emit('generateTitles')">
        生成标题
      </button>
      <button type="button" :disabled="isLoading || !canCreateDraft" @click="$emit('generateDraft')">
        生成临时草稿
      </button>
    </div>

    <p v-if="!titles.length" class="empty">选择方向后生成多个标题，再选一个生成正文。</p>
    <button
      v-for="title in titles"
      :key="title"
      class="option"
      :class="{ selected: selectedTitle === title }"
      type="button"
      @click="selectedTitle = title"
    >
      <strong>{{ title }}</strong>
    </button>
  </section>
</template>
