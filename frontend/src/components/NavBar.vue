<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(loadUser())

function loadUser() {
  try {
    return JSON.parse(localStorage.getItem('placement_portal_user') || 'null')
  } catch {
    return null
  }
}

function syncAuth() {
  user.value = loadUser()
}

function logout() {
  localStorage.removeItem('placement_portal_token')
  localStorage.removeItem('placement_portal_user')
  syncAuth()
  window.dispatchEvent(new Event('auth-changed'))
  router.push('/')
}

const dashboardRoute = computed(() => {
  if (!user.value) return '/login'
  if (user.value.role === 'Student') return '/student'
  if (user.value.role === 'CompanyHR') return '/hr'
  if (user.value.role === 'Admin') return '/admin'
  return '/'
})

onMounted(() => {
  window.addEventListener('storage', syncAuth)
  window.addEventListener('auth-changed', syncAuth)
})

onBeforeUnmount(() => {
  window.removeEventListener('storage', syncAuth)
  window.removeEventListener('auth-changed', syncAuth)
})
</script>

<template>
  <header class="nav">
    <div class="container nav-inner surface">
      <router-link class="brand" to="/">
        <span class="brand-mark"></span>
        <span>Placement Portal</span>
      </router-link>

      <nav class="nav-links">
        <router-link to="/">Home</router-link>
        <router-link v-if="user?.role === 'Student'" to="/student">Student</router-link>
        <router-link v-if="user?.role === 'CompanyHR'" to="/hr">HR Dashboard</router-link>
        <router-link v-if="user?.role === 'Admin'" to="/admin">Admin</router-link>
        <router-link to="/match-score">Match Score</router-link>
        <router-link v-if="!user" to="/login">Login</router-link>
        <router-link v-if="!user" to="/register">Register</router-link>
        <router-link v-if="user" :to="dashboardRoute">Dashboard</router-link>
        <button v-if="user" class="btn btn-light" @click="logout">Logout</button>
      </nav>
    </div>
  </header>
</template>
