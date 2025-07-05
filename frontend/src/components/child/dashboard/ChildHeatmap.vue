<template>
  <div class="heatmap">
    <CalendarHeatmap :values="[
      { date: '2018-9-21', count: 1 },
      { date: '2018-9-22', count: 1 },
    ]" :end-date="'2018-10-22'" :round="3"
      :range-color="['rgb(230, 230, 230)', 'rgb(239, 71, 111)', 'rgb(239, 71, 111)']" class="chart" />
  </div>
</template>

<script>
import { CalendarHeatmap } from "vue3-calendar-heatmap";

export default {
  name: "GitHubHeatmap",
  components: {
    CalendarHeatmap,
  },
  data() {
    return {
      heatmapData: [
        { date: "2018-9-21", count: 1 },
        { date: "2018-9-22", count: 1 },
      ],
      heatmapColors: ["#e6e6e6", "#ef476f", "#ef476f"],
    };
  },
};
</script>

<style scoped>
.heatmap {
  padding: var(--size-md);
}

.chart {
  margin-bottom: -100px;
}
</style>
