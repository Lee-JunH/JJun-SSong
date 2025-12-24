<template>
  <div class="page-container">
    <!-- 0. 내비게이션 바 -->
    <nav class="navbar">
      <div class="nav-content">
        <div class="logo">
          <span class="logo-icon bounce-on-hover">🍴</span>
          <span class="logo-text">MY헬린더</span>
        </div>
        <div class="nav-links">
          <a 
            href="#" 
            :class="{ active: currentView === 'calendar' }" 
            @click.prevent="currentView = 'calendar'"
          >캘린더</a>
          <a 
            href="#" 
            :class="{ active: currentView === 'report' }" 
            @click.prevent="goReportWithReload"
          >리포트</a>
        </div>
      </div>
    </nav>

    <!-- 1. 메인 콘텐츠 -->
    <main class="main-content">
      <!-- A. 캘린더 화면 -->
      <div class="calendar-wrapper" v-if="currentView === 'calendar'">
        <!-- 방향에 따라 트랜지션 이름이 동적으로 변경됨 (slide-next 또는 slide-prev) -->
        <Transition :name="transitionDirection" mode="out-in">
          <MonthCalendar
            :key="month"
            :month="month"
            :summaries="cal.byDate"
            :loading="cal.loading"
            :error="cal.error"
            :selectedDate="selectedDate"
            @changeMonth="onChangeMonth"
            @select="onSelect"
          >
            <template #date-cell="{ date, data }">
              <div class="meal-buttons" v-if="date <= today">
                <button 
                  class="meal-btn" 
                  :class="{ 'active': data?.breakfast, 'clicked': activeBtn === `${date}-breakfast` }"
                  @click.stop="triggerAnim(date, 'breakfast'); toggleMeal(date, 'breakfast')"
                  title="아침"
                >☀️</button>
                <button 
                  class="meal-btn" 
                  :class="{ 'active': data?.lunch, 'clicked': activeBtn === `${date}-lunch` }"
                  @click.stop="triggerAnim(date, 'lunch'); toggleMeal(date, 'lunch')"
                  title="점심"
                >🌤️</button>
                <button 
                  class="meal-btn" 
                  :class="{ 'active': data?.dinner, 'clicked': activeBtn === `${date}-dinner` }"
                  @click.stop="triggerAnim(date, 'dinner'); toggleMeal(date, 'dinner')"
                  title="저녁"
                >🌜</button>
                <button 
                  class="meal-btn" 
                  :class="{ 'active': data?.nutrition, 'clicked': activeBtn === `${date}-nutrition` }"
                  @click.stop="triggerAnim(date, 'nutrition'); toggleMeal(date, 'nutrition')"
                  title="영양제"
                >💊</button>
              </div>
            </template>
          </MonthCalendar>
        </Transition>
      </div>

      <!-- B. 리포트 화면 -->
      <div class="report-wrapper" v-show="currentView === 'report'">
        <HealthReport :active="currentView === 'report'" />
      </div>
    </main>

    <!-- 2. 식단 입력 모달 -->
    <Transition name="modal-pop">
      <div v-if="isModalOpen" class="modal-backdrop" @click.self="closeModal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>{{ selectedDate }} 식단 관리</h3>
            <button class="close-btn" @click="closeModal">&times;</button>
          </div>
          
          <div class="modal-body">
            <DayDetailPanel 
              v-if="selectedDate" 
              :date="selectedDate"
              @close="closeModal" 
            />
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import dayjs from "dayjs"
import { ref, onMounted, watch } from "vue"
import { useCalendarStore } from "@/stores/calendar"
import MonthCalendar from "@/components/MonthCalendar.vue"
import DayDetailPanel from "@/components/DayDetailPanel.vue"
import HealthReport from "@/components/HealthReport.vue"

const cal = useCalendarStore()
const month = ref(dayjs().format("YYYY-MM"))
const today = dayjs().format("YYYY-MM-DD")
const selectedDate = ref(dayjs().format("YYYY-MM-DD"))
const isModalOpen = ref(false)

