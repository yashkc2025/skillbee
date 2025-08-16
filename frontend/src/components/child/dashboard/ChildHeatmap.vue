<template>
  <div class="heatmap">
    <CalendarHeatmap
      :values="heatmapValues"
      :end-date="endDate"
      :round="3"
      :range-color="['rgb(230, 230, 230)', 'rgb(239, 71, 111)', 'rgb(239, 71, 111)']"
      class="chart"
    />
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
    const response = await fetch(`${base_url}child_heatmap`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch heatmap data: ${response.statusText}`);
    }

    const data = await response.json();

    if (data && data.heatmap) {
      heatmapValues.value = data.heatmap;
    } else {
      throw new Error("Invalid data format from API");
    }
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
/*
.chart {
  margin-bottom: -100px;
} */

.chart {
  width: 100%;
  max-width: 800px; /* or whatever fits */
  height: auto;
}

.chart svg {
  width: 100%;
  height: auto;
}
</style>
