<script setup lang="tsx">
import CardV2 from "@/components/CardV2.vue";
import InputComponent from "@/components/InputComponent.vue";
import TableComponent from "@/components/TableComponent.vue";
import { useRouter } from "vue-router";
import sitemap from "@/router/sitemap.json";
import AdminAppLayout from "@/layouts/AdminAppLayout.vue";
import { ref } from "vue";
import { onMounted } from "vue";

type LessonsType = {
  id: number;
  title: string;
  curriculum: string;
}[];

const lessons = ref<LessonsType>([]);
const searchText = ref("");

const lessonLabels = ["ID", "Title", "Curriculum", "Activities", "Quiz", "Edit"];

const router = useRouter();

onMounted(async () => {
  const data = [
    {
      id: 1,
      title: "Let's make a ship!",
      curriculum: "Extracurricular Activities",
    },
    {
      id: 2,
      title: "Debate Club: Argue like a Pro",
      curriculum: "Communication Skills",
    },
    {
      id: 3,
      title: "Budget Your Pocket Money",
      curriculum: "Financial Literacy",
    },
    {
      id: 4,
      title: "Solve the Mystery! Logic Puzzle Day",
      curriculum: "Critical Thinking",
    },
    {
      id: 5,
      title: "Plan a Perfect Study Week",
      curriculum: "Time Management",
    },
    {
      id: 6,
      title: "Public Speaking Bootcamp",
      curriculum: "Communication Skills",
    },
    {
      id: 7,
      title: "Escape Room Challenge",
      curriculum: "Critical Thinking",
    },
    {
      id: 8,
      title: "Start Your Own Club",
      curriculum: "Extracurricular Activities",
    },
    {
      id: 9,
      title: "Track Your Spending for a Month",
      curriculum: "Financial Literacy",
    },
    {
      id: 10,
      title: "Beat the Clock: Productivity Games",
      curriculum: "Time Management",
    },
  ];

  lessons.value = data;
});
function addLesson() {
  router.push(sitemap.admin.new.lesson);
}

function navToLink(name: string, id: number) {
  router.push({ name, params: { id } });
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
      ...p,
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
      edit: <i class="bi bi-pen pointer" onClick={() => addLesson()}></i>,
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
