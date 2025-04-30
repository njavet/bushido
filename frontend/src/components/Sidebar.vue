<template>
  <div class="sidebar">
    <h3>Navigation</h3>
    <form class="nav-options">
      <label v-for="(option, idx) in props.navOptions" :key="idx">
        <input
          type="radio"
          :value="option.key"
          v-model="selected"
          @change="selectOption(option.key)"
        />
        {{ option.value }}
      </label>
    </form>
  </div>
</template>

<script setup>
const props = defineProps(
    ['navOptions']
)
const emit = defineEmits(['select'])
const selected = defineModel('selected')

function selectOption(key) {
  emit('select', key)
}

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
.nav-options {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 1rem;
}

.nav-options input[type="radio"] {
  margin-right: 0.5rem;
}
</style>
