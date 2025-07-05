<script setup lang="ts">
import CardV2 from '@/components/CardV2.vue';
import InputComponent from '@/components/InputComponent.vue';
import AdminAppLayout from '@/layouts/AdminAppLayout.vue';
import { ref } from 'vue';

const title = ref("")
const image = ref("")
const points = ref()
</script>

<template>
  <AdminAppLayout>
    <p class="intro">
      <span class="darken">New Badge</span>
    </p>
    <CardV2 label-title="Metadata" label-image="bi bi-book">
      <template #content class="form">
        <div class="form">
          <InputComponent icon="bi bi-journal" name="title" placeholder="Title" v-model="title" />
          <InputComponent icon="bi bi-arrow-up" name="points" placeholder="Unlocked at Points" v-model="points" />
          <InputComponent icon="bi bi-image" name="image" placeholder="Image" v-model="image" field-type="file" />
          <button type="button" class="button-admin">Create</button>
        </div>
      </template>
    </CardV2>
  </AdminAppLayout>
</template>

<style scoped>
.intro {
  margin-bottom: 20px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: var(--size-xs)
}

.outer {
  display: flex;
  flex-direction: column;
  gap: var(--size-sm);
}
</style>
