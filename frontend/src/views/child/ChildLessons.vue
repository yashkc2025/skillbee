<template>
  <ChildAppLayout>
    <div class="lessons" :class="{ 'blur-bg': selectedLesson }">
      <div class="top-section">
        <h2 class="ft-head-1">🎉 Let’s Explore {{ skillType.name }}!</h2>
        <input type="text" v-model="searchInput" placeholder="Type to find a lesson… 🕵️‍♂️"
          class="search-box box-shadow" />
      </div>
      <div class="card-item">
        <div v-for="lesson in filteredLessons" :key="lesson.lesson_id">
          <ModuleCard @click="openLesson(lesson)" :image="lesson.image" :name="lesson.title"
            :description="lesson.description" primary-label="📝 Activities" secondary-label="✍️ Quizzes"
            :tertiary-label="isLessonRead(lesson.lesson_id) ? '✔✔ Marked as read' : '✔ Mark as read'
              " :disabledTertiary="isLessonRead(lesson.lesson_id)" @primary="goToActivities(lesson.lesson_id)"
            @secondary="goToQuizzes(lesson.lesson_id)" @tertiary="markAsRead(lesson.lesson_id)" />
        </div>
      </div>
      <Card>
        <CardItem v-for="lesson in filteredLessons" :key="lesson.lesson_id"> s </CardItem>
      </Card>
      <p v-if="lessons.length === 0" class="empty-result">
        There is no single lesson in "{{ skillType.name }}"
      </p>
      <p v-if="filteredLessons.length === 0 && lessons.length > 0" class="empty-result">
        None of the lesson's title and description has "{{ searchInput }}"
      </p>
      <p v-if="filteredLessons.length !== 0 && lessons.length !== 0" class="empty-result">
        Click on a lesson title to view its contents.
      </p>
    </div>

    <div :class="['lesson-contents', { 'show-content': selectedLesson }]">
      <h2 class="lesson-title">📘 {{ selectedLesson?.title }}</h2>
      <button class="back-btn" @click="selectedLesson = null">🔙 Back to Lessons</button>
      <p>🧠 {{ selectedLesson?.content }}</p>
      <div v-if="selectedLesson && isUrl(selectedLesson.url_details)" class="reference-link">
        <h4 class="reference-title">
          🌐 Please go through reference link to learn more about lesson.
        </h4>
        <ol>
          <li v-for="link in Object.values(selectedLesson.url_details)" :key="link">
            🔗
            <a :href="link" target="_blank" class="ref-link">
              {{ link }}
            </a>
          </li>
        </ol>
      </div>
      <div class="completed-buttons">
        <p v-if="selectedLesson && getCompletedAt(selectedLesson.lesson_id)" class="completed-lesson">
          ✅ Completed on: {{ getCompletedAt(selectedLesson.lesson_id) }}
        </p>
        <div v-if="selectedLesson" class="content-buttons">
          <AppButton type="primary" @click="goToActivities(selectedLesson.lesson_id)">📝 Activities
          </AppButton>
          <AppButton type="secondary" @click="goToQuizzes(selectedLesson.lesson_id)">✍️ Quizzes
          </AppButton>
          <AppButton type="tertiary" :class="[
            'tertiary',
            { 'disabled-tertiary': isLessonRead(selectedLesson.lesson_id) },
          ]" :disabled="isLessonRead(selectedLesson.lesson_id)" @click="markAsRead(selectedLesson.lesson_id)">
            {{
              isLessonRead(selectedLesson.lesson_id)
                ? "✔✔ Marked as read"
                : "✔ Mark as read"
            }}
          </AppButton>
        </div>
      </div>
    </div>
  </ChildAppLayout>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import ChildAppLayout from "@/layouts/ChildAppLayout.vue";
import ModuleCard from "@/components/ModuleCard.vue";
import AppButton from "@/components/AppButton.vue";
import { useRouter } from "vue-router";
import { searchQuery } from "@/fx/utils";
import Card from "@/components/Card.vue";
import CardItem from "@/components/CardItem.vue";

const router = useRouter();

interface Lesson {
  lesson_id: number;
  image: string;
  title: string;
  description: string;
  content: string;
  url_details: Record<string, string>;
}

interface SkillType {
  curriculum_id: number;
  name: string;
}

interface LessonHistory {
  lesson_id: number;
  completed_at: string;
}

interface LessonsHistory {
  lesson_id: number;
  completed_at: string;
}

const skillType = { curriculum_id: 1, name: "XYZ" };

