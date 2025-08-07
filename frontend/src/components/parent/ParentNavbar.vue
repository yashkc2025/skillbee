<script setup lang="ts">
import sitemap from "../../router/sitemap.json";
import { useRouter } from "vue-router";
import { logout } from "../../fx/utils";

const router = useRouter()

const navOptions = [
  // {
  //   label: "Dashboard",
  //   link: sitemap.parent.dashboard,
  // },
  {
    label: "Settings",
    link: sitemap.parent.settings,
  },
];
</script>

<template>
  <div class="navbar box-shadow">
    <section class="logo-parent">
      <img src="/logo.png" alt="" @click="router.push(sitemap.parent.dashboard)" />
    </section>
    <section class="items-parent">
      <a :href="n.link" class="nav-items" v-for="n in navOptions" :key="n.label">{{
        n.label
        }}</a>
      <a class="danger" href="/" @click="logout">Logout</a>
    </section>
    <!-- <section class="third-parent">
    </section> -->
  </div>
</template>

<style scoped>
.navbar {
  padding: var(--size-2xs) var(--size-md);
  border: 1px solid var(--color-border);
  border-radius: 30px;
  display: flex;
  flex-direction: row;
  background-color: var(--color-text-light);
  gap: var(--size-xl);
  min-width: 800px;
  justify-content: space-between;
}

.items-parent,
.third-parent {
  display: flex;
  flex-direction: row;
  gap: 10px;
}

a {
  color: var(--color-text-dark);
  padding: var(--size-2xs) var(--size-xs);
  border-radius: calc(var(--border-radius) / 2);
  font-size: var(--font-sm);
  /* border-radius: var(--border-radius); */
  border: 1px solid none;
  font-family: "VAGRoundedNext";
  font-weight: 400;
  text-decoration: none;
}

a:hover {
  background-color: var(--color-hover);
  border-color: var(--color-border);
}

.logo-parent {
  display: flex;
  justify-content: center;
  align-items: center;
}

img {
  width: 90px;
  padding: var(--size-2xs) var(--size-xs);
}

.danger {
  color: var(--color-pink);
}
</style>
