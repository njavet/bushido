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

    <main class="chat">
      <div class="history">
        <section v-for="(entries, date) in unitsByDay" :key="date" class="panel">
          <h3><span class="text-cyan-200">{{ date }}</span></h3>
          <ul>
            <li v-for="(entry, i) in entries" :key="i">
              <span class="text-cyan-100">{{ entry[0] }} {{ entry[1] }}</span>
            </li>
          </ul>
        </section>
        <section v-if="show.day" class="panel">
          <h3>Today</h3>
          <ul>
            <li v-for="(entry, i) in todayEntries" :key="i">{{ entry }}</li>
          </ul>
        </section>

        <section v-if="show.week" class="panel">
          <h3>This Week</h3>
          <ul>
            <li v-for="(entry, i) in weekEntries" :key="i">{{ entry }}</li>
          </ul>
        </section>
      </div>

      <div class="input">
        <span class="prompt">user@bushido:~$</span>
        <input
          type="text"
          v-model="inputValue"
          ref="terminalInput"
          @keydown.enter="handleEnter"
          placeholder=":emoji command..."
        />
      </div>
    </main>
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
