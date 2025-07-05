<template>
  <div class="chart-wrapper">
    <v-chart ref="chartRef" class="chart" :option="option" autoresize />
  </div>
</template>

<script setup lang="ts">
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  ToolboxComponent
} from 'echarts/components';
import VChart from 'vue-echarts';
import { ref, onMounted, nextTick } from 'vue';
import type { ECRef } from 'vue-echarts';

use([
  CanvasRenderer,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  ToolboxComponent
]);

const chartRef = ref<ECRef>();

onMounted(() => {
  nextTick(() => {
    chartRef.value?.resize();
  });
});

// Top 5 skills
const skills = ['Critical Thinking', 'Communication Skills', 'Time Management', 'Extracurricular Activities', 'Financial Literacy'];

const option = ref({
  textStyle: {
    fontFamily: 'DMSans',
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  legend: {
    bottom: 0,
    icon: 'circle',
    itemGap: 20,

  },
  xAxis: {
    type: 'category',
    data: skills,
    axisLabel: {
      interval: 0,      // show all labels, no skipping
      rotate: 5
    }
  },
  yAxis: {
    type: 'value',
    name: 'Count'
  },
  series: [
    {
      name: 'Lessons Started',
      type: 'bar',
      data: [120, 90, 150, 80, 110],
      barGap: 0
    },
    {
      name: 'Lessons Completed',
      type: 'bar',
      data: [100, 70, 130, 60, 90]
    },
    {
      name: 'Quizzes Attempted',
      type: 'bar',
      data: [80, 60, 110, 40, 70]
    }
  ],
  grid: {
    left: 10,
    right: 10,
    bottom: 30,
    top: 10,
    containLabel: true
  },
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
