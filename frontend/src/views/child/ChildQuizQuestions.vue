<template>
    <div class="quiz-header">
        <!-- <h2 class="quiz-title">🧩 Quiz Time! 🎉</h2> -->
        <h2 class="quiz-title">
            🧩 <span style="color: #4caf50">{{ curriculum.name }}</span> &rarr;
            <span style="color: #ffa726">{{ lesson.title }}</span> &rarr;
            <span style="color: #42a5f5">{{ quiz.name }}</span> <br />
            🎉 Quiz Time! Good luck! 🍀
        </h2>
        <div v-if="!quizHistory && timeDuration" class="time-left" :class="{ danger: timeDuration < 60 }">
            ⏰ Time Left: {{ formatTime }}
        </div>
        <div v-if="quizHistory">
            <span class="score">Score: {{ quizHistory.score }}/{{ questionCount }}</span>
            <button class="back-btn" @click="back()">🔙 Back to quizzes</button>
        </div>
    </div>
    <div class="quiz-questions" :class="{ 'blur-bg': submitted }">
        <div v-for="(question, index) in questionList" :key="index" class="question-card">
            <div class="question-row">
                <p class="question-text">Q{{ index + 1 }}: {{ question.question }}</p>
                <span class="marks">{{ question.marks }} marks</span>
            </div>
            <ul class="options-list">
                <li v-for="(option, idx) in question.options" :key="idx" class="option-item"
                    :class="{ selected: getSelectedOption(index) === idx }"
                    @click="!quizHistory && toggleOption(index, idx)">
                    <span class="option-label">{{ String.fromCharCode(65 + idx) }}.</span>
                    {{ option.text }}
                    <span v-if="getSelectedOption(index) === idx" class="selected-emoji">✅</span>
                </li>
            </ul>
        </div>
        <AppButton v-if="!quizHistory" type="primary" class="submit-btn" @click="submitQuiz" :disabled="submitted">
            {{ submitted ? "Submitted! 🎉" : "🚀 Submit Answers" }}
        </AppButton>
    </div>

    <div v-if="submitted" class="quiz-submitted kid-center">
        <h2>🎉 Quiz Submitted! 🎉</h2>
        <p>You scored {{ score }}/{{ totalMarks }}</p>
        <p>
            Thank you for participating!<br />Your answers have been recorded.<br />🌟 Great
            job! 🌟
        </p>
        <AppButton type="secondary" @click="router.push({ name: 'child_quizzes' })">
            ⬅️ Back to quizzes
        </AppButton>
    </div>
</template>

<script setup lang="ts">
import AppButton from "@/components/AppButton.vue";
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { base_url } from "../../router";

// --- SETUP ---
const router = useRouter();
const route = useRoute();

// --- STATE ---
const timer = ref<ReturnType<typeof setInterval> | null>(null);
const submitted = ref(false);
const loading = ref(true);
const error = ref<string | null>(null);

const curriculum = ref<any>({});
const lesson = ref<any>({});
const quiz = ref<any>({});
const questionList = ref<any[]>([]);
const quizHistory = ref<any>(null);
const timeDuration = ref<number | null>(null);
const score = ref<number | null>(null);
const totalMarks = ref<number | null>(null)

// length of questionList
const questionCount = computed(() => questionList.value.length || 0);

const selectedOptions = ref<{ [key: number]: number }>({}); // key: 0-based question index, value: 0-based option index
const quizHistoryAnswers = ref<{ [key: number]: number }>({}); // key: 0-based question index, value: 0-based option index

// --- METHODS ---

function back() {
    router.push({ name: 'child_quizzes' });
}


function toggleOption(question_index: number, optIdx: number) {
    if (selectedOptions.value[question_index] === optIdx) {
        selectedOptions.value[question_index] = undefined;
    } else {
        selectedOptions.value[question_index] = optIdx;
    }
}

function getSelectedOption(question_index: number, optIdx?: number) {
    // If optIdx is provided, apply toggle logic
    if (typeof optIdx === 'number') {
        if (selectedOptions.value[question_index] === optIdx) {
            selectedOptions.value[question_index] = undefined;
        } else {
            selectedOptions.value[question_index] = optIdx;
        }
    }
    return selectedOptions.value[question_index];
}

function clearTimer() {
    if (timer.value) {
        clearInterval(timer.value);
        timer.value = null;
    }
}

function handleTimeUp() {
    if (!submitted.value) {
        alert("Time's up! Submitting your answers automatically.");
        submitQuiz();
    }
}

// --- API INTEGRATION ---

