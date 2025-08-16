<script setup lang="ts">
import AdminNavbar from "@/components/admin/AdminNavbar.vue";
import { onMounted } from "vue";
import { fetchData } from "../fx/api";
import { getBackendURL, logout } from "../fx/utils";

onMounted(async () => {
  const userData = await fetchData(getBackendURL("auth/get_user"));
  if (userData) {
    console.log(userData);
    if (userData.user.role !== "admin") {
      logout();
    }
  }
});
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
