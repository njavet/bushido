<template>
  <div class="chat-area" ref="container">
    <div
      v-for="(msg, index) in messages"
      :key="index"
      class="message"
      :class="msg.role === 'User' ? 'user' : 'bot'"
    >
      <div class="bubble">{{ msg.text }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  messages: Array,
})

const container = ref(null)

watch(() => props.messages.length, () => {
  nextTick(() => {
    if (container.value) {
      container.value.scrollTop = container.value.scrollHeight
    }
  })
})
</script>
<style scoped>
.chat-area {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  border: 2px solid cyan;
  border-radius: 8px;
  background-color: #333;
}

.message {
  display: flex;
  margin: 0.5rem 0;
}

.message.user {
  justify-content: flex-end;
}

.message.bot {
  justify-content: flex-start;
}

.bubble {
  max-width: 70%;
  padding: 0.75rem 1rem;
  border-radius: 18px;
  background: #d1e7dd;
  word-break: break-word;
}

.message.user .bubble {
  background: #cfe2ff;
}
</style>
