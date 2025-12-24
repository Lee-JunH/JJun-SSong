import { defineStore } from "pinia"
import http from "@/api/http"

const activityMap = { 1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9 }

function calcTdee(p) {
  if (!p) return null

  const gender = String(p.gender ?? "").toLowerCase()
  const weight = Number(p.weight)
  const height = Number(p.height)
  const age = Number(p.age)
  const activity = Number(p.activity_level)

  // 필수값 없으면 계산 불가
  if (![weight, height, age].every(v => Number.isFinite(v) && v > 0)) return null

  let base = 0
  if (gender === "male" || gender === "m") {
    base = 66.47 + 13.75 * weight + 5 * height - 6.76 * age
  } else {
    base = 655.1 + 9.56 * weight + 1.85 * height - 4.68 * age
  }

  const mult = activityMap[activity] ?? 1.2
  return Math.round(base * mult)
}

export const useProfileStore = defineStore("profile", {
  state: () => ({
    me: null,
    loading: false,
    error: "",
    loaded: false,
  }),

  getters: {
    // ✅ ProfileView, 모달 어디서든 동일한 값 사용
    tdee(state) {
      return calcTdee(state.me) // null 가능
    },
    isComplete(state) {
      const p = state.me
      return (
        !!p?.height &&
        !!p?.weight &&
        !!p?.gender &&
        p?.activity_level != null &&
        !!p?.age
      )
    },
  },
  
  actions: {
    reset() {
      this.me = null
      this.loading = false
      this.error = ""
      this.loaded = false
    },
    async fetchMe(force = false) {
      if (this.loaded && !force) return

      this.loading = true
      this.error = ""
      try {
        const res = await http.get("/profile/me/")
        this.me = res.data
        this.loaded = true
      } catch (e) {
        this.error = e?.response?.data?.detail || "프로필을 불러오지 못했습니다."
        throw e
      } finally {
        this.loading = false
      }
    },

    async updateMe(payload) {
      this.loading = true
      this.error = ""
      try {
        const res = await http.patch("/profile/me/", payload)

        // ✅ 1) 204/빈 응답이면: 서버가 바디를 안 주는 케이스 → 재조회로 보정
        const data = res?.data
        const isEmptyObject =
          data && typeof data === "object" && !Array.isArray(data) && Object.keys(data).length === 0

        if (!data || isEmptyObject) {
          await this.fetchMe()
          return
        }

        // ✅ 2) 부분 응답이면: 기존 me에 merge해서 height/age/gender/activity_level 유지
        this.me = { ...(this.me || {}), ...(data || {}) }
      } catch (e) {
        this.error = "프로필 저장에 실패했습니다."
        throw e
      } finally {
        this.loading = false
      }
    },
  },
})