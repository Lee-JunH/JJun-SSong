<template>
  <section>
    <h1>Calendar</h1>

    <div style="display:flex; gap:8px; align-items:center; margin: 12px 0;">
      <button type="button" @click="prevMonth">◀</button>
      <strong>{{ monthLabel }}</strong>
      <button type="button" @click="nextMonth">▶</button>
      <button type="button" @click="reload" :disabled="loading">새로고침</button>
    </div>

    <p v-if="error" style="color:red;">{{ error }}</p>
    <p v-if="loading">불러오는 중...</p>

    <CalendarGrid
      :year="year"
      :month="month"
      :statusMap="statusMap"
      @select="goDay"
    />
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import CalendarGrid from "@/components/CalendarGrid.vue"
import { monthKey } from "@/utils/date"
import { recordsApi } from "@/api/records.api"

const router = useRouter()

const base = ref(new Date())
const loading = ref(false)
const error = ref("")
const statusMap = ref(new Map()) // dateStr -> {has_meal,...}

const year = computed(() => base.value.getFullYear())
const month = computed(() => base.value.getMonth() + 1)
const monthLabel = computed(() => `${year.value}-${String(month.value).padStart(2,"0")}`)

async function reload() {
  error.value = ""
  loading.value = true
  try {
    const { data } = await recordsApi.calendar(monthKey(base.value))
    const m = new Map()
    for (const d of data.days) {
      m.set(d.date, d)
    }
    statusMap.value = m
  } catch (e) {
    error.value = "캘린더 데이터를 불러오지 못했습니다."
  } finally {
    loading.value = false
  }
}

function prevMonth() {
  const d = new Date(base.value)
  d.setMonth(d.getMonth() - 1)
  base.value = d
  reload()
}
function nextMonth() {
  const d = new Date(base.value)
  d.setMonth(d.getMonth() + 1)
  base.value = d
  reload()
}

function goDay(dateStr) {
  router.push({ name: "day", params: { date: dateStr } })
}

onMounted(reload)
</script>
