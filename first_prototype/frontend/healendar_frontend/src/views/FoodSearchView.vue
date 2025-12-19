<template>
  <section style="max-width: 720px;">
    <h1>Food Search</h1>

    <p style="opacity:.8;">
      date: <strong>{{ date }}</strong>,
      meal: <strong>{{ mealType }}</strong>
    </p>

    <div style="display:flex; gap:8px; margin: 10px 0;">
      <input v-model.trim="q" placeholder="음식명 검색" style="flex:1;" />
      <button type="button" @click="search" :disabled="loading">검색</button>
      <button type="button" @click="goBack">뒤로</button>
    </div>

    <p v-if="error" style="color:red;">{{ error }}</p>
    <p v-if="loading">불러오는 중...</p>

    <div v-if="results.length" style="display:grid; gap:8px;">
      <div
        v-for="r in results"
        :key="r.source + '-' + r.id"
        style="border:1px solid #3333; border-radius:10px; padding:10px;"
      >
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <strong>{{ r.name }}</strong>
          <span style="opacity:.7;">{{ r.source }}</span>
        </div>

        <div style="font-size:13px; opacity:.85; margin-top:6px;">
          기준 {{ r.serving_g }}g / {{ r.kcal }}kcal (C/P/F: {{ r.carb_g }}/{{ r.protein_g }}/{{ r.fat_g }})
        </div>

        <div style="display:flex; gap:8px; margin-top:10px; align-items:center;">
          <input v-model.number="amountMap[r.source + ':' + r.id]" type="number" min="1" placeholder="그램(g)" style="width:120px;" />
          <button type="button" @click="addToMeal(r)">추가</button>
        </div>
      </div>
    </div>

    <div v-else style="opacity:.7;">
      검색 결과가 없습니다. (또는 검색어를 입력하세요)
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { foodsApi } from "@/api/foods.api"
import { recordsApi } from "@/api/records.api"

const route = useRoute()
const router = useRouter()

const date = computed(() => route.query.date || "")
const mealType = computed(() => route.query.meal_type || "")

const q = ref("")
const loading = ref(false)
const error = ref("")
const results = ref([])

const mealId = ref(null)

// result별 grams 입력값 저장
const amountMap = ref({})

async function ensureMeal() {
  if (!date.value || !mealType.value) {
    error.value = "date, meal_type 쿼리가 필요합니다. (/foods?date=YYYY-MM-DD&meal_type=breakfast)"
    return
  }
  const { data } = await recordsApi.mealUpsert({ date: date.value, meal_type: mealType.value })
  mealId.value = data.meal.id
}

async function search() {
  error.value = ""
  if (!q.value) {
    results.value = []
    return
  }
  loading.value = true
  try {
    const { data } = await foodsApi.search(q.value)
    results.value = data.results || []
  } catch (e) {
    error.value = "검색 실패"
  } finally {
    loading.value = false
  }
}

async function addToMeal(food) {
  if (!mealId.value) await ensureMeal()
  const key = `${food.source}:${food.id}`
  const grams = Number(amountMap.value[key] || 0)
  if (!grams || grams <= 0) {
    error.value = "그램(g)을 입력하세요."
    return
  }

  const payload = { meal: mealId.value, amount_g: grams }
  if (food.source === "dataset") payload.food = food.id
  else payload.custom_food = food.id

  try {
    await recordsApi.addMealItem(payload)
    goBack()
  } catch (e) {
    error.value = "식단 추가 실패"
  }
}

function goBack() {
  // DayDetail로 복귀
  if (date.value) router.push({ name: "day", params: { date: date.value } })
  else router.push({ name: "calendar" })
}

onMounted(ensureMeal)
</script>
