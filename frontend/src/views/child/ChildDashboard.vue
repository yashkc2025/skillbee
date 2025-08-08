<script setup lang="ts">
import ChildAppLayout from "../../layouts/ChildAppLayout.vue";
import { getTodayName } from "../../fx/utils";
import ChildHeatmap from "../../components/child/dashboard/ChildHeatmap.vue";
import Grid from "@/components/Grid.vue";
import SkillTemplate from "@/components/child/dashboard/SkillTemplate.vue";
import BadgesTemplate from "../../components/child/dashboard/BadgesTemplate.vue";
import ChildLeaderboard from "@/components/child/ChildLeaderboard.vue";
import { onMounted, ref } from "vue";
import { base_url } from "../../router";

// const skillTypes = [
//   { skill_id: 1, label: "🧠 Critical Thinking", link: "", progress: 60 },
//   { skill_id: 2, label: "💬 Communication Skills", link: "", progress: 40 },
//   { skill_id: 3, label: "⏰ Time Management", link: "", progress: 80 },
//   { skill_id: 4, label: "🎵 Extracurricular Activities", link: "", progress: 20 },
//   { skill_id: 5, label: "💰 Financial Literacy", link: "", progress: 100 },
// ];

// const badges = [
//   {
//     label: "Quick Thinker",
//     image:
//       "http://static.vecteezy.com/system/resources/previews/055/850/981/non_2x/cute-brain-cartoon-with-lightning-bolt-vector.jpg",
//   },
//   {
//     label: "Quick Thinker (alt)",
//     image:
//       "https://thumbs.dreamstime.com/b/brain-lightning-brainstorm-concept-like-cloud-power-mind-103281710.jpg",
//   },
//   {
//     label: "Math Magician",
//     image:
//       "https://play-lh.googleusercontent.com/_amVHhZZT0Jk3MAHEog0rZeCVMl2w6zQYoDH8Mo7ZjKUIQwRoUxg-FhgALctyKmAjoo",
//   },
//   {
//     label: "Math Magician (alt)",
//     image:
//       "https://is3-ssl.mzstatic.com/image/thumb/Purple122/v4/91/5c/c1/915cc1a2-0c75-4f6a-437b-68553220653e/source/512x512bb.jpg",
//   },
// ];

function getIntroText(name: string): string {
  const dayName = getTodayName();

  const introOptions = [
    `👋 Hello ${name}, let's learn some skills!`,
    `😊 Happy ${dayName}, ${name}!`,
    `🚀 Ready to grow, ${name}? Let's do this!`,
    `📘 Hey ${name}, today is a great day to learn something new.`,
    `🎯 Welcome back, ${name}! Let's make ${dayName} count.`,
    `💡 What’s up, ${name}? Let’s sharpen those skills!`,
    `🌟 Good to see you, ${name}! Let's dive into learning.`,
    `🔥 You’ve got this, ${name}. Let's crush it this ${dayName}.`,
    `📅 ${name}, it's ${dayName} – perfect time to level up!`,
    `🧠 Hi ${name}, let’s turn curiosity into knowledge!`,
    `✨ Let’s make today amazing, ${name}!`,
    `📈 ${name}, success starts with showing up let’s go!`,
    `🎉 Hey ${name}, learning time is the best time!`,
  ];

  const randomIndex = Math.floor(Math.random() * introOptions.length);
  return introOptions[randomIndex];
}

// const stats = [
//   {
//     label: "Lessons Completed",
//     answer: "12",
//   },
//   {
//     label: "Badges Earned",
//     answer: "6",
//   },
//   {
//     label: "Skills Completed",
//     count: "2",
//   },
//   {
//     label: "Leaderboard Rank",
//     answer: "#2",
//   },
//   {
//     label: "Streak",
//     count: "25",
//   },
// ];

const user = ref({});

const stats = ref([
  { label: "Lessons Completed", answer: "-" },
  { label: "Badges Earned", answer: "-" },
  { label: "Skills Completed", count: "-" },
  { label: "Leaderboard Rank", answer: "-" },
  { label: "Streak", count: "-" },
]);

const skillTypes = ref([]);
const badges = ref([]);

