<template>
  <div class="sidebar">
    <h3>Navigation</h3>
    <form class="category-options">
      <label v-for="(category, idx) in categories" :key="idx">
        <input
          type="radio"
          :value="category.value"
          v-model="selected"
        />
        {{ category.value }}
      </label>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps(['categories'])
const selected = ref('home')
</script>

<style scoped>
.sidebar {
  width: 220px;
  flex-shrink: 0;
  background-color: #1f1f1f;
  color: white;
  padding: 1rem;
  box-sizing: border-box;
  border-right: 1px solid #444;
  text-align: left;
}
.category-options {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 1rem;
}

.category-options input[type="radio"] {
  margin-right: 0.5rem;
}
</style>
