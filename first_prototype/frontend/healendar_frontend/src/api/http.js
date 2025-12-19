import axios from "axios"
import { useAuthStore } from "@/stores/auth"

export const http = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 8000,
})

http.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.accessToken) {
    config.headers.Authorization = `Bearer ${auth.accessToken}`
  }
  return config
})

/**
 * 선택: access 만료 시 refresh로 재발급 후 원 요청 재시도
 * (프로토타입에서는 없어도 됩니다. 있으면 UX가 좋아집니다.)
 */
let refreshing = false
let queue = []

http.interceptors.response.use(
  (res) => res,
  async (error) => {
    const auth = useAuthStore()
    const original = error.config

    if (error.response?.status === 401 && auth.refreshToken && !original._retry) {
      original._retry = true

      if (refreshing) {
        return new Promise((resolve, reject) => {
          queue.push({ resolve, reject })
        }).then((token) => {
          original.headers.Authorization = `Bearer ${token}`
          return http(original)
        })
      }

      refreshing = true
      try {
        const newAccess = await auth.refreshAccessToken()
        queue.forEach((p) => p.resolve(newAccess))
        queue = []
        original.headers.Authorization = `Bearer ${newAccess}`
        return http(original)
      } catch (e) {
        queue.forEach((p) => p.reject(e))
        queue = []
        auth.logout()
        return Promise.reject(e)
      } finally {
        refreshing = false
      }
    }

    return Promise.reject(error)
  }
)
