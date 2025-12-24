<template>
  <section class="start">
    <!-- 인트로 섹션: 페이지 로드 시 바로 애니메이션 -->
    <div class="intro fade-in-up">
      <h1 class="title">헬린더 시작하기</h1>
      <p class="subtitle">3단계로 간편하게 시작하는 건강 관리</p>
    </div>

    <!-- 스텝 섹션: 스크롤 시 순차적으로 등장 -->
    <div class="steps" aria-label="시작하기 3단계">
      <article 
        v-for="(step, index) in steps" 
        :key="index" 
        class="step scroll-reveal"
        :style="{ transitionDelay: `${index * 200}ms` }"
        ref="stepRefs"
      >
        <div class="art">
          <img class="art-img" :src="step.img" :alt="step.alt" />
        </div>
        <div class="meta">
          <div class="step-no">{{ step.no }}</div>
          <div class="step-title">{{ step.title }}</div>
          <p class="step-desc">{{ step.desc }}</p>
        </div>
      </article>
    </div>

    <!-- FAQ 섹션 -->
    <section class="faq scroll-reveal" ref="faqSectionRef" aria-label="자주 묻는 질문">
      <h2 class="faq-title">자주 묻는 질문</h2>

      <div class="faq-list">
        <!-- 아코디언 UI 적용 -->
        <div 
          v-for="(item, idx) in faqs" 
          :key="idx" 
          class="faq-item"
          :class="{ active: openFaqIndex === idx }"
          @click="toggleFaq(idx)"
        >
          <div class="q">
            <span class="qa-prefix">Q.</span>
            <span class="qa-text">{{ item.q }}</span>
            <!-- 화살표 아이콘 -->
            <span class="arrow-icon"></span>
          </div>
          <div class="a-wrapper" :style="{ maxHeight: openFaqIndex === idx ? '200px' : '0px' }">
            <div class="a">
              <span class="qa-prefix">A.</span>
              <span class="qa-text">{{ item.a }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="faq-cta">
        <button class="cta-btn pulse-animation" type="button" @click="goSignup">
          회원가입하고 시작하기
        </button>
      </div>
    </section>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue"
import { useRouter } from "vue-router"

// 이미지 경로 (실제 경로에 맞게 유지)
import start1 from "@/assets/start_1.png"
import start2 from "@/assets/start_2.png"
import start3 from "@/assets/start_3.png"

const router = useRouter()

// 데이터 구조화 (v-for 렌더링을 위해)
const steps = [
  {
    img: start1,
    alt: "STEP 1 회원가입 안내 이미지",
    no: "STEP 1",
    title: "회원가입",
    desc: "이메일과 비밀번호만으로\n간편하게 가입하세요."
  },
  {
    img: start2,
    alt: "STEP 2 프로필 설정 안내 이미지",
    no: "STEP 2",
    title: "프로필 설정",
    desc: "기본 정보와 건강 목표를 입력하세요.\n언제든 수정 가능합니다."
  },
  {
    img: start3,
    alt: "STEP 3 첫 기록 시작 안내 이미지",
    no: "STEP 3",
    title: "첫 기록 시작",
    desc: "오늘의 식단과 운동을 기록하고\n건강한 습관을 만들어가세요."
  }
]

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

// --- FAQ 아코디언 로직 ---
const openFaqIndex = ref(null) // 현재 열려있는 FAQ 인덱스 (null이면 모두 닫힘)

function toggleFaq(idx) {
  // 이미 열린 것을 누르면 닫기, 아니면 해당 인덱스 열기
  openFaqIndex.value = openFaqIndex.value === idx ? null : idx
}

function goSignup() {
  router.push("/signup")
}

// --- 스크롤 애니메이션 (IntersectionObserver) ---
const stepRefs = ref([])
const faqSectionRef = ref(null)

let observer = null

onMounted(() => {
  // IntersectionObserver 설정
  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible')
        // 한 번 보이면 관찰 중지 (성능 최적화)
        observer.unobserve(entry.target)
      }
    })
  }, {
    threshold: 0.15, // 15% 정도 보이면 트리거
    rootMargin: "0px 0px -50px 0px" // 약간 미리 로드
  })

  // 관찰 대상 등록
  // 1. Step 요소들 (배열 ref 처리 주의: Vue 3 v-for ref)
  if (stepRefs.value) {
    // stepRefs는 DOM 엘리먼트 배열이 됨 (Vue 3.2.25+ v-for ref 자동 언랩)
    stepRefs.value.forEach(el => observer.observe(el))
  }
  
  // 2. FAQ 섹션
  if (faqSectionRef.value) {
    observer.observe(faqSectionRef.value)
  }
})

onUnmounted(() => {
  if (observer) observer.disconnect()
})
</script>

<style scoped>
.start {
  margin-top: 20px;
  padding: 110px 0 120px;
  overflow: hidden; /* 애니메이션으로 인한 가로 스크롤 방지 */
}

