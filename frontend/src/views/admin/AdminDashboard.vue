<script setup lang="ts">
import AdminAppLayout from "@/layouts/AdminAppLayout.vue";
import ChildrenTable from "@/components/admin/dashboard/ChildrenTable.vue"
import ParentTable from "@/components/admin/dashboard/ParentTable.vue";
import ActiveUserChart from "@/components/admin/charts/ActiveUserChart.vue";
import CardV2 from "@/components/CardV2.vue";
import SkillChart from "@/components/admin/charts/SkillChart.vue";
</script>

<template>
  <AdminAppLayout>
    <div class="dashboard">
      <p class="intro">
        <span class="darken">Hello Admin - </span> here's what has been happening with
        your app
      </p>
      <div class="top-charts">
        <CardV2 class="first-chart" label-image="bi bi-people" label-title="Active users">
          <template #content>
            <ActiveUserChart />
          </template>
        </CardV2>
        <CardV2 class="second-chart" label-image="bi bi-journals" label-title="Skill Engagement">
          <template #content>
            <SkillChart />
          </template>
        </CardV2>
      </div>
      <ChildrenTable :show-expand="true" :max-items="5" />
      <ParentTable :show-expand="true" :max-items="5" />
    </div>
  </AdminAppLayout>
</template>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: var(--size-sm);
}

.top-charts {
  display: flex;
  gap: var(--size-sm);
  /* flex-wrap: wrap; */
}

.first-chart {
  flex: 60%;
}

.second-chart {
  flex: 50%
}
</style>
