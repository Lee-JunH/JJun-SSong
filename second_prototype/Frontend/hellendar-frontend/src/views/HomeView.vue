<template>
  <section>
    <h1>건강한 하루를 기록하는 가장 쉬운 방법</h1>
    <p>식단, 운동, 몸무게, 영양제까지 한 번에 기록하고 확인하세요.</p>
    <div class="cta">
      <RouterLink class="btn" to="/my">마이헬린더</RouterLink>
      <RouterLink class="btn ghost" to="/features">기능소개</RouterLink>
    </div>
  </section>
</template>

<style scoped>
.cta { display:flex; gap:10px; margin-top:12px; }
.btn { padding:10px 14px; border:1px solid #ddd; border-radius:10px; background:#fff; }
.ghost { background:#fafafa; }
</style>
