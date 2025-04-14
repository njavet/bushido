<template>
  <div class="layout">
    <aside class="sidebar">
      <h2 class="section-title">Bushido</h2>
      <nav>
        <ul>
          <li><button @click="togglePanel('day')">Day View</button></li>
          <li><button @click="togglePanel('week')">Week View</button></li>
        </ul>
      </nav>
    </aside>

    <main class="chat">
      <div class="history">
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import Tribute from "tributejs";
import 'tributejs/dist/tribute.css'

const inputValue = ref("")
const terminalInput = ref(null)
const show = reactive({ day: true, week: true })
const todayEntries = ref([])
const weekEntries = ref([])

function togglePanel(view) {
  show[view] = !show[view]
}

async function handleEnter() {
  const res = await fetch('/api/log_unit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: inputValue.value })
  })
  const data = await res.json()
  todayEntries.value.push(`${emoji} ${words.join(" ")}`)
  inputValue.value = ""
}

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

</script>

<style scoped>
body, html, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

.layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.sidebar {
  width: 200px;
  background: #222;
  color: #fff;
  padding: 1rem;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
}

.sidebar .section-title {
  margin-bottom: 1rem;
}

.chat {
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
