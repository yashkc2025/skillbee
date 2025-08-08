<script setup lang="ts">
import ProgressBar from "@/components/ProgressBar.vue";
import Card from "@/components/Card.vue";
import CardItem from "@/components/CardItem.vue";
import { useRouter } from "vue-router";

const router = useRouter();

interface SkillType {
  skill_id: number;
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
    params: { curriculumId, curriculumName },
  });
}

function getSkillLink(id: number): string {
  return `http://localhost:5173/child/curriculum/${id}/lessons`;
}
</script>

<template>
  <div>
    <Card title="📚 Curriculums">
      <CardItem v-for="(s, i) in props.skillTypes" :key="i">
        <div
          @click="openCurriculum(s.skill_id, s.label)"
          class="skill-card"
          style="display: grid; grid-template-columns: 30% 10% 60%; align-items: center"
        >
          <a :href="getSkillLink(s.skill_id)" class="">{{ s.label }}</a>
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
  background: #fff8e1;
  border-radius: var(--border-radius);
  margin: 1px 0;
  /* padding: 10px 0; */
  padding: var(--size-xs) var(--size-md);
  box-shadow: 0 1px 4px rgba(255, 193, 7, 0.08);
  transition: background 0.2s, transform 0.15s;
}

.skill-card:hover {
  background: #fff3e0;
  /* transform: scale(1.02); */
}

a {
  text-decoration: none;
  color: var(--color-text-dark);
}
</style>
