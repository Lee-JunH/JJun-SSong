import { createRouter, createWebHistory } from "vue-router"

import LoginView from "@/views/LoginView.vue"
import CalendarView from "@/views/CalendarView.vue"
import DayDetailView from "@/views/DayDetailView.vue"
import FoodSearchView from "@/views/FoodSearchView.vue"

const routes = [
  { path: "/", redirect: "/calendar" },
  { path: "/login", name: "login", component: LoginView },
  { path: "/calendar", name: "calendar", component: CalendarView },
  { path: "/day/:date", name: "day-detail", component: DayDetailView, props: true },
  { path: "/foods", name: "foods", component: FoodSearchView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
