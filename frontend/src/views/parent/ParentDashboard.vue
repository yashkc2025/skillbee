<script setup lang="ts">
import AdminAppLayout from "@/layouts/AdminAppLayout.vue";
import ChildrenTable from "@/components/admin/dashboard/ChildrenTable.vue"
import ParentTable from "@/components/admin/dashboard/ParentTable.vue";
import ActiveUserChart from "@/components/admin/charts/ActiveUserChart.vue";
import CardV2 from "@/components/CardV2.vue";
import SkillChart from "@/components/admin/charts/SkillChart.vue";
import ParentAppLayout from "@/layouts/ParentAppLayout.vue";
import { useRouter } from "vue-router";

const parent = {
  'name': 'Mr. Kumar',
  'child': [
    {
      'id': 1,
      'name': 'Yash Kumar',
      'profile_image': "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ09_SsUhus7pTrYp8oZpJp434QP-XFp_4F7Q&s"
    }
  ]
}

const router = useRouter()

function navToProfile(id: number) {
  router.push({ name: 'child_profile_parent', params: { id } })
}

function newChild() {
  router.push({ name: 'parent_new_children' })
}
</script>

<template>
  <ParentAppLayout>
    <div class="dashboard">
      <h2>Select or Add a child get started</h2>
      <div class="child-group">
        <div v-for="i in parent.child" class="child" @click="navToProfile(i.id)">
          <img :src="i.profile_image" />
          <p>{{ i.name }}</p>
        </div>
        <div class="child" @click="newChild()">
          <i class="bi bi-plus-lg"></i>
          <p>Add Child</p>
        </div>
      </div>
    </div>
  </ParentAppLayout>
</template>

<style scoped>
h2 {
  font-weight: 800;
}

.dashboard {
  display: flex;
  flex-direction: column;
  /* background-color: red; */
  height: 85vh;
  gap: var(--size-md);
  justify-content: center;
  align-items: center;
}

.child-group {
  display: flex;
  flex-direction: row;
  gap: var(--size-xl);
}

.child {
  /* width: 170px; */
  /* border: 1px solid var(--color-border); */
  border-radius: var(--border-radius);
  /* padding: var(--size-xs); */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: var(--font-sm);
  gap: var(--size-2xs);
  cursor: pointer;
}

.child>img {
  width: 120px;
  height: 120px;
  border-radius: 100%
}

.child i {
  font-size: 50px;
  border: 1px solid var(--color-border);
  padding: var(--size-md) var(--size-lg);
  border-radius: 100%;
}
</style>
