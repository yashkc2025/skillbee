<template>
    <ChildAppLayout>
        <div class="activities" :class="{ 'blur-bg': selectedActivity }">
            <AnimatedHeader v-model="searchInput"
                :heading-messages="[`🎉 Let’s play the ${lesson.name} activity from ${curriculum.name}! 🌟`, '✨ Tap an activity to see details and upload your work! 🚀']"
                :placeholder-messages="['Type to find a activity… 🕵️‍♂️']" :typing-speed="50" :pause-duration="1500" />

            <div v-if="!isLoading && !error">
                <div class="card-item">
                    <div v-for="activity in filteredActivities" :key="activity.activity_id">
                        <ModuleCard @click="openActivity(activity)" :image="activity.image" :name="activity.name"
                            :description="activity.description" :show-buttons="true"
                            :primary-label="activity.progress_status === 100 ? '📤 Reupload' : '📤 Upload'"
                            secondary-label="📜 History" :progress-status="activity.progress_status"
                            not-started-label="🔍 Let's Explore!" completed-label="🏆 Activity Mastered!"
                            @primary="uploadActivity(activity.activity_id)"
                            @secondary="openActivitySubmissions(activity)">
                            <p class="card-activity-difficulty"
                                :style="{ color: getDifficultyStyle(activity.difficulty).color }"> Difficulty:
                                {{ activity.difficulty || 'Unknown' }}
                            </p>
                        </ModuleCard>
                    </div>
                </div>
                <input type="file" ref="fileInput" class="hidden" accept=".jpg,.jpeg,.png,.pdf"
                    @change="handleFileUpload" />

                <p v-if="activities.length === 0" class="empty-result">
                    No activities in this lesson yet. Please check back later.
                </p>
                <p v-if="filteredActivities.length === 0 && activities.length > 0" class="empty-result">
                    No activities found matching your search. Please try a different keyword.
                </p>
                <p v-if="filteredActivities.length !== 0 && activities.length !== 0" class="empty-result">
                    Tip: Click on an activity to view details and upload your work!
                </p>
            </div>

            <div v-if="isLoading" class="loading-state">Loading activities...</div>
            <div v-if="error" class="error-state">
                <p>😕 Oops! Could not load activities. {{ error }}</p>
                <button @click="fetchActivities" class="retry-button">Try Again</button>
            </div>
        </div>

        <div :class="['activity-contents', { 'show-content': selectedActivity }]" v-if="selectedActivity">
            <h2 class="activity-name">🎯 {{ selectedActivity?.name }}</h2>
            <button class="back-btn" @click="closePanel">🔙 Back to Activities</button>

            <div v-if="showHistory" class="activity-history">
                <h3>📚 Your Activity History</h3>
                <div v-if="isHistoryLoading" class="loading-state">Loading history...</div>
                <div v-else-if="activityHistory.length > 0">
                    <div v-for="history in activityHistory" :key="history.activity_history_id" class="history-card">
                        <div class="view-submission-btn-wrap">
                            <div class="submission-datetime">🗓️ {{ formatDateTime(history.submitted_at) }}</div>
                            <button class="view-submission-btn" @click="viewSubmission(history)">
                                👀 View Submission
                            </button>
                        </div>
                        <div class="history-feedback">
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
                <div v-else class="no-history">
                    <span>😅 No submissions yet! Try uploading your work.</span>
                </div>
            </div>

            <div v-if="!showHistory">
                <p class="activity-description">📝 {{ selectedActivity?.description }}</p>
                <p class="activity-difficulty">
                    💪 Difficulty:
                    <span :style="{ color: getDifficultyStyle(selectedActivity?.difficulty).color }">
                        {{ getDifficultyStyle(selectedActivity?.difficulty).emoji }}
                        {{ selectedActivity?.difficulty || 'Unknown' }}
                    </span>
                </p>
                <div class="completed-buttons">
                    <p v-if="selectedActivity.progress_status === 100" class="completed-activity">
                        🎉 Activity Completed! You can re-upload your work if needed.
                    </p>
                    <div class="content-buttons">
                        <AppButton type="primary" @click="uploadActivity(selectedActivity.activity_id)">
                            {{ selectedActivity.progress_status === 0 ? '📤 Upload' : '📤 Reupload' }}
                        </AppButton>
                        <AppButton type="secondary" @click="openActivitySubmissions(selectedActivity)">
                            📜 History
                        </AppButton>
                    </div>
                </div>
            </div>
        </div>
    </ChildAppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import ChildAppLayout from '@/layouts/ChildAppLayout.vue';
