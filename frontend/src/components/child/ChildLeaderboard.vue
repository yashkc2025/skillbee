<script setup lang="ts">
import { ref, computed } from "vue";
import Card from '@/components/Card.vue';
import CardItem from '@/components/CardItem.vue';
import AppButton from "../AppButton.vue";

const leaderboardStats = [
  { position: 1, name: "Nishant Kumar", promoted_on: "2025-06-20" },
  { position: 2, name: "Aarav Mehta", promoted_on: "2025-06-22" },
  { position: 3, name: "Rohan Verma", promoted_on: "2025-06-24" },
  { position: 4, name: "Sneha Reddy", promoted_on: "2025-06-25" },
  { position: 5, name: "Vivaan Nair", promoted_on: "2025-06-27" },
  { position: 6, name: "Ananya Singh", promoted_on: "2025-06-28" },
  { position: 7, name: "Arjun Patel", promoted_on: "2025-06-30" },
  { position: 8, name: "Isha Kapoor", promoted_on: "2025-07-01" },
  { position: 9, name: "Rahul Sharma", promoted_on: "2025-07-02" },
  { position: 10, name: "Priya Gupta", promoted_on: "2025-07-03" }
];

const showAll = ref(false);
const userName = "Isha Kapoor"; // Replace with actual user name from auth context or props

const userIndex = computed(() => leaderboardStats.findIndex(s => s.name === userName));

const visibleRows = computed(() => {
  if (showAll.value) {
    return leaderboardStats;
  }
  // If user is not in leaderboard, show top 6
  if (userIndex.value === -1) {
    return leaderboardStats.slice(0, 6);
  }
  // If user is in top 6, show top 6
  if (userIndex.value < 6) {
    return leaderboardStats.slice(0, 6);
  }
  // If user is below 6th, show 1st 3, then previous, user, next
  const rows: typeof leaderboardStats = [];
  rows.push(...leaderboardStats.slice(0, 3));
  // previous, user, next
  if (userIndex.value > 0) rows.push(leaderboardStats[userIndex.value - 1]);
  rows.push(leaderboardStats[userIndex.value]);
  if (userIndex.value < leaderboardStats.length - 1) rows.push(leaderboardStats[userIndex.value + 1]);
  return rows;
});

function expandTable() {
  if (showAll.value === false)
    showAll.value = true;
  else
    showAll.value = false;
}
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
          <span class="leaderboard-col">Promoted On</span>
        </div>
      </div>
      <CardItem v-for="(s, i) in visibleRows" :key="i">
        <div class="leaderboard-row" :class="{
          'leaderboard-me': s.name === userName,
          'leaderboard-top': s.position === 1,
          'leaderboard-other': s.name !== userName && s.position !== 1
        }">
          <span class="leaderboard-rank">
            <span v-if="s.position === 1">🥇</span>
            <span v-else-if="s.position === 2">🥈</span>
            <span v-else-if="s.position === 3">🥉</span>
            <span v-else>#{{ s.position }}</span>
          </span>
          <span class="leaderboard-name">{{ s.name === userName ? "👦 You" : s.name }}</span>
          <span class="leaderboard-date">{{ s.promoted_on }}</span>
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
.leaderboard-table-header {
  display: grid;
  grid-template-columns: 15% 55% 30%;
  font-family: 'VAGRoundedNext';
  font-size: var(--font-md);
  color: #42a5f5;
  font-weight: bold;
  background: #fff3e0;
  border-radius: var(--border-radius);
  /* padding: 8px 0 8px 0; */
  margin-bottom: 1px;
  text-align: left;
  letter-spacing: 1px;
  /* margin: 4px 0; */
  padding: var(--size-xs) var(--size-md);
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
  /* padding: 10px 0; */
  padding: var(--size-xs) var(--size-md);
  box-shadow: 0 1px 4px rgba(255, 193, 7, 0.08);
  transition: background 0.2s, transform 0.15s;
}

.leaderboard-top {
  /* background: linear-gradient(90deg, #ffe082 0%, #fffde7 100%); */
  background: #fffde7;
  font-weight: bold;
  color: #ff9800;
  border: 2px solid #ffd54f;
}

.leaderboard-me {
  /* background: linear-gradient(90deg, #b2ff59 0%, #fffde7 100%); */
  background: #b2ff5983;
  font-weight: bold;
  color: #388e3c;
  border: 2px solid #43a047;
  /* transform: scale(1.03); */
}

.leaderboard-other {
  color: #6d4c41;
}

.leaderboard-rank {
  font-size: 1.3rem;
  font-family: 'VAGRoundedNext', cursive;
  /* text-align: center; */
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

/* .expand-btn {
   background: linear-gradient(90deg, #ffd54f 0%, #ffb300 100%);
   color: #4a148c;
   font-weight: bold;
   border-radius: 12px;
   font-family: 'VAGRoundedNext', cursive;
   font-size: 1.1rem;
   padding: 8px 28px;
   box-shadow: 0 2px 8px rgba(255, 193, 7, 0.13);
   border: none;
   cursor: pointer;
   transition: background 0.2s, color 0.2s;
 } */

.expand-btn:hover {
  background: #ffe082;
  color: #d84315;
}
</style>
