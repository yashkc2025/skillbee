<script setup lang="ts">
const props = withDefaults(defineProps<{
  name: string;
  placeholder: string;
  icon: string;
  inputType?: 'TextArea' | 'Input';
}>(), {
  inputType: 'Input',
});
</script>

<template>
  <div class="input-wrapper">
    <i :class="icon"></i>
    <input v-if="inputType !== 'TextArea'" :placeholder="placeholder" :name="name" />
    <textarea v-if="inputType === 'TextArea'" :placeholder="placeholder" :name="name" />
  </div>
</template>

<style scoped>
.input-wrapper {
  position: relative;
  width: 100%;
  /* max-width: 300px; */
  /* background-color: red; */
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

input,
textarea {
  width: 100%;
  padding: 4px;
  padding-left: 30px;
  /* left padding to make space for icon */
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  outline: none;
  font-size: var(--font-sm);
  font-family: 'DMSans';
  transition: border-color 0.3s ease;
}

.styled-input:focus {
  border-color: var(--color-border);
}
</style>
