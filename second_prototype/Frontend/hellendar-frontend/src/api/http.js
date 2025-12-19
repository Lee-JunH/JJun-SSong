import axios from "axios"
import { useAuthStore } from "@/stores/auth"

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
})

http.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.accessToken) {
    config.headers.Authorization = `Bearer ${auth.accessToken}`
  }
  return config
})

let isRefreshing = false
let queue = []

function resolveQueue(error, token = null) {
  queue.forEach(p => (error ? p.reject(error) : p.resolve(token)))
  queue = []
}

http.interceptors.response.use(
  (res) => res,
  async (err) => {
    const auth = useAuthStore()
    const original = err.config

    if (err.response?.status === 401 && !original._retry && auth.refreshToken) {
      original._retry = true

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          queue.push({ resolve, reject })
        }).then((token) => {
          original.headers.Authorization = `Bearer ${token}`
          return http(original)
        })
      }

      isRefreshing = true
      try {
        const newToken = await auth.refresh()
        resolveQueue(null, newToken)
        original.headers.Authorization = `Bearer ${newToken}`
        return http(original)
      } catch (e) {
        resolveQueue(e, null)
        auth.logout()
        throw e
      } finally {
        isRefreshing = false
      }
    }

    throw err
  }
)

export default http
