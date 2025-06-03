import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DemoView from '@/views/DemoView.vue'
// import ParentLoginView from './auth/ParentLoginView.vue'
import SignInSignUp from '../views/SignInSignUp.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/demo',
      name: 'demo',
      component: DemoView,
    },

    {
      path: '/signin-signup',
      name: 'sign',
      component: SignInSignUp,
    },
    // {
    //   path: '/auth/parent_login',
    //   name: 'Login as Parent',
    //   component: ParentLoginView,
    // },
  ],
})

export default router
