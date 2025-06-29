<template>
    <ChildAppLayout>
        <div class="activities" :class="{ 'blur-bg': selectedActivity }">
            <div class="top-section">
                <h2 class="ft-head-1">🎉 Let’s Have Fun with the {{ lesson.name }} Activity from {{ curriculum.name }}!
                </h2>
                <input type="text" v-model="searchInput" placeholder="Type to find a activity… 🕵️‍♂️"
                    class="search-box" />
            </div>
            <div class="card-item">
                <div v-for="activity in filteredActivities" :key="activity.activity_id">
                    <ModuleCard @click="openActivity(activity)" :image="activity.image" :name="activity.name"
                        :description="activity.description" :show-buttons="true"
                        :primary-label="activity.progress_status === 100 ? '📤 Reupload' : '📤 Upload'"
                        secondary-label="📜 History" :progress-status="activity.progress_status"
                        not-started-label="🔍 Let's Explore!" completed-label="🏆 Activity Mastered!"
                        @primary="uploadActivity(activity.activity_id)">
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
                <strong>Tip:</strong> Click on an activity to view details and upload your work!
            </p>
        </div>

        <div :class="['activity-contents', { 'show-content': selectedActivity }]">
            <h2 class="activity-name">🎯 {{ selectedActivity?.name }}</h2>
            <button class="back-btn" @click="selectedActivity = null">🔙 Back to Activities</button>
            <p class="activity-description">📝 {{ selectedActivity?.description }}</p>
            <p>📋 {{ selectedActivity?.instruction }}</p>
            <p class="activity-difficulty">
                💪 Difficulty:
                <span :style="{ color: getDifficultyStyle(selectedActivity?.difficulty).color }">
                    {{ getDifficultyStyle(selectedActivity?.difficulty).emoji }}
                    {{ selectedActivity?.difficulty || 'Unknown' }}
                </span>
            </p>

            <div class="completed-buttons">
                <p v-if="selectedActivity && selectedActivity.progress_status === 100" class="completed-activity">
                    🎉 Activity Completed! You can re-upload your work if needed.
                </p>
                <div v-if="selectedActivity" class="content-buttons">
                    <AppButton type="primary" @click="uploadActivity(selectedActivity.activity_id)">
                        {{ selectedActivity.progress_status === 0 ? '📤 Upload' : '📤 Reupload' }}
                    </AppButton>
                    <AppButton type="secondary" @click="openActivity(selectedActivity)">
                        📜 History
                    </AppButton>

                </div>
            </div>
        </div>
    </ChildAppLayout>

</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import ChildAppLayout from '@/layouts/ChildAppLayout.vue';
import ModuleCard from '@/components/ModuleCard.vue';
import AppButton from '@/components/AppButton.vue';
import { searchQuery } from '@/fx/utils';
import { useRouter } from 'vue-router';

const router = useRouter();

const curriculum = { curriculum_id: 1, name: 'XYZ' };
const lesson = { lesson_id: 1, name: 'ABC' };
const activities = [
    {
        activity_id: 1,
        name: 'Activity 1',
        description: 'Description for Activity 1',
        instruction: 'Draw a picture of your favorite animal and use three words to describe it.',
        difficulty: 'Easy',
        progress_status: 0,
        image: '/files/activity1.jpeg',
    },
    {
        activity_id: 2,
        name: 'Activity 2',
        description: 'Description for Activity 2',
        instruction: 'Find five objects in your room that are red. Line them up from smallest to largest.',
        difficulty: 'Medium',
        progress_status: 100,
        image: '/files/activity2.jpeg',
    },
    {
        activity_id: 3,
        name: 'Activity 3',
        description: 'Description for Activity 3',
        instruction: 'Create a treasure map for your backyard or living room. Write clues and draw symbols to help someone find the hidden treasure.',
        difficulty: 'Hard',
        progress_status: 100,
        image: '/files/activity3.png',
    },
    {
        activity_id: 4,
        name: 'Activity 4',
        description: 'Description for Activity 4',
        instruction: 'Listen to a short story. Retell the story in your own words using five sentences.',
        difficulty: 'Medium',
        progress_status: 100,
        image: '/files/activity4.jpeg',
    }
];

const searchInput = ref('');
const filteredActivities = computed(() =>
    searchQuery(activities, searchInput.value, ['name', 'description', 'difficulty'])
);

const fileInput = ref<HTMLInputElement | null>(null);
const selectedActivityId = ref<number | null>(null);

function uploadActivity(activityId: number) {
    selectedActivityId.value = activityId;
    if (fileInput.value) {
        fileInput.value.value = '';
        fileInput.value.click();
    }
}

async function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files || input.files.length === 0 || selectedActivityId.value === null) return;
    const file = input.files[0];
    const formData = new FormData();
    formData.append('file', file);
    formData.append('activity_id', selectedActivityId.value.toString());
}

const selectedActivity = ref<null | typeof activities[0]>(null);

function openActivity(activity: typeof activities[0]) {
    selectedActivity.value = activity;
}

const getDifficultyStyle = (difficulty: string) => {
    switch (difficulty?.toLowerCase()) {
        case 'easy': return { color: '#4CAF50', emoji: '😊' };
        case 'medium': return { color: '#ffa14f', emoji: '🤔' };
        case 'hard': return { color: '#F44336', emoji: '🧠' };
        default: return { color: '#9E9E9E', emoji: '❓' };
    }
};

</script>

<style scoped>
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
    padding: 0 20px;
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
}

.completed-buttons {
    margin-top: 20px;
}

.completed-activity {
    font-size: var(--font-sm);
    color: #2e7d32;
    background-color: #c8e6c9;
    padding: 8px 12px;
    border-radius: 10px;
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
</style>