async function fetchDashboardData() {
  try {
    const token = localStorage.getItem("authToken");

    // // Authorization
    const userDataResponse = await fetch(`${base_url}auth/get_user`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    if (!userDataResponse.ok) {
      throw new Error("Failed to fetch user data");
    }
    const userData = await userDataResponse.json();
    user.value = {
      id: userData.user.id,
      role: userData.user.role,
      username: userData.user.username,
      name: userData.user.name,
      email: userData.user.email,
      dob: userData.user.dob,
      school: userData.user.school,
    };

    // Dashboard Stats
    const dashStatsResponse = await fetch(`${base_url}child_dashboard_stats`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    if (!dashStatsResponse.ok) {
      throw new Error("Failed to fetch dashboard stats");
    }
    const dashStatsData = await dashStatsResponse.json();
    stats.value = [
      { label: "Lessons Completed", answer: dashStatsData.lessons_completed },
      { label: "Badges Earned", answer: dashStatsData.badges_earned },
      { label: "Skills Completed", count: dashStatsData.skills_completed },
      { label: "Leaderboard Rank", answer: dashStatsData.leaderboard_rank },
      { label: "Streak", count: dashStatsData.streak },
    ];

    // Skills
    const skillsResponse = await fetch(`${base_url}skill_categories`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    if (!skillsResponse.ok) {
      throw new Error("Failed to fetch skills");
    }
    const skillsData = await skillsResponse.json();
    skillTypes.value = skillsData.map((skill: any) => ({
      skill_id: skill.id,
      label: skill.name,
      progress: skill.progress_status,
    }));

    // Badges
    const badgesResponse = await fetch(`${base_url}user_badges`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    if (!badgesResponse.ok) {
      throw new Error("Failed to fetch badges");
    }
    const badgesData = await badgesResponse.json();
    badges.value = badgesData.map((badge: any) => ({
      label: badge.name,
      image: badge.image,
    }));
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
  }
}

onMounted(() => {
  fetchDashboardData();
});
</script>

<template>
  <ChildAppLayout>
    <div class="dashboard kid-dashboard">
      <div class="intro kid-intro">
        <p>{{ getIntroText(user.name) }}</p>
      </div>
      <div class="top-section kid-top-section">
        <div class="stats-grid kid-stats-grid">
          <Grid :stats="stats" />
        </div>
        <div class="leaderboard box-shadow kid-heatmap">
          <ChildHeatmap class="heatmap-fullwidth" />
        </div>
      </div>
      <ChildLeaderboard />
      <SkillTemplate :skillTypes="skillTypes" />
      <div class="kid-badges-section">
        <BadgesTemplate :badges="badges" />
      </div>
    </div>
  </ChildAppLayout>
</template>

<style scoped>
.kid-dashboard {
  display: flex;
  flex-direction: column;
  gap: var(--size-lg);
  background: #fffde7;
  border-radius: var(--border-radius);
  padding: 0 24px 24px 24px;
  min-height: 100vh;
}

.kid-intro {
  font-family: "VAGRoundedNext";
  font-size: var(--font-lg);
  color: #ff9800;
  /* background: #fff8e1; */
  border-radius: var(--border-radius);
  padding: 18px 24px;
  margin-bottom: 10px;
  text-align: center;
  /* box-shadow: 0 2px 8px rgba(255, 193, 7, 0.08); */
  letter-spacing: 1px;
}

.kid-top-section {
  display: flex;
  flex-direction: row;
  gap: var(--size-md);
  align-items: stretch;
  margin-bottom: 10px;
  height: 100%;
  width: 100%;
}

.kid-stats-grid {
  width: 32%;
  min-width: 220px;
}

.kid-heatmap {
  flex: 1;
  background: linear-gradient(90deg, #e3f2fd 0%, #fffde7 100%);
  border-radius: var(--border-radius);
  /* display: flex;flex-direction: column; */
  /* justify-content: center; */
  /* align-items: center; */
  border: 2px solid #ffd54f;
  /* box-shadow: 0 2px 8px rgba(33, 150, 243, 0.08); */
  /* padding: 18px 0; */
  width: 100%;
  /* height: 200px; */
}

.kid-badges-section {
  margin: 18px 0 0 0;
  background: #fff8e1;
  border-radius: var(--border-radius);
  box-shadow: 0 2px 8px rgba(255, 193, 7, 0.08);
  padding: 18px 0;
}

:global(.skill-card) {
  text-decoration: none;
  color: var(--color-text-dark);
  font-family: "VAGRoundedNext";
}

@media (max-width: 900px) {
  .kid-top-section {
    flex-direction: column;
    gap: var(--size-md);
  }

  .kid-stats-grid {
    width: 100%;
    min-width: unset;
  }
}
</style>
