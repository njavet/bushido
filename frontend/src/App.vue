<template>
  <h1>Bushido</h1>
  <div class="app-container">
    <Sidebar :emojis="emojis"/>
    <div class="main-content">
      <Units :emojis="emojis" />
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted} from "vue";
import Sidebar from "./components/Sidebar.vue"
import Units from "./components/Units.vue";

const emojis = ref([])

onMounted(async() => {
  const res = await fetch('/api/emojis')
  emojis.value = await res.json()
})
</script>

<style scoped>
.app-container {
  flex: 1;
  display: flex;
  overflow: hidden;
}
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
