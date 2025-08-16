<script setup lang="ts">
import CardV2 from "@/components/CardV2.vue";
import InputComponent from "@/components/InputComponent.vue";
import ParentAppLayout from "@/layouts/ParentAppLayout.vue";
import { ref, onMounted } from "vue";
import { fetchData, updateData } from "@/fx/api";
import { getBackendURL } from "@/fx/utils";

const email = ref();
const name = ref();
const oldPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");

onMounted(async () => {
  const data = await fetchData(getBackendURL("/settings"));

  if (data) {
    email.value = data.email_id;
    name.value = data.name;
  }
});

async function updateSettings() {
  updateData(getBackendURL("/settings"), {
    email_id: email.value,
    name: name.value,
  });
}

async function updatePassword() {
  updateData(getBackendURL("/parent/update_password"), {
    oldPassword: oldPassword.value,
    newPassword: newPassword.value,
    confirmPassword: confirmPassword.value,
  });
}
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
            <InputComponent
              icon="bi bi-emoji-smile"
              name="name"
              placeholder="Your name"
              v-model="name"
            />
            <InputComponent
              icon="bi bi-envelope"
              name="email"
              placeholder="Enter an email"
              v-model="email"
              field-type="email"
            />
            <button type="button" @click="updateSettings" class="button-admin">
              Update email
            </button>
          </form>
        </template>
      </CardV2>
      <CardV2 label-title="Change Password" label-image="bi bi-asterisk">
        <template #content class="form">
          <form @submit.prevent="" class="form">
            <InputComponent
              icon="bi bi-asterisk"
              name="old-pass"
              placeholder="Old Password"
              v-model="oldPassword"
              field-type="password"
              :required="True"
            />
            <InputComponent
              icon="bi bi-asterisk"
              name="new-pass"
              placeholder="New Password"
              v-model="newPassword"
              field-type="password"
              :required="True"
            />
            <InputComponent
              icon="bi bi-asterisk"
              name="confirm-pass"
              placeholder="Confirm Password"
              v-model="confirmPassword"
              field-type="password"
              :required="True"
            />
            <button type="button" class="button-admin" @click="updatePassword">
              Update Password
            </button>
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
  gap: var(--size-sm);
}

.outer {
  display: flex;
  flex-direction: column;
  gap: var(--size-sm);
}
</style>
