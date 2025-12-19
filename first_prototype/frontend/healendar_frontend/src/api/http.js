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
