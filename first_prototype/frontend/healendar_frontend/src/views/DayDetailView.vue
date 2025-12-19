<template>
  <section>
    <h1>Day Detail</h1>
    <p>date: {{ date }}</p>
  </section>
</template>

<script setup>
defineProps({
  date: { type: String, required: true },
})
</script>
