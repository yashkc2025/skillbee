<script setup lang="ts">
import ChildAppLayout from "../../layouts/ChildAppLayout.vue";
import { getTodayName } from "../../fx/utils";
import ChildHeatmap from "../../components/child/dashboard/ChildHeatmap.vue";
import Grid from "@/components/Grid.vue";
import SkillTemplate from "@/components/child/dashboard/SkillTemplate.vue";
import BadgesTemplate from "../../components/child/dashboard/BadgesTemplate.vue";
import ChildLeaderboard from "@/components/child/ChildLeaderboard.vue";

const skillTypes = [
  { curriculum_id: 1, label: "🧠 Critical Thinking", link: "", progress: 60 },
  { curriculum_id: 2, label: "💬 Communication Skills", link: "", progress: 40 },
  { curriculum_id: 3, label: "⏰ Time Management", link: "", progress: 80 },
  { curriculum_id: 4, label: "🎵 Extracurricular Activities", link: "", progress: 20 },
  { curriculum_id: 5, label: "💰 Financial Literacy", link: "", progress: 100 },
];

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

const stats = [
  {
    label: "Lessons Completed",
    answer: "12",
  },
  {
    label: "Badges Earned",
    answer: "6",
  },
  {
    label: "Skills Completed",
    count: "2",
  },
  {
    label: "Leaderboard Rank",
    answer: "#2",
  },
  {
    label: "Streak",
    count: "25",
  },
];
</script>

<template>
  <ChildAppLayout>
    <div class="dashboard kid-dashboard">
      <div class="intro kid-intro">
        <p>{{ getIntroText("Yash") }}</p>
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
