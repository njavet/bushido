<template>
  <div class="app-container">
    <Sidebar/>


  </div>
  <div id="app">
    <aside class="sidebar">
      <h2>Dashboards</h2>
      <button><dumbbell-icon /> Weight Lifting</button>
      <button><calendar-days-icon /> Calendar</button>
    </aside>

    <!-- Main content -->
    <main class="main-content">
      <h1>Bushido</h1>
      <img src="/logo.png" alt="Bushido Logo" class="logo" />

      <div class="unit-list">
        <div v-for="(unit, idx) in units" :key="idx" class="unit-item">
          <div class="unit-date">{{ unit.date }}</div>
          <div>{{ unit.text }}</div>
        </div>
      </div>

      <div class="input-area">
        <input
          v-model="input"
          @keydown.enter="addUnit"
          placeholder="New training unit..."
        />
        <button @click="addUnit">Add</button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import Sidebar from "./components/Sidebar.vue"

const router = useRouter()
const goToUnits = () => {
  router.push('/units')
}
</script>

<style scoped>

</style>
