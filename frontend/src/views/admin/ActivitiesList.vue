<script setup lang="tsx">
import CardV2 from "@/components/CardV2.vue";
import InputComponent from "@/components/InputComponent.vue";
import TableComponent from "@/components/TableComponent.vue";
import { useRouter, useRoute } from "vue-router";
import sitemap from "@/router/sitemap.json";
import AdminAppLayout from "@/layouts/AdminAppLayout.vue";
import { onMounted } from "vue";
import { ref } from "vue";
import { deleteData, fetchData } from "@/fx/api";
import { getBackendURL } from "@/fx/utils";

type ActivitiesType = {
  id: number;
  title: string;
  lesson: string;
  curriculum: string;
}[];

const router = useRouter();
const activities = ref<ActivitiesType>([]);
const searchText = ref("");
const lesson_id = useRoute().query.lesson_id;

onMounted(async () => {
  const data = await fetchData(getBackendURL("activities"), {
    lesson_id: lesson_id,
  });

  activities.value = data;
});

const activitiesLabels = ["ID", "Title", "Lesson", "Curriculum", "Edit", "Delete"];

function addEntry() {
  router.push(sitemap.admin.new.activity);
}

function navToLink(name: string, id: number) {
  router.push({ name, params: { id } });
}

function tableEntries() {
  const lowerSearch = searchText.value.toLowerCase().trim();

  return activities.value
    .filter((activity) =>
      [activity.title, activity.lesson, activity.curriculum].some((field) =>
        field.toLowerCase().includes(lowerSearch)
      )
    )
    .map((p) => ({
      id: p.id,
      title: p.title,
      lesson: p.lesson,
      curriculum: p.curriculum,
      edit: (
        <i class="bi bi-pen pointer" onClick={() => navToLink("edit_activity", p.id)}></i>
      ),
      delete: <i class="bi bi-trash3 pointer" onClick={() => deleteItem(p.id)}></i>,
    }));
}

async function deleteItem(id) {
  await deleteData(getBackendURL("/admin/activity"), { id });
}
</script>

<template>
  <AdminAppLayout>
    <p class="intro">
      <span class="darken" v-if="lesson_id && activities[0]?.lesson"
        >Activities for : {{ activities[0].lesson }}</span
      >
      <span class="darken" v-else>Manage Activities</span>
    </p>
    <CardV2 label-title="Activities" label-image="bi bi-book">
      <template #top-content>
        <div class="table-header">
          <InputComponent
            icon="bi bi-search"
            name="search"
            placeholder="Search for an Activity"
            v-model="searchText"
          />
          <i class="bi bi-plus-lg" @click="addEntry"></i>
        </div>
      </template>
      <template #content>
        <TableComponent :header="activitiesLabels" :rows="tableEntries()" />
      </template>
    </CardV2>
  </AdminAppLayout>
</template>

<style scope>
.table-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--size-xs);
}

.table-header > i {
  font-size: var(--font-sm);
  font-weight: 500;
  cursor: pointer;
  font-size: 12px;
  /* background-color: var(--color-background); */
  border: 1px solid var(--color-border);
  padding: 5px 7px;
  border-radius: var(--border-radius);
}

.intro {
  margin-bottom: 20px;
}
</style>
