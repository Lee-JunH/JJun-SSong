import { defineStore } from "pinia"
import { authApi } from "@/api/auth.api"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: localStorage.getItem("access") || "",
    refreshToken: localStorage.getItem("refresh") || "",
  }),
  getters: {
    isAuthed: (s) => !!s.accessToken,
  },
  actions: {
    async login(email, password) {
      const res = await authApi.token({ email, password })
      this.accessToken = res.data.access
      this.refreshToken = res.data.refresh
      localStorage.setItem("access", this.accessToken)
      localStorage.setItem("refresh", this.refreshToken)
    },
    logout() {
      this.accessToken = ""
      this.refreshToken = ""
      localStorage.removeItem("access")
      localStorage.removeItem("refresh")
    },
    async refreshAccessToken() {
      const res = await authApi.refresh({ refresh: this.refreshToken })
      this.accessToken = res.data.access
      localStorage.setItem("access", this.accessToken)
      return this.accessToken
    },
  },
})
