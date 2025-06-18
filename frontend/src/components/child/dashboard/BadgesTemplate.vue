<script setup lang="ts">
import Card from "@/components/Card.vue";
import HorizontalCardItem from "@/components/HorizontalCardItem.vue";

interface BadgeType {
  label: string;
  image: string;
}

const props = defineProps<{
  badges: BadgeType[];
}>();
</script>

<template>
  <div>
    <Card title="🏅 Badges" direction="row" isFitToContent="true">
      <HorizontalCardItem v-for="(s, i) in props.badges" :key="i">
        <div class="badge-parent">
          <img :src="s.image" :alt="s.label" />
          <span class="skill-card">{{ s.label }}</span>
        </div>
      </HorizontalCardItem>
    </Card>
  </div>
</template>

<style>
img {
  width: 100px;
}

.badge-parent {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100px;
  height: 150px;
}
</style>
