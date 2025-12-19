<template>
  <div class="layout">
    <header class="header">
      <nav class="nav">
        <div class="brand" @click="$router.push('/')">헬린더</div>
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
const auth = useAuthStore()
const onLogout = () => auth.logout()
</script>

<style scoped>
.layout { min-height: 100vh; display:flex; flex-direction:column; }
.header { border-bottom:1px solid #eee; background:#fff; position:sticky; top:0; z-index:10; }
.nav { max-width:1100px; margin:0 auto; padding:14px 16px; display:flex; align-items:center; gap:16px; }
.brand { font-weight:800; cursor:pointer; }
.links { display:flex; gap:12px; flex:1; }
.auth { display:flex; gap:10px; align-items:center; }
.me { font-size:12px; color:#666; }
.btn { padding:6px 10px; border:1px solid #ddd; background:#fff; border-radius:8px; cursor:pointer; }
.main { flex:1; max-width:1100px; width:100%; margin:0 auto; padding:18px 16px; }
.footer { border-top:1px solid #eee; padding:16px; text-align:center; color:#888; font-size:12px; }
a.router-link-active { font-weight:700; }
</style>
