<template>
  <div class="page">
    <div class="left">
      <MonthCalendar
        :month="month"
        :summaries="cal.days"
        :loading="cal.loading"
        :error="cal.error"
        :selectedDate="selectedDate"
        @changeMonth="onChangeMonth"
        @select="onSelect"
      />
    </div>
    <div class="right">
      <DayDetailPanel v-if="selectedDate" :date="selectedDate" />
      <div v-else class="placeholder">날짜를 선택하세요.</div>
    </div>
  </div>
</template>

<script setup>
import dayjs from "dayjs"
import { ref, onMounted } from "vue"
import { useCalendarStore } from "@/stores/calendar"
import MonthCalendar from "@/components/MonthCalendar.vue"
import DayDetailPanel from "@/components/DayDetailPanel.vue"

const cal = useCalendarStore()
const month = ref(dayjs().format("YYYY-MM"))
const selectedDate = ref(dayjs().format("YYYY-MM-DD"))

onMounted(async () => {
  await cal.fetchMonth(month.value)
})

async function onChangeMonth(m) {
  month.value = m
  await cal.fetchMonth(m)
  // 선택 날짜가 해당 월에 없으면 1일로 보정
  selectedDate.value = `${m}-01`
}

function onSelect(d) {
  selectedDate.value = d
}
</script>

<style scoped>
.page { display:grid; grid-template-columns: 1.1fr 0.9fr; gap:12px; }
.placeholder { border:1px dashed #ddd; border-radius:14px; padding:18px; color:#666; background:#fafafa; }
</style>