async function fetchQuizData() {
    loading.value = true;
    error.value = null;
    const { curriculumId, lessonId, quizId, quizHistoryId } = route.params;

    if (!curriculumId || !lessonId || !quizId) {
        error.value =
            "Required information (curriculum, lesson, or quiz ID) is missing from the URL.";
        loading.value = false;
        return;
    }

    try {
        const token = localStorage.getItem("authToken");
        if (!token) throw new Error("Authentication token not found.");

        if (!quizHistoryId) {

            const url = `${base_url}api/child/curriculum/${curriculumId}/lesson/${lessonId}/quiz/${quizId}`;
            const response = await fetch(url, {
                headers: { Authorization: `Bearer ${token}` },
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(
                    errData.error || `Failed to fetch quiz data (status ${response.status})`
                );
            }

            const data = await response.json();
            curriculum.value = data.curriculum;
            lesson.value = data.lesson;
            quiz.value = data.quizzes; // API returns 'quizzes' object for the single quiz
            questionList.value = data.questions;

            // Handle time duration
            if (quiz.value.time_duration) {
                // Assuming format is like "5 mins" or just a number in seconds
                const durationString = String(quiz.value.time_duration);
                const parsedSeconds = parseInt(durationString, 10);

                // If it's a string like "5 mins", convert to seconds
                if (durationString.toLowerCase().includes("min")) {
                    timeDuration.value = parsedSeconds * 60;
                } else if (!isNaN(parsedSeconds)) {
                    // If it's just a number, assume it's already in seconds
                    timeDuration.value = parsedSeconds;
                }
            }
        } else {
            const url = `${base_url}api/child/curriculum/${curriculumId}/lesson/${lessonId}/quiz/${quizId}/quiz_history/${quizHistoryId}`;
            const response = await fetch(url, {
                headers: { Authorization: `Bearer ${token}` },
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(
                    errData.error || `Failed to fetch quiz history (status ${response.status})`
                );
            }

            const data = await response.json();
            curriculum.value = data.curriculum;
            lesson.value = data.lesson;
            quiz.value = data.quizzes;
            questionList.value = data.questions;
            quizHistory.value = data.quiz_history;
            console.log("Quiz history data:", quizHistory.value);
            quizHistoryAnswers.value = data.quiz_history.responses || {};

        }
    } catch (e: any) {
        error.value = e.message;
    } finally {
        loading.value = false;
    }
}

async function submitQuiz() {
    if (submitted.value) return;

    clearTimer();
    const { quizId } = route.params;
    if (!quizId) {
        error.value = "Quiz ID is missing, cannot submit.";
        return;
    }

    // Backend expects question keys to be 1-based index as strings
    const answersPayload: Record<string, string> = {};
    for (const [qIndexStr, oIndex] of Object.entries(selectedOptions.value)) {
        const questionIndex = parseInt(qIndexStr, 10);
        answersPayload[String(questionIndex)] = String(oIndex);
    }

    console.log("Submitting answers:", answersPayload);

    try {
        const token = localStorage.getItem("authToken");
        if (!token) throw new Error("Authentication token not found.");

        const response = await fetch(`${base_url}api/child/quizzes/${quizId}/submit`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ answers: answersPayload }),
        });

        const data = await response.json();

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.error || "Failed to submit the quiz.");
        }

        score.value = data.score;
        totalMarks.value = data.total_score;
        submitted.value = true;
    } catch (e: any) {
        alert(`Submission failed: ${e.message}`);
        console.error("Quiz submission error:", e);
    }
}

// --- COMPUTED & LIFECYCLE ---

const formatTime = computed(() => {
    if (timeDuration.value === null) return "";
    const minutes = Math.floor(timeDuration.value / 60);
    const seconds = timeDuration.value % 60;
    return `${minutes} min ${seconds.toString().padStart(2, "0")} sec`;
});

onMounted(async () => {
    await fetchQuizData();

    // If in history mode, populate quizHistoryAnswers from API and toggle those options
    if (quizHistory.value) {
        // Use 'responses' field for answers if present
        const responses = quizHistory.value.responses || quizHistory.value.answers;
        if (responses) {
            quizHistoryAnswers.value = responses;
            Object.entries(responses).forEach(([qIdx, optIdx]) => {
                selectedOptions.value[Number(qIdx)] = Number(optIdx);
            });
        }
    } else {
        // Start timer only if timeDuration is a valid number
        if (typeof timeDuration.value === "number" && timeDuration.value > 0) {
            timer.value = setInterval(() => {
                if (timeDuration.value! > 0) {
                    timeDuration.value!--;
                } else {
                    handleTimeUp();
                }
            }, 1000);
        }
    }
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
    font-family: "VAGRoundedNext";
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
    border-radius: calc(var(--border-radius) / 2);
    padding: 6px 18px;
    box-shadow: 0 1px 4px rgba(255, 193, 7, 0.08);
    margin-left: 10px;
    transition: color 0.3s, background 0.3s;
}

.back-btn {
    padding: 10px 20px;
    border: none;
    border-radius: calc(var(--border-radius) / 2);
    background-color: #ffe082;
    font-size: var(--font-sm);
    color: #bf360c;
    font-family: "VAGRoundedNext";
    font-weight: bold;
    cursor: pointer;
    transition: background 0.3s;
}

.time-left.danger {
    color: #d32f2f;
    background: #ffebee;
    animation: blink 1s steps(2, start) infinite;
}

.score {
    color: #4a148c;
    font-size: var(--font-md);
    font-family: "VAGRoundedNext";
    margin-right: 10px;
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
    box-shadow: 0 2px 8px rgba(255, 193, 7, 0.1);
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
    font-family: "VAGRoundedNext";
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
    font-family: "VAGRoundedNext";
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
    font-family: "Delius", cursive;
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
    font-family: "VAGRoundedNext";
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
    font-family: "VAGRoundedNext";
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
    font-family: "Comic Sans MS", "Delius", cursive;
    min-width: 320px;
    max-width: 90vw;
    animation: pop-in 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55);
}

.quiz-submitted.kid-center h2 {
    color: #ff9800;
    font-family: "VAGRoundedNext", cursive;
    font-size: 2.2rem;
    margin-bottom: 18px;
    letter-spacing: 1px;
}

.quiz-submitted.kid-center p {
    color: #4a148c;
    font-size: 1.25rem;
    margin-bottom: 28px;
    font-family: "Delius", cursive;
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
