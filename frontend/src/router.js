import { createRouter, createWebHistory } from 'vue-router'

import AdminDashboard from './pages/AdminDashboard.vue'
import HRDashboard from './pages/HRDashboard.vue'
import Home from './pages/Home.vue'
import Login from './pages/Login.vue'
import MatchScore from './pages/MatchScore.vue'
import NotFound from './pages/NotFound.vue'
import Register from './pages/Register.vue'
import StudentDashboard from './pages/StudentDashboard.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/login', name: 'login', component: Login },
  { path: '/register', name: 'register', component: Register },
  { path: '/student', name: 'student', component: StudentDashboard, meta: { requiresAuth: true, roles: ['Student'] } },
  { path: '/hr', name: 'hr', component: HRDashboard, meta: { requiresAuth: true, roles: ['CompanyHR', 'Admin'] } },
  { path: '/admin', name: 'admin', component: AdminDashboard, meta: { requiresAuth: true, roles: ['Admin'] } },
  { path: '/match-score', name: 'match-score', component: MatchScore },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  const token = localStorage.getItem('placement_portal_token')
  const user = JSON.parse(localStorage.getItem('placement_portal_user') || 'null')

  if (to.meta.requiresAuth && !token) {
    return '/login'
  }

  if (to.meta.roles && user && !to.meta.roles.includes(user.role)) {
    return '/'
  }

  if ((to.name === 'login' || to.name === 'register') && token) {
    return '/'
  }
})

export default router
