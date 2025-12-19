<script setup>
import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"

const auth = useAuthStore()
const router = useRouter()

function onLogout() {
  auth.logout()
  router.push("/login")
}
</script>

<template>
  <header style="display:flex; justify-content:center; gap:16px; padding:12px; border-bottom:1px solid #eee;">
    <router-link to="/calendar">Calendar</router-link>
    <router-link to="/foods">Food Search</router-link>

    <router-link v-if="!auth.isAuthed" to="/login">Login</router-link>
    <router-link v-if="!auth.isAuthed" to="/register">Register</router-link>

    <button v-if="auth.isAuthed" type="button" @click="onLogout">Logout</button>
  </header>

  <main style="padding: 16px;">
    <router-view />
  </main>
</template>
