<template>
  <div class="input-area horizontal">
    <input
      type="text"
      v-model="inputValue"
      @keydown.enter="emitSend"
      placeholder="Type your message..."
      autofocus
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
const inputValue = ref('')
const emit = defineEmits(['send'])

function emitSend() {
  if (inputValue.value) {
    emit('send', inputValue.value)
    inputValue.value = ''
  }
}

</script>
<style scoped>
.input-area {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: #333;
}

.input-area input[type="text"] {
  flex-grow: 1;
  padding: 0.5rem;
  border: none;
  border-radius: 8px;
  outline: none;
}
</style>