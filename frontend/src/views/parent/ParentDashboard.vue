<script setup lang="ts">
import { fetchData } from "@/fx/api";
import { getBackendURL } from "@/fx/utils";
import ParentAppLayout from "@/layouts/ParentAppLayout.vue";
import { ref } from "vue";
import { onMounted } from "vue";
import { useRouter } from "vue-router";

type ChildType = {
  id: number;
  name: string;
  image: string;
}[];

const child = ref<ChildType>();

onMounted(async () => {
  const data = await fetchData(getBackendURL("children"));

  if (data) {
    child.value = data;
  }
});

const router = useRouter();

function navToProfile(id: number) {
  router.push({ name: "child_profile_parent", params: { id } });
}

function newChild() {
  router.push({ name: "parent_new_children" });
}

function fixMalformedBase64Image(input: string | null | undefined): string {
  const fallbackImage = "/assets/default-user.jpg"; // ✅ your basic fallback image path

  if (!input || input.trim() === "") {
    return fallbackImage;
  }

  // Already valid
  if (input.startsWith("data:image/") && input.includes(";base64,")) {
    return input;
  }

  // Try to fix malformed known patterns
  const fixed = input.replace(
    /^dataimage\/(jpeg|png|webp|gif)base64[\/,]?/,
    "data:image/$1;base64,"
  );

  // Still malformed? Assume JPEG
  if (!fixed.startsWith("data:image/")) {
    return "data:image/jpeg;base64," + input;
  }

  return fixed;
}
</script>

<template>
  <ParentAppLayout>
    <div class="dashboard" v-if="child">
      <h2>Select or Add a child get started</h2>
      <div class="child-group">
        <div v-for="i in child" class="child" @click="navToProfile(i.id)" :key="i.id">
          <img :src="fixMalformedBase64Image(i.image)" />
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

.child > img {
  width: 120px;
  height: 120px;
  border-radius: 100%;
}

.child i {
  font-size: 50px;
  border: 1px solid var(--color-border);
  padding: var(--size-md) var(--size-lg);
  border-radius: 100%;
}
</style>
