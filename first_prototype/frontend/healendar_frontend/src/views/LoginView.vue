<template>
  <section>
    <h1>Login</h1>

    <form @submit.prevent="onSubmit" style="display:grid; gap:8px; max-width:320px;">
      <input v-model="email" placeholder="email" />
      <input v-model="password" type="password" placeholder="password" />
      <button type="submit">login</button>
    </form>

    <p v-if="error" style="color:red;">{{ error }}</p>
  </section>
</template>

<script setup>
import { ref } from "vue"
import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"

const email = ref("")
const password = ref("")
const error = ref("")

const auth = useAuthStore()
const router = useRouter()

async function onSubmit() {
  error.value = ""
  try {
    await auth.login(email.value, password.value)
    router.push("/calendar")
  } catch (e) {
    error.value = "로그인 실패(토큰 API 확인 필요)"
  }
}
</script>
