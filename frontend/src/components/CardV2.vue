<script setup lang="ts">
defineProps<{
  labelTitle?: string;
  labelImage: string;
}>();
</script>

<template>
  <div class="card box-shadow">
    <div class="header">
      <div class="label">
        <i :class="labelImage"></i>
        <p>{{ labelTitle }}</p>
      </div>
      <div class="header-content">
        <slot name="top-content"></slot>
      </div>
    </div>
    <div class="content">
      <slot name="content"></slot>
    </div>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.card {
  padding: var(--size-sm);
  border: 1px solid var(--color-border);
  background-color: var(--color-light);
  border-radius: var(--border-radius);
}

.label {
  display: flex;
  flex-direction: row;
  gap: var(--size-xs);
  align-items: center;
  /* font-family: "Inter"; */
}

.label>p {
  font-weight: 500;
}

.label>i {
  background-color: var(--color-border);
  padding: 1px 3px;
  border-radius: 5px;
  padding-top: 2px;
}

.content {
  margin-top: var(--size-sm);
}
</style>
