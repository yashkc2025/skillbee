<script setup lang="tsx">
const props = withDefaults(
  defineProps<{
    maxItems?: number;
    showExpand?: boolean;
  }>(),
  {
    showExpand: false,
  }
);

import CardV2 from "@/components/CardV2.vue";
import InputComponent from "@/components/InputComponent.vue";
import TableComponent from "@/components/TableComponent.vue";
import { useRouter } from "vue-router";
import sitemap from "@/router/sitemap.json";
import { onMounted } from "vue";
import { fetchData } from "@/fx/api";
import { getBackendURL } from "@/fx/utils";
import { ref } from "vue";

type ParemtType = {
  id: number;
  name: string;
  email: string;
  blocked: boolean;
};
const parents = ref<ParemtType[]>([]);

onMounted(async () => {
  const data = await fetchData(getBackendURL("parents"));

  parents.value = data;
});

const parentLabel = ["ID", "Name", "Email", "Status"];

const router = useRouter();
function expandTable() {
  router.push(sitemap.admin.user_management.parent);
}

function viewKids() {
  router.push(sitemap.admin.user_management.children);
}

function tableEntries() {
  const c = parents.value.map((p) => ({
    id: p.id,
    name: p.name,
    email: p.email,
    blocked: <span class="chip pointer">{p.blocked ? "Active" : "Blocked"}</span>,
    // p.view_children = <i class="bi bi-patch-plus pointer" onClick={() => viewKids()}></i>;
  }));

  if (props.maxItems) {
    return c.slice(0, props.maxItems);
  }

  return c;
}
</script>

<template>
  <CardV2 label-title="Parents" label-image="bi bi-person">
    <template #top-content>
      <div class="table-header">
        <InputComponent
          icon="bi bi-search"
          name="search"
          placeholder="Search for a parent"
        />
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

.table-header > i {
  font-size: var(--font-sm);
  font-weight: 500;
  cursor: pointer;
  font-size: 12px;
  border: 1px solid var(--color-border);
  padding: 5px 7px;
  border-radius: var(--border-radius);
}
</style>
