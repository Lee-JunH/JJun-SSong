import { defineStore } from "pinia"
import http from "@/api/http"

export const useDayStore = defineStore("day", {
  state: () => ({
    date: "",
    detail: null,
    loading: false,
    error: "",
  }),
  actions: {
    async fetchDay(date) {
      this.loading = true
      this.error = ""
      try {
        const res = await http.get(`/days/${date}/`)
        this.date = date
        this.detail = res.data
      } catch (e) {
        this.error = e?.response?.data?.detail || "하루 상세를 불러오지 못했습니다."
      } finally {
        this.loading = false
      }
    },
    async addMeal(payload) {
      await http.post(`/days/${this.date}/meals/`, payload)
      await this.fetchDay(this.date)
    },
    async deleteMeal(mealId) {
      await http.delete(`/meals/${mealId}/`)
      await this.fetchDay(this.date)
    },
    async setWeight(weight_kg) {
      await http.put(`/days/${this.date}/weight/`, { weight_kg })
      await this.fetchDay(this.date)
    },
    async setCondition(emoji, note = "") {
      await http.put(`/days/${this.date}/condition/`, { emoji, note })
      await this.fetchDay(this.date)
    },
    async setSupplement(taken) {
      await http.put(`/days/${this.date}/supplements/`, { supplement_taken: taken })
      await this.fetchDay(this.date)
    },
  },
})
