<script setup lang="tsx">
const props = withDefaults(defineProps<{
  maxItems?: number;
  showExpand?: boolean;
}>(), {
  showExpand: false,
})

import CardV2 from "@/components/CardV2.vue";
import InputComponent from "@/components/InputComponent.vue";
import TableComponent from "@/components/TableComponent.vue";
import { useRouter } from "vue-router";
import sitemap from "@/router/sitemap.json"

const parents = [
  {
    id: 1,
    name: "Kiran Kumar",
    email: "kiran.kumar@app.com",
    blocked: false,
  },
  {
    id: 2,
    name: "Sunita Sharma",
    email: "sunita.sharma@app.com",
    blocked: false,
  },
  {
    id: 3,
    name: "Ravi Reddy",
    email: "ravi.reddy@app.com",
    blocked: true,
  },
  {
    id: 4,
    name: "Neha Mehta",
    email: "neha.mehta@app.com",
    blocked: false,
  },
  {
    id: 5,
    name: "Anil Verma",
    email: "anil.verma@app.com",
    blocked: false,
  },
];


const parentLabel = ['ID', 'Name', 'Email', 'Status', 'Children']

const router = useRouter()
function expandTable() {
  router.push(sitemap.admin.user_management.parent)
}

function viewKids() {
  router.push(sitemap.admin.user_management.children)
}

function tableEntries() {
  parents.forEach((p) => {
    p.blocked = <span class="chip pointer">{p.blocked ? "Blocked" : "Active"}</span>
    p.view_children = <i class="bi bi-patch-plus pointer" onClick={() => viewKids()}></i>
  })
  if (props.maxItems) {
    return parents.slice(0, props.maxItems)
  }

  return parents
}
</script>

<template>
  <CardV2 label-title="Parents" label-image="bi bi-person">
    <template #top-content>
      <div class="table-header">
        <InputComponent icon="bi bi-search" name="search" placeholder="Search for a parent" />
        <i class="bi bi-arrows-angle-expand" @click="expandTable" v-if="showExpand"></i>
      </div>
    </template>
    <template #content>
      <TableComponent :header="parentLabel" :rows="tableEntries()" />
    </template>
  </CardV2>
</template>
<style scope>
.table-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--size-xs);
}

.table-header>i {
  font-size: var(--font-sm);
  font-weight: 500;
  cursor: pointer;
  font-size: 12px;
  border: 1px solid var(--color-border);
  padding: 5px 7px;
  border-radius: var(--border-radius);
}
</style>
