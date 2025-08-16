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
  DatasetComponent,
  ToolboxComponent,
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
  DatasetComponent,
  ToolboxComponent,
]);
type AgeGroupData = {
  age_8_10: number;
  age_10_12: number;
  age_12_14: number;
};

type SkillData = {
  skill_id: string;
  skill_name: string;
  lesson_completed_count: AgeGroupData;
  lesson_started_count: AgeGroupData;
  quiz_attempted_count: AgeGroupData;
};

type TransformedSkillData = {
  skill_name: string[];
  total_lesson_completed_count: number[];
  total_lesson_started_count: number[];
  total_quiz_attempted_count: number[];
};

function transformSkillData(data: SkillData[]): TransformedSkillData {
  const joinedData = data.map((skill) => {
    const sum = (group: AgeGroupData): number =>
      group.age_8_10 + group.age_10_12 + group.age_12_14;

    return {
      skill_name: skill.skill_name,
      total_lesson_completed_count: sum(skill.lesson_completed_count),
      total_lesson_started_count: sum(skill.lesson_started_count),
      total_quiz_attempted_count: sum(skill.quiz_attempted_count),
    };
  });

  return {
    skill_name: joinedData.map((x) => x.skill_name),
    total_lesson_completed_count: joinedData.map((x) => x.total_lesson_completed_count),
    total_lesson_started_count: joinedData.map((x) => x.total_lesson_started_count),
    total_quiz_attempted_count: joinedData.map((x) => x.total_quiz_attempted_count),
  };
}

const chartRef = ref<ECRef>();
const chartData = ref<TransformedSkillData>();
const option = ref();

onMounted(async () => {
  const data = await fetchData(getBackendURL("admin/age_distribution_chart"));
  if (data) {
    chartData.value = transformSkillData(data);
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
          rotate: 40,
          textStyle: {
            fontSize: 10, // change this value as needed
          },
        },
      },
      yAxis: {
        type: "value",
        name: "Count",
      },
      series: [
        {
          name: "Lessons Started",
          type: "bar",
          data: chartData.value.total_lesson_started_count,
          barGap: 0,
        },
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
