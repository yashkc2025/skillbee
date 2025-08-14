<script setup lang="ts">
import { ref, computed, onMounted, defineProps } from "vue";
import Card from '@/components/Card.vue';
import CardItem from '@/components/CardItem.vue';
import AppButton from "../AppButton.vue";
import { base_url } from "../../router";

// Props to receive the current user's name from the parent component
const props = defineProps({
  userName: {
    type: String,
    required: true,
  },
});

const leaderboardStats = ref<Array<{ position: number; name: string; promoted_on: string }>>([]);
const showAll = ref(false);

const userIndex = computed(() => leaderboardStats.value.findIndex(s => s.name === props.userName));

const visibleRows = computed(() => {
  if (showAll.value) {
    return leaderboardStats.value;
  }
  // If user is not in leaderboard, show top 6
  if (userIndex.value === -1) {
    return leaderboardStats.value.slice(0, 6);
  }
  // If user is in top 6, show top 6
  if (userIndex.value < 6) {
    return leaderboardStats.value.slice(0, 6);
  }
  // If user is below 6th, show 1st 3, then previous, user, next
  const rows: typeof leaderboardStats.value = [];
  rows.push(...leaderboardStats.value.slice(0, 3));
  // previous, user, next
  if (userIndex.value > 0) rows.push(leaderboardStats.value[userIndex.value - 1]);
  rows.push(leaderboardStats.value[userIndex.value]);
  if (userIndex.value < leaderboardStats.value.length - 1) rows.push(leaderboardStats.value[userIndex.value + 1]);
  return rows;
});

function expandTable() {
  showAll.value = !showAll.value;
}

// Function to fetch leaderboard data from the API
async function fetchLeaderboard() {
  try {
    const token = localStorage.getItem("authToken");
    const response = await fetch(`${base_url}child_leaderboard`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch leaderboard data");
    }

    const data = await response.json();
    leaderboardStats.value = data.map((item: any) => ({
      position: item.rank,
      name: item.name,
      // Assuming 'promoted_on' is not available in the new API,
      // you'll need to decide how to handle this.
      // For now, I'll use a placeholder or remove it if not needed.
      // If you need this data, please update your API to include it.
      promoted_on: "N/A",
    }));
  } catch (error) {
    console.error("Error fetching leaderboard:", error);
  }
}

onMounted(() => {
  fetchLeaderboard();
});
</script>

<template>
  <div>
    <Card title="🏆 Leaderboard" direction="column" :is-fit-to-content="false">
      <div v-if="visibleRows.length === 0">
        <div class="leaderboard-table-header">
          <span class="leaderboard-col center">No Data Available</span>
        </div>
      </div>
      <div v-else-if="visibleRows.length > 0">
        <div class="leaderboard-table-header">
          <span class="leaderboard-col center">Rank</span>
          <span class="leaderboard-col">Name</span>
          <span class="leaderboard-col">Points</span>
        </div>
      </div>
      <CardItem v-for="(s, i) in visibleRows" :key="i">
        <div class="leaderboard-row" :class="{
          'leaderboard-me': s.name === props.userName,
          'leaderboard-top': s.position === 1,
          'leaderboard-other': s.name !== props.userName && s.position !== 1
        }">
          <span class="leaderboard-rank">
            <span v-if="s.position === 1">🥇</span>
            <span v-else-if="s.position === 2">🥈</span>
            <span v-else-if="s.position === 3">🥉</span>
            <span v-else>#{{ s.position }}</span>
          </span>
          <span class="leaderboard-name">{{ s.name === props.userName ? "👦 You" : s.name }}</span>
          <span class="leaderboard-date">{{ s.points }}</span>
        </div>
      </CardItem>
    </Card>
    <div class="expand-btn-wrap">
      <AppButton type='primary' @click="expandTable">{{ showAll ? 'Show Less 👀' : 'Show All 🏆' }}
      </AppButton>
    </div>
  </div>
</template>

<style scoped>
/* Your existing styles remain unchanged */
.leaderboard-table-header {
  display: grid;
  grid-template-columns: 15% 55% 30%;
  font-family: 'VAGRoundedNext';
  font-size: var(--font-md);
  color: #42a5f5;
  font-weight: bold;
  background: #fff3e0;
  border-radius: var(--border-radius);
  padding: var(--size-xs) var(--size-md);
  margin-bottom: 1px;
  text-align: left;
  letter-spacing: 1px;
  border: 1px solid rgba(211, 210, 210, 0.455);
}

.center {
  margin-left: 20px;
}

.leaderboard-row {
  display: grid;
  grid-template-columns: 15% 55% 30%;
  align-items: center;
  font-family: 'Delius';
  font-size: var(--font-md);
  background: #fff8e1;
  border-radius: var(--border-radius);
  margin: 1px 0;
  padding: var(--size-xs) var(--size-md);
  box-shadow: 0 1px 4px rgba(255, 193, 7, 0.08);
  transition: background 0.2s, transform 0.15s;
}

.leaderboard-top {
  background: #fffde7;
  font-weight: bold;
  color: #ff9800;
  border: 2px solid #ffd54f;
}

.leaderboard-me {
  background: #b2ff5983;
  font-weight: bold;
  color: #388e3c;
  border: 2px solid #43a047;
}

.leaderboard-other {
  color: #6d4c41;
}

.leaderboard-rank {
  font-size: 1.3rem;
  font-family: 'VAGRoundedNext', cursive;
  margin-left: 20px;
}

.leaderboard-name {
  font-size: 1.1rem;
  font-family: 'Comic Sans MS', cursive;
  text-align: left;
}

.leaderboard-date {
  font-size: 1rem;
  color: #1976d2;
  font-family: 'Delius', cursive;
  text-align: left;
}

.expand-btn-wrap {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.expand-btn:hover {
  background: #ffe082;
  color: #d84315;
}
</style>