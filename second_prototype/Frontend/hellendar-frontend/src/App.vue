<template>
  <div class="layout">
    <header class="header">
      <nav class="nav">
        <div class="brand" role="button" tabindex="0" @click="$router.push('/')">
          <img class="brand-logo" :src="logoUrl" alt="헬린더 로고" />
          <!-- 필요하면 텍스트도 같이 -->
          <!-- <span class="brand-text">헬린더</span> -->
        </div>


        <div class="links">
          <RouterLink to="/">홈</RouterLink>
          <RouterLink to="/features">기능소개</RouterLink>
          <RouterLink to="/start">시작하기</RouterLink>
          <RouterLink to="/my">마이헬린더</RouterLink>
        </div>
        <div class="auth">
          <template v-if="auth.me">
            <span class="me">{{ auth.me.email }}</span>
            <button class="btn" @click="onLogout">로그아웃</button>
          </template>
          <template v-else>
            <RouterLink to="/login">로그인</RouterLink>
            <RouterLink to="/signup">회원가입</RouterLink>
          </template>
        </div>
      </nav>
    </header>

    <main class="main">
      <RouterView />
    </main>

    <footer class="footer">
      © Healendar
    </footer>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth"
import logoUrl from "@/assets/logo.png"

const auth = useAuthStore()
const onLogout = () => auth.logout()
</script>


<style scoped>
/* 헤더 높이(원하는 값으로 조정) */
.layout {
  --header-h: 56px; /* 56~72px 추천 */
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* sticky 헤더는 “위에 떠있으므로” 배경/보더 확실히 + 겹침 방지 */
.header {
  height: var(--header-h);
  border-bottom: 1px solid #eee;
  background: #fff;

  position: sticky;
  top: 0;
  z-index: 1000;           /* 캘린더보다 확실히 위 */
}

/* nav가 헤더 높이를 꽉 채우도록 */
.nav {
  height: 100%;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 16px;         /* 세로 padding 제거하고 height로 맞춤 */
  display: flex;
  align-items: center;
  gap: 16px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  user-select: none;
}

.brand-logo {
  height: 34px;     /* 네브바 높이에 맞춰 조정: 28~40px */
  width: auto;
  display: block;
}

.brand:focus-visible {
  outline: 2px solid #dee2e6;
  outline-offset: 4px;
  border-radius: 8px;
}

.links { display: flex; gap: 12px; flex: 1; }
.auth { display: flex; gap: 10px; align-items: center; }
.me { font-size: 12px; color: #666; }
.btn {
  padding: 6px 10px;
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 8px;
  cursor: pointer;
}
a.router-link-active { font-weight: 700; }

/* main은 원래 padding-top을 줄 필요 없음(헤더가 레이아웃을 차지하므로).
   다만 sticky+transform 등 영향으로 겹침이 생기는 프로젝트가 있어 안전장치로 둠 */
.main {
  flex: 1;
  max-width: 1100px;
  width: 100%;
  margin: 0 auto;
  padding: 18px 16px;

  /* 안전장치: 캘린더 등 내부 요소가 header를 침범하는 경우가 있어 방지 */
  position: relative;
  z-index: 0;
}

/* footer */
.footer {
  border-top: 1px solid #eee;
  padding: 16px;
  text-align: center;
  color: #888;
  font-size: 12px;
}
</style>
