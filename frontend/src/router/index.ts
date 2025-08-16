import { createRouter, createWebHistory } from 'vue-router'
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
import EditLesson from '@/views/admin/edit/EditLesson.vue'
import EditQuiz from '@/views/admin/edit/EditQuiz.vue'
import EditActivity from '@/views/admin/edit/EditActivity.vue'
import ActivitiesListByParent from "@/views/parent/ActivitiesListByParent.vue"
import NewActivityByParent from "@/views/parent/NewActivityByParent.vue"
import EditActivityByParent from "@/views/parent/EditActivityByParent.vue"

export const base_url = 'http://127.0.0.1:5000/'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'sign',
      component: SignInSignUp,
      meta: { title: 'Sign In / Sign Up' }
    },
    {
      path: sitemap.child_app.dashboard,
      name: 'child_dashboard',
      component: ChildDashboard,
      meta: { title: 'Child Dashboard' }
    },
    {
      path: sitemap.child_app.curriculum.curriculums,
      name: 'child_curriculums',
      component: ChildCurriculum,
      meta: { title: 'Curriculums' }
    },
    {
      path: sitemap.child_app.curriculum.lessons,
      name: 'child_lessons',
      component: ChildLessons,
      props: true,
      meta: { title: 'Lessons' }
    },
    {
      path: sitemap.child_app.curriculum.activities,
      name: 'child_activities',
      component: ChildActivities,
      props: true,
      meta: { title: 'Activities' }
    },
    {
      path: sitemap.child_app.curriculum.quizzes,
      name: 'child_quizzes',
      component: ChildQuizzes,
      props: true,
      meta: { title: 'Quizzes' }
    },
    {
      path: sitemap.child_app.curriculum.attempt,
      name: 'child_quiz_attempt',
      component: ChildQuizQuestions,
      props: true,
      meta: { title: 'Quiz Attempt' }
    },
    {
      path: sitemap.child_app.curriculum.attempt_history,
      name: 'child_quiz_attempt_history',
      component: ChildQuizQuestions,
      props: true,
      meta: { title: 'Quiz Attempt History' }
    },
    {
      path: sitemap.child_app.achievements,
      name: 'child_achievements',
      component: ChildAchievements,
      meta: { title: 'Achievements' }
    },
    {
      path: sitemap.child_app.settings,
      name: 'child_settings',
      component: ChildSettings,
      meta: { title: 'Settings' }
    },
    {
      path: '/parent_dashboard',
      name: 'parent_dashboard',
      component: ParentDashboard,
      meta: { title: 'Parent Dashboard' }
    },
    {
      path: sitemap.admin.dashboard,
      name: 'admin_dashboard',
      component: AdminDashboard,
      meta: { title: 'Admin Dashboard' }
    },
    {
      path: sitemap.admin.user_management.parent,
      name: 'parent_list',
      component: ParentList,
      meta: { title: 'Parent Management' }
    },
    {
      path: sitemap.admin.user_management.children,
      name: 'child_list',
      component: ChildrenList,
      meta: { title: 'Children Management' }
    },
    {
      path: '/admin/children/:id',
      name: 'child_profile_admin',
      component: ChildrenProfile,
      props: true,
      meta: { title: 'Child Profile' }
    },
    {
      path: '/parent/children/:id',
      name: 'child_profile_parent',
      component: ParentChildrenProfile,
      props: true,
      meta: { title: 'Child Profile' }
    },
    {
      path: sitemap.admin.curriculum.lessons,
      name: 'admin_lessons',
      component: LessonList,
      meta: { title: 'Lessons' }
    },
    {
      path: sitemap.admin.curriculum.quiz,
      name: 'admin_quiz',
      component: QuizList,
      meta: { title: 'Quizzes' }
    },
    {
      path: sitemap.admin.curriculum.activities,
      name: 'admin_activities',
      component: ActivitiesList,
      meta: { title: 'Activities' }
    },
    {
      path: sitemap.admin.curriculum.badges,
      name: 'admin_badges',
      component: BadgesList,
      meta: { title: 'Badges' }
    },
    {
      path: sitemap.admin.settings,
      name: 'admin_settings',
      component: AdminSettings,
      meta: { title: 'Settings' }
    },
    {
      path: sitemap.admin.analytics.performance,
      name: 'admin_performance',
      component: AdminAnalytics,
      meta: { title: 'Performance Analytics' }
    },
    {
      path: sitemap.admin.new.lesson,
      name: 'new_lesson',
      component: NewLesson,
      meta: { title: 'Create New Lesson' }
    },
    {
      path: sitemap.admin.new.activity,
      name: 'new_activity',
      component: NewActivity,
      meta: { title: 'Create New Activity' }
    },
    {
      path: sitemap.parent.activity.new,
      name: 'new_activity_parent',
      component: NewActivityByParent,
      meta: { title: 'Create New Activity (Parent)' }
    },
    {
      path: sitemap.parent.activity.list,
      name: 'activity_parent_list',
      component: ActivitiesListByParent,
      meta: { title: 'Activities List' }
    },
    {
      path: sitemap.admin.new.badge,
      name: 'new_badge',
      component: NewBadge,
      meta: { title: 'Create New Badge' }
    },
    {
      path: sitemap.admin.new.quiz,
      name: 'new_quiz',
      component: NewQuiz,
      meta: { title: 'Create New Quiz' }
    },
    {
      path: sitemap.admin.edit.lesson,
      name: 'edit_lesson',
      component: EditLesson,
      props: true,
      meta: { title: 'Edit Lesson' }
    },
    {
      path: sitemap.admin.edit.activity,
      name: 'edit_activity',
      component: EditActivity,
      props: true,
      meta: { title: 'Edit Activity' }
    },
    {
      path: sitemap.parent.activity.edit,
      name: 'edit_activity_parent',
      component: EditActivityByParent,
      props: true,
      meta: { title: 'Edit Activity' }
    },
    {
      path: sitemap.admin.edit.quiz,
      name: 'edit_quiz',
      component: EditQuiz,
      props: true,
      meta: { title: 'Edit Quiz' }
    },
    {
      path: sitemap.parent.dashboard,
      name: 'parent_dashboard',
      component: ParentDashboard,
      meta: { title: 'Parent Dashboard' }
    },
    {
      path: sitemap.parent.new_children,
      name: 'parent_new_children',
      component: NewChildren,
      meta: { title: 'Add New Child' }
    },
    {
      path: sitemap.parent.settings,
      name: 'parent_settings',
      component: ParentSettings,
      meta: { title: 'Settings' }
    }
  ]
})

router.afterEach((to) => {
  if (to.meta && to.meta.title) {
    document.title = `${to.meta.title} `
  } else {
    document.title = appName
  }
})

export default router
