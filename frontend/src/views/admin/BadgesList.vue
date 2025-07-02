<script setup lang="ts">
import CardV2 from '@/components/CardV2.vue';
import AdminAppLayout from '@/layouts/AdminAppLayout.vue';

const badges = [
  {
    label: "Quick Thinker",
    image:
      "http://static.vecteezy.com/system/resources/previews/055/850/981/non_2x/cute-brain-cartoon-with-lightning-bolt-vector.jpg",
  },
  {
    label: "Quick Thinker (alt)",
    image:
      "https://thumbs.dreamstime.com/b/brain-lightning-brainstorm-concept-like-cloud-power-mind-103281710.jpg",
  },
  {
    label: "Math Magician",
    image:
      "https://play-lh.googleusercontent.com/_amVHhZZT0Jk3MAHEog0rZeCVMl2w6zQYoDH8Mo7ZjKUIQwRoUxg-FhgALctyKmAjoo",
  },
  {
    label: "Math Magician (alt)",
    image:
      "https://is3-ssl.mzstatic.com/image/thumb/Purple122/v4/91/5c/c1/915cc1a2-0c75-4f6a-437b-68553220653e/source/512x512bb.jpg",
  },
];


</script>

<template>
  <AdminAppLayout>
    <CardV2 labelTitle="Badges" labelImage="bi bi-stars">
      <template #top-content>
        <div class="table-header">
          <i class="bi bi-plus-lg"></i>
        </div>
      </template>
      <template #content>
        <div class="badge-group">
          <div v-for="(s, i) in badges" :key="i" class="badge-parent">
            <i class="bi bi-pen edit "></i>
            <img :src="s.image" :alt="s.label" />
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
