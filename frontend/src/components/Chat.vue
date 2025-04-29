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
import ChatContainer from "./ChatContainer.vue";
import ChatInput from './ChatInput.vue'
import { tabs, sendMessage } from '../js/chatUtils'

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
<style scoped>
.chat {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  background: #f8f9fa;
  font-family: Arial, sans-serif;
}

.tab-bar {
  display: flex;
  justify-content: center;
  background: #e9ecef;
  padding: 0.5rem;
}

.tab-bar button {
  background: none;
  border: none;
  padding: 0.5rem 1rem;
  margin: 0 0.25rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}

.tab-bar button.active {
  background: #dee2e6;
  border-radius: 8px;
}
</style>