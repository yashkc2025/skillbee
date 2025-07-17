<script lang="ts" setup>
import { defineProps } from 'vue'

// Define props and their types
const props = defineProps<{
  header: string[]
  rows: unknown[]
}>()


function isComponent(val: unknown) {
  return typeof val === 'object' && val !== null && ('__v_isVNode' in val || 'render' in val)
}
</script>

<template>
  <table class="table">
    <thead>
      <tr>
        <th v-for="heading in props.header" :key="heading">
          {{ heading }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(child, index) in props.rows" :key="index">
        <td v-for="(value, key) in child" :key="key">
          <component :is="value" v-if="isComponent(value)" />
          <span v-else>{{ value }}</span>
        </td>
      </tr>
    </tbody>
  </table>
  <div class="empty" v-if="rows.length === 0">No such rows found</div>
</template>


<style scoped>
.table {
  border-collapse: collapse;
  /* border-spacing: 16px 0; */
  width: 100%;
}

.table td {
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

.table tr:nth-last-child(1) td {
  border-bottom: none;
}

.table tr:nth-child(1) td {
  border-top: none;
}

.table th,
.table td {
  text-align: start;
  padding: 10px 12px;

  box-sizing: border-box;
  font-size: 14px;
}

.table td:nth-last-child(1) {
  border-bottom-left-radius: var(--border-radius);
  border-bottom-right-radius: var(--border-radius);
}

.table th {
  background-color: #f5f5f5;
  /* font-weight: bold; */
  text-transform: uppercase;
  font-size: var(--font-xs);
  color: var(--color-heading-2);
}

.table th:first-child {
  border-top-left-radius: var(--border-radius);
  border-bottom-left-radius: var(--border-radius);
}

.table th:last-child {
  border-top-right-radius: var(--border-radius);
  border-bottom-right-radius: var(--border-radius);
}

.empty {
  text-align: center;
  font-weight: 500;
  width: 100%;
  margin: 50px 0;
}
</style>
