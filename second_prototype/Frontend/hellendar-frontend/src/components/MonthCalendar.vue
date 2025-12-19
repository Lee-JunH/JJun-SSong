<template>
  <div class="cal">
    <div class="cal-head">
      <button class="icon" @click="prevMonth">‹</button>
      <div class="title">{{ label }}</div>
      <button class="icon" @click="nextMonth">›</button>
    </div>

    <div class="dow">
      <div v-for="d in ['일','월','화','수','목','금','토']" :key="d" class="dow-cell">{{ d }}</div>
    </div>

    <div v-if="loading" class="grid">
      <div v-for="i in 42" :key="i" class="cell skeleton"></div>
    </div>

    <div v-else class="grid">
      <button
        v-for="cell in cells"
        :key="cell.key"
        class="cell"
        :class="{ muted: !cell.inMonth, selected: cell.date === selectedDate }"
        @click="$emit('select', cell.date)"
      >
        <div class="date">{{ cell.dayNum }}</div>
        <div class="badges" v-if="cell.summary">
          <span v-if="cell.summary.has_meal" class="badge">식</span>
          <span v-if="cell.summary.has_exercise" class="badge">운</span>
          <span v-if="cell.summary.has_weight" class="badge">체</span>
          <span v-if="cell.summary.condition_emoji" class="emoji">{{ cell.summary.condition_emoji }}</span>
          <span v-if="cell.summary.supplement_taken" class="pill">💊</span>
          <span v-if="cell.summary.warning_flags?.length" class="warn">!</span>
        </div>
      </button>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import dayjs from "dayjs"
import { computed, ref, watchEffect } from "vue"

const props = defineProps({
  month: { type: String, required: true }, // YYYY-MM
  summaries: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  error: { type: String, default: "" },
  selectedDate: { type: String, default: "" },
})
const emit = defineEmits(["changeMonth", "select"])

const map = computed(() => {
  const m = new Map()
  props.summaries.forEach(s => m.set(s.date, s))
  return m
})

const label = computed(() => props.month)

const cells = computed(() => {
  const first = dayjs(props.month + "-01")
  const start = first.startOf("month").startOf("week") // 일요일 시작
  const end = first.endOf("month").endOf("week")

  const arr = []
  let cur = start
  while (cur.isBefore(end) || cur.isSame(end, "day")) {
    const d = cur.format("YYYY-MM-DD")
    arr.push({
      key: d,
      date: d,
      dayNum: cur.date(),
      inMonth: cur.month() === first.month(),
      summary: map.value.get(d) || null,
    })
    cur = cur.add(1, "day")
  }
  // 항상 42칸(6주) 맞추기
  while (arr.length < 42) {
    const last = dayjs(arr[arr.length - 1].date).add(1, "day")
    const d = last.format("YYYY-MM-DD")
    arr.push({
      key: d,
      date: d,
      dayNum: last.date(),
      inMonth: false,
      summary: map.value.get(d) || null,
    })
  }
  return arr.slice(0, 42)
})

function prevMonth() {
  const m = dayjs(props.month + "-01").add(-1, "month").format("YYYY-MM")
  emit("changeMonth", m)
}
function nextMonth() {
  const m = dayjs(props.month + "-01").add(1, "month").format("YYYY-MM")
  emit("changeMonth", m)
}
</script>

<style scoped>
.cal { border:1px solid #eee; border-radius:14px; padding:14px; background:#fff; }
.cal-head { display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; }
.title { font-weight:800; }
.icon { width:34px; height:34px; border:1px solid #ddd; border-radius:10px; background:#fff; cursor:pointer; }
.dow { display:grid; grid-template-columns:repeat(7, 1fr); gap:8px; margin-bottom:8px; color:#666; font-size:12px; }
.dow-cell { text-align:center; }
.grid { display:grid; grid-template-columns:repeat(7, 1fr); gap:8px; }
.cell { min-height:78px; border:1px solid #eee; border-radius:12px; background:#fff; padding:8px; text-align:left; cursor:pointer; }
.cell.muted { opacity:0.45; }
.cell.selected { outline:2px solid #00EEFF; }
.date { font-weight:700; font-size:12px; color:#333; }
.badges { margin-top:6px; display:flex; flex-wrap:wrap; gap:6px; align-items:center; }
.badge { font-size:11px; border:1px solid #ddd; border-radius:8px; padding:2px 6px; }
.emoji { font-size:14px; }
.pill { font-size:13px; }
.warn { font-weight:900; color:#b00; }
.error { margin-top:10px; color:#b00; font-size:13px; }
.skeleton { background:#f5f5f5; border-color:#f5f5f5; }
</style>
