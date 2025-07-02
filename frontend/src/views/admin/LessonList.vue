<script setup lang="tsx">
const props = withDefaults(defineProps<{
  maxItems?: number;
  showExpand?: boolean;
}>(), {
  showExpand: false,
})

import CardV2 from "@/components/CardV2.vue";
import InputComponent from "@/components/InputComponent.vue";
import TableComponent from "@/components/TableComponent.vue";
import { useRouter } from "vue-router";
import sitemap from "@/router/sitemap.json"
import AdminAppLayout from "@/layouts/AdminAppLayout.vue";

const lessons = [
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
  }
];

const lessonLabels = ["ID", "Title", "Curriculum", "Activities", "Quiz", "Edit"];

const router = useRouter()

function expandTable() {
  router.push(sitemap.admin.user_management.children)
}

function navToLink(name: string, id: number) {
  router.push({ name, params: { id } })
}

function tableEntries() {
  lessons.forEach((p) => {
    // p.blocked = <span class="chip pointer">{p.blocked ? "Blocked" : "Active"}</span>
    p.activities = <i class="bi bi-patch-plus pointer" onClick={() => navToLink(sitemap.admin.curriculum.activities, p.id)}></i>
    p.quiz = <i class="bi bi-patch-plus pointer" onClick={() => navToLink(sitemap.admin.curriculum.quiz, p.id)}> </i>
    p.edit = <i class="bi bi-pen pointer" onClick={() => navToLink(sitemap.admin.curriculum.quiz, p.id)}> </i>

  })

  return lessons
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
          <InputComponent icon="bi bi-search" name="search" placeholder="Search for a lesson" />
          <i class="bi bi-arrows-angle-expand" @click="expandTable" v-if="showExpand"></i>
          <i class="bi bi-plus-lg"></i>
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

.table-header>i {
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
