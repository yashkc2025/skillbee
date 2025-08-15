<template>
  <ChildAppLayout>
    <div class="achievements-page">
      <h2 class="achievements-title ft-head-1">🏆 My Achievements</h2>

      <div class="badges-section">
        <h3>🎖️ Badges Earned</h3>
        <div class="badges-list">
          <div v-if="badges.length === 0">You're on your way to your first badge — keep trying!</div>
          <div v-for="badge in badges" :key="badge.id" class="badge-card">
            <img :src="fixImage(badge.image)" :alt="badge.label" class="badge-icon" />
          </div>
        </div>
      </div>

      <div class="heatmap-section">
        <h3>🔥 Activity Streak</h3>
        <div class="heatmap-kid-bg">
          <ChildHeatmap class="heatmap-fullwidth" />
        </div>
      </div>

      <div class="charts-section" v-if="childId">
        <h3>📚 Curriculum Progress</h3>
        <ChildSkillChart :child-id="childId.toString()" />
      </div>

      <div class="charts-section" v-if="childId">
        <h3>📈 Points Earned Over Time</h3>
        <PointsChart :child-id="childId.toString()" />
      </div>
    </div>
  </ChildAppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import ChildAppLayout from "@/layouts/ChildAppLayout.vue";
import ChildSkillChart from "@/components/admin/charts/ChildSkillChart.vue";
import PointsChart from "@/components/admin/charts/PointsChart.vue";
import ChildHeatmap from "@/components/child/dashboard/ChildHeatmap.vue";
import { base_url } from "../../router";
import { fixImage } from "../../fx/utils";

const childId = ref<number | undefined>();

const props = defineProps({
  child_id: {
    type: Number,
    required: true,
  },
});

interface Badge {
  id: number;
  label: string;
  image: string;
}

const badges = ref<Badge[]>([]);

async function fetchBadges() {
  const token = localStorage.getItem("authToken");
  try {
    const response = await fetch(`${base_url}child_badges`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch badges");
    }
    const data: Badge[] = await response.json();
    badges.value = data;
    console.log("Badges fetched successfully:", badges.value);
  } catch (error) {
    console.error("Error fetching badges:", error);
  }
}

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
    console.log("ChildID", childId.value);
  }
  await fetchBadges();
});
</script>

<style scoped>
/* Your existing styles remain unchanged */
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

.heatmap-section {
  margin-bottom: 36px;
  background: #fff3e0;
  border-radius: var(--border-radius);
  padding: 18px 18px 10px 18px;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.08);
}

.heatmap-section h3 {
  color: #ef476f;
  font-family: "VAGRoundedNext";
  font-size: var(--font-ml-lg);
  margin-bottom: 10px;
  letter-spacing: 1px;
}

.heatmap-kid-bg {
  background: #fffde7;
  border-radius: var(--border-radius);
  margin-bottom: 8px;
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