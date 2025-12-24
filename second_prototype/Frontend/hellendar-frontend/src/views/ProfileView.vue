<template>
  <div class="profile-page">
    <!-- 1. 프로필 정보가 있을 때: 웹사이트 대시보드 뷰 -->
    <div v-if="profileData" class="dashboard-container fade-in">
      <!-- 상단 헤더: 프로필 요약 -->
      <header class="dash-header">
        <div class="user-intro">
          <div class="user-avatar">
            {{ profileData.gender === 'male' ? '👦' : '👧' }}
          </div>
          <div class="user-text">
            <h1 class="greeting">안녕하세요, {{ displayName }}님! 👋</h1>
            <p class="summary">
              현재 <span class="highlight">{{ bmiStatus }}</span> 상태이며,
              <template v-if="goalReachedText">
                <span class="goal-msg">{{ goalReachedText }}</span>
              </template>
              <template v-else>
                목표까지 <span class="highlight">{{ weightDiff }}kg</span> 남았어요.
              </template>
            </p>
          </div>
        </div>
        <button class="edit-btn" @click="openModal">
          정보 수정
        </button>
        <button class="edit-btn" @click="openAccountModal">
          회원정보 수정
        </button>

        <AccountManageModal
          v-if="isAccountModalOpen"
          @close="isAccountModalOpen = false"
          @loggedOut="handleLoggedOut"
        />

      </header>

      <!-- 메인 스탯 그리드 -->
      <section class="stats-grid">
        <!-- BMI 카드 -->
        <article class="stat-card">
          <div class="card-icon blue">⚖️</div>
          <h3 class="card-title">BMI 지수</h3>
          <p class="card-value">{{ bmiValue }}</p>
          <div class="bmi-badge" :class="bmiClass">{{ bmiStatus }}</div>
        </article>

        <!-- 활동량 카드 -->
        <article class="stat-card">
          <div class="card-icon yellow">🔥</div>
          <h3 class="card-title">기초 대사량(추정)</h3>
          <p class="card-value">{{ bmrValue }} <span class="unit">kcal</span></p>
          <p class="card-desc">하루 권장 섭취량</p>
        </article>

        <!-- 현재 체중 카드 -->
        <article class="stat-card highlight">
          <div class="card-icon pink">💪</div>
          <h3 class="card-title">현재 체중</h3>
          <p class="card-value">{{ currentWeightText }} <span class="unit">kg</span></p>
          <p class="card-desc">
            시작보다 {{ ((currentWeight ?? 0) - (profileData.start_weight ?? (currentWeight ?? 0))).toFixed(1) }}kg 변화
          </p>
        </article>
      </section>

      <!-- 상세 정보 패널 -->
      <section class="detail-panel">
        <h2 class="panel-title">상세 리포트</h2>
        <div class="info-row">
          <div class="info-item">
            <span class="label">키</span>
            <span class="value">{{ profileData.height }} cm</span>
          </div>
          <div class="info-item">
            <span class="label">나이</span>
            <span class="value">{{ profileData.age }} 세</span>
          </div>
          <div class="info-item">
            <span class="label">시작 체중</span>
            <span class="value">{{ profileData.start_weight }} kg</span>
          </div>
          <div class="info-item">
            <span class="label">목표 체중</span>
            <span class="value">{{ profileData.goal_weight }} kg</span>
          </div>
        </div>

        <!-- 체중 진행 바 -->
        <div class="progress-box">
          <div class="progress-labels">
            <span>시작 {{ profileData.start_weight }}kg</span>
            <span>목표 {{ profileData.goal_weight }}kg</span>
          </div>
          <div class="progress-track">
            <div class="progress-bar" :style="progressBarStyle"></div>

            <div class="current-marker" :style="{ left: progressPercent + '%' }">
              <div class="marker-dot" :style="markerDotStyle"></div>
              <span class="marker-label" :style="markerLabelStyle">현재 {{ currentWeightText }}</span>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 2. 프로필 정보가 없을 때 -->
    <div v-else class="empty-state">
      <p v-if="loading">프로필 정보를 불러오는 중입니다...</p>
      <p v-else>프로필 정보가 없습니다. 설정을 진행해주세요.</p>
    </div>

    <!-- 3. 프로필 설정 모달 -->
    <Transition name="modal">
      <MyProfile
        v-if="isModalOpen"
        :initial-data="profileData"
        @save="handleSave"
        @close="handleClose"
      />
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"
import http from "@/api/http"
import MyProfile from "@/components/MyProfile.vue"
import { useAuthStore } from "@/stores/auth"  
import AccountManageModal from "@/components/AccountManageModal.vue"

