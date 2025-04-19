<template>
  <div id="app">
    <button @click="goToUnits">Units</button>
    <router-view />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const goToUnits = () => {
  router.push('/units')
}
</script>

<style scoped>

</style>
