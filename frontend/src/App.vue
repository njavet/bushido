<template>
  <h1>Bushido</h1>
  <div class="app-container">
    <Sidebar/>
    <div class="main-content">
      <Units />
    </div>
  </div>
</template>

<script setup>
import Sidebar from "./components/Sidebar.vue"
import Units from "./components/Units.vue";
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
