<script setup lang="ts">
const props = defineProps<{ title?: string }>();
</script>

<template>
  <div>
    <h3 class="card-title">{{ props.title }}</h3>
    <div class="card box-shadow">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
}

.card-title {
  font-family: "VAGRoundedNext";
  margin-bottom: var(--size-xs);
  font-weight: 600;
}
</style>
