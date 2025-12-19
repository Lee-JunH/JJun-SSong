import { http } from "./http"

export const recordsApi = {
  calendar(month) {
    return http.get("/records/calendar/", { params: { month } })
  },
  dayDetail(dateStr) {
    return http.get(`/records/days/${dateStr}/`)
  },
  mealUpsert(payload) {
    return http.post("/records/meals/", payload)
  },
  addMealItem(payload) {
    return http.post("/records/meal-items/", payload)
  },
  deleteMealItem(id) {
    return http.delete(`/records/meal-items/${id}/`)
  },

  listExercises(dateStr) {
    return http.get("/records/exercises/", { params: { date: dateStr } })
  },
  addExercise(payload) {
    return http.post("/records/exercises/", payload)
  },
  deleteExercise(id) {
    return http.delete(`/records/exercises/${id}/`)
  },

  upsertWeight(dateStr, payload) {
    return http.put(`/records/weights/${dateStr}/`, payload)
  },
  upsertCondition(dateStr, payload) {
    return http.put(`/records/conditions/${dateStr}/`, payload)
  },
  upsertSupplement(dateStr, payload) {
    return http.put(`/records/supplements/${dateStr}/`, payload)
  },
}
