<script setup lang="tsx">
const props = defineProps({
  id: {
    type: Number,
    required: true,
  },
});
import AdminAppLayout from "@/layouts/AdminAppLayout.vue";
import CardV2 from "@/components/CardV2.vue";
import { generateLabel, getBackendURL } from "@/fx/utils";
import SkillChart from "@/components/admin/charts/SkillChart.vue";
import Badges from "@/components/admin/children/AdminBadgesComponent.vue";
import TableComponent from "@/components/TableComponent.vue";
import { ref } from "vue";
import PointsChart from "@/components/admin/charts/PointsChart.vue";
import { fetchData, postData } from "@/fx/api";
import { onMounted } from "vue";
import ChildSkillChart from "@/components/admin/charts/ChildSkillChart.vue";

export type ProfileType = {
  info: {
    child_id: string;
    full_name: string;
    age: number;
    enrollment_date: string; // e.g., "2024-09-20"
    status: string;
    parent: {
      id: number;
      name: string;
      email: string;
    };
  };

  skills_progress: Array<{
    skill_id: string;
    skill_name: string;
    lesson_started_count: number;
    lesson_completed_count: number;
    quiz_attempted_count: number;
  }>;

  point_earned: Array<{
    point: number;
    date: string; // YYYY-MM-DD
  }>;

  assessments: Array<{
    id: number;
    skill_id: string;
    assessment_type: "Quiz" | "Activity";
    title: string;
    date: string; // ISO or YYYY-MM-DD
    score: number | "Pass";
    max_score: number | string;
  }>;

  achievements: {
    badges: Array<{
      badge_id: string;
      title: string;
      image: string; // Base64
      awarded_on: string; // ISO or date string
    }>;
    streak: number;
  };
};

type RowTypes = { [key: string]: string | number };

const profile = ref<ProfileType>();
const infoRows = ref<RowTypes>();
const parentRows = ref<RowTypes>();
const points = ref({ point: [], dates: [] });
const feedbackText = ref("");

onMounted(async () => {
  const data: ProfileType = await fetchData(getBackendURL("children/profile"), {
    id: props.id,
  });
  if (data) {
    profile.value = data;

    infoRows.value = {
      ID: profile.value.info.child_id,
      "Full Name": profile.value.info.full_name,
      Age: profile.value.info.age,
      Status: profile.value.info.status,
      "Enrollment Date": profile.value.info.enrollment_date,
    };

    parentRows.value = {
      ID: profile.value.info.parent.id,
      Name: profile.value.info.parent.name,
      Email: profile.value.info.parent.email,
    };
  }
});

const assessmentLabels = [
  "ID",
  "Skill ID",
  "Type",
  "Title",
  "Date",
  "Score",
  "Max Score",
];

function tableEntries() {
  if (!profile.value || !Array.isArray(profile.value.assessments)) {
    return [];
  }
  return profile?.value.assessments.map((p) => ({
    id: p.id,
    skill_id: p.skill_id,
    a_type: p.assessment_type,
    title: p.title,
    dt: p.date,
    score: p.score,
    max_score: p.max_score,
  }));
}

async function blockChild() {
  await postData("", {
    children_id: profile.value?.info.child_id,
  });
}

async function unBlockChild() {
  await postData("", {
    children_id: profile.value?.info.child_id,
  });
}
</script>

<template>
  <AdminAppLayout>
    <!-- Intro -->
    <p class="intro">
      <span class="darken">{{ profile?.info.full_name }}</span>
    </p>

    <!-- Info and Charts -->
    <section class="child-info">
      <div class="first">
        <CardV2 label-title="Children Info" label-image="bi bi-emoji-smile">
          <template #content>
            <div v-for="(value, property) in infoRows" class="info-elem" :key="value">
              <span>{{ generateLabel(property as string) }}</span>
              <span>{{ value }}</span>
            </div>
          </template>
        </CardV2>
        <CardV2 label-title="Parent Info" label-image="bi bi-person">
          <template #content>
            <div v-for="(value, property) in parentRows" class="info-elem" :key="value">
              <span>{{ generateLabel(property as string) }}</span>
              <span>{{ value }}</span>
            </div>
          </template>
        </CardV2>
        <Badges
          :badges="profile.achievements.badges"
          v-if="profile?.achievements.badges"
        />
        <button class="button-admin" v-if="profile?.info.status === 'Active'">
          Block User
        </button>
        <button class="button-admin" v-if="profile?.info.status !== 'Active'">
          Unblock User
        </button>
      </div>
      <div class="second">
        <CardV2 label-title="Skills" label-image="bi bi-bar-chart">
          <template #content>
            <ChildSkillChart :child-id="props.id" />
          </template>
        </CardV2>
        <CardV2 label-title="Points Earned" label-image="bi bi-stars">
          <template #content>
            <PointsChart :child-id="props.id" />
          </template>
        </CardV2>
      </div>
    </section>
    <CardV2
      label-image="bi bi-patch-question"
      label-title="Assessment Scores"
      class="scores"
    >
      <template #content>
        <TableComponent :rows="tableEntries()" :header="assessmentLabels" />
      </template>
    </CardV2>
  </AdminAppLayout>
</template>

<style scoped>
.intro {
  margin-bottom: 20px;
}

.child-info {
  display: flex;
  flex-direction: row;
  gap: var(--size-sm);
}

.info-elem {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-sm);
  margin-bottom: 5px;
}

.first {
  flex: 40%;
  display: flex;
  flex-direction: column;
  gap: var(--size-sm);
}

.second {
  flex: 60%;
  display: flex;
  flex-direction: column;
  gap: var(--size-sm);
}

.scores {
  margin-top: 20px;
}

.feedback-form {
  /* display: none; */
  width: 500px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
