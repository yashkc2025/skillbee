<template>
    <ChildAppLayout>
        <div class="child-settings">
            <h2 class="settings-title">⚙️ My Settings</h2>

            <!-- Profile Image Section -->
            <div class="settings-section profile-section">
                <h3>🖼️ Profile Image</h3>
                <div class="profile-image-wrap">
                    <img :src="profileImageUrl" alt="Profile" class="profile-image" @click="showProfileModal = true" />
                    <input type="file" accept="image/*" @change="onProfileImageChange" id="profile-upload"
                        class="profile-upload-input" />
                    <label for="profile-upload" class="profile-upload-btn">Change Image</label>
                </div>
            </div>

            <!-- Profile Image Modal -->
            <div v-if="showProfileModal" class="profile-modal-bg" @click.self="showProfileModal = false">
                <div class="profile-modal">
                    <img :src="profileImageUrl" alt="Profile Large" class="profile-image-large" />
                    <AppButton type="secondary" class="close-modal-btn" @click="showProfileModal = false">
                        Close
                    </AppButton>
                </div>
            </div>

            <!-- Details Section -->
            <div class="settings-section details-section">
                <h3>📝 My Details</h3>
                <form @submit.prevent="saveDetails">
                    <div class="form-row">
                        <label>Name:</label>
                        <input v-model="details.name" type="text" required />
                    </div>
                    <div class="form-row">
                        <label>Email:</label>
                        <input v-model="details.email_id" type="email" required />
                    </div>
                    <div class="form-row">
                        <label>Date of Birth:</label>
                        <input v-model="details.dob" type="date" required :max="maxDate" :min="minDate" />
                    </div>
                    <div class="form-row">
                        <label>School:</label>
                        <input v-model="details.school" type="text" />
                    </div>
                    <AppButton type="primary" class="save-btn" :disabled="savingDetails">
                        {{ savingDetails ? "Saving..." : "💾 Save Details" }}
                    </AppButton>
                </form>
                <div v-if="detailsSuccess" class="success-msg">{{ detailsSuccess }}</div>
            </div>

            <!-- Password Section -->
            <div class="settings-section password-section">
                <h3>🔒 Change Password</h3>
                <form @submit.prevent="changePassword">
                    <div class="form-row password-row">
                        <label>Current Password:</label>
                        <div class="password-input-wrap">
                            <input :type="showCurrentPassword ? 'text' : 'password'" v-model="passwordForm.current"
                                required />
                            <span class="eye-icon" @click="showCurrentPassword = !showCurrentPassword">
                                <i v-if="showCurrentPassword" class="bi bi-eye"></i>
                                <i v-else class="bi bi-eye-slash"></i>
                            </span>
                        </div>
                    </div>
                    <div class="form-row password-row">
                        <label>New Password:</label>
                        <div class="password-input-wrap">
                            <input :type="showNewPassword ? 'text' : 'password'" v-model="passwordForm.new" required
                                minlength="6" />
                            <span class="eye-icon" @click="showNewPassword = !showNewPassword">
                                <i v-if="showNewPassword" class="bi bi-eye"></i>
                                <i v-else class="bi bi-eye-slash"></i>
                            </span>
                        </div>
                    </div>
                    <div class="form-row password-row">
                        <label>Confirm Password:</label>
                        <div class="password-input-wrap">
                            <input :type="showConfirmPassword ? 'text' : 'password'" v-model="passwordForm.confirm"
                                required minlength="6" />
                            <span class="eye-icon" @click="showConfirmPassword = !showConfirmPassword">
                                <i v-if="showConfirmPassword" class="bi bi-eye"></i>
                                <i v-else class="bi bi-eye-slash"></i>
                            </span>
                        </div>
                    </div>
                    <AppButton type="primary" class="save-btn" :disabled="changingPassword">
                        {{ changingPassword ? "Changing..." : "🔑 Change Password" }}
                    </AppButton>
                </form>
                <div v-if="passwordError" class="error-msg">{{ passwordError }}</div>
                <div v-if="passwordSuccess" class="success-msg">{{ passwordSuccess }}</div>
            </div>
        </div>
    </ChildAppLayout>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import ChildAppLayout from "../../layouts/ChildAppLayout.vue";
import AppButton from "@/components/AppButton.vue";

const profileImageUrl = ref("/files/default-profile.jpg");
const details = ref({
    name: "Kid Name",
    email_id: "kid@email.com",
    dob: "2013-01-01",
    school: "Happy Kids School"
});
const savingDetails = ref(false);
const detailsSuccess = ref("");

const showProfileModal = ref(false);

const today = new Date();
const minDate = computed(() => {
    const d = new Date(today);
    d.setFullYear(d.getFullYear() - 14);
    return d.toISOString().split("T")[0];
});
const maxDate = computed(() => {
    const d = new Date(today);
    d.setFullYear(d.getFullYear() - 8);
    return d.toISOString().split("T")[0];
});

function onProfileImageChange(e: Event) {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (ev) => {
            profileImageUrl.value = ev.target?.result as string;
        };
        reader.readAsDataURL(file);
    }
}

async function saveDetails() {
    savingDetails.value = true;
    setTimeout(() => {
        savingDetails.value = false;
        detailsSuccess.value = "Details saved! 🎉";
        setTimeout(() => {
            detailsSuccess.value = "";
        }, 5000);
    }, 1000);
}

