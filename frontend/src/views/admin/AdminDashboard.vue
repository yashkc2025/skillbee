<script setup lang="ts">
import Card from "@/components/Card.vue";
import SkillTemplate from "@/components/child/dashboard/SkillTemplate.vue";
import AdminAppLayout from "@/layouts/AdminAppLayout.vue";

const skillTypes = [
  { label: "🧠 Critical Thinking", link: "", progress: 10 },
  { label: "💬 Communication Skills", link: "", progress: 30 },
  { label: "⏰ Time Management", link: "", progress: 56 },
  { label: "🎵 Extracurricular Activities", link: "", progress: 18 },
  { label: "💰 Financial Literacy", link: "", progress: 78 },
];
</script>
<template>
  <AdminAppLayout>
    <div class="dashboard">
      <p class="intro">
        <span class="darken">Hello Admin - </span> here's what has been happening with
        your app
      </p>
      <div class="group">
        <div class="three"></div>
        <div class="four"></div>
      </div>
      <div class="one"></div>
      <div class="group">
        <div class="four"></div>
        <div class="three"></div>
      </div>
    </div>
  </AdminAppLayout>
</template>

<style scoped>
.darken {
  font-weight: bold;
}

.dashboard {
  display: flex;
  flex-direction: column;
  gap: var(--size-md);
}

.one {
  width: 100%;
  height: 300px;
}

.group {
  display: flex;
  flex-direction: row;
  gap: var(--size-md);
}

.three {
  flex: 70%;
  width: 100%;
  height: 300px;
}

.four {
  width: 100%;
  height: 300px;
  flex: 30%;
}

.one,
.three,
.four {
  border: 1px solid var(--color-border);
  background-color: var(--color-light);
  border-radius: var(--border-radius);
}
</style>
