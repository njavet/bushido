<template>
  <div class="chat">
    <div class="tab-bar">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        :class="{ active: currentTab === tab.key }"
        @click="currentTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <ChatContainer
      :messages="filteredMessages"
    />

    <ChatInput
      @send="handleUserMessage"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ChatInput from './ChatInput.vue'
import { tabs, normalizeText, sendMessage, sendFile } from '../js/chatUtils'
import ChatContainer from "./ChatContainer.vue";

const messages = ref([])
const currentTab = ref('base')
const inputValue = ref('')
const loading = ref(false)

const props = defineProps({
  base_url: String,
  lm_name: String,
  system_message: String
})

const filteredMessages = computed(() =>
  messages.value.filter(msg => msg.tab === currentTab.value)
)

function handleUserMessage(text) {
  const query = text.trim()
  if (!query) return

  loading.value = true
  messages.value.push({ role: 'User', text: query, tab: currentTab.value })

  sendMessage({
    query,
    props,
    tab: currentTab.value
  }).then(response => {
    messages.value.push({ role: 'Bot', text: normalizeText(response), tab: currentTab.value })
    loading.value = false
  })
}

function handleFileUpload(file) {
  loading.value = true
  messages.value.push({ role: 'User', text: `[Sent DOCX: ${file.name}]`, tab: currentTab.value })

  sendFile({
    file,
    props,
    tab: currentTab.value
  }).then(response => {
    messages.value.push({ role: 'Bot', text: normalizeText(response), tab: currentTab.value })
    loading.value = false
  })
}
</script>