<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { applicationsApi, jobsApi } from '../services/api'

function loadUser() {
  try {
    return JSON.parse(localStorage.getItem('placement_portal_user') || 'null')
  } catch {
    return null
  }
}

const user = ref(loadUser())
const jobs = ref([])
const applications = ref([])
const loading = ref(false)
const error = ref('')
const form = reactive({
  title: '',
  description: '',
  required_skills: '',
  package: '',
  deadline: '',
})

const companyId = computed(() => user.value?.company?.id || null)
const companyJobs = computed(() => jobs.value.filter((job) => job.company_id === companyId.value))

async function refreshData() {
  loading.value = true
  error.value = ''
  try {
    const [jobsResponse, applicationsResponse] = await Promise.all([
      jobsApi.list(),
      applicationsApi.list(),
    ])
    jobs.value = jobsResponse.data.jobs || []
    applications.value = applicationsResponse.data.applications || []
  } catch (err) {
    error.value = err?.response?.data?.error || 'Unable to load HR dashboard.'
  } finally {
    loading.value = false
  }
}

async function createJob() {
  error.value = ''
  try {
    await jobsApi.create({
      title: form.title,
      description: form.description,
      required_skills: form.required_skills,
      package: form.package,
      deadline: form.deadline ? new Date(form.deadline).toISOString() : null,
    })
    form.title = ''
    form.description = ''
    form.required_skills = ''
    form.package = ''
    form.deadline = ''
    await refreshData()
  } catch (err) {
    error.value = err?.response?.data?.error || 'Unable to create job.'
  }
}

async function updateStatus(applicationId, status) {
  try {
    await applicationsApi.updateStatus(applicationId, { status })
    await refreshData()
  } catch (err) {
    error.value = err?.response?.data?.error || 'Unable to update application status.'
  }
}

function jobApplications(jobId) {
  return applications.value.filter((application) => application.job_id === jobId)
}

onMounted(refreshData)
</script>

<template>
  <section class="hero">
    <div class="section-title">
      <div>
        <div class="kicker">HR dashboard</div>
        <h2 style="margin: 6px 0 0">Publish jobs and shortlist applicants.</h2>
      </div>
      <div class="badge">{{ user?.company?.name || 'Recruiter' }}</div>
    </div>

    <p v-if="error" class="badge" style="background:#fee2e2;color:#991b1b">{{ error }}</p>

    <div class="panel-grid">
      <section class="surface card">
        <div class="section-title" style="margin-bottom: 14px">
          <div>
            <h3 style="margin: 0">Post a job</h3>
            <p class="muted" style="margin: 6px 0 0">New job posts trigger the Celery notifier.</p>
          </div>
        </div>

        <div class="form">
          <label class="inline-field">
            <span class="muted">Title</span>
            <input v-model="form.title" type="text" placeholder="Backend Engineer" />
          </label>
          <label class="inline-field">
            <span class="muted">Description</span>
            <textarea v-model="form.description" placeholder="Job responsibilities"></textarea>
          </label>
          <div class="grid grid-2">
            <label class="inline-field">
              <span class="muted">Required skills</span>
              <input v-model="form.required_skills" type="text" placeholder="python, flask, sql" />
            </label>
            <label class="inline-field">
              <span class="muted">Package</span>
              <input v-model="form.package" type="text" placeholder="12 LPA" />
            </label>
          </div>
          <label class="inline-field">
            <span class="muted">Deadline</span>
            <input v-model="form.deadline" type="datetime-local" />
          </label>
          <button class="btn btn-primary" @click="createJob">Publish job</button>
        </div>
      </section>

      <section class="surface card">
        <div class="section-title" style="margin-bottom: 14px">
          <div>
            <h3 style="margin: 0">Your jobs</h3>
            <p class="muted" style="margin: 6px 0 0">Track applications for your company.</p>
          </div>
        </div>

        <div v-if="loading" class="empty-state">Loading dashboard...</div>
        <div v-else-if="!companyJobs.length" class="empty-state">No jobs posted yet.</div>

        <div v-else class="stack">
          <article v-for="job in companyJobs" :key="job.id" class="surface card" style="background: rgba(255,255,255,0.92)">
            <div class="toolbar">
              <div>
                <h4 style="margin: 0 0 6px">{{ job.title }}</h4>
                <p class="muted" style="margin: 0">{{ job.required_skills }}</p>
              </div>
              <span class="badge">{{ job.package || 'Package N/A' }}</span>
            </div>
            <p class="muted" style="line-height: 1.6">{{ job.description }}</p>
            <div class="toolbar">
              <span class="tag">Deadline: {{ job.deadline ? job.deadline.slice(0, 10) : 'Open' }}</span>
              <span class="badge">{{ jobApplications(job.id).length }} applicants</span>
            </div>
          </article>
        </div>
      </section>
    </div>

    <section class="surface card" style="margin-top: 22px">
      <div class="toolbar">
        <div>
          <h3 style="margin: 0 0 6px">Applicants</h3>
          <p class="muted" style="margin: 0">Shortlist or reject candidates directly.</p>
        </div>
      </div>

      <div v-if="!applications.length" class="empty-state" style="margin-top: 16px">No applications yet.</div>
      <table v-else class="table" style="margin-top: 16px">
        <thead>
          <tr>
            <th>Student</th>
            <th>Job</th>
            <th>Status</th>
            <th>Match</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="application in applications" :key="application.id">
            <td>{{ application.student_name }}</td>
            <td>{{ application.job_title }}</td>
            <td><span class="badge">{{ application.status }}</span></td>
            <td>{{ application.match_score }}%</td>
            <td>
              <div class="nav-links" style="padding: 0; gap: 8px">
                <button class="btn btn-light" @click="updateStatus(application.id, 'Shortlisted')">Shortlist</button>
                <button class="btn btn-light" @click="updateStatus(application.id, 'Rejected')">Reject</button>
                <button class="btn btn-accent" @click="updateStatus(application.id, 'Hired')">Hire</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </section>
</template>
