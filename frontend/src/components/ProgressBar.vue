<template>
  <div>
    <v-chart :option="chartOptions" autoresize style="height: 40px; width: 100%; margin: 0; padding: 0;" />
  </div>
</template>

<style scoped>
div {
  width: 100%;
  height: 40px !important;
  margin-bottom: -15px;
  margin-top: -15px;
  padding: 0;
}
</style>

<script setup lang="ts">
import { ref } from 'vue'
import * as echarts from 'echarts/core'
import { BarChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  TitleComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

import VChart from 'vue-echarts'

// Register the required components
echarts.use([
  BarChart,
  GridComponent,
  TooltipComponent,
  TitleComponent,
  CanvasRenderer
])

const props = defineProps({
  progress: {
    type: Number,
    required: true
  },
  barColor: {
    type: String,
    default: '#ef476f'
  },
  radius: {
    type: Number,
    default: 10
  },
  width: {
    type: Number,
    default: 15
  },
  labelColor: {
    type: String,
    default: '#fff'
  }
})



const chartOptions = ref({
  xAxis: {
    type: 'value',
    max: 100,
    show: false
  },
  yAxis: {
    type: 'category',
    data: ['Progress'],
    show: false
  },
  series: [
    {
      type: 'bar',
      data: [props.progress],
      barWidth: props.width,
      itemStyle: {
        color: props.barColor,
        borderRadius: [props.radius, props.radius, props.radius, props.radius]
      },
      label: {
        show: true,
        position: 'insideRight',
        formatter: '{c}%',
        fontWeight: 'bold',
        color: props.labelColor
      }
    },
  ],
  grid: {
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
    containLabel: false
  },
})
</script>
