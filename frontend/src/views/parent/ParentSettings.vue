<script setup lang="ts">
import CardV2 from '@/components/CardV2.vue';
import InputComponent from '@/components/InputComponent.vue';
import ParentAppLayout from '@/layouts/ParentAppLayout.vue';
import { ref } from 'vue';

const parent = {
  'name': 'Mr. Kumar',
  'email': 'a.kumar@gmail.com'
}

const email = ref(parent.email)
const name = ref(parent.name)
const oldPassword = ref("")
const newPassword = ref("")
const confirmPassword = ref("")

</script>

<template>
  <ParentAppLayout>
    <div class="outer">
      <p class="intro">
        <span class="darken">Account Settings</span>
      </p>
      <CardV2 label-title="Personal Details" label-image="bi bi-envelope">
        <template #content class="form">
          <form @submit.prevent="" class="form">
            <InputComponent icon="bi bi-emoji-smile" name="name" placeholder="Your name" v-model="name" />
            <InputComponent icon="bi bi-envelope" name="email" placeholder="Enter an email" v-model="email"
              field-type="email" />
            <button type="button" class="button-admin">Update email</button>
          </form>
        </template>
      </CardV2>
      <CardV2 label-title="Change Password" label-image="bi bi-asterisk">
        <template #content class="form">
          <form @submit.prevent="" class="form">
            <InputComponent icon="bi bi-asterisk" name="old-pass" placeholder="Old Password" v-model="oldPassword"
              field-type="password" />
            <InputComponent icon="bi bi-asterisk" name="new-pass" placeholder="New Password" v-model="newPassword"
              field-type="password" />
            <InputComponent icon="bi bi-asterisk" name="confirm-pass" placeholder="Confirm Password"
              v-model="confirmPassword" field-type="password" />
            <button type="button" class="button-admin">Update Password</button>
          </form>
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
  gap: var(--size-sm)
}

.outer {
  display: flex;
  flex-direction: column;
  gap: var(--size-sm);
}
</style>
