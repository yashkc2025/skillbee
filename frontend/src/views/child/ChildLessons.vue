<template>
  <ChildAppLayout>
    <div class="lessons" :class="{ 'blur-bg': selectedLesson }">
      <AnimatedHeader
        v-model="searchInput"
        :heading-messages="[
          `🎉 Let’s discover the lessons in ${curriculum.name}! 🌟`,
          '✨ Tap the card to start your learning adventure! 🚀',
        ]"
        :placeholder-messages="['Type to find a lesson… 🕵️‍♂️']"
        :typing-speed="50"
        :pause-duration="1500"
      />

      <div v-if="isLoading" class="loading-state">
        Available lessons are visible below...
      </div>

      <div v-else-if="error" class="error-state">
        <p>😕 Oops! We couldn't load the lessons. {{ error }}</p>
        <button @click="fetchCurriculumLessons" class="retry-button">Try Again</button>
      </div>

      <div v-else>
        <div class="card-item">
          <div v-for="lesson in filteredLessons" :key="lesson.lesson_id">
            <ModuleCard
              @click="openLesson(lesson)"
              :image="lesson.image"
              :name="lesson.title"
              :description="lesson.description"
              primary-label="📝 Activities"
              secondary-label="✍️ Quizzes"
              @primary="
                goToActivities(
                  curriculum.curriculum_id,
                  curriculum.name,
                  lesson.lesson_id,
                  lesson.title
                )
              "
              @secondary="
                goToQuizzes(
                  curriculum.curriculum_id,
                  curriculum.name,
                  lesson.lesson_id,
                  lesson.title
                )
              "
              :progress-status="lesson.progress_status"
              :show-buttons="true"
              not-started-label="📚 New Lesson!"
              completed-label="✅ Lesson Complete!"
            />
          </div>
        </div>
        <p v-if="lessons.length === 0" class="empty-result">
          There are no lessons in "{{ curriculum.name }}" yet.
        </p>
        <p v-if="filteredLessons.length === 0 && lessons.length > 0" class="empty-result">
          None of the lesson's title and description has "{{ searchInput }}"
        </p>
        <p v-if="filteredLessons.length > 0" class="empty-result">
          Tip: Click on a lesson card to view its contents.
        </p>
      </div>
    </div>

    <div
      v-if="selectedLesson"
      :class="['lesson-contents', { 'show-content': !!selectedLesson }]"
    >
      <template v-if="isDetailLoading">
        <h2 class="lesson-title">📘 {{ selectedLesson.title }}</h2>
        <div class="loading-state">Loading lesson details...</div>
      </template>
      <template v-else>
        <h2 class="lesson-title">📘 {{ selectedLesson.title }}</h2>
        <button
          class="back-btn"
          @click="
            closeLessonDetail();
            fetchCurriculumLessons();
          "
        >
          🔙 Back to Lessons
        </button>
        <p class="lesson-main-content">🧠 {{ selectedLesson.content.text }}</p>

        <div v-if="selectedLesson.content.url" class="reference-link">
          <h4 class="reference-title">
            🌐 Please go through reference link to learn more about lesson.
          </h4>
          <ol>
            <li v-for="(link, index) in selectedLesson.content.url" :key="index">
              <a :href="link" target="_blank" class="ref-link">{{ link }}</a>
            </li>
          </ol>
        </div>

        <div class="completed-buttons">
          <p v-if="selectedLesson.completed_at" class="completed-lesson">
            ✅ Completed on: {{ formatCompletionDate(selectedLesson.completed_at) }}
          </p>
          <div class="content-buttons">
            <AppButton
              type="primary"
              @click="
                goToActivities(
                  curriculum.curriculum_id,
                  curriculum.name,
                  selectedLesson.lesson_id,
                  selectedLesson.title
                )
              "
            >
              📝 Activities
            </AppButton>
            <AppButton
              type="secondary"
              @click="
                goToQuizzes(
                  curriculum.curriculum_id,
                  curriculum.name,
                  selectedLesson.lesson_id,
                  selectedLesson.title
                )
              "
            >
              ✍️ Quizzes
            </AppButton>
            <AppButton
              type="tertiary"
              :class="[
                'tertiary',
                { 'disabled-tertiary': !!selectedLesson.completed_at },
              ]"
              :disabled="!!selectedLesson.completed_at"
              @click="markAsRead(selectedLesson.lesson_id)"
            >
              {{ selectedLesson.completed_at ? "✔✔ Marked as read" : "✔ Mark as read" }}
            </AppButton>
            <AppButton type="quaternary" @click="downloadPDF">
              📥 Download as PDF
            </AppButton>
          </div>
        </div>
      </template>
    </div>
  </ChildAppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import ChildAppLayout from "@/layouts/ChildAppLayout.vue";
