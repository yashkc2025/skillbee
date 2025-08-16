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
import { BarChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  ToolboxComponent,
} from "echarts/components";
import VChart from "vue-echarts";
import { ref, onMounted, nextTick } from "vue";
import type { ECRef } from "vue-echarts";
import { fetchData } from "@/fx/api";
import { getBackendURL } from "@/fx/utils";
import type { ProfileType } from "@/views/admin/ChildrenProfile.vue";

use([
  CanvasRenderer,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  ToolboxComponent,
]);

type SkillData = {
  skill_id: string;
  skill_name: string;
  lesson_completed_count: number;
  lesson_started_count: number;
  quiz_attempted_count: number;
};

type TransformedSkillData = {
  skill_name: string[];
  total_lesson_completed_count: number[];
  total_lesson_started_count: number[];
  total_quiz_attempted_count: number[];
};

function transformSkillData(data: SkillData[]): TransformedSkillData {
  const joinedData = data;

  return {
    skill_name: joinedData.map((x) => x.skill_name),
    total_lesson_completed_count: joinedData.map((x) => x.lesson_completed_count),
    total_lesson_started_count: joinedData.map((x) => x.lesson_started_count),
    total_quiz_attempted_count: joinedData.map((x) => x.quiz_attempted_count),
  };
}

const chartRef = ref<ECRef>();
const chartData = ref<TransformedSkillData>();
const option = ref();

onMounted(async () => {
  const data: ProfileType = await fetchData(getBackendURL("children/profile"), {
    id: props.childId,
  });
  if (data) {
    chartData.value = transformSkillData(data.skills_progress);
    option.value = {
      textStyle: {
        fontFamily: "DMSans",
      },
      tooltip: {
        trigger: "axis",
        axisPointer: {
          type: "shadow",
        },
      },
      legend: {
        bottom: 0,
        icon: "circle",
        itemGap: 20,
      },
      xAxis: {
        type: "category",
        data: chartData.value.skill_name,
        axisLabel: {
          interval: 0, // show all labels, no skipping
          rotate: 30,
        },
      },
      yAxis: {
        type: "value",
        name: "Count",
      },
      series: [
        // {
        //   name: "Lessons Started",
        //   type: "bar",
        //   data: chartData.value.total_lesson_started_count,
        //   barGap: 0,
        // },
        {
          name: "Lessons Completed",
          type: "bar",
          data: chartData.value.total_lesson_completed_count,
        },
        {
          name: "Quizzes Attempted",
          type: "bar",
          data: chartData.value.total_quiz_attempted_count,
        },
      ],
      grid: {
        left: 10,
        right: 10,
        bottom: 30,
        top: 10,
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
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
