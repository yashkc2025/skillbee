<template>
  <div class="chart-wrapper">
    <v-chart ref="chartRef" class="chart" :option="option" autoresize />
  </div>
</template>

<script setup lang="ts">
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { LineChart } from 'echarts/charts';
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
  LineChart,
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

const option = ref({
  textStyle: {
    fontFamily: 'DMSans',
  },
  tooltip: { trigger: 'axis' },
  legend: {
    // data: ['Direct', 'Email', 'Ad Networks', 'Video Ads', 'Search Engines'],
    bottom: 0,
    icon: 'circle',
    itemGap: 20,
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: [
      '2025-02-15', '2025-02-16', '2025-02-17', '2025-02-18', '2025-02-19',
      '2025-02-20', '2025-02-21', '2025-02-22', '2025-02-23', '2025-02-24',
      '2025-02-25', '2025-02-26', '2025-02-27', '2025-02-28', '2025-03-01',
      '2025-03-02'
    ]
  },
  yAxis: { type: 'value' },
  series: [
    {
      name: 'Active Children',
      type: 'line',
      data: [42, 45, 40, 38, 43, 50, 48, 51, 47, 45, 49, 52, 50, 46, 48, 47],
      smooth: true,
      barGap: 0,
    },
    {
      name: 'Active Parents',
      type: 'line',
      data: [30, 32, 34, 33, 35, 38, 36, 39, 37, 36, 38, 40, 41, 39, 38, 37],
      smooth: true
    },
    {
      name: 'New Children Signups',
      type: 'line',
      data: [5, 7, 6, 4, 8, 10, 9, 7, 6, 5, 7, 6, 8, 6, 5, 7],
      smooth: true
    },
    {
      name: 'New Parents Signups',
      type: 'line',
      data: [3, 4, 4, 5, 6, 5, 4, 6, 5, 4, 5, 4, 6, 5, 4, 5],
      smooth: true
    },
    {
      name: 'Total Active Users',
      type: 'line',
      data: [72, 77, 74, 71, 78, 85, 82, 88, 84, 81, 87, 92, 91, 85, 86, 84],
      smooth: true
    }
  ],
  grid: {
    top: 10,
    bottom: 30, // increased for x-axis labels
    left: 10,   // small padding
    right: 35,  // allows space for last label
    containLabel: true
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
  width: 100%;
  height: 100%;
}
</style>