import AnimatedHeader from "@/components/child/AnimatedHeader.vue";
import ModuleCard from "@/components/ModuleCard.vue";
import AppButton from "@/components/AppButton.vue";
import { searchQuery } from "@/fx/utils";
import { base_url } from "../../router";
import jsPDF from "jspdf";

// INTERFACES
interface Curriculum {
  curriculum_id: number;
  name: string;
}

interface LessonSummary {
  lesson_id: number;
  image: string | null;
  title: string;
  description: string;
  progress_status: number;
}

interface LessonDetail extends LessonSummary {
  completed_at: string;
  content: {
    text: string;
    url: { [key: number]: string }[];
  };
}

// ROUTING
const route = useRoute();
const router = useRouter();

// STATE
const curriculum = ref<Curriculum>({
  curriculum_id: Number(route.params.curriculumId),
  name: (route.params.curriculumName as string) || "Curriculum",
});
const lessons = ref<LessonSummary[]>([]);
const selectedLesson = ref<LessonDetail | null>(null);
const searchInput = ref("");

// UI STATE
const isLoading = ref(true);
const isDetailLoading = ref(false);
const error = ref<string | null>(null);

// COMPUTED
const filteredLessons = computed(() => {
  return searchQuery(lessons.value, searchInput.value, ["title", "description"]);
});

function downloadPDF() {
  if (!selectedLesson.value) return;

  const doc = new jsPDF();
  const lesson = selectedLesson.value;
  const margin = 15;
  let y = margin;

  // Title
  doc.setFont("helvetica", "bold");
  doc.setFontSize(20);
  doc.text(lesson.title, margin, y);
  y += 12;

  // Description
  doc.setFont("helvetica", "normal");
  doc.setFontSize(12);
  const desc = `Description: ${lesson.description || "N/A"}`;
  const splitDesc = doc.splitTextToSize(desc, 180);
  doc.text(splitDesc, margin, y);
  y += splitDesc.length * 7 + 5;

  // Divider line
  doc.setDrawColor(180);
  doc.line(margin, y, 200 - margin, y);
  y += 10;

  // Content
  doc.setFont("helvetica", "bold");
  doc.setFontSize(14);
  doc.text("Content:", margin, y);
  y += 8;

  doc.setFont("helvetica", "normal");
  doc.setFontSize(12);
  const content = lesson.content?.text || lesson.content || "";
  const splitContent = doc.splitTextToSize(content, 180);
  doc.text(splitContent, margin, y);
  y += splitContent.length * 7 + 5;

  // Reference Links
  if (lesson.content.url?.length > 0) {
    doc.setFont("helvetica", "bold");
    doc.setFontSize(14);
    doc.text("Reference Links:", margin, y);
    y += 8;

    doc.setFont("helvetica", "normal");
    doc.setFontSize(12);

    lesson.content.url.forEach((linkObj, index) => {
      // Each linkObj is like { 0: "https://..." }
      const link = Object.values(linkObj)[0];
      const linkText = `${index + 1}. ${link}`;
      const splitLink = doc.splitTextToSize(linkText, 180);
      doc.text(splitLink, margin, y);
      y += splitLink.length * 7;
    });
  }

  // Save PDF
  doc.save(`${lesson.title}.pdf`);
}

// API CALLS
async function fetchCurriculumLessons() {
  isLoading.value = true;
  error.value = null;
  try {
    const token = localStorage.getItem("authToken");
    if (!token) throw new Error("Authentication token not found.");

    const response = await fetch(
      `${base_url}api/child/curriculum/${curriculum.value.curriculum_id}/lessons`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );

    if (!response.ok)
      throw new Error(`Failed to fetch lessons (status: ${response.status}).`);

    const data = await response.json();
    isLoading.value = false;

    curriculum.value = data.curriculum;
    lessons.value = data.lessons;
    console.log("Fetched lessons:", lessons.value);
  } catch (e: any) {
    error.value = e.message;
    lessons.value = [];
  }
}

