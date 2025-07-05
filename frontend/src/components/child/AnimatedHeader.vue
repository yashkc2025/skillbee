<!-- AnimatedHeader.vue -->
<template>
    <div class="top-section">
        <h2 class="ft-head-1">{{ displayHeading }}</h2>
        <input type="text" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)"
            :placeholder="displayPlaceholder" class="search-box" />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue';

const props = defineProps<{
    modelValue: string;
    headingMessages?: string[];
    placeholderMessages?: string[];
    typingSpeed?: number;
    pauseDuration?: number;
}>();

const emit = defineEmits(['update:modelValue']);

const headingMessages = props.headingMessages;
const typingSpeed = props.typingSpeed || 100;
const pauseDuration = props.pauseDuration || 2000;

const displayHeading = ref('');
let headingAnimationId: number;

function typewriterEffect(
    messages: string[],
    displayRef: typeof displayHeading,
    currentIndex = 0,
    isDeleting = false,
    charIndex = 0
) {
    const currentMessage = messages[currentIndex % messages.length];

    if (!isDeleting) {
        displayRef.value = currentMessage.substring(0, charIndex + 1);
        charIndex++;

        if (charIndex === currentMessage.length) {
            setTimeout(() => {
                typewriterEffect(messages, displayRef, currentIndex, true, charIndex);
            }, pauseDuration);
            return;
        }
    } else {
        displayRef.value = currentMessage.substring(0, charIndex - 1);
        charIndex--;

        if (charIndex === 0) {
            currentIndex = (currentIndex + 1) % messages.length;
            isDeleting = false;
        }
    }

    const animationId = window.setTimeout(
        () => typewriterEffect(messages, displayRef, currentIndex, isDeleting, charIndex),
        isDeleting ? typingSpeed / 2 : typingSpeed
    );

    if (displayRef === displayHeading) {
        headingAnimationId = animationId;
    }
}

onMounted(() => {
    typewriterEffect(headingMessages, displayHeading);
});

onUnmounted(() => {
    clearTimeout(headingAnimationId);
});

watch(() => [props.headingMessages], () => {
    clearTimeout(headingAnimationId);
    typewriterEffect(
        props.headingMessages,
        displayHeading
    );
});

const displayPlaceholder = computed(() => {
    return props.placeholderMessages;
});
</script>

<style scoped>
.top-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 25px;
    height: 30px;
}

.search-box {
    min-width: 25%;
    width: 40%;
    max-width: 400px;
    height: 30px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: calc(var(--border-radius) / 1.5);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    font-family: "VAGRoundedNext";
}

.search-box::placeholder {
    font-style: italic;
}
</style>
