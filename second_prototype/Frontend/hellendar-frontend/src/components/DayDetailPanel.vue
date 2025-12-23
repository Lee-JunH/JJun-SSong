<template>
  <!-- ✅ 부모 모달 내부에 들어갈 “내용”만 -->
  <div class="meal-content">
    <!-- 헤더(부모 모달에 헤더가 이미 있으면 이 블록 삭제해도 됨) -->


    <!-- 로딩/에러 -->
    <div v-if="loading" class="state-box loading">
      <span class="spinner"></span>
      데이터 불러오는 중...
    </div>
    <div v-else-if="error" class="state-box error">
      {{ error }}
    </div>

    <!-- 본문 -->
    <template v-else>
      <!-- 1) 영양 대시보드 -->
      <div class="dashboard-grid">
        <div class="nutri-card total-card">
          <div class="card-label">총 섭취 칼로리</div>
          <div class="card-value main">
            {{ Number(detailSafe.total_kcal).toFixed(0) }}
            <span class="unit">kcal</span>
          </div>

          <div class="progress-bar-bg" aria-hidden="true">
            <div
              class="progress-bar-fill"
              :style="{ width: progressWidth }"
            ></div>
          </div>
        </div>

        <div class="sub-stats">
          <div class="nutri-item">
            <span class="n-label">탄수화물</span>
            <span class="n-val">{{ Number(detailSafe.total_carb).toFixed(1) }}g</span>
          </div>
          <div class="nutri-item">
            <span class="n-label">단백질</span>
            <span class="n-val">{{ Number(detailSafe.total_protein).toFixed(1) }}g</span>
          </div>
          <div class="nutri-item">
            <span class="n-label">지방</span>
            <span class="n-val">{{ Number(detailSafe.total_fat).toFixed(1) }}g</span>
          </div>
        </div>
      </div>

      <!-- 2) 컨디션/체중 -->
      <div class="daily-check-row">
        <div class="check-item">
          <select v-model="condEmoji" class="clean-select" aria-label="컨디션 선택">
            <option value="">기분 선택</option>
            <option value="😊">😊 좋음</option>
            <option value="🙂">🙂 보통</option>
            <option value="😣">😣 나쁨</option>
          </select>
          <div class="v-divider"></div>
          <input
            v-model="condNote"
            placeholder="오늘의 한줄 메모"
            class="clean-input grow"
            aria-label="컨디션 메모"
          />
          <button class="icon-btn" type="button" @click="saveCondition" title="저장" aria-label="컨디션 저장">💾</button>
        </div>

        <div class="check-item weight-item">
          <span class="check-icon">⚖️ 몸무게</span>
          <input
            v-model.number="weight"
            type="number"
            step="0.1"
            placeholder="0.0"
            class="clean-input weight-input"
            aria-label="몸무게 입력"
          />
          <span class="unit-text">kg</span>
          <button class="icon-btn" type="button" @click="saveWeight" title="저장" aria-label="몸무게 저장">💾</button>
        </div>
      </div>

      <!-- 3) 식단 추가 -->
      <div class="add-meal-card">
        <div class="card-header">
          <span class="title-text">🍽️ 식단 추가</span>
        </div>

        <!-- 검색 -->
        <div class="search-wrapper">
          <input
            v-model="searchQuery"
            @keyup.enter="performSearch"
            placeholder="음식을 검색해보세요 (예: 닭가슴살, 사과)"
            class="search-input"
            aria-label="음식 검색"
          />
          <button class="search-icon-btn" type="button" @click="performSearch" aria-label="검색">🔍</button>

          <transition name="fade">
            <ul v-if="searchResults.length > 0" class="search-dropdown" role="listbox">
              <li
                v-for="item in searchResults"
                :key="item.id"
                @mousedown.prevent
                @click="selectFoodItem(item)"
                role="option"
              >
                <div class="res-info-main">{{ item.name }}</div>
                <div class="res-info-sub">{{ item.kcal }}kcal / 100g</div>
              </li>
            </ul>
          </transition>
        </div>

        <!-- 입력 -->
        <div class="input-area">
          <div class="row-top">
            <select v-model="mealType" class="styled-select" aria-label="식사 구분">
              <option value="breakfast">☀️ 아침</option>
              <option value="lunch">⛅ 점심</option>
              <option value="dinner">🌙 저녁</option>
            </select>

            <div v-if="selectedFood" class="food-pill">
              <span class="food-pill-text">{{ selectedFood.name }}</span>
              <button type="button" @click="resetSelection" class="pill-close" aria-label="선택 해제">×</button>
            </div>

            <input
              v-else
              v-model="foodName"
              placeholder="음식명 직접 입력"
              class="styled-input grow"
              aria-label="음식명 입력"
            />
          </div>

          <div class="nutrient-capsules">
            <div class="capsule main">
              <label>양(g)</label>
              <input v-model.number="grams" type="number" min="0" placeholder="0" aria-label="그램" />
            </div>

            <div class="capsule">
              <label>총 칼로리(Kcal)</label>
              <input v-model.number="kcal" type="number" min="0" placeholder="0" aria-label="칼로리" />
            </div>

            <div class="capsule">
              <label>탄수화물(g)</label>
              <input v-model.number="carb" type="number" min="0" step="0.1" placeholder="0" aria-label="탄수화물" />
            </div>

            <div class="capsule">
              <label>단백질(g)</label>
              <input v-model.number="protein" type="number" min="0" step="0.1" placeholder="0" aria-label="단백질" />
            </div>

            <div class="capsule">
              <label>지방(g)</label>
              <input v-model.number="fat" type="number" min="0" step="0.1" placeholder="0" aria-label="지방" />
            </div>

            <button class="add-btn-gradient" type="button" @click="addMeal">
              추가
            </button>
          </div>
        </div>
      </div>

      <!-- 4) 리스트 -->
      <div class="timeline-container">
        <div v-if="!detailSafe.meals?.length" class="empty-state">
          <div class="empty-icon">🥣</div>
          <p>오늘 먹은 음식을 기록해주세요.</p>
        </div>

        <div v-else class="meal-list">
          <template v-for="type in ['breakfast', 'lunch', 'dinner']" :key="type">
            <div v-if="getMeals(type).length > 0" class="timeline-group">
              <div class="time-label">
                <span class="badge" :class="type">{{ mealLabel(type) }}</span>
                <span class="total-kcal">{{ getGroupCalories(type) }} kcal</span>
              </div>

              <div class="meal-cards">
                <div v-for="m in getMeals(type)" :key="m.id" class="meal-card-item">
                  <div class="mc-content">
                    <div class="mc-name">
                      {{ m.name }} <span class="mc-gram">{{ m.grams }}g</span>
                    </div>
                    <div class="mc-nutri">
                      {{ Number(m.kcal || 0).toFixed(0) }} kcal · 탄 {{ m.carb }}g · 단 {{ m.protein }}g · 지 {{ m.fat }}g
                    </div>
                  </div>
                  <button class="mc-delete" type="button" @click="delMeal(m.id)" aria-label="삭제">🗑️</button>
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue"
import { useDayStore } from "@/stores/day"