import AnimatedHeader from '@/components/child/AnimatedHeader.vue';
import ModuleCard from '@/components/ModuleCard.vue';
import AppButton from '@/components/AppButton.vue';
import { searchQuery } from '@/fx/utils';
import { base_url } from '../../router';

// --- INTERFACES to match API responses ---
interface CurriculumInfo {
    curriculum_id: number;
    name: string;
}

interface LessonInfo {
    lesson_id: number;
    name: string; // Mapped from 'title' in API
}

interface Activity {
    activity_id: number;
    name: string;
    description: string;
    image: string | null;
    progress_status: number;
    // These fields are in the template but not the API response, so they are optional
    instruction?: string;
    difficulty?: 'Easy' | 'Medium' | 'Hard' | string;
}

interface ActivityHistoryItem {
    activity_history_id: number;
    activity_id: number;
    submitted_at: string;
    feedback: {
        admin?: string;
        parent?: string;
    } | null;
}


// --- COMPONENT STATE ---
const route = useRoute();
const curriculum = ref<CurriculumInfo>({ curriculum_id: Number(route.params.curriculumId), name: route.params.curriculumName as string });
const lesson = ref<LessonInfo>({ lesson_id: Number(route.params.lessonId), name: route.params.lessonName as string });
const activities = ref<Activity[]>([]);
const activityHistory = ref<ActivityHistoryItem[]>([]);
const selectedActivity = ref<Activity | null>(null);

const searchInput = ref('');
const fileInput = ref<HTMLInputElement | null>(null);
const selectedActivityIdForUpload = ref<number | null>(null);

// --- UI & PANEL STATE ---
const isLoading = ref(true);
const isHistoryLoading = ref(false);
const error = ref<string | null>(null);
const showHistory = ref(false);


// --- COMPUTED PROPERTIES ---
const filteredActivities = computed(() =>
    searchQuery(activities.value, searchInput.value, ['name', 'description', 'difficulty'])
);


// --- API & DATA HANDLING ---
async function fetchActivities() {
    isLoading.value = true;
    error.value = null;
    try {
        const token = localStorage.getItem('authToken');
        if (!token) throw new Error("Authentication token missing.");

        const response = await fetch(`${base_url}api/child/lesson/${lesson.value.lesson_id}/activities`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        if (!response.ok) throw new Error(`Failed to fetch activities (status ${response.status})`);

        const data = await response.json();
        curriculum.value = data.curriculum;
        lesson.value = { ...data.lesson, name: data.lesson.title }; // Map title to name
        activities.value = data.activities;

    } catch (e: any) {
        error.value = e.message;
        activities.value = [];
    } finally {
        isLoading.value = false;
    }
}

async function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length || selectedActivityIdForUpload.value === null) return;

    const file = input.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
        const token = localStorage.getItem('authToken');
        if (!token) throw new Error("Authentication token missing.");

        const response = await fetch(`${base_url}api/child/activity/${selectedActivityIdForUpload.value}/submit`, {
            method: 'POST',
            headers: { Authorization: `Bearer ${token}` },
            body: formData,
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.error || `Upload failed (status ${response.status})`);
        }

        alert('File uploaded successfully!');
        fetchActivities(); // Refresh list to show updated progress

    } catch (e: any) {
        alert(`Error uploading file: ${e.message}`);
    } finally {
        selectedActivityIdForUpload.value = null;
    }
}

async function fetchActivityHistory(activityId: number) {
    isHistoryLoading.value = true;
    activityHistory.value = [];
    try {
        const token = localStorage.getItem('authToken');
        if (!token) throw new Error("Authentication token missing.");

        const response = await fetch(`${base_url}api/child/activity/${activityId}/history`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        if (!response.ok) throw new Error(`Failed to fetch history (status ${response.status})`);

        const data = await response.json();
        activityHistory.value = data.activities_submission;
        console.log("Activity History:", activityHistory.value);
    } catch (e: any) {
        console.error("Error fetching history:", e.message);
    } finally {
        isHistoryLoading.value = false;
    }
}

async function viewSubmission(historyItem: ActivityHistoryItem) {
    try {
        const token = localStorage.getItem('authToken');
        if (!token) throw new Error("Authentication token missing.");

        const response = await fetch(`${base_url}api/child/activity/history/${historyItem.activity_history_id}`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        if (!response.ok) throw new Error(`Could not download file (status ${response.status})`);

        const blob = await response.blob();
        const contentDisposition = response.headers.get('content-disposition');
        let filename = `submission_${historyItem.activity_history_id}`;

        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename="(.+)"/);
            if (filenameMatch?.length === 2) filename = filenameMatch[1];
        }

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();

    } catch (e: any) {
        alert(`Error downloading submission: ${e.message}`);
    }
}


