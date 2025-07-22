<script setup lang="ts">
const props = defineProps<{
  title?: string;
  direction: "row" | "column";
  isFitToContent: boolean;
}>();

console.log(props.isFitToContent);
</script>

<template>
  <div>
    <h3 class="card-title">{{ props.title }}</h3>
    <div class="card box-shadow" :style="{
      width: isFitToContent ? 'fit-content' : '100%',
      flexDirection: props.direction ? props.direction : 'column',
    }">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.card {
  display: flex;
  /* border: 1px solid var(--color-border); */
  border-radius: var(--border-radius);
  background-color: #fffde7;
  width: fit-content;
  background: #fffde7;
}

.card-title {
  font-family: "VAGRoundedNext";
  margin-bottom: var(--size-xs);
  font-weight: 600;
}
</style>
