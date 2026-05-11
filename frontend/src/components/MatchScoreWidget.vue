<script setup>
import { ref } from 'vue'
import { matchScoreApi } from '../services/api'

const studentSkills = ref('python, machine learning, flask')
const jobDescription = ref('We need a python developer with ML experience')
const score = ref(null)
const matchedSkills = ref([])
const loading = ref(false)
const error = ref('')

async function computeScore() {
  error.value = ''
  loading.value = true
  try {
    const response = await matchScoreApi.calculate({
      student_skills: studentSkills.value,
      job_description: jobDescription.value,
    })
    score.value = response.data.match_score
    matchedSkills.value = response.data.matched_skills
  } catch (err) {
    error.value = err?.response?.data?.error || 'Unable to calculate match score.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="surface card match-widget">
    <div class="section-title" style="margin-bottom: 0">
      <div>
        <div class="kicker">AI match score</div>
        <h3 style="margin: 6px 0 0">Paste skills and a job description</h3>
      </div>
      <button class="btn btn-accent" :disabled="loading" @click="computeScore">
        {{ loading ? 'Calculating...' : 'Score match' }}
      </button>
    </div>

    <div class="split">
      <label class="inline-field">
        <span class="muted">Student skills</span>
        <textarea v-model="studentSkills" placeholder="python, flask, sql"></textarea>
      </label>

      <label class="inline-field">
        <span class="muted">Job description</span>
        <textarea v-model="jobDescription" placeholder="Job requirements"></textarea>
      </label>
    </div>

    <p v-if="error" class="badge" style="background:#fee2e2;color:#991b1b">{{ error }}</p>
    <div v-if="score !== null" class="grid grid-2">
      <div class="metric">
        <span class="muted">Match score</span>
        <strong class="match-score">{{ score }}%</strong>
      </div>
      <div class="metric">
        <span class="muted">Matched skills</span>
        <strong>{{ matchedSkills.length ? matchedSkills.join(', ') : 'None found' }}</strong>
      </div>
    </div>
  </section>
</template>
