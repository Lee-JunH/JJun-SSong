<template>
  <section>
    <h1>Login</h1>

    <form @submit.prevent="onSubmit" style="display:grid; gap:8px; max-width:320px;">
      <input v-model="email" placeholder="email" />
      <input v-model="password" type="password" placeholder="password" />
      <button type="submit" :disabled="loading">{{ loading ? "..." : "login" }}</button>

      <div style="font-size: 14px;">
        계정이 없나요?
        <a href="" @click.prevent="goRegister">회원가입</a>
      </div>
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
const loading = ref(false)

const auth = useAuthStore()
const router = useRouter()

async function onSubmit() {
  error.value = ""
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    router.push({ name: "calendar" })
  } catch (e) {
    error.value = "로그인 실패: 이메일/비밀번호 또는 백엔드 토큰 API 확인"
  } finally {
    loading.value = false
  }
}

function goRegister() {
  router.push({ name: "register" })
}
</script>
