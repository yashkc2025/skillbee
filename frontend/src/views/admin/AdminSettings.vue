<script setup lang="ts">
import CardV2 from '@/components/CardV2.vue';
import InputComponent from '@/components/InputComponent.vue';
import AdminAppLayout from '@/layouts/AdminAppLayout.vue';
import { ref } from 'vue';

const email = ref("")
const oldPassword = ref("")
const newPassword = ref("")
const confirmPassword = ref("")

</script>

<template>
  <AdminAppLayout>
    <div class="outer">
      <p class="intro">
        <span class="darken">Admin Settings</span>
      </p>
      <CardV2 label-title="Change Email" label-image="bi bi-envelope">
        <template #content class="form">
          <form @submit.prevent="" class="form">
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
  </AdminAppLayout>
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
