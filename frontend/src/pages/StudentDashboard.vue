<script setup>
import { onMounted, ref } from 'vue'
import MatchScoreWidget from '../components/MatchScoreWidget.vue'
import { applicationsApi, jobsApi } from '../services/api'

const jobs = ref([])
const applications = ref([])
const loading = ref(false)
const error = ref('')

function loadUser() {
  try {
    return JSON.parse(localStorage.getItem('placement_portal_user') || 'null')
  } catch {
    return null
  }
}

const user = ref(loadUser())

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
    error.value = err?.response?.data?.error || 'Unable to load student dashboard.'
  } finally {
    loading.value = false
  }
}

async function apply(jobId) {
  try {
    await jobsApi.apply(jobId)
    await refreshData()
  } catch (err) {
    error.value = err?.response?.data?.error || 'Unable to apply to job.'
  }
}

function applicationForJob(jobId) {
  return applications.value.find((application) => application.job_id === jobId)
}

onMounted(refreshData)
</script>

<template>
  <section class="hero">
    <div class="section-title">
      <div>
        <div class="kicker">Student dashboard</div>
        <h2 style="margin: 6px 0 0">Browse jobs and track your applications.</h2>
      </div>
      <div class="badge">{{ user?.student_profile?.name || user?.email || 'Student' }}</div>
    </div>

    <div class="grid" style="gap: 22px">
      <MatchScoreWidget />

      <div class="surface card">
        <div class="toolbar">
          <div>
            <h3 style="margin: 0 0 6px">Open jobs</h3>
            <p class="muted" style="margin: 0">Apply quickly and see your placement readiness.</p>
          </div>
          <button class="btn btn-light" @click="refreshData">Refresh</button>
        </div>

        <p v-if="error" class="badge" style="margin-top: 16px;background:#fee2e2;color:#991b1b">{{ error }}</p>

        <div v-if="loading" class="empty-state" style="margin-top: 16px">Loading jobs...</div>
        <div v-else-if="!jobs.length" class="empty-state" style="margin-top: 16px">No jobs available yet.</div>

        <div v-else class="grid grid-2" style="margin-top: 16px">
          <article v-for="job in jobs" :key="job.id" class="surface card" style="background: rgba(255,255,255,0.9)">
            <div class="toolbar">
              <div>
                <div class="tag">{{ job.company_name || 'Company' }}</div>
                <h3 style="margin: 12px 0 6px">{{ job.title }}</h3>
                <p class="muted" style="margin: 0; line-height: 1.6">{{ job.description }}</p>
              </div>
              <span class="badge">{{ job.package || 'Package N/A' }}</span>
            </div>
            <div class="grid grid-2" style="margin-top: 12px">
              <div class="metric">
                <span class="muted">Skills</span>
                <strong>{{ job.required_skills || 'Any relevant skills' }}</strong>
              </div>
              <div class="metric">
                <span class="muted">Deadline</span>
                <strong>{{ job.deadline ? job.deadline.slice(0, 10) : 'Open' }}</strong>
              </div>
            </div>
            <div class="toolbar" style="margin-top: 14px">
              <span class="badge" :style="applicationForJob(job.id) ? 'background:#dcfce7;color:#166534' : ''">
                {{ applicationForJob(job.id) ? `Applied • ${applicationForJob(job.id).status}` : 'Not applied' }}
              </span>
              <button class="btn btn-primary" :disabled="!!applicationForJob(job.id)" @click="apply(job.id)">
                {{ applicationForJob(job.id) ? 'Applied' : 'Apply now' }}
              </button>
            </div>
            <p v-if="applicationForJob(job.id)" class="muted" style="margin-top: 12px">
              Match score: {{ applicationForJob(job.id).match_score }}%
            </p>
          </article>
        </div>
      </div>

      <div class="surface card">
        <div class="toolbar">
          <div>
            <h3 style="margin: 0 0 6px">My applications</h3>
            <p class="muted" style="margin: 0">Monitor status and match score in one place.</p>
          </div>
        </div>

        <div v-if="!applications.length" class="empty-state" style="margin-top: 16px">No applications yet.</div>
        <table v-else class="table" style="margin-top: 16px">
          <thead>
            <tr>
              <th>Job</th>
              <th>Status</th>
              <th>Match</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="application in applications" :key="application.id">
              <td>{{ application.job_title }}</td>
              <td><span class="badge">{{ application.status }}</span></td>
              <td>{{ application.match_score }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>