const props = defineProps({
  date: { type: String, required: true },
})
const emit = defineEmits(["close"])

const day = useDayStore()
const detail = computed(() => day.detail)
const loading = computed(() => day.loading)
const error = computed(() => day.error)

/** ✅ detail이 null이어도 템플릿이 안전하도록 */
const detailSafe = computed(() => {
  return (
    detail.value ?? {
      total_kcal: 0,
      total_carb: 0,
      total_protein: 0,
      total_fat: 0,
      meals: [],
      condition: { emoji: "", note: "" },
      weight: { weight_kg: null },
    }
  )
})

const progressWidth = computed(() => {
  const kcal = Number(detailSafe.value.total_kcal || 0)
  const pct = Math.min((kcal / 2500) * 100, 100)
  return `${pct}%`
})

// 날짜 분리
const dateParts = computed(() => {
  if (!props.date) return { y: "", m: "", d: "" }
  const [y, m, d] = props.date.split("-")
  return { y, m, d }
})

// 상태
const condEmoji = ref("")
const condNote = ref("")
const weight = ref(null)

const mealType = ref("breakfast")
const foodName = ref("")
const grams = ref(null)
const kcal = ref(null)
const carb = ref(null)
const protein = ref(null)
const fat = ref(null)

// 검색
const searchQuery = ref("")
const searchResults = ref([])
const selectedFood = ref(null)

