import { http } from "./http"

export const authApi = {
  register(payload) {
    return http.post("/auth/register/", payload)
  },
  token(payload) {
    return http.post("/auth/token/", payload)
  },
  refresh(payload) {
    return http.post("/auth/token/refresh/", payload)
  },
  me() {
    return http.get("/me/")
  },
  updateProfile(payload) {
    return http.patch("/me/profile/", payload)
  },
}