// --- METHODS (Template Interactions) ---
function uploadActivity(activityId: number) {
    selectedActivityIdForUpload.value = activityId;
    if (fileInput.value) {
        fileInput.value.value = ''; // Reset file input
        fileInput.value.click();
    }
}

function openActivity(activity: Activity) {
    selectedActivity.value = activity;
    showHistory.value = false;
}

function openActivitySubmissions(activity: Activity) {
    selectedActivity.value = activity;
    showHistory.value = true;
    fetchActivityHistory(activity.activity_id);
}

function closePanel() {
    selectedActivity.value = null;
    showHistory.value = false;
    activityHistory.value = [];
}

// --- FORMATTERS & HELPERS ---
function formatDateTime(dateString: string): string {
    const options: Intl.DateTimeFormatOptions = {
        day: '2-digit', month: 'short', year: 'numeric',
        hour: '2-digit', minute: '2-digit', hour12: true
    };
    return new Date(dateString).toLocaleString('en-US', options).replace(',', ' at');
}

const getDifficultyStyle = (difficulty?: string) => {
    switch (difficulty?.toLowerCase()) {
        case 'easy': return { color: '#4CAF50', emoji: '😊' };
        case 'medium': return { color: '#ffa14f', emoji: '🤔' };
        case 'hard': return { color: '#F44336', emoji: '🧠' };
        default: return { color: '#9E9E9E', emoji: '❓' };
    }
};

// --- LIFECYCLE HOOK ---
onMounted(() => {
    fetchActivities();
});
</script>

<style scoped>
/* Scoped styles remain unchanged as requested */
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

.top-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0 25px;
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

.card-item {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 20px;
    padding: 20px;
}

.card-activity-difficulty {
    font-size: var(--font-md);
    margin-top: -15px;
    margin-bottom: 10px;
    padding: 0 15px;
    min-height: 40px;
}

.hidden {
    display: none;
}

.empty-result {
    margin-top: 20px;
    text-align: center;
    padding-bottom: 30px;
}

.activity-contents {
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

.activity-contents.show-content {
    transform: translate(-50%, -50%);
    opacity: 1;
    pointer-events: auto;
    z-index: 1000;
}

.activity-contents .back-btn {
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

.activity-contents .back-btn:hover {
    background-color: #ffd54f;
}

.activity-name {
    color: #ff6f00;
    margin-bottom: 12px;
    text-align: center;
    font-family: "VAGRoundedNext";
    padding-right: 150px;
    /* Space for back button */
}

.completed-buttons {
    margin-top: 20px;
}

.completed-activity {
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

.activity-history {
    padding: 18px 0;
}

.activity-history h3 {
    color: #ff9800;
    margin-bottom: 16px;
    font-family: 'VAGRoundedNext';
}

.history-card {
    background: #fff8e1;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 14px;
    box-shadow: 0 1px 6px rgba(255, 193, 7, 0.08);
}

.submission-datetime {
    color: #ffb300;
    font-weight: bold;
    margin-bottom: 6px;
}

.feedback-admin,
.feedback-parent,
.no-feedback {
    margin-top: 8px;
    padding-left: 8px;
    font-size: 0.95em;
}

.no-feedback span {
    color: #9E9E9E;
    font-style: italic;
}

.feedback-admin span {
    color: #4caf50;
}

.feedback-parent span {
    color: #1976d2;
}

.no-history {
    text-align: center;
    color: #bdbdbd;
    margin-top: 10px;
    font-style: italic;
}

.view-submission-btn-wrap {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.view-submission-btn {
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

.view-submission-btn:hover {
    background-color: #ffd54f;
    color: #d84315;
}

.activity-description,
.activity-difficulty {
    margin-bottom: 1rem;
}
</style>