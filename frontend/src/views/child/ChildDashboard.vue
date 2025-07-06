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
    <div class="dashboard">
      <div class="intro">
        <p>{{ getIntroText("Yash") }}</p>
      </div>
      <div class="top-section">
        <div class="stats-grid">
          <Grid :stats="stats" />
        </div>
        <div class="leaderboard box-shadow">
          <ChildHeatmap />
        </div>
      </div>
      <ChildLeaderboard />
      <SkillTemplate :skillTypes="skillTypes" />
      <BadgesTemplate :badges="badges" />
    </div>
  </ChildAppLayout>
</template>

<style scoped>
.intro {
  font-family: "VAGRoundedNext";
  font-size: var(--font-md);
}

.dashboard {
  display: flex;
  flex-direction: column;
  gap: var(--size-md);
}

:global(.skill-card) {
  text-decoration: none;
  color: var(--color-text-dark);
  font-family: "VAGRoundedNext";
}

.top-section {
  display: flex;
  flex-direction: row;
  gap: var(--size-sm);
  align-items: stretch;
  /* Ensures children stretch to same height */
}

.stats-grid {
  width: 30%;
}

.leaderboard {
  /* width: 30%; */
  background-color: var(--color-light);

  flex: 1;
  display: flex;
  flex-direction: column;

  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
}
</style>
