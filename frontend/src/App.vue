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
          :emojis="filterEmojis(selectedOption)"/>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Sidebar from "./components/Sidebar.vue"

const router = useRouter()
const md = ref([])
const emojis = ref([])
const navOptions = ref([
    {key: 'units', value: 'Units'}
])
const selectedOption = ref('units')

onMounted(async() => {
  const res = await fetch('/api/get-master-data')
  md.value = await res.json()
  const newOptions = Object.keys(md.value.categories)
      .map(cat => ({
        key: cat,
        value: cat.charAt(0).toUpperCase() + cat.slice(1)
  }))
  navOptions.value.push(...newOptions)
  emojis.value = Object.entries(md.value.categories)
      .flatMap(([_, pairs]) =>
          pairs.map(([emoji, unit_name]) => ({
            key: unit_name,
            value: emoji
      })))
})

function filterEmojis(category) {
  if (category === 'units') {
    return emojis.value
  } else {
    return md.value.categories[category].map(([emoji, unit_name]) => ({
      key: unit_name,
      value: emoji
    }))
  }
}

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
