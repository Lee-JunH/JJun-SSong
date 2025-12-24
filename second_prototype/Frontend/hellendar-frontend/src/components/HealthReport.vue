<template>
  <div class="report-container">
    <header class="report-header">
      <div>
        <h1 class="page-title">건강 리포트</h1>
        <p class="sub-title">
          <span v-if="titleMonth">{{ titleMonth }} 리포트</span>
          <span v-else>{{ today }} 기준</span>
        </p>
      </div>

      <button class="month-btn" type="button" @click="openMonthPicker">
        다른 달 리포트
      </button>
    </header>

    <div v-if="loading" class="state">불러오는 중...</div>
    <div v-else-if="error" class="state error">{{ error }}</div>

    <template v-else>
      <!-- 1. 요약 섹션 -->
      <section class="summary-section">
        <div class="summary-card weight">
          <span class="label">현재 체중</span>
          <div class="value-group">
            <span class="number">{{ currentWeightText }}</span>
            <span class="unit">kg</span>
          </div>

          <span
            class="change-badge"
            :class="weightDeltaSignClass"
            v-if="weightDeltaText !== '-'"
          >
            {{ weightDeltaText }}kg (지난달 대비)
          </span>
          <span class="change-badge neutral" v-else>지난달 비교 불가</span>
        </div>

        <div class="summary-card bmi">
          <span class="label">현재 BMI</span>
          <div class="value-group">
            <span class="number">{{ currentBMIText }}</span>
            <span class="unit">{{ bmiStatusText }}</span>
          </div>
        </div>

        <div class="summary-card record">
          <span class="label">헬린더에 담은 기록</span>
          <div class="value-group">
            <span class="number">{{ recordedDays }}</span>
            <span class="unit">일 동안의 변화</span>
          </div>
        </div>
      </section>
      
      <!-- 2. 식단 도넛 차트 섹션 -->
      <section class="meal-section">
        <div class="meal-card" v-for="(item, key) in mealStats" :key="key">
          <h4 class="meal-title">{{ item.label }}</h4>
          <div class="doughnut-wrapper">
            <canvas :ref="el => mealChartRefs[key] = el"></canvas>
            
            <div class="center-text">
              <span class="percent">{{ item.percent }}%</span>
              
              <span class="status">
                {{ item.count > 0 ? `${item.count}/${daysInMonth}` : '기록 없음' }}
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- 구분선 및 나트륨/당 섹션 -->
      <div class="w-full">
        <hr class="my-8 border-gray-200" />

        <section class="nutrient-section">
          <h2 class="section-title">
            <span class="bar-point"></span>
            나트륨/당 섭취 분석
          </h2>
          
          <div class="nutrient-summary-grid">
            <div class="nutrient-summary-card sodium-warning">
              <p class="label">나트륨 주의(초과)</p>
              <p class="value sodium-text">{{ sodiumExceedCount }}일</p>
            </div>
            <div class="nutrient-summary-card sugar-warning">
              <p class="label">당류 주의(초과)</p>
              <p class="value sugar-text">{{ sugarExceedCount }}일</p>
            </div>
          </div>

          <div class="chart-card nutrient-chart-card">
            <div class="card-header">
              <h3 class="font-semibold text-gray-700">🧂 나트륨 섭취 추이</h3>
              <span class="description">권장: {{ recommendedSodium }}mg 미만</span>
            </div>
            <div class="canvas-wrapper h-64">
              <canvas ref="sodiumChartRef"></canvas>
            </div>
            <p class="chart-info-text">* 붉은색 막대는 권장량(2,000mg) 초과일입니다.</p>
          </div>

          <div class="chart-card nutrient-chart-card">
            <div class="card-header">
              <h3 class="font-semibold text-gray-700">🍬 당류 섭취 추이</h3>
              <span class="description">권장: {{ recommendedSugar }}g 미만</span>
            </div>
            <div class="canvas-wrapper h-64">
              <canvas ref="sugarChartRef"></canvas>
            </div>
            <p class="chart-info-text">* 붉은색 막대는 권장량(50g) 초과일입니다.</p>
          </div>

        </section>
      </div>

      <!-- 3. 체중/BMI 라인 차트 섹션 -->
      <section class="charts-section">
        <div class="chart-card">
          <div class="card-header">
            <h3>체중</h3>
            <span class="period">{{ titleMonth || "이번 달" }}</span>
          </div>
          <div class="canvas-wrapper">
            <canvas ref="weightChartRef"></canvas>
          </div>
        </div>

        <div class="chart-card">
          <div class="card-header">
            <h3>BMI</h3>
            <span class="description">신체 질량 지수</span>
          </div>
          <div class="canvas-wrapper">
            <canvas ref="bmiChartRef"></canvas>
          </div>
        </div>

        <div class="chart-card">
          <div class="card-header">
            <h3>기초대사량(BMR)</h3>
            <span class="description">체중 변화에 따른 대사량 추이</span>
          </div>
          <div class="canvas-wrapper">
            <canvas ref="bmrChartRef"></canvas>
          </div>
          <p class="chart-info">
            * Mifflin-St Jeor 공식을 기반으로 추산된 수치입니다.
          </p>
        </div>
      </section>

      <ul class="insights">
        <li>식단 기록과 체중 변화를 한눈에 비교해보세요.</li>
        <li v-if="recordedDays === 0">이번 달은 기록이 없어서 그래프가 비어 있어요.</li>
        <li v-else>꾸준한 기록이 건강 관리의 시작입니다!</li>
      </ul>
    </template>

    <MonthPickerModal
      v-if="monthPickerOpen"
      v-model="selectedMonth"
      :available-months="availableMonths"
      @select="handleMonthSelected"
      @close="monthPickerOpen = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onBeforeUnmount, nextTick } from "vue"
