<template>
  <div class="chart-wrapper">
    <v-chart ref="chartRef" class="chart" :option="option" autoresize />
  </div>
</template>

<script setup lang="ts">
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart } from "echarts/charts";
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

use([
  CanvasRenderer,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
]);

type InputItem = {
  age_10_12: number;
  age_12_14: number;
  age_8_10: number;
  badge_name: string;
};

type Output = {
  badge_names: string[];
  age_10_12: number[];
  age_12_14: number[];
  age_8_10: number[];
};

function transformData(data: InputItem[]): Output {
  const output: Output = {
    badge_names: [],
    age_10_12: [],
    age_12_14: [],
    age_8_10: [],
  };

  for (const item of data) {
    output.badge_names.push(item.badge_name);
    output.age_10_12.push(item.age_10_12);
    output.age_12_14.push(item.age_12_14);
    output.age_8_10.push(item.age_8_10);
  }

  return output;
}

const chartRef = ref<ECRef>();
const chartData = ref<Output>();
const option = ref();

onMounted(async () => {
  const data = await fetchData(getBackendURL("admin/badge_by_age_group_chart"));

  if (data) {
    chartData.value = transformData(data);
    option.value = {
      textStyle: {
        fontFamily: "DMSans",
      },
      tooltip: {
        trigger: "axis",
        axisPointer: { type: "shadow" },
      },
      legend: {
        bottom: 0,
        icon: "circle",
        itemGap: 20,
      },
      xAxis: {
        type: "category",
        data: chartData.value.badge_names,
        axisTick: { alignWithLabel: true },
      },
      yAxis: {
        type: "value",
      },
      grid: {
        top: 10,
        bottom: 30,
        left: 10,
        right: 20,
        containLabel: true,
      },
      series: [
        {
          name: "Age 8-10",
          type: "bar",
          stack: isStacked ? "age" : undefined,
          barGap: 0,
          data: chartData.value.age_8_10,
        },
        {
          name: "Age 10-12",
          type: "bar",
          stack: isStacked ? "age" : undefined,
          data: chartData.value.age_10_12,
        },
        {
          name: "Age 12-14",
          type: "bar",
          stack: isStacked ? "age" : undefined,
          data: chartData.value.age_12_14,
        },
      ],
    };
    await nextTick();
    chartRef.value?.resize();
  }
});

// Toggle this to switch between grouped and stacked view
const isStacked = true;
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 300px;
  position: relative;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
