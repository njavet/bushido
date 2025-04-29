<template>
  <div class="input-area horizontal">
    <input
      type="text"
      v-model="inputValue"
      @keydown.enter="emitSend"
      :disabled="disabled"
      :title="disabled ? 'Select a model first' : ''"
      placeholder="Type your message..."
      autofocus
    />
    <div class="upload-area">
      <label for="upload" class="upload-button">@</label>
      <input
        id="upload"
        type="file"
        accept=".docx"
        @change="emitUpload"
        :disabled="disabled"
        hidden
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const inputValue = ref('')
const props = defineProps({ disabled: Boolean })

const emit = defineEmits(['send', 'upload'])

function emitSend() {
  if (inputValue.value.trim()) {
    emit('send', inputValue.value)
    inputValue.value = ''
  }
}

function emitUpload(event) {
  const file = event.target.files[0]
  if (file) emit('upload', file)
}
</script>