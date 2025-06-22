<script setup lang="ts">
import ProgressBar from "@/components/ProgressBar.vue";
import Card from "@/components/Card.vue";
import CardItem from "@/components/CardItem.vue";

interface SkillType {
  label: string;
  link: string;
  progress: number;
}

const props = defineProps<{
  skillTypes: SkillType[];
}>();
</script>

<template>
  <div>
    <Card title="🌟 Skill Categories">
      <CardItem v-for="(s, i) in props.skillTypes" :key="i">
        <div style="display: grid; grid-template-columns: 30% 10% 60%; align-items: center">
          <a :href="s.link" class="skill-card">{{ s.label }}</a>
          <div></div>
          <ProgressBar :progress="s.progress" />
        </div>
      </CardItem>
    </Card>
  </div>
</template>
