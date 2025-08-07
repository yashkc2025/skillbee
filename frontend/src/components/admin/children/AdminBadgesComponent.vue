<script setup lang="ts">
import CardV2 from "@/components/CardV2.vue";
import { fixImage } from "@/fx/utils";

interface BadgeType {
  title: string;
  image: string;
}

const props = defineProps<{
  badges: BadgeType[];
}>();
</script>

<template>
  <CardV2 labelTitle="Badges" labelImage="bi bi-stars">
    <template #content>
      <div class="badge-group">
        <div v-for="(s, i) in props.badges" :key="i" class="badge-parent">
          <img :src="fixImage(s.image)" :alt="s.title" />
          <span class="skill-card">{{ s.title }}</span>
        </div>
      </div>
    </template>
  </CardV2>
</template>

<style scoped>
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

.badge-group {
  display: flex;
  flex-wrap: wrap;
  gap: var(--size-base);
}
</style>
