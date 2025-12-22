<template>
  <div class="layout">
    <header class="header">
      <nav class="nav">
        <div class="nav-inner">
          <div class="brand" role="button" tabindex="0" @click="$router.push('/')">
            <img class="brand-logo" :src="logoUrl" alt="헬린더 로고" />
          </div>

          <div class="links" aria-label="메인 메뉴">
            <RouterLink to="/" class="nav-link" exact-active-class="is-active">홈</RouterLink>
            <RouterLink to="/features" class="nav-link" exact-active-class="is-active">기능소개</RouterLink>
            <RouterLink v-if="!auth.me" to="/start" class="nav-link" exact-active-class="is-active">시작하기</RouterLink>
            <RouterLink to="/my" class="nav-link" exact-active-class="is-active">마이헬린더</RouterLink>
          </div>

          <div class="auth">
            <template v-if="!auth.isBootstrapped">
              <span style="font-size:12px;color:#999;">확인 중...</span>
            </template>

            <template v-else-if="auth.me">
              <span class="user-profile">
                <RouterLink v-if="auth.me" to="/profile" class="user-id">
                  {{ auth.me.email }}
                </RouterLink>
              </span>
              <!-- 클래스 추가 및 클릭 핸들러 수정 -->
              <button class="btn logout-btn" @click="openLogoutModal">로그아웃</button>
            </template>

            <template v-else>
              <!-- 클래스 추가: 스타일 적용을 위해 auth-link, signup-btn 추가 -->
              <RouterLink to="/login" class="auth-link">로그인</RouterLink>
              <RouterLink to="/signup" class="btn signup-btn">회원가입</RouterLink>
            </template>
          </div>
        </div>
      </nav>
    </header>


    <main class="main">
      <RouterView />
    </main>

    <footer class="footer">
      © 헬린더
    </footer>
  </div>

  <ConfirmModal
    :open="showLogoutModal"
    title=""                              
    message="로그아웃 하시겠습니까?"
    confirm-text="네"
    cancel-text="아니요"
    @confirm="confirmLogout"
    @cancel="closeLogoutModal"
  />

</template>

<script setup>
import { ref, onMounted } from "vue"
import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"
import logoUrl from "@/assets/logo.png"
import ConfirmModal from "@/components/ConfirmModal.vue"

const auth = useAuthStore()
const router = useRouter()

const showLogoutModal = ref(false)

onMounted(async () => {
  // 새로고침 시 localStorage에서 토큰을 복구해두었으므로
  // accessToken이 있으면 사용자 정보를 가져와 `auth.me`를 채웁니다.
  if (auth.accessToken && !auth.me) {
    try {
      await auth.fetchMe()
    } catch (e) {
      // 토큰 만료/오류 시 안전하게 로그아웃 처리
      auth.logout()
      // 선택: 홈으로 리다이렉트(현재는 강제 이동하지 않음)
      router.replace("/")
    }
  }
})

function openLogoutModal() {
  showLogoutModal.value = true
}

function closeLogoutModal() {
  showLogoutModal.value = false
}

async function confirmLogout() {
  try {
    await auth.logout()
  } finally {
    showLogoutModal.value = false
    router.replace("/")
  }
}
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
  width: 100%;              /* ✅ header 폭을 그대로 사용 */
  padding: 0;               /* ✅ 바깥은 full-bleed */
}

.nav-inner {
  height: 100%;
  max-width: 1200px;        /* ✅ 내용만 1200 제한 */
  margin: 0 auto;
  padding: 0 24px;

  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;       /* links absolute 기준점 */
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
  padding: 8px 12px; /* 패딩 추가 */
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
  display: inline-flex; /* 버튼 내용 정렬 */
  align-items: center;
  justify-content: center;
  text-decoration: none; /* a태그 밑줄 제거 */
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