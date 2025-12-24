<template>
  <!-- ✅ 부모 모달 내부에 들어갈 “내용”만 -->
  <div class="meal-content">
    
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
          <div class="card-label">
            총 섭취 칼로리
            <span class="bmr-label">(일일 권장량 기준)</span>
          </div>

          <div class="card-value main">
            {{ Number(detailSafe.total_kcal).toFixed(0) }}
            <span class="bmr-text">/ {{ userTdeeText }}</span>
            <span class="unit">kcal</span>
          </div>

          <div class="progress-bar-bg" aria-hidden="true">
            <div class="progress-bar-fill" :style="progressBarStyle"></div>
          </div>
        </div>

        <div class="sub-stats">
          <div class="nutri-item">
            <div class="n-left">
              <span class="n-label">탄수화물</span>
              <span class="n-sub">{{ goalLabel }} 권장</span>
            </div>
            <div class="n-right">
              <div class="n-main">
                <span class="n-eaten">{{ macroRows.carb.eaten.toFixed(1) }}g</span>
                <span class="n-target">/ {{ macroRows.carb.target }}g</span>
              </div>
              <div class="n-pct">{{ macroRows.carb.percent }}%</div>
            </div>
          </div>

          <div class="nutri-item">
            <div class="n-left">
              <span class="n-label">단백질</span>
              <span class="n-sub">{{ goalLabel }} 권장</span>
            </div>
            <div class="n-right">
              <div class="n-main">
                <span class="n-eaten">{{ macroRows.protein.eaten.toFixed(1) }}g</span>
                <span class="n-target">/ {{ macroRows.protein.target }}g</span>
              </div>
              <div class="n-pct">{{ macroRows.protein.percent }}%</div>
            </div>
          </div>

          <div class="nutri-item">
            <div class="n-left">
              <span class="n-label">지방</span>
              <span class="n-sub">{{ goalLabel }} 권장</span>
            </div>
            <div class="n-right">
              <div class="n-main">
                <span class="n-eaten">{{ macroRows.fat.eaten.toFixed(1) }}g</span>
                <span class="n-target">/ {{ macroRows.fat.target }}g</span>
              </div>
              <div class="n-pct">{{ macroRows.fat.percent }}%</div>
            </div>
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
            placeholder="오늘의 한 줄 메모"
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
              <label>Kcal</label>
              <input v-model.number="kcal" type="number" min="0" placeholder="0" aria-label="칼로리" />
            </div>

            <div class="capsule">
              <label>탄(g)</label>
              <input v-model.number="carb" type="number" min="0" step="0.1" placeholder="0" aria-label="탄수화물" />
            </div>

            <div class="capsule">
              <label>단(g)</label>
              <input v-model.number="protein" type="number" min="0" step="0.1" placeholder="0" aria-label="단백질" />
            </div>

            <div class="capsule">
              <label>지(g)</label>
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
                      {{ Number(m.kcal || 0).toFixed(0) }} kcal · 탄 {{ m.carb }} · 단 {{ m.protein }} · 지 {{ m.fat }}
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
import { useProfileStore } from "@/stores/profile"
import { useAuthStore } from "@/stores/auth"
import { useCalendarStore } from "@/stores/calendar"
import dayjs from "dayjs"

const props = defineProps({
  date: { type: String, required: true },
})
defineEmits(["close"])

const day = useDayStore()
const profile = useProfileStore()
const auth = useAuthStore()
const cal = useCalendarStore()

/**
 * ✅ 로그인 유저가 바뀔 때만 프로필 재조회
 * - id가 없으면(로그아웃) me 비움
 * - id가 바뀌면(계정 전환) me 비우고 fetch
 */
watch(
  () => auth.me?.id,
  async (id, prev) => {
    if (!id) {
      profile.me = null
      return
    }
    if (prev && id !== prev) {
      profile.me = null
    }
    await profile.fetchMe()
  },
  { immediate: true }
)

watch(
  () => props.date,
  async (d) => {
    if (!d) return
    await day.fetchDay(d)
    resetForm()
  },
  { immediate: true }
)

const detail = computed(() => day.detail)
const loading = computed(() => day.loading)
const error = computed(() => day.error)

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

/**
 * ✅ TDEE 계산: profile.me만 신뢰
 * - 값이 없거나 NaN이면 null
 */
