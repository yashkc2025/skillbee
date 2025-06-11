<template>
    <ChildAppLayout>
        <div class="lessons">
            <input type="text" v-model="searchInput" placeholder="Search Lessons..." class="search-box" />
            <Card :title="`Learn lessons of ${skillType.name}`">
                <CardItem v-for="lesson in filteredLessons" :key="lesson.lesson_id" @click="openLesson(lesson)"
                    class="card-item">
                    <h2 class="lesson-title"
                        :class="selectedLesson && selectedLesson.lesson_id === lesson.lesson_id ? 'lesson-title-cursor' : ''">
                        {{ lesson.title }}
                    </h2>
                    <div
                        :class="selectedLesson && selectedLesson.lesson_id === lesson.lesson_id ? 'content-buttons' : 'buttons'">
                        <button class="btn" @click.stop="goToActivities(lesson.lesson_id)">Activities</button>
                        <button class="btn" @click.stop="goToQuizzes(lesson.lesson_id)">Quizzes</button>
                        <button class="btn" :class="isLessonRead(lesson.lesson_id) ? 'marked-btn' : ''"
                            :disabled="isLessonRead(lesson.lesson_id)" @click.stop="markAsRead(lesson.lesson_id)">
                            {{ isLessonRead(lesson.lesson_id) ? 'Marked as read' : 'Mark as read' }}
                        </button>
                    </div>
                    <div v-if="selectedLesson && selectedLesson.lesson_id === lesson.lesson_id" class="lesson-contents">
                        <p>{{ selectedLesson.content }}</p>
                        <div v-if="isUrl(lesson.url_details)" class="reference-link">
                            <h4 class="reference-title">Please go through reference link to learn more about lesson.
                            </h4>
                            <ol>
                                <li v-for="link in Object.values(lesson.url_details)" :key="link">
                                    <a :href="link" target="_blank">
                                        {{ link }}
                                    </a>
                                </li>
                            </ol>
                        </div>
                        <p v-if="getCompletedAt(lesson.lesson_id)" class="completed-lesson">
                            Completed on: {{ getCompletedAt(lesson.lesson_id) }}
                        </p>
                    </div>
                </CardItem>

                <p v-if="lessons.length === 0" class="empty-result">
                    There is no single lesson in "{{ skillType.name }}"
                </p>

                <p v-if="filteredLessons.length === 0 && lessons.length > 0" class="empty-result">
                    None of the lesson's title has "{{ searchInput }}"
                </p>
            </Card>
        </div>
    </ChildAppLayout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import ChildAppLayout from '@/layouts/ChildAppLayout.vue';
import Card from '@/components/Card.vue';
import CardItem from '@/components/CardItem.vue';
import { useRouter } from 'vue-router';
import { searchQuery } from '@/fx/utils';

const router = useRouter();

const skillType = { curriculum_id: 1, name: 'XYZ' };

const lessons = [
    {
        lesson_id: 1,
        title: 'Lesson 1',
        content: 'Lesson 1. What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
        url_details: { 0: 'https://www.lipsum.com/', 1: 'https://drawsql.app/teams/student-839/diagrams/life-skills-app-for-school-aged-children' }
    },
    {
        lesson_id: 2,
        title: 'Lesson 2',
        content: 'Lesson 2. What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
        url_details: { 0: 'https//:dflsjds.com', 1: 'https//:google.com' }
    },
    {
        lesson_id: 3,
        title: 'Lesson 3',
        content: 'Lesson 3. What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
        url_details: { 0: 'https//:dflsjds.com', 1: 'https//:google.com' }
    },
    {
        lesson_id: 4,
        title: 'Ram 4',
        content: 'Ram 4. What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
        url_details: {}
    },
];

const lessonsHistory = ref([
    { lesson_id: 2, completed_at: '10/09/2025' },
    { lesson_id: 4, completed_at: '14/09/2025' }
]);

const searchInput = ref('');

const filteredLessons = computed(() =>
    searchQuery(lessons, searchInput.value, ['title'])
);

function isLessonRead(lessonId: number) {
    return lessonsHistory.value.some(entry => entry.lesson_id === lessonId);
}

function markAsRead(lessonId: number) {
    if (!isLessonRead(lessonId)) {
        const now = new Date();
        const completedAt =
            now.toLocaleDateString() + ', ' + now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        lessonsHistory.value.push({
            lesson_id: lessonId,
            completed_at: completedAt
        });
    }
}

function getCompletedAt(lessonId: number): string | null {
    const entry = lessonsHistory.value.find(e => e.lesson_id === lessonId);
    return entry ? entry.completed_at : null;
}

function goToActivities(lessonId: number) {
    router.push({ name: 'activities', params: { lessonId } });
}

function goToQuizzes(lessonId: number) {
    router.push({ name: 'quizzes', params: { lessonId } });
}

const selectedLesson = ref<null | typeof lessons[0]>(null);

function openLesson(lesson: typeof lessons[0]) {
    selectedLesson.value = lesson;
}

function isUrl(url_details: Record<string, string> | undefined): boolean {
    return !!url_details && Object.keys(url_details).length > 0;
}
</script>

<style scoped>
.lessons {
    position: relative;
}

.search-box {
    position: absolute;
    width: 25%;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
    right: 0;
    top: -10px;
    font-family: "VAGRoundedNext";
}

.empty-result {
    margin: 10px;
    text-align: center;
}

.lesson-title {
    color: var(--color-text-dark);
    font-family: "VAGRoundedNext";
    cursor: pointer;
    font-size: 1.5rem;
}

.lesson-title-cursor {
    cursor: auto;
}

.card-item {
    position: relative;
}

.btn {
    border: none;
    outline: none;
    background: none;
    border-radius: calc(var(--border-radius) / 2);
    padding: 10px 40px;
    color: var(--color-text-dark);
    font-family: "VAGRoundedNext";
    cursor: pointer;
    transition: 0.5s;
    font-size: var(--font-sm);
    font-weight: bolder;
}

.marked-btn {
    padding: 10px 32px;
    color: #06d6a0;
}

.btn:hover {
    background-color: var(--color-hover);
    border-color: var(--color-border);
}

.buttons {
    position: absolute;
    right: 20px;
    top: 14px;
}

.content-buttons {
    position: absolute;
    bottom: 10px;
    right: 20px;
}

.completed-lesson {
    position: absolute;
    bottom: 10px;
    color: gray;
    font-size: 1rem;
}

.lesson-contents {
    margin-top: 10px;
    font-size: 1.3rem;
    line-height: 1.7;
    margin-bottom: 45px;
}

.reference-link {
    margin-top: 10px;
}

.reference-title {
    font-weight: 700;
}
</style>