<template>
  <div class="dashboard">
    <div class="left-panel">
      <h2>Graphics</h2>
      <div class="graphic-box">[Chart Placeholder]</div>
      <div class="graphic-box">[Another Graphic]</div>
    </div>

    <div class="right-panel">
      <div class="history">
        <h2>Unit History</h2>
          <section v-for="(entries, date) in unitsByDay" :key="date" class="panel">
          <h3><span class="text-cyan-200">{{ date }}</span></h3>
          <ul>
            <li v-for="(entry, i) in entries" :key="i">
              <span class="text-cyan-100">{{ entry[0] }} {{ entry[1] }}</span>
            </li>
          </ul>
          </section>
      </div>
      <div class="input-area">
        <input
          type="text"
          v-model="inputValue"
          ref="terminalInput"
          @keydown.enter="handleEnter"
          placeholder="Log unit..."
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import Tribute from "tributejs";
import 'tributejs/dist/tribute.css'

const inputValue = ref("")
const terminalInput = ref(null)
const unitsByDay = ref({})
const history = ref([])

async function fetchUnits() {
  const res = await fetch('/api/get_units')
  const data = await res.json()
  console.log(data)
  unitsByDay.value = data
}

async function handleEnter() {
  const res = await fetch('/api/log_unit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: inputValue.value })
  })
  const data = await res.json()
  history.value.push(inputValue.value)
  inputValue.value = ""
}

onMounted(async () => {
  await fetchUnits()
  const res = await fetch('/api/emojis')
  const emojis = await res.json()

  const tribute = new Tribute({
    trigger: ":",
    values: emojis,
    selectTemplate: (item) => item.original.value,
  })
  tribute.attach(terminalInput.value)
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