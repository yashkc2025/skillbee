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

const quiz = [
  // Critical Thinking
  {
    id: 1,
    title: "Spot the Flaw in Logic",
    lesson: "Understanding Logical Fallacies",
    curriculum: "Critical Thinking",
  },
  {
    id: 2,
    title: "Decision-Making Under Pressure",
    lesson: "Evaluating Options and Consequences",
    curriculum: "Critical Thinking",
  },

  // Communication Skills
  {
    id: 3,
    title: "Tone and Clarity in Writing",
    lesson: "Writing Effective Emails",
    curriculum: "Communication Skills",
  },
  {
    id: 4,
    title: "Active Listening Challenge",
    lesson: "Listening vs. Hearing",
    curriculum: "Communication Skills",
  },

  // Time Management
  {
    id: 5,
    title: "Prioritize Your Day",
    lesson: "Eisenhower Matrix Activity",
    curriculum: "Time Management",
  },
  {
    id: 6,
    title: "Time Wasters Quiz",
    lesson: "Identifying Unproductive Habits",
    curriculum: "Time Management",
  },

  // Extracurricular Activities
  {
    id: 7,
    title: "Leadership Role Scenarios",
    lesson: "Learning from Club Involvement",
    curriculum: "Extracurricular Activities",
  },
  {
    id: 8,
    title: "Teamwork Simulation",
    lesson: "Working in Group Projects",
    curriculum: "Extracurricular Activities",
  },

  // Financial Literacy
  {
    id: 9,
    title: "Budgeting Basics",
    lesson: "Creating a Personal Budget",
    curriculum: "Financial Literacy",
  },
  {
    id: 10,
    title: "Credit vs. Debit",
    lesson: "Understanding Payment Methods",
    curriculum: "Financial Literacy",
  },
];


const quizLabels = ["ID", "Title", "Lesson", "Curriculum", "Edit"];

const router = useRouter()

function addEntry() {
  router.push(sitemap.admin.new.quiz)
}

function navToLink(name: string, id: number) {
  router.push({ name, params: { id } })
}

function tableEntries() {
  quiz.forEach((p) => {
    p.edit = <i class="bi bi-pen pointer" onClick={() => addEntry()}> </i>
  })

  return quiz
}
</script>

<template>
  <AdminAppLayout>
    <p class="intro">
      <span class="darken">Manage Quiz</span>
    </p>
    <CardV2 label-title="Quiz" label-image="bi bi-book">
      <template #top-content>
        <div class="table-header">
          <InputComponent icon="bi bi-search" name="search" placeholder="Search for a quiz" />
          <i class="bi bi-plus-lg" @click="addEntry()"></i>
        </div>
      </template>
      <template #content>
        <TableComponent :header="quizLabels" :rows="tableEntries()" />
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
