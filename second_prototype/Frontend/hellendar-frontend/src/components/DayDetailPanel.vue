<template>
  <div class="panel">
    <div class="head">
      <div class="h-title">{{ date }}</div>
    </div>

    <div v-if="loading" class="box">불러오는 중...</div>
    <div v-else-if="error" class="box error">{{ error }}</div>

    <template v-else>
      <div class="stats">
        <div class="stat"><div class="k">총 칼로리</div><div class="v">{{ detail.total_kcal.toFixed(0) }} kcal</div></div>
        <div class="stat"><div class="k">탄수화물</div><div class="v">{{ detail.total_carb.toFixed(1) }} g</div></div>
        <div class="stat"><div class="k">단백질</div><div class="v">{{ detail.total_protein.toFixed(1) }} g</div></div>
        <div class="stat"><div class="k">지방</div><div class="v">{{ detail.total_fat.toFixed(1) }} g</div></div>
      </div>

      <div class="row">
        <div class="box">
          <div class="box-title">컨디션</div>
          <div class="inline">
            <select v-model="condEmoji" class="small">
              <option value="">선택</option>
              <option value="😊">😊 좋음</option>
              <option value="🙂">🙂 보통</option>
              <option value="😣">😣 나쁨</option>
            </select>
            <input v-model="condNote" placeholder="메모(선택)" class="grow" />
            <button class="btn" @click="saveCondition">저장</button>
          </div>
        </div>

        <div class="box">
          <div class="box-title">몸무게</div>
          <div class="inline">
            <input v-model.number="weight" type="number" step="0.1" placeholder="kg" class="small" />
            <button class="btn" @click="saveWeight">저장</button>
          </div>
        </div>
      </div>

      <div class="box">
        <div class="box-title">식단 추가</div>
        <div class="inline">
          <select v-model="mealType" class="small">
            <option value="breakfast">아침</option>
            <option value="lunch">점심</option>
            <option value="dinner">저녁</option>
          </select>
          <input v-model="foodName" placeholder="음식명" class="grow" />
          <input v-model.number="grams" type="number" step="1" placeholder="그램수(g)" class="small" />
        </div>
        
        <!-- 변경: 영양성분 입력을 위한 그리드 레이아웃 적용 -->
        <div class="nutrition-row">
          <input v-model.number="kcal" type="number" step="1" placeholder="칼로리(kcal)" />
          <input v-model.number="carb" type="number" step="0.1" placeholder="탄수화물(g)" />
          <input v-model.number="protein" type="number" step="0.1" placeholder="단백질(g)" />
          <input v-model.number="fat" type="number" step="0.1" placeholder="지방(g)" />
          <button class="btn" @click="addMeal">추가</button>
        </div>

        <div class="list" v-if="detail.meals?.length">
          <template v-for="type in ['breakfast', 'lunch', 'dinner']" :key="type">
            <div v-if="getMeals(type).length > 0" class="meal-group">
              <div class="meal-divider">{{ mealLabel(type) }}</div>
              <div v-for="m in getMeals(type)" :key="m.id" class="item">
                <div class="meta">
                  <div class="t">{{ m.name }} ({{ m.grams }}g)</div>
                  <div class="s">{{ m.kcal.toFixed(0) }} kcal</div>
                </div>
                <button class="x" @click="delMeal(m.id)">삭제</button>
              </div>
            </div>
          </template>
        </div>
        <div v-else class="muted">아직 식단 기록이 없습니다.</div>
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

const day = useDayStore()
const detail = computed(() => day.detail)
const loading = computed(() => day.loading)
const error = computed(() => day.error)

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

watch(() => props.date, async (d) => {
  if (d) {
    await day.fetchDay(d)
    grams.value = null
    foodName.value = ""
    kcal.value = carb.value = protein.value = fat.value = null
  }
}, { immediate: true })

watch(detail, (v) => {
  if (!v) return
  condEmoji.value = v.condition_emoji || v.condition?.emoji || ""
  condNote.value = v.condition?.note || ""
  weight.value = v.weight?.weight_kg ?? null
}, { immediate: true })

function mealLabel(t) {
  return t === "breakfast" ? "아침" : t === "lunch" ? "점심" : "저녁"
}

function getMeals(type) {
  return detail.value.meals?.filter(m => m.meal_type === type) || []
}

async function saveCondition() {
  await day.setCondition(condEmoji.value, condNote.value)
}

async function saveWeight() {
  if (weight.value === null || weight.value === "") return
  await day.setWeight(weight.value)
}

async function onSupp(e) {
  await day.setSupplement(e.target.checked)
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
  foodName.value = ""
  grams.value = null
  kcal.value = carb.value = protein.value = fat.value = null
}

async function delMeal(id) {
  await day.deleteMeal(id)
}
</script>

<style scoped>
.panel { border:1px solid #eee; border-radius:14px; padding:14px; background:#fff; }
.head { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
.h-title { font-weight:900; }
.toggle { display:flex; align-items:center; gap:8px; font-size:13px; color:#444; }
.stats { display:grid; grid-template-columns:repeat(4, 1fr); gap:10px; margin-bottom:10px; }
.stat { border:1px solid #eee; border-radius:12px; padding:10px; }
.k { font-size:12px; color:#666; }
.v { margin-top:4px; font-weight:800; }

.row { display:grid; grid-template-columns: 2.2fr 1fr; gap:10px; margin-bottom:10px; }

.box { border:1px solid #eee; border-radius:12px; padding:12px; }
.box-title { font-weight:800; margin-bottom:8px; }
.inline { display:flex; gap:8px; align-items:center; }
.small { width:120px; padding:8px; border:1px solid #ddd; border-radius:10px; }
.grow { flex:1; padding:8px; border:1px solid #ddd; border-radius:10px; }

.btn { 
  padding:8px 12px; 
  border:1px solid #ddd; 
  background:#fff; 
  border-radius:10px; 
  cursor:pointer; 
  white-space: nowrap; 
  flex-shrink: 0; 
}

/* 추가: 영양성분 입력줄 그리드 스타일 */
.nutrition-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr auto;
  gap: 8px;
  margin-top: 8px;
}
/* 영양성분 입력창 스타일 (기존 small/grow 스타일 적용) */
.nutrition-row input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 10px;
}

.list { margin-top:10px; display:flex; flex-direction:column; gap:8px; }

.meal-group { display: flex; flex-direction: column; gap: 8px; }
.meal-divider { 
  font-size: 13px; 
  font-weight: 700; 
  color: #888; 
  margin-top: 8px; 
  margin-bottom: 2px;
  padding-left: 4px;
  display: flex;
  align-items: center;
}
.meal-divider::after { 
  content: ""; 
  flex: 1; 
  height: 1px; 
  background: #eee; 
  margin-left: 8px; 
}

.item { display:flex; justify-content:space-between; align-items:center; border:1px solid #eee; border-radius:12px; padding:10px; }
.meta .t { font-weight:700; }
.meta .s { color:#666; font-size:12px; margin-top:2px; }
.x { border:1px solid #ddd; background:#fff; border-radius:10px; padding:6px 10px; cursor:pointer; }
.muted { color:#777; font-size:13px; }
.error { color:#b00; }
</style>