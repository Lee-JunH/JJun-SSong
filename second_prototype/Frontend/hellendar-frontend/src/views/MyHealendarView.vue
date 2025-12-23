<template>
  <div class="page-container">
    <!-- 0. 내비게이션 바 -->
    <nav class="navbar">
      <div class="nav-content">
        <div class="logo">
          <span class="logo-icon">🍴</span>
          <span class="logo-text">MY헬린더</span>
        </div>
        <div class="nav-links">
          <a href="#" class="active">캘린더</a>
          <a href="#">리포트</a>
        </div>
        <div class="user-profile">
          <div class="avatar">U</div>
        </div>
      </div>
    </nav>

    <!-- 1. 메인 콘텐츠 (달력 영역) -->
    <main class="main-content">
      <div class="calendar-wrapper">
        <MonthCalendar
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
                :class="{ active: data?.breakfast }"
                @click.stop="toggleMeal(date, 'breakfast')"
                title="아침"
              >☀️</button>
              <button 
                class="meal-btn" 
                :class="{ active: data?.lunch }"
                @click.stop="toggleMeal(date, 'lunch')"
                title="점심"
              >🌤️</button>
              <button 
                class="meal-btn" 
                :class="{ active: data?.dinner }"
                @click.stop="toggleMeal(date, 'dinner')"
                title="저녁"
              >🌜</button>
              <button 
                class="meal-btn" 
                :class="{ active: data?.nutrition }"
                @click.stop="toggleMeal(date, 'nutrition')"
                title="영양제"
              >💊</button>
            </div>
          </template>
        </MonthCalendar>
      </div>
    </main>

    <!-- 2. 식단 입력 모달 -->
    <Transition name="modal-fade">
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
import { ref, onMounted } from "vue"
import { useCalendarStore } from "@/stores/calendar"
import MonthCalendar from "@/components/MonthCalendar.vue"
import DayDetailPanel from "@/components/DayDetailPanel.vue"

const cal = useCalendarStore()
const month = ref(dayjs().format("YYYY-MM"))
const today = dayjs().format("YYYY-MM-DD")
const selectedDate = ref(dayjs().format("YYYY-MM-DD"))
const isModalOpen = ref(false)

onMounted(async () => {
  await cal.fetchMonth(month.value)
})

async function onChangeMonth(m) {
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

async function toggleMeal(date, mealType) {
  console.log(`${date}의 ${mealType} 상태 변경`)

  const cur = cal.byDate[date] || {}
  const next = !Boolean(cur[mealType])

  await cal.patchToggles(date, { [mealType]: next })
}
</script>

<style scoped>
/* --- 전체 레이아웃 --- */
.page-container {
  min-height: 100vh;
  background-color: #f8f9fa; /* 부드러운 배경색 */
  display: flex;
  flex-direction: column;
}

/* --- Navbar 디자인 --- */
.navbar {
  background: white;
  height: 64px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  position: sticky;
  top: 0;
  z-index: 100;
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
}
.logo-icon { font-size: 1.5rem; }

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
  transition: color 0.2s;
}

.nav-links a:hover, .nav-links a.active {
  color: #db1f4b;
}

.nav-links a.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #db1f4b;
  border-radius: 2px;
}

.user-profile .avatar {
  width: 36px;
  height: 36px;
  background: #e9ecef;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #495057;
  font-weight: bold;
  cursor: pointer;
}

/* --- 메인 콘텐츠 --- */
.main-content {
  flex: 1;
  padding: 30px 20px;
  display: flex;
  justify-content: center;
}

.calendar-wrapper {
  width: 100%;
  max-width: 1000px; /* 캘린더 최대 너비 조정 */
  background: transparent; /* 캘린더 배경은 투명하게 (카드 스타일은 MonthCalendar에서 처리) */
}

/* --- 식사 버튼 스타일 --- */
.meal-buttons {
  /* 기존: width: fit-content; 제거 */
  width: 100%;
  height: 100%;

  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);

  gap: 6px;           /* 버튼 사이 간격 */
  margin-top: 0;      /* 기존 auto 제거 */
  padding-top: 0;     /* 기존 6px 제거 */
}

.meal-btn {
  /* 기존: width/height 28px 제거 */
  width: 100%;
  height: 100%;

  /* 전역 button padding 영향 제거 */
  padding: 0;
  border: 0;

  border-radius: 12px;
  background: #f1f3f5;

  display: flex;
  align-items: center;
  justify-content: center;

  /* 이모지 크기: 화면/셀 크기에 따라 유연하게 */
  font-size: clamp(16px, 2.2vw, 26px);
  line-height: 1;

  cursor: pointer;
  transition: transform 0.15s ease, background-color 0.15s ease, opacity 0.15s ease;
  filter: grayscale(100%);
  opacity: 0.65;
}

.meal-btn:hover {
  transform: translateY(-1px);
  filter: grayscale(0%);
  opacity: 1;
}

.meal-btn.active {
  filter: grayscale(0%);
  opacity: 1;
}

.meal-btn:nth-child(1).active { background-color: #FFB74D; }
.meal-btn:nth-child(2).active { background-color: #81C784; }
.meal-btn:nth-child(3).active { background-color: #64B5F6; }
.meal-btn:nth-child(4).active { background-color: #BA68C8; }

.meal-btn:focus,
.meal-btn:focus-visible {
  outline: none;
  box-shadow: none;
}


/* --- 모달 스타일 (기존 유지) --- */
.modal-backdrop {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-color: rgba(0,0,0,0.4); /* 조금 더 투명하게 */
  backdrop-filter: blur(4px); /* 배경 블러 효과 추가 */
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
  transition: color 0.2s;
}

.close-btn:hover { color: #495057; }

.modal-body { padding: 0; flex: 1; overflow-y: auto; }

.modal-fade-enter-active, .modal-fade-leave-active { transition: all 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; transform: scale(0.98); }
</style>