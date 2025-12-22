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
            <h1 class="greeting">안녕하세요, 헬린이님! 👋</h1>
            <p class="summary">
              현재 <span class="highlight">{{ bmiStatus }}</span> 상태이며, 
              목표까지 <span class="highlight">{{ weightDiff }}kg</span> 남았어요.
            </p>
          </div>
        </div>
        <button class="edit-btn" @click="openModal">
          정보 수정
        </button>
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
          <p class="card-value">{{ profileData.weight }} <span class="unit">kg</span></p>
          <p class="card-desc">
            시작보다 {{ (profileData.weight - profileData.startWeight).toFixed(1) }}kg 변화
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
            <span class="value">{{ profileData.startWeight }} kg</span>
          </div>
          <div class="info-item">
            <span class="label">목표 체중</span>
            <span class="value">{{ profileData.goalWeight }} kg</span>
          </div>
        </div>
        
        <!-- 체중 진행 바 -->
        <div class="progress-box">
          <div class="progress-labels">
            <span>시작 {{ profileData.startWeight }}kg</span>
            <span>목표 {{ profileData.goalWeight }}kg</span>
          </div>
          <div class="progress-track">
            <div class="progress-bar" :style="{ width: progressPercent + '%' }"></div>
            <div class="current-marker" :style="{ left: progressPercent + '%' }">
              <div class="marker-dot"></div>
              <span class="marker-label">현재 {{ profileData.weight }}</span>
            </div>
          </div>
        </div>
      </section>

    </div>

    <!-- 2. 프로필 정보가 없을 때 (로딩 중이거나 최초 진입) -->
    <div v-else class="empty-state">
      <p>프로필 정보를 불러오는 중입니다...</p>
    </div>

    <!-- 3. 프로필 설정 모달 (MyProfile 컴포넌트 재사용) -->
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
import { ref, computed, onMounted } from 'vue'
import MyProfile from '@/components/MyProfile.vue'

// --- State ---
const profileData = ref(null)
const isModalOpen = ref(false)

// --- Lifecycle ---
onMounted(() => {
  // 1. 로컬 스토리지에서 데이터 확인
  const savedProfile = localStorage.getItem('hellendar_profile')
  
  if (savedProfile) {
    // 데이터가 있으면 파싱해서 보여줌
    profileData.value = JSON.parse(savedProfile)
  } else {
    // 데이터가 없으면 모달 즉시 실행
    isModalOpen.value = true
  }
})

// --- Logic ---
function handleSave(newData) {
  // 데이터 저장 (실제 앱에선 API 호출)
  profileData.value = newData
  localStorage.setItem('hellendar_profile', JSON.stringify(newData))
  
  isModalOpen.value = false
  // 알림 등 추가 가능
}

function handleClose() {
  // 만약 프로필이 아예 없는 상태에서 닫기를 누르면?
  // -> 강제로 다시 열거나, 빈 화면을 보여줄 수 있음. 
  // 여기서는 데이터가 있으면 닫고, 없으면 경고 후 유지.
  if (profileData.value) {
    isModalOpen.value = false
  } else {
    alert("서비스 이용을 위해 프로필 설정이 필요해요! 😅")
  }
}

function openModal() {
  isModalOpen.value = true
}

// --- Computed Stats ---
// 1. BMI 계산: 몸무게(kg) / (키(m) * 키(m))
const bmiValue = computed(() => {
  if (!profileData.value) return 0
  const h = profileData.value.height / 100
  const w = profileData.value.weight
  return (w / (h * h)).toFixed(1)
})

const bmiStatus = computed(() => {
  const bmi = parseFloat(bmiValue.value)
  if (bmi < 18.5) return '저체중'
  if (bmi < 23) return '정상'
  if (bmi < 25) return '과체중'
  return '비만'
})

const bmiClass = computed(() => {
  const status = bmiStatus.value
  if (status === '정상') return 'good'
  if (status === '저체중') return 'warn'
  return 'danger'
})

