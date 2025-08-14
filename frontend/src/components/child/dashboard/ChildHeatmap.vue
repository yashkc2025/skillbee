<template>
  <div class="heatmap">
    <CalendarHeatmap :values="heatmapValues" :end-date="endDate" :round="3"
      :range-color="['rgb(230, 230, 230)', 'rgb(239, 71, 111)', 'rgb(239, 71, 111)']" class="chart" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { CalendarHeatmap } from "vue3-calendar-heatmap";
import { base_url } from "../../../router";

// Define a type for the heatmap values to ensure type safety
interface HeatmapValue {
  date: string;
  count: number;
}

const heatmapValues = ref<HeatmapValue[]>([]);
const endDate = ref<string>(new Date().toISOString().slice(0, 10)); // Current date in YYYY-MM-DD format

async function fetchHeatmapData() {
  try {
    const token = localStorage.getItem("authToken");
    const response = await fetch(`${base_url}child_dashboard_stats`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch heatmap data");
    }

    const data = await response.json();
    // The API returns an array of objects with 'date' and 'status'
    // We need to map 'status' to 'count' to be compatible with vue3-calendar-heatmap
    heatmapValues.value = data.heatmap.map((item: any) => ({
      date: item.date,
      count: item.status,
    }));
  } catch (error) {
    console.error("Error fetching heatmap data:", error);
  }
}

onMounted(() => {
  fetchHeatmapData();
});
</script>

<style scoped>
.heatmap {
  padding: var(--size-md);
}

.chart {
  margin-bottom: -100px;
}
</style>