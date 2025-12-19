<template>
  <section class="auth">
    <h1>Login</h1>
    <form @submit.prevent="onSubmit" class="form">
      <input v-model="email" placeholder="email" />
      <input v-model="password" type="password" placeholder="password" />
      <button type="submit">login</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </section>
</template>

<script setup>
import { ref } from "vue"
import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"

const router = useRouter()
const auth = useAuthStore()

const email = ref("")
const password = ref("")
const error = ref("")

async function onSubmit() {
  error.value = ""
  try {
    await auth.login({ email: email.value, password: password.value })
    router.push("/my")
  } catch (e) {
    error.value = e?.response?.data?.detail || "로그인 실패"
  }
}
</script>

<style scoped>
.auth { max-width:360px; }
.form { display:grid; gap:10px; }
input { padding:10px; border:1px solid #ddd; border-radius:10px; }
button { padding:10px; border:1px solid #ddd; background:#fff; border-radius:10px; cursor:pointer; }
.error { color:#b00; font-size:13px; }
</style>
