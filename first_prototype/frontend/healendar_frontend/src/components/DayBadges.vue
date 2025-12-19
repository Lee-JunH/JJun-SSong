<template>
  <div style="margin-top: 8px; display:flex; flex-wrap:wrap; gap:6px; font-size: 13px;">
    <span v-if="status?.has_meal">🍽</span>
    <span v-if="status?.has_exercise">🏃</span>
    <span v-if="status?.has_weight">⚖</span>
    <span v-if="status?.supplement_taken">💊</span>
    <span v-if="status?.mood === 'good'">🙂</span>
    <span v-else-if="status?.mood === 'ok'">😐</span>
    <span v-else-if="status?.mood === 'bad'">🙁</span>
  </div>
</template>

<script setup>
defineProps({
  status: Object
})
</script>
