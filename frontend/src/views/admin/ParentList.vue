<script setup lang="ts">
import ParentTable from '@/components/admin/dashboard/ParentTable.vue';
import AdminAppLayout from '@/layouts/AdminAppLayout.vue';
</script>

<template>
  <AdminAppLayout>
    <p class="intro">
      <span class="darken">Manage Parent</span>
    </p>
    <ParentTable />
  </AdminAppLayout>
</template>

<style scoped>
.intro {
  margin-bottom: 20px;
}
</style>
