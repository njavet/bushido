<template>
  <div>
    <h1>Bushido</h1>
    <h2>Units</h2>
    <label>Log Unit</label>
    <div class="terminal">
      <span class="prompt">user@bushido:~$</span>
      <input
        type="text"
        v-model="inputValue"
        placeholder="Type :emoji and press Enter"
        ref="terminalInput"
        @keydown.enter="handleEnter"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Tribute from 'tributejs'
import 'tributejs/dist/tribute.css'

let inputValue = ref("")
let terminalInput = ref(null)

onMounted(async () => {
  const res = await fetch('/api/emojis')
  const emojis = await res.json()

  const tribute = new Tribute({
    trigger: ":",
    values: emojis,
    selectTemplate: (item) => item.original.value,
  })
  tribute.attach(terminalInput.value)
})

async function handleEnter() {
  const res = await fetch('/api/log_unit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: inputValue.value })
  })
  const data = await res.json()
  console.log("Sent:", data.res)
  inputValue.value = ""
}
</script>

<style scoped>
.prompt {
  font-family: monospace;
  margin-right: 0.5rem;
}

.terminal {
  background: #111;
  color: #0f0;
  padding: 1rem;
  font-family: monospace;
  display: flex;
  align-items: center;
}

.terminal input {
  background: #000;
  color: #0f0;
  border: none;
  outline: none;
  font-family: monospace;
  width: 100%;
}
</style>
