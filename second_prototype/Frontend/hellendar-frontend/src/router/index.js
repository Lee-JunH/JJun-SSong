import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import HomeView from "@/views/HomeView.vue"
import FeaturesView from "@/views/FeaturesView.vue"
import StartView from "@/views/StartView.vue"
import MyHealendarView from "@/views/MyHealendarView.vue"
import LoginView from "@/views/LoginView.vue"
import SignupView from "@/views/SignupView.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: HomeView },
    { path: "/features", component: FeaturesView },
    { path: "/start", component: StartView },
    { path: "/login", component: LoginView },
    { path: "/signup", component: SignupView },
    { path: "/my", component: MyHealendarView, meta: { requiresAuth: true } },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth) {
    if (!auth.accessToken) return "/login"
    if (!auth.me) {
      try { await auth.fetchMe() } catch { return "/login" }
    }
  }
})

export default router
