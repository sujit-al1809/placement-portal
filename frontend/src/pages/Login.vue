<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../services/api'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const form = reactive({
  email: '',
  password: '',
})

function nextRoute(role) {
  if (role === 'Student') return '/student'
  if (role === 'CompanyHR') return '/hr'
  if (role === 'Admin') return '/admin'
  return '/'
}

async function submit() {
  error.value = ''
  loading.value = true
  try {
    const response = await authApi.login(form)
    localStorage.setItem('placement_portal_token', response.data.token)
    localStorage.setItem('placement_portal_user', JSON.stringify(response.data.user))
    window.dispatchEvent(new Event('auth-changed'))
    await router.push(nextRoute(response.data.user.role))
  } catch (err) {
    error.value = err?.response?.data?.error || 'Login failed.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="hero">
    <div class="hero-grid" style="grid-template-columns: 0.9fr 1.1fr">
      <div class="hero-copy surface">
        <div class="kicker">Welcome back</div>
        <h1>Sign in to manage placements.</h1>
        <p>
          Use your token-based account to access jobs, applications, and dashboard actions.
        </p>
      </div>

      <div class="surface card">
        <form class="form" @submit.prevent="submit">
          <label class="inline-field">
            <span class="muted">Email</span>
            <input v-model="form.email" type="email" placeholder="student@college.edu" required />
          </label>
          <label class="inline-field">
            <span class="muted">Password</span>
            <input v-model="form.password" type="password" placeholder="••••••••" required />
          </label>
          <p v-if="error" class="badge" style="background:#fee2e2;color:#991b1b">{{ error }}</p>
          <button class="btn btn-primary" :disabled="loading" type="submit">
            {{ loading ? 'Signing in...' : 'Sign in' }}
          </button>
        </form>
      </div>
    </div>
  </section>
</template>
