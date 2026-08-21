<script setup lang="ts">
import { ref } from 'vue'
import type { Direction } from '../../../types/article'

defineProps<{
  directions: Direction[]
  isLoading: boolean
}>()

const keywords = defineModel<string>('keywords', { required: true })
const selectedDirection = defineModel<Direction | null>('selectedDirection', { required: true })
const isConfigOpen = ref(false)
const selectedGeneration = ref('90后')
const selectedContentType = ref('动漫')
const selectedArticleAngle = ref('怀旧')
const targetName = ref('')
const extraWords = ref('')

const generationOptions = ['80后', '90后', '00后', '10后']
const contentTypeOptions = ['电视剧', '电影', '动画', '动漫', '小说', '游戏', '综艺']
const articleAngleOptions = ['怀旧', '盘点', '单人/单作品', '对比', '热点评论', '重看感受']

defineEmits<{
  generate: []
}>()

function setGeneration(value: string) {
  selectedGeneration.value = value
}

function setContentType(value: string) {
  selectedContentType.value = value
}

function setArticleAngle(value: string) {
  selectedArticleAngle.value = value
}

function buildKeywords() {
  keywords.value = [selectedGeneration.value, selectedContentType.value, selectedArticleAngle.value, targetName.value, extraWords.value]
    .map((item) => item.trim())
    .filter(Boolean)
    .join(' ')
}

function clearKeywordConfig() {
  targetName.value = ''
  extraWords.value = ''
  keywords.value = ''
}
</script>

<template>
  <section class="panel">
    <h3>选题设置</h3>
    <p class="hint">可以直接输入关键词，也可以展开配置后自动生成。</p>

    <div class="keyword-summary">
      <strong>{{ keywords || '还没有关键词' }}</strong>
      <button type="button" @click="isConfigOpen = !isConfigOpen">
        {{ isConfigOpen ? '收起配置' : '展开配置' }}
      </button>
    </div>

    <div v-if="isConfigOpen" class="keyword-config">
      <div>
        <span>年代</span>
        <div class="chip-row">
          <button
            v-for="option in generationOptions"
            :key="option"
            class="chip"
            :class="{ selected: selectedGeneration === option }"
            type="button"
            @click="setGeneration(option)"
          >
            {{ option }}
          </button>
        </div>
      </div>

      <div>
        <span>内容类型</span>
        <div class="chip-row">
          <button
            v-for="option in contentTypeOptions"
            :key="option"
            class="chip"
            :class="{ selected: selectedContentType === option }"
            type="button"
            @click="setContentType(option)"
          >
            {{ option }}
          </button>
        </div>
      </div>

      <div>
        <span>写作方向</span>
        <div class="chip-row">
          <button
            v-for="option in articleAngleOptions"
            :key="option"
            class="chip"
            :class="{ selected: selectedArticleAngle === option }"
            type="button"
            @click="setArticleAngle(option)"
          >
            {{ option }}
          </button>
        </div>
      </div>

      <label>
        指定作品/人物（可选）
        <input v-model="targetName" placeholder="例如：龙珠、仙剑奇侠传、李连杰" />
      </label>

      <label>
        补充关键词（可选）
        <input v-model="extraWords" placeholder="例如：童年回忆、名场面、片头曲、重映" />
      </label>

      <div class="button-row">
        <button type="button" @click="buildKeywords">生成关键词</button>
        <button type="button" @click="clearKeywordConfig">清空重填</button>
      </div>
    </div>

    <label>
      关键词
      <textarea v-model="keywords" rows="3" placeholder="例如：90后 动漫 怀旧 龙珠 童年回忆 名场面"></textarea>
    </label>

    <div class="actions">
      <button type="button" :disabled="isLoading || !keywords.trim()" @click="$emit('generate')">
        本地生成方向（不调用 DeepSeek）
      </button>
    </div>

    <p v-if="!directions.length" class="empty">输入关键词后，可以本地生成方向，也可以在“方向来源”里粘贴平台热点或 DeepSeek 方向。</p>
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
