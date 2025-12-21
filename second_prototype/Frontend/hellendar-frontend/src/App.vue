<template>
  <div class="layout">
    <header class="header">
      <nav class="nav">
        <!-- 로고 (기존 코드 유지) -->
        <div class="brand" role="button" tabindex="0" @click="$router.push('/')">
          <img class="brand-logo" :src="logoUrl" alt="헬린더 로고" />
        </div>

        <!-- 중앙 정렬된 메뉴 링크들 -->
        <div class="links" aria-label="메인 메뉴">
          <RouterLink to="/" class="nav-link" exact-active-class="is-active">홈</RouterLink>
          <RouterLink to="/features" class="nav-link" active-class="is-active">기능소개</RouterLink>
          <RouterLink to="/start" class="nav-link" active-class="is-active">시작하기</RouterLink>
          <RouterLink to="/my" class="nav-link" active-class="is-active">마이헬린더</RouterLink>
        </div>

        <!-- 우측 인증 버튼 -->
        <div class="auth">
          <template v-if="auth.me">
            <span class="me">{{ auth.me.email }}</span>
            <button class="btn logout-btn" @click="onLogout">로그아웃</button>
          </template>
          <template v-else>
            <RouterLink to="/login" class="auth-link">로그인</RouterLink>
            <RouterLink to="/signup" class="btn signup-btn">회원가입</RouterLink>
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
/* --- 레이아웃 설정 --- */
.layout {
  --header-h: 64px; /* 헤더 높이 */
  --primary-color: #DB1F4B; /* 포인트 컬러 */
  
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
}

/* --- Header & Nav --- */
.header {
  height: var(--header-h);
  border-bottom: 1px solid rgba(0,0,0,0.08);
  background: #fff;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav {
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  
  display: flex;
  align-items: center;
  justify-content: space-between; /* 양 끝 정렬 */
  position: relative; /* 자식 요소(links)의 absolute 기준점 */
}

/* 로고 영역 */
.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
  z-index: 10; /* 링크보다 위에 위치 */
}

.brand-logo {
  height: 34px; /* 로고 높이 */
  width: auto;
  display: block;
}

/* --- 중앙 정렬 링크 스타일 --- */
.links {
  position: absolute;
  left: 50%;
  top: 0;
  transform: translateX(-50%); /* 정확한 중앙 정렬 */
  
  height: 100%; /* 헤더 높이 꽉 채우기 */
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-link {
  text-decoration: none;
  color: #868e96;
  font-size: 1rem;
  font-weight: 500;
  
  height: 100%; /* 부모 높이 상속 */
  display: flex;
  align-items: center; /* 텍스트 세로 중앙 */
  padding: 0 16px;
  
  position: relative;
  transition: all 0.2s ease;
  border-bottom: 3px solid transparent; /* 미리 투명 테두리 공간 확보 */
}

/* 호버 효과 */
.nav-link:hover {
  color: #495057;
  background-color: rgba(0,0,0,0.02);
}

/* 활성화(Active) 상태 스타일 */
.nav-link.is-active {
  color: var(--primary-color);
  font-weight: 700;
  border-bottom-color: var(--primary-color); /* 테두리 색상 변경 */
}

/* --- 우측 인증 영역 --- */
.auth {
  display: flex;
  gap: 12px;
  align-items: center;
  z-index: 10; /* 링크보다 위에 위치 */
}

.auth-link {
  text-decoration: none;
  color: #495057;
  font-size: 0.9rem;
  font-weight: 500;
}
.auth-link:hover { color: #212529; }

.btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.logout-btn {
  background: #f1f3f5;
  color: #495057;
}
.logout-btn:hover { background: #e9ecef; }

.signup-btn {
  background: var(--primary-color);
  color: white;
}
.signup-btn:hover {
  background: #c91b42; /* 조금 더 진한 색 */
  transform: translateY(-1px);
}

.me { font-size: 0.85rem; color: #868e96; }

/* --- Main Content --- */
.main {
  flex: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
  position: relative;
}

/* --- Footer --- */
.footer {
  border-top: 1px solid #eee;
  padding: 24px;
  text-align: center;
  color: #adb5bd;
  font-size: 0.85rem;
  background: #fff;
}
</style>