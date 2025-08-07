<script setup lang="ts">
import CardV2 from "@/components/CardV2.vue";
import { fetchData, deleteData } from "@/fx/api";
import { getBackendURL, fixImage } from "@/fx/utils";
import AdminAppLayout from "@/layouts/AdminAppLayout.vue";
import sitemap from "@/router/sitemap.json";
import { ref } from "vue";
import { onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

type Badges = {
  label: string;
  image: string;
  id: number;
}[];
const badges = ref<Badges>();

function addEntry() {
  router.push(sitemap.admin.new.badge);
}

onMounted(async () => {
  const data = await fetchData(getBackendURL("badges"));
  badges.value = data;
});

async function deleteBadge(id: number) {
  await deleteData(getBackendURL("admin/badge"), { id });
}
</script>

<template>
  <AdminAppLayout>
    <CardV2 labelTitle="Badges" labelImage="bi bi-stars">
      <template #top-content>
        <div class="table-header">
          <i class="bi bi-plus-lg" @click="addEntry"></i>
        </div>
      </template>
      <template #content>
        <div class="badge-group">
          <div v-for="(s, i) in badges" :key="i" class="badge-parent">
            <i class="bi bi-trash edit" @click="deleteBadge(s.id)"></i>
            <img :src="fixImage(s.image)" :alt="s.label" />
            <span class="skill-card">{{ s.label }}</span>
          </div>
        </div>
      </template>
    </CardV2>
  </AdminAppLayout>
</template>

<style scoped>
img {
  width: 100px;
  border-top-left-radius: var(--border-radius);
  border-top-right-radius: var(--border-radius);
}

.badge-parent {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 140px;
  /* height: 150px; */
  /* background-color: red; */
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  font-size: var(--font-sm);
  padding: var(--size-xs);
  gap: 2px;
}

.badge-group {
  display: flex;
  flex-wrap: wrap;
  gap: var(--size-xs);
}

.edit {
  position: absolute;
  right: 5px;
  top: 5px;
  cursor: pointer;
  font-size: var(--font-xs);
  border: 2px solid var(--color-border);
  background-color: white;
  padding: 4px 6px;
  border-radius: 10px;
}
</style>
