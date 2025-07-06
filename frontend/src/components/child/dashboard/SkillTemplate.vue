<script setup lang="ts">
import ProgressBar from "@/components/ProgressBar.vue";
import Card from "@/components/Card.vue";
import CardItem from "@/components/CardItem.vue";
import { useRouter } from "vue-router";

const router = useRouter();

interface SkillType {
  curriculum_id: number;
  label: string;
  link: string;
  progress: number;
}

const props = defineProps<{
  skillTypes: SkillType[];
}>();

function openCurriculum(curriculumId: number, curriculumName: string) {
  router.push({
    name: "child_lessons",
    params: { curriculumId, curriculumName }
  });
}
</script>

<template>
  <div>
    <Card title="🌟 Skill Categories">
      <CardItem v-for="(s, i) in props.skillTypes" :key="i">
        <div @click.prevent="openCurriculum(s.curriculum_id, s.label)"
          style="display: grid; grid-template-columns: 30% 10% 60%; align-items: center">
          <div class="skill-card">{{ s.label }}</div>
          <div></div>
          <ProgressBar :progress="s.progress" />
        </div>
      </CardItem>
    </Card>
  </div>
</template>

<style scoped>
.skill-card {
  cursor: pointer;
}
</style>