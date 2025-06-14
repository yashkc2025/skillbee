<template>
  <!-- Responsive Chart -->
  <v-chart :option="option" autoresize class="chart" />
</template>

<script setup>
import { use } from "echarts/core";
import VChart from "vue-echarts";
import { LineChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
} from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";

use([
  LineChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  CanvasRenderer,
]);

// Generate sample data with actual dates
const generateDateData = () => {
  const data = [];
  const startDate = new Date("2025-01-01");
  const endDate = new Date("2025-05-01"); // 4 months later

  for (let i = 0; i < 15; i++) {
    const randomTime =
      startDate.getTime() + Math.random() * (endDate.getTime() - startDate.getTime());
    const randomDate = new Date(randomTime);

    data.push({
      date: randomDate.toISOString().split("T")[0], // YYYY-MM-DD format
      revenue: Math.floor(Math.random() * 5), // Random revenue between 0-4
    });
  }

  return data;
};

const sampleData = generateDateData();

const option = {
  grid: {
    top: 30,
    left: 50,
    right: 30,
    bottom: 40,
  },
  xAxis: {
    type: "category",
    data: sampleData.map((item) => {
      const date = new Date(item.date);
      return date.toLocaleDateString("en-US", {
        month: "short",
        day: "2-digit",
        year: "2-digit",
      });
    }),
  },
  yAxis: {
    type: "value",
    name: "Points Earned",
    position: "left",
    nameLocation: "middle", // Center the label along the axis
    nameGap: 25, // Adjust distance from the axis (tweak as needed)
    axisLabel: {
      formatter: function (value) {
        return value;
      },
    },
    splitLine: {
      show: false,
    },
  },
  series: [
    {
      name: "Revenue",
      type: "line",
      smooth: true,
      data: sampleData.map((item) => item.revenue),
      lineStyle: {
        width: 3,
        color: "#ef476f",
      },
      itemStyle: {
        color: "#ef476f",
      },
    },
  ],
  dataZoom: [
    {
      type: "slider",
      xAxisIndex: 0,
      filterMode: "none",
    },
  ],
  tooltip: {
    trigger: "axis", // Show tooltip when hovering over axis (line chart)
    axisPointer: {
      type: "line", // Can be 'line' | 'shadow' | 'cross'
    },
    formatter: function (params) {
      const data = params[0];
      return `
<div style="padding: 10px;">
${data.data} Points earned on ${data.axisValue}
</div>

      `;
    },
    extraCssText:
      "padding: 0 !important; border: none; border-radius: 10px; font-size: 12px",
  },
};
</script>

<style scoped>
.chart {
  width: 100%;
  /* height: 500px; */
  /* min-height: 400px; */
  background-color: var(--color-light);
}
</style>
