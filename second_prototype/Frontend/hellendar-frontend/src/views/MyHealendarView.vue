<template>
  <div class="page">
    <!-- 1. 달력 영역 (이제 전체 너비 사용) -->
    <div class="calendar-container">
      <MonthCalendar
        :month="month"
        :summaries="cal.days"
        :loading="cal.loading"
        :error="cal.error"
        :selectedDate="selectedDate"
        @changeMonth="onChangeMonth"
        @select="onSelect"
      />
    </div>

    <!-- 2. 식단 입력 모달 -->
    <Transition name="modal-fade">
      <div v-if="isModalOpen" class="modal-backdrop" @click.self="closeModal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>{{ selectedDate }} 식단 관리</h3>
            <button class="close-btn" @click="closeModal">&times;</button>
          </div>
          
          <div class="modal-body">
            <!-- 기존의 상세 패널을 모달 안으로 이동 -->
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
const selectedDate = ref(dayjs().format("YYYY-MM-DD"))

// 모달 상태 관리 변수
const isModalOpen = ref(false)

onMounted(async () => {
  await cal.fetchMonth(month.value)
})

async function onChangeMonth(m) {
  month.value = m
  await cal.fetchMonth(m)
  // 월 변경 시에는 모달을 띄우지 않고, 날짜 데이터만 1일로 초기화 (필요시)
  // selectedDate.value = `${m}-01` 
}

// 날짜 선택 시 모달 열기
function onSelect(d) {
  selectedDate.value = d
  isModalOpen.value = true
}

// 모달 닫기
function closeModal() {
  isModalOpen.value = false
}
</script>

<style scoped>
.page {
  /* 기존 grid 제거하고 전체 레이아웃 잡기 */
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.calendar-container {
  width: 100%;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

/* --- 모달 스타일 --- */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 반투명 배경 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  width: 90%;
  max-width: 800px; /* 모달 최대 너비 증가 (500px -> 800px) */
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 90vh; /* 화면 높이보다 크면 스크롤 */
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
  overflow-y: auto; /* 내용이 길면 스크롤 */
}

/* --- 모달 애니메이션 (Transition) --- */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>