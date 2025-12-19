<template>
  <section>
    <h1>Calendar</h1>
    <p>월 캘린더 프로토타입</p>

    <button @click="goToday">오늘 상세로 이동</button>
  </section>
</template>

<script setup>
import { useRouter } from "vue-router"

const router = useRouter()

function goToday() {
  const yyyy = new Date().getFullYear()
  const mm = String(new Date().getMonth() + 1).padStart(2, "0")
  const dd = String(new Date().getDate()).padStart(2, "0")
  router.push(`/day/${yyyy}-${mm}-${dd}`)
}
</script>
