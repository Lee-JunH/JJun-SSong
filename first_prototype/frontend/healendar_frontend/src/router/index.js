import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import LoginView from "@/views/LoginView.vue"
import RegisterView from "@/views/RegisterView.vue"
import CalendarView from "@/views/CalendarView.vue"
import DayDetailView from "@/views/DayDetailView.vue"
import FoodSearchView from "@/views/FoodSearchView.vue"

const routes = [
  { path: "/login", name: "login", component: LoginView },
  { path: "/register", name: "register", component: RegisterView },

  { path: "/calendar", name: "calendar", component: CalendarView, meta: { requiresAuth: true } },
  { path: "/day/:date", name: "day", component: DayDetailView, meta: { requiresAuth: true } },
  { path: "/foods", name: "foods", component: FoodSearchView, meta: { requiresAuth: true } },

  // 기본 진입
  { path: "/", redirect: "/calendar" },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthed) return { name: "login" }
})

export default router
