<template>
  <div class="container">
    <h3>Wimhof Stats</h3>
    <vue-good-table
      :columns="columns"
      :rows="wimhofUnits"
      :search-options="{ enabled: true }"
      :pagination-options="{ enabled: true, perPage: 10 }"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { VueGoodTable } from 'vue-good-table-next'
import 'vue-good-table-next/dist/vue-good-table-next.css'

const wimhofUnits = ref([])

const columns = [
  { label: 'Date', field: 'date', sortable: true },
  { label: 'Round', field: 'round', sortable: true },
  { label: 'Breaths', field: 'breaths', sortable: true },
  { label: 'Retention', field: 'retention', sortable: true }
]

onMounted(async () => {
  const res = await fetch('/api/get-wimhof-units')
  wimhofUnits.value = await res.json()
})
</script>

<style scoped>
.container {
  padding: 1rem;
  background: #1f1f1f;
  color: white;
  border-radius: 8px;
}
</style>