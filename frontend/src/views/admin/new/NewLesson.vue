<script setup lang="ts">
import CardV2 from '@/components/CardV2.vue';
import InputComponent from '@/components/InputComponent.vue';
import AdminAppLayout from '@/layouts/AdminAppLayout.vue';
import SelectComponent from "@/components/SelectComponent.vue"
import { ref } from 'vue';

const title = ref("")
const content = ref("")
const image = ref("")
const description = ref("")
const badge_id = ref()
const curriculum_id = ref()

const curriculumDetails = [
  { label: "Critical Thinking", value: "c-t" },
  { label: "Communication Skills", value: 'c-s' },
  { label: "Time Management", value: 't-m' },
  { label: "Extracurricular Activities", value: 'e-a' },
  { label: "Financial Literacy", value: 'f-l' },
]

const badgeDetails = [
  {
    label: 'Quick Thinker', value: 'quick-thinker'
  },
  {
    label: 'Math Magician', value: 'math-magician'
  }
]
</script>

<template>
  <AdminAppLayout>
    <div class="outer">
      <p class="intro">
        <span class="darken">New Lesson</span>
      </p>
      <CardV2 label-title="Metadata" label-image="bi bi-book">
        <template #content class="form">
          <div class="form">
            <InputComponent icon="bi bi-journal" name="title" placeholder="Title" v-model="title" />
            <InputComponent icon="bi bi-book" name="content" placeholder="Content" v-model="content"
              input-type="TextArea" />
            <InputComponent icon="bi bi-body-text" name="description" placeholder="Description" v-model="description" />
            <InputComponent icon="bi bi-image" name="image" placeholder="Image" v-model="image" field-type="file" />
          </div>
        </template>
      </CardV2>
      <CardV2 label-title="Curriculum" label-image="bi bi-collection">
        <template #content class="form">
          <div class="form">
            <SelectComponent v-model="curriculum_id" name="curriculum" icon="bi bi-collection"
              placeholder="Select a curriculum" :options="curriculumDetails" />
          </div>
        </template>
      </CardV2>
      <CardV2 label-title="Badge" label-image="bi bi-stars">
        <template #content class="form">
          <div class="form">
            <SelectComponent v-model="badge_id" name="badge" icon="bi bi-stars" placeholder="Select a Badge"
              :options="badgeDetails" />
            <button type="button" class="button-admin">Create</button>
          </div>
        </template>
      </CardV2>
    </div>
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
