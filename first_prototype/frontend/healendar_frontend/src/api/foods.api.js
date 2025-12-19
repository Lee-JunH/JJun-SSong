import { http } from "./http"

export const foodsApi = {
  search(q) {
    return http.get("/foods/search/", { params: { q } })
  },
  createCustomFood(payload) {
    return http.post("/custom-foods/", payload)
  },
  listCustomFoods() {
    return http.get("/custom-foods/")
  },
}
