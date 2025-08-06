<script setup lang="ts">
const props = defineProps<{ isHeading?: boolean }>();
</script>

<template>
  <div :class="['card-item hover', { 'use-vag': props.isHeading }]">
    <slot></slot>
  </div>
</template>

<style scoped>
.card-item {
  padding: var(--size-sm) var(--size-md);
  background-color: var(--color-light);
  border: 1px solid var(--color-border);
}

.card-item:nth-child(1) {
  border-top-left-radius: var(--border-radius);
  border-top-right-radius: var(--border-radius);
}

.card-item:nth-last-child(1) {
  border-bottom-left-radius: var(--border-radius);
  border-bottom-right-radius: var(--border-radius);
}

.use-vag {
  font-family: "VAGRoundedNext";
}
</style>
