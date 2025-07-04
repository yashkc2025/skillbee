<script setup lang="ts">
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
      // {
      //   label: "Feedbacks",
      //   icon: "bi bi-journal-text",
      //   link: sitemap.admin.analytics.feedback,
      // },
    ],
  },
  {
    heading: "Curriculum",
    items: [
      {
        label: "Lessons",
        icon: "bi bi-book",
        link: sitemap.admin.curriculum.lessons,
      },
      {
        label: "Quiz",
        icon: "bi bi-patch-question",
        link: sitemap.admin.curriculum.quiz,
      },
      {
        label: "Activities",
        icon: "bi bi-pen",
        link: sitemap.admin.curriculum.activities,
      },
      {
        label: "Badges",
        icon: "bi bi-stars",
        link: sitemap.admin.curriculum.badges,
      },
    ],
  },
  {
    heading: "Miscellanous",
    items: [
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
  <div class="navbar">
    <section class="logo-parent">
      <img src="/logo.png" alt="" />
      <span>Admin</span>
    </section>
    <div class="navbar-content">
      <!-- <a :href="sitemap.admin.new.all" class="create">
        <i class="bi bi-plus-lg"></i>
        <span>Create something</span>
      </a> -->
      <div class="navbar-section" v-for="section in navOptions" :key="section.heading">
        <p v-if="section.heading !== ''">{{ section.heading }}</p>
        <a :href="item.link" v-for="item in section.items" :key="item.label" class="navbar-item">
          <i :class="item.icon" class="nav-icon chip"></i>
          <span>{{ item.label }}</span>
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.logo-parent {
  display: flex;
  align-items: center;
  /* justify-content: center; */
  gap: var(--size-xs);
  padding: var(--size-sm) var(--size-md);
  border-bottom: 1px solid var(--color-border);
}

.logo-parent>span {
  font-weight: 600;
  font-family: "Inter";
  font-size: 20px;
}

.logo-parent>img {
  width: 20px;
}

.create {
  display: inline-flex;
  align-items: center;
  width: auto;
  align-self: flex-start;

  text-decoration: none;
  background-color: var(--accent-admin);

  padding: var(--size-xs) var(--size-xs);
  border-radius: var(--border-radius);
  gap: var(--size-2xs);
}

.create>span,
.create>i {
  color: var(--color-text-light);
  font-size: var(--font-sm);
}

.navbar {
  max-width: 15rem;
  height: 100vh;
  background-color: var(--color-background);
  display: flex;
  flex-direction: column;
  gap: var(--size-md);
  /* padding: var(--size-md); */
  /* padding-top: 0px; */
}

.navbar-content {
  width: 20rem;
  height: 100vh;
  background-color: var(--color-background);
  display: flex;
  flex-direction: column;
  gap: var(--size-md);
  padding: var(--size-md);
  padding-top: 0px;
}

.navbar-section>p {
  margin-bottom: var(--size-sm);
  text-transform: uppercase;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-heading-2);
}

.navbar-section {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: var(--size-xs);
}

.navbar-section>a {
  text-decoration: none;
  color: var(--color-text-dark);
}

span {
  font-size: var(--size-sm);
  font-weight: 500;
}

.navbar-item {
  font-weight: 600;
  display: flex;
  flex-direction: row;
  gap: var(--size-xs);
}

.nav-icon {
  font-size: 13px;
}
</style>
