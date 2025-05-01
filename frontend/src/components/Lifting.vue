<template>
  <div class="container">
    <div class="tab-bar">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        :class="{ active: currentTab === tab.key}"
        :title="tab.unit_name"
        @click="currentTab = tab.key">
        {{ tab.label }}
      </button>
    </div>
    <div>
      <vue-good-table
          :columns="columns"
          :rows="filteredUnits"
          :search-options="{ enabled: true }"
          :pagination-options="{ enabled: false }"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { VueGoodTable } from 'vue-good-table-next'
import 'vue-good-table-next/dist/vue-good-table-next.css'

const props = defineProps(['emojis'])
const tabs = props.emojis.map(({key, value}) => ({
  key,
  label: value,
  unit_name: key
}))
const currentTab = ref(tabs.length ? tabs[0].key : null)
const liftingUnits = ref([])
const filteredUnits = computed(() =>
    liftingUnits.value.filter(unit => unit.unit_name === currentTab.value)
)

const numericSort = (a, b) => Number(b) - Number(a)
const columns = [
  { label: 'Date', field: 'date', sortable: true },
  { label: 'Set', field: 'set', sortable: true, sortFn: numericSort },
  { label: 'Weight', field: 'weight', sortable: true, sortFn: numericSort},
  { label: 'Reps', field: 'reps', sortable: true, sortFn: numericSort},
  { label: 'Pause', field: 'pause', sortable: true, sortFn: numericSort }
]

onMounted(async () => {
  const res = await fetch('/api/get-lifting-units')
  liftingUnits.value = await res.json()
})

</script>

<style scoped>
.container {
  padding: 1rem;
  background: #1f1f1f;
  color: white;
  border-radius: 8px;
  border: 2px solid darkcyan;
}
.tab-bar {
  display: flex;
  gap: 1rem;
  margin: 1rem;
}
.tab-bar button {
  background: #444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s ease;
}
.tab-bar button.active {
  background: cyan;
  color: black;
}
</style>
