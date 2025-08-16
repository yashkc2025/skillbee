<script setup lang="ts">
import CardV2 from "@/components/CardV2.vue";
import InputComponent from "@/components/InputComponent.vue";
import AdminAppLayout from "@/layouts/AdminAppLayout.vue";
import SelectComponent from "@/components/SelectComponent.vue";
import { ref } from "vue";
import { onMounted } from "vue";
import { fetchData, postData } from "@/fx/api";
import { getBackendURL, type OptionsType } from "@/fx/utils";

const title = ref("");
const content = ref("");
const image = ref("");
const description = ref("");
const curriculum_id = ref("");
const curriculumSelectRef = ref<InstanceType<typeof SelectComponent> | null>(null);
const links = ref("")

const curriculumDetails = ref<OptionsType[]>([]);

onMounted(async () => {
  const curr = await fetchData(getBackendURL("skills"));
  curriculumDetails.value = curr.map((c) => ({
    label: c.name,
    value: c.id,
  }));
});

async function createLesson() {
  await postData(getBackendURL("admin/lesson"), {
  title: title.value,
  content: {
    text: content.value,
    url: links.value.trim() === ""
      ? {}
      : links.value
          .split(",")
          .map(link => link.trim())
          .reduce((acc, link, index) => {
            acc[index] = link;
            return acc;
          }, {})
  },
  image: image.value,
  description: description.value,
  skill_id: curriculum_id.value
}, "/admin/lessons")}
</script>

<template>
  <AdminAppLayout>
    <div class="outer">
      <p class="intro">
        <span class="darken">New Lesson</span>
      </p>
      <form class="form" @submit.prevent="createLesson">
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
                icon="bi bi-book"
                name="content"
                placeholder="Content"
                v-model="content"
                input-type="TextArea"
                :required="true"
              />
              <InputComponent
                icon="bi bi-link"
                name="links"
                placeholder="Links Comma Seperated"
                v-model="links"
                input-type="TextArea"
              />
              <InputComponent
                icon="bi bi-body-text"
                name="description"
                placeholder="Description"
                v-model="description"
                :required="true"
              />
              <InputComponent
                icon="bi bi-image"
                name="image"
                placeholder="Image"
                v-model="image"
                field-type="file"
                :required="true"
              />
            </div>
          </template>
        </CardV2>
        <CardV2 label-title="Curriculum" label-image="bi bi-collection">
          <template #content class="form">
            <div class="form">
              <SelectComponent
                ref="curriculumSelectRef"
                v-model="curriculum_id"
                name="curriculum"
                icon="bi bi-collection"
                placeholder="Select a curriculum"
                :options="curriculumDetails"
              />
              <button type="submit" class="button-admin">Create</button>
            </div>
          </template>
        </CardV2>
      </form>
      <!-- <CardV2 label-title="Badge" label-image="bi bi-stars">
        <template #content class="form">
          <div class="form">
            <SelectComponent
              v-model="badge_id"
              name="badge"
              icon="bi bi-stars"
              placeholder="Select a Badge"
              :options="badgeDetails"
            />
          </div>
        </template>
      </CardV2> -->
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
</style>
