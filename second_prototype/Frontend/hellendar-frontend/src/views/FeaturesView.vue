<template>
  <section class="features">
    <!-- Hero -->
    <header class="hero">
      <h1 class="hero-title">헬린더의 주요 기능</h1>
      <p class="hero-subtitle">건강 관리를 위한 모든 기능을 한 곳에서</p>
    </header>

    <!-- Feature Sections -->
    <div class="feature-list">
      <article
        v-for="(f, idx) in featureSections"
        :key="f.key"
        class="feature"
        :class="{ reverse: idx % 2 === 1 }"
        :ref="(el) => (featureRefs[idx] = el)"
      >
        <div class="media">
          <div class="media-inner">
            <img class="media-img" :src="f.image" :alt="f.title + ' 이미지'" />
          </div>
        </div>

        <div class="content">
          <div class="content-title">
            <span class="icon-chip" aria-hidden="true">
              <!-- 간단 아이콘 (inline svg) -->
              <component :is="f.icon" class="icon" />
            </span>
            <h2 class="title">{{ f.title }}</h2>
          </div>

          <p class="desc">{{ f.desc }}</p>

          <ul class="bullets">
            <li v-for="(b, bIdx) in f.bullets" :key="bIdx">{{ b }}</li>
          </ul>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue"

/**
 * 이미지 파일명은 프로젝트에 맞게 수정하세요.
 * 예) /src/assets/features/calendar.png 등
 */
import calendarImg from "@/assets/features_calendar.png"
import foodImg from "@/assets/features_food.png"
import insightImg from "@/assets/features_insight.png"

/* --- Intersection Observer 설정 --- */
const featureRefs = ref([])

onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          // 화면에 동시에 나타나는 요소들에게 순차적인 딜레이 적용
          // (스크롤하여 하나씩 만날 때는 index가 0이므로 즉시 실행됨)
          entry.target.style.animationDelay = `${index * 0.2}s`
          entry.target.classList.add("is-visible")
          
          // 한 번 애니메이션 실행 후 관찰 중지
          observer.unobserve(entry.target)
        }
      })
    },
    {
      threshold: 0.40,
    }
  )

  featureRefs.value.forEach((el) => {
    if (el) observer.observe(el)
  })
})

/* --- 아이콘 컴포넌트(외부 라이브러리 없이 inline) --- */
const IconCalendar = {
  name: "IconCalendar",
  template: `
    <svg viewBox="0 0 24 24" fill="none">
      <path d="M7 3v2M17 3v2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <path d="M4 7h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <path d="M6 5h12a2 2 0 0 1 2 2v13a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2Z" stroke="currentColor" stroke-width="2" />
      <path d="M8 11h3v3H8v-3Zm5 0h3v3h-3v-3Z" fill="currentColor" opacity="0.25"/>
    </svg>
  `,
}

const IconFood = {
  name: "IconFood",
  template: `
    <svg viewBox="0 0 24 24" fill="none">
      <path d="M4 12c0 4.5 3.6 8 8 8s8-3.5 8-8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <path d="M6 12c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="currentColor" stroke-width="2"/>
      <path d="M9.2 10.8c.6-1 1.7-1.8 2.8-1.8s2.2.8 2.8 1.8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>
  `,
}

const IconInsight = {
  name: "IconInsight",
  template: `
    <svg viewBox="0 0 24 24" fill="none">
      <path d="M4 19V5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <path d="M4 19h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <path d="M7 15l3-4 3 2 4-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="7" cy="15" r="1.2" fill="currentColor"/>
      <circle cx="10" cy="11" r="1.2" fill="currentColor"/>
      <circle cx="13" cy="13" r="1.2" fill="currentColor"/>
      <circle cx="17" cy="7" r="1.2" fill="currentColor"/>
    </svg>
  `,
}

