import { createRouter, createWebHistory } from 'vue-router'
import DemoView from '@/views/DemoView.vue'
import ChildDashboard from '@/views/child/ChildDashboard.vue'
import ChildLessons from '@/views/child/ChildLessons.vue'

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
      path: '/lesson',
      name: 'child_lessons',
      component: ChildLessons
    }
    // {
    //   path: '/auth/parent_login',
    //   name: 'Login as Parent',
    //   component: ParentLoginView,
    // },
  ],
})

export default router
