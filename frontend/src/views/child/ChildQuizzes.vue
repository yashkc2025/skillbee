<template>
    <ChildAppLayout>
        <div class="quizzes" :class="{ 'blur-bg': selectedQuiz }">
            <!-- <div class="top-section">
                <h2 class="ft-head-1">✨ Let’s Take the Quiz for {{ lesson.name }} in {{ curriculum.name }}! 🧩</h2>
                <input type="text" v-model="searchInput" placeholder="Type to find a quiz... 🕵️‍♂️"
                    class="search-box" />
            </div> -->
            <AnimatedHeader v-model="searchInput" :heading-messages="[
                `✨ Let’s take the ${lesson.name} quiz in ${curriculum.name}! 🧩`,
                '🚀 Tap a quiz to begin your challenge! 🎯'
            ]" :placeholder-messages="['Type to find a quiz... 🕵️‍♂️']" :typing-speed="50" :pause-duration="1500" />
            <div class="card-item">
                <div v-for="quiz in filteredQuizzes" :key="quiz.quiz_id">
                    <ModuleCard :image="quiz.image" :name="quiz.name" :description="quiz.description"
                        :progress-status="quiz.progress_status" not-started-label="🚀 Start Quiz!"
                        completed-label="🏅 Quiz Attempted!" :show-buttons="true"
                        :primary-label="quiz.progress_status === 100 ? '🔁 Reattempt' : '📝 Attempt'"
                        secondary-label="📜 History" @primary="openQuiz(quiz)"
                        @secondary="openQuizHistory(quiz), moduleHistory = true" @click="openQuiz(quiz)">
                        <div class="extra">
                            <p class="time-duration">You have {{ quiz.time_duration }} to finish the quiz!</p>
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

        <div :class="['quiz-info', { 'show-info': selectedQuiz }]" v-if="selectedQuiz">
            <h2 class="quiz-name">{{ selectedQuiz.name }}</h2>
            <button class="back-btn" v-if="moduleHistory"
                @click="selectedQuiz = null; showHistory = false; moduleHistory = false">🔙 Back to Quizzes</button>
            <button class="back-btn" v-if="selectedQuiz && showHistory === false && moduleHistory === false"
                @click="selectedQuiz = null; showHistory = false">🔙 Back to Quizzes</button>
            <button v-if="selectedQuiz && showHistory === true && moduleHistory === false" class="back-btn"
                @click="showHistory = false">🔙 Back to Info</button>
            <div v-if="showHistory" class="quiz-history">
                <h3>📚 Your Quiz Attempt History</h3>
                <div v-if="getQuizHistory(selectedQuiz.quiz_id).length > 0">
                    <div v-for="history in getQuizHistory(selectedQuiz.quiz_id)" :key="history.quiz_history_id"
                        class="history-card">
                        <div class="view-submission-btn-wrap">
                            <div class="attempted-datetime">🗓️ {{ formatDateTime(history.attempted_at) }}</div>
                            <button class="view-attempt" @click="viewSubmission(history)">
                                👀 View Attempt
                            </button>
                        </div>
                        <div class="quiz-history-details">
                            <p class="quiz-history-score">🏆 Score: {{ history.score }}</p>
                            <div class="feedback">
                                <div v-if="history.feedback.admin" class="feedback-admin">
                                    <span>👩‍🏫 <b>Admin:</b> {{ history.feedback.admin }}</span>
                                </div>
                                <div v-if="history.feedback.parent" class="feedback-parent">
                                    <span>👨‍👩‍👧 <b>Parent:</b> {{ history.feedback.parent }}</span>
                                </div>
                                <div v-if="!history.feedback.admin && !history.feedback.parent" class="no-feedback">
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
                <p>❓ Number of Questions: <b>{{ selectedQuiz.no_questions }}</b></p>
                <p>🏅 Total Marks: <b>{{ selectedQuiz.total_marks }}</b></p>
                <p>📢 <b>How to Play:</b></p>
                <ul>
                    <li>👀 Read every question carefully.</li>
                    <li>🖍️ Pick the best answer from the choices.</li>
                    <li>⏭️ You can skip and come back to questions later.</li>
                    <li>⏰ Don’t forget to submit your answers before time is up!</li>
                </ul>

                <div class="completed-buttons">
                    <p v-if="selectedQuiz && selectedQuiz.progress_status === 100" class="completed-quiz">
                        🎉 You have already completed this quiz! You can reattempt it if you want.
                    </p>
                    <div v-if="selectedQuiz" class="content-buttons">
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
import { ref, computed } from 'vue';
import ChildAppLayout from '@/layouts/ChildAppLayout.vue';
import AnimatedHeader from '@/components/child/AnimatedHeader.vue';
import ModuleCard from '@/components/ModuleCard.vue';
import AppButton from '@/components/AppButton.vue';
import { searchQuery } from '@/fx/utils';
import { useRouter } from 'vue-router';

const router = useRouter();

