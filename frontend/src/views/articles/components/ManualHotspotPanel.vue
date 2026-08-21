<script setup lang="ts">
const props = defineProps<{
  keywords: string
  canImport: boolean
  isLoading: boolean
}>()

const manualHotspotText = defineModel<string>('manualHotspotText', { required: true })

defineEmits<{
  generateDirectionPrompt: []
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
    <h3>方向来源</h3>
    <p class="hint">
      可以从百度、微博、B站复制热点，也可以去 DeepSeek 生成可写方向后粘贴回来；这里仍然只是整理临时方向。
    </p>

    <div class="button-row">
      <a :href="searchUrl('baidu')" target="_blank" rel="noreferrer">百度搜索</a>
      <a :href="searchUrl('weibo')" target="_blank" rel="noreferrer">微博搜索</a>
      <a :href="searchUrl('bilibili')" target="_blank" rel="noreferrer">B站搜索</a>
      <button type="button" :disabled="isLoading || !keywords.trim()" @click="$emit('generateDirectionPrompt')">
        生成 DeepSeek 方向 Prompt
      </button>
    </div>

    <label>
      平台热点 / DeepSeek 方向
      <textarea
        v-model="manualHotspotText"
        rows="6"
        placeholder="每行粘贴一个热词、标题、评论切口，或 DeepSeek 返回的可写方向"
      ></textarea>
    </label>

    <div class="actions">
      <button type="button" :disabled="isLoading || !canImport" @click="$emit('importHotspots')">
        粘贴内容整理为方向
      </button>
    </div>
  </section>
</template>
