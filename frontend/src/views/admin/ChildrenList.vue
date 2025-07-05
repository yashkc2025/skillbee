<script setup lang="ts">
import ChildrenTable from '@/components/admin/dashboard/ChildrenTable.vue';
import AdminAppLayout from '@/layouts/AdminAppLayout.vue';
</script>

<template>
  <AdminAppLayout>
    <p class="intro">
      <span class="darken">Manage Children</span>
    </p>
    <ChildrenTable />
  </AdminAppLayout>
</template>

<style scoped>
.intro {
  margin-bottom: 20px;
}
</style>