const router = useRouter()
const auth = useAuthStore() 

const profileData = ref(null)
const isModalOpen = ref(false)
const isAccountModalOpen = ref(false)
const loading = ref(false)
const displayName = computed(() => {
  // 백엔드에 따라 username / name / nickname 중 하나일 수 있으니 안전하게
  return auth.me?.username || auth.me?.name || auth.me?.nickname || "헬린이"
})

async function fetchProfile() {
  loading.value = true
  try {
    const res = await http.get("/profile/me/")
    profileData.value = res.data

    // ✅ “최초 1회 자동 오픈” 판단 로직 (백엔드 flag 없어도 동작)
    const p = profileData.value

    // 일부 구현(또는 서버 응답)에서는 `weight` 대신 `start_weight`만 있는 경우가 있음.
    // 이런 경우를 위해 start_weight를 fallback으로 사용해서 최초 오픈 판단을 해야 함.
    const hasWeight =
      (p?.weight !== null && p?.weight !== undefined && p?.weight !== "") ||
      (p?.start_weight !== null && p?.start_weight !== undefined && p?.start_weight !== "")

    const isComplete =
      !!p?.height &&
      !!hasWeight &&
      !!p?.gender &&
      (p?.activity_level !== null && p?.activity_level !== undefined)

    // 완성돼 있으면 자동 오픈 X
    isModalOpen.value = !isComplete
  } catch (e) {
    const status = e?.response?.status

    if (status === 401) {
      router.push("/login")
    } else {
      console.error(e)
      alert("프로필 정보를 불러오는 중 오류가 발생했습니다.")
    }
  } finally {
    loading.value = false
  }
}



onMounted(async () => {
  // ✅ me가 없으면 먼저 가져오기
  if (!auth.me) {
    try { await auth.fetchMe() } catch {}
  }
  fetchProfile()
})

const currentWeight = computed(() => {
  const p = profileData.value
  if (!p) return null

  // weight가 null/undefined/"" 이면 start_weight로 대체
  const w = p.weight
  if (w !== null && w !== undefined && w !== "") return Number(w)

  const sw = p.start_weight
  if (sw !== null && sw !== undefined && sw !== "") return Number(sw)

  return null
})

const currentWeightText = computed(() => {
  return currentWeight.value == null ? "-" : Number(currentWeight.value).toFixed(1)
})

function handleSave(saved) {
  // MyProfile에서 PATCH 성공 후 전달된 최신 데이터
  profileData.value = saved
  isModalOpen.value = false
}

function handleClose() {
  // 프로필이 없는 상태면 닫기 막기(원하면 정책 변경 가능)
  if (profileData.value) {
    isModalOpen.value = false
  } else {
    alert("서비스 이용을 위해 프로필 설정이 필요해요!")
    isModalOpen.value = true
  }
}

function openModal() {
  isModalOpen.value = true
}

function openAccountModal() {
  isAccountModalOpen.value = true
}

function handleLoggedOut() {
  // 로그아웃/탈퇴 이후 공통 이동
  router.replace("/login")
}

/* ---------- Computed Stats ---------- */

const goalReachedText = computed(() => {
  if (!profileData.value) return ""

  const start = Number(profileData.value.start_weight)
  const goal = Number(profileData.value.goal_weight)
  const current = Number(profileData.value.weight)

  // 값이 하나라도 없으면 멘트 없음
  if (!Number.isFinite(start) || !Number.isFinite(goal) || !Number.isFinite(current)) return ""

  // 시작 > 목표 : 감량 목표 → current <= goal 이면 달성
  if (start > goal && current <= goal) return "목표 체중에 도달했습니다!"

  // 시작 < 목표 : 증량 목표 → current >= goal 이면 달성
  if (start < goal && current >= goal) return "목표 체중에 도달했습니다!"

  // 시작 == 목표 : 현재가 목표와 같으면 달성
  if (start === goal && current === goal) return "목표 체중에 도달했습니다!"

  return ""
})


