<template>
  <section style="max-width: 420px;">
    <h1>Register</h1>

    <form @submit.prevent="onSubmit" style="display:grid; gap:8px;">
      <input v-model.trim="email" placeholder="email" type="email" />
      <input v-model="password" placeholder="password (min 8)" type="password" />
      <input v-model.trim="firstName" placeholder="name (optional)" />

      <button type="submit" :disabled="loading">{{ loading ? "..." : "가입하기" }}</button>

      <div style="font-size: 14px;">
        이미 계정이 있나요?
        <a href="" @click.prevent="goLogin">로그인</a>
      </div>
    </form>

    <p v-if="error" style="color:red;">{{ error }}</p>
    <p v-if="success" style="color:green;">가입 완료! 로그인으로 이동합니다.</p>
  </section>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { authApi } from "@/api/auth.api"

const router = useRouter()
const email = ref("")
const password = ref("")
const firstName = ref("")
const loading = ref(false)
const error = ref("")
const success = ref(false)

async function onSubmit() {
  error.value = ""
  success.value = false
  loading.value = true
  try {
    await authApi.register({
      email: email.value,
      password: password.value,
      first_name: firstName.value,
      last_name: "",
    })
    success.value = true
    setTimeout(() => router.push({ name: "login" }), 500)
  } catch (e) {
    const data = e?.response?.data
    error.value = data?.detail || (data ? JSON.stringify(data) : "회원가입 실패")
  } finally {
    loading.value = false
  }
}

function goLogin() {
  router.push({ name: "login" })
}
</script>
