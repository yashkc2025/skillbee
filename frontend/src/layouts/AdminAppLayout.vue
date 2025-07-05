<script setup lang="ts">
import AdminNavbar from "@/components/admin/AdminNavbar.vue";
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
