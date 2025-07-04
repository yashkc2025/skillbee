<template>
  <div class="chart-wrapper">
    <v-chart ref="chartRef" class="chart" :option="option" autoresize />
  </div>
</template>

<script setup lang="ts">
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { FunnelChart } from 'echarts/charts';
import {
  TooltipComponent,
  TitleComponent,
  LegendComponent,
} from 'echarts/components';
import VChart from 'vue-echarts';
import { ref, onMounted, nextTick } from 'vue';
import type { ECRef } from 'vue-echarts';

use([
  CanvasRenderer,
  FunnelChart,
  TooltipComponent,
  TitleComponent,
  LegendComponent,
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
  tooltip: {
    trigger: 'item',
    formatter: ({ name, value, percent }: any) => `${name}: ${value} (${percent}%)`
  },
  legend: {
    bottom: 0
  },
  series: [
    {
      name: 'Learning Funnel',
      type: 'funnel',
      left: '10%',
      top: 20,
      bottom: 40,
      width: '80%',
      min: 0,
      max: 500,
      minSize: '30%',
      maxSize: '100%',
      sort: 'descending', // top to bottom funnel
      gap: 5,
      label: {
        show: true,
        position: 'inside',
        formatter: '{b}\n{c}',
        fontWeight: 'bold'
      },
      itemStyle: {
        borderColor: '#fff',
        borderWidth: 2
      },
      emphasis: {
        label: {
          fontSize: 16
        }
      },
      data: [
        { value: 500, name: 'Users Started Skill' },
        { value: 350, name: 'Lessons Completed' },
        { value: 250, name: 'Quizzes Attempted' },
        { value: 120, name: 'Badges Earned' }
      ]
    }
  ]
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
