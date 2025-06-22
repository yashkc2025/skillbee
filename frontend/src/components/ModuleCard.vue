<template>
  <div class="module-card">
    <img :src="image" :alt="name" class="module-image" />
    <h2 class="module-name">{{ name }}</h2>
    <p class="module-description">{{ description }}</p>
    <slot></slot>
    <div class="module-buttons">
      <AppButton type="primary" class="primary" @click="$emit('primary')">{{
        primaryLabel
        }}</AppButton>
      <AppButton type="secondary" class="secondary" @click="$emit('secondary')">{{ secondaryLabel }}
      </AppButton>
    </div>
    <AppButton v-if="tertiaryLabel" type="tertiary" :class="['tertiary', { 'disabled-tertiary': disabledTertiary }]"
      :disabled="disabledTertiary" @click="$emit('tertiary')">
      {{ tertiaryLabel }}
    </AppButton>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from "vue";
import AppButton from "./AppButton.vue";

const props = defineProps<{
  image: string;
  name: string;
  description: string;
  primaryLabel?: string;
  secondaryLabel?: string;
  tertiaryLabel?: string;
  disabledTertiary?: boolean;
}>();

defineEmits(["primary", "secondary", "tertiary"]);
</script>

<style scoped>
.module-card {
  background: linear-gradient(135deg, #f9f6ff 0%, #e0f7fa 100%);
  border-radius: var(--border-radius);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 2px 0 10px 0;
  max-width: 350px;
  margin: 20px auto;
  transition: box-shadow 0.3s;
}

.module-card:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
  cursor: pointer;
}

.module-image {
  width: 100%;
  border-radius: var(--border-radius) var(--border-radius) 0 0;
  object-fit: cover;
  border: 4px solid #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: #fff;
}

.module-name {
  font-family: "VAGRoundedNext";
  font-size: var(--font-lg);
  color: #4a148c;
  margin: 10px 0 10px 0;
  padding: 0 15px;
  letter-spacing: 1px;
}

.module-description {
  font-size: var(--font-md);
  color: #00796b;
  margin-bottom: 10px;
  padding: 0 15px;
  min-height: 40px;
}

.module-buttons {
  display: flex;
  gap: 5%;
  justify-content: center;
}

.primary {
  width: 44%;
}

.secondary {
  width: 44%;
}

.tertiary {
  display: block;
  width: 95%;
  margin: 18px auto 0 auto;
}

.tertiary.disabled-tertiary {
  background: #ffb2dd;
  color: #ad1457;
  cursor: not-allowed;
}
</style>
