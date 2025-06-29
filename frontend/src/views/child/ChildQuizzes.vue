<template>
    <ChildAppLayout>
        <div class="quizzes">
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
                        secondary-label="📜 History">
                        <p class="time-duration"> You have {{ quiz.time_duration }} to finish the quiz! Let’s go!
                        </p>
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
                Tip: Click on an quiz to start!
            </p>
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
    },
    {
        quiz_id: 2,
        name: 'Quiz 2',
        description: 'Description for Quiz 2',
        time_duration: '2 min',
        difficulty: 'Medium',
        progress_status: 0,
        image: '/files/quiz2.png',
    },
    {
        quiz_id: 3,
        name: 'Quiz 3',
        description: 'Description for Quiz 3',
        time_duration: '10 mins',
        difficulty: 'Hard',
        progress_status: 100,
        image: '/files/quiz3.png',
    },
    {
        quiz_id: 4,
        name: 'Quiz 4',
        description: 'Description for Quiz 4',
        time_duration: '15 mins',
        difficulty: 'Medium',
        progress_status: 0,
        image: '/files/quiz4.jpeg',
    }
];

const searchInput = ref('');
const filteredQuizzes = computed(() => {
    return searchQuery(quizzes, searchInput.value, ['name', 'description', 'difficulty']);
});

</script>

<style>
.time-duration {
    font-size: var(--font-md);
    margin-top: -15px;
    color: #00796b;
    margin-bottom: 10px;
    padding: 0 15px;
    min-height: 40px;
}
</style>