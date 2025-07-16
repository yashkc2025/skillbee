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
      <div v-for="(stat, index) in stats" :key="index" class="grid-card kid-grid-card">
        <p class="label kid-label">{{ stat.label }}</p>
        <p class="value kid-value">{{ stat.answer || stat.count || "-" }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
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
  border: 2px solid #ffd54f;
  gap: 10px;
  padding: 10px 0;
  justify-content: center;
}

.grid-card.kid-grid-card {
  min-height: 90px;
  min-width: 90px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s, box-shadow 0.15s;
}

.kid-label {
  font-size: calc(var(--font-md)/1.1);
  color: #4a148c;
  font-family: 'Delius';
  margin-bottom: 6px;
  text-align: center;
  font-weight: 600;
}

.kid-value {
  font-size: var(--font-lg);
  color: #43a047;
  font-family: "VAGRoundedNext";
  font-weight: bold;
  text-align: center;
  margin-top: 2px;
  letter-spacing: 1px;
}

@media (max-width: 700px) {
  .grid {
    grid-auto-flow: row;
    grid-template-rows: none;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    padding: 8px 0;
  }

  .grid-card.kid-grid-card {
    min-width: 80px;
    max-width: 100px;
    padding: 14px 6px;
  }
}
</style>
