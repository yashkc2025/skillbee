<template>
    <ChildAppLayout>
        <div class="curriculums">
            <div class="top-section">
                <h2 class="ft-head-1">✨ What do you want to learn? 🎯</h2>
                <input type="text" v-model="searchInput" placeholder="Type to find curriculum... 🕵️‍♂️"
                    class="search-box">
            </div>
            <div class="card-item">
                <div v-for="curriculum in filteredCurriculums" :key="curriculum.curriculum_id">
                    <ModuleCard @click="openLessons(curriculum.curriculum_id, curriculum.name)"
                        :image="curriculum.image" :name="curriculum.name" :description="curriculum.description"
                        :progress-status="curriculum.progress_status" :show-buttons="false">
                    </ModuleCard>

                </div>
            </div>
        </div>
    </ChildAppLayout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import ChildAppLayout from '@/layouts/ChildAppLayout.vue';
import ModuleCard from '@/components/ModuleCard.vue';
import { searchQuery } from '@/fx/utils';
import { useRouter } from 'vue-router';

const router = useRouter();

const curriculums = [
    {
        curriculum_id: 1,
        name: 'Critical Thinking',
        image: '/files/critical_thinking.jpeg',
        description: 'Develop your critical thinking skills through engaging lessons and activities.',
        progress_status: 60
    },
    {
        curriculum_id: 2,
        name: 'Communication Skills',
        image: '/files/communication_skill.jpeg',
        description: 'Enhance your communication skills with interactive lessons and practical exercises.',
        progress_status: 40
    },
    {
        curriculum_id: 3,
        name: 'Time Management',
        image: '/files/time_management.jpeg',
        description: 'Learn effective time management techniques to boost your productivity in your life.',
        progress_status: 80
    },
    {
        curriculum_id: 4,
        name: 'Extracurricular Activities',
        image: '/files/extracurriculum_activities.jpeg',
        description: 'Explore various extracurricular activities to enrich your learning experience.',
        progress_status: 20
    },
    {
        curriculum_id: 5,
        name: 'Financial Literacy',
        image: '/files/financial_literacy.jpeg',
        description: 'Understand the basics knowledge of financial literacy and money management.',
        progress_status: 100
    }
]

const searchInput = ref('');

const filteredCurriculums = computed(() => {
    return searchQuery(curriculums, searchInput.value, ['name', 'description']);
});

function openLessons(curriculumId: number, curriculumName: string) {
    router.push({
        name: 'child_lessons',
        params: { curriculumId, curriculumName }
    });

}

</script>

<style>
.top-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 25px;
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
</style>