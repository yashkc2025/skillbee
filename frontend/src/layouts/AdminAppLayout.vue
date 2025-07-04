<script setup lang="ts">
import AdminNavbar from "@/components/admin/AdminNavbar.vue";
import sitemap from "@/router/sitemap.json";

const navOptions = [
  {
    heading: "",
    items: [
      {
        label: "Dashboard",
        icon: "bi bi-house",
        link: sitemap.admin.dashboard,
      },
    ],
  },
  {
    heading: "Analytics",
    items: [
      {
        label: "Performance",
        icon: "bi bi-bar-chart",
        link: sitemap.admin.analytics.performance,
      },
      {
        label: "Feedbacks",
        icon: "bi bi-journal-text",
        link: sitemap.admin.analytics.feedback,
      },
    ],
  },
  {
    heading: "Curriculum",
    items: [
      {
        label: "Lessons",
        icon: "bi bi-journal-bookmark",
        link: sitemap.admin.curriculum.lessons,
      },
      {
        label: "Quiz",
        icon: "bi bi-patch-question",
        link: sitemap.admin.curriculum.quiz,
      },
      {
        label: "Activities",
        icon: "bi bi-check2-square",
        link: sitemap.admin.curriculum.activities,
      },
      {
        label: "Badges",
        icon: "bi bi-patch-check",
        link: sitemap.admin.curriculum.badges,
      },
    ],
  },
  {
    heading: "",
    items: [
      {
        label: "Manage Users",
        icon: "bi bi-people",
        link: sitemap.admin.user_management,
      },
      {
        label: "Settings",
        icon: "bi bi-gear",
        link: sitemap.admin.settings,
      },
    ],
  },
];
</script>

<template>
  <main class="admin-layout">
    <AdminNavbar />
    <div class="content">
      <slot></slot>
    </div>
  </main>
</template>

<style scoped>
.admin-layout {
  font-family: "DMSans";
  width: 100%;
  height: 100%;
  display: flex;
  background-color: green;
  overflow: hidden;
}

.content {
  padding: var(--size-md);
  flex: 70%;
  height: 100vh;
  background-color: var(--color-background);
  overflow: scroll;
  overflow-x: hidden;
}
</style>
