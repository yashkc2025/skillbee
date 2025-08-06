<script setup lang="ts">
import Card from '@/components/Card.vue';
import CardItem from '@/components/CardItem.vue';

const leaderboardStats = [
  {
    position: 1,
    name: "Aarav Mehta",
    promoted_on: "2025-06-20"
  },
  {
    position: 2,
    name: "You",
    promoted_on: "2025-06-22"
  },
  {
    position: 3,
    name: "Rohan Verma",
    promoted_on: "2025-06-24"
  },
  {
    position: 4,
    name: "Sneha Reddy",
    promoted_on: "2025-06-25"
  },
  {
    position: 5,
    name: "Vivaan Nair",
    promoted_on: "2025-06-27"
  },
];
</script>

<template>
  <div>
    <Card title="🏆 Leaderboard" direction="column" :is-fit-to-content="false">
      <CardItem v-for="(s, i) in leaderboardStats" :key="i">
        <div class="card skill-card">
          <p :class="{ danger: s.name === 'You' }">{{ s.position }}</p>
          <p :class="{ danger: s.name === 'You' }">{{ s.name }}</p>
        </div>
      </CardItem>
    </Card>
  </div>
</template>

<style scoped>
.card {
  display: grid;
  grid-template-columns: 30% 10% 30%;
  align-items: center
}

.danger {
  color: var(--color-pink);
}
</style>
