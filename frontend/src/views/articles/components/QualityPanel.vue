<script setup lang="ts">
import type { QualityReport } from '../../../types/article'

defineProps<{
  report: QualityReport | null
  canCheck: boolean
  isLoading: boolean
}>()

defineEmits<{
  check: []
}>()
</script>

<template>
  <section class="panel quality-panel">
    <div class="preview-head">
      <h3>5. 发布检测</h3>
      <button type="button" :disabled="isLoading || !canCheck" @click="$emit('check')">检测当前草稿</button>
    </div>

    <p v-if="!report" class="empty">保存前先检测。检测报告也是临时结果，不会自动保存。</p>
    <div v-else>
      <p class="quality-result" :class="{ pass: report.publishable }">
        {{ report.publishable ? '建议：可以保存发布' : '建议：先修改后再保存' }}，评分 {{ report.score }}
      </p>
      <ul v-if="report.issues.length">
        <li v-for="issue in report.issues" :key="issue.message">
          <strong>{{ issue.level }}</strong> {{ issue.message }}
        </li>
      </ul>
      <ul v-if="report.suggestions.length">
        <li v-for="suggestion in report.suggestions" :key="suggestion">{{ suggestion }}</li>
      </ul>
    </div>
  </section>
</template>
