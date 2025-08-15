<script setup lang="ts">
const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();

const props = withDefaults(
  defineProps<{
    required: boolean;
    modelValue: string;
    name: string;
    placeholder: string;
    icon: string;
    options: { label: string; value: string | number }[];
  }>(),
  {
    required: false,
  }
);
</script>

<template>
  <div class="input-wrapper">
    <i :class="icon"></i>
    <select
      :name="name"
      :value="modelValue"
      :required
      @change="(e) => emit('update:modelValue', (e.target as HTMLSelectElement).value)"
    >
      <option disabled value="">{{ placeholder }}</option>
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
  </div>
</template>

<style scoped>
.input-wrapper {
  position: relative;
  width: 100%;
}

i {
  position: absolute;
  top: 50%;
  left: 8px;
  transform: translateY(-50%);
  color: #888;
  font-size: 13px;
  pointer-events: none;
}

select {
  width: 100%;
  padding: 4px;
  padding-left: 30px;
  /* space for icon */
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  outline: none;
  font-size: var(--font-sm);
  font-family: "DMSans";
  appearance: none;
  /* Remove native arrow in some browsers */
  background-color: white;
  transition: border-color 0.3s ease;
}
</style>
