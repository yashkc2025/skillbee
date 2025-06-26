<template>
    <div class="module-card">
        <img :src="image" :alt="name" class="module-image" />
        <h2 class="module-name">{{ name }}</h2>
        <p class="module-description">{{ description }}</p>
        <slot></slot>
        <div class="module-buttons">
            <AppButton type="primary" class="primary" @click="$emit('primary')">{{ primaryLabel }}</AppButton>
            <AppButton type="secondary" class="secondary" @click="$emit('secondary')">{{ secondaryLabel }}
            </AppButton>
        </div>
        <div class="progress-bar-container">
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" :style="{ width: progressStatus + '%' }"></div>
                <span class="progress-bar-label">{{ progress }}</span>
            </div>
        </div>
        <!-- <AppButton v-if="tertiaryLabel" type="tertiary" :class="['tertiary', { 'disabled-tertiary': disabledTertiary }]"
            :disabled="disabledTertiary" @click="$emit('tertiary')">
            {{ tertiaryLabel }}
        </AppButton> -->
    </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, computed } from 'vue';
import AppButton from './AppButton.vue';

const props = defineProps<{
    image: string;
    name: string;
    description: string;
    primaryLabel?: string;
    secondaryLabel?: string;
    progressStatus?: number; // e.g. '3/5 Completed' or '60% Complete'
}>();

defineEmits(['primary', 'secondary']);

const progress = computed(() => {
    if (!props.progressStatus) return 'Not Started';
    else if (props.progressStatus === 0) return 'Not Started';
    else if (props.progressStatus === 100) return 'Completed';
    else return `Progress ${props.progressStatus}%`;
});
</script>

<style scoped>
.module-card {
    background: linear-gradient(135deg, #f9f6ff 0%, #e0f7fa 100%);
    border-radius: var(--border-radius);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    padding: 2px 0 10px 0;
    max-width: 350px;
    margin: 20px auto;
    transition: box-shadow 0.3s;
}

.module-card:hover {
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
    cursor: pointer;
}

.module-image {
    width: 100%;
    border-radius: var(--border-radius) var(--border-radius) 0 0;
    object-fit: cover;
    border: 4px solid #fff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.10);
    background: #fff;
}

.module-name {
    font-family: 'VAGRoundedNext';
    font-size: var(--font-lg);
    color: #4a148c;
    margin: 10px 0 10px 0;
    padding: 0 15px;
    letter-spacing: 1px;
}

.module-description {
    font-size: var(--font-md);
    color: #00796b;
    margin-bottom: 10px;
    padding: 0 15px;
    min-height: 40px;
}

.module-buttons {
    display: flex;
    gap: 5%;
    justify-content: center;
}

.primary {
    width: 44%;
}

.secondary {
    width: 44%;
}

.tertiary {
    /* display: block; */
    /* width: 95%; */
    /* margin: 18px auto 0 auto; */
}

.tertiary.disabled-tertiary {
    /* background: #ffb2dd; */
    /* color: #ad1457; */
    /* cursor: not-allowed; */
}

.progress-bar-container {
    width: 92%;
    margin: 18px auto 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.progress-bar-bg {
    width: 100%;
    height: 28px;
    /* border-radius: 5px; */
    border-radius: calc(var(--border-radius) / 1.5);
    background: linear-gradient(135deg, #ef476f, #f78fa7);
    /* box-shadow: 0 2px 8px rgba(255, 193, 7, 0.10); */
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
}

.progress-bar-fill {
    height: 100%;
    background: linear-gradient(135deg, #ccf0a9f6, #b2ff59);
    /* border-radius: 18px 0 0 18px; */
    border-radius: calc(var(--border-radius) / 1.5) 0 0 calc(var(--border-radius) / 1.5);
    transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    /* box-shadow: 0 2px 8px rgba(255, 128, 171, 0.10); */
    /* border: 2px solid #fff; */
    animation: progress-bar-fill 1s ease-in-out forwards;
}

@keyframes progress-bar-fill {
    0% {
        width: 0;
    }

    100% {
        width: var(progressPercent);
    }
}

.progress-bar-label {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    /* font-family: 'VAGRoundedNext', 'Comic Sans MS', cursive, sans-serif; */
    font-size: 1.1rem;
    color: #4a148c;
    /* font-weight: bold; */
    /* text-shadow: 1px 1px 0 #fffde7; */
    pointer-events: none;
}
</style>
