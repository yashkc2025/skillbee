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
import { install$5 } from 'echarts/types/dist/shared';

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
      '2025-02-15', '2025-02-16', '2025-02-19',
      '2025-02-23', '2025-02-24',
      '2025-02-25', '2025-02-26', '2025-02-27', '2025-03-01',

    ]
  },
  yAxis: { type: 'value' },
  series: [
    {
      name: 'Points ',
      type: 'line',
      data: [10, 15, 5, 20, 12, 14, 1, 20],
      smooth: false
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
  max-width: 100%;
  height: 100%;
  display: block;
}
</style>
