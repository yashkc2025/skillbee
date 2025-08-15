<template>
  <button :class="['btn', type]" :disabled="disabled" @click.stop="$emit('click')">
    <slot />
  </button>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from "vue";

const props = defineProps<{
  type: "primary" | "secondary" | "tertiary" | "quaternary";
  disabled?: boolean;
}>();

defineEmits(["click"]);
</script>

<style scoped>
.btn {
  /* font-family: 'VAGRoundedNext'; */
  font-size: var(--font-md);
  padding: 10px 15px;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: bold;
  transition: background 0.4s, color 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.btn.primary {
  background: #ffd600;
  color: #4a148c;
}

.btn.primary:hover {
  background: #fff176;
}

.btn.secondary {
  background: #fff;
  color: #00796b;
  border: 2px solid #b2dfdb;
}

.btn.secondary:hover {
  background: #b2dfdb;
  color: #004d40;
}

.btn.tertiary {
  background: #ff80ab;
  color: #fff;
}

.btn.tertiary:hover {
  background: #ffb2dd;
  color: #ad1457;
}

.btn.quaternary {
  background: #007bff;
  color: #fff;
}
</style>
