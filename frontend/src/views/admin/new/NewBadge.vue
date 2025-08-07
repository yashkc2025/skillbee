<script setup lang="ts">
import CardV2 from "@/components/CardV2.vue";
import InputComponent from "@/components/InputComponent.vue";
import { postData } from "@/fx/api";
import { getBackendURL } from "@/fx/utils";
import AdminAppLayout from "@/layouts/AdminAppLayout.vue";
import { ref } from "vue";

const title = ref("");
const points = ref();
const image = ref();
const description = ref("");

async function newBadge() {
  if (!image.value) {
    console.error("Image not uploaded");
    return;
  }

  postData(getBackendURL("admin/badge"), {
    title: title.value,
    image: image.value,
    points: points.value,
    description: description.value,
  });
}
</script>

<template>
  <AdminAppLayout>
    <p class="intro">
      <span class="darken">New Badge</span>
    </p>
    <CardV2 label-title="Metadata" label-image="bi bi-book">
      <template #content class="form">
        <form class="form" @submit.prevent="newBadge">
          <InputComponent
            icon="bi bi-journal"
            name="title"
            placeholder="Title"
            v-model="title"
            :required="true"
          />
          <InputComponent
            icon="bi bi-justify"
            name="description"
            placeholder="Description"
            v-model="description"
            :required="true"
          />
          <InputComponent
            icon="bi bi-arrow-up"
            name="points"
            placeholder="Unlocked at Points"
            v-model="points"
            :required="true"
          />
          <InputComponent
            icon="bi bi-image"
            name="image"
            placeholder="Image"
            field-type="file"
            v-model="image"
            :required="true"
          />
          <button type="submit" class="button-admin">Create</button>
        </form>
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
  gap: var(--size-xs);
}

.outer {
  display: flex;
  flex-direction: column;
  gap: var(--size-sm);
}
</style>
