<script setup lang="tsx">
defineProps(['id'])
import AdminAppLayout from '@/layouts/AdminAppLayout.vue';
import CardV2 from '@/components/CardV2.vue';
import { generateLabel } from "@/fx/utils"
import SkillChart from '@/components/admin/charts/SkillChart.vue';
import Badges from "@/components/admin/children/AdminBadgesComponent.vue"
import TableComponent from '@/components/TableComponent.vue';
import { ref } from 'vue';
import InputComponent from '@/components/InputComponent.vue';

const profile = {
  "info": {
    "child_id": "1",
    "full_name": "Aryan Mehta",
    "age": 10,
    "grade": "5th",
    "enrollment_date": "20 September 2024",
    "status": "Active",
    "parent": {
      "id": 1,
      "name": "Sunita Mehta",
      "email": "sunita@gmail.com",
    },
  },
  "skills_progress": [
    {
      "skill_id": "drawing-basic",
      "skill_name": "Drawing Basics",
      "progress_percent": 85,
    },
    {
      "skill_id": "math-fractions",
      "skill_name": "Fractions",
      "progress_percent": 45,
    }
  ],

  "assessments": [
    {
      "id": 23,
      "skill_id": "Critical Thinking",
      "assessment_type": "Quiz",
      "title": "Fractions Quiz 1",
      "date": "2025-06-28",
      "score": 70,
      "max_score": 100,
    },
    {
      "id": 25,
      "skill_id": "Extracurricular",
      "assessment_type": "Project",
      "title": "Sketch a Fruit Bowl",
      "date": "2025-06-15",
      "max_score": "Pass",
      "score": "Pass",
    }
  ],

  "achievements": {
    "badges": [
      {
        "badge_id": "art-beginner",
        "title": "Art Beginner",
        "awarded_on": "2025-06-10"
      },
      {
        "badge_id": "weekly-3day-streak",
        "title": "3-Day Learning Streak",
        "awarded_on": "2025-06-29"
      }
    ],
    "streak": 7
  },
}

const assessmentLabels = ["ID", "Skill ID", "Type", "Title", "Date", "Score", "Max Score", "Feedback"]

const infoRows = {
  "ID": profile.info.child_id,
  "Full Name": profile.info.full_name,
  "Age": profile.info.age,
  "Grade": profile.info.grade,
  "Status": profile.info.status,
  "Enrollment Date": profile.info.enrollment_date
}

const parentRows = {
  "ID": profile.info.parent.id,
  "Name": profile.info.parent.name,
  "Email": profile.info.parent.email
}

const badges = [
  {
    label: "Quick Thinker",
    image:
      "http://static.vecteezy.com/system/resources/previews/055/850/981/non_2x/cute-brain-cartoon-with-lightning-bolt-vector.jpg",
  },
  {
    label: "Quick Thinker (alt)",
    image:
      "https://thumbs.dreamstime.com/b/brain-lightning-brainstorm-concept-like-cloud-power-mind-103281710.jpg",
  },
  {
    label: "Math Magician",
    image:
      "https://play-lh.googleusercontent.com/_amVHhZZT0Jk3MAHEog0rZeCVMl2w6zQYoDH8Mo7ZjKUIQwRoUxg-FhgALctyKmAjoo",
  },
  {
    label: "Math Magician (alt)",
    image:
      "https://is3-ssl.mzstatic.com/image/thumb/Purple122/v4/91/5c/c1/915cc1a2-0c75-4f6a-437b-68553220653e/source/512x512bb.jpg",
  },
];

function tableEntries() {
  profile.assessments.forEach((p) => {
    p.feedback = <i class="bi bi-journal-text pointer" onClick={() => showFeedbackForm(p.id)}> </i>
  })
  return profile.assessments
}

const showForm = ref(false);
const assessmentId = ref<number | null>(null);

function showFeedbackForm(id: number) {
  assessmentId.value = id;
  showForm.value = true;
}

function hideFeedbackForm() {
  showForm.value = false
}

</script>

<template>
  <AdminAppLayout>
    <!-- Intro -->
    <p class="intro">
      <span class="darken">{{ profile.info.full_name }}</span>
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
        <Badges :badges />
        <button class="button-admin">Block User</button>
      </div>
      <div class="second">
        <CardV2 label-title="Skills" label-image="bi bi-bar-chart">
          <template #content>
            <SkillChart />
          </template>
        </CardV2>
        <CardV2 label-title="Skills" label-image="bi bi-bar-chart">
          <template #content>
            <SkillChart />
          </template>
        </CardV2>
      </div>
    </section>
    <CardV2 label-image="bi bi-patch-question" label-title="Assessment Scores" class="scores">
      <template #content>
        <TableComponent :rows="tableEntries()" :header="assessmentLabels" />
      </template>
    </CardV2>

    <!-- Feedback Form -->
    <section class="feedback-form box-shadow" v-show="showForm">
      <div class="blur-background"></div>
      <CardV2 label-image="bi bi-input-cursor-text" label-title="Feedback Form">
        <template #top-content>
          <i class="bi bi-x-circle" @click="hideFeedbackForm"></i>
        </template>
        <template #content>
          <InputComponent icon="bi bi-cursor-text" name="feedback" placeholder="Write something!"
            input-type="TextArea" />
          <button class="button-admin" @click="hideFeedbackForm">Submit</button>
        </template>
      </CardV2>
    </section>
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
