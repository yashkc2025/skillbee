<template>
  <ChildAppLayout>
    <div class="curriculums">
      <AnimatedHeader
        v-model="searchInput"
        :heading-messages="[
          '✨ What do you want to learn? 🎯',
          '✨ Tap the card to start learning!',
        ]"
        :placeholder-messages="['Type to find curriculum... 🕵️‍♂️']"
        :typing-speed="50"
        :pause-duration="1500"
      />

      <div v-if="isLoading" class="loading-state">
        <p>Loading your learning journey...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <p>😕 Oops! We couldn't load the curriculums. {{ error }}</p>
        <button @click="fetchCurriculums" class="retry-button">Try Again</button>
      </div>

      <div v-else>
        <div class="card-item">
          <div v-for="curriculum in filteredCurriculums" :key="curriculum.curriculum_id">
            <ModuleCard
              @click="openLessons(curriculum.curriculum_id, curriculum.name)"
              :image="'data:image/png;base64,' + curriculum.image"
              :name="curriculum.name"
              :description="curriculum.description"
              :progress-status="curriculum.progress_status"
              :show-buttons="false"
              not-started-label="🚦 Ready to Start!"
              completed-label="🎓 Curriculum Complete!"
            >
            </ModuleCard>
          </div>
        </div>
        <p
          v-if="filteredCurriculums.length === 0 && curriculums.length > 0"
          class="empty-result"
        >
          None of the curriculum's name and description has "{{ searchInput }}"
        </p>
        <p v-if="filteredCurriculums.length !== 0" class="empty-result">
          Tip: Click on a curriculum card to view its lessons.
        </p>
        <p v-if="curriculums.length === 0" class="empty-result">
          No curriculums are available for you at the moment. Please check back later!
        </p>
      </div>
    </div>
  </ChildAppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import ChildAppLayout from "@/layouts/ChildAppLayout.vue";
import AnimatedHeader from "@/components/child/AnimatedHeader.vue";
import ModuleCard from "@/components/ModuleCard.vue";
import { searchQuery } from "@/fx/utils";
import { useRouter } from "vue-router";
import { base_url } from "../../router";

const router = useRouter();

// Interface for User object
interface User {
  id: number;
  role?: string;
  username?: string;
  name?: string;
  email?: string;
  dob?: string;
  school?: string;
}

// Interface for Curriculum object based on backend response
interface Curriculum {
  curriculum_id: number;
  name: string;
  description: string;
  image: string | null;
  progress_status: number;
}

const user = ref<User | null>(null);
const curriculums = ref<Curriculum[]>([]);
const searchInput = ref("");

// Refs for loading and error states
const isLoading = ref(true);
const error = ref<string | null>(null);

const filteredCurriculums = computed(() => {
  if (!Array.isArray(curriculums.value)) return [];
  return searchQuery(curriculums.value, searchInput.value, ["name", "description"]);
});

function openLessons(curriculumId: number, curriculumName: string) {
  router.push({
    name: "child_lessons",
    params: { curriculumId, curriculumName },
  });
}

async function fetchCurriculums() {
  isLoading.value = true;
  error.value = null;

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      // No token found, user needs to log in.
      throw new Error("Authentication token not found. Please log in again.");
    }

    const userDataResponse = await fetch(`${base_url}auth/get_user`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!userDataResponse.ok) {
      if (userDataResponse.status === 401) {
        throw new Error("Your session has expired. Please log in again.");
      }
      throw new Error(`Failed to fetch user data (status: ${userDataResponse.status})`);
    }

    const userData = await userDataResponse.json();
    user.value = userData.user;

    if (!user.value?.id) {
      throw new Error("Could not retrieve a valid user ID.");
    }

    const response = await fetch(`${base_url}api/child/${user.value.id}/curriculums`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch curriculums (status: ${response.status})`);
    }

    const curriculumData = await response.json();
    curriculums.value = curriculumData.curriculums;
  } catch (e: any) {
    console.error("Error fetching curriculums:", e);
    error.value = e.message || "An unknown error occurred.";
    curriculums.value = [];
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  fetchCurriculums();
});
</script>

<style scoped>
.curriculums {
  padding-bottom: 20px;
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

.empty-result {
  text-align: center;
  margin: 20px;
  color: #555;
}
</style>
