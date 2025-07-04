<script setup lang="ts">
import CardV2 from '@/components/CardV2.vue';
import InputComponent from '@/components/InputComponent.vue';
import AdminAppLayout from '@/layouts/AdminAppLayout.vue';
import SelectComponent from "@/components/SelectComponent.vue"
import { ref } from 'vue';

const lesson = ref("")
const image = ref("")
const title = ref("")
const description = ref("")
const instructions = ref("")
const difficulty = ref("")
const point = ref()

const curriculumDetails = [
  { label: "Critical Thinking", value: "c-t" },
  { label: "Communication Skills", value: 'c-s' },
  { label: "Time Management", value: 't-m' },
  { label: "Extracurricular Activities", value: 'e-a' },
  { label: "Financial Literacy", value: 'f-l' },
]

const lessonDetails = [
  {
    label: 'Build a ship', value: 'build-ship'
  },
  {
    label: 'How to swim!', value: 'how-to-swim'
  }
]

</script>

<template>
  <AdminAppLayout>
    <div class="outer">
      <p class="intro">
        <span class="darken">New Activity</span>
      </p>
      <CardV2 label-title="Metadata" label-image="bi bi-book">
        <template #content class="form">
          <div class="form">
            <InputComponent icon="bi bi-journal" name="title" placeholder="Title" v-model="title" />
            <InputComponent icon="bi bi-image" name="image" placeholder="Image" v-model="image" field-type="file" />
            <InputComponent icon="bi bi-book" name="instructions" placeholder="Instructions" v-model="instructions"
              input-type="TextArea" />
            <InputComponent icon="bi bi-body-text" name="description" placeholder="Description" v-model="description"
              input-type="TextArea" />
          </div>
        </template>
      </CardV2>
      <CardV2 label-title="Scoring" label-image="bi bi-arrow-up">
        <template #content class="form">
          <div class="form">
            <InputComponent icon="bi bi-journal" name="difficulty" placeholder="Difficulty" v-model="difficulty" />
            <InputComponent icon="bi bi-arrow-up" name="point" placeholder="Points" v-model="point"
              field-type="number" />
          </div>
        </template>
      </CardV2>
      <CardV2 label-title="Lesson" label-image="bi bi-book">
        <template #content class="form">
          <div class="form">
            <SelectComponent v-model="lesson" name="badge" icon="bi bi-book" placeholder="Select a Lesson"
              :options="lessonDetails" />
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