// 현재 보여줄 화면 상태 ('calendar' | 'report')
const currentView = ref('calendar')

// 애니메이션 방향 제어용 상태 ('slide-next' | 'slide-prev')
const transitionDirection = ref('slide-next')

const activeBtn = ref(null)

onMounted(async () => {
  // ✅ 새로고침 후 리포트 자동 오픈 플래그 처리
  const nextView = sessionStorage.getItem("healendar_next_view")
  if (nextView) {
   currentView.value = nextView
    sessionStorage.removeItem("healendar_next_view")
  }

  await cal.fetchMonth(month.value)
})

watch(
  () => currentView.value,
  async (v) => {
    if (v === "report") {
      await cal.fetchMonth(month.value)
    }
  }
)

function goReportWithReload() {
  // 이미 리포트면 굳이 새로고침 안 함(원하면 제거 가능)
  if (currentView.value === "report") return

  // ✅ 새로고침 후 리포트로 열리게 플래그 저장
  sessionStorage.setItem("healendar_next_view", "report")

  // ✅ “리포트 선택 시 자동 새로고침 1회”
  window.location.reload()
}

async function onChangeMonth(m) {
  // 현재 달과 새로운 달을 비교하여 방향 결정
  if (m > month.value) {
    transitionDirection.value = 'slide-next'
  } else {
    transitionDirection.value = 'slide-prev'
  }

  month.value = m
  await cal.fetchMonth(m)
}

function onSelect(d) {
  selectedDate.value = d
  isModalOpen.value = true
}

function closeModal() {
  isModalOpen.value = false
}

function triggerAnim(date, type) {
  const key = `${date}-${type}`
  activeBtn.value = key
  setTimeout(() => {
    if (activeBtn.value === key) activeBtn.value = null
  }, 300)
}

async function toggleMeal(date, mealType) {
  const cur = cal.byDate[date] || {}
  const next = !Boolean(cur[mealType])
  await cal.patchToggles(date, { [mealType]: next })
}
</script>

<style scoped>
/* --- 전체 레이아웃 --- */
.page-container {
  min-height: 100vh;
  background-color: #f8f9fa;
  display: flex;
  flex-direction: column;
  animation: pageFadeIn 0.6s ease-out;
}

@keyframes pageFadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* --- Navbar 디자인 --- */
.navbar {
  background: white;
  height: 64px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: box-shadow 0.3s;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 1.25rem;
  color: #2c3e50;
  margin-right: 40px;
  cursor: default;
}