// Mock DB (100g 기준)
const mockFoodDB = [
  { id: 1, name: "현미밥", kcal: 150, carb: 32, protein: 3, fat: 1 },
  { id: 2, name: "닭가슴살 (삶은것)", kcal: 109, carb: 0, protein: 23, fat: 1.2 },
  { id: 3, name: "고구마 (찐것)", kcal: 130, carb: 30, protein: 1.5, fat: 0.2 },
  { id: 4, name: "삶은 달걀", kcal: 77, carb: 0.6, protein: 6.3, fat: 5.3 },
  { id: 5, name: "아몬드", kcal: 597, carb: 21, protein: 21, fat: 49 },
  { id: 6, name: "사과", kcal: 57, carb: 14, protein: 0.3, fat: 0.2 },
  { id: 7, name: "바나나", kcal: 89, carb: 22.8, protein: 1.1, fat: 0.3 },
  { id: 8, name: "우유", kcal: 65, carb: 5, protein: 3, fat: 3.2 },

]

// 날짜 변경 시 fetch
watch(
  () => props.date,
  async (d) => {
    if (!d) return
    await day.fetchDay(d)
    resetForm()
  },
  { immediate: true }
)

// store detail 반영
watch(
  detailSafe,
  (v) => {
    condEmoji.value = v.condition_emoji || v.condition?.emoji || ""
    condNote.value = v.condition?.note || ""
    weight.value = v.weight?.weight_kg ?? null
  },
  { immediate: true }
)

// grams 변경 시 자동 계산(선택된 음식이 있을 때만)
watch(grams, (newGrams) => {
  const g = Number(newGrams || 0)
  if (!selectedFood.value || g <= 0) return
  const ratio = g / 100
  kcal.value = Math.round(selectedFood.value.kcal * ratio)
  carb.value = Number((selectedFood.value.carb * ratio).toFixed(1))
  protein.value = Number((selectedFood.value.protein * ratio).toFixed(1))
  fat.value = Number((selectedFood.value.fat * ratio).toFixed(1))
})

// Methods
function resetForm() {
  foodName.value = ""
  grams.value = null
  kcal.value = null
  carb.value = null
  protein.value = null
  fat.value = null
  selectedFood.value = null
  searchQuery.value = ""
  searchResults.value = []
}

function resetSelection() {
  selectedFood.value = null
  foodName.value = ""
  // 선택 해제하면 자동계산 값도 같이 초기화(원하면 유지해도 됨)
  kcal.value = null
  carb.value = null
  protein.value = null
  fat.value = null
}

function performSearch() {
  const q = searchQuery.value.trim()
  if (!q) return
  const query = q.toLowerCase()

  // ✅ 양쪽 다 lower 비교
  searchResults.value = mockFoodDB.filter((f) => f.name.toLowerCase().includes(query))
}

