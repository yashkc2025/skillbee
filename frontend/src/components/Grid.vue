<script setup lang="ts">
const props = defineProps<{
  title?: string;
  stats: {
    label: string;
    answer?: string;
    count?: string;
  }[];
}>();
</script>

<template>
  <div class="grid-parent">
    <h3 class="grid-title" v-if="props.title">{{ props.title }}</h3>
    <div class="grid box-shadow">
      <div v-for="(stat, index) in stats" :key="index" class="grid-card">
        <p class="label">{{ stat.label }}</p>
        <p class="value">{{ stat.answer || stat.count || "-" }}</p>
      </div>
    </div>
  </div>
</template>

<style>
.grid-title {
  font-family: "VAGRoundedNext";
  margin-bottom: var(--size-xs);
  font-weight: 600;
}

.grid {
  display: grid;
  grid-auto-flow: column;
  grid-template-rows: repeat(2, auto);
  border-radius: var(--border-radius);
  background-color: var(--color-light);
  border: 1px solid var(--color-border);
}

.grid-card {
  padding: var(--size-sm) var(--size-md);
  border-radius: var(--border-radius);
  background-color: var(--color-light);
  min-height: 90px;
  max-width: 80px;
}

.label {
  font-size: var(--font-sm);
}

.value {
  font-size: var(--font-lg);
  font-family: "VAGRoundedNext";
}
</style>