.logo-icon {
  font-size: 1.5rem;
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.logo:hover .logo-icon {
  transform: rotate(-10deg) scale(1.2);
}

.nav-links {
  display: flex;
  gap: 24px;
  flex: 1;
}

.nav-links a {
  text-decoration: none;
  color: #6c757d;
  font-weight: 500;
  padding: 8px 0;
  position: relative;
  transition: color 0.3s;
  cursor: pointer;
}

.nav-links a:hover, .nav-links a.active {
  color: #db1f4b;
}

.nav-links a::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0%;
  height: 2px;
  background-color: #db1f4b;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.nav-links a.active::after,
.nav-links a:hover::after {
  width: 100%;
}

/* --- 메인 콘텐츠 --- */
.main-content {
  flex: 1;
  padding: 30px 20px;
  display: flex;
  justify-content: center;
  overflow-x: hidden; /* 슬라이드 시 가로 스크롤 방지 */
}

.calendar-wrapper {
  width: 100%;
  max-width: 1000px;
  background: transparent;
}

.report-wrapper {
  width: 100%;
  max-width: 1000px;
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* --- 식사 버튼 스타일 --- */
.meal-buttons {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 6px;
  margin-top: 0;
  padding-top: 0;
}

.meal-btn {
  width: 100%;
  height: 100%;
  padding: 0;
  border: 0;
  border-radius: 12px;
  background: #f1f3f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: clamp(16px, 2.2vw, 26px);
  line-height: 1;
  cursor: pointer;
  filter: grayscale(100%);
  opacity: 0.5;
  transform: scale(1);
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
  outline: none;
}

.meal-btn:hover {
  transform: scale(1.05);
  opacity: 0.8;
  filter: grayscale(50%);
}

.meal-btn.active {
  filter: grayscale(0%);
  opacity: 1;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
  outline: none;
}


.meal-btn:nth-child(1).active { background-color: #FFB74D; }
.meal-btn:nth-child(2).active { background-color: #81C784; }
.meal-btn:nth-child(3).active { background-color: #64B5F6; }
.meal-btn:nth-child(4).active { background-color: #BA68C8; }

.meal-btn:focus-visible {
  outline: 2px solid #db1f4b;
  outline-offset: 2px;
}

/* --- 모달 스타일 --- */
.modal-backdrop {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-color: rgba(0,0,0,0.4);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-content {
  background: white;
  width: 90%;
  max-width: 800px;
  border-radius: 20px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.15);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 85vh;
  border: 1px solid rgba(255,255,255,0.8);
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid #f1f3f5;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #212529;
  font-weight: 700;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  line-height: 1;
  cursor: pointer;
  color: #ced4da;
  transition: all 0.2s;
}

.close-btn:hover { 
  color: #495057; 
  transform: rotate(90deg);
}

.modal-body { padding: 0; flex: 1; overflow-y: auto; }

/* --- Vue Transitions (애니메이션 정의) --- */

/* 1. 모달 팝업 */
.modal-pop-enter-active, .modal-pop-leave-active {
  transition: opacity 0.3s ease;
}
.modal-pop-enter-active .modal-content {
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.modal-pop-leave-active .modal-content {
  transition: transform 0.3s ease-in;
}

.modal-pop-enter-from, .modal-pop-leave-to {
  opacity: 0;
}
.modal-pop-enter-from .modal-content {
  transform: translateY(30px) scale(0.95);
}
.modal-pop-leave-to .modal-content {
  transform: translateY(30px) scale(0.95);
}

/* 2. 월 이동 슬라이드 효과 (수정됨: 짧고 간결한 Fade/Slide) */
/* 공통 활성화 상태 - 시간 단축 (0.5s -> 0.3s) */
.slide-next-enter-active, .slide-next-leave-active,
.slide-prev-enter-active, .slide-prev-leave-active {
  transition: all 0.3s ease;
}

/* [다음 달] Next: 살짝 오른쪽에서 들어옴 */
.slide-next-enter-from {
  opacity: 0;
  transform: translateX(20px); /* 50px -> 20px */
}
.slide-next-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* [이전 달] Prev: 살짝 왼쪽에서 들어옴 */
.slide-prev-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}
.slide-prev-leave-to {
  opacity: 0;
  transform: translateX(20px);
}


/* --- [핵심] 버튼 슬라이딩 방지 트릭 --- */
/* 달력이 슬라이드 되는 동안(Leave Active) 버튼을 숨깁니다 */
.slide-next-leave-active .meal-btn,
.slide-prev-leave-active .meal-btn {
  opacity: 0 !important;
  transition: opacity 0.1s !important; /* 빠르게 사라짐 */
}

/* 새로운 달력이 들어올 때(Enter From)도 버튼은 숨겨진 상태 */
.slide-next-enter-from .meal-btn,
.slide-prev-enter-from .meal-btn {
  opacity: 0 !important;
  transform: scale(0.8);
}

/* 새로운 달력이 자리를 잡은 뒤(Enter Active) 버튼이 나타남 */
/* 0.15s 딜레이를 주어 달력이 거의 멈춘 뒤에 버튼이 팝업되도록 함 */
.slide-next-enter-active .meal-btn,
.slide-prev-enter-active .meal-btn {
  transition: opacity 0.3s ease 0.15s, transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) 0.15s !important;
}
</style>