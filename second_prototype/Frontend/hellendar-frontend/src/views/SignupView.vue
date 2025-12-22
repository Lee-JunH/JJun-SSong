<template>
  <section class="signup-page">
    <div class="panel" role="region" aria-label="회원가입">
      <div class="badge" aria-hidden="true">
        <!-- user + plus icon -->
        <svg viewBox="0 0 24 24" class="badge-icon">
          <path
            d="M15 14c-3.3 0-6 1.7-6 3.75V20h12v-2.25C21 15.7 18.3 14 15 14Zm0-2a4 4 0 1 0-4-4 4 4 0 0 0 4 4Z"
            fill="currentColor"
            opacity="0.95"
          />
          <path
            d="M4 10V8H2V6h2V4h2v2h2v2H6v2H4Z"
            fill="currentColor"
          />
        </svg>
      </div>

      <form @submit.prevent="onSubmit" class="form">
        <!-- Nickname Input (formerly Name) -->
        <div class="field">
          <span class="icon" aria-hidden="true">
            <!-- user icon -->
            <svg viewBox="0 0 24 24" class="icon-svg">
              <path
                d="M12 12a4.5 4.5 0 1 0-4.5-4.5A4.5 4.5 0 0 0 12 12Zm0 2.25c-4.1 0-7.5 2.05-7.5 4.5V20h15v-1.25c0-2.45-3.4-4.5-7.5-4.5Z"
                fill="currentColor"
              />
            </svg>
          </span>
          <input
            v-model="name"
            type="text"
            placeholder="닉네임"
            autocomplete="username"
            required
          />
        </div>

        <div class="field">
          <span class="icon" aria-hidden="true">
            <!-- mail icon -->
            <svg viewBox="0 0 24 24" class="icon-svg">
              <path
                d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 4-8 5L4 8V6l8 5 8-5v2Z"
                fill="currentColor"
              />
            </svg>
          </span>
          <input
            v-model="email"
            type="email"
            placeholder="Email ID"
            autocomplete="email"
            required
          />
        </div>

        <div class="field">
          <span class="icon" aria-hidden="true">
            <!-- lock icon -->
            <svg viewBox="0 0 24 24" class="icon-svg">
              <path
                d="M17 9h-1V7a4 4 0 0 0-8 0v2H7a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2Zm-7-2a2 2 0 0 1 4 0v2h-4V7Z"
                fill="currentColor"
              />
            </svg>
          </span>
          <input
            v-model="password"
            type="password"
            placeholder="Password (min 8)"
            autocomplete="new-password"
            minlength="8"
            required
          />
        </div>

        <div class="row">
          <button class="ghost-link" type="button" @click="goLogin">
            이미 계정이 있으신가요?
          </button>
        </div>

        <button class="submit" type="submit" :disabled="loading">
          {{ loading ? "CREATING..." : "CREATE ACCOUNT" }}
        </button>

        <p v-if="msg" class="msg">{{ msg }}</p>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue"
import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"

const router = useRouter()
const auth = useAuthStore()

const name = ref("") // 닉네임
const email = ref("")
const password = ref("")

const msg = ref("")
const error = ref("")
const loading = ref(false)

async function onSubmit() {
  msg.value = ""
  error.value = ""
  loading.value = true

  try {
    // 1) 회원가입
    await auth.register({
      name: name.value,
      email: email.value,
      password: password.value,
    })

    // 2) ✅ 바로 로그인 (토큰 저장 + me fetch)
    await auth.login({ email: email.value, password: password.value })

    // 3) ✅ 프로필 페이지로 이동 (ProfileView에서 프로필 없으면 모달 자동 오픈)
    msg.value = "가입 완료! 프로필 설정으로 이동합니다."
    router.replace("/profile") // TODO: 실제 ProfileView 경로로 변경

  } catch (e) {
    // 백엔드 에러 포맷에 따라 메시지 다르게 표시
    const data = e?.response?.data
    if (data?.email?.[0]) error.value = data.email[0]
    else if (data?.password?.[0]) error.value = data.password[0]
    else if (data?.name?.[0]) error.value = data.name[0]
    else error.value = data?.detail || "회원가입 실패"
  } finally {
    loading.value = false
  }
}

function goLogin() {
  router.push("/login")
}
</script>


<style scoped>
/* LoginView와 동일한 full-bleed 처리 */
.signup-page {
  width: 100vw;
  margin-left: calc(50% - 50vw);

  min-height: calc(100vh - 64px);
  display: grid;
  place-items: center;
  padding: 48px 16px;

  /* LoginView와 동일한 배경 */
  background:
    radial-gradient(1100px 620px at 18% 18%, rgba(236, 53, 99, 0.55), transparent 62%),
    radial-gradient(900px 520px at 86% 22%, rgba(255, 217, 225, 0.32), transparent 60%),
    radial-gradient(900px 720px at 22% 90%, rgba(255, 191, 208, 0.45), transparent 58%),
    radial-gradient(760px 540px at 82% 86%, rgba(221, 156, 173, 0.18), transparent 62%),
    linear-gradient(135deg, #99717d 0%, #d37189 42%, #a31f3e 100%);
}

/* 카드(유리 느낌) */
.panel {
  position: relative;
  width: min(560px, 92vw);
  padding: 56px 44px 34px;
  border-radius: 8px;

  background: rgba(255, 255, 255, 0.22);
  border: 1px solid rgba(255, 255, 255, 0.22);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(10px);
}

/* 상단 원형 배지 */
.badge {
  position: absolute;
  left: 50%;
  top: 0;
  transform: translate(-50%, -50%);

  width: 92px;
  height: 92px;
  border-radius: 999px;

  display: grid;
  place-items: center;

  background: #db1f4b;
  box-shadow: 0 14px 30px rgba(0, 0, 0, 0.35);
}

.badge-icon {
  width: 46px;
  height: 46px;
  color: rgba(255, 255, 255, 0.95);
}

.form {
  display: grid;
  gap: 14px;
}

.field {
  display: grid;
  grid-template-columns: 42px 1fr;
  align-items: center;

  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 4px;
  overflow: hidden;
}

.icon {
  display: grid;
  place-items: center;
  height: 44px;
  color: rgba(0, 0, 0, 0.55);
}

.icon-svg {
  width: 18px;
  height: 18px;
}

input {
  height: 44px;
  border: 0;
  outline: 0;
  padding: 0 12px;
  background: transparent;
  font-size: 14px;
  color: #111827;
}

input::placeholder {
  color: rgba(0, 0, 0, 0.45);
}

.row {
  margin-top: 4px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  font-size: 12px;
}

.ghost-link {
  border: 0;
  background: transparent;
  color: rgba(255, 255, 255, 0.85);
  cursor: pointer;
  padding: 6px 8px;
}
.ghost-link:hover {
  text-decoration: underline;
}

.submit {
  margin-top: 10px;
  width: 100%;
  height: 46px;
  border: 0;
  border-radius: 2px;
  cursor: pointer;

  background: #db1f4b;
  color: #fff;
  font-weight: 800;
  letter-spacing: 0.06em;
}

.submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 메시지 */
.msg {
  margin: 10px 0 0;
  color: rgba(230, 255, 235, 0.98);
  font-size: 12px;
  text-align: center;
}

.error {
  margin: 8px 0 0;
  color: rgba(255, 220, 220, 0.98);
  font-size: 12px;
  text-align: center;
}

/* 반응형 */
@media (max-width: 520px) {
  .panel {
    padding: 54px 18px 26px;
  }
}
</style>