const passwordForm = ref({
    current: "",
    new: "",
    confirm: ""
});
const changingPassword = ref(false);
const passwordError = ref("");
const passwordSuccess = ref("");
const showCurrentPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref("");

async function changePassword() {
    passwordError.value = "";
    passwordSuccess.value = "";
    if (passwordForm.value.new !== passwordForm.value.confirm) {
        passwordError.value = "New passwords do not match!";
        setTimeout(() => {
            passwordError.value = "";
        }, 5000);
        return;
    }
    changingPassword.value = true;
    setTimeout(() => {
        changingPassword.value = false;
        passwordSuccess.value = "Password changed successfully! 🎉";
        passwordForm.value.current = "";
        passwordForm.value.new = "";
        passwordForm.value.confirm = "";
        setTimeout(() => {
            passwordSuccess.value = "";
        }, 5000);
    }, 1200);
}
</script>

<style scoped>
.child-settings {
    border-radius: var(--border-radius);
    font-family: 'Delius';
}

.settings-title {
    color: #ff9800;
    font-family: 'VAGRoundedNext';
    font-size: var(--font-lg);
    margin-bottom: 15px;
    letter-spacing: 1px;
}

.settings-section {
    margin-bottom: 32px;
    background: #fff8e1;
    border-radius: var(--border-radius);
    padding: 18px 18px 12px 18px;
    box-shadow: 0 2px 8px rgba(255, 193, 7, 0.08);
    border: 1px solid rgba(211, 210, 210, 0.455);
}

h3 {
    color: #ffb300;
    font-family: 'VAGRoundedNext';
    font-size: var(--font-ml-lg);
    margin-bottom: 12px;
    letter-spacing: 1px;
}

.profile-image-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
}

.profile-image {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #ffb300;
    background: #fffde7;
    margin-bottom: 8px;
    cursor: pointer;
    transition: transform 0.2s;
}

.profile-image:hover {
    transform: scale(1.08);
    box-shadow: 0 0 0 4px #ffe082;
}

.profile-upload-input {
    display: none;
}

.profile-upload-btn {
    display: inline-block;
    background: #ffd54f;
    color: #4a148c;
    font-weight: bold;
    border-radius: var(--border-radius);
    font-family: 'VAGRoundedNext';
    padding: 6px 18px;
    box-shadow: 0 2px 8px rgba(255, 193, 7, 0.13);
    cursor: pointer;
    transition: background 0.2s;
}

.profile-upload-btn:hover {
    background: #ffe082;
}

.profile-modal-bg {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.35);
    z-index: 1002;
    display: flex;
    align-items: center;
    justify-content: center;
}

.profile-modal {
    background: #fffde7;
    border-radius: var(--border-radius);
    padding: 32px 24px 24px 24px;
    box-shadow: 0 8px 32px rgba(255, 193, 7, 0.18);
    display: flex;
    flex-direction: column;
    align-items: center;
    animation: pop-in 0.4s cubic-bezier(.68, -0.55, .27, 1.55);
}

.profile-image-large {
    width: 220px;
    height: 220px;
    /* border-radius: 50%; */
    object-fit: cover;
    border: 3px solid #ffb300;
    background: #fffde7;
    margin-bottom: 18px;
}

.close-modal-btn {
    margin-top: 10px;
    width: 120px;
}

@keyframes pop-in {
    0% {
        transform: scale(0.8);
        opacity: 0;
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }
}

.form-row {
    display: flex;
    align-items: center;
    margin-bottom: 16px;
    gap: 12px;
}

.form-row label {
    min-width: 110px;
    color: #1976d2;
    font-weight: bold;
    font-family: 'VAGRoundedNext';
}

.form-row input {
    flex: 1;
    padding: 8px 12px;
    border-radius: var(--border-radius);
    border: 1px solid #ffb300;
    font-size: calc(var(--font-md)/1.15);
    font-family: 'Delius';
    background: #fffde7;
}

.save-btn {
    margin-top: 10px;
    width: 100%;
}

.password-section {
    margin-top: 24px;
}

.password-section .form-row label {
    min-width: 130px;
}

.error-msg {
    color: #d32f2f;
    background: #ffebee;
    border-radius: var(--border-radius);
    padding: 8px 12px;
    margin-top: 10px;
    text-align: center;
    font-family: 'Delius';
    animation: fade-in-out 5s linear;
}

.success-msg {
    color: #388e3c;
    background: #e8f5e9;
    border-radius: var(--border-radius);
    padding: 8px 12px;
    margin-top: 10px;
    text-align: center;
    font-family: 'Delius';
    animation: fade-in-out 5s linear;
}

@keyframes fade-in-out {
    0% {
        opacity: 0;
    }

    10% {
        opacity: 1;
    }

    90% {
        opacity: 1;
    }

    100% {
        opacity: 0;
    }
}

.password-row {
    position: relative;
}

.password-input-wrap {
    position: relative;
    width: 100%;
    display: flex;
    align-items: center;
}

.password-input-wrap input {
    width: 100%;
    padding-right: 36px;
}

.eye-icon {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
    user-select: none;
    display: flex;
    align-items: center;
    transition: color 0.2s;
}

.eye-icon svg {
    display: block;
}
</style>