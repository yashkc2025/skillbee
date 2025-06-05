<script setup lang="ts">
import sitemap from "../../router/sitemap.json";

const navOptions = [
  {
    label: "Dashboard",
    link: sitemap.child_app.dashboard,
  },
  // {
  //   label: "Achievements",
  //   link: sitemap.child_app.achievements,
  // },
  {
    label: "Settings",
    link: sitemap.child_app.settings,
  },
  {
    label: "Create",
    link: sitemap.child_app.lessons,
  },
];
</script>

<template>
  <div class="navbar">
    <section class="logo-parent">
      <img src="/logo.png" alt="" />
    </section>
    <section class="items-parent">
      <a :href="n.link" class="nav-items" v-for="n in navOptions" :key="n.label">{{
        n.label
        }}</a>
    </section>
    <section class="third-parent">
      <a class="danger" href="">Logout</a>
    </section>
  </div>
</template>

<style scoped>
.navbar {
  padding: var(--size-2xs) var(--size-md);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  display: flex;
  flex-direction: row;
  background-color: var(--color-text-light);
  box-shadow: 0 8px 32px var(--color-border);
  gap: var(--size-xl);
}

.items-parent,
.third-parent {
  display: flex;
  flex-direction: row;
  gap: 10px;
}

a {
  color: var(--color-text-dark);
  text-decoration: none;
  padding: var(--size-2xs) var(--size-xs);
  border-radius: calc(var(--border-radius) / 2);
  font-size: var(--font-sm);
  /* border-radius: var(--border-radius); */
  border: 1px solid none;
  font-family: "VAGRoundedNext";
  font-weight: 400;
}

a:hover {
  background-color: var(--color-background);
  border-color: var(--color-border);
}

.logo-parent {
  display: flex;
  justify-content: center;
  align-items: center;
}

img {
  width: 35px;
  padding: var(--size-2xs) var(--size-xs);
}

.danger {
  color: var(--color-pink);
}
</style>
