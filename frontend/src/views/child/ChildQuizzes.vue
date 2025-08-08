<template>
    <ChildAppLayout>
        <div class="quizzes" :class="{ 'blur-bg': selectedQuiz }">
            <AnimatedHeader v-model="searchInput" :heading-messages="[
                `✨ Let’s take the ${lesson.name} quiz in ${curriculum.name}! 🧩`,
                '🚀 Tap a quiz to begin your challenge! 🎯'
            ]" :placeholder-messages="['Type to find a quiz... 🕵️‍♂️']" :typing-speed="50" :pause-duration="1500" />

            <div v-if="!isLoading && !error">
                <div class="card-item">
                    <div v-for="quiz in filteredQuizzes" :key="quiz.quiz_id">
                        <ModuleCard :image="quiz.image" :name="quiz.name" :description="quiz.description"
                            :progress-status="quiz.progress_status" not-started-label="🚀 Start Quiz!"
                            completed-label="🏅 Quiz Attempted!" :show-buttons="true"
                            :primary-label="quiz.progress_status === 100 ? '🔁 Reattempt' : '📝 Attempt'"
                            secondary-label="📜 History" @primary="openQuiz(quiz)" @secondary="openQuizHistory(quiz)"
                            @click="openQuiz(quiz)">
                            <div class="extra">
                                <p class="time-duration">You have
                                    {{ quiz.time_duration ? quiz.time_duration : 'no time-limit' }}
                                    to finish the quiz!</p>
                                <p class="card-quiz-difficulty"
                                    :style="{ color: getDifficultyStyle(quiz.difficulty).color }">
                                    Difficulty: {{ quiz.difficulty || 'Unknown' }}
                                </p>
                            </div>
                        </ModuleCard>
                    </div>
                </div>
                <p v-if="quizzes.length === 0" class="empty-result">
                    No quizzes in this lesson yet. Please check back later.
                </p>
                <p v-if="filteredQuizzes.length === 0 && quizzes.length > 0" class="empty-result">
                    No Quizzes found matching your search. Please try a different keyword.
                </p>
                <p v-if="filteredQuizzes.length !== 0 && quizzes.length !== 0" class="empty-result">
                    Tip: Click on a quiz to start!
                </p>
            </div>

            <div v-if="isLoading" class="loading-state">Loading quizzes...</div>
            <div v-if="error" class="error-state">
                <p>😕 Oops! Could not load quizzes. {{ error }}</p>
                <button @click="fetchQuizzes" class="retry-button">Try Again</button>
            </div>
        </div>

        <div :class="['quiz-info', { 'show-info': selectedQuiz }]" v-if="selectedQuiz">
            <h2 class="quiz-name">{{ selectedQuiz.name }}</h2>
            <button class="back-btn" @click="closePanel">🔙 Back to Quizzes</button>

            <div v-if="showHistory" class="quiz-history">
                <h3>📚 Your Quiz Attempt History</h3>
                <div v-if="isHistoryLoading" class="loading-state">Loading history...</div>
                <div v-else-if="quizHistory.length > 0">
                    <div v-for="history in quizHistory" :key="history.quiz_history_id" class="history-card">
                        <div class="view-submission-btn-wrap">
                            <div class="attempted-datetime">🗓️ {{ formatDateTime(history.attempted_at) }}</div>
                            <button class="view-attempt" @click="viewSubmission(history)">
                                👀 View Attempt
                            </button>
                        </div>
                        <div class="quiz-history-details">
                            <p class="quiz-history-score">🏆 Score: {{ history.score }}</p>
                            <div class="feedback">
                                <div v-if="history.feedback?.admin" class="feedback-admin">
                                    <span>👩‍🏫 <b>Admin:</b> {{ history.feedback.admin }}</span>
                                </div>
                                <div v-if="history.feedback?.parent" class="feedback-parent">
                                    <span>👨‍👩‍👧 <b>Parent:</b> {{ history.feedback.parent }}</span>
                                </div>
                                <div v-if="!history.feedback?.admin && !history.feedback?.parent" class="no-feedback">
                                    <span>📝 No feedback yet.</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else class="no-history">
                    <span>😅 No quiz attempts yet! Try attempting a quiz.</span>
                </div>
            </div>

            <div v-if="!showHistory">
                <p class="quiz-description">📝 {{ selectedQuiz.description }}</p>
                <p class="quiz-duration">⏳ You have <b>{{ selectedQuiz.time_duration }}</b> to finish this quiz!</p>
                <p class="quiz-difficulty" :style="{ color: getDifficultyStyle(selectedQuiz.difficulty).color }">
                    💪 Level: {{ selectedQuiz.difficulty || 'Unknown' }}
                    <span class="emoji">{{ getDifficultyStyle(selectedQuiz.difficulty).emoji }}</span>
                </p>
                <p class="no-questions">❓ Number of Questions: <b>{{ selectedQuiz.no_questions }}</b></p>
                <p class="total-marks">🏅 Total Marks: <b>{{ selectedQuiz.total_marks }}</b></p>
                <p>📢 <b>How to Play:</b></p>
                <ul>
                    <li>👀 Read every question carefully.</li>
                    <li>🖍️ Pick the best answer from the choices.</li>
                    <li>⏭️ You can skip and come back to questions later.</li>
                    <li>⏰ Don’t forget to submit your answers before time is up!</li>
                </ul>
                <div class="completed-buttons">
                    <p v-if="selectedQuiz.progress_status === 100" class="completed-quiz">
                        🎉 You have already completed this quiz! You can reattempt it if you want.
                    </p>
                    <div class="content-buttons">
                        <AppButton type="primary" class="primary" @click="attemptQuiz(selectedQuiz)">📝 Start Quiz
                        </AppButton>
                        <AppButton type="secondary" class="secondary" @click="openQuizHistory(selectedQuiz)">📜 View
                            History</AppButton>
                    </div>
                </div>
            </div>
        </div>
    </ChildAppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import ChildAppLayout from '@/layouts/ChildAppLayout.vue';
