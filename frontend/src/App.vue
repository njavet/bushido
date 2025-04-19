<template>
  <div class="layout">
    <aside class="sidebar">
      <h2 class="section-title">Bushido</h2>
      <nav>
        <ul>
          <li><button @click="togglePanel('day')">Day View</button></li>
          <li><button @click="togglePanel('week')">Week View</button></li>
        </ul>
      </nav>
    </aside>
  </div>
</template>

<script setup>


</script>

<style scoped>
body, html, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

.layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.sidebar {
  width: 200px;
  background: #222;
  color: #fff;
  padding: 1rem;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
}

.sidebar .section-title {
  margin-bottom: 1rem;
}

</style>
