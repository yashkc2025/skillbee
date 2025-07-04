<script setup lang="ts">
import CardV2 from '@/components/CardV2.vue';
import InputComponent from '@/components/InputComponent.vue';
import AdminAppLayout from '@/layouts/AdminAppLayout.vue';
import SelectComponent from "@/components/SelectComponent.vue"
import { ref } from 'vue';
import ParentAppLayout from '@/layouts/ParentAppLayout.vue';

const name = ref("")
const username = ref("")
const confirmPass = ref("")
const password = ref("")
const dob = ref()
const school = ref("")
</script>

<template>
  <ParentAppLayout>
    <div class="outer">
      <p class="intro">
        <span class="darken">Add Children</span>
      </p>
      <CardV2 label-title="Personal Info" label-image="bi bi-person">
        <template #content class="form">
          <div class="form">
            <InputComponent icon="bi bi-emoji-smile" name="name" placeholder="Title" v-model="name" />
            <InputComponent icon="bi bi-dot" name="username" placeholder="Username" v-model="username" />
            <InputComponent icon="bi bi-calendar-date" name="dob" placeholder="Date of Birth" v-model="dob"
              field-type="date" />
            <InputComponent icon="bi bi-buildings" name="school" placeholder="School" v-model="school" />
          </div>
        </template>
      </CardV2>
      <CardV2 label-title="Password" label-image="bi bi-asterisk">
        <template #content class="form">
          <div class="form">
            <InputComponent icon="bi bi-asterisk" name="password" placeholder="Password" v-model="password"
              field-type="password" />
            <InputComponent icon="bi bi-asterisk" name="conf-password" placeholder="Confirm Password"
              v-model="confirmPass" field-type="password" />
            <button type="button" class="button-admin">Create</button>
          </div>
        </template>
      </CardV2>
    </div>
  </ParentAppLayout>
</template>

<style scoped>
.intro {
  margin-bottom: 20px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: var(--size-xs)
}

.outer {
  display: flex;
  flex-direction: column;
  gap: var(--size-sm);
}
</style>
