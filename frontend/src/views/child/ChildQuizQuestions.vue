<template>
    <div class="quiz-header">
        <!-- <h2 class="quiz-title">🧩 Quiz Time! 🎉</h2> -->
        <h2 class="quiz-title">
            🧩 <span style="color: #4CAF50">{{ curriculum.name }}</span> &rarr;
            <span style="color: #FFA726">{{ lesson.title }}</span> &rarr;
            <span style="color: #42A5F5">{{ quiz.name }}</span> <br>
            🎉 Quiz Time! Good luck! 🍀
        </h2>
        <div class="time-left" :class="{ 'danger': timeDuration < 60 }">
            ⏰ Time Left: {{ formatTime }}
        </div>
    </div>
    <div class="quiz-questions" :class="{ 'blur-bg': submitted }">
        <div v-for="(question, index) in questionList" :key="index" class="question-card">
            <div class="question-row">
                <p class="question-text">
                    Q{{ index + 1 }}: {{ question.question }}
                </p>
                <span class="marks">{{ question.marks }} marks</span>
            </div>
            <ul class="options-list">
                <li v-for="(option, idx) in question.options" :key="idx" class="option-item"
                    :class="{ selected: selectedOptions[index] === idx }" @click="selectOption(index, idx)">
                    <span class="option-label">{{ String.fromCharCode(65 + idx) }}.</span>
                    {{ option }}
                    <span v-if="selectedOptions[index] === idx" class="selected-emoji">✅</span>
                </li>
            </ul>
        </div>
        <AppButton type="primary" class="submit-btn" @click="submitQuiz" :disabled="submitted">
            {{ submitted ? 'Submitted! 🎉' : '🚀 Submit Answers' }}
        </AppButton>
    </div>

    <div v-if="submitted" class="quiz-submitted kid-center">
        <h2>🎉 Quiz Submitted! 🎉</h2>
        <p>Thank you for participating!<br>Your answers have been recorded.<br>🌟 Great job! 🌟</p>
        <AppButton type="secondary" @click="router.push({ name: 'child_quizzes' })">
            ⬅️ Back to quizzes
        </AppButton>
    </div>
</template>

<script setup lang="ts">
import AppButton from '@/components/AppButton.vue';
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const timer = ref<ReturnType<typeof setInterval> | null>(null);
const submitted = ref(false);

const curriculum = { curriculum_id: 1, name: 'General Knowledge' };
const lesson = { lesson_id: 1, title: 'Quiz on General Knowledge' };
const quiz = { quiz_id: 1, name: 'General Knowledge Quiz', time_duration: 90 };

const timeDuration = ref(quiz.time_duration); // 5 minutes in seconds

const questions = {
    "1": {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "marks": 10,
    },
    "2": {
        "question": "What is the largest planet in our solar system?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn"],
        "marks": 10,
    },
    "3": {
        "question": "What is the chemical symbol for water?",
        "options": ["H2O", "CO2", "O2", "NaCl"],
        "marks": 10,
    },
    "4": {
        "question": "What is the smallest prime number?",
        "options": ["1", "2", "3", "5"],
        "marks": 10,
    },
    "5": {
        "question": "What is the main ingredient in guacamole?",
        "options": ["Tomato", "Avocado", "Onion", "Pepper"],
        "marks": 10,
    },
    "6": {
        "question": "What is the largest mammal in the world?",
        "options": ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
        "marks": 10,
    },
    "7": {
        "question": "What is the capital of Japan?",
        "options": ["Seoul", "Beijing", "Tokyo", "Bangkok"],
        "marks": 10,
    },
};
const questionList = Object.values(questions);

const selectedOptions = ref<{ [key: number]: number }>({});

function selectOption(question_index: number, optIdx: number) {
    if (submitted.value) return;
    selectedOptions.value[question_index] = optIdx;
}

function submitQuiz() {
    if (submitted.value) return;
    submitted.value = true;
    clearTimer();
    console.log('Quiz submitted with answers:', selectedOptions.value);
    // alert("Quiz submitted! 🎉");
}

function clearTimer() {
    if (timer.value) {
        clearInterval(timer.value);
        timer.value = null;
    }
}

const formatTime = computed(() => {
    const minutes = Math.floor(timeDuration.value / 60);
    const seconds = timeDuration.value % 60;
    return `${minutes} min ${seconds.toString().padStart(2, '0')} sec`;
});

onMounted(() => {
    timer.value = setInterval(() => {
        if (timeDuration.value > 0) {
            timeDuration.value--;
        } else {
            if (!submitted.value) {
                submitQuiz();
            }
        }
    }, 1000);
});

onBeforeUnmount(() => {
    clearTimer();
});
</script>

