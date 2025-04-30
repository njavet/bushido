<template>
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
  <div class="unit-history" ref="container">
    <div
        v-for="(units, date) in unitsByDay"
        :key="date"
        class="date-block">
      <div class="date-bubble">{{ date }}</div>
      <ul class="unit-list">
        <li v-for="(unit, idx) in units"
            :key="idx"
            class="unit-entry">
          <span class="emoji">{{ unit.emoji }}</span>
          <span class="payload">{{ unit.payload }}</span>
          <span class="time">{{ unit.hms }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import {nextTick, onMounted, ref, watch} from 'vue'
import Tribute from "tributejs";
const inputValue = ref('')
const inputRef = ref(null)
const unitsByDay = ref([])
const container = ref(null)

onMounted(async () => {
  const res0 = await fetch('/api/emojis')
  const emojis = await res0.json()
  const res1 = await fetch('/api/get-units')
  unitsByDay.value = await res1.json()

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

watch(() => unitsByDay.length, () => {
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

  .date-block {
    margin-bottom: 2rem;
  }

  .date-bubble {
    display: inline-block;
    background-color: #d0e7ff;
    color: #004080;
    padding: 0.4em 1em;
    border-radius: 999px;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }

  .unit-list {
    list-style: none;
    padding-left: 1.5rem;
    margin-top: 0.3rem;
  }

  .unit-entry {
    background-color: #222;
    color: #fff;
    padding: 0.5rem 0.75rem;
    border-radius: 6px;
    margin-bottom: 0.5rem;
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
</style>
