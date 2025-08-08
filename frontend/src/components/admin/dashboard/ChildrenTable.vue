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
import { ref } from "vue";
import { onMounted } from "vue";
import { fetchData } from "@/fx/api";
import { getBackendURL } from "@/fx/utils";

type ChildType = {
  id: number;
  name: string;
  email: string;
  age: number;
  school_name: string;
  last_login: string;
};

const children = ref<ChildType[]>([]);

onMounted(async () => {
  const data = await fetchData(getBackendURL("children"));

  children.value = data;
});

const childrenLabel = [
  "ID",
  "Name",
  "Email",
  "Age",
  "School Name",
  "Last Login",
  "View More",
];

const router = useRouter();

function expandTable() {
  router.push(sitemap.admin.user_management.children);
}

function navToProfile(id: number) {
  router.push({ name: "child_profile_admin", params: { id } });
}

function tableEntries() {
  const c = children.value.map((p) => ({
    id: p.id,
    name: p.name,
    email: p.email ?? "-",
    age: p.age,
    school: p.school_name,
    last_login: p.last_login ?? "-",
    view_more: (
      <i class="bi bi-patch-plus pointer" onClick={() => navToProfile(p.id)}></i>
    ),
  }));
  if (props.maxItems) {
    return c.slice(0, props.maxItems);
  }

  return c;
}
</script>

<template>
  <CardV2 label-title="Children" label-image="bi bi-emoji-smile">
    <template #top-content>
      <div class="table-header">
        <InputComponent
          icon="bi bi-search"
          name="search"
          placeholder="Search for a student"
        />
        <i class="bi bi-arrows-angle-expand" @click="expandTable" v-if="showExpand"></i>
      </div>
    </template>
    <template #content>
      <TableComponent :header="childrenLabel" :rows="tableEntries()" />
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
  /* background-color: var(--color-background); */
  border: 1px solid var(--color-border);
  padding: 5px 7px;
  border-radius: var(--border-radius);
}
</style>
