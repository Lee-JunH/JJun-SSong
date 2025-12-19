import { defineStore } from "pinia"
import { http } from "@/api/http"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: localStorage.getItem("access") || "",
    refreshToken: localStorage.getItem("refresh") || "",
  }),
  actions: {
    async login(email, password) {
      const res = await http.post("/auth/token/", { email, password })
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
  },
})
