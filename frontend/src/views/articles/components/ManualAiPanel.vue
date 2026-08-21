<script setup lang="ts">
import { ref } from 'vue'
import type { Direction } from '../../../types/article'

const props = defineProps<{
  keywords: string
  selectedDirection: Direction | null
  selectedTitle: string
  canImport: boolean
  isLoading: boolean
}>()

const pastedText = defineModel<string>('pastedText', { required: true })
const manualHotspotText = defineModel<string>('manualHotspotText', { required: true })
const selectedTemplate = ref('情绪共鸣文')
const promptText = ref('')

const templateOptions = [
  {
    name: '情绪共鸣文',
    content: [
      '模板：情绪共鸣文',
      '- 开头用一个具体生活场景切入，不要写“开头切入”这种模板标题。',
      '- 摘要用一句话说明文章对象和核心情绪。',
      '- 正文按 3-4 个顺序小标题展开，每节都要有具体画面、判断或情绪转折。',
      '- 结尾只保留一个“互动话题”。',
    ],
  },
  {
    name: '单作品深聊',
    content: [
      '模板：单作品深聊',
      '- 全文只围绕标题里的一个对象展开，不扩展成泛泛清单。',
      '- 结构建议：为什么被想起、真正留下什么、现在重看有什么变化、互动话题。',
      '- 每一节都必须回应标题里的核心对象，不能只写通用怀旧。',
    ],
  },
  {
    name: '对比观点文',
    content: [
      '模板：对比观点文',
      '- 如果标题包含两个或多个对象，正文要逐段比较差异。',
      '- 不要简单分胜负，要写清楚它们分别代表哪种情绪、记忆或价值。',
      '- 结尾把选择权交给读者，只保留一个互动话题。',
    ],
  },
  {
    name: '清单盘点文',
    content: [
      '模板：清单盘点文',
      '- 每个对象独立成节，不要复制同一种句式。',
      '- 每节包含：具体记忆点、为什么被记住、现在回看的一层理解。',
      '- 避免所有对象都写成“很多人先记住，长大后才发现”。',
    ],
  },
  {
    name: '普通观点文',
    content: [
      '模板：普通观点文',
      '- 不要写“最近热议”“全网都在说”“网友都在讨论”等需要来源支撑的表达。',
      '- 直接围绕标题提出观点、展开理由、给出读者能接住的结尾问题。',
      '- 不编造平台、数据、链接、发布时间或引用。',
    ],
  },
]

defineEmits<{
  copyPrompt: [promptText: string]
  importDraft: []
}>()

function appendBlock(title: string, lines: string[]) {
  const block = [`【${title}】`, ...lines].filter(Boolean).join('\n')
  promptText.value = [promptText.value.trim(), block].filter(Boolean).join('\n\n')
}

function insertDirection() {
  const direction = props.selectedDirection
  appendBlock('方向/分类', [
    `关键词：${props.keywords || '请在这里填写关键词'}`,
    direction ? `已选方向：${direction.title}` : '已选方向：请在这里填写文章方向',
    direction?.reader_question ? `读者问题：${direction.reader_question}` : '',
    direction?.angle ? `写作角度：${direction.angle}` : '',
  ])
}

function insertTitle() {
  appendBlock('标题', [`${props.selectedTitle || '请在这里填写标题'}`])
}

function insertHotwords() {
  appendBlock('热词/补充要求', [manualHotspotText.value || '请在这里填写想保留的热词、关键词、角度或禁用表达'])
}

function insertOutline() {
  appendBlock('大纲', [
    '请按这个结构写，也可以在保证标题一致的前提下微调：',
    '一、用具体场景打开话题',
    '二、解释这个对象为什么会被记住',
    '三、写现在回看时多出来的理解',
    '四、用一个问题收束到评论区',
  ])
}

function insertTemplate() {
  const template = templateOptions.find((option) => option.name === selectedTemplate.value) || templateOptions[0]
  appendBlock('模板', template.content)
}

function resetPrompt() {
  promptText.value = ''
}

function buildBasePrompt() {
  promptText.value = [
    '请根据下面要求生成一篇可直接导入公众号编辑器的正文。',
    '',
    '输出格式必须严格包含：',
    '标题：',
    '摘要：',
    '一、',
    '二、',
    '三、',
    '互动话题：',
    '',
    '硬性要求：',
    '1. 不要解释写作过程，不要输出 Markdown 代码块。',
    '2. 小标题必须顺序编号，不能出现两个“一、”。',
    '3. 不要使用“开头切入”“正文展开”“结尾收束”这种模板小标题。',
    '4. 正文最后只能有一个“互动话题”，不要再写“互动引导”。',
    '5. 不要输出素材说明、版权说明、参考来源、配图建议。',
    '6. 不要编造平台、数据、链接、发布时间或引用。',
    '7. 每一节必须回应标题里的核心对象或核心问题。',
    '8. 避免空泛套话，每一节都要有具体画面、判断或信息增量。',
  ].join('\n')
}

</script>

<template>
  <section class="panel manual-panel">
    <h3>生成正文 Prompt</h3>
    <p class="hint">这里是最终复制给 DeepSeek 免费版的大输入框。按钮只是插入内容，你可以继续手动改。</p>

    <div class="prompt-builder">
      <div class="prompt-toolbar">
        <button type="button" @click="buildBasePrompt">基础规则</button>
        <button type="button" @click="insertDirection">方向/分类</button>
        <button type="button" @click="insertTitle">标题</button>
        <button type="button" @click="insertHotwords">热词</button>
        <button type="button" @click="insertOutline">大纲</button>
        <button type="button" @click="insertTemplate">模板</button>
      </div>

      <label>
        模板选择
        <select v-model="selectedTemplate">
          <option v-for="option in templateOptions" :key="option.name" :value="option.name">{{ option.name }}</option>
        </select>
      </label>

      <label>
        热词 / 补充要求（可选）
        <textarea v-model="manualHotspotText" rows="3" placeholder="例如：强调童年暗号、不要写成清单、不要提全网热议"></textarea>
      </label>

      <label>
        DeepSeek 输入框
        <textarea
          v-model="promptText"
          class="prompt-editor"
          rows="16"
          placeholder="点击上方按钮插入基础规则、方向、标题、大纲或模板，也可以直接在这里手写完整问题。"
        ></textarea>
      </label>

      <div class="button-row compact">
        <button type="button" :disabled="!promptText.trim()" @click="$emit('copyPrompt', promptText)">复制去 DeepSeek</button>
        <button type="button" :disabled="!promptText.trim()" @click="resetPrompt">清空重写</button>
      </div>
    </div>

    <label>
      粘贴 DeepSeek 返回正文
      <textarea v-model="pastedText" rows="8" placeholder="把 DeepSeek 生成的公众号正文粘贴到这里；没选标题时会尝试用第一行作为标题"></textarea>
    </label>
    <div class="actions">
      <button type="button" :disabled="isLoading || !canImport" @click="$emit('importDraft')">导入并套公众号模板</button>
    </div>
  </section>
</template>