const bmiValue = computed(() => {
  if (!profileData.value?.height || currentWeight.value == null) return 0
  const h = profileData.value.height / 100
  const w = currentWeight.value
  return (w / (h * h)).toFixed(1)
})


const bmiStatus = computed(() => {
  const bmi = parseFloat(bmiValue.value)
  if (!bmi) return "-"
  if (bmi < 18.5) return "저체중"
  if (bmi < 23) return "정상"
  if (bmi < 25) return "과체중"
  return "비만"
})

const bmiClass = computed(() => {
  const status = bmiStatus.value
  if (status === "정상") return "good"
  if (status === "저체중") return "warn"
  if (status === "-") return "warn"
  return "danger"
})

const bmrValue = computed(() => {
  if (!profileData.value) return 0
  const { gender, height, age, activity_level } = profileData.value
  const weight = currentWeight.value

  if (!weight || !height || !age) return 0

  let base = 0
  if (gender === "male") base = 66.47 + (13.75 * weight) + (5 * height) - (6.76 * age)
  else base = 655.1 + (9.56 * weight) + (1.85 * height) - (4.68 * age)

  const activityMap = { 1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9 }
  const multiplier = activityMap[activity_level] || 1.2

  return Math.round(base * multiplier)
})

const weightDiff = computed(() => {
  if (currentWeight.value == null || !profileData.value?.goal_weight) return 0
  return Math.abs(currentWeight.value - profileData.value.goal_weight).toFixed(1)
})


const progressPercent = computed(() => {
  if (!profileData.value) return 0

  const start = Number(profileData.value.start_weight)
  const goal = Number(profileData.value.goal_weight)

  // ✅ 캘린더에서 체중 입력이 없으면 start_weight를 현재로 간주 (안전)
  const currentRaw = profileData.value.weight ?? profileData.value.start_weight
  const current = Number(currentRaw)

  if ([start, goal, current].some((v) => Number.isNaN(v))) return 0
  if (start === goal) return current === goal ? 100 : 0

  // 감량 목표: start > goal  → 진행 = (start - current) / (start - goal)
  if (start > goal) {
    const denom = start - goal
    const numer = start - current
    const ratio = numer / denom // numer < 0 이면 역방향(증가)
    return Math.min(Math.max(ratio * 100, 0), 100) // ✅ 역방향이면 0%로 고정
  }

  // 증량 목표: start < goal → 진행 = (current - start) / (goal - start)
  const denom = goal - start
  const numer = current - start
  const ratio = numer / denom // numer < 0 이면 역방향(감소)
  return Math.min(Math.max(ratio * 100, 0), 100)   // ✅ 역방향이면 0%로 고정
})


const isGoalAchieved = computed(() => {
  if (!profileData.value) return false
  const { start_weight, goal_weight } = profileData.value
  const weight = currentWeight.value
  if (start_weight == null || goal_weight == null || weight == null) return false

  const start = Number(start_weight)
  const goal = Number(goal_weight)
  const current = Number(weight)

  if (start < goal) return current >= goal
  if (start > goal) return current <= goal
  return current === goal
})


const progressBarStyle = computed(() => {
  // 기존 width는 그대로 사용
  const width = progressPercent.value + "%"

  // ✅ 달성: 초록 그라데이션 + 은은한 글로우
  if (isGoalAchieved.value) {
    return {
      width,
      background: "linear-gradient(90deg, #86efac 0%, #16a34a 55%, #0f766e 100%)",
      boxShadow: "0 6px 16px rgba(22, 163, 74, 0.25)",
    }
  }

  // ✅ 미달성: 핑크 그라데이션 (기존 톤 유지)
  return {
    width,
    background: "linear-gradient(90deg, #ff9a9e 0%, #db1f4b 60%, #b9153b 100%)",
    boxShadow: "none",
  }
})

const markerDotStyle = computed(() => {
  // dot 테두리색을 progress와 동기화
  return {
    borderColor: isGoalAchieved.value ? "#16a34a" : "#db1f4b",
  }
})

const markerLabelStyle = computed(() => {
  return {
    color: isGoalAchieved.value ? "#16a34a" : "#db1f4b",
  }
})


</script>

