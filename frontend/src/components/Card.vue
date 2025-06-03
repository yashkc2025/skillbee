<script setup lang="ts">
</script>

<template>
  <div class="card">
    <slot></slot>
  </div>
</template>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  border: 1px solid #e6e6e6;
  border-radius: var(--border-radius);
  /* Testin only */
  width: 400px;
}
</style>
