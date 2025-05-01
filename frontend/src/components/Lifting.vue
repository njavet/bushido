<template>
  <div class="container">
    <vue-good-table
      :columns="columns"
      :rows="liftingUnits"
      :search-options="{ enabled: true }"
      :pagination-options="{ enabled: false }"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { VueGoodTable } from 'vue-good-table-next'
import 'vue-good-table-next/dist/vue-good-table-next.css'

const liftingUnits = ref([])
const tabs = []

const columns = [
  { label: 'Date', field: 'date', sortable: true },
  { label: 'Set', field: 'set', sortable: true },
  { label: 'Weight', field: 'weight', sortable: true },
  { label: 'Reps', field: 'reps', sortable: true },
  { label: 'Pause', field: 'pause', sortable: true }
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
}
</style>
