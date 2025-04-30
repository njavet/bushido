<template>
  <div class="unit-history" ref="container">
    <div
        v-for="(msg, index) in units"
        :key="index"
        class="message">
      <div class="bubble">{{ msg.text }}</div>
    </div>
  </div>

  <div class="input-area">
    <input
      type="text"
      ref="inputRef"
      v-model="inputValue"
      @keydown.enter="sendMessage"
      placeholder="Log unit..."
      autofocus
    />
  </div>

</template>

<script setup>
import {nextTick, onMounted, ref, watch} from 'vue'
import Tribute from "tributejs";
const inputValue = ref('')
const inputRef = ref(null)
const units = ref([])
const container = ref(null)

onMounted(async () => {
  const res0 = await fetch('/api/emojis')
  const emojis = await res0.json()
  const res1 = await fetch('/api/get-units')
  const units = await res1.json()

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

watch(() => units.length, () => {
  nextTick(() => {
    if (container.value) {
      container.value.scrollTop = container.value.scrollHeight
    }
  })
})

async function sendMessage() {
  const res = await fetch('/api/log-unit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        text: inputValue.value
    })
  })
  const data = await res.json()
  inputValue.value = ''
  return data.response || 'Error.'
}
</script>
<style scoped>
  .unit-history {
    display: flex;
    flex-direction: column;
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    border: 2px solid cyan;
    border-radius: 8px;
    background-color: #333;
  }

  .bubble {
    max-width: 70%;
    padding: 0.75rem 1rem;
    border-radius: 18px;
    background: #444;
    word-break: break-word;
  }

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