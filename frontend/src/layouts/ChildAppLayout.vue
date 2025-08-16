<script setup lang="ts">
import ChildNavbar from "@/components/child/ChildNavbar.vue";
import { onMounted } from "vue";
import { getBackendURL, logout } from "../fx/utils";
import { fetchData } from "../fx/api";

onMounted(async () => {
  const userData = await fetchData(getBackendURL("auth/get_user"));

  if (userData) {
    console.log(userData);
    if (userData.user.role !== "child") {
      logout();
    }
  }
});
</script>

<template>
  <main>
    <div class="navbar-parent">
      <ChildNavbar />
    </div>
    <div class="app-layout">
      <div>
        <slot></slot>
      </div>
    </div>
  </main>
</template>

<style scoped>
.navbar-parent {
  position: fixed;
  top: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  /* padding-top: var(--size-sm); */
  z-index: 1000;
}

.app-layout {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.app-layout > div {
  /* background-color: blue; */
  /* max-width: 1200px; */
  width: 100%;
  margin-top: var(--size-4xl);
  padding: 0 1rem;
}
</style>