const lessons = [
  {
    lesson_id: 1,
    title: "Lesson 1",
    image: "/files/lesson1.jpg",
    description: "Learn about the basics of Lesson 1",
    content:
      "Lesson 1. What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
    url_details: {
      0: "https://www.lipsum.com/",
      1: "https://drawsql.app/teams/student-839/diagrams/life-skills-app-for-school-aged-children",
    },
  },
  {
    lesson_id: 2,
    title: "Lesson 2",
    image: "/files/lesson2.jpeg",
    description: "Learn about the basics of Lesson 2",
    content:
      "Lesson 2. What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
    url_details: { 0: "https//:dflsjds.com", 1: "https//:google.com" },
  },
  {
    lesson_id: 3,
    title: "Lesson 3",
    image: "/files/lesson3.jpeg",
    description: "Learn about the basics of Lesson 3",
    content:
      "Lesson 3. What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
    url_details: { 0: "https//:dflsjds.com", 1: "https//:google.com" },
  },
  {
    lesson_id: 4,
    title: "Ram 4",
    image: "/files/lesson4.jpeg",
    description: "Learn about the basics of Ram 4",
    content:
      "Ram 4. What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
    url_details: {},
  },
  {
    lesson_id: 5,
    title: "Ram 5",
    image: "/files/lesson5.jpeg",
    description: "Learn about the basics of Ram 5",
    content:
      "Ram 5. What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.vWhat is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
    url_details: {},
  },
];

const lessonsHistory = ref([
  { lesson_id: 2, completed_at: "10/09/2025" },
  { lesson_id: 4, completed_at: "14/09/2025" },
]);

const searchInput = ref("");

const filteredLessons = computed(() =>
  searchQuery(lessons, searchInput.value, ["title", "description"])
);

function isLessonRead(lessonId: number) {
  return lessonsHistory.value.some((entry) => entry.lesson_id === lessonId);
}

function markAsRead(lessonId: number) {
  if (!isLessonRead(lessonId)) {
    const now = new Date();
    const completedAt =
      now.toLocaleDateString() +
      ", " +
      now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    lessonsHistory.value.push({
      lesson_id: lessonId,
      completed_at: completedAt,
    });
  }
}

function getCompletedAt(lessonId: number): string | null {
  const entry = lessonsHistory.value.find((e) => e.lesson_id === lessonId);
  return entry ? entry.completed_at : null;
}

function goToActivities(lessonId: number) {
  router.push({ name: "activities", params: { lessonId } });
}

function goToQuizzes(lessonId: number) {
  router.push({ name: "quizzes", params: { lessonId } });
}

const selectedLesson = ref<null | typeof lessons[0]>(null);

function openLesson(lesson: typeof lessons[0]) {
  selectedLesson.value = lesson;
}

function isUrl(url_details: Record<string, string> | undefined): boolean {
  if (!url_details) return false;
  return Object.values(url_details).some((v) => typeof v === "string" && v.trim() !== "");
}
</script>

<style scoped>
.top-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 25px;
}

.card-item {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
  padding: 0 20px;
}

.search-box {
  min-width: 25%;
  width: 40%;
  max-width: 400px;
  height: 30px;
  padding: var(--size-xs);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  font-family: "VAGRoundedNext";
}

.content-buttons .tertiary {
  width: 200px;
}

.content-buttons .disabled-tertiary {
  background: #ffb2dd;
  color: #ad1457;
  cursor: not-allowed;
}

.lesson-contents {
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
  font-family: "Comic Sans MS", "Fredoka", "cursive";
  font-size: var(--font-ml-lg);
  overflow-y: auto;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1),
    opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: -100;
}

.lesson-contents.show-content {
  transform: translate(-50%, -50%);
  opacity: 1;
  pointer-events: auto;
  z-index: 1000;
}

.lesson-contents .back-btn {
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

.lesson-contents .back-btn:hover {
  background-color: #ffd54f;
}

.lesson-title {
  color: #ff6f00;
  margin-bottom: 12px;
  text-align: center;
  font-family: "VAGRoundedNext";
}

.reference-link {
  margin-top: 20px;
  margin-bottom: 10px;
  background-color: #e3f2fd;
  padding: 10px 16px;
  border-radius: var(--border-radius);
  color: #0277bd;
}

.reference-title {
  font-size: var(--font-md);
  font-weight: bold;
  margin-bottom: 10px;
}

.ref-link {
  color: #0288d1;
  font-size: var(--font-md);
}

.ref-link:hover {
  color: #01579b;
}

.completed-buttons {
  margin-top: 20px;
}

.completed-lesson {
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

.empty-result {
  margin-bottom: 20px;
  text-align: center;
}

.blur-bg {
  filter: blur(5px);
  pointer-events: none;
  user-select: none;
}
</style>
