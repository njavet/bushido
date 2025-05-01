<template>
  <div class="container">
    <h3>Wimhof Stats</h3>
    <div ref="tableRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted} from "vue";
import * as Tabulator from 'tabulator-tables'

const tableRef = ref(null)
const wimhofUnits = ref([])

onMounted(async() => {
  const res = await fetch('/api/get-wimhof-units')
  wimhofUnits.value = await res.json()
  new Tabulator.Tabulator(tableRef.value, {
    data: wimhofUnits.value,
    layout: "fitColumns",
    height: "auto",
    columns: [
      { title: "Date", field: "date", width: 90 },
      { title: "Round", field: "round", width: 90 },
      { title: "Breaths", field: "breaths" },
      { title: "Retention", field: "retention" }
    ]
  })
})

onMounted(async () => {
})


</script>

<style scoped>
.container {
  background-color: #1f1f1f;
}
</style>