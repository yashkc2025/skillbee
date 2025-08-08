<template>
  <div class="chart-wrapper">
    <v-chart ref="chartRef" class="chart" :option="options" autoresize />
  </div>
</template>

<script setup lang="ts">
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { FunnelChart } from "echarts/charts";
import { TooltipComponent, TitleComponent, LegendComponent } from "echarts/components";
import VChart from "vue-echarts";
import { ref, onMounted, nextTick } from "vue";
import type { ECRef } from "vue-echarts";
import { fetchData } from "@/fx/api";
import { getBackendURL } from "@/fx/utils";

use([CanvasRenderer, FunnelChart, TooltipComponent, TitleComponent, LegendComponent]);

interface DataFormat {
  badges_earned: number;
  lessons_completed: number;
  quizzes_attempted: number;
  user_started_skill: number;
}

const chartRef = ref<ECRef>();
const chartData = ref<DataFormat>();
const options = ref();

onMounted(async () => {
  const data = await fetchData(getBackendURL("admin/learning_funnel_chart")).then(
    (r) => r[0]
  );

  if (
    data &&
    typeof data.user_started_skill === "number" &&
    typeof data.lessons_completed === "number" &&
    typeof data.quizzes_attempted === "number" &&
    typeof data.badges_earned === "number"
  ) {
    chartData.value = data;

    options.value = {
      textStyle: {
        fontFamily: "DMSans",
      },
      tooltip: {
        trigger: "item",
        formatter: ({ name, value, percent }: any) => `${name}: ${value} (${percent}%)`,
      },
      legend: {
        bottom: 0,
      },
      series: [
        {
          name: "Learning Funnel",
          type: "funnel",
          left: "10%",
          top: 20,
          bottom: 40,
          width: "80%",
          min: 0,
          max: 500,
          minSize: "30%",
          maxSize: "100%",
          sort: "descending",
          gap: 5,
          label: {
            show: true,
            position: "inside",
            formatter: "{b}\n{c}",
            fontWeight: "bold",
          },
          itemStyle: {
            borderColor: "#fff",
            borderWidth: 2,
          },
          emphasis: {
            label: {
              fontSize: 16,
            },
          },
          data: [
            { value: data.user_started_skill, name: "Users Started Skill" },
            { value: data.lessons_completed, name: "Lessons Completed" },
            { value: data.quizzes_attempted, name: "Quizzes Attempted" },
            { value: data.badges_earned, name: "Badges Earned" },
          ],
        },
      ],
    };

    await nextTick();
    chartRef.value?.resize();
  } else {
    console.error("Invalid data from API", data);
  }
});
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 350px;
  position: relative;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
