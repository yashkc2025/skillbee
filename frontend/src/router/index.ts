import { createRouter, createWebHistory } from 'vue-router'
import DemoView from '@/views/DemoView.vue'
import ChildDashboard from '@/views/child/ChildDashboard.vue'
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import sitemap from "./sitemap.json"
import SignInSignUp from '@/views/SignInSignUp.vue'
import ParentList from "@/views/admin/ParentList.vue"
import ChildrenList from "@/views/admin/ChildrenList.vue"
import ChildrenProfile from "@/views/admin/ChildrenProfile.vue"
import LessonList from "@/views/admin/LessonList.vue"
import QuizList from "@/views/admin/QuizList.vue"
import ActivitiesList from "@/views/admin/ActivitiesList.vue"
import BadgesList from "@/views/admin/BadgesList.vue"
import AdminSettings from '@/views/admin/AdminSettings.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login_register',
      name: 'sign',
      component: SignInSignUp,
    },
    {
      path: '/demo',
      name: 'demo',
      component: DemoView,
    },
    {
      path: sitemap.child_app.dashboard,
      name: 'child_dashboard',
      component: ChildDashboard
    },
    {
      path: "/admin",
      name: 'admin_dashboard',
      component: AdminDashboard
    },
    {
      path: "/admin/parent",
      name: "parent_list",
      component: ParentList
    },
    {
      path: "/admin/children",
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
      path: "/admin/lessons",
      name: "admin_lessons",
      component: LessonList,
    },
    {
      path: "/admin/quiz",
      name: "admin_quiz",
      component: QuizList,
    },
    {
      path: "/admin/activities",
      name: "admin_activities",
      component: ActivitiesList,
    },
    {
      path: "/admin/badges",
      name: "admin_badges",
      component: BadgesList,
    },
    {
      path: "/admin/settings",
      name: "admin_settings",
      component: AdminSettings
    }
  ],
})

export default router