import dayjs from "dayjs"
import Chart from "chart.js/auto"
import http from "@/api/http"
import MonthPickerModal from "@/components/MonthPickerModal.vue"

const today = dayjs().format("YYYY-MM-DD")
const selectedMonth = ref(dayjs().format("YYYY-MM"))
const availableMonths = ref([]) 
const monthPickerOpen = ref(false)

const loading = ref(false)
const error = ref("")

const profile = ref(null) 
const report = ref(null) 

// 권장 섭취량 상수
const RECOMMENDED_SODIUM = 2000;
const RECOMMENDED_SUGAR = 50;

const recommendedSodium = RECOMMENDED_SODIUM.toLocaleString();
const recommendedSugar = RECOMMENDED_SUGAR;


// ✅ 해당 월의 총 날짜 수 (30/31/28/29)
const daysInMonth = computed(() => dayjs(`${selectedMonth.value}-01`).daysInMonth())

// ✅ 캘린더 토글(아침/점심/저녁/영양제) 및 영양 정보 월 데이터
const monthSummaryDays = ref([])

async function fetchMonthSummary(ym) {
  // 백엔드: GET /api/calendar?month=YYYY-MM
  const res = await http.get("/calendar", { params: { month: ym } })
  monthSummaryDays.value = Array.isArray(res.data?.days) ? res.data.days : []
}

// ---- Chart refs (Line Charts) ----
const weightChartRef = ref(null)
const bmiChartRef = ref(null)
const bmrChartRef = ref(null)

// ---- Chart refs (Meal Doughnuts) ----
const mealChartRefs = ref({
  breakfast: null,
  lunch: null,
  dinner: null,
  nutrition: null,
})

// ---- Chart refs (Nutrient Bars) ----
const sodiumChartRef = ref(null)
const sugarChartRef = ref(null)

// 인스턴스 보관
let chartInstances = []

function destroyCharts() {
  chartInstances.forEach(c => c && c.destroy())
  chartInstances = []
}

onBeforeUnmount(() => destroyCharts())

// ---- Data Processing ----

