import { defineStore } from "pinia"
import http from "@/api/http"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: localStorage.getItem("access") || "",
    refreshToken: localStorage.getItem("refresh") || "",
    me: null,
  }),
  actions: {
    async register(payload) {
      await http.post("/auth/register/", payload)
    },
    async login({ email, password }) {
      const res = await http.post("/auth/login/", { email, password })
      this.accessToken = res.data.access
      this.refreshToken = res.data.refresh
      localStorage.setItem("access", this.accessToken)
      localStorage.setItem("refresh", this.refreshToken)
      await this.fetchMe()
    },
    async refresh() {
      const res = await http.post("/auth/refresh/", { refresh: this.refreshToken })
      this.accessToken = res.data.access
      localStorage.setItem("access", this.accessToken)
      return this.accessToken
    },
    async fetchMe() {
      const res = await http.get("/auth/me/")
      this.me = res.data
    },
    logout() {
      this.accessToken = ""
      this.refreshToken = ""
      this.me = null
      localStorage.removeItem("access")
      localStorage.removeItem("refresh")
    },
  },
})
