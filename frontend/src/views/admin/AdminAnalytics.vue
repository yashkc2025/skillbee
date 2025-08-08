<script setup lang="ts">
import ActiveUserChart from "@/components/admin/charts/ActiveUserChart.vue";
import SkillChart from "@/components/admin/charts/SkillChart.vue";
import BadgesEarnedChart from "@/components/admin/charts/BadgesEarnedChart.vue";
import UserFunnelChart from "@/components/admin/charts/UserFunnelChart.vue";
import SegmentPieChart from "@/components/admin/charts/SegmentPieChart.vue";
import CardV2 from "@/components/CardV2.vue";
import AdminAppLayout from "@/layouts/AdminAppLayout.vue";
</script>

<template>
  <AdminAppLayout>
    <div class="outer">
      <div class="top-charts">
        <CardV2 class="first-chart" label-image="bi bi-people" label-title="Active users">
          <template #content>
            <ActiveUserChart />
          </template>
        </CardV2>
        <CardV2
          class="second-chart"
          label-image="bi bi-pie-chart"
          label-title="Age Group Distribution of Users"
        >
          <template #content>
            <SegmentPieChart />
          </template>
        </CardV2>
      </div>
      <div class="top-charts">
        <CardV2
          class="first-chart"
          label-image="bi bi-stars"
          label-title="Badges Earned by Age Groups"
        >
          <template #content>
            <BadgesEarnedChart />
          </template>
        </CardV2>
        <CardV2
          class="second-chart"
          label-image="bi bi-funnel"
          label-title="Learning Funnel"
        >
          <template #content>
            <UserFunnelChart />
          </template>
        </CardV2>
      </div>
      <div class="top-charts">
        <CardV2
          class="wide-chart"
          label-image="bi bi-people"
          label-title="Skill Engagement"
        >
          <template #content>
            <SkillChart />
          </template>
        </CardV2>
      </div>
    </div>
  </AdminAppLayout>
</template>

<style scoped>
.outer {
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
  flex: 50%;
}

.second-chart {
  flex: 50%;
}

.wide-chart {
  width: 100%;
}
</style>
