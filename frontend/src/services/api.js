import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('placement_portal_token')
  if (token) {
    config.headers['Authentication-Token'] = token
  }
  return config
})

export const authApi = {
  register: (payload) => api.post('/auth/register', payload),
  login: (payload) => api.post('/auth/login', payload),
}

export const profileApi = {
  get: () => api.get('/profile'),
  update: (payload) => api.put('/profile', payload),
}

export const jobsApi = {
  list: () => api.get('/jobs'),
  create: (payload) => api.post('/jobs', payload),
  update: (jobId, payload) => api.put(`/jobs/${jobId}`, payload),
  remove: (jobId) => api.delete(`/jobs/${jobId}`),
  apply: (jobId) => api.post(`/jobs/${jobId}/apply`),
}

export const applicationsApi = {
  list: () => api.get('/applications'),
  updateStatus: (applicationId, payload) => api.put(`/applications/${applicationId}/status`, payload),
}

export const matchScoreApi = {
  calculate: (payload) => api.post('/match-score', payload),
}

export const adminApi = {
  users: () => api.get('/admin/users'),
  updateUser: (userId, payload) => api.put(`/admin/users/${userId}`, payload),
  companies: () => api.get('/admin/companies'),
  createCompany: (payload) => api.post('/admin/companies', payload),
}

export default api
