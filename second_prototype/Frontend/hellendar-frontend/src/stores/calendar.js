import { defineStore } from "pinia"
import http from "@/api/http"

export const useCalendarStore = defineStore("calendar", {
  state: () => ({
    month: "",
    days: [], // 서버 요약
    loading: false,
    error: "",
  }),
  getters: {
    byDate: (state) => {
      const map = {}
      for (const d of state.days) map[d.date] = d
      return map
    },
  },
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
    async patchToggles(date, patch) {
      await http.patch(`/days/${date}/toggles/`, patch)

      // 서버 저장 후 캘린더 UI 즉시 반영
      const idx = this.days.findIndex((x) => x.date === date)
      if (idx !== -1) {
        this.days[idx] = { ...this.days[idx], ...patch }
      } else {
        this.days.push({ date, ...patch })
      }
    },

  },
})
