<!-- src/components/AccountManageModal.vue -->
<template>
  <Transition name="modal-fade">
    <div class="modal-backdrop" @click.self="emit('close')">
      <div class="modal-content" role="dialog" aria-modal="true">
        <div class="modal-header">
          <h3>회원정보 수정</h3>
          <button class="close-btn" @click="emit('close')" aria-label="닫기">×</button>
        </div>

        <div class="modal-body">
          <!-- 공통 상태 -->
          <div v-if="commonError" class="alert error">{{ commonError }}</div>
          <div v-if="commonSuccess" class="alert success">{{ commonSuccess }}</div>

          <!-- 1) 비밀번호 변경 -->
          <section class="section">
            <div class="section-title">비밀번호 변경</div>
            <div class="desc">
              현재 비밀번호 확인 후 새 비밀번호를 입력하세요. 변경 완료 시 보안을 위해 자동 로그아웃됩니다.
            </div>

            <div class="form">
              <label class="label">현재 비밀번호</label>
              <input
                v-model="pw.current"
                type="password"
                class="input"
                autocomplete="current-password"
                placeholder="현재 비밀번호"
              />

              <label class="label">새 비밀번호</label>
              <input
                v-model="pw.new1"
                type="password"
                class="input"
                autocomplete="new-password"
                placeholder="새 비밀번호"
              />

              <label class="label">새 비밀번호 확인</label>
              <input
                v-model="pw.new2"
                type="password"
                class="input"
                autocomplete="new-password"
                placeholder="새 비밀번호 확인"
              />

              <div v-if="pwError" class="hint error">{{ pwError }}</div>

              <button class="btn" :disabled="busyPw" @click="changePassword">
                {{ busyPw ? "변경 중..." : "비밀번호 변경" }}
              </button>
            </div>
          </section>

          <hr class="divider" />

          <!-- 2) 회원 탈퇴 -->
          <section class="section danger">
            <div class="section-title">회원 탈퇴</div>
            <div class="desc">
              회원 탈퇴 시 계정 및 관련 데이터가 삭제됩니다. 진행하려면 현재 비밀번호를 입력하세요.
            </div>

            <div class="form">
              <label class="label">현재 비밀번호</label>
              <input
                v-model="del.current"
                type="password"
                class="input"
                autocomplete="current-password"
                placeholder="현재 비밀번호"
              />

              <label class="check">
                <input type="checkbox" v-model="del.confirmed" />
                위 내용을 확인했으며, 회원 탈퇴에 동의합니다.
              </label>

              <div v-if="delError" class="hint error">{{ delError }}</div>

              <button class="btn danger" :disabled="busyDel" @click="deleteAccount">
                {{ busyDel ? "처리 중..." : "회원 탈퇴" }}
              </button>
            </div>
          </section>
        </div>

        <div class="modal-footer">
          <button class="btn ghost" @click="emit('close')">닫기</button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref } from "vue"
import http from "@/api/http"
import { useAuthStore } from "@/stores/auth"

const emit = defineEmits(["close", "loggedOut"])

const auth = useAuthStore()

// 엔드포인트(프로젝트에 맞게 필요 시 수정)
const CHANGE_PW_URL = "/auth/password/change/"
const DELETE_URL = "/auth/delete/"

const busyPw = ref(false)
const busyDel = ref(false)

const commonError = ref("")
const commonSuccess = ref("")

const pwError = ref("")
const delError = ref("")

const pw = ref({
  current: "",
  new1: "",
  new2: "",
})

const del = ref({
  current: "",
  confirmed: false,
})

function resetAlerts() {
  commonError.value = ""
  commonSuccess.value = ""
  pwError.value = ""
  delError.value = ""
}

function extractFieldError(e, field) {
  const data = e?.response?.data
  if (!data) return ""
  const v = data[field]
  if (Array.isArray(v)) return v.join(" ")
  if (typeof v === "string") return v
  if (typeof data.detail === "string") return data.detail
  return ""
}

