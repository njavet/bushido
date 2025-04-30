<template>
  <h1>Bushido</h1>
  <div class="app-container">
    <Sidebar :categories="categories"/>
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
const categories = ref([])

onMounted(async() => {
  const category_res = await fetch('/api/get-categories')
  categories.value = await category_res.json()

  const emoji_res = await fetch('/api/get-emojis')
  emojis.value = await emoji_res.json()
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
