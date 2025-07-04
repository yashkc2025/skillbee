<script setup lang="ts">
import { ref, reactive } from 'vue'
import CardV2 from '@/components/CardV2.vue'
import InputComponent from '@/components/InputComponent.vue'
import AdminAppLayout from '@/layouts/AdminAppLayout.vue'
import SelectComponent from '@/components/SelectComponent.vue'

// Metadata Fields
const lesson = ref("")
const image = ref("")
const title = ref("")
const description = ref("")
const difficulty = ref("")
const point = ref()

// Dummy lesson list (replace with actual data or API call)
const lessonDetails = ref([
  { label: 'Lesson 1', value: 'lesson-1' },
  { label: 'Lesson 2', value: 'lesson-2' }
])

// Quiz Form State
const questions = reactive<Array<{
  question: string
  options: Array<{ text: string; isCorrect: boolean }>
}>>([])

function addQuestion() {
  questions.push({
    question: '',
    options: [{ text: '', isCorrect: true }]
  })
}

function addOption(qIndex: number) {
  questions[qIndex].options.push({ text: '', isCorrect: false })
}

function removeOption(qIndex: number, oIndex: number) {
  const opts = questions[qIndex].options
  const removed = opts[oIndex]
  opts.splice(oIndex, 1)
  if (removed.isCorrect && opts.length > 0) {
    opts[0].isCorrect = true
  }
}

function markCorrect(qIndex: number, oIndex: number) {
  questions[qIndex].options.forEach((opt, i) => {
    opt.isCorrect = i === oIndex
  })
}

// Final payload preparation (on submit)
function createActivity() {
  const payload = {
    title: title.value,
    image: image.value,
    description: description.value,
    difficulty: difficulty.value,
    point: point.value,
    lessonId: lesson.value,
    questions: questions
  }

  console.log("Submitting Activity:", payload)

}
</script>

<template>
  <AdminAppLayout>
    <div class="outer">
      <p class="intro">
        <span class="darken">New Quiz</span>
      </p>

      <!-- Metadata -->
      <CardV2 label-title="Metadata" label-image="bi bi-book">
        <template #content class="form">
          <div class="form">
            <InputComponent icon="bi bi-journal" name="title" placeholder="Title" v-model="title" />
            <InputComponent icon="bi bi-image" name="image" placeholder="Image" v-model="image" field-type="file" />
            <InputComponent icon="bi bi-body-text" name="description" placeholder="Description" v-model="description"
              input-type="TextArea" />
          </div>
        </template>
      </CardV2>

      <!-- Scoring -->
      <CardV2 label-title="Scoring" label-image="bi bi-arrow-up">
        <template #content class="form">
          <div class="form">
            <InputComponent icon="bi bi-journal" name="difficulty" placeholder="Difficulty" v-model="difficulty" />
            <InputComponent icon="bi bi-arrow-up" name="point" placeholder="Points" v-model="point"
              field-type="number" />
          </div>
        </template>
      </CardV2>

      <!-- Lesson -->
      <CardV2 label-title="Lesson" label-image="bi bi-book">
        <template #content class="form">
          <div class="form">
            <SelectComponent v-model="lesson" name="lesson" icon="bi bi-book" placeholder="Select a Lesson"
              :options="lessonDetails" />
          </div>
        </template>
      </CardV2>

      <!-- QUIZ BUILDER -->
      <CardV2 label-title="Quiz Builder" label-image="bi bi-question-circle">
        <template #content class="form">
          <div class="form">
            <div v-for="(questionBlock, qIndex) in questions" :key="qIndex" class="question-block">
              <InputComponent icon="bi bi-question-circle" :name="`question-${qIndex}`" placeholder="Enter question"
                v-model="questionBlock.question" />

              <div v-for="(option, oIndex) in questionBlock.options" :key="oIndex" class="option-item">
                <div style="display: flex; align-items: center; gap: 8px;">
                  <input type="radio" :name="'correct-option-' + qIndex" :checked="option.isCorrect"
                    @change="markCorrect(qIndex, oIndex)" />
                  <InputComponent icon="bi " :name="`option-${qIndex}-${oIndex}`" placeholder="Enter option"
                    v-model="option.text" />
                  <button type="button" class="button-admin minimal-button" @click="removeOption(qIndex, oIndex)"
                    v-if="questionBlock.options.length > 1">Remove</button>
                </div>
              </div>

              <button type="button" class="button-admin" @click="addOption(qIndex)">Add Option</button>
              <hr />
            </div>

            <button type="button" class="button-admin" @click="addQuestion">Add Question</button>
          </div>
        </template>
      </CardV2>

      <!-- Submit Button -->
      <div style="display: flex; justify-content: flex-end;">
        <button type="button" class="button-admin" @click="createActivity">Create Activity</button>
      </div>
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
  gap: var(--size-xs);
}

.outer {
  display: flex;
  flex-direction: column;
  gap: var(--size-sm);
}

.question-block {
  background: #f9f9f9;
  border: 1px dashed var(--border-color-light);
  padding: 10px;
  border-radius: 6px;
}

.option-item {
  margin-left: 16px;
  margin-bottom: 5px;
}

.minimal-button {
  padding: 2px 6px;
  width: auto;
  min-width: 0;
  flex: 0 0 auto;
  white-space: nowrap;
}
</style>