async function changePassword() {
  resetAlerts()

  if (!pw.value.current) {
    pwError.value = "현재 비밀번호를 입력하세요."
    return
  }
  if (!pw.value.new1 || !pw.value.new2) {
    pwError.value = "새 비밀번호를 2번 입력하세요."
    return
  }
  if (pw.value.new1 !== pw.value.new2) {
    pwError.value = "새 비밀번호가 일치하지 않습니다."
    return
  }

  busyPw.value = true
  try {
    await http.post(CHANGE_PW_URL, {
      current_password: pw.value.current,
      new_password1: pw.value.new1,
      new_password2: pw.value.new2,
    })

    commonSuccess.value = "비밀번호가 변경되었습니다. 다시 로그인해주세요."

    // 보안상 토큰 무효화/재로그인 유도
    auth.logout()
    emit("loggedOut")
    emit("close")
  } catch (e) {
    pwError.value =
      extractFieldError(e, "current_password") ||
      extractFieldError(e, "new_password1") ||
      extractFieldError(e, "new_password2") ||
      "비밀번호 변경에 실패했습니다."
  } finally {
    busyPw.value = false
  }
}

async function deleteAccount() {
  resetAlerts()

  if (!del.value.current) {
    delError.value = "현재 비밀번호를 입력하세요."
    return
  }
  if (!del.value.confirmed) {
    delError.value = "회원 탈퇴 동의 체크가 필요합니다."
    return
  }

  // 마지막 확인(실수 방지)
  const ok = window.confirm("정말로 회원 탈퇴를 진행하시겠습니까? 삭제 후 복구할 수 없습니다.")
  if (!ok) return

  busyDel.value = true
  try {
    await http.post(DELETE_URL, {
      current_password: del.value.current,
    })

    // 서버에서 계정 삭제 완료 → 로컬 세션 정리
    auth.logout()
    emit("loggedOut")
    emit("close")
  } catch (e) {
    delError.value =
      extractFieldError(e, "current_password") ||
      "회원 탈퇴에 실패했습니다."
  } finally {
    busyDel.value = false
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-color: rgba(0,0,0,0.4);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1200;
}

.modal-content {
  background: #fff;
  width: 92%;
  max-width: 720px;
  border-radius: 18px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.18);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 85vh;
}

.modal-header {
  padding: 18px 22px;
  border-bottom: 1px solid #f1f3f5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 800;
  color: #212529;
}

.close-btn {
  background: none;
  border: none;
  font-size: 26px;
  line-height: 1;
  cursor: pointer;
  color: #ced4da;
}
.close-btn:hover { color: #495057; }

.modal-body {
  padding: 18px 22px;
  overflow-y: auto;
}

.modal-footer {
  padding: 14px 22px;
  border-top: 1px solid #f1f3f5;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.section-title {
  font-weight: 900;
  color: #212529;
}

.desc {
  font-size: 13px;
  color: #6c757d;
  line-height: 1.45;
}

.form {
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
}

.label {
  font-size: 12px;
  color: #495057;
  font-weight: 700;
  margin-top: 4px;
}

.input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #dee2e6;
  border-radius: 12px;
  outline: none;
}
.input:focus {
  border-color: #adb5bd;
}

.hint {
  font-size: 12px;
  margin-top: 2px;
}
.hint.error { color: #b00020; }

.check {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 13px;
  color: #495057;
  margin-top: 6px;
}

.btn {
  padding: 10px 12px;
  border: 1px solid #dee2e6;
  background: #fff;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 800;
}
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.btn:hover:not(:disabled) {
  background: #f8f9fa;
}

.btn.ghost {
  background: #fff;
}

.btn.danger {
  border-color: #ffc9c9;
  color: #b00020;
}
.btn.danger:hover:not(:disabled) {
  background: #fff5f5;
}

.divider {
  border: 0;
  border-top: 1px solid #f1f3f5;
  margin: 16px 0;
}

.alert {
  padding: 10px 12px;
  border-radius: 12px;
  font-size: 13px;
  margin-bottom: 12px;
}
.alert.error {
  background: #fff5f5;
  border: 1px solid #ffc9c9;
  color: #b00020;
}
.alert.success {
  background: #f3fffb;
  border: 1px solid #b2f2bb;
  color: #0a750a;
}

.modal-fade-enter-active, .modal-fade-leave-active { transition: all 0.25s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; transform: scale(0.98); }

.section.danger .section-title { color: #b00020; }
</style>