const userTdeeRaw = computed(() => {
  const p = profile.me
  if (!p) return null

  const weight = Number(p.weight)
  const height = Number(p.height)
  const age = Number(p.age)
  const gender = p.gender
  const activityLevel = Number(p.activity_level)

  if (!Number.isFinite(weight) || !Number.isFinite(height) || !Number.isFinite(age)) return null
  if (!gender) return null

  let base = 0
  if (gender === "male" || gender === "M") {
    base = 66.47 + 13.75 * weight + 5 * height - 6.76 * age
  } else {
    base = 655.1 + 9.56 * weight + 1.85 * height - 4.68 * age
  }

  const activityMap = { 1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9 }
  const multiplier = activityMap[activityLevel] || 1.2

  return Math.round(base * multiplier)
})

/**
 * ✅ 프로그레스 바 계산용 숫자 (0/undefined 방어)
 */
const userTdeeNumber = computed(() => userTdeeRaw.value ?? 2000)

/**
 * ✅ 템플릿 표시용 문자열 (여기서 toLocaleString 안전하게)
 */
const userTdeeText = computed(() => userTdeeNumber.value.toLocaleString())

/**
 * ✅ 프로그레스 바 스타일
 */
const progressBarStyle = computed(() => {
  const kcal = Number(detailSafe.value.total_kcal || 0)
  const tdee = userTdeeNumber.value
  const ratio = kcal / tdee
  const pct = Math.min(ratio * 100, 100)

  let background = "linear-gradient(90deg, #ff9a9e 0%, #db1f4b 100%)"
  let boxShadow = "none"

  if (ratio > 1.0) {
    background = "linear-gradient(90deg, #ff512f, #dd2476)"
    boxShadow = "0 0 30px rgba(221, 36, 118, 0.4)"
  }

  return {
    width: `${pct}%`,
    background,
    boxShadow,
    transition: "width 0.5s ease, background 0.5s ease",
  }
})
const goalType = computed(() => profile.me?.goal_type || "maintain")

const goalLabel = computed(() => {
  return goalType.value === "loss"
    ? "체중감량"
    : goalType.value === "gain"
    ? "근육증가"
    : "건강유지"
})

/**
 * 권장 탄/단/지(g) 계산
 * - 기준 체중: profile.me.weight가 있으면 그 값, 없으면 start_weight, 둘 다 없으면 70kg
 * - 목표별(maintain/loss/gain)로 단백질/지방 g/kg과 목표 kcal 계수 적용
 */
function computeMacroTarget({ tdeeKcal, weightKg, goal }) {
  // 목표 칼로리: 유지 1.0 / 감량 0.85 / 증량 1.10 (원하면 여기 계수만 조절)
  const kcalFactor = goal === "loss" ? 0.85 : goal === "gain" ? 1.1 : 1.0
  const targetKcal = Math.round(tdeeKcal * kcalFactor)

  // g/kg 가이드(일반적 범위의 “앱용 기본값”)
  const proteinPerKg = goal === "loss" ? 2.0 : goal === "gain" ? 1.8 : 1.6
  const fatPerKg = goal === "loss" ? 0.8 : goal === "gain" ? 1.0 : 0.9

  let proteinG = Math.round(weightKg * proteinPerKg)
  let fatG = Math.round(weightKg * fatPerKg)

  // 칼로리로 환산
  const proteinKcal = proteinG * 4
  let fatKcal = fatG * 9

  // 탄수화물은 남는 칼로리로 채움
  let carbKcal = targetKcal - (proteinKcal + fatKcal)

  // 남는 칼로리가 음수면(단/지가 너무 커서) 지방부터 줄여 맞추기
  if (carbKcal < 0) {
    fatKcal = Math.max(targetKcal - proteinKcal, 0)
    fatG = Math.round(fatKcal / 9)
    carbKcal = 0
  }

  const carbG = Math.round(carbKcal / 4)

  return {
    targetKcal,
    carbG,
    proteinG,
    fatG,
  }
}

const macroTarget = computed(() => {
  const baseW =
    Number(profile.me?.weight) ||
    Number(profile.me?.start_weight) ||
    70

  const tdee = userTdeeNumber.value || 2000

  return computeMacroTarget({
    tdeeKcal: tdee,
    weightKg: baseW,
    goal: goalType.value,
  })
})

function pct(eaten, target) {
  const e = Number(eaten || 0)
  const t = Number(target || 0)
  if (!t) return 0
  return Math.round((e / t) * 100)
}

