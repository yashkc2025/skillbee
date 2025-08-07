<template>
  <div class="chart-wrapper">
    <v-chart ref="chartRef" class="chart" :option="option" autoresize />
  </div>
</template>

<script setup lang="ts">
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart } from "echarts/charts";
import { TooltipComponent, LegendComponent, TitleComponent } from "echarts/components";
import VChart from "vue-echarts";
import { ref, onMounted, nextTick } from "vue";
import type { ECRef } from "vue-echarts";
import { fetchData } from "@/fx/api";
import { getBackendURL } from "@/fx/utils";

use([CanvasRenderer, PieChart, TooltipComponent, LegendComponent, TitleComponent]);
interface DataFormat {
  age_10_12: number;
  age_12_14: number;
  age_8_10: number;
}
const chartRef = ref<ECRef>();
const chartData = ref<DataFormat>();

onMounted(async () => {
  const data = await fetchData(getBackendURL("age_group_chart"));
  if (data) {
    chartData.value = data;
    option.value = {
      textStyle: {
        fontFamily: "DMSans",
      },
      tooltip: {
        trigger: "item",
        formatter: "{b}: {c} users ({d}%)",
      },
      legend: {
        bottom: 0,
        icon: "circle",
        itemGap: 20,
      },
      series: [
        {
          name: "User Segmentation",
          type: "pie",
          radius: ["40%", "70%"], // donut shape
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 5,
            borderColor: "#fff",
            borderWidth: 2,
          },
          label: {
            show: true,
            position: "inside",
            formatter: "{d}%",
            fontSize: 12,
            fontWeight: "bold",
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 14,
              fontWeight: "bold",
            },
          },
          labelLine: {
            show: false,
          },
          data: [
            { value: chartData.value?.age_8_10, name: "Age 8-10" },
            { value: chartData.value?.age_10_12, name: "Age 10-12" },
            { value: chartData.value?.age_12_14, name: "Age 12-14" },
          ],
        },
      ],
    };
    await nextTick();
    chartRef.value?.resize();
  }
});

const option = ref();
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 200px;
  position: relative;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