// 2. BMR (기초대사량) - 해리스-베네딕트 공식 약식
const bmrValue = computed(() => {
  if (!profileData.value) return 0
  const { gender, weight, height, age } = profileData.value
  // 남성: 66.47 + (13.75 × 체중) + (5 × 키) - (6.76 × 나이)
  // 여성: 655.1 + (9.56 × 체중) + (1.85 × 키) - (4.68 × 나이)
  let base = 0
  if (gender === 'male') {
    base = 66.47 + (13.75 * weight) + (5 * height) - (6.76 * age)
  } else {
    base = 655.1 + (9.56 * weight) + (1.85 * height) - (4.68 * age)
  }
  
  // 활동량 계수 (단순화)
  // 1->1.2, 2->1.375, 3->1.55, 4->1.725, 5->1.9
  const activityMap = { 1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9 }
  const multiplier = activityMap[profileData.value.activityLevel] || 1.2
  
  return Math.round(base * multiplier)
})

// 3. 목표까지 남은 체중 & 진행률
const weightDiff = computed(() => {
  if (!profileData.value) return 0
  return Math.abs(profileData.value.weight - profileData.value.goalWeight).toFixed(1)
})

const progressPercent = computed(() => {
  if (!profileData.value) return 0
  const { startWeight, goalWeight, weight } = profileData.value
  const totalDiff = Math.abs(startWeight - goalWeight)
  const currentDiff = Math.abs(startWeight - weight)
  
  if (totalDiff === 0) return 100
  let pct = (currentDiff / totalDiff) * 100
  return Math.min(Math.max(pct, 0), 100) // 0~100 사이
})

</script>

<style scoped>
/* 페이지 전체 컨테이너 */
.profile-page {
  min-height: 100vh;
  background-color: #f9fafb;
  padding: 40px 20px;
  max-width: 1000px;
  margin: 0 auto;
}

/* 대시보드 페이드인 */
.fade-in {
  animation: fadeIn 0.8s ease forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* --- 상단 헤더 --- */
.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  background: white;
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

/* --- 스탯 그리드 --- */
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
.stat-card:hover {
  transform: translateY(-4px);
}
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
.stat-card.highlight .card-icon {
  background: rgba(255,255,255,0.2);
}

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

.card-title {
  font-size: 14px; color: #6b7280; margin: 0 0 8px; font-weight: 600;
}
.card-value {
  font-size: 28px; font-weight: 800; color: #111827; margin: 0 0 4px;
}
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

/* --- 상세 패널 --- */
.detail-panel {
  background: white;
  padding: 30px;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}
.panel-title {
  font-size: 18px; font-weight: 800; margin: 0 0 24px; color: #111827;
}

.info-row {
  display: flex; gap: 40px; flex-wrap: wrap; margin-bottom: 40px;
}
.info-item { display: flex; flex-direction: column; gap: 6px; }
.info-item .label { font-size: 13px; color: #6b7280; font-weight: 600; }
.info-item .value { font-size: 18px; color: #1f2937; font-weight: 700; }

/* 프로그래스 바 */
.progress-box { position: relative; padding-top: 10px; }
.progress-labels {
  display: flex; justify-content: space-between; font-size: 12px; color: #9ca3af; margin-bottom: 8px;
}
.progress-track {
  height: 12px; background: #f3f4f6; border-radius: 99px; position: relative;
}
.progress-bar {
  height: 100%; background: #db1f4b; border-radius: 99px; transition: width 1s ease;
}
.current-marker {
  position: absolute; top: 50%; transform: translate(-50%, -50%);
  display: flex; flex-direction: column; align-items: center;
}
.marker-dot {
  width: 20px; height: 20px; background: white; border: 4px solid #db1f4b; border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.marker-label {
  position: absolute; top: 24px; font-size: 12px; font-weight: 700; color: #db1f4b; white-space: nowrap;
}

/* 빈 상태 */
.empty-state {
  height: 80vh; display: flex; align-items: center; justify-content: center; color: #9ca3af;
}

/* Modal Transition */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .dash-header { flex-direction: column; align-items: flex-start; gap: 20px; }
  .edit-btn { align-self: flex-end; }
  .info-row { gap: 20px; justify-content: space-between; }
  .info-item { width: 45%; }
}
</style>