<template>
  <div class="chat">
    <ChatContainer
      :messages="messages"
    />
    <ChatInput
      @send="handleUserMessage"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ChatContainer from "./ChatContainer.vue";
import ChatInput from './ChatInput.vue'
import { sendMessage } from '../js/chatUtils'

const messages = ref([])

const props = defineProps({
  base_url: String,
  lm_name: String,
  system_message: String
})

function handleUserMessage(text) {
  if (!text) return
  messages.value.push({ role: 'User', text: text })

  sendMessage({
    text,
    props,
  }).then(response => {
    messages.value.push({ role: 'Bot', text: response })
  })
}
</script>
<style scoped>
.chat {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  font-family: monospace;
}
</style>