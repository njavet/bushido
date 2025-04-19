<template>
  <div class="dashboard">
    <!-- Left: Graphics -->
    <div class="left-panel">
      <h2>Graphics</h2>
      <div class="graphic-box">[Chart Placeholder]</div>
      <div class="graphic-box">[Another Graphic]</div>
    </div>

    <!-- Right: Input + History -->
    <div class="right-panel">
      <div class="history">
        <h2>History</h2>
        <pre class="history-text">{{ history.join('\n') }}</pre>
      </div>
      <div class="input-area">
        <input
          type="text"
          v-model="input"
          ref="inputField"
          @keydown.enter="submit"
          placeholder="Type something..."
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import Tribute from 'tributejs'

const input = ref('')
const history = ref([])

function submit() {
  if (input.value.trim()) {
    history.value.push(`> ${input.value}`)
    input.value = ''
  }
}

onMounted(() => {
  const tribute = new Tribute({
    values: [
      { key: 'run', value: ':run' },
      { key: 'reset', value: ':reset' },
      { key: 'help', value: ':help' },
    ],
  })
  tribute.attach(document.querySelector('input'))
})
</script>

<style>
.dashboard {
  display: flex;
  height: 100vh;
  font-family: sans-serif;
}

.left-panel,
.right-panel {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
  overflow-y: auto;
}

.left-panel {
  background-color: #222;
  color: #fff;
}

.right-panel {
  background-color: #111;
  color: #eee;
  display: flex;
  flex-direction: column;
}

.graphic-box {
  background-color: #333;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.history {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 10px;
}

.history-text {
  white-space: pre-wrap;
  font-family: monospace;
}

.input-area input {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: none;
  font-size: 1em;
  background-color: #222;
  color: white;
  outline: none;
}
</style>