<style scoped>
/* ===== 기존 디자인 그대로 ===== */
.profile-page {
  min-height: 100vh;
  background-color: #f9fafb;
  padding: 40px 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.fade-in {
  animation: fadeIn 0.8s ease forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  background: rgb(255, 255, 255);
  padding: 30px;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}

.user-intro {
  display: flex;
  align-items: center;
  gap: 20px;
}
.user-avatar {
  width: 64px;
  height: 64px;
  font-size: 32px;
  background: #ffeef2;
  border-radius: 50%;
  display: grid;
  place-items: center;
}
.greeting {
  font-size: 24px;
  font-weight: 800;
  color: #111827;
  margin: 0 0 8px;
}
.summary {
  font-size: 15px;
  color: #6b7280;
  margin: 0;
}
.highlight {
  color: #db1f4b;
  font-weight: 700;
}

.edit-btn {
  padding: 10px 20px;
  border-radius: 99px;
  border: 1px solid #e5e7eb;
  background: white;
  color: #374151;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.edit-btn:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  transition: transform 0.2s;
}
.stat-card:hover { transform: translateY(-4px); }

.stat-card.highlight {
  background: linear-gradient(135deg, #db1f4b 0%, #ff5e83 100%);
  color: white;
}
.stat-card.highlight .card-title,
.stat-card.highlight .card-value,
.stat-card.highlight .card-desc,
.stat-card.highlight .unit {
  color: white;
}
.stat-card.highlight .card-icon { background: rgba(255,255,255,0.2); }

.card-icon {
  width: 40px; height: 40px;
  border-radius: 12px;
  display: grid; place-items: center;
  font-size: 20px;
  margin-bottom: 16px;
}
.card-icon.blue { background: #eff6ff; }
.card-icon.yellow { background: #fffbeb; }
.card-icon.pink { background: #ffeef2; }

.card-title { font-size: 14px; color: #6b7280; margin: 0 0 8px; font-weight: 600; }
.card-value { font-size: 28px; font-weight: 800; color: #111827; margin: 0 0 4px; }
.unit { font-size: 16px; font-weight: 600; color: #9ca3af; }
.card-desc { font-size: 13px; color: #9ca3af; margin: 0; }

.bmi-badge {
  margin-top: auto;
  padding: 4px 12px;
  border-radius: 99px;
  font-size: 12px;
  font-weight: 700;
}
.bmi-badge.good { background: #dcfce7; color: #166534; }
.bmi-badge.warn { background: #fef9c3; color: #854d0e; }
.bmi-badge.danger { background: #fee2e2; color: #991b1b; }

.detail-panel {
  background: white;
  padding: 30px;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}
.panel-title { font-size: 18px; font-weight: 800; margin: 0 0 24px; color: #111827; }

.info-row {
  display: flex; gap: 40px; flex-wrap: wrap; margin-bottom: 40px;
}
.info-item { display: flex; flex-direction: column; gap: 6px; }
.info-item .label { font-size: 13px; color: #6b7280; font-weight: 600; }
.info-item .value { font-size: 18px; color: #1f2937; font-weight: 700; }

.progress-box { position: relative; padding-top: 10px; }
.progress-labels {
  display: flex; justify-content: space-between; font-size: 12px; color: #9ca3af; margin-bottom: 8px;
}
.progress-track { height: 12px; background: #f3f4f6; border-radius: 99px; position: relative; }
.progress-bar { height: 100%; background: #db1f4b; border-radius: 99px; transition: width 1s ease; }
.current-marker {
  position: absolute; top: 50%; transform: translate(-50%, -50%);
  display: flex; flex-direction: column; align-items: center;
}
.marker-dot {
  width: 20px;
  height: 20px;
  background: white;
  border: 4px solid;         /* ✅ 색상은 인라인(style)에서 주입 */
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.marker-label {
  position: absolute;
  top: 24px;
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
  /* ✅ color는 인라인(style)에서 주입 */
}


.empty-state {
  height: 80vh; display: flex; align-items: center; justify-content: center; color: #9ca3af;
}

.modal-enter-active,
.modal-leave-active { transition: opacity 0.3s ease; }
.modal-enter-from,
.modal-leave-to { opacity: 0; }

@media (max-width: 768px) {
  .dash-header { flex-direction: column; align-items: flex-start; gap: 20px; }
  .edit-btn { align-self: flex-end; }
  .info-row { gap: 20px; justify-content: space-between; }
  .info-item { width: 45%; }
}
</style>
