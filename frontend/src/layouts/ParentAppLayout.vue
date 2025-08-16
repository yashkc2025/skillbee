<script setup lang="ts">
import ParentNavbar from "@/components/parent/ParentNavbar.vue";
import { onMounted } from "vue";
import { fetchData } from "../fx/api";
import { getBackendURL, logout } from "../fx/utils";

onMounted(async () => {
  const userData = await fetchData(getBackendURL("auth/get_user"));
  if (userData) {
    console.log(userData);
    if (userData.user.role !== "parent") {
      logout();
    }
  }
});
</script>

<template>
  <main>
    <div class="navbar-parent">
      <ParentNavbar />
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
  position: absolute;
  top: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: var(--size-sm);
}

.app-layout {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: "DMSans";
}

.app-layout > div {
  /* background-color: blue; */
  /* max-width: 1200px; */
  width: 100%;
  margin-top: var(--size-4xl);
  padding: 0 1rem;
}
</style>