function selectFoodItem(item) {
  selectedFood.value = item
  foodName.value = item.name
  searchResults.value = []
  searchQuery.value = ""

  // 이미 grams가 있으면 즉시 계산
  const g = Number(grams.value || 0)
  if (g > 0) {
    const ratio = g / 100
    kcal.value = Math.round(item.kcal * ratio)
    carb.value = Number((item.carb * ratio).toFixed(1))
    protein.value = Number((item.protein * ratio).toFixed(1))
    fat.value = Number((item.fat * ratio).toFixed(1))
  }
}

function mealLabel(t) {
  return t === "breakfast" ? "아침" : t === "lunch" ? "점심" : "저녁"
}

function getMeals(type) {
  return detailSafe.value.meals?.filter((m) => m.meal_type === type) || []
}

function getGroupCalories(type) {
  const meals = getMeals(type)
  return meals.reduce((acc, cur) => acc + Number(cur.kcal || 0), 0).toFixed(0)
}

async function saveCondition() {
  await day.setCondition(condEmoji.value, condNote.value)
}

async function saveWeight() {
  if (weight.value === null || weight.value === "") return
  await day.setWeight(weight.value)
}

async function addMeal() {
  if (!foodName.value.trim()) return
  await day.addMeal({
    meal_type: mealType.value,
    name: foodName.value.trim(),
    grams: Number(grams.value || 0),
    kcal: Number(kcal.value || 0),
    carb: Number(carb.value || 0),
    protein: Number(protein.value || 0),
    fat: Number(fat.value || 0),
    sugar: 0,
    sodium: 0,
  })

  const currentType = mealType.value
  resetForm()
  mealType.value = currentType
}

async function delMeal(id) {
  if (confirm("정말 삭제하시겠습니까?")) {
    await day.deleteMeal(id)
  }
}
</script>

<style scoped>
/* ✅ scoped에서도 변수 적용되도록 wrapper에 선언 */
.meal-content{
  --primary: #db1f4b;
  --primary-hover: #b9153b;
  --bg-soft: #f8f9fa;
  --bg-panel: #ffffff;
  --text-main: #333333;
  --text-sub: #888888;
  --border-radius: 20px;
  --shadow-soft: 0 8px 30px rgba(0,0,0,0.08);

  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  padding: 5%;
}

/* 폰트는 프로젝트 글로벌(예: main.css)에서 선언하는 것을 권장.
   여기서는 scoped로 쓰되, 경로가 맞는지 확인 필요 */
