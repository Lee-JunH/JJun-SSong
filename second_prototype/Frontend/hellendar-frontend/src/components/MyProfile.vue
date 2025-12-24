<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="profile-card fade-in-up">
      <button type="button" class="close-btn" @click="$emit('close')" aria-label="닫기">
        ✕
      </button>

      <header class="header">
        <div class="avatar-circle">
          <span class="avatar-emoji">🐣</span>
        </div>
        <h1 class="title">프로필 설정</h1>
        <p class="subtitle">
          더 정확한 분석을 위해<br />
          회원님의 정보를 알려주세요!
        </p>
      </header>

      <form class="form-body" @submit.prevent="saveProfile">
        <!-- 1. 성별 선택 -->
        <div class="form-group">
          <label class="label">성별</label>
          <div class="gender-toggle">
            <button
              type="button"
              class="gender-btn"
              :class="{ active: localForm.gender === 'male' }"
              @click="localForm.gender = 'male'"
            >
              <span class="icon">👦</span> 남성
            </button>
            <button
              type="button"
              class="gender-btn"
              :class="{ active: localForm.gender === 'female' }"
              @click="localForm.gender = 'female'"
            >
              <span class="icon">👧</span> 여성
            </button>
          </div>
        </div>

        <!-- 2. 나이 & 키 -->
        <div class="row-2">
          <div class="form-group">
            <label class="label" for="age">나이</label>
            <div class="input-wrapper">
              <input
                id="age"
                type="number"
                v-model.number="localForm.age"
                placeholder="0"
                class="input-box"
              />
              <span class="unit">세</span>
            </div>
          </div>

          <div class="form-group">
            <label class="label" for="height">키</label>
            <div class="input-wrapper">
              <input
                id="height"
                type="number"
                v-model.number="localForm.height"
                placeholder="0"
                class="input-box"
              />
              <span class="unit">cm</span>
            </div>
          </div>
        </div>

        <!-- 3. 체중 관리 섹션 (시작/목표만) -->
        <div class="weight-section">
          <label class="label">체중 목표</label>

          <!-- ✅ 2칸 구성으로 변경 -->
          <div class="weight-grid two">
            <!-- ✅ 시작: 기존 "현재" highlight 스타일 적용 -->
            <div class="weight-item highlight">
              <span class="sub-label">시작</span>
              <div class="input-wrapper sm">
                <input
                  type="number"
                  v-model.number="localForm.start_weight"
                  placeholder="0"
                  class="input-box bold"
                />
                <span class="unit">kg</span>
              </div>
            </div>

            <div class="weight-item">
              <span class="sub-label">목표</span>
              <div class="input-wrapper sm">
                <input
                  type="number"
                  v-model.number="localForm.goal_weight"
                  placeholder="0"
                  class="input-box"
                />
                <span class="unit">kg</span>
              </div>
            </div>
          </div>
        </div>
                
                <div class="form-group">
          <label class="label">개인 목표</label>

          <div class="goal-toggle">
            <button
              type="button"
              class="goal-btn"
              :class="{ active: localForm.goal_type === 'maintain' }"
              @click="localForm.goal_type = 'maintain'"
            >
              🧘 건강 유지
            </button>

            <button
              type="button"
              class="goal-btn"
              :class="{ active: localForm.goal_type === 'loss' }"
              @click="localForm.goal_type = 'loss'"
            >
              🔥 체중감량(체지방)
            </button>

            <button
              type="button"
              class="goal-btn"
              :class="{ active: localForm.goal_type === 'gain' }"
              @click="localForm.goal_type = 'gain'"
            >
              💪 근육량 증가
            </button>
          </div>

          <p class="helper-text subtle">
            목표에 따라 권장 탄·단·지 비율이 달라집니다.
          </p>
        </div>
        <!-- 4. 활동량 선택 -->
        <div class="form-group">
          <label class="label" for="activity">평소 활동량</label>
          <div class="select-wrapper">
            <select
              id="activity"
              v-model.number="localForm.activity_level"
              class="select-box"
            >
              <option :value="null" disabled>활동량을 선택해주세요</option>
              <option v-for="opt in activityOptions" :key="opt.value" :value="opt.value">
                {{ opt.emoji }} {{ opt.label }}
              </option>
            </select>
            <span class="arrow-icon">▼</span>
          </div>

          <p class="helper-text" v-if="currentActivityDesc">
            {{ currentActivityDesc }}
          </p>
        </div>

        <!-- 저장 버튼 -->
        <div class="action-area">
          <button type="submit" class="save-btn" :disabled="isLoading">
            {{ isLoading ? '저장 중...' : '저장하고 시작하기' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineEmits, defineProps, watchEffect } from "vue"
import http from "@/api/http"

const props = defineProps({
  initialData: { type: Object, default: () => null },
})
const emit = defineEmits(["save", "close"])
const isLoading = ref(false)

/** ✅ snake_case 통일 */
const localForm = ref({
  gender: "female",
  age: null,
  height: null,

  // ✅ 현재(weight) 입력 제거 (데이터는 서버/기존값으로 유지될 수 있음)
  weight: null,

  start_weight: null,
  goal_weight: null,
  goal_type: "maintain",
  activity_level: null,
})

watchEffect(() => {
  if (props.initialData) {
    localForm.value = { ...localForm.value, ...props.initialData }
  }
})

const activityOptions = [
  { value: 1, emoji: "🛋️", label: "거의 없음 (숨쉬기 운동만)", desc: "앉아서 일하는 시간이 대부분이에요." },
  { value: 2, emoji: "🚶", label: "가벼운 활동 (주 1-3회)", desc: "이동이 잦거나 가벼운 운동을 해요." },
  { value: 3, emoji: "🏃", label: "보통 활동 (주 3-5회)", desc: "규칙적으로 운동을 즐기는 편이에요." },
  { value: 4, emoji: "🔥", label: "매우 활동적 (주 6-7회)", desc: "격렬한 운동이나 육체 노동을 많이 해요." },
  { value: 5, emoji: "🏋️", label: "선수급 활동 (매일 2회 이상)", desc: "전문 운동선수 수준의 활동량이에요." },
]

const currentActivityDesc = computed(() => {
  const selected = activityOptions.find((o) => o.value === localForm.value.activity_level)
  return selected ? selected.desc : "라이프스타일에 맞는 활동량을 골라주세요."
})

/** ✅ payload: start/goal 중심. (weight는 기본적으로 보내지 않음) */
function toPayload(form) {
  const n = (v) => (v === null || v === "" || v === undefined ? null : Number(v))

  const payload = {
    gender: form.gender,
    age: n(form.age),
    height: n(form.height),
    start_weight: n(form.start_weight),
    goal_weight: n(form.goal_weight),
    goal_type: form.goal_type || "maintain",
    activity_level: n(form.activity_level),
  }

  // ✅ 옵션 A) 서버가 weight를 "필수"로 요구하면 시작체중으로 자동 세팅해서 보내기
  // payload.weight = n(form.start_weight)

  // ✅ 옵션 B) 서버가 기존 weight를 유지하고 싶으면(초기 데이터에 weight가 있으면) 그대로 보내기
  // payload.weight = n(form.weight ?? form.start_weight)

  return payload
}

async function saveProfile() {
  // ✅ 현재 입력을 없앴으므로, 최소 필수값 기준 재정의
  if (!localForm.value.height || !localForm.value.start_weight) {
    alert("키와 시작 체중은 필수입니다!")
    return
  }

  isLoading.value = true
  try {
    const payload = toPayload(localForm.value)
    const res = await http.patch("/profile/me/", payload)

    emit("save", res.data)
    emit("close")
  } catch (e) {
    const status = e?.response?.status
    if (status === 401) alert("로그인이 필요합니다.")
    else alert("저장 중 오류가 발생했습니다.")
    console.error("프로필 저장 실패:", e?.response?.data || e)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* ===== 기존 디자인 그대로 ===== */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.profile-card {
  width: 100%;
  max-width: 420px;
  max-height: 90vh;
  overflow-y: auto;
  background: #ffffff;
  border-radius: 32px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  padding: 40px 32px;
  position: relative;
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.profile-card::-webkit-scrollbar {
  display: none;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;

  /* ✅ 아이콘 버튼 고정 크기 */
  width: 36px;
  height: 36px;
  padding: 0;                 /* 기본 padding 제거 */
  margin: 0;

  display: inline-flex;
  align-items: center;
  justify-content: center;

  /* ✅ 기본 버튼 외형 초기화 */
  background: #fff;
  appearance: none;
  -webkit-appearance: none;

  /* ✅ X 정렬/크기 안정화 */
  font-size: 18px;
  line-height: 1;
  color: #6b7280;

  cursor: pointer;

  /* ✅ 클릭 시 생기는 outline/box-shadow(전역 스타일 포함) 방지 */
  outline: none;
  box-shadow: none;

  transition: background 0.2s, border-color 0.2s, color 0.2s, transform 0.08s;
}
.close-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.fade-in-up {
  animation: fadeInUp 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}
@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.header {
  text-align: center;
  margin-bottom: 24px;
}
.avatar-circle {
  width: 72px;
  height: 72px;
  background: #ffeef2;
  border-radius: 50%;
  margin: 0 auto 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  box-shadow: 0 6px 12px rgba(219, 31, 75, 0.1);
}
.title {
  font-size: 22px;
  font-weight: 800;
  color: #1f2937;
  margin: 0;
}
.subtitle {
  margin-top: 6px;
  font-size: 13px;
  color: #6b7280;
  line-height: 1.5;
}

.form-body {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.label {
  display: block;
  font-size: 13px;
  font-weight: 700;
  color: #374151;
  margin-bottom: 6px;
}

.gender-toggle {
  display: flex;
  background: #f3f4f6;
  padding: 4px;
  border-radius: 14px;
}
.gender-btn {
  flex: 1;
  border: none;
  background: transparent;
  padding: 10px;
  border-radius: 10px;
  font-weight: 600;
  color: #9ca3af;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 14px;
}
.gender-btn.active {
  background: #fff;
  color: #db1f4b;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.row-2 {
  display: flex;
  gap: 12px;
}
.row-2 .form-group {
  flex: 1;
}
.goal-toggle {
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
}

.goal-btn {
  border: 2px solid #f3f4f6;
  background: #f9fafb;
  padding: 12px;
  border-radius: 14px;
  font-weight: 700;
  color: #6b7280;
  cursor: pointer;
  transition: all .2s;
  text-align: left;
}

.goal-btn.active {
  background: #fff0f3;
  border-color: #db1f4b;
  color: #db1f4b;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}

.helper-text.subtle {
  background: transparent;
  color: #9ca3af;
  padding: 0;
  margin-top: 8px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.input-box {
  width: 100%;
  padding: 12px 14px;
  padding-right: 36px;
  font-size: 15px;
  border: 2px solid #f3f4f6;
  background: #f9fafb;
  border-radius: 14px;
  color: #111827;
  outline: none;
  transition: all 0.2s;
}
.input-box:focus {
  background: #fff;
  border-color: #db1f4b;
}
.unit {
  position: absolute;
  right: 14px;
  font-size: 13px;
  color: #9ca3af;
  pointer-events: none;
}

.weight-section {
  background: #fffbfc;
  border: 1px solid #ffe4e8;
  border-radius: 18px;
  padding: 16px;
}

/* ✅ 2칸용 그리드 추가 */
.weight-grid {
  display: grid;
  gap: 10px;
  align-items: end;
}
.weight-grid.two {
  grid-template-columns: 1fr 1fr;
}

.weight-item {
  text-align: center;
}
.sub-label {
  display: block;
  font-size: 11px;
  color: #6b7280;
  margin-bottom: 4px;
}

/* ✅ highlight(원래 '현재')를 '시작'에 적용 */
.weight-item.highlight .sub-label {
  color: #db1f4b;
  font-weight: 700;
}

.input-wrapper.sm .input-box {
  padding: 8px 6px;
  padding-right: 26px;
  text-align: center;
  font-size: 14px;
}

/* ✅ bold(원래 '현재')를 '시작'에 적용 */
.input-wrapper.sm .input-box.bold {
  font-weight: 700;
  color: #db1f4b;
  background: #fff;
  border-color: #ffe4e8;
}

.input-wrapper.sm .unit {
  right: 6px;
  font-size: 11px;
}

.select-wrapper {
  position: relative;
}
.select-box {
  width: 100%;
  padding: 12px 14px;
  font-size: 14px;
  border: 2px solid #f3f4f6;
  background: #f9fafb;
  border-radius: 14px;
  color: #1f2937;
  appearance: none;
}
.select-box:focus {
  border-color: #db1f4b;
  background: #fff;
}
.arrow-icon {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 11px;
  color: #9ca3af;
}
.helper-text {
  margin-top: 6px;
  font-size: 12px;
  color: #db1f4b;
  background: #fff0f3;
  padding: 6px 10px;
  border-radius: 6px;
  display: inline-block;
}

.action-area {
  margin-top: 8px;
}
.save-btn {
  width: 100%;
  padding: 14px;
  border: none;
  border-radius: 999px;
  background: linear-gradient(90deg, #db1f4b, #f03e67);
  color: white;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(219, 31, 75, 0.3);
  transition: transform 0.1s;
}
.save-btn:active {
  transform: scale(0.98);
}
.save-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

@media (max-width: 400px) {
  .profile-card {
    padding: 30px 20px;
  }
}
</style>