/* --- 목업 기반 섹션 데이터 --- */
const featureSections = [
  {
    key: "calendar",
    title: "메인 캘린더",
    desc: "월 단위로 한눈에 보는 건강 기록",
    image: calendarImg,
    icon: IconCalendar,
    bullets: [
      "날짜별 식단/운동/몸무게 기록 여부 뱃지 표시",
      "컨디션 이미지로 그날의 기분 확인",
      "날짜 클릭 시 상세 페이지로 이동",
    ],
  },
  {
    key: "food",
    title: "음식 검색",
    desc: "수천 개 음식 데이터로 빠르게 영양 정보 확인",
    image: foodImg,
    icon: IconFood,
    bullets: [
      "식품명 검색/자동완성으로 빠른 선택",
      "자동으로 탄단지 비율 계산",
      "커스텀 음식 등록 지원",
    ],
  },
  {
    key: "insight",
    title: "통계 & 인사이트",
    desc: "기록이 쌓일수록 더 똑똑해지는 건강 관리",
    image: insightImg,
    icon: IconInsight,
    bullets: [
      "주/월 단위 변화 추이 요약",
      "탄단지/칼로리 목표 대비 달성률",
      "몸무게/운동량 트렌드 확인",
    ],
  },
]
</script>

<style scoped>
.features {
  padding: 110px 0 120px;
}

/* Hero */
.hero {
  text-align: center;
  padding: 30px 0 70px;
}
.hero-title {
  margin: 0;
  font-size: 48px;
  letter-spacing: -0.05em;
  line-height: 1.15;
  color: #111827;
  font-weight: 800;
}
.hero-subtitle {
  margin: 18px 0 0;
  font-size: 15px;
  color: #6b7280;
}

/* Feature list */
.feature-list {
  display: grid;
  gap: 120px; /* 섹션 간 큰 여백(목업 느낌) */
}

/* Each feature block */
.feature {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr; /* 이미지가 조금 더 크게 */
  align-items: center;
  gap: 46px;

  /* 초기 상태: 투명하고 약간 아래에 위치 */
  opacity: 0;
  transform: translate3d(0, 40px, 0);
  /* transition을 사용하지 않고 animation 클래스로 제어합니다 */
}

/* Intersection Observer에 의해 추가되는 클래스 */
.feature.is-visible {
  animation: fadeInDown 1s ease-out forwards;
}

.feature.reverse {
  grid-template-columns: 0.85fr 1.15fr;
}
.feature.reverse .media {
  order: 2;
}
.feature.reverse .content {
  order: 1;
}

/* Media */
.media-inner {
  background: #eef2f6;
  border-radius: 18px;
  padding: 26px;
  box-shadow: 0 18px 40px rgba(17, 24, 39, 0.12);
  border: 1px solid rgba(0, 0, 0, 0.06);
}
.media-img {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 12px;
}

/* Content */
.content-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon-chip {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: rgba(219, 31, 75, 0.12);
  display: grid;
  place-items: center;
  color: #db1f4b;
}
.icon {
  width: 20px;
  height: 20px;
}

.title {
  margin: 0;
  font-size: 26px;
  font-weight: 800;
  color: #111827;
}

.desc {
  margin: 12px 0 0;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.8;
}

.bullets {
  margin: 18px 0 0;
  padding: 0 0 0 18px;
  color: #374151;
  line-height: 1.9;
  font-size: 14px;
}
.bullets li {
  margin: 6px 0;
}

/* fadeInDown 애니메이션 정의 */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translate3d(0, 40px, 0); /* 아래에서 위로 올라오는 느낌으로 변경 (fadeInUp) */
    /* 만약 위에서 아래로 떨어지는 느낌을 원하시면 40px 대신 -40px로 설정하세요 */
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
}

/* Responsive */
@media (max-width: 980px) {
  .features { padding: 80px 0 90px; }
  .hero-title { font-size: 38px; }
  .feature-list { gap: 70px; }

  .feature,
  .feature.reverse {
    grid-template-columns: 1fr;
    gap: 22px;
  }
  .feature.reverse .media,
  .feature.reverse .content {
    order: initial;
  }
}
</style>