import AnimatedHeader from '@/components/child/AnimatedHeader.vue';
import ModuleCard from '@/components/ModuleCard.vue';
import AppButton from '@/components/AppButton.vue';
import { searchQuery } from '@/fx/utils';
import { base_url } from '../../router';


// --- INTERFACES for API data ---
interface CurriculumInfo {
    curriculum_id: number;
    name: string;
}

interface LessonInfo {
    lesson_id: number;
    name: string;
}

interface Quiz {
    quiz_id: number;
    name: string;
    description: string;
    time_duration: string;
    difficulty: string;
    progress_status: number;
    image: string | null;
    no_questions: number;
    total_marks: number;
}

interface QuizHistoryItem {
    quiz_history_id: number;
    quiz_id: number;
    quiz_name: string;
    attempted_at: string;
    score: number;
    feedback: {
        admin: string | null;
        parent: string | null;
    };
}

// --- COMPONENT STATE ---
const router = useRouter();
const route = useRoute();

const curriculum = ref<CurriculumInfo>({ curriculum_id: Number(route.params.curriculumId), name: route.params.curriculumName as string });
const lesson = ref<LessonInfo>({ lesson_id: Number(route.params.lessonId), name: route.params.lessonName as string });
const quizzes = ref<Quiz[]>([]);
const quizHistory = ref<QuizHistoryItem[]>([]);
const selectedQuiz = ref<Quiz | null>(null);

const searchInput = ref('');
const showHistory = ref(false);

// --- UI STATE ---
const isLoading = ref(true);
const isHistoryLoading = ref(false);
const error = ref<string | null>(null);

// --- COMPUTED PROPERTIES ---
const filteredQuizzes = computed(() => {
    return searchQuery(quizzes.value, searchInput.value, ['name', 'description', 'difficulty']);
});