// 1. 월 표시
function monthTitle(ym) {
  if (!ym) return ""
  const y = ym.slice(0, 4)
  const m = String(Number(ym.slice(5, 7)))
  return `${y}년 ${m}월`
}
const titleMonth = computed(() => monthTitle(selectedMonth.value))

// 2. 기록 일수
const recordedDays = computed(() => report.value?.stats?.recorded_days ?? 0)

// 3. 체중 통계
const currentWeight = computed(() => report.value?.stats?.weight?.current ?? null)
const currentWeightText = computed(() => (currentWeight.value == null ? "-" : Number(currentWeight.value).toFixed(1)))
const weightDelta = computed(() => report.value?.stats?.weight?.change_from_prev_month ?? null)
const weightDeltaText = computed(() => {
  if (weightDelta.value == null) return "-"
  const n = Number(weightDelta.value)
  return (n > 0 ? "+" : "") + n.toFixed(1)
})
const weightDeltaSignClass = computed(() => {
  if (weightDelta.value == null) return "neutral"
  return Number(weightDelta.value) >= 0 ? "plus" : "minus"
})

// 4. BMI / BMR 계산
function calculateBMI(weightKg, heightCm) {
  const h = heightCm / 100
  return weightKg / (h * h)
}
function getBMIStatus(bmi) {
  if (bmi < 18.5) return "저체중"
  if (bmi < 23) return "정상"
  if (bmi < 25) return "과체중"
  return "비만"
}
const currentBMI = computed(() => {
  const w = currentWeight.value
  const h = profile.value?.height
  if (w == null || !h) return null
  return calculateBMI(Number(w), Number(h))
})
const currentBMIText = computed(() => (currentBMI.value == null ? "-" : currentBMI.value.toFixed(1)))
const bmiStatusText = computed(() => (currentBMI.value == null ? "-" : getBMIStatus(currentBMI.value)))

function calculateBMR(weightKg) {
  const { height, age, gender } = profile.value || {}
  if (!height || !age || !gender) return null
  const base = (10 * weightKg) + (6.25 * Number(height)) - (5 * Number(age))
  return gender === "male" ? Math.round(base + 5) : Math.round(base - 161)
}

// 5. 식단 데이터 통계 계산
const mealStats = computed(() => {
  const denom = daysInMonth.value || 1

  const stats = {
    breakfast: { label: "아침", count: 0, percent: 0 },
    lunch:     { label: "점심", count: 0, percent: 0 },
    dinner:    { label: "저녁", count: 0, percent: 0 },
    nutrition: { label: "영양제", count: 0, percent: 0 },
  }

  for (const d of (monthSummaryDays.value || [])) {
    if (d.breakfast) stats.breakfast.count++
    if (d.lunch)     stats.lunch.count++
    if (d.dinner)    stats.dinner.count++
    if (d.nutrition) stats.nutrition.count++
  }

  for (const key of Object.keys(stats)) {
    stats[key].percent = Math.round((stats[key].count / denom) * 100)
  }

  return stats
})

// 6. 나트륨/당 초과 일수 계산
const sodiumExceedCount = computed(() => {
  return (monthSummaryDays.value || []).filter(d => (d.total_sodium || 0) > RECOMMENDED_SODIUM).length
})

const sugarExceedCount = computed(() => {
  return (monthSummaryDays.value || []).filter(d => (d.total_sugar || 0) > RECOMMENDED_SUGAR).length
})


// ---- API Call ----
async function fetchProfile() {
  const res = await http.get("/profile/me/")
  profile.value = res.data
}

async function fetchAvailableMonths() {
  try {
    const res = await http.get("/reports/available-months/")
    availableMonths.value = Array.isArray(res.data) ? res.data : (res.data?.months || [])
    if (availableMonths.value.length > 0 && !availableMonths.value.includes(selectedMonth.value)) {
      selectedMonth.value = availableMonths.value[availableMonths.value.length - 1]
    }
  } catch (e) {
    console.warn("월 목록 로드 실패", e)
  }
}

async function fetchMonthlyReport(ym) {
  const res = await http.get("/reports/monthly/", { params: { month: ym } })
  report.value = res.data
}