/* --- Intro Animation --- */
.intro { 
  text-align: center; 
}

/* 페이지 로드 시 자동 실행 애니메이션 */
.fade-in-up {
  animation: fadeInUp 0.8s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.title {   
  margin: 0;
  font-size: 48px;
  letter-spacing: -0.05em;
  line-height: 1.15;
  color: #111827;
  font-weight: 800;
}
.subtitle { margin: 18px 0 0; font-size: 16px; color: #6b7280; }

/* --- Steps Section --- */
.steps {
  margin-top: 78px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 58px;
  align-items: start;
}

.step { 
  text-align: center; 
  /* Scroll Reveal 초기 상태 */
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}

/* 화면에 들어왔을 때 붙는 클래스 */
.step.visible {
  opacity: 1;
  transform: translateY(0);
}

.art {
  border-radius: 20px; /* 더 부드럽게 */
  min-height: 330px;
  display: grid;
  place-items: center;
  overflow: hidden;
  background: #f9fafb; /* 배경색 추가로 깊이감 */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* Hover Effect: 카드가 살짝 떠오르는 느낌 */
.step:hover .art {
  transform: translateY(-8px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
}

.art-img {
  width: 90%; /* 여백을 줘서 답답하지 않게 */
  height: auto;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.step:hover .art-img {
  transform: scale(1.05); /* 이미지 살짝 확대 */
}

.meta { margin-top: 24px; }

.step-no {
  font-size: 32px;
  font-weight: 700;
  color: #db1f4b;
}

.step-title { margin-top: 12px; font-size: 20px; font-weight: 700; }

.step-desc {
  margin: 14px auto 0;
  max-width: 360px;
  color: #6b7280;
  line-height: 1.7;
  font-size: 14px;
  white-space: pre-line;
}

/* ---- FAQ ---- */
.faq {
  margin-top: 200px;
  padding: 80px 0 0;
  
  /* Scroll Reveal 초기 상태 */
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}

.faq.visible {
  opacity: 1;
  transform: translateY(0);
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
  max-width: 780px;
  padding: 0 20px;
  text-align: left;
}

/* FAQ Item 스타일 개선 (Interactive) */
.faq-item {
  border-bottom: 1px solid #e5e7eb;
  padding: 24px 0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.faq-item:first-child {
  border-top: 1px solid #e5e7eb;
}

.q {
  display: flex;
  gap: 10px;
  align-items: center;
  font-size: 18px;
  font-weight: 700;
  color: #111827;
  position: relative;
}

/* 화살표 아이콘 */
.arrow-icon {
  margin-left: auto; /* 우측 정렬 */
  width: 24px;
  height: 24px;
  position: relative;
  transition: transform 0.3s ease;
}

/* CSS로 만든 화살표 (V 모양) */
.arrow-icon::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 10px;
  height: 10px;
  border-right: 2px solid #9ca3af;
  border-bottom: 2px solid #9ca3af;
  transform: translate(-50%, -70%) rotate(45deg);
  transition: border-color 0.3s;
}

/* 활성화 시 화살표 회전 및 색상 변경 */
.faq-item.active .arrow-icon {
  transform: rotate(180deg);
}
.faq-item.active .arrow-icon::after {
  border-color: #db1f4b;
}
.faq-item.active .q {
  color: #db1f4b; /* 질문 색상 강조 */
}

/* 답변 영역 (아코디언 애니메이션) */
.a-wrapper {
  overflow: hidden;
  transition: max-height 0.3s ease-out; /* 부드러운 펼침 효과 */
}

.a {
  padding-top: 16px;
  display: flex;
  gap: 10px;
  align-items: baseline;
  font-size: 15px; /* 가독성 위해 약간 키움 */
  color: #4b5563;
  line-height: 1.6;
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
  padding: 18px 52px; /* 좌우 여백 조금 더 줌 */
  border-radius: 999px;
  background: #db1f4b; 
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
  box-shadow: 0 4px 6px -1px rgba(219, 31, 75, 0.3);
  transition: all 0.3s ease;
}

.cta-btn:hover {
  transform: translateY(-2px);
  background: #be123c;
  box-shadow: 0 10px 15px -3px rgba(219, 31, 75, 0.4);
}

/* 펄스 애니메이션 (주목도 향상) */
.pulse-animation {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(219, 31, 75, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(219, 31, 75, 0); }
  100% { box-shadow: 0 0 0 0 rgba(219, 31, 75, 0); }
}

/* Responsive */
@media (max-width: 980px) {
  .steps { grid-template-columns: 1fr; gap: 60px; }
  .title { font-size: 36px; }
  .faq-title { font-size: 32px; }
  .faq { margin-top: 120px; padding-top: 40px; }
  
  /* 모바일에서는 Step 딜레이 줄이거나 제거 */
  .step { transition-delay: 0s !important; }
}
</style>