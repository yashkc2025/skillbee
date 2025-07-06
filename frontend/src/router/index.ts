import { createRouter, createWebHistory } from 'vue-router'
import DemoView from '@/views/DemoView.vue'
import LandingPage from '@/views/LandingPage.vue'
import ChildDashboard from '@/views/child/ChildDashboard.vue'
import ChildLessons from '@/views/child/ChildLessons.vue'
import ChildCurriculum from '@/views/child/ChildCurriculums.vue'
import ChildActivities from '@/views/child/ChildActivities.vue'
import ChildQuizzes from '@/views/child/ChildQuizzes.vue'
import ChildQuizQuestions from '@/views/child/ChildQuizQuestions.vue'
import ChildAchievements from '@/views/child/ChildAchievements.vue'
import ChildSettings from '@/views/child/ChildSettings.vue'
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import sitemap from "./sitemap.json"
import SignInSignUp from '@/views/SignInSignUp.vue'
import ParentList from "@/views/admin/ParentList.vue"
import ChildrenList from "@/views/admin/ChildrenList.vue"
import LessonList from "@/views/admin/LessonList.vue"
import QuizList from "@/views/admin/QuizList.vue"
import ActivitiesList from "@/views/admin/ActivitiesList.vue"
import BadgesList from "@/views/admin/BadgesList.vue"
import AdminSettings from '@/views/admin/AdminSettings.vue'
import AdminAnalytics from '@/views/admin/AdminAnalytics.vue'
import NewLesson from '@/views/admin/new/NewLesson.vue'
import NewActivity from '@/views/admin/new/NewActivity.vue'
import NewBadge from '@/views/admin/new/NewBadge.vue'
import ParentDashboard from '@/views/parent/ParentDashboard.vue'
import NewChildren from '@/views/parent/NewChildren.vue'
import ParentSettings from '@/views/parent/ParentSettings.vue'
import ParentChildrenProfile from '@/views/parent/ParentChildrenProfile.vue'
import ChildrenProfile from '@/views/admin/ChildrenProfile.vue'
import NewQuiz from '@/views/admin/new/NewQuiz.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {
    //   path: '/',
    //   name: 'landing-page',
    //   component: LandingPage
    // },
    {
      path: '/',
      name: 'sign',
      component: SignInSignUp,
    },
    {
      path: sitemap.child_app.dashboard,
      name: 'child_dashboard',
      component: ChildDashboard
    },
    {
      path: sitemap.child_app.curriculum.curriculums,
      name: 'child_curriculums',
      component: ChildCurriculum
    },
    {
      path: sitemap.child_app.curriculum.lessons,
      name: 'child_lessons',
      component: ChildLessons,
      props: true
    },
    {
      path: sitemap.child_app.curriculum.activities,
      name: 'child_activities',
      component: ChildActivities,
      props: true
    },
    {
      path: sitemap.child_app.curriculum.quizzes,
      name: 'child_quizzes',
      component: ChildQuizzes,
      props: true
    },
    {
      path: sitemap.child_app.curriculum.attempt,
      name: 'child_quiz_attempt',
      component: ChildQuizQuestions,
      props: true
    },
    {
      path: sitemap.child_app.achievements,
      name: 'child_achievements',
      component: ChildAchievements
    },
    {
      path: sitemap.child_app.settings,
      name: 'child_settings',
      component: ChildSettings
    },
    // {
    //   path: '/auth/parent_login',
    //   name: 'Login as Parent',
    //   component: ParentLoginView,
    // },
    {
      path: '/parent_dashboard',
      name: 'parent_dashboard',
      component: ParentDashboard
    },
    {
      path: '/admin_dashboard',
      name: 'admin_dashboard',
      component: AdminDashboard
    },
    {

      path: sitemap.admin.dashboard,
      name: 'admin_dashboard',
      component: AdminDashboard
    },
    {
      path: sitemap.admin.user_management.parent,
      name: "parent_list",
      component: ParentList
    },
    {
      path: sitemap.admin.user_management.children,
      name: "child_list",
      component: ChildrenList
    },
    {
      path: "/admin/children/:id",
      name: "child_profile_admin",
      component: ChildrenProfile,
      props: true
    },
    {
      path: "/parent/children/:id",
      name: "child_profile_parent",
      component: ParentChildrenProfile,
      props: true
    },
    {
      path: sitemap.admin.curriculum.lessons,
      name: "admin_lessons",
      component: LessonList,
    },
    {
      path: sitemap.admin.curriculum.quiz,
      name: "admin_quiz",
      component: QuizList,
    },
    {
      path: sitemap.admin.curriculum.activities,
      name: "admin_activities",
      component: ActivitiesList,
    },
    {
      path: sitemap.admin.curriculum.badges,
      name: "admin_badges",
      component: BadgesList,
    },
    {
      path: sitemap.admin.settings,
      name: "admin_settings",
      component: AdminSettings
    },
    {
      path: sitemap.admin.analytics.performance,
      name: "admin_performance",
      component: AdminAnalytics
    },
    {
      path: sitemap.admin.new.lesson,
      name: 'new_lesson',
      component: NewLesson
    },
    {
      path: sitemap.admin.new.activity,
      name: 'new_activity',
      component: NewActivity
    },
    {
      path: sitemap.admin.new.badge,
      name: 'new_badge',
      component: NewBadge
    },
    {
      path: sitemap.admin.new.quiz,
      name: 'new_quiz',
      component: NewQuiz
    },
    {
      path: sitemap.parent.dashboard,
      name: 'parent_dashboard',
      component: ParentDashboard
    },
    {
      path: sitemap.parent.new_children,
      name: 'parent_new_children',
      component: NewChildren
    },
    {
      path: sitemap.parent.settings,
      name: "parent_settings",
      component: ParentSettings
    },
  ],
})

export default router
