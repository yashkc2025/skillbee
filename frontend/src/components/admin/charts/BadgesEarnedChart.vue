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
]);

const chartRef = ref<ECRef>();

onMounted(() => {
  nextTick(() => {
    chartRef.value?.resize();
  });
});

// Toggle this to switch between grouped and stacked view
const isStacked = true;

const option = ref({
  textStyle: {
    fontFamily: 'DMSans',
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' },
  },
  legend: {
    bottom: 0,
    icon: 'circle',
    itemGap: 20,
  },
  xAxis: {
    type: 'category',
    data: ['Math Whiz', 'Reading Star', 'Science Explorer', 'Art Champ', 'Sports Hero'],
    axisTick: { alignWithLabel: true }
  },
  yAxis: {
    type: 'value'
  },
  grid: {
    top: 10,
    bottom: 30,
    left: 10,
    right: 20,
    containLabel: true
  },
  series: [
    {
      name: 'Age 8-10',
      type: 'bar',
      stack: isStacked ? 'age' : undefined,
      data: [20, 35, 30, 40, 25],
      barGap: 0,
    },
    {
      name: 'Age 10-12',
      type: 'bar',
      stack: isStacked ? 'age' : undefined,
      data: [30, 25, 35, 20, 30],
    },
    {
      name: 'Age 12-14',
      type: 'bar',
      stack: isStacked ? 'age' : undefined,
      data: [25, 30, 20, 35, 40],
    }
  ]
});
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
