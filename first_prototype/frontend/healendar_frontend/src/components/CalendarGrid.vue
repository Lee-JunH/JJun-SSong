<template>
  <div style="display:grid; grid-template-columns: repeat(7, 1fr); gap:8px;">
    <div v-for="w in week" :key="w" style="font-weight:600; opacity:.7;">{{ w }}</div>

    <button
      v-for="cell in grid"
      :key="cell.key"
      type="button"
      @click="$emit('select', cell.dateStr)"
      :style="{
        border: '1px solid #3333',
        padding: '10px',
        borderRadius: '8px',
        textAlign: 'left',
        opacity: cell.inMonth ? 1 : 0.35,
        cursor: 'pointer',
        minHeight: '70px',
        background: 'transparent',
        color: 'inherit'
      }"
    >
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <strong>{{ cell.day }}</strong>
      </div>

      <DayBadges :status="statusMap?.get(cell.dateStr)" />
    </button>
  </div>
</template>

<script setup>
import { computed } from "vue"
import DayBadges from "./DayBadges.vue"
import { buildMonthGrid, formatDate } from "@/utils/date"

const props = defineProps({
  year: Number,
  month: Number, // 1..12
  statusMap: Object, // Map
})

defineEmits(["select"])

const week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

const grid = computed(() => {
  const cells = buildMonthGrid(props.year, props.month)
  return cells.map((c) => {
    const y = c.date.getFullYear()
    const m = c.date.getMonth() + 1
    const d = c.date.getDate()
    return {
      key: c.date.toISOString(),
      dateStr: formatDate(y, m, d),
      day: d,
      inMonth: c.inMonth,
    }
  })
})
</script>
