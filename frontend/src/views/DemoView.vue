<script setup lang="ts">
import AdminNavbar from "@/components/admin/AdminNavbar.vue";
import ChildNavbar from "@/components/child/ChildNavbar.vue";
</script>

<template>
  <main>
    <ChildNavbar />
    <AdminNavbar />
  </main>
</template>

<style scoped>
main {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  gap: 20px;
  flex-direction: column;
}
</style>
