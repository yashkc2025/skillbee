<script setup lang="ts">
import CardV2 from '@/components/CardV2.vue';
import InputComponent from '@/components/InputComponent.vue';
import AdminAppLayout from '@/layouts/AdminAppLayout.vue';
import SelectComponent from "@/components/SelectComponent.vue"
import { ref } from 'vue';
import ParentAppLayout from '@/layouts/ParentAppLayout.vue';
import { postData } from '@/fx/api';

const name = ref("")
const username = ref("")
const confirmPass = ref("")
const password = ref("")
const dob = ref()
const school = ref("")

async function newChildren() {
  await postData("", {
    "name": name.value,
    "username": username.value,
    "confirmPass": confirmPass.value,
    "password": password.value,
    "dob": dob.value,
    "school": school.value
  })
}
</script>

<template>
  <ParentAppLayout>
    <form class="outer" @submit.prevent="newChildren">
      <p class="intro">
        <span class="darken">Add Children</span>
      </p>
      <CardV2 label-title="Personal Info" label-image="bi bi-person">
        <template #content class="form">
          <div class="form">
            <InputComponent icon="bi bi-emoji-smile" name="name" placeholder="Title" v-model="name" :required="true" />
            <InputComponent icon="bi bi-dot" name="username" placeholder="Username" v-model="username"
              :required="true" />
            <InputComponent icon="bi bi-calendar-date" name="dob" placeholder="Date of Birth" v-model="dob"
              field-type="date" :required="true" />
            <InputComponent icon="bi bi-buildings" name="school" placeholder="School" v-model="school"
              :required="true" />
          </div>
        </template>
      </CardV2>
      <CardV2 label-title="Password" label-image="bi bi-asterisk">
        <template #content class="form">
          <div class="form">
            <InputComponent icon="bi bi-asterisk" name="password" placeholder="Password" v-model="password"
              field-type="password" :required="true" />
            <InputComponent icon="bi bi-asterisk" name="conf-password" placeholder="Confirm Password"
              v-model="confirmPass" field-type="password" :required="true" />
            <button type="submit" class="button-admin">Create</button>
          </div>
        </template>
      </CardV2>
    </form>
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
