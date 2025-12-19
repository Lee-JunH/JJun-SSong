import { defineStore } from "pinia"
import http from "@/api/http"

export const useCalendarStore = defineStore("calendar", {
  state: () => ({
    month: "",
    days: [], // 서버 요약
    loading: false,
    error: "",
  }),
  actions: {
    async fetchMonth(month) {
      this.loading = true
      this.error = ""
      try {
        const res = await http.get("/calendar/", { params: { month } })
        this.month = res.data.month
        this.days = res.data.days
      } catch (e) {
        this.error = e?.response?.data?.detail || "월 데이터를 불러오지 못했습니다."
      } finally {
        this.loading = false
      }
    },
  },
})
