<template>
  <div class="report-container">
    <!-- 헤더 영역 -->
    <header class="report-header">
      <h1 class="page-title">건강 리포트</h1>
      <span class="report-date">{{ today }} 기준</span>
    </header>

    <div class="content-wrapper">
      <!-- 요약 정보 카드 (현재 상태) -->
      <section class="summary-section">
        <div class="summary-card weight">
          <span class="label">현재 체중</span>
          <div class="value-group">
            <span class="number">{{ currentWeight }}</span>
            <span class="unit">kg</span>
          </div>
          <span class="change-badge" :class="weightChange >= 0 ? 'plus' : 'minus'">
            {{ weightChange > 0 ? '+' : '' }}{{ weightChange }}kg (지난달 대비)
          </span>
        </div>

        <div class="summary-card bmi">
          <span class="label">현재 BMI</span>
          <div class="value-group">
            <span class="number">{{ currentBMI }}</span>
            <span class="unit">{{ getBMIStatus(currentBMI) }}</span>
          </div>
        </div>
      </section>

      <!-- 그래프 섹션 -->
      <section class="charts-section">
        <!-- 1. 체중 변화 그래프 -->
        <div class="chart-card">
          <div class="card-header">
            <h3>체중 변화</h3>
            <span class="period">최근 6개월</span>
          </div>
          <div class="canvas-wrapper">
            <canvas ref="weightChartRef"></canvas>
          </div>
        </div>

        <!-- 2. BMI 변화 그래프 -->
        <div class="chart-card">
          <div class="card-header">
            <h3>BMI 추이</h3>
            <span class="description">신체 질량 지수</span>
          </div>
          <div class="canvas-wrapper">
            <canvas ref="bmiChartRef"></canvas>
          </div>
        </div>

        <!-- 3. 기초대사량(BMR) 변화 그래프 -->
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
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import dayjs from 'dayjs';
import Chart from 'chart.js/auto';

const today = dayjs().format("YYYY-MM-DD");

// --- 가상 데이터 (실제 앱에서는 Props나 Pinia/Vuex Store에서 가져와야 함) ---
const userProfile = {
  height: 175, // cm
  age: 28,
  gender: 'male', // 'male' or 'female'
};

// 최근 6개월 데이터 예시
const historyData = [
  { date: '2023-07', weight: 78.5 },
  { date: '2023-08', weight: 77.2 },
  { date: '2023-09', weight: 76.0 },
  { date: '2023-10', weight: 75.5 },
  { date: '2023-11', weight: 74.8 },
  { date: '2023-12', weight: 73.5 },
];

// --- 상태 관리 ---
const weightChartRef = ref(null);
const bmiChartRef = ref(null);
const bmrChartRef = ref(null);

// --- 계산 로직 ---
const currentWeight = computed(() => historyData[historyData.length - 1].weight);
const prevWeight = computed(() => historyData[historyData.length - 2].weight);
const weightChange = computed(() => (currentWeight.value - prevWeight.value).toFixed(1));

// BMI 계산: 체중(kg) / (키(m) * 키(m))
const calculateBMI = (weight, heightCm) => {
  const heightM = heightCm / 100;
  return (weight / (heightM * heightM)).toFixed(1);
};

const currentBMI = computed(() => calculateBMI(currentWeight.value, userProfile.height));

const getBMIStatus = (bmi) => {
  if (bmi < 18.5) return '저체중';
  if (bmi < 23) return '정상';
  if (bmi < 25) return '과체중';
  return '비만';
};

// 기초대사량(BMR) 계산 (Mifflin-St Jeor 공식)
const calculateBMR = (weight) => {
  const { height, age, gender } = userProfile;
  let base = (10 * weight) + (6.25 * height) - (5 * age);
  return gender === 'male' ? Math.round(base + 5) : Math.round(base - 161);
};

// --- 차트 렌더링 함수 ---
const createChart = (ctx, label, data, color, yAxisMin = null) => {
  // 그라디언트 생성
  const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 400);
  gradient.addColorStop(0, `${color}50`); // 투명도 50%
  gradient.addColorStop(1, `${color}00`); // 투명도 0%

  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: historyData.map(d => d.date),
      datasets: [{
        label: label,
        data: data,
        borderColor: color,
        backgroundColor: gradient,
        borderWidth: 3,
        pointBackgroundColor: '#fff',
        pointBorderColor: color,
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
        fill: true,
        tension: 0.4 // 부드러운 곡선
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#333',
          titleFont: { family: 'AritaDotumKR' },
          bodyFont: { family: 'AritaDotumKR' },
          padding: 10,
          cornerRadius: 8,
          displayColors: false,
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          min: yAxisMin,
          grid: {
            color: '#f0f0f0',
            borderDash: [5, 5]
          },
          ticks: { font: { family: 'AritaDotumKR' } }
        },
        x: {
          grid: { display: false },
          ticks: { font: { family: 'AritaDotumKR' } }
        }
      }
    }
  });
};

onMounted(() => {
  // 데이터 가공
  const weights = historyData.map(d => d.weight);
  const bmis = historyData.map(d => calculateBMI(d.weight, userProfile.height));
  const bmrs = historyData.map(d => calculateBMR(d.weight));

  // 1. 체중 차트 (Teal 컬러)
  if (weightChartRef.value) {
    createChart(weightChartRef.value, '체중(kg)', weights, '#14b8a6', Math.min(...weights) - 2);
  }

  // 2. BMI 차트 (Purple 컬러)
  if (bmiChartRef.value) {
    createChart(bmiChartRef.value, 'BMI', bmis, '#8b5cf6', 15);
  }

  // 3. BMR 차트 (Orange 컬러)
  if (bmrChartRef.value) {
    createChart(bmrChartRef.value, 'BMR(kcal)', bmrs, '#f97316');
  }
});
</script>

<style scoped>
/* 폰트 선언은 App.vue에서 전역으로 하거나 여기서 따로 해도 됨 */
.report-container {
  font-family: 'AritaDotumKR', sans-serif;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 헤더 스타일 */
.report-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  padding: 0 10px;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.report-date {
  color: #64748b;
  font-size: 0.9rem;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 요약 섹션 스타일 */
.summary-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.summary-card {
  background: white;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.summary-card.weight .value-group .number { color: #14b8a6; }
.summary-card.bmi .value-group .number { color: #8b5cf6; }

.label {
  font-size: 0.9rem;
  color: #64748b;
}

.value-group {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.value-group .number {
  font-size: 1.8rem;
  font-weight: 700;
}

.value-group .unit {
  font-size: 0.9rem;
  color: #94a3b8;
}

.change-badge {
  font-size: 0.75rem;
  padding: 4px 8px;
  border-radius: 12px;
  width: fit-content;
}

.change-badge.minus {
  background-color: #ecfdf5;
  color: #059669;
}
.change-badge.plus {
  background-color: #fef2f2;
  color: #dc2626;
}

/* 차트 카드 스타일 */
.chart-card {
  background: white;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
}

.chart-card:hover {
  transform: translateY(-2px);
}

.card-header {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.card-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #334155;
}

.card-header .period, .card-header .description {
  font-size: 0.8rem;
  color: #94a3b8;
}

.canvas-wrapper {
  position: relative;
  height: 200px;
  width: 100%;
}

.chart-info {
  margin-top: 12px;
  font-size: 0.75rem;
  color: #cbd5e1;
  text-align: right;
}
</style>