@font-face {
  font-family: 'AritaDotumKR';
  src: url('@/assets/fonts/AritaDotumKR-Medium.woff2') format('woff2');
  font-weight: 500;
  font-style: normal;
}
@font-face {
  font-family: 'AritaDotumKR';
  src: url('@/assets/fonts/AritaDotumKR-Bold.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
}

* {
  font-family: 'AritaDotumKR', sans-serif;
  box-sizing: border-box;
}
img, svg { display:block; }

/* --- Header --- */
.head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 18px;
}
.h-title {
  display: flex;
  align-items: baseline;
  gap: 8px;
  min-width: 0;
}
.date-highlight {
  font-size: 32px;
  font-weight: 700;
  color: var(--primary);
  line-height: 1;
}
.date-sub { display: flex; flex-direction: column; }
.year-mon { font-size: 14px; color: var(--text-sub); font-weight: 500; }
.day-label { font-size: 12px; color: var(--text-sub); opacity: 0.85; }
.close-btn {
  background: transparent;
  border: none;
  font-size: 20px;
  color: #c7c7c7;
  cursor: pointer;
  transition: color 0.2s;
  line-height: 1;
}
.close-btn:hover { color: #333; }

/* --- State --- */
.state-box {
  padding: 28px 0;
  text-align: center;
  color: #888;
  font-size: 13px;
}
.state-box.error { color: #d32f2f; }
.spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 2px solid #eee;
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: 8px;
  vertical-align: middle;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* --- Dashboard --- */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1.15fr 1.85fr;
  gap: 16px;
  margin-bottom: 18px;
}
@media (max-width: 520px) {
  .dashboard-grid { grid-template-columns: 1fr; }
}
.nutri-card {
  background: white;
  border-radius: 16px;
  padding: 16px;
  border: 1px solid #f0f0f0;
  box-shadow: 0 4px 10px rgba(0,0,0,0.02);
}
.nutri-card.total-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: linear-gradient(135deg, #fff0f5 0%, #fff 100%);
  border-color: #ffe0e6;
}
.card-label { font-size: 12px; color: var(--text-sub); margin-bottom: 4px; }
.card-value.main { font-size: 24px; font-weight: 800; color: var(--primary); }
.card-value .unit { font-size: 14px; font-weight: 500; color: var(--text-sub); margin-left: 4px; }

.progress-bar-bg {
  width: 100%;
  height: 6px;
  background: #eee;
  border-radius: 999px;
  margin-top: 10px;
  overflow: hidden;
}
.progress-bar-fill {
  height: 100%;
  background: var(--primary);
  border-radius: 999px;
  transition: width 0.5s ease;
}
.sub-stats {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 8px;
  min-width: 0;
}
.nutri-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fdfdfd;
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid #f5f5f5;
}
.n-label { font-size: 13px; color: #666; font-weight: 500; }
.n-val { font-size: 14px; font-weight: 700; color: #333; }

/* --- Daily Check --- */
.daily-check-row {
  display: flex;
  gap: 12px;
  margin-bottom: 18px;
  flex-wrap: wrap; /* ✅ 좁으면 내려가게 */
}
.check-item {
  flex: 1 1 240px;
  display: flex;
  align-items: center;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 14px;
  padding: 8px 12px;
  gap: 8px;
  min-width: 0;
}
/* body row에서 몸무게 박스가 남는 공간을 먹지 않게 */
.weight-item{
  flex: 0 0 auto;     /* ✅ grow=0 */
  width: fit-content; /* ✅ 내용만큼 */
}

.check-icon { font-size: 13px; white-space: pre-line; white-space: nowrap;}
.v-divider { width: 1px; height: 16px; background: #eee; }
.clean-input, .clean-select {
  border: none;
  background: transparent;
  font-size: 13px;
  outline: none;
  color: #333;
  padding: 4px;
  min-width: 0;
}
.clean-input.grow { flex: 1; }
.clean-input.weight-input { width: 70px; text-align: right; font-weight: 700; }
.unit-text { font-size: 12px; color: #999; }
.icon-btn {
  border: none;
  background: none;
  font-size: 14px;
  cursor: pointer;
  opacity: 0.55;
  transition: opacity 0.2s;
}
.icon-btn:hover { opacity: 1; }

/* --- Add Meal Card --- */
.add-meal-card {
  background: #ffffff;
  border: 1px solid #eee;
  border-radius: 18px;
  padding: 18px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.03);
  margin-bottom: 18px;
}
.card-header { margin-bottom: 12px; }
.title-text { font-size: 14px; font-weight: 700; color: #333; }

/* Search */
.search-wrapper {
  position: relative;
  display: flex;
  gap: 8px;
  margin-bottom: 14px;
}
.search-input {
  flex: 1;
  padding: 12px 14px;
  background: #f9f9f9;
  border: 1px solid transparent;
  border-radius: 12px;
  font-size: 14px;
  transition: all 0.2s;
  min-width: 0;
}
.search-input:focus {
  background: #fff;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(219, 31, 75, 0.1);
  outline: none;
}
.search-icon-btn {
  background: #333;
  color: white;
  border: none;
  border-radius: 12px;
  width: 44px;
  cursor: pointer;
  font-size: 16px;
}

.search-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  width: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
  list-style: none;
  padding: 0;
  margin: 0;
  z-index: 10;
  max-height: 220px;
  overflow-y: auto;
  border: 1px solid #eee;
}
.search-dropdown li {
  padding: 12px 14px;
  cursor: pointer;
  border-bottom: 1px solid #f5f5f5;
  transition: background 0.1s;
}
.search-dropdown li:hover { background: #fff0f5; }
.res-info-main { font-weight: 600; color: #333; margin-bottom: 2px; }
.res-info-sub { font-size: 12px; color: #888; }

/* Inputs */
.input-area { display: flex; flex-direction: column; gap: 12px; }
.row-top { display: flex; gap: 8px; align-items: center; min-height: 40px; flex-wrap: wrap; }
.styled-select, .styled-input {
  padding: 0 12px;
  height: 40px;
  border-radius: 10px;
  border: 1px solid #eee;
  background: #fff;
  font-size: 13px;
  outline: none;
}
.styled-select { width: 110px; }
.styled-input.grow { flex: 1; min-width: 160px; }
.styled-input:focus, .styled-select:focus { border-color: var(--primary); }

.food-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--primary);
  color: white;
  padding: 0 12px;
  height: 40px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
  max-width: 100%;
}
.food-pill-text {
  max-width: 220px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.pill-close {
  background: rgba(255,255,255,0.2);
  border: none;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 14px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Capsules */
.nutrient-capsules {
  display: grid;
  grid-template-columns: 1.2fr 1fr 1fr 1fr 1fr 90px;
  gap: 6px;
  align-items: end;
}
@media (max-width: 520px) {
  .nutrient-capsules {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .add-btn-gradient { width: 100%; }
}
.capsule {
  display: flex;
  flex-direction: column;
  gap: 4px;
  background: #f9f9f9;
  border-radius: 10px;
  padding: 8px 6px;
  text-align: center;
  border: 1px solid transparent;
  transition: all 0.2s;
  min-width: 0;
}
.capsule.main { background: #fff0f5; border-color: #fecdd6; }
.capsule label { font-size: 10px; color: #888; }
.capsule input {
  width: 100%;
  text-align: center;
  background: transparent;
  border: none;
  font-size: 13px;
  font-weight: 700;
  outline: none;
  padding: 0;
  color: #333;
}
.capsule:focus-within { border-color: var(--primary); background: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }

.add-btn-gradient {
  height: 48px;
  padding: 0 12px;
  background: linear-gradient(135deg, #db1f4b 0%, #b9153b 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 800;
  font-size: 13px;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(219, 31, 75, 0.25);
  transition: transform 0.1s;
}
.add-btn-gradient:active { transform: scale(0.97); }

/* Timeline */
.timeline-container { margin-top: 8px; }
.timeline-group { margin-bottom: 18px; }
.time-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 0 4px;
}
.badge {
  font-size: 12px;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 999px;
}
.badge.breakfast { background: #fff8e1; color: #f57f17; }
.badge.lunch { background: #e3f2fd; color: #1976d2; }
.badge.dinner { background: #f3e5f5; color: #7b1fa2; }
.total-kcal { font-size: 12px; color: #aaa; font-weight: 600; }

.meal-cards { display: flex; flex-direction: column; gap: 8px; }
.meal-card-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 14px;
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
}
.meal-card-item:hover {
  transform: translateX(2px);
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
  border-color: #eee;
}
.mc-content { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.mc-name { font-size: 14px; font-weight: 800; color: #333; }
.mc-gram { font-size: 12px; color: var(--primary); font-weight: 600; margin-left: 4px; }
.mc-nutri { font-size: 11px; color: #999; }
.mc-delete {
  background: #f8f8f8;
  border: none;
  width: 34px;
  height: 34px;
  border-radius: 10px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  transition: all 0.2s;
}
.mc-delete:hover { background: #ffebee; }

/* Empty */
.empty-state {
  text-align: center;
  padding: 36px 0;
  color: #bbb;
}
.empty-icon { font-size: 32px; margin-bottom: 8px; opacity: 0.55; }

/* Transition */
.fade-enter-active, .fade-leave-active { transition: opacity 0.18s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