<style scoped>
.quiz-questions {
    padding: 0 18px 18px 18px;
    position: relative;
}

.quiz-header {
    position: sticky;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    top: 0;
    z-index: 1;
    background-color: #fff3e0;
    padding: 0 10px;
}

.quiz-title {
    color: #ff9800;
    font-family: 'VAGRoundedNext';
    font-size: var(--font-ml-lg);
    letter-spacing: 1px;
    padding: 5px 0 5px 0;
}

.time-left {
    font-size: var(--font-md);
    font-weight: bold;
    width: fit-content;
    color: #388e3c;
    background: #fff8e1;
    border-radius: calc(var(--border-radius)/2);
    padding: 6px 18px;
    box-shadow: 0 1px 4px rgba(255, 193, 7, 0.08);
    margin-left: 10px;
    transition: color 0.3s, background 0.3s;
}

.time-left.danger {
    color: #d32f2f;
    background: #ffebee;
    animation: blink 1s steps(2, start) infinite;
}

@keyframes blink {
    to {
        visibility: hidden;
    }
}

.question-card {
    margin-bottom: 24px;
    padding: 18px 16px;
    background: #fff8e1;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(255, 193, 7, 0.10);
    transition: transform 0.15s;
    border: 1px solid rgba(211, 210, 210, 0.455);
}

.question-card:hover {
    transform: scale(1.01);
    box-shadow: 0 4px 16px rgba(255, 193, 7, 0.18);
}

.question-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.question-text {
    font-weight: bold;
    color: #4a148c;
    font-size: var(--font-md);
    font-family: 'VAGRoundedNext';
    margin-bottom: 0;
}

.marks {
    /* background: #ffd54f; */
    color: #bf360c;
    font-weight: bold;
    border-radius: 8px;
    padding: 4px 12px;
    font-size: calc(var(--font-md) / 1.2);
    margin-left: 10px;
    font-family: 'VAGRoundedNext';
}

.options-list {
    list-style-type: none;
    padding-left: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 12px;
}

.option-item {
    padding: 12px 16px;
    background: #ffe082;
    border-radius: 8px;
    color: #6d4c41;
    font-family: 'Delius', cursive;
    display: flex;
    align-items: center;
    box-shadow: 0 1px 4px rgba(255, 193, 7, 0.08);
    transition: background 0.2s, border 0.2s;
    cursor: pointer;
    border: 2px solid transparent;
    position: relative;
}

.option-item.selected {
    background: #b2ff59;
    border: 2px solid #43a047;
    color: #1b5e20;
    font-weight: bold;
}

.option-item:hover:not(.selected) {
    background: #ffd54f;
    border: 2px solid #ffb300;
}

.option-label {
    font-weight: bold;
    color: #ff9800;
    margin-right: 12px;
    font-size: var(--font-md);
    font-family: 'VAGRoundedNext';
}

.selected-emoji {
    margin-left: 10px;
    font-size: var(--font-md);
}

.submit-btn {
    display: block;
    margin: 32px auto 0 auto;
    color: #4a148c;
    font-weight: bold;
    border-radius: var(--border-radius);
    font-family: 'VAGRoundedNext';
    font-size: var(--font-md);
    padding: 12px 36px;
    box-shadow: 0 2px 8px rgba(255, 193, 7, 0.13);
    border: none;
    cursor: pointer;
    transition: background 0.2s, color 0.2s;
}

.submit-btn:disabled {
    background: #fff176;
    cursor: not-allowed;
}

.blur-bg {
    filter: blur(1px);
    pointer-events: none;
    user-select: none;
}

.quiz-submitted.kid-center {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #fff3e0;
    border-radius: 24px;
    box-shadow: 0 8px 32px rgba(255, 193, 7, 0.18);
    padding: 48px 36px 36px 36px;
    z-index: 1001;
    text-align: center;
    font-family: 'Comic Sans MS', 'Delius', cursive;
    min-width: 320px;
    max-width: 90vw;
    animation: pop-in 0.5s cubic-bezier(.68, -0.55, .27, 1.55);
}

.quiz-submitted.kid-center h2 {
    color: #ff9800;
    font-family: 'VAGRoundedNext', cursive;
    font-size: 2.2rem;
    margin-bottom: 18px;
    letter-spacing: 1px;
}

.quiz-submitted.kid-center p {
    color: #4a148c;
    font-size: 1.25rem;
    margin-bottom: 28px;
    font-family: 'Delius', cursive;
}

@keyframes pop-in {
    0% {
        transform: translate(-50%, -60%) scale(0.8);
        opacity: 0;
    }

    100% {
        transform: translate(-50%, -50%) scale(1);
        opacity: 1;
    }
}
</style>