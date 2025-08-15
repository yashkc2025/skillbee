<template>
  <div class="chart-wrapper">
    <v-chart ref="chartRef" class="chart" :option="option" autoresize />
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  childId: string;
}>();

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
import { install$5 } from "echarts/types/dist/shared";
import { watch } from "vue";
import type { ProfileType } from "@/views/admin/ChildrenProfile.vue";
import { fetchData } from "@/fx/api";
import { getBackendURL } from "@/fx/utils";

use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
]);

const chartRef = ref<ECRef>();
const chartData = ref();
const option = ref();

console.log(props.childId);

onMounted(async () => {
  const data: ProfileType = await fetchData(getBackendURL("children/profile"), {
    id: props.childId,
  });
  if (data) {
    chartData.value = {
      point: data.point_earned.map((p) => p.point) ?? [],
      dates: data.point_earned.map((p) => p.date) ?? [],
    };

    option.value = {
      textStyle: {
        fontFamily: "DMSans",
      },
      tooltip: { trigger: "axis" },
      legend: {
        // data: ['Direct', 'Email', 'Ad Networks', 'Video Ads', 'Search Engines'],
        bottom: 0,
        icon: "circle",
        itemGap: 20,
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: chartData.value.dates,
      },
      yAxis: { type: "value" },
      series: [
        {
          name: "Points ",
          type: "line",
          data: chartData.value.point,
          smooth: false,
        },
      ],
      grid: {
        top: 10,
        bottom: 30, // increased for x-axis labels
        left: 10, // small padding
        right: 35, // allows space for last label
        containLabel: true,
      },
    };
    await nextTick();
    chartRef.value?.resize();
  }
});
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 250px;
  position: relative;
}

.chart {
  max-width: 100%;
  height: 100%;
  display: block;
}
</style>
