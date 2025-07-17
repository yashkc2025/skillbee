<script setup lang="tsx">
import CardV2 from "@/components/CardV2.vue";
import InputComponent from "@/components/InputComponent.vue";
import TableComponent from "@/components/TableComponent.vue";
import { useRouter, useRoute } from "vue-router";
import sitemap from "@/router/sitemap.json"
import AdminAppLayout from "@/layouts/AdminAppLayout.vue";
import { onMounted } from "vue";
import { ref } from "vue";

type ActivitiesType = {
  id: number,
  title: string,
  lesson: string,
  curriculum: string
}[]

const router = useRouter()
const activities = ref<ActivitiesType>([])
const searchText = ref("")
const lesson_id = useRoute().query.lesson_id

onMounted(async () => {
  // const data = fetchData(getBackendURL(""),[["lesson_id", lesson_id]])
  const data = [
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

  activities.value = data
})

const activitiesLabels = ["ID", "Title", "Lesson", "Curriculum", "Edit"];


function addEntry() {
  router.push(sitemap.admin.new.activity)
}

function navToLink(name: string, id: number) {
  router.push({ name, params: { id } })
}

function tableEntries() {
  const lowerSearch = searchText.value.toLowerCase().trim();

  return activities.value
    .filter((activity) =>
      [activity.title, activity.lesson, activity.curriculum]
        .some((field) => field.toLowerCase().includes(lowerSearch))
    )
    .map((p) => ({
      ...p,
      edit: (
        <i class="bi bi-pen pointer" onClick={() => addEntry()}></i>
      ),
    }));
}

</script>

<template>
  <AdminAppLayout>
    <p class="intro">
      <span class="darken" v-if="lesson_id && activities[0]?.lesson">Activities for : {{ activities[0].lesson }}</span>
      <span class="darken" v-else>Manage Activities</span>
    </p>
    <CardV2 label-title="Activities" label-image="bi bi-book">
      <template #top-content>
        <div class="table-header">
          <InputComponent icon="bi bi-search" name="search" placeholder="Search for an Activity" v-model="searchText" />
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
