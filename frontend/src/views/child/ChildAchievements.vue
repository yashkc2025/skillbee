<template>
  <ChildAppLayout>
    <div class="achievements-page">
      <h2 class="achievements-title ft-head-1">🏆 My Achievements</h2>

      <!-- Badges Section -->
      <div class="badges-section">
        <h3>🎖️ Badges Earned</h3>
        <div class="badges-list">
          <div v-for="badge in badges" :key="badge.id" class="badge-card">
            <img :src="badge.icon" :alt="badge.name" class="badge-icon" />
            <!-- <div class="badge-name">{{ badge.name }}</div>
                        <div class="badge-desc">{{ badge.description }}</div> -->
          </div>
        </div>
      </div>

      <!-- Heatmap Section -->
      <div class="heatmap-section">
        <h3>🔥 Activity Streak</h3>
        <div class="heatmap-kid-bg">
          <ChildHeatmap class="heatmap-fullwidth" />
        </div>
      </div>

      <!-- Curriculum-wise Performance Chart -->
      <div class="charts-section">
        <h3>📚 Curriculum Progress</h3>
        <SkillChart />
      </div>

      <!-- Points Earned Over Time Chart -->
      <div class="charts-section" v-if="childId">
        <h3>📈 Points Earned Over Time</h3>
        <PointsChart :child-id="childId" />
      </div>
    </div>
  </ChildAppLayout>
</template>

<script setup lang="ts">
import { ref } from "vue";
import ChildAppLayout from "@/layouts/ChildAppLayout.vue";
import SkillChart from "@/components/admin/charts/SkillChart.vue";
import PointsChart from "@/components/admin/charts/PointsChart.vue";
import ChildHeatmap from "@/components/child/dashboard/ChildHeatmap.vue";
import { onMounted } from "vue";
import { base_url } from "../../router";

const childId = ref<number>();

onMounted(async () => {
  const token = localStorage.getItem("authToken");

  const userDataResponse = await fetch(`${base_url}auth/get_user`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  }).then((p) => p.json());

  if (userDataResponse) {
    childId.value = userDataResponse.user.id;
  }
});

// Dummy badge data
const badges = ref([
  {
    id: 1,
    // name: "Quiz Master",
    icon: "/badges/quiz_master.png",
    // description: "Completed 5 quizzes!",
  },
  {
    id: 2,
    // name: "Finisher",
    icon: "/badges/finisher.png",
    // description: "Completed all lessons in a curriculum!",
  },
  {
    id: 3,
    // name: "Perfect",
    icon: "/badges/perfect.png",
    // description: "Achieved 100% score in a quiz!",
  },
  {
    id: 4,
    // name: "30 Day Streak",
    icon: "/badges/30_day_streak.png",
    // description: "Maintained a 30-day activity streak!",
  },
  {
    id: 5,
    // name: "Math Magician",
    icon: "/badges/all_rounder.png",
    // description: "Solved 100 math problems!",
  },
  {
    id: 6,
    // name: "Quick Thinker",
    icon: "/badges/cash_clash.png",
    // description: "Answered 50 questions in under 1 minute!",
  },
]);
</script>

<style scoped>
.achievements-page {
  margin: 0 auto;
  padding: 28px 18px 18px 18px;
  font-family: "Delius";
}

.achievements-title {
  color: #ff9800;
  font-family: "VAGRoundedNext";
  margin-bottom: 24px;
  letter-spacing: 1px;
}

.badges-section {
  margin-bottom: 36px;
  background: #fff8e1;
  border-radius: 18px;
  padding: 18px 18px 12px 18px;
  box-shadow: 0 2px 8px rgba(255, 193, 7, 0.08);
}

.badges-section h3 {
  color: #ffb300;
  font-family: "VAGRoundedNext";
  font-size: var(--font-ml-lg);
  margin-bottom: 12px;
}

.badges-list {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
}

.badge-card {
  background: #fff3e0;
  border-radius: var(--border-radius);
  box-shadow: 0 2px 8px rgba(255, 193, 7, 0.13);
  padding: 18px 16px;
  min-width: 120px;
  max-width: 160px;
  text-align: center;
  font-family: "Delius";
  transition: transform 0.15s;
}

.badge-card:hover {
  transform: scale(1.07);
  box-shadow: 0 4px 16px rgba(255, 193, 7, 0.18);
}

.badge-icon {
  width: 100%;
  height: 100%;
  margin-bottom: 8px;
}

.badge-name {
  color: #4caf50;
  font-weight: bold;
  font-size: var(--font-md);
  margin-bottom: 4px;
}

.badge-desc {
  color: #6d4c41;
  font-size: var(--font-sm);
}

/* Kid-friendly Heatmap Section */
.heatmap-section {
  margin-bottom: 36px;
  background: #fff3e0;
  border-radius: var(--border-radius);
  padding: 18px 18px 10px 18px;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.08);
  /* text-align: center; */
}

.heatmap-section h3 {
  color: #ef476f;
  font-family: "VAGRoundedNext";
  font-size: var(--font-ml-lg);
  margin-bottom: 10px;
  letter-spacing: 1px;
}

.heatmap-kid-bg {
  /* background: linear-gradient(90deg, #fffde7 0%, #ffe082 100%); */
  background: #fffde7;
  border-radius: var(--border-radius);
  /* padding: 18px 0 10px 0; */
  margin-bottom: 8px;
  /* display: flex; */
  /* justify-content: center;align-items: center; */
  width: 100%;
  height: 200px;
}

.heatmap-fullwidth {
  width: 100%;
  min-width: 100%;
  max-width: 100%;
  height: 100%;
}

.charts-section {
  margin-bottom: 36px;
  background: #fffde7;
  border-radius: var(--border-radius);
  padding: 18px 18px 12px 18px;
  box-shadow: 0 2px 8px rgba(255, 193, 7, 0.08);
}

.charts-section h3 {
  color: #42a5f5;
  font-family: "VAGRoundedNext";
  font-size: var(--font-ml-lg);
  margin-bottom: 12px;
  text-align: left;
}
</style>
