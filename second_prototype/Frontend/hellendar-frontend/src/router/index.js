import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import HomeView from "@/views/HomeView.vue"
import FeaturesView from "@/views/FeaturesView.vue"
import StartView from "@/views/StartView.vue"
import MyHealendarView from "@/views/MyHealendarView.vue"
import LoginView from "@/views/LoginView.vue"
import SignupView from "@/views/SignupView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", component: HomeView },
    { path: "/features", component: FeaturesView },
    { path: "/start", component: StartView },
    { path: "/login", component: LoginView },
    { path: "/signup", component: SignupView },
    { path: "/my", component: MyHealendarView, meta: { requiresAuth: true } },
    { path: "/profile", name: "profile", component: () => import("@/views/ProfileView.vue"), meta: { requiresAuth: true } },
  ],
  scrollBehavior(to, from, savedPosition) {
    // 뒤로가기/앞으로가기면 기존 위치 복원
    if (savedPosition) return savedPosition

    // 해시(#section) 이동이 있으면 해당 요소로
    if (to.hash) return { el: to.hash, behavior: "smooth" }

    // 기본: 항상 맨 위로
    return { left: 0, top: 0 }
  },
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
