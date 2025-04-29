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
const inputValue = ref('')
const inputRef = ref(null)
const emit = defineEmits(['send'])

onMounted(async () => {
  const res = await fetch('/api/emojis')
  const emojis = await res.json()

  const tribute = new Tribute({
    trigger: ":",
    values: emojis,
    menuItemTemplate: (item) => {
      return `<span>${item.original.value}  </span>${item.original.key}`
    },
    menuShowMinLength: 0,
    selectTemplate: (item) => item.original.value,
    menuContainer: inputRef.value.parentNode
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
<style>
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
.tribute-container {
  display: block;
  background: #1f1f1f;
  color: #f0f0f0;
  border: 1px solid #444;
  border-radius: 8px;
  overflow: hidden;
  font-size: 14px;
  text-align: left;
  z-index: 9999;
  width: 200px;
  max-width: 90vw;
}

.tribute-container ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.tribute-container li {
  padding: 8px 12px;
  cursor: pointer;
  width: 100%;
}

.tribute-container li.highlight {
  background: #333;
  color: #fff;
}

</style>