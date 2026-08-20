<script setup lang="ts">
const props = defineProps<{
  keywords: string
  canImport: boolean
  isLoading: boolean
}>()

const manualHotspotText = defineModel<string>('manualHotspotText', { required: true })

defineEmits<{
  importHotspots: []
}>()

function searchUrl(platform: 'baidu' | 'weibo' | 'bilibili') {
  const query = encodeURIComponent(props.keywords || '')
  if (platform === 'baidu') return `https://www.baidu.com/s?wd=${query}`
  if (platform === 'weibo') return `https://s.weibo.com/weibo?q=${query}`
  return `https://search.bilibili.com/all?keyword=${query}`
}
</script>

<template>
  <section class="panel manual-hotspot-panel">
    <h3>2. 手动热点粘贴</h3>
    <p class="hint">自动抓取不可用时，打开平台搜索，把热词、标题或评论切口复制回来整理成临时方向。</p>

    <div class="button-row">
      <a :href="searchUrl('baidu')" target="_blank" rel="noreferrer">百度搜索</a>
      <a :href="searchUrl('weibo')" target="_blank" rel="noreferrer">微博搜索</a>
      <a :href="searchUrl('bilibili')" target="_blank" rel="noreferrer">B站搜索</a>
    </div>

    <label>
      平台复制内容
      <textarea v-model="manualHotspotText" rows="6" placeholder="每行粘贴一个热词、标题、评论切口或讨论点"></textarea>
    </label>

    <div class="actions">
      <button type="button" :disabled="isLoading || !canImport" @click="$emit('importHotspots')">
        整理为临时方向
      </button>
    </div>
  </section>
</template>