// ---- Chart Creation Functions ----

// 1. Line Chart (기존)
function createLineChart(canvasEl, label, labels, data, color, yMin = null) {
  const ctx = canvasEl.getContext("2d")
  if (!ctx) return null;
  const gradient = ctx.createLinearGradient(0, 0, 0, 400)
  gradient.addColorStop(0, `${color}50`)
  gradient.addColorStop(1, `${color}00`)

  return new Chart(canvasEl, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label, data, borderColor: color, backgroundColor: gradient,
        borderWidth: 3, pointBackgroundColor: "#fff", pointBorderColor: color,
        pointBorderWidth: 2, pointRadius: 4, pointHoverRadius: 6,
        fill: true, tension: 0.4, spanGaps: true,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: { backgroundColor: "#333", displayColors: false } },
      scales: {
        y: { beginAtZero: false, min: yMin, grid: { color: "#f0f0f0", borderDash: [5, 5] } },
        x: { grid: { display: false } }
      }
    }
  })
}

// 2. Doughnut Chart (식단)
function createDoughnutChart(canvasEl, percent, color) {
  const ctx = canvasEl.getContext("2d")
  if (!ctx) return null

  return new Chart(canvasEl, {
    type: "doughnut",
    data: {
      labels: ["섭취", "미섭취"],
      datasets: [{
        data: [percent, 100 - percent],
        backgroundColor: [color, "#f1f5f9"], 
        borderWidth: 0,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "75%",
      plugins: {
        legend: { display: false },
        tooltip: { enabled: false }
      },
      animation: { animateScale: true, animateRotate: true }
    }
  })
}

// 3. Bar Chart (나트륨/당)
function createBarChart(canvasEl, label, labels, data, threshold, baseColor, warnColor) {
  const ctx = canvasEl.getContext("2d")
  if (!ctx) return null

  // 값에 따라 색상 결정
  const backgroundColors = data.map(val => (val > threshold ? warnColor : baseColor));

  return new Chart(canvasEl, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: label,
        data: data,
        backgroundColor: backgroundColors,
        borderRadius: 4,
        barPercentage: 0.6,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#333",
          displayColors: false,
          callbacks: {
            label: (ctx) => `${ctx.raw} ${label.includes('나트륨') ? 'mg' : 'g'}`
          }
        },
        annotation: { // 기준선 (Chart.js annotation plugin 필요, 없으면 무시됨)
           annotations: {
             line1: {
               type: 'line',
               yMin: threshold,
               yMax: threshold,
               borderColor: '#94a3b8',
               borderWidth: 1,
               borderDash: [4, 4],
             }
           }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: "#f0f0f0" },
          ticks: { font: { size: 10 } }
        },
        x: {
          grid: { display: false },
          ticks: { font: { size: 10 } }
        }
      }
    }
  })
}


