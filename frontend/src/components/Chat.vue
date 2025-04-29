<template>
  <div class="chat">
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
    messages.value.push({ role: 'Bot', text: response, tab: currentTab.value })
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
</style>