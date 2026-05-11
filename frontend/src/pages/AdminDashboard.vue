<script setup>
import { onMounted, reactive, ref } from 'vue'
import { adminApi } from '../services/api'

const users = ref([])
const companies = ref([])
const loading = ref(false)
const error = ref('')
const companyForm = reactive({
  name: '',
  industry: '',
  hr_user_id: '',
  description: '',
})

async function refreshData() {
  loading.value = true
  error.value = ''
  try {
    const [usersResponse, companiesResponse] = await Promise.all([
      adminApi.users(),
      adminApi.companies(),
    ])
    users.value = usersResponse.data.users || []
    companies.value = companiesResponse.data.companies || []
  } catch (err) {
    error.value = err?.response?.data?.error || 'Unable to load admin dashboard.'
  } finally {
    loading.value = false
  }
}

async function saveUser(user) {
  try {
    await adminApi.updateUser(user.id, { role: user.role, active: user.active })
    await refreshData()
  } catch (err) {
    error.value = err?.response?.data?.error || 'Unable to update user.'
  }
}

async function createCompany() {
  try {
    await adminApi.createCompany({
      name: companyForm.name,
      industry: companyForm.industry,
      hr_user_id: Number(companyForm.hr_user_id),
      description: companyForm.description,
    })
    companyForm.name = ''
    companyForm.industry = ''
    companyForm.hr_user_id = ''
    companyForm.description = ''
    await refreshData()
  } catch (err) {
    error.value = err?.response?.data?.error || 'Unable to create company.'
  }
}

onMounted(refreshData)
</script>

<template>
  <section class="hero">
    <div class="section-title">
      <div>
        <div class="kicker">Admin dashboard</div>
        <h2 style="margin: 6px 0 0">Manage users and companies.</h2>
      </div>
    </div>

    <p v-if="error" class="badge" style="background:#fee2e2;color:#991b1b">{{ error }}</p>

    <div class="panel-grid">
      <section class="surface card">
        <div class="toolbar">
          <div>
            <h3 style="margin: 0 0 6px">Create company</h3>
            <p class="muted" style="margin: 0">Assign an HR user to a company profile.</p>
          </div>
        </div>
        <div class="form" style="margin-top: 16px">
          <label class="inline-field">
            <span class="muted">Company name</span>
            <input v-model="companyForm.name" type="text" />
          </label>
          <label class="inline-field">
            <span class="muted">Industry</span>
            <input v-model="companyForm.industry" type="text" />
          </label>
          <label class="inline-field">
            <span class="muted">HR user ID</span>
            <input v-model="companyForm.hr_user_id" type="number" min="1" />
          </label>
          <label class="inline-field">
            <span class="muted">Description</span>
            <textarea v-model="companyForm.description"></textarea>
          </label>
          <button class="btn btn-primary" @click="createCompany">Create company</button>
        </div>
      </section>

      <section class="surface card">
        <div class="toolbar">
          <div>
            <h3 style="margin: 0 0 6px">Companies</h3>
            <p class="muted" style="margin: 0">Current company records.</p>
          </div>
          <button class="btn btn-light" @click="refreshData">Refresh</button>
        </div>
        <div v-if="loading" class="empty-state" style="margin-top: 16px">Loading admin data...</div>
        <div v-else-if="!companies.length" class="empty-state" style="margin-top: 16px">No companies yet.</div>
        <table v-else class="table" style="margin-top: 16px">
          <thead>
            <tr>
              <th>Name</th>
              <th>Industry</th>
              <th>HR user</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="company in companies" :key="company.id">
              <td>{{ company.name }}</td>
              <td>{{ company.industry }}</td>
              <td>{{ company.hr_email || company.hr_user_id }}</td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>

    <section class="surface card" style="margin-top: 22px">
      <div class="toolbar">
        <div>
          <h3 style="margin: 0 0 6px">Users</h3>
          <p class="muted" style="margin: 0">Update roles and activation state.</p>
        </div>
      </div>

      <table class="table" style="margin-top: 16px">
        <thead>
          <tr>
            <th>Email</th>
            <th>Role</th>
            <th>Active</th>
            <th>Save</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.email }}</td>
            <td>
              <select v-model="user.role">
                <option value="Student">Student</option>
                <option value="CompanyHR">CompanyHR</option>
                <option value="Admin">Admin</option>
              </select>
            </td>
            <td>
              <input v-model="user.active" type="checkbox" />
            </td>
            <td>
              <button class="btn btn-accent" @click="saveUser(user)">Save</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </section>
</template>
