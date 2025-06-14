<template>
  <div class="chart-wrapper">
    <v-chart :option="chartOptions" autoresize style="width: 100%; height: 220px" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import { use } from "echarts/core";
import VChart from "vue-echarts";

// ECharts Core Modules
import { CanvasRenderer } from "echarts/renderers";
import { HeatmapChart } from "echarts/charts";
import {
  CalendarComponent,
  TooltipComponent,
  VisualMapComponent,
} from "echarts/components";

// Register the components you need
use([
  CanvasRenderer,
  HeatmapChart,
  CalendarComponent,
  TooltipComponent,
  VisualMapComponent,
]);

// Generate dummy GitHub-style heatmap data
const generateCalendarData = () => {
  const year = new Date().getFullYear();
  const start = new Date(year, 0, 1);
  const end = new Date(year, 11, 31);
  const data = [];
  for (let date = new Date(start); date <= end; date.setDate(date.getDate() + 1)) {
    const formatted = date.toISOString().split("T")[0];
    data.push([formatted, Math.floor(Math.random() * 10)]);
  }
  return data;
};

const chartOptions = ref({
  tooltip: {
    position: "top",
    formatter: (params) => {
      const date = params.data[0];
      const count = params.data[1];
      return `${date}: ${count} contribution${count !== 1 ? "s" : ""}`;
    },
  },
  visualMap: {
    show: false,
    min: 0,
    max: 10,
    inRange: {
      color: ["#ffffff", "#fce4ec", "#f8bbd0", "#f48fb1", "#ec407a"],
    },
  },
  calendar: {
    top: 40,
    left: 40,
    right: 40,
    bottom: 40,
    range: new Date().getFullYear().toString(),
    cellSize: ["auto", 15], // auto width, fixed height
    splitLine: {
      show: false,
    },
    dayLabel: {
      firstDay: 1,
      nameMap: "en",
    },
    monthLabel: {
      nameMap: "en",
      margin: 15,
    },
    yearLabel: {
      show: false,
    },
  },
  series: [
    {
      type: "heatmap",
      coordinateSystem: "calendar",
      data: generateCalendarData(),
    },
  ],
});
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
}
</style>
