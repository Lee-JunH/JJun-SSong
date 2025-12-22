<template>
  <div class="month-calendar">
    <!-- 헤더 -->
    <div class="calendar-header">
      <!-- 이전 달 (< 모양 아이콘) -->
      <button class="nav-btn" @click="moveMonth(-1)" aria-label="이전 달">
        <img class="nav-icon" :src="chevronLeft" alt="" aria-hidden="true" />
      </button>

      
      <h2>{{ dayjs(month).format('YYYY년 M월') }}</h2>
      
      <!-- 다음 달 (> 모양 아이콘) -->
      <button class="nav-btn" @click="moveMonth(1)" aria-label="다음 달">
        <img class="nav-icon" :src="chevronRight" alt="" aria-hidden="true" />
      </button>

    </div>

    <div class="calendar-grid-container">
      <!-- 요일 헤더 -->
      <div class="weekdays">
        <div v-for="(day, index) in ['일', '월', '화', '수', '목', '금', '토']" 
             :key="day" 
             class="weekday"
             :class="{ 'sunday': index === 0, 'saturday': index === 6 }"
        >
          {{ day }}
        </div>
      </div>

      <!-- 날짜 그리드 -->
      <div class="days-grid">
        <div v-for="n in startWeekday" :key="'empty-'+n" class="day empty"></div>

        <div 
          v-for="date in daysInMonth" 
          :key="date"
          class="day"
          :class="{ 
            'selected': date === selectedDate,
            'today': date === today,
            'sunday': dayjs(date).day() === 0
          }"
          @click="$emit('select', date)"
        >
          <div class="day-header">
            <span class="day-number">{{ dayjs(date).format('D') }}</span>
            <span v-if="date === today" class="today-badge">오늘</span>
          </div>
          
          <div class="cell-content">
            <slot name="date-cell" :date="date" :data="summaries[date] || {}"></slot>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import dayjs from 'dayjs'
import chevronRight from "@/assets/icons/chevron_right.png"
import chevronLeft from "@/assets/icons/chevron_left.png"


const props = defineProps({
  month: String, 
  summaries: { type: Object, default: () => ({}) },
  selectedDate: String,
  loading: Boolean,
  error: { type: String, default: "" }
})

const emit = defineEmits(['changeMonth', 'select'])

const today = dayjs().format('YYYY-MM-DD')

const startWeekday = computed(() => {
  return dayjs(props.month + '-01').day()
})

const daysInMonth = computed(() => {
  const start = dayjs(props.month + '-01')
  const days = start.daysInMonth()
  const result = []
  for(let i=1; i<=days; i++) {
    result.push(start.date(i).format('YYYY-MM-DD'))
  }
  return result
})

function moveMonth(delta) {
  const newMonth = dayjs(props.month).add(delta, 'month').format('YYYY-MM')
  emit('changeMonth', newMonth)
}
</script>

<style scoped>
.month-calendar {
  width: 100%;
}

/* --- 헤더 --- */
.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 0 10px;
}

.calendar-header h2 {
  font-size: 1.5rem;
  font-weight: 800;
  color: #343a40;
  margin: 0;
}

/* 네비게이션 버튼 스타일 (원형 아이콘) */
/* 네비게이션 버튼 스타일 (원형) */
.nav-btn {

  border-radius: 999px;
  width: 36px;
  height: 36px;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 0;       /* ✅ 전역 button padding 무력화 */
  line-height: 0;   /* ✅ 아이콘 수직 정렬 안정 */
  cursor: pointer;

}

.nav-icon {
  width: 40px;

  object-fit: contain;
  display: block;
}


.nav-btn:hover {
  background: #f8f9fa;
  border-color: #ced4da;
  color: #212529;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.08);
}

.nav-btn:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

/* --- 그리드 레이아웃 --- */
.calendar-grid-container {
  border-top: 1px solid #dee2e6;
  border-left: 1px solid #dee2e6;
}

/* 요일 헤더 */
.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  background: #f8f9fa;
}

.weekday {
  text-align: center;
  font-size: 0.9rem;
  font-weight: 600;
  color: #495057;
  padding: 10px 0;
  border-right: 1px solid #dee2e6;
  border-bottom: 1px solid #dee2e6;
  background: #f8f9fa;
}
.weekday.sunday { color: #ff6b6b; }
.weekday.saturday { color: #4dabf7; }

/* 날짜 그리드 */
.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0;
}

.day {
  background: white;
  aspect-ratio: 1 / 1; /* 1:1 비율 유지 */
  padding: 8px;
  cursor: pointer;
  position: relative;
  display: flex;
  flex-direction: column;
  transition: background-color 0.2s;
  
  /* 테두리 설정: 컨테이너의 Top/Left와 합쳐져 완전한 격자 형성 */
  border-right: 1px solid #dee2e6;
  border-bottom: 1px solid #dee2e6;
}

.day:hover {
  background-color: #f8f9fa;
  z-index: 1;
}

/* 선택된 날짜 스타일 */
.day.selected {
  background-color: #e9ffec;
  box-shadow: inset 0 0 0 2px #35da43; /* 내부 테두리로 강조하여 격자선 유지 */
}

.day.sunday .day-number { color: #ff6b6b; }

/* 날짜 숫자 헤더 */
.day-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 4px; /* 간격 줄임 */
}

.day-number {
  font-size: 0.95rem;
  font-weight: 500;
  color: #495057;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.day.today .day-number {
  background: #0a750a;
  color: rgb(255, 255, 255);
  font-weight: 700;
}

.today-badge {
  font-size: 10px;
  font-weight: bold;
  color: #49a741;
  background: rgba(61, 121, 94, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
}

/* [수정] 내용물을 중앙에 배치 */
.cell-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center; /* 수직 중앙 정렬 */
  align-items: center;     /* 수평 중앙 정렬 */
  width: 100%;
  overflow: hidden;
}

.empty {
  background: #fdfdfd;
  cursor: default;
}
</style>