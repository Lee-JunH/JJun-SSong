<template>
  <section>
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <h1>Day: {{ dateStr }}</h1>
      <button type="button" @click="reload" :disabled="loading">새로고침</button>
    </div>

    <p v-if="error" style="color:red;">{{ error }}</p>
    <p v-if="loading">불러오는 중...</p>

    <div v-if="data" style="display:grid; gap:16px; max-width: 900px;">
      <!-- Totals -->
      <div style="border:1px solid #3333; padding:12px; border-radius:10px;">
        <h3>Nutrition Totals</h3>
        <div>kcal: {{ data.nutrition_totals.kcal }}</div>
        <div>carb/protein/fat: {{ data.nutrition_totals.carb_g }} / {{ data.nutrition_totals.protein_g }} / {{ data.nutrition_totals.fat_g }}</div>
        <div>sugar(g): {{ data.nutrition_totals.sugar_g }} <span v-if="data.warnings.sugar_excess" style="color:orange;">(과다)</span></div>
        <div>sodium(mg): {{ data.nutrition_totals.sodium_mg }} <span v-if="data.warnings.sodium_excess" style="color:orange;">(과다)</span></div>
      </div>

      <!-- Quick editors -->
      <div style="border:1px solid #3333; padding:12px; border-radius:10px;">
        <h3>Quick</h3>

        <div style="display:flex; gap:12px; flex-wrap:wrap; align-items:center;">
          <div>
            <div style="font-size:12px; opacity:.7;">Weight (kg)</div>
            <input v-model="weightKg" type="number" step="0.1" style="width:120px;" />
            <button type="button" @click="saveWeight">저장</button>
          </div>

          <div>
            <div style="font-size:12px; opacity:.7;">Condition</div>
            <select v-model="mood">
              <option value="">-</option>
              <option value="good">좋음 🙂</option>
              <option value="ok">보통 😐</option>
              <option value="bad">나쁨 🙁</option>
            </select>
            <button type="button" @click="saveCondition">저장</button>
          </div>

          <div>
            <div style="font-size:12px; opacity:.7;">Supplement</div>
            <label style="display:flex; gap:6px; align-items:center;">
              <input type="checkbox" v-model="supplementTaken" />
              복용
            </label>
            <button type="button" @click="saveSupplement">저장</button>
          </div>
        </div>
      </div>

      <!-- Meals -->
      <div style="border:1px solid #3333; padding:12px; border-radius:10px;">
        <h3>Meals</h3>

        <div style="display:flex; gap:8px; margin-bottom: 10px;">
          <button type="button" @click="goFoodAdd('breakfast')">아침 추가</button>
          <button type="button" @click="goFoodAdd('lunch')">점심 추가</button>
          <button type="button" @click="goFoodAdd('dinner')">저녁 추가</button>
        </div>

        <div v-if="data.meals.length === 0" style="opacity:.7;">아직 식단 기록이 없습니다.</div>

        <MealCard
          v-for="m in data.meals"
          :key="m.meal.id"
          :meal="m"
          @deleteItem="deleteMealItem"
        />
      </div>

      <!-- Exercises -->
      <div style="border:1px solid #3333; padding:12px; border-radius:10px;">
        <h3>Exercises</h3>

        <form @submit.prevent="addExercise" style="display:flex; gap:8px; flex-wrap:wrap; align-items:end;">
          <div>
            <div style="font-size:12px; opacity:.7;">Name</div>
            <input v-model="exName" placeholder="걷기" />
          </div>
          <div>
            <div style="font-size:12px; opacity:.7;">Minutes</div>
            <input v-model.number="exMinutes" type="number" min="1" style="width:100px;" />
          </div>
          <div>
            <div style="font-size:12px; opacity:.7;">Intensity</div>
            <select v-model="exIntensity">
              <option value="low">낮음</option>
              <option value="mid">보통</option>
              <option value="high">높음</option>
            </select>
          </div>
          <button type="submit">추가</button>
        </form>

        <ul style="margin-top:10px;">
          <li v-for="ex in data.exercises" :key="ex.id" style="display:flex; gap:8px; align-items:center;">
            <span>{{ ex.name }} / {{ ex.minutes }}m / {{ ex.intensity }} / {{ ex.estimated_kcal }}kcal</span>
            <button type="button" @click="deleteExercise(ex.id)">삭제</button>
          </li>
        </ul>
      </div>

    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import { recordsApi } from "@/api/records.api"
import MealCard from "@/components/MealCard.vue"

const route = useRoute()
const router = useRouter()

const dateStr = computed(() => route.params.date)

const loading = ref(false)
const error = ref("")
const data = ref(null)

// quick editors
const weightKg = ref("")
const mood = ref("")
const supplementTaken = ref(false)

// exercise form
const exName = ref("")
const exMinutes = ref(30)
const exIntensity = ref("mid")

async function reload() {
  error.value = ""
  loading.value = true
  try {
    const res = await recordsApi.dayDetail(dateStr.value)
    data.value = res.data

    // init quick editors
    weightKg.value = data.value.weight?.weight_kg ?? ""
    mood.value = data.value.condition?.mood ?? ""
    supplementTaken.value = data.value.supplement?.taken ?? false
  } catch (e) {
    error.value = "하루 상세를 불러오지 못했습니다."
  } finally {
    loading.value = false
  }
}

function goFoodAdd(mealType) {
  router.push({
    name: "foods",
    query: { date: dateStr.value, meal_type: mealType, back: "day" },
  })
}

async function deleteMealItem(itemId) {
  await recordsApi.deleteMealItem(itemId)
  reload()
}

async function addExercise() {
  if (!exName.value || !exMinutes.value) return
  await recordsApi.addExercise({
    date: dateStr.value,
    name: exName.value,
    minutes: exMinutes.value,
    intensity: exIntensity.value,
  })
  exName.value = ""
  reload()
}

async function deleteExercise(id) {
  await recordsApi.deleteExercise(id)
  reload()
}

async function saveWeight() {
  if (weightKg.value === "" || weightKg.value === null) return
  await recordsApi.upsertWeight(dateStr.value, { weight_kg: Number(weightKg.value) })
  reload()
}
async function saveCondition() {
  if (!mood.value) return
  await recordsApi.upsertCondition(dateStr.value, { mood: mood.value })
  reload()
}
async function saveSupplement() {
  await recordsApi.upsertSupplement(dateStr.value, { taken: !!supplementTaken.value })
  reload()
}

onMounted(reload)
watch(() => route.params.date, reload)
</script>
