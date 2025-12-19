<script setup>

</script>

<template>
  <header
    style="
      display: flex;
      justify-content: center;
      gap: 16px;
      padding: 12px;
      border-bottom: 1px solid #eee;
    "
  >
    <router-link to="/calendar">Calendar</router-link>
    <router-link to="/foods">Food Search</router-link>
    <router-link to="/login">Login</router-link>
  </header>

  <main style="padding: 16px;">
    <router-view />
  </main>
</template>



<style scoped>

</style>
