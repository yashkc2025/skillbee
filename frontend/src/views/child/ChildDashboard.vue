<script setup lang="tsx">
import ChildAppLayout from "../../layouts/ChildAppLayout.vue";
import { getTodayName } from "@/fx/utils";
import Card from "@/components/Card.vue";
import CardItem from "@/components/CardItem.vue";
import Grid from "@/components/Grid.vue";
import DashboardPointsCharts from "@/components/child/DashboardPointsCharts.vue";
import SkillsProgressBar from "@/components/child/SkillsProgressBar.vue"

const skillTypes = [
  { label: "🧠 Critical Thinking", link: "" },
  { label: "💬 Communication Skills", link: "" },
  { label: "⏰ Time Management", link: "" },
  { label: "🎵 Extracurricular Activities", link: "" },
  { label: "💰 Financial Literacy", link: "" },
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
    `📈 ${name}, success starts with showing up—let’s go!`,
    `🎉 Hey ${name}, learning time is the best time!`,
  ];

  const randomIndex = Math.floor(Math.random() * introOptions.length);
  return introOptions[randomIndex];
}

const SkillTemplate = () => {
  return (
    <div>
      <Card title="🌟 Skill Categories">
        {skillTypes.map((s) => (
          <CardItem>
            <div style="display: grid; grid-template-columns: 30% 10% 60%; align-items: center;">
              <a href={s.link} class="skill-card">
                {s.label}
              </a>
              <div></div>
              <SkillsProgressBar />
            </div>
          </CardItem>
        ))}
      </Card>
    </div>
  );
};

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
    label: "Leaderboard Rank",
    answer: "#1",
  },
  {
    label: "Skills Completed",
    count: "2",
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
        <div class="chart box-shadow">
          <DashboardPointsCharts />
        </div>
      </div>
      <SkillTemplate />
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
  align-items: stretch;
  gap: var(--size-sm);
  /* background-color: red; */
}

.stats-grid {
  width: 20%;
}

.chart {
  /* min-width: 30%; */
  /* min-height: 100%; */
  /* width: 30%; */

  flex: 1;
  display: flex;
  flex-direction: column;

  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
}
</style>