async function renderCharts() {
  await nextTick()
  destroyCharts() 

  if (!report.value) return

  // 1. 식단 도넛 차트
  const colors = { breakfast: "#f59e0b", lunch: "#10b981", dinner: "#3b82f6", supplement: "#8b5cf6" }
  Object.keys(mealStats.value).forEach((key) => {
    const el = mealChartRefs.value[key]
    const stat = mealStats.value[key]
    if (el) {
      chartInstances.push(createDoughnutChart(el, stat.percent, colors[key] || "#db1f4b"))
    }
  })

  // [수정] 월 전체 일수(1~N일) 기준 라벨 및 데이터 생성
  const totalDays = daysInMonth.value
  const fullLabels = Array.from({ length: totalDays }, (_, i) => String(i + 1))

  // 2. 나트륨/당 바 차트 데이터 매핑
  const summaryDays = monthSummaryDays.value || []
  
  // 날짜별 데이터 Map 생성 (빠른 조회용, key: "일")
  const summaryMap = new Map()
  summaryDays.forEach(d => summaryMap.set(dayjs(d.date).format("D"), d))

  // 1일부터 말일까지 순회하며 데이터 채우기 (기록 없으면 0)
  const sodiumValues = fullLabels.map(dayStr => {
    const d = summaryMap.get(dayStr)
    return d ? (d.total_sodium || 0) : 0
  })
  const sugarValues = fullLabels.map(dayStr => {
    const d = summaryMap.get(dayStr)
    return d ? (d.total_sugar || 0) : 0
  })

  if (sodiumChartRef.value) {
    chartInstances.push(createBarChart(
      sodiumChartRef.value, "나트륨", fullLabels, sodiumValues, 
      RECOMMENDED_SODIUM, "#cbd5e1", "#db1f4b"
    ))
  }
  if (sugarChartRef.value) {
    chartInstances.push(createBarChart(
      sugarChartRef.value, "당류", fullLabels, sugarValues, 
      RECOMMENDED_SUGAR, "#cbd5e1", "#f97316"
    ))
  }

  // 3. 체중/BMI 라인 차트 데이터 매핑
  const reportDays = report.value.days || []
  const reportMap = new Map()
  reportDays.forEach(d => reportMap.set(dayjs(d.date).format("D"), d))

  const weights = fullLabels.map(dayStr => {
    const d = reportMap.get(dayStr)
    return (d && d.weight_kg != null) ? Number(d.weight_kg) : null
  })

  const h = profile.value?.height
  const bmis = fullLabels.map(dayStr => {
    const d = reportMap.get(dayStr)
    if (!d || d.weight_kg == null || !h) return null
    return Number(calculateBMI(Number(d.weight_kg), Number(h)).toFixed(1))
  })
  const bmrs = fullLabels.map(dayStr => {
    const d = reportMap.get(dayStr)
    if (!d || d.weight_kg == null) return null
    const v = calculateBMR(Number(d.weight_kg))
    return v == null ? null : v
  })

  const wMin = weights.filter(v => v != null)
  const wYMin = wMin.length ? Math.min(...wMin) - 2 : null

  if (weightChartRef.value) chartInstances.push(createLineChart(weightChartRef.value, "체중(kg)", fullLabels, weights, "#14b8a6", wYMin))
  if (bmiChartRef.value) chartInstances.push(createLineChart(bmiChartRef.value, "BMI", fullLabels, bmis, "#8b5cf6", 15))
  if (bmrChartRef.value) chartInstances.push(createLineChart(bmrChartRef.value, "BMR(kcal)", fullLabels, bmrs, "#f97316", null))
}

watch(
  [loading, report, profile, monthSummaryDays],
  async ([newLoading, newReport, newProfile]) => {
    if (!newLoading && newReport && newProfile) {
      await nextTick()
      renderCharts()
    }
  },
  { deep: true }
)


// ---- Interaction ----
function openMonthPicker() { monthPickerOpen.value = true }
async function handleMonthSelected(ym) { await loadAll(ym) }

async function loadAll(ym = selectedMonth.value) {
  loading.value = true
  error.value = ""
  destroyCharts()

  try {
    if (!profile.value) await fetchProfile()
    await fetchAvailableMonths()
    await fetchMonthlyReport(ym)
    await fetchMonthSummary(ym)
  } catch (e) {
    console.error(e)
    const status = e?.response?.status
    if (status === 401) error.value = "로그인이 필요합니다."
    else error.value = "리포트를 불러오는 중 오류가 발생했습니다."
  } finally {
    loading.value = false
  }
}

onMounted(() => { loadAll() })
</script>

<style scoped>
/* 기존 스타일 유지 */
.report-container {
  font-family: 'AritaDotumKR', sans-serif;
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.report-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding: 0 10px;
}
.page-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
}
.sub-title {
  margin: 6px 0 0;
  color: #64748b;
  font-size: .9rem;
}
.month-btn {
  border: 1px solid #e5e7eb;
  background: #fff;
  border-radius: 999px;
  padding: 10px 14px;
  font-weight: 700;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}
