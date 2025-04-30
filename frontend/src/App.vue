<template>
  <h1>Bushido</h1>
  <div class="app-container">
    <Sidebar
        :navOptions="navOptions"
        :selected="selectedOption"
        @select="handleSelect"/>
    <div class="main-content">
      <router-view
          :key="selectedOption"
          :emojis="emojis"/>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted} from "vue";
import { useRouter } from "vue-router";
import Sidebar from "./components/Sidebar.vue"

const router = useRouter()
const emojis = ref([])
const navOptions = ref([
    {key: 'units', value: 'Units'}
])
const selectedOption = ref('units')

onMounted(async() => {
  const category_res = await fetch('/api/get-categories')
  const newOptions = await category_res.json()
  navOptions.value.push(...newOptions)
  const emoji_res = await fetch('/api/get-emojis')
  emojis.value = await emoji_res.json()
})

function handleSelect(key) {
  selectedOption.value = key
  router.push(`/${key}`)
}
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
