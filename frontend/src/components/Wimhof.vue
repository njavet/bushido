<template>
  <div class="container">
    <h3>Wimhof Stats</h3>
    <div
      v-for="(day, units) in wimhofUnits"
      :key="day">

      {{units}}
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted} from "vue";
const wimhofUnits = ref([])

onMounted(async () => {
  const res = await fetch('/api/get-wimhof-units')
  wimhofUnits.value = await res.json()
})


</script>

<style scoped>
.container {
  background-color: #1f1f1f;
}
</style>