const macroRows = computed(() => {
  const eatenCarb = Number(detailSafe.value.total_carb || 0)
  const eatenProtein = Number(detailSafe.value.total_protein || 0)
  const eatenFat = Number(detailSafe.value.total_fat || 0)

  return {
    carb: {
      label: "탄수화물",
      eaten: eatenCarb,
      target: macroTarget.value.carbG,
      percent: pct(eatenCarb, macroTarget.value.carbG),
    },
    protein: {
      label: "단백질",
      eaten: eatenProtein,
      target: macroTarget.value.proteinG,
      percent: pct(eatenProtein, macroTarget.value.proteinG),
    },
    fat: {
      label: "지방",
      eaten: eatenFat,
      target: macroTarget.value.fatG,
      percent: pct(eatenFat, macroTarget.value.fatG),
    },
  }
})

// 이하 상태/메서드들은 네 코드 그대로 유지
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

const searchQuery = ref("")
const searchResults = ref([])
const selectedFood = ref(null)

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

watch(
  detailSafe,
  (v) => {
    condEmoji.value = v.condition_emoji || v.condition?.emoji || ""
    condNote.value = v.condition?.note || ""
    weight.value = v.weight?.weight_kg ?? null
  },
  { immediate: true }
)

watch(grams, (newGrams) => {
  const g = Number(newGrams || 0)
  if (!selectedFood.value || g <= 0) return
  const ratio = g / 100
  kcal.value = Math.round(selectedFood.value.kcal * ratio)
  carb.value = Number((selectedFood.value.carb * ratio).toFixed(1))
  protein.value = Number((selectedFood.value.protein * ratio).toFixed(1))
  fat.value = Number((selectedFood.value.fat * ratio).toFixed(1))
})

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
  kcal.value = null
  carb.value = null
  protein.value = null
  fat.value = null
}

function performSearch() {
  const q = searchQuery.value.trim()
  if (!q) return
  const query = q.toLowerCase()
  searchResults.value = mockFoodDB.filter((f) => f.name.toLowerCase().includes(query))
}

function selectFoodItem(item) {
  selectedFood.value = item
  foodName.value = item.name
  searchResults.value = []
  searchQuery.value = ""

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
  

  const t = new Date()
  const todayStr = `${t.getFullYear()}-${String(t.getMonth() + 1).padStart(2, "0")}-${String(t.getDate()).padStart(2, "0")}`

  if (props.date === todayStr) {
    try {
      await profile.updateMe({ weight: Number(weight.value) })
    } catch (e) {
      console.error("프로필 체중 동기화 실패:", e)
    }
  }
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
.meal-content {
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

* {
  font-family: 'AritaDotumKR', sans-serif;
  box-sizing: border-box;
}

/* State Box */
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

/* Dashboard */
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

.card-label {
  font-size: 12px;
  color: var(--text-sub);
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.bmr-label {
  font-size: 11px;
  color: #aaa;
  font-weight: 400;
}

.card-value.main {
  font-size: 24px;
  font-weight: 800;
  color: var(--primary);
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
}
.card-value .unit {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-sub);
  margin-left: 4px;
}
.bmr-text {
  font-size: 16px;
  font-weight: 500;
  color: #999;
  margin-left: 6px;
}

.progress-bar-bg {
  width: 100%;
  height: 8px; /* 높이 약간 조정 */
  background: rgba(0,0,0,0.06); /* 배경색 조금 더 진하게 */
  border-radius: 999px;
  margin-top: 12px;
  overflow: hidden;
}
.progress-bar-fill {
  height: 100%;
  background: var(--primary);
  border-radius: 999px;
  /* transition은 script에서 직접 바인딩으로 처리됨 */
}

/* Sub Stats */
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

/* Daily Check */
.daily-check-row {
  display: flex;
  gap: 12px;
  margin-bottom: 18px;
  flex-wrap: wrap;
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
.weight-item { flex: 0 0 auto; width: fit-content; }
.check-icon { font-size: 13px; white-space: nowrap; }
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

/* Add Meal Card */
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
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9f9f9;
  color: white;
  border: 1px solid transparent;
  border-radius: 12px;
  cursor: pointer;
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

/* Inputs Area */
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
  .add-btn-gradient { width: 100%; grid-column: span 2; }
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
.nutri-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fdfdfd;
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid #f5f5f5;
  gap: 10px;
}

.n-left {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.n-sub {
  font-size: 11px;
  color: #aaa;
  font-weight: 600;
}

.n-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
  white-space: nowrap;
}

.n-main {
  display: flex;
  gap: 6px;
  align-items: baseline;
}

.n-eaten {
  font-size: 14px;
  font-weight: 800;
  color: #333;
}

.n-target {
  font-size: 12px;
  font-weight: 700;
  color: #9ca3af;
}

.n-pct {
  font-size: 12px;
  font-weight: 800;
  color: #db1f4b;
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

/* Empty State */
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