const curriculum = { curriculum_id: 1, name: 'XYZ' };
const lesson = { lesson_id: 1, name: 'ABC' };
const quizzes = [
    {
        quiz_id: 1,
        name: 'Quiz 1',
        description: 'Description for Quiz 1',
        time_duration: '5 mins',
        difficulty: 'Easy',
        progress_status: 100,
        image: '/files/quiz1.jpeg',
        no_questions: 5,
        total_marks: 50
    },
    {
        quiz_id: 2,
        name: 'Quiz 2',
        description: 'Description for Quiz 2',
        time_duration: '2 mins',
        difficulty: 'Medium',
        progress_status: 0,
        image: '/files/quiz2.png',
        no_questions: 8,
        total_marks: 80
    },
    {
        quiz_id: 3,
        name: 'Quiz 3',
        description: 'Description for Quiz 3',
        time_duration: '10 mins',
        difficulty: 'Hard',
        progress_status: 100,
        image: '/files/quiz3.png',
        no_questions: 7,
        total_marks: 70
    },
    {
        quiz_id: 4,
        name: 'Quiz 4',
        description: 'Description for Quiz 4',
        time_duration: '15 mins',
        difficulty: 'Medium',
        progress_status: 0,
        image: '/files/quiz4.jpeg',
        no_questions: 6,
        total_marks: 60
    }
];

const quiz_history = [
    {
        quiz_history_id: 1,
        quiz_id: 1,
        quiz_name: 'Quiz 1',
        attempted_at: '2023-10-01T10:00:00Z',
        score: 30,
        feedback: {
            admin: 'Attempt Good',
            parent: 'Attempt again'
        }
    },
    {
        quiz_history_id: 2,
        quiz_id: 1,
        quiz_name: 'Quiz 1',
        attempted_at: '2023-10-02T11:30:00Z',
        score: 50,
        feedback: {
            admin: 'Well done!',
            parent: 'Great effort!'
        }
    },
    {
        quiz_history_id: 3,
        quiz_id: 3,
        quiz_name: 'Quiz 3',
        attempted_at: '2023-10-03T14:15:00Z',
        score: 10,
        feedback: {
            admin: 'Excellent work!',
            parent: 'Proud of you!'
        }
    },
    {
        quiz_history_id: 4,
        quiz_id: 3,
        quiz_name: 'Quiz 3',
        attempted_at: '2023-10-04T16:45:00Z',
        score: 40,
        feedback: {
            admin: 'Good attempt!',
            parent: 'Keep it up!'
        }
    }
];

const moduleHistory = ref(false);
const showHistory = ref(false);
const selectedQuiz = ref<null | typeof quizzes[0]>(null);

const searchInput = ref('');
const filteredQuizzes = computed(() => {
    return searchQuery(quizzes, searchInput.value, ['name', 'description', 'difficulty']);
});

const getQuizHistory = (quizId: number) => {
    return quiz_history.filter(sub => sub.quiz_id === quizId);
};

const getDifficultyStyle = (difficulty: string) => {
    switch (difficulty?.toLowerCase()) {
        case 'easy': return { color: '#4CAF50', emoji: '😊' };
        case 'medium': return { color: '#ffa14f', emoji: '🤔' };
        case 'hard': return { color: '#F44336', emoji: '🧠' };
        default: return { color: '#9E9E9E', emoji: '❓' };
    }
};

function openQuiz(quiz: typeof quizzes[0]) {
    selectedQuiz.value = quiz;
    showHistory.value = false;
}

function openQuizHistory(quiz: typeof quizzes[0]) {
    selectedQuiz.value = quiz;
    showHistory.value = true;
}

function attemptQuiz(quiz: typeof quizzes[0]) {
    router.push({
        name: 'child_quiz_attempt',
        params: { quizId: quiz.quiz_id, quizName: quiz.name, lessonId: lesson.lesson_id, curriculumId: curriculum.curriculum_id }
    });
}

function viewSubmission(history: typeof quiz_history[0]) {
    // Implement logic to view quiz attempt details
    alert(`Viewing attempt for: ${history.quiz_name} (ID: ${history.quiz_history_id})`);
}

function formatDateTime(dateStr: string) {
    const date = new Date(dateStr);
    const day = date.getDate().toString().padStart(2, '0');
    const month = date.toLocaleString('en-US', { month: 'short' });
    const year = date.getFullYear();
    let hours = date.getHours();
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    return `${day} / ${month} / ${year} ${hours}:${minutes} ${ampm}`;
}
</script>

<style scoped>
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
    max-height: 80vh;
    padding: 20px 24px 20px;
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
    padding: 18px 20px;
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
    padding: 0 20px;
    box-shadow: 0 2px 8px rgba(255, 193, 7, 0.13);
    transition: background 0.2s;
}

.view-attempt:hover {
    background: linear-gradient(90deg, #ffe082 0%, #ffd54f 100%);
    color: #d84315;
}

.attempted-datetime {
    color: #ffb300;
    font-weight: bold;
    margin-bottom: 6px;
}

.quiz-history-details {
    margin-top: 6px;
    margin-bottom: 4px;
    padding-left: 8px;
}

.quiz-history-score {
    color: #388e3c;
    font-weight: bold;
    margin-bottom: 4px;
}

.feedback-admin span {
    color: #4caf50;
}

.feedback-parent span {
    color: #1976d2;
}

.no-feedback span {
    color: #bdbdbd;
}

.no-history {
    text-align: center;
    color: #bdbdbd;
    font-size: 1.1rem;
    margin-top: 10px;
}
</style>