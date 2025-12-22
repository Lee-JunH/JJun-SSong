import { defineStore } from "pinia"
import http from "@/api/http"

export const useProfileStore = defineStore("profile", {
  state: () => ({
    me: null,
    loading: false,
    error: "",
  }),

  actions: {
    async fetchMe() {
      this.loading = true
      this.error = ""
      try {
        const res = await http.get("/profile/me/")
        this.me = res.data
      } catch (e) {
        this.error = e?.response?.data?.detail || "프로필을 불러오지 못했습니다."
      } finally {
        this.loading = false
      }
    },

    async updateMe(payload) {
      this.loading = true
      this.error = ""
      try {
        const res = await http.patch("/profile/me/", payload)
        this.me = res.data
      } catch (e) {
        this.error = "프로필 저장에 실패했습니다."
        throw e
      } finally {
        this.loading = false
      }
    },
  },
})
