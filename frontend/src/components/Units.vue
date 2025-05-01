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
  <div v-for="(days, week) in unitsByWeek" :key="week">
    <div class="week-header" @click="toggleWeek(week)">
      {{ expandedWeeks[week] ? '▼' : '▶' }} Week {{ week }}
    </div>

  <transition name="collapse">
    <div v-if="expandedWeeks[week]" class="week-content">
      <div
        v-for="(units, date) in days"
        :key="date"
        class="day-block"
      >
        <div class="date-header" @click="toggleDay(date)">
          {{ expandedDays[date] ? '▼' : '▶' }} {{ date }}
        </div>

        <transition name="collapse">
          <ul v-if="expandedDays[date]" class="unit-list">
            <li v-for="(unit, idx) in units" :key="idx" class="unit-entry">
              <span class="time">{{ unit.hms }}</span>
              <span class="emoji">{{ unit.emoji }}</span>
              <span class="payload">{{ unit.payload }}</span>
            </li>
          </ul>
        </transition>
      </div>
    </div>
  </transition>
  </div>

</template>

<script setup>
import {nextTick, onMounted, ref, watch} from 'vue'
import Tribute from "tributejs";
const inputValue = ref('')
const inputRef = ref(null)
const container = ref(null)
const unitsByWeek = ref({})
const expandedWeeks = ref({})
const expandedDays = ref({})

const props = defineProps(['emojis'])

function toggleWeek(week) {
  expandedWeeks.value[week] = !expandedWeeks.value[week]
}

function toggleDay(date) {
  expandedDays.value[date] = !expandedDays.value[date]
}

watch(() => props.emojis, (newVal) => {
  if (!newVal?.length || !inputRef.value) return
  const tribute = new Tribute({
    trigger: ":",
    values: props.emojis,
    menuItemTemplate: (item) => {
      return `<span>${item.original.value}  </span>${item.original.key}`
    },
    menuShowMinLength: 0,
    selectTemplate: (item) => item.original.value,
    menuContainer: inputRef.value.parentNode,
  })
  tribute.attach(inputRef.value)
}, { immediate: true })

onMounted(async () => {
  const res1 = await fetch('/api/get-units')
  unitsByWeek.value = await res1.json()
  expandedWeeks.value = Object.fromEntries(
      Object.keys(unitsByWeek.value).map(date => [date, false])
  )
})

function toggle(date) {
  expanded.value[date] = !expanded.value[date]
}

watch(() => unitsByWeek.length, () => {
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
    text-align: left;
  }
  .date-bubble {
    display: inline-block;
    background-color: #444;
    color: darkcyan;
    padding: 0.4em 1em;
    border-radius: 999px;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }
  .unit-list {
    list-style: none;
    padding-left: 0.5rem;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    margin-top: 0;
    margin-bottom: 0.4rem;
    background-color: #222;
    border-radius: 16px;
  }
  .unit-entry {
    display: flex;
    color: #fff;
    padding: 0.3rem;
    justify-content: space-between;
    align-items: center;
  }
  .payload {
    flex: 1 1 auto;
    text-align: left;
    padding: 0 1rem;
    white-space: nowrap;
    overflow-x: auto;
  }
  .time {
    flex: 0 0 auto;
    margin-top: 1rem;
    margin-right: 1rem;
    font-size: 8px;
  }
  .collapse-enter-active,
  .collapse-leave-active {
    transition: all 0.3s ease;
    overflow: hidden;
  }
  .collapse-enter-from,
  .collapse-leave-to {
    max-height: 0;
    opacity: 0;
  }
  .collapse-enter-to,
  .collapse-leave-from {
    max-height: 500px; /* max expected height */
    opacity: 1;
  }
</style>
