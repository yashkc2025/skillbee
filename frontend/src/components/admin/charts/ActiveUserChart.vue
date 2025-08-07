<template>
  <div class="chart-wrapper">
    <v-chart ref="chartRef" class="chart" :option="option" autoresize />
  </div>
</template>

<script setup lang="ts">
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { LineChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from "echarts/components";
import VChart from "vue-echarts";
import { ref, onMounted, nextTick } from "vue";
import type { ECRef } from "vue-echarts";
import { fetchData } from "@/fx/api";
import { getBackendURL } from "@/fx/utils";

interface DataFormat {
  active_children: number[];
  active_parents: number[];
  dates: string[];
  new_children_signups: number[];
  new_parent_signups: number[];
  total_active_users: number[];
}

use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
]);

const chartRef = ref<ECRef>();
const chartData = ref<DataFormat>();
const option = ref(); // initialize empty

onMounted(async () => {
  chartData.value = await fetchData(getBackendURL("admin/active_users_chart"));

  option.value = {
    textStyle: {
      fontFamily: "DMSans",
    },
    tooltip: { trigger: "axis" },
    legend: {
      bottom: 0,
      icon: "circle",
      itemGap: 20,
    },
    xAxis: {
      type: "category",
      boundaryGap: false,
      data: chartData.value?.dates,
    },
    yAxis: { type: "value" },
    series: [
      {
        name: "Active Children",
        type: "line",
        data: chartData.value?.active_children,
        smooth: true,
      },
      {
        name: "Active Parents",
        type: "line",
        data: chartData.value?.active_parents,
        smooth: true,
      },
      {
        name: "New Children Signups",
        type: "line",
        data: chartData.value?.new_children_signups,
        smooth: true,
      },
      {
        name: "New Parents Signups",
        type: "line",
        data: chartData.value?.new_parent_signups,
        smooth: true,
      },
      {
        name: "Total Active Users",
        type: "line",
        data: chartData.value?.total_active_users,
        smooth: true,
      },
    ],
    grid: {
      top: 10,
      bottom: 30,
      left: 10,
      right: 35,
      containLabel: true,
    },
  };

  await nextTick();
  chartRef.value?.resize();
});
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 250px;
  position: relative;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
