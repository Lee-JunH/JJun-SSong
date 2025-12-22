<!-- StartView.vue -->
<template>
  <section class="start">
    <div class="intro">
      <h1 class="title">헬린더 시작하기</h1>
      <p class="subtitle">3단계로 간편하게 시작하는 건강 관리</p>
    </div>

    <div class="steps" aria-label="시작하기 3단계">
      <article class="step">
        <div class="art">
          <img class="art-img" :src="start1" alt="STEP 1 회원가입 안내 이미지" />
        </div>
        <div class="meta">
          <div class="step-no">STEP 1</div>
          <div class="step-title">회원가입</div>
          <p class="step-desc">이메일과 비밀번호만으로 간편하게 가입하세요.</p>
        </div>
      </article>

      <article class="step">
        <div class="art">
          <img class="art-img" :src="start2" alt="STEP 2 프로필 설정 안내 이미지" />
        </div>
        <div class="meta">
          <div class="step-no">STEP 2</div>
          <div class="step-title">프로필 설정</div>
          <p class="step-desc">기본 정보와 건강 목표를 입력하세요.
            언제든 수정 가능합니다.
          </p>
        </div>
      </article>

      <article class="step">
        <div class="art">
          <img class="art-img" :src="start3" alt="STEP 3 첫 기록 시작 안내 이미지" />
        </div>
        <div class="meta">
          <div class="step-no">STEP 3</div>
          <div class="step-title">첫 기록 시작</div>
          <p class="step-desc">오늘의 식단과 운동을 기록하고
            건강한 습관을 만들어가세요.
          </p>
        </div>
      </article>
    </div>
    <section class="faq" aria-label="자주 묻는 질문">
      <h2 class="faq-title">자주 묻는 질문</h2>

      <div class="faq-list">
        <div v-for="(item, idx) in faqs" :key="idx" class="faq-item">
          <div class="q">
            <span class="qa-prefix">Q.</span>
            <span class="qa-text">{{ item.q }}</span>
          </div>
          <div class="a">
            <span class="qa-prefix">A.</span>
            <span class="qa-text">{{ item.a }}</span>
          </div>
        </div>
      </div>

      <div class="faq-cta">
        <button class="cta-btn" type="button" @click="goSignup">회원가입하고 시작하기</button>
      </div>
    </section>
  </section>
  
</template>

<script setup>
// 확장자(.png/.jpg/.svg)는 실제 파일에 맞춰 수정하세요.
import start1 from "@/assets/start_1.png"
import start2 from "@/assets/start_2.png"
import start3 from "@/assets/start_3.png"

import { useRouter } from "vue-router"

const router = useRouter()

const faqs = [
  {
    q: "헬린더는 무료인가요?",
    a: "기본 기능은 무료로 제공합니다. 프리미엄 기능은 추후 업데이트 예정입니다.",
  },
  {
    q: "모바일 앱도 있나요?",
    a: "현재는 웹 버전만 제공되며, 반응형 디자인으로 모바일에서도 편리하게 사용 가능합니다.",
  },
  {
    q: "데이터는 안전하게 보관되나요?",
    a: "JWT 토큰 기반 인증과 암호화된 통신으로 안전하게 데이터를 보호합니다.",
  },
  {
    q: "음식 데이터베이스는 얼마나 방대한가요?",
    a: "한국 음식을 중심으로 수천 개의 음식 데이터를 제공하며, 커스텀 음식 등록도 가능합니다.",
  },
]

function goSignup() {
  router.push("/signup")
}
</script>


<style scoped>
.start {
  padding: 80px 0 110px;
}

.intro { text-align: center; }
.title { margin: 0; font-size: 52px; letter-spacing: -0.05em; line-height: 1.15; }
.subtitle { margin: 18px 0 0; font-size: 16px; color: #6b7280; }

.steps {
  margin-top: 78px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 58px;
  align-items: start;
}

.step { text-align: center; }

.art {
  border-radius: 8px;
  min-height: 330px;
  display: grid;
  place-items: center;
  overflow: hidden;
}

.art-img {
  width: 100%;
  height: 100%;
  object-fit: contain; /* 전체가 보이게 */
}

.meta { margin-top: 24px; }

.step-no {
  font-size: 32px;
  font-weight: 700; /* Bold를 쓰려면 @font-face에 700 등록 권장 */
  color: #db1f4b;
}

.step-title { margin-top: 12px; font-size: 20px; font-weight: 700; }

.step-desc {
  margin: 14px auto 0;
  max-width: 360px;
  color: #6b7280;
  line-height: 1.7;
  font-size: 14px;

  /* 줄바꿈 방지 + 넘치면 ... */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ---- FAQ ---- */
.faq {
  margin-top: 200px; /* steps 아래 충분한 여백 */
  padding: 80px 0 0;
}

.faq-title {
  text-align: center;
  margin: 0;
  font-size: 40px;
  font-weight: 700;
  letter-spacing: -0.04em;
}

.faq-list {
  margin: 70px auto 0;
  max-width: 780px;        /* 스샷처럼 가운데에 모아두기 */
  padding: 0 20px;
  text-align: left;        /* 내용은 좌측 정렬 */
}

.faq-item + .faq-item {
  margin-top: 34px;
}

.q {
  display: flex;
  gap: 10px;
  align-items: baseline;
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}

.a {
  margin-top: 10px;
  display: flex;
  gap: 10px;
  align-items: baseline;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.8;
}

.qa-prefix {
  flex: 0 0 auto;
  font-weight: 800;
}

.qa-text {
  flex: 1 1 auto;
}

/* CTA 버튼 */
.faq-cta {
  margin-top: 80px;
  display: flex;
  justify-content: center;
}

.cta-btn {
  border: 0;
  cursor: pointer;
  padding: 18px 42px;
  border-radius: 999px;
  background: #16a34a; /* 스샷의 초록 느낌 */
  color: #ffffff;
  font-size: 16px;
  font-weight: 800;
  transition: transform 0.2s ease, filter 0.2s ease;
}

.cta-btn:hover {
  transform: translateY(-1px);
  filter: brightness(0.95);
}

/* Responsive */
@media (max-width: 980px) {
  .steps { grid-template-columns: 1fr; gap: 44px; }
  .title { font-size: 40px; }
  .faq-title { font-size: 34px; }
  .faq { margin-top: 90px; padding-top: 50px; }
}
</style>