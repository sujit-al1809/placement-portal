<script setup>
import { computed, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../services/api'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const role = ref('Student')
const form = reactive({
  email: '',
  password: '',
  name: '',
  skills: '',
  resume_url: '',
  cgpa: '',
  branch: '',
  company_name: '',
  industry: '',
  company_description: '',
})

const isStudent = computed(() => role.value === 'Student')

async function submit() {
  error.value = ''
  loading.value = true
  try {
    await authApi.register({
      email: form.email,
      password: form.password,
      role: role.value,
      name: form.name,
      skills: form.skills,
      resume_url: form.resume_url,
      cgpa: form.cgpa,
      branch: form.branch,
      company_name: form.company_name,
      industry: form.industry,
      company_description: form.company_description,
    })
    await router.push('/login')
  } catch (err) {
    error.value = err?.response?.data?.error || 'Registration failed.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="hero">
    <div class="hero-grid" style="grid-template-columns: 0.9fr 1.1fr">
      <div class="hero-copy surface">
        <div class="kicker">Create account</div>
        <h1>Register as a student or recruiter.</h1>
        <p>
          Students get a profile, recruiters get a company record, and admins can manage both from the dashboard.
        </p>
      </div>

      <div class="surface card">
        <form class="form" @submit.prevent="submit">
          <div class="grid grid-2">
            <label class="inline-field">
              <span class="muted">Role</span>
              <select v-model="role">
                <option value="Student">Student</option>
                <option value="CompanyHR">Company HR</option>
              </select>
            </label>
            <label class="inline-field">
              <span class="muted">Email</span>
              <input v-model="form.email" type="email" required />
            </label>
          </div>

          <label class="inline-field">
            <span class="muted">Password</span>
            <input v-model="form.password" type="password" required />
          </label>

          <div v-if="isStudent" class="grid grid-2">
            <label class="inline-field">
              <span class="muted">Name</span>
              <input v-model="form.name" type="text" placeholder="Student name" />
            </label>
            <label class="inline-field">
              <span class="muted">CGPA</span>
              <input v-model="form.cgpa" type="number" step="0.01" min="0" max="10" />
            </label>
            <label class="inline-field">
              <span class="muted">Branch</span>
              <input v-model="form.branch" type="text" placeholder="CSE" />
            </label>
            <label class="inline-field">
              <span class="muted">Resume URL</span>
              <input v-model="form.resume_url" type="url" placeholder="https://..." />
            </label>
            <label class="inline-field" style="grid-column: 1 / -1">
              <span class="muted">Skills</span>
              <textarea v-model="form.skills" placeholder="python, flask, sql"></textarea>
            </label>
          </div>

          <div v-else class="grid grid-2">
            <label class="inline-field">
              <span class="muted">Company name</span>
              <input v-model="form.company_name" type="text" placeholder="Acme Corp" />
            </label>
            <label class="inline-field">
              <span class="muted">Industry</span>
              <input v-model="form.industry" type="text" placeholder="Software" />
            </label>
            <label class="inline-field" style="grid-column: 1 / -1">
              <span class="muted">Company description</span>
              <textarea v-model="form.company_description" placeholder="About the company"></textarea>
            </label>
          </div>

          <p v-if="error" class="badge" style="background:#fee2e2;color:#991b1b">{{ error }}</p>
          <button class="btn btn-primary" :disabled="loading" type="submit">
            {{ loading ? 'Creating account...' : 'Register' }}
          </button>
        </form>
      </div>
    </div>
  </section>
</template>
