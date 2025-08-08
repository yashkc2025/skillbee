<script setup lang="ts">
const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();

const props = withDefaults(
  defineProps<{
    modelValue: string;
    name: string;
    placeholder: string;
    icon: string;
    inputType?: "TextArea" | "Input";
    fieldType?:
      | "url"
      | "tel"
      | "text"
      | "number"
      | "email"
      | "password"
      | "file"
      | "datetime-local"
      | "date";
    required?: boolean;
  }>(),
  {
    inputType: "Input",
    fieldType: "text",
    required: false,
  }
);

// function onInput(event: Event) {
//   const target = event.target as HTMLInputElement | HTMLTextAreaElement;
//   emit('update:modelValue', target.value);
// }

function onInput(event: Event) {
  const target = event.target as HTMLInputElement | HTMLTextAreaElement;

  // Handle file input manually
  if (props.fieldType === "file") {
    const file = (target as HTMLInputElement).files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      emit("update:modelValue", reader.result as string); // Emit base64 string
    };
    reader.readAsDataURL(file);
  } else {
    emit("update:modelValue", target.value);
  }
}
</script>

<template>
  <div class="input-wrapper">
    <i :class="icon"></i>
    <input
      v-if="inputType !== 'TextArea'"
      :placeholder="placeholder"
      :name="name"
      :type="fieldType"
      :value="modelValue"
      @input="onInput"
      :required
    />
    <textarea
      v-if="inputType === 'TextArea'"
      :placeholder="placeholder"
      :name="name"
      @input="onInput"
      :value="modelValue"
      :required
    />
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
  font-family: "DMSans";
  transition: border-color 0.3s ease;
}

.styled-input:focus {
  border-color: var(--color-border);
}
</style>
