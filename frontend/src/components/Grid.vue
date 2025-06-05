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
  <div>
    <h3 class="grid-title">{{ props.title }}</h3>
    <div class="grid">
      <div v-for="(stat, index) in stats" :key="index" class="grid-card">
        <p class="label">{{ stat.label }}</p>
        <p class="value">{{ stat.answer || stat.count || "-" }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.grid-title {
  font-family: "VAGRoundedNext", sans-serif;
  margin-bottom: var(--size-xs);
  font-weight: 600;
  font-size: 1.25rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--size-sm);
}

.grid-card {
  background-color: var(--color-light);
  padding: var(--size-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  transition: box-shadow 0.2s ease, transform 0.2s ease;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
}

.grid-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.label {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.value {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--color-text-dark);
}
</style>
