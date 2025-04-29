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