<script setup lang="ts">
import CardV2 from '@/components/CardV2.vue';

interface BadgeType {
  label: string;
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
          <img :src="s.image" :alt="s.label" />
          <span class="skill-card">{{ s.label }}</span>
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