async function openLesson(lesson: LessonSummary) {
  isDetailLoading.value = true;
  // Set initial data for the panel to show title immediately
  selectedLesson.value = { ...lesson, content: "", completed_at: null };

  try {
    const token = localStorage.getItem("authToken");
    if (!token) throw new Error("Authentication token not found.");

    const response = await fetch(`${base_url}api/child/lesson/${lesson.lesson_id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok)
      throw new Error(`Failed to load lesson details (status: ${response.status}).`);

    const lessonDetails = await response.json();
    // The backend gives 'content' and 'completed_at'. We merge it with existing summary.
    selectedLesson.value = { ...lesson, ...lessonDetails };
  } catch (e: any) {
    console.error("Error opening lesson:", e.message);
    // Optionally close the panel or show an error inside it
    closeLessonDetail();
  } finally {
    isDetailLoading.value = false;
  }
}

async function markAsRead(lessonId: number) {
  if (!selectedLesson.value || selectedLesson.value.completed_at) return;

  try {
    const token = localStorage.getItem("authToken");
    if (!token) throw new Error("Authentication token not found.");

    const completedAt = new Date().toISOString();

    const response = await fetch(`${base_url}api/child/lesson/${lessonId}/mark-read`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ completed_at: completedAt }),
    });

    if (!response.ok)
      throw new Error(`Failed to mark as read (status: ${response.status}).`);

    // Update UI instantly on success
    selectedLesson.value.completed_at = completedAt;
  } catch (e: any) {
    console.error("Error marking lesson as read:", e.message);
  }
}

// METHODS
function closeLessonDetail() {
  selectedLesson.value = null;
}

function goToActivities(
  curriculumId: number,
  curriculumName: string,
  lessonId: number,
  lessonName: string
) {
  router.push({
    name: "child_activities",
    params: { curriculumId, curriculumName, lessonId, lessonName },
  });
}

function goToQuizzes(
  curriculumId: number,
  curriculumName: string,
  lessonId: number,
  lessonName: string
) {
  router.push({
    name: "child_quizzes",
    params: { curriculumId, curriculumName, lessonId, lessonName },
  });
}

function formatCompletionDate(isoString: string): string {
  if (!isoString) return "";
  return new Date(isoString).toLocaleString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

// LIFECYCLE HOOK
onMounted(() => {
  fetchCurriculumLessons();
});
</script>

<style scoped>
/* Scoped styles remain largely the same, with added loading/error states */
.lessons {
  transition: filter 0.5s ease;
}

.blur-bg {
  filter: blur(5px);
  pointer-events: none;
  user-select: none;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 50px 20px;
  font-size: 1.2rem;
  color: #666;
}

.retry-button {
  margin-top: 20px;
  padding: 10px 25px;
  border: none;
  background-color: #007bff;
  /* Example primary color */
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-family: "VAGRoundedNext", sans-serif;
  font-size: 1rem;
  transition: background-color 0.2s ease;
}

.retry-button:hover {
  background-color: #0056b3;
}

.card-item {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
  padding: 20px;
}

.lesson-contents {
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
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  background: #fff3e0;
  font-family: "Delius", cursive;
  font-size: var(--font-ml-lg);
  overflow-y: auto;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1),
    opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: -100;
}

.lesson-contents.show-content {
  transform: translate(-50%, -50%);
  opacity: 1;
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
  margin-bottom: 20px;
  padding-right: 150px;
  /* Space for back button */
  text-align: center;
  font-family: "VAGRoundedNext";
}

.lesson-main-content {
  line-height: 1.6;
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
  margin-top: 25px;
}

.completed-lesson {
  font-size: var(--font-sm);
  color: #2e7d32;
  background-color: #c8e6c9;
  padding: 8px 12px;
  border-radius: calc(var(--border-radius) / 2);
  text-align: center;
  margin-bottom: 20px;
}

.content-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
}

.content-buttons .tertiary {
  width: 220px;
}

.content-buttons .disabled-tertiary {
  background: #ffb2dd;
  color: #ad1457;
  cursor: not-allowed;
  opacity: 0.8;
}

.empty-result {
  margin-top: 20px;
  text-align: center;
  padding-bottom: 30px;
  color: #555;
}
</style>
