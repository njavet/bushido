<template>
  <div class="input-area horizontal">
    <input
      type="text"
      ref="inputRef"
      v-model="inputValue"
      @keydown.enter="emitSend"
      placeholder="Log unit..."
      autofocus
    />
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import Tribute from "tributejs";
import 'tributejs/dist/tribute.css'
const inputValue = ref('')
const inputRef = ref(null)
const emit = defineEmits(['send'])

onMounted(async () => {
  const res = await fetch('/api/emojis')
  const emojis = await res.json()

  const tribute = new Tribute({
    trigger: ":",
    values: emojis,
    selectTemplate: (item) => item.original.value,
  })
  if (inputRef.value) {
    tribute.attach(inputRef.value)
  }
})

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