<script setup lang="tsx">
import CardV2 from "@/components/CardV2.vue";
import InputComponent from "@/components/InputComponent.vue";
import TableComponent from "@/components/TableComponent.vue";
import { useRouter } from "vue-router";
import sitemap from "@/router/sitemap.json";
import AdminAppLayout from "@/layouts/AdminAppLayout.vue";
import { ref } from "vue";
import { onMounted } from "vue";
import { deleteData, fetchData } from "@/fx/api";
import { getBackendURL } from "@/fx/utils";

type LessonsType = {
  id: number;
  title: string;
  curriculum: string;
}[];

const lessons = ref<LessonsType>([]);
const searchText = ref("");

const lessonLabels = [
  "ID",
  "Title",
  "Curriculum",
  "Activities",
  "Quiz",
  "Edit",
  "Delete",
];

const router = useRouter();

onMounted(async () => {
  const data = await fetchData(getBackendURL("lessons"));

  lessons.value = data;
});
function addLesson() {
  router.push(sitemap.admin.new.lesson);
}

function navToLink(name: string, id: number) {
  router.push({ name, params: { id } });
}

async function deleteItem(id) {
  await deleteData(getBackendURL("/admin/lesson"), { id });
}

function tableEntries() {
  const lowerSearch = searchText.value.toLowerCase().trim();

  return lessons.value
    .filter((lesson) =>
      [lesson.title, lesson.curriculum].some((field) =>
        field.toLowerCase().includes(lowerSearch)
      )
    )
    .map((p) => ({
      id: p.id,
      title: p.title,
      curriculum: p.curriculum,
      activities: (
        <i
          class="bi bi-patch-plus pointer"
          onClick={() =>
            router.push({
              path: sitemap.admin.curriculum.activities,
              query: { lesson_id: p.id },
            })
          }
        ></i>
      ),
      quiz: (
        <i
          class="bi bi-patch-plus pointer"
          onClick={() =>
            router.push({
              path: sitemap.admin.curriculum.quiz,
              query: { lesson_id: p.id },
            })
          }
        ></i>
      ),
      edit: (
        <i class="bi bi-pen pointer" onClick={() => navToLink("edit_lesson", p.id)}></i>
      ),
      delete: <i class="bi bi-trash3 pointer" onClick={() => deleteItem(p.id)}></i>,
    }));
}
</script>

<template>
  <AdminAppLayout>
    <p class="intro">
      <span class="darken">Manage Lessons</span>
    </p>
    <CardV2 label-title="Lessons" label-image="bi bi-book">
      <template #top-content>
        <div class="table-header">
          <InputComponent
            icon="bi bi-search"
            name="search"
            placeholder="Search for a lesson"
            v-model="searchText"
          />
          <i class="bi bi-plus-lg" @click="addLesson"></i>
        </div>
      </template>
      <template #content>
        <TableComponent :header="lessonLabels" :rows="tableEntries()" />
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
