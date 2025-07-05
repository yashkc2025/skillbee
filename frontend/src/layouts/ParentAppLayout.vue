<script setup lang="ts">
import ParentNavbar from "@/components/parent/ParentNavbar.vue"
</script>

<template>
  <main>
    <div class="navbar-parent">
      <ParentNavbar />
    </div>
    <div class="app-layout">
      <div>
        <slot></slot>
      </div>
    </div>
  </main>
</template>

<style scoped>
.navbar-parent {
  position: absolute;
  top: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: var(--size-sm);
}

.app-layout {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: "DMSans";

}

.app-layout>div {
  /* background-color: blue; */
  /* max-width: 1200px; */
  width: 100%;
  margin-top: var(--size-4xl);
  padding: 0 1rem;
}
</style>
