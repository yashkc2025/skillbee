<script setup lang="ts">
import Card from '@/components/Card.vue';
import CardItem from '@/components/CardItem.vue';

</script>

<template>
  <main>
    <Card>
      <CardItem>
        <p class="ft-head-1 text-xl">I am a heading!</p>
      </CardItem>
      <CardItem>
        <p class="text-sm ft-delius">This is part of a UI system created for an ed-tech platform. A product
          loved
          by both students and educators.
        </p>
      </CardItem>
    </Card>
  </main>
</template>

<style scoped>
main {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
