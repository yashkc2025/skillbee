import { createRouter, createWebHistory } from 'vue-router'
import DemoView from '@/views/DemoView.vue'
import ChildDashboard from '@/views/child/ChildDashboard.vue'
import ChildLessons from '@/views/child/ChildLessons.vue'
import ChildCurriculum from '@/views/child/ChildCurriculums.vue'
import ChildActivities from '@/views/child/ChildActivities.vue'
import ChildQuizzes from '@/views/child/ChildQuizzes.vue'
import ChildQuizQuestions from '@/views/child/ChildQuizQuestions.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/demo',
      name: 'demo',
      component: DemoView,
    },
    {
      path: '/',
      name: 'child_dashboard',
      component: ChildDashboard
    },
    {
      path: '/curriculums',
      name: 'child_curriculum',
      component: ChildCurriculum
    },
    {
      path: '/:curriculumName/:curriculumId/lessons',
      name: 'child_lessons',
      component: ChildLessons,
      props: true
    },
    {
      path: '/:curriculumName/:curriculumId/:lessonName/:lessonId/activities',
      name: 'child_activities',
      component: ChildActivities,
      props: true
    },
    {
      path: '/:curriculumName/:curriculumId/:lessonName/:lessonId/quizzes',
      name: 'child_quizzes',
      component: ChildQuizzes,
      props: true
    },
    {
      path: '/:curriculumName/:curriculumId/:lessonName/:lessonId/quizzes/:quizId/attempt',
      name: 'child_quiz_attempt',
      component: ChildQuizQuestions,
      props: true
    }
    // {
    //   path: '/auth/parent_login',
    //   name: 'Login as Parent',
    //   component: ParentLoginView,
    // },
  ],
})

export default router
