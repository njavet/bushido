<template>
  <main class="terminal">
    <div class="history">
      <section v-for="(entries, date) in unitsByDay" :key="date" class="panel">
        <h3><span class="text-cyan-200">{{ date }}</span></h3>
        <ul>
          <li v-for="(entry, i) in entries" :key="i">
            <span class="text-cyan-100">{{ entry[0] }} {{ entry[1] }}</span>
          </li>
        </ul>
      </section>
      <section v-if="show.day" class="panel">
        <h3>Today</h3>
        <ul>
          <li v-for="(entry, i) in todayEntries" :key="i">{{ entry }}</li>
        </ul>
      </section>

      <section v-if="show.week" class="panel">
        <h3>This Week</h3>
        <ul>
          <li v-for="(entry, i) in weekEntries" :key="i">{{ entry }}</li>
        </ul>
      </section>
    </div>

    <div class="input">
      <span class="prompt">user@bushido:~$</span>
      <input
          type="text"
          v-model="inputValue"
          ref="terminalInput"
          @keydown.enter="handleEnter"
          placeholder=":emoji command..."
      />
    </div>
  </main>
</template>

<script setup>
import {onMounted, reactive, ref} from "vue";
import Tribute from "tributejs";
import 'tributejs/dist/tribute.css'
const show = reactive({ day: true, week: true })
const inputValue = ref('')
const terminalInput = ref(null)
const unitsByDay = ref({})
const todayEntries = ref([])
const weekEntries = ref([])

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
  todayEntries.value.push(inputValue.value)
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

<style scoped>
.terminal {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  background: #111;
  color: #0f0;
  font-family: monospace;
  overflow: hidden;
}

.history {
  flex-grow: 1;
  overflow-y: auto;
  padding: 1rem;
  scroll-behavior: smooth;
}

.input {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: #000;
}

.input .prompt {
  margin-right: 0.5rem;
}

.input input {
  flex-grow: 1;
  background: #000;
  color: #0f0;
  border: none;
  outline: none;
  font-family: monospace;
}

.panel {
  margin-bottom: 1rem;
}

.panel h3 {
  margin: 0 0 0.5rem;
}
</style>