// --- API & DATA HANDLING ---
async function fetchQuizzes() {
    isLoading.value = true;
    error.value = null;
    try {
        const token = localStorage.getItem('authToken');
        if (!token) throw new Error("Authentication token not found.");

        const response = await fetch(`${base_url}api/child/lesson/${lesson.value.lesson_id}/quizzes`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        if (!response.ok) throw new Error(`Failed to fetch quizzes (status ${response.status})`);

        const data = await response.json();
        curriculum.value = data.curriculum;
        lesson.value = { ...data.lesson, name: data.lesson.title }; // Map API's 'title' to component's 'name'
        quizzes.value = data.quizzes;

    } catch (e: any) {
        error.value = e.message;
        quizzes.value = [];
    } finally {
        isLoading.value = false;
    }
}

async function fetchQuizHistory(quizId: number) {
    isHistoryLoading.value = true;
    quizHistory.value = [];
    try {
        const token = localStorage.getItem('authToken');
        if (!token) throw new Error("Authentication token not found.");

        const response = await fetch(`${base_url}api/child/quiz/${quizId}/history`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        if (!response.ok) throw new Error(`Failed to fetch quiz history (status ${response.status})`);

        const data = await response.json();
        quizHistory.value = data.quizzes_history;

    } catch (e: any) {
        console.error("Error fetching quiz history:", e.message);
        quizHistory.value = [];
    } finally {
        isHistoryLoading.value = false;
    }
}

// --- METHODS (Template Interactions) ---
function openQuiz(quiz: Quiz) {
    selectedQuiz.value = quiz;
    showHistory.value = false;
}

function openQuizHistory(quiz: Quiz) {
    selectedQuiz.value = quiz;
    showHistory.value = true;
    fetchQuizHistory(quiz.quiz_id);
}

function closePanel() {
    selectedQuiz.value = null;
    showHistory.value = false;
    quizHistory.value = [];
}

function attemptQuiz(quiz: Quiz) {
    router.push({
        name: 'child_quiz_attempt',
        params: {
            quizId: quiz.quiz_id,
            quizName: quiz.name,
            lessonId: lesson.value.lesson_id,
            curriculumId: curriculum.value.curriculum_id
        }
    });
}

function viewSubmission(history: QuizHistoryItem) {
    // There is no backend endpoint for viewing a specific attempt's details.
    // This function will remain as an alert.
    alert(`Viewing attempt for: ${history.quiz_name} (ID: ${history.quiz_history_id}) with score: ${history.score}`);
}

// --- FORMATTERS & HELPERS ---
const getDifficultyStyle = (difficulty: string) => {
    switch (difficulty?.toLowerCase()) {
        case 'easy': return { color: '#4CAF50', emoji: '😊' };
        case 'medium': return { color: '#ffa14f', emoji: '🤔' };
        case 'hard': return { color: '#F44336', emoji: '🧠' };
        default: return { color: '#9E9E9E', emoji: '❓' };
    }
};

function formatDateTime(dateStr: string) {
    if (!dateStr || dateStr === "N/A") return "Date not available";
    const options: Intl.DateTimeFormatOptions = {
        day: '2-digit', month: 'short', year: 'numeric',
        hour: '2-digit', minute: '2-digit', hour12: true
    };
    return new Date(dateStr).toLocaleString('en-US', options).replace(',', ' at');
}

// --- LIFECYCLE HOOK ---
onMounted(() => {
    fetchQuizzes();
});
</script>

<style scoped>
/* All scoped styles remain unchanged as per the original file */
.loading-state,
.error-state {
    text-align: center;
    padding: 40px 20px;
    font-size: 1.2rem;
    color: #666;
}

.retry-button {
    margin-top: 15px;
    padding: 10px 20px;
    border: none;
    background-color: var(--color-primary, #007bff);
    color: white;
    border-radius: var(--border-radius, 8px);
    cursor: pointer;
    font-family: "VAGRoundedNext";
}

.card-item {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 20px;
    padding: 20px;
}

.extra {
    font-size: var(--font-md);
    margin-top: -15px;
    color: #00796b;
    margin-bottom: 10px;
    padding: 0 15px;
    min-height: 40px;
}

.card-quiz-difficulty {
    line-height: 40px;
    margin-top: 5px;
}

.empty-result {
    margin-top: 20px;
    text-align: center;
    padding-bottom: 30px;
}

.quiz-info {
    position: fixed;
    top: 52%;
    left: 50%;
    transform: translate(-50%, 100%);
    opacity: 0;
    width: 80%;
    max-width: 900px;
    max-height: 80vh;
    padding: 20px 24px;
    border-radius: var(--border-radius);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    background: #fff3e0;
    font-family: 'Delius';
    font-size: var(--font-ml-lg);
    overflow-y: auto;
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: -100;
}

.quiz-info.show-info {
    transform: translate(-50%, -50%);
    opacity: 1;
    pointer-events: auto;
    z-index: 1000;
}

.quiz-name {
    color: #ff9800;
    margin-bottom: 12px;
    text-align: center;
    font-family: "VAGRoundedNext";
    padding-right: 150px;
}

.back-btn {
    position: absolute;
    top: 20px;
    right: 20px;
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

.back-btn:hover {
    background-color: #ffd54f;
}

.quiz-history {
    padding: 18px 0;
}

.quiz-history h3 {
    color: #ff9800;
    margin-bottom: 16px;
    font-family: 'VAGRoundedNext';
}

.completed-buttons {
    margin-top: 20px;
}

.completed-quiz {
    font-size: var(--font-sm);
    color: #2e7d32;
    background-color: #c8e6c9;
    padding: 8px 12px;
    border-radius: calc(var(--border-radius) / 2);
    text-align: center;
}

.content-buttons {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 20px;
}

.blur-bg {
    filter: blur(5px);
    pointer-events: none;
    user-select: none;
}

.history-card {
    background: #fff8e1;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 14px;
    box-shadow: 0 1px 6px rgba(255, 193, 7, 0.08);
}

.view-submission-btn-wrap {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.view-attempt {
    background-color: #ffe082;
    color: #bf360c;
    font-size: var(--font-sm);
    font-weight: bold;
    border-radius: calc(var(--border-radius) / 2);
    border: none;
    font-family: 'VAGRoundedNext';
    cursor: pointer;
    padding: 8px 16px;
    box-shadow: 0 2px 8px rgba(255, 193, 7, 0.13);
    transition: background 0.2s;
}

.view-attempt:hover {
    background-color: #ffd54f;
}

.attempted-datetime {
    color: #ffb300;
    font-weight: bold;
}

.quiz-history-details {
    margin-top: 6px;
    margin-bottom: 4px;
    padding-left: 8px;
    font-size: 0.95em;
}

.quiz-history-score {
    color: #388e3c;
    font-weight: bold;
    margin-bottom: 4px;
}

.feedback-admin span,
.feedback-parent span {
    display: block;
    margin-top: 4px;
}

.feedback-admin span {
    color: #4caf50;
}

.feedback-parent span {
    color: #1976d2;
}

.no-feedback span {
    color: #bdbdbd;
    font-style: italic;
}

.no-history {
    text-align: center;
    color: #bdbdbd;
    font-size: 1.1rem;
    margin-top: 10px;
    font-style: italic;
}

.quiz-description,
.quiz-duration,
.quiz-difficulty,
.no-questions,
.total-marks {
    margin-bottom: 0.5rem;
}

ul {
    padding-left: 50px;
}

li {
    margin-bottom: 0.5rem;
}
</style>