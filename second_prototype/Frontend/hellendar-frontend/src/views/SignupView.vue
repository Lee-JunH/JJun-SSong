<template>
  <section class="auth">
    <h1>Signup</h1>
    <form @submit.prevent="onSubmit" class="form">
      <input v-model="name" placeholder="name (optional)" />
      <input v-model="email" placeholder="email" />
      <input v-model="password" type="password" placeholder="password (min 8)" />
      <button type="submit">create account</button>
      <p v-if="msg" class="msg">{{ msg }}</p>
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

const name = ref("")
const email = ref("")
const password = ref("")
const msg = ref("")
const error = ref("")

async function onSubmit() {
  msg.value = ""
  error.value = ""
  try {
    await auth.register({ name: name.value, email: email.value, password: password.value })
    msg.value = "가입 완료. 로그인 해주세요."
    router.push("/login")
  } catch (e) {
    error.value = "회원가입 실패"
  }
}
</script>

<style scoped>
.auth { max-width:360px; }
.form { display:grid; gap:10px; }
input { padding:10px; border:1px solid #ddd; border-radius:10px; }
button { padding:10px; border:1px solid #ddd; background:#fff; border-radius:10px; cursor:pointer; }
.msg { color:#060; font-size:13px; }
.error { color:#b00; font-size:13px; }
</style>
