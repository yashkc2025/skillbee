<script setup lang="ts">
const props = defineProps({
  id: {
    type: Number,
    required: true,
  },
});
import CardV2 from "@/components/CardV2.vue";
import InputComponent from "@/components/InputComponent.vue";
import ParentAppLayout from "@/layouts/ParentAppLayout.vue";
import SelectComponent from "@/components/SelectComponent.vue";
import { ref } from "vue";
import { onMounted } from "vue";
import { fetchData, postData, updateData } from "@/fx/api";
import { getBackendURL, type OptionsType } from "@/fx/utils";

const childId = ref()
const lesson = ref("");
const image = ref("");
const title = ref("");
const description = ref("");
const instructions = ref("");
const difficulty = ref("");
const answerFormat = ref<"Text" | "Image" | "PDF" | "">("");
const children = ref()

export interface ActInterface {
  answer_format: string
  description: string
  difficulty: string
  id: number
  instructions: string
  lesson_id: number
  title: string
}
const afOptions = [
  {
    label: "PDF",
    value: "pdf",
  },
  {
    label: "Text",
    value: "text",
  },
  {
    label: "Image",
    value: "image",
  },
];

const lessons = ref<OptionsType[]>([]);
const actDetails = ref<ActInterface>()

onMounted(async () => {
  const lessonData = await fetchData(getBackendURL("lessons"))
  actDetails.value = await fetchData(getBackendURL(`admin/activity/${props.id}`))
  const childData = await fetchData(getBackendURL("children"));

  if (childData){
    children.value = childData.map((c) => ({
      label : c.name,
      value : c.id
    }))
  }
  if (actDetails.value){
    lesson.value = actDetails.value.lesson_id
    title.value = actDetails.value.title
    description.value = actDetails.value.description
    instructions.value = actDetails.value.instructions
    difficulty.value = actDetails.value.difficulty
    answerFormat.value = actDetails.value.answer_format
    childId.value = actDetails.value.child_id
  }
  lessons.value = lessonData.map((d) => ({ value: d.id, label: d.title }));
});

async function updateActivity() {
  const data = {
    id : props.id,
    title: title.value,
    image: image.value,
    instructions: instructions.value,
    description: description.value,
    difficulty: difficulty.value,
    lesson_id: lesson.value,
    answer_format : answerFormat.value,
    child_id : childId.value

  };
  if (image.value && image.value.trim() !== "") {
    data.image = image.value;
  }

  await updateData(getBackendURL("admin/activity"), data, '/parent/activity');
}
</script>

<template>
  <ParentAppLayout>
    <form class="outer" @submit.prevent="updateActivity">
      <p class="intro">
        <span class="darken">Update Activity</span>
      </p>
      <CardV2 label-title="Metadata" label-image="bi bi-book">
        <template #content class="form">
          <div class="form">
            <InputComponent
              icon="bi bi-journal"
              name="title"
              placeholder="Title"
              v-model="title"
              :required="true"
            />
            <InputComponent
              icon="bi bi-image"
              name="image"
              placeholder="Image"
              v-model="image"
              field-type="file"
            />
            <SelectComponent
              v-model="childId"
              name="child_id"
              icon="bi bi-emoji-smile"
              placeholder="Select a child"
              :options="children"
              :required="true"
            />
            <InputComponent
              icon="bi bi-book"
              name="instructions"
              placeholder="Instructions"
              v-model="instructions"
              input-type="TextArea"
              :required="true"
            />
            <InputComponent
              icon="bi bi-body-text"
              name="description"
              placeholder="Description"
              v-model="description"
              input-type="TextArea"
              :required="true"
            />
          </div>
        </template>
      </CardV2>
      <CardV2 label-title="Scoring" label-image="bi bi-arrow-up">
        <template #content class="form">
          <div class="form">
            <InputComponent
              icon="bi bi-journal"
              name="difficulty"
              placeholder="Difficulty"
              v-model="difficulty"
              :required="true"
            />
          </div>
        </template>
      </CardV2>
      <CardV2 label-title="Lesson" label-image="bi bi-book">
        <template #content class="form">
          <div class="form">
            <SelectComponent
              v-model="lesson"
              name="badge"
              icon="bi bi-book"
              placeholder="Select a Lesson"
              :options="lessons"
              :required="true"
            />
            <SelectComponent
              v-model="answerFormat"
              name="answerFormat"
              icon="bi bi-pen"
              placeholder="Answer Format"
              :options="afOptions"
              :required="true"
            />
            <button type="submit" class="button-admin">Create</button>
          </div>
        </template>
      </CardV2>
    </form>
  </ParentAppLayout>
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
</style>
