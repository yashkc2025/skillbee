import { createRouter, createWebHistory } from 'vue-router'
import DemoView from '@/views/DemoView.vue'
import LandingPage from '@/views/LandingPage.vue'
import ChildDashboard from '@/views/child/ChildDashboard.vue'
import SignInSignUp from '@/views/SignInSignUp.vue'
import ParentDashboard from '@/views/parent/ParentDashboard.vue'
import AdminDashboard from '@/views/admin/AdminDashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing-page',
      component: LandingPage
    },
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
      path: '/child_dashboard',
      name: 'child_dashboard',
      component: ChildDashboard
    },
    {
      path: '/parent_dashboard',
      name: 'parent_dashboard',
      component: ParentDashboard
    },
    {
      path: '/admin_dashboard',
      name: 'admin_dashboard',
      component: AdminDashboard
    }
    // {
    //   path: '/auth/parent_login',
    //   name: 'Login as Parent',
    //   component: ParentLoginView,
    // },
  ],
})

export default router