.month-btn:hover {
  border-color: #db1f4b;
  color: #db1f4b;
  background: #fff0f3;
}
.state { padding: 18px; color: #64748b; }
.state.error { color: #b91c1c; }

/* 요약 섹션 */
.summary-section {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}
.summary-card {
  background: #fff;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,.05);
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.summary-card.weight .value-group .number { color: #14b8a6; }
.summary-card.bmi .value-group .number { color: #8b5cf6; }
.summary-card.record .value-group .number { color: #db1f4b; }
.label { font-size: .9rem; color: #64748b; }
.value-group { display: flex; align-items: baseline; gap: 6px; }
.value-group .number { font-size: 1.8rem; font-weight: 800; }
.value-group .unit { font-size: .9rem; color: #94a3b8; font-weight: 700; }
.change-badge { font-size: .75rem; padding: 4px 8px; border-radius: 12px; width: fit-content; }
.change-badge.minus { background: #ecfdf5; color: #059669; }
.change-badge.plus { background: #fef2f2; color: #dc2626; }
.change-badge.neutral { background: #f3f4f6; color: #6b7280; }

/* 식단(도넛 차트) 섹션 */
.meal-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.meal-card {
  background: #fff;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,.05);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}
.meal-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: #334155;
}
.doughnut-wrapper {
  position: relative;
  width: 120px;
  height: 120px;
}
.center-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  pointer-events: none;
}
.center-text .percent {
  font-size: 1.2rem;
  font-weight: 800;
  color: #334155;
  line-height: 1;
}
.center-text .status {
  font-size: 0.7rem;
  color: #94a3b8;
  margin-top: 2px;
}

/* --- [NEW] 나트륨/당 섹션 스타일 --- */
.nutrient-section {
  /* Tailwind 대체 스타일 */
  margin-bottom: 20px;
}
.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
}
.bar-point {
  width: 8px;
  height: 24px;
  background-color: #db1f4b;
  border-radius: 999px;
  margin-right: 8px;
}

/* 나트륨/당 요약 카드 그리드 */
.nutrient-summary-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 24px;
}
.nutrient-summary-card {
  padding: 16px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}
.nutrient-summary-card.sodium-warning {
  background-color: #fef2f2; /* red-50 */
  border: 1px solid #fee2e2; /* red-100 */
}
.nutrient-summary-card.sugar-warning {
  background-color: #fff7ed; /* orange-50 */
  border: 1px solid #ffedd5; /* orange-100 */
}
.nutrient-summary-card .label {
  font-size: 0.75rem;
  color: #6b7280;
  margin-bottom: 4px;
}
.nutrient-summary-card .value {
  font-size: 1.5rem;
  font-weight: 700;
}
.sodium-text { color: #db1f4b; }
.sugar-text { color: #f97316; }

/* 나트륨/당 차트 카드 */
.nutrient-chart-card {
  margin-bottom: 24px;
}
.chart-info-text {
  text-align: center;
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: 8px;
}


/* 차트 카드 공통 */
.charts-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.chart-card {
  background: #fff;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 10px 15px -3px rgba(0,0,0,.05);
  transition: transform .2s;
}
.chart-card:hover { transform: translateY(-2px); }
.card-header {
  margin-bottom: 18px;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}
.card-header h3 { margin: 0; font-size: 1.1rem; font-weight: 700; color: #334155; }
.card-header .period, .card-header .description { font-size: .8rem; color: #94a3b8; }
.canvas-wrapper { position: relative; height: 200px; width: 100%; }
.chart-info { margin-top: 12px; font-size: .75rem; color: #cbd5e1; text-align: right; }
.insights { margin: 8px 0 0; padding: 0 18px; color: #475569; font-size: 14px; line-height: 1.6; }

/* 모바일 대응 */
@media (max-width: 860px) {
  .summary-section { grid-template-columns: 1fr; }
  .meal-section { grid-template-columns: 1fr 1fr; } 
  .nutrient-summary-grid { grid-template-columns: 1fr 1fr; }
}
</style>