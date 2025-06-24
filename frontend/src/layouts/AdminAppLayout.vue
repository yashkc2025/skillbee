<script setup lang="ts">
import sitemap from "@/router/sitemap.json";

const navOptions = [
  {
    heading: "",
    items: [
      {
        label: "Dashboard",
        image: "",
        link: sitemap.admin.dashboard,
      },
    ],
  },
  {
    heading: "Analytics",
    items: [
      {
        label: "Performance",
        image: "",
        link: sitemap.admin.analytics.performance,
      },
      {
        label: "Feedbacks",
        image: "",
        link: sitemap.admin.analytics.feedback,
      },
    ],
  },
  {
    heading: "Curriculum",
    items: [
      {
        label: "Lessons",
        image: "",
        link: sitemap.admin.curriculum.lessons
      },
      {
        label: "Quiz",
        image: "",
        link: sitemap.admin.curriculum.quiz
      },
      {
        label: "Activities",
        image: "",
        link: sitemap.admin.curriculum.activities
      },
      {
        label: "Badges",
        image: "",
        link: sitemap.admin.curriculum.badges
      }
    ]
  },
  {
    heading: "",
    items: [
      {
        label: "Manage Users",
        image: "",
        link: sitemap.admin.user_management
      },
      {
        label: "Settings",
        image: "",
        link: sitemap.admin.settings
      }
    ]
  }
];
</script>

<template>
  <main class="admin-layout">
    <div class="navbar">w</div>
    <div class="content"></div>
  </main>
</template>

<style scoped>
.admin-layout {
  width: 100%;
  height: 100%;
  display: flex;
  background-color: green;
}

.navbar {
  width: 20rem;
  height: 100vh;
  background-color: pink;
}

.content {
  flex: 70%;
  min-height: 100vh;
  background-color: white;
}
</style>
