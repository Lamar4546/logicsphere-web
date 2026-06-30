import axios from 'axios'

function apiBaseUrl() {
  const configured = import.meta.env.VITE_API_BASE_URL
  if (!configured) return '/api'

  const trimmed = configured.replace(/\/+$/, '')
  if (trimmed.endsWith('/api')) return trimmed
  return `${trimmed}/api`
}

const api = axios.create({
  baseURL: apiBaseUrl()
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('ls_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export default api
