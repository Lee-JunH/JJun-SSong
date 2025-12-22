<!-- src/views/HomeView.vue -->
<template>
  <section class="home">
    <!-- Banner (full-bleed) -->
    <section class="banner" aria-label="홈 배너">
      <div
        ref="frameEl"
        class="banner-frame"
        :class="{ dragging: isDragging }"
        :style="{ opacity: fadeOpacity }"
        @pointerdown="onPointerDown"
        @pointermove="onPointerMove"
        @pointerup="onPointerUp"
        @pointercancel="onPointerUp"
        @click.capture="onClickCapture"
      >
        <!-- 슬라이드 트랙 -->
        <div
          class="track"
          :class="{ dragging: isDragging, 'no-anim': noSlideAnim }"
          :style="{ transform: `translateX(${translateX}px)` }"
        >
          <div v-for="(b, i) in banners" :key="i" class="slide">
            <img class="banner-img" :src="b.img" :alt="b.alt" draggable="false" />

            <div class="banner-overlay">
              <h1 class="banner-title">{{ b.title }}</h1>
              <p class="banner-subtitle">{{ b.subtitle }}</p>


            </div>
          </div>
        </div>

        <!-- dots -->
        <div class="dots" aria-label="배너 선택">
          <button
            v-for="(_, i) in banners"
            :key="i"
            class="dot"
            :class="{ active: i === active }"
            type="button"
            @click="go(i)"
            :aria-label="`배너 ${i + 1} 보기`"
          />
        </div>
      </div>
    </section>

    <!-- ✅ 배너 아래: 스크롤 섹션들 -->
    <div class="features-page">
      <!-- (1) 헬린더가 특별한 이유 -->
      <section class="block reveal">
        <header class="block-head">
          <h2 class="block-title">헬린더가 특별한 이유</h2>
          <p class="block-sub">바쁜 현대인을 위한 맞춤형 건강 관리 솔루션</p>
        </header>

        <div class="reason-grid" aria-label="특별한 이유 3가지">
          <article v-for="(r, i) in reasons" :key="i" class="reason-card">
            <div class="img-box">
              <img class="img" :src="r.img" :alt="r.title" />
            </div>
            <h3 class="reason-title">{{ r.title }}</h3>
            <p class="reason-desc">{{ r.desc }}</p>
          </article>
        </div>
      </section>

      <!-- (2) 다음 항목 -->
      <section class="block reveal">
        <header class="block-head">
          <h2 class="block-title">기록부터 분석까지, 한 번에</h2>
          <p class="block-sub">식단 · 운동 · 몸무게 · 컨디션을 끊김 없이 관리하세요.</p>
        </header>

        <div class="next-grid" aria-label="다음 기능 소개">
          <article v-for="(n, i) in nextItems" :key="i" class="next-card">
            <div class="next-icon">
              <img class="next-icon-img" :src="n.icon" :alt="n.title" />
            </div>

            <div class="next-meta">
              <h3 class="next-title">{{ n.title }}</h3>
              <p class="next-desc">{{ n.desc }}</p>

              <ul class="next-bullets">
                <li v-for="(b, j) in n.bullets" :key="j">{{ b }}</li>
              </ul>
            </div>
          </article>
        </div>
      </section>

      <!-- (3) CTA -->
      <section class="block reveal">
        <div class="cta-box">
          <h2 class="cta-title">오늘부터 헬린더로 시작해볼까요?</h2>
          <p class="cta-sub">3단계로 간편하게 시작하고, 기록을 습관으로 만들어요.</p>

          <!-- ✅ 로그인 상태 -->
          <div v-if="auth.me" class="cta-actions">
            <RouterLink class="cta-btn" to="/my">마이캘린더 시작하기</RouterLink>
          </div>

          <!-- ✅ 비로그인 상태 -->
          <div v-else class="cta-actions">
            <RouterLink class="cta-btn" to="/signup">회원가입하고 시작하기</RouterLink>
            <RouterLink class="cta-btn ghost" to="/start">시작하기</RouterLink>
          </div>
        </div>
      </section>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from "vue"
import { useAuthStore } from "@/stores/auth"

const auth = useAuthStore()

/* =======================
   Banner 이미지 (본인 assets에 맞게 수정)
======================= */
import banner1 from "@/assets/home_banner_1.png"
import banner2 from "@/assets/home_banner_2.png"

const banners = [
  {
    img: banner1,
    alt: "건강 식재료 배너 이미지",
    title: "간편한 기록,\n스마트한 관리",
    subtitle: "바쁜 일상 속에서도 쉽게 건강을 챙기세요.",
  },
  {
    img: banner2,
    alt: "헬린더 캘린더 미리보기 배너 이미지",
    title: "건강한 하루,\n헬린더와 함께",
    subtitle: "식단, 운동, 컨디션을 한눈에 기록하고 관리하세요.",
  },
]

/* =======================
   아래 스크롤 섹션 이미지 (파일명/경로 수정)
======================= */
import reason1 from "@/assets/reason_1.png"
import reason2 from "@/assets/reason_2.png"
import reason3 from "@/assets/reason_3.png"

import nextIcon1 from "@/assets/icons/calendar.png"
import nextIcon2 from "@/assets/icons/search.png"
import nextIcon3 from "@/assets/icons/report.png"

const reasons = [
  { img: reason1, title: "한눈에 보는 캘린더", desc: "월 단위로 기록을 모아보고, 한 달 건강 습관을 빠르게 파악해요." },
  { img: reason2, title: "빠른 음식 검색", desc: "내장 영양 DB로 음식 검색 후 칼로리·영양소를 자동 계산해요." },
  { img: reason3, title: "스마트 영양 분석", desc: "탄단지 비율을 확인하고, 과다 섭취 항목은 경고로 알려줘요." },
]

const nextItems = [
  {
    icon: nextIcon1,
    title: "메인 캘린더 기록",
    desc: "하루 기록을 한 화면에서 관리합니다.",
    bullets: ["날짜별 식단/운동/몸무게 표시", "클릭 시 상세 페이지 이동", "컨디션·영양제 아이콘 표시"],
  },
  {
    icon: nextIcon2,
    title: "음식 검색 & 커스텀 등록",
    desc: "검색부터 기록까지 흐름이 끊기지 않아요.",
    bullets: ["DB 검색으로 즉시 기록", "커스텀 음식 등록 지원", "영양소 자동 합산"],
  },
  {
    icon: nextIcon3,
    title: "차트 기반 리포트",
    desc: "변화를 숫자와 그래프로 확인합니다.",
    bullets: ["몸무게 추세", "탄단지 비율", "섭취량 과다/부족 알림"],
  },
]

/* =======================
   Banner 상태
======================= */
const active = ref(0)

const frameEl = ref(null)
const frameW = ref(0)

const isDragging = ref(false)
const dragStartX = ref(0)
const dragOffset = ref(0)
const moved = ref(false)

const fadeOpacity = ref(1)
const noSlideAnim = ref(false)

const translateX = computed(() => -active.value * frameW.value + dragOffset.value)

function measure() {
  if (!frameEl.value) return
  frameW.value = frameEl.value.clientWidth || 0
}

function clampIndex(i) {
  if (i < 0) return 0
  if (i > banners.length - 1) return banners.length - 1
  return i
}

/* =======================
   자동 전환(페이드)
======================= */
let autoTimer = null
let fadeTimer1 = null
let fadeTimer2 = null
const AUTO_INTERVAL = 4500
const FADE_MS = 420

function clearFadeTimers() {
  if (fadeTimer1) window.clearTimeout(fadeTimer1)
  if (fadeTimer2) window.clearTimeout(fadeTimer2)
  fadeTimer1 = null
  fadeTimer2 = null
}
function startAuto() {
  stopAuto()
  autoTimer = window.setInterval(() => {
    if (isDragging.value) return

    clearFadeTimers()

    // 1) 페이드 아웃
    fadeOpacity.value = 0

    // 2) 완전히 흐려진 뒤, transition 없이 인덱스 점프
    fadeTimer1 = window.setTimeout(async () => {
      noSlideAnim.value = true               // ✅ transform transition OFF (유지!)
      active.value = (active.value + 1) % banners.length
      dragOffset.value = 0

      await nextTick()

      // 3) 다음 프레임에 페이드 인만 시작
      requestAnimationFrame(() => {
        fadeOpacity.value = 1
      })

      // 4) ✅ 페이드 인이 끝난 뒤에만 transition을 다시 켠다
      fadeTimer2 = window.setTimeout(() => {
        noSlideAnim.value = false
      }, FADE_MS + 30) // 약간의 버퍼(10~50ms) 권장

    }, FADE_MS)
  }, AUTO_INTERVAL)
}


function stopAuto() {
  if (autoTimer) window.clearInterval(autoTimer)
  autoTimer = null
  clearFadeTimers()
}

/* dot 클릭 */
function go(i) {
  active.value = clampIndex(i)
  dragOffset.value = 0
  startAuto()
}

/* 드래그 */
function onPointerDown(e) {
  isDragging.value = true
  moved.value = false
  dragStartX.value = e.clientX
  dragOffset.value = 0

  stopAuto()
  try {
    e.currentTarget.setPointerCapture(e.pointerId)
  } catch {}
}

function onPointerMove(e) {
  if (!isDragging.value) return
  const dx = e.clientX - dragStartX.value
  dragOffset.value = dx
  if (Math.abs(dx) > 6) moved.value = true
}

function onPointerUp() {
  if (!isDragging.value) return

  const dx = dragOffset.value
  const threshold = Math.max(60, frameW.value * 0.18)

  if (dx <= -threshold) active.value = clampIndex(active.value + 1)
  else if (dx >= threshold) active.value = clampIndex(active.value - 1)

  dragOffset.value = 0
  isDragging.value = false

  fadeOpacity.value = 1
  startAuto()
}

function onClickCapture(e) {
  if (moved.value) {
    e.preventDefault()
    e.stopPropagation()
    moved.value = false
  }
}

/* 리사이즈 */
function onResize() {
  measure()
}

/* =======================
   스크롤 Reveal(IntersectionObserver)
======================= */
let io = null

function setupReveal() {
  const els = Array.from(document.querySelectorAll(".reveal"))

  io = new IntersectionObserver(
    (entries) => {
      entries.forEach((ent) => {
        if (ent.isIntersecting) {
          ent.target.classList.add("is-visible")
          io?.unobserve(ent.target)
        }
      })
    },
    { threshold: 0.40 }
  )

  els.forEach((el) => io.observe(el))
}

/* 라이프사이클 */
onMounted(async () => {
  await nextTick()
  measure()
  window.addEventListener("resize", onResize)
  startAuto()
  setupReveal()
})

onBeforeUnmount(() => {
  window.removeEventListener("resize", onResize)
  stopAuto()
  io?.disconnect()
  io = null
})
</script>

<style scoped>
/* =======================
   Banner
======================= */
.banner {
  width: 100vw;
  margin-left: calc(50% - 50vw);
}

.banner-frame {
  position: relative;
  width: 100%;
  height: clamp(360px, 52vh, 520px);
  overflow: hidden;
  background: #f3f4f6;
  transition: opacity 420ms ease;
  touch-action: pan-y;
}

.banner-frame.dragging {
  transition: none;
}

.track {
  height: 100%;
  display: flex;
  will-change: transform;
  transition: transform 300ms ease;
}

.track.dragging {
  transition: none;
}
.track.no-anim {
  transition: none !important;
}

.slide {
  position: relative;
  flex: 0 0 100%;
  height: 100%;
}

.banner-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  user-select: none;
}

.banner-overlay {
  position: absolute;
  left: min(80px, 6vw);
  top: 50%;
  transform: translateY(-50%);
  max-width: 560px;
  color: rgba(17, 24, 39, 0.92);
}

.banner-title {
  margin: 0;
  font-size: clamp(34px, 4vw, 56px);
  font-weight: 600;
  letter-spacing: -0.05em;
  line-height: 1.08;
  white-space: pre-line;
  text-shadow: 0 2px 16px rgba(255, 255, 255, 0.45);
}

.banner-subtitle {
  margin: 18px 0 0;
  font-size: 14px;
  color: rgba(55, 65, 81, 0.78);
  line-height: 1.7;
}

/* 배너 내부 버튼을 쓰는 경우 */
.banner-cta {
  display: flex;
  gap: 12px;
  margin-top: 18px;
}

.btn {
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.12);
  background: rgba(255, 255, 255, 0.9);
  color: #111827;
  font-weight: 800;
  text-decoration: none;
  transition: transform 0.15s ease, filter 0.15s ease;
}
.btn:hover {
  transform: translateY(-1px);
  filter: brightness(0.98);
}
.btn.ghost {
  background: rgba(255, 255, 255, 0.72);
}

/* dots */
.dots {
  position: absolute;
  left: 50%;
  bottom: 16px;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  align-items: center;
}

.dot {
  width: 9px;
  height: 9px;
  border-radius: 999px;
  border: 1px solid rgba(17, 24, 39, 0.45);
  background: rgba(255, 255, 255, 0.65);
  cursor: pointer;
  padding: 0;
}
.dot.active {
  background: rgba(17, 24, 39, 0.9);
  border-color: rgba(17, 24, 39, 0.9);
}

@media (max-width: 900px) {
  .banner-overlay {
    left: 20px;
    right: 20px;
    max-width: none;
  }
}

/* =======================
   아래 섹션(스크롤)
======================= */
.features-page {
  width: 100%;
}

.block {
  padding: 110px 0;
}

/* Reveal */
.reveal {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}
.reveal.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.block-head {
  text-align: center;
  margin-bottom: 70px;
}
.block-title {
  margin: 0;
  font-size: 44px;
  font-weight: 800;
  letter-spacing: -0.04em;
  color: #111827;
}
.block-sub {
  margin: 16px 0 0;
  font-size: 14px;
  color: #6b7280;
}

/* 3칸 카드 */
.reason-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 34px;
  align-items: start;
}
.reason-card {
  text-align: center;
}

.img {
  width: 90%;
  height: 90%;
  object-fit: contain;
}
.reason-title {
  margin: 26px 0 10px;
  font-size: 18px;
  font-weight: 800;
  color: #111827;
}
.reason-desc {
  margin: 0 auto;
  max-width: 320px;
  font-size: 12px;
  line-height: 1.8;
  color: #6b7280;
}

/* 다음 항목 */
.next-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 22px;
  max-width: 980px;
  margin: 0 auto;
}
.next-card {
  display: grid;
  grid-template-columns: 54px 1fr;
  gap: 16px;
  padding: 22px 22px;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.06);
}
.next-icon {
  width: 54px;
  height: 54px;
  border-radius: 12px;
  background: rgba(219, 31, 75, 0.08);
  display: grid;
  place-items: center;
}
.next-icon-img {
  width: 26px;
  height: 26px;
  object-fit: contain;
}
.next-title {
  margin: 0;
  font-size: 16px;
  font-weight: 800;
  color: #111827;
}
.next-desc {
  margin: 8px 0 10px;
  font-size: 13px;
  color: #6b7280;
  line-height: 1.7;
}
.next-bullets {
  margin: 0;
  padding-left: 18px;
  color: #374151;
  font-size: 13px;
  line-height: 1.8;
}

/* CTA (배너의 .cta와 충돌 방지 위해 이름 변경) */
.cta-box {
  max-width: 980px;
  margin: 0 auto;
  padding: 54px 26px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  background: #fff;
  text-align: center;
}
.cta-title {
  margin: 0;
  font-size: 26px;
  font-weight: 900;
  letter-spacing: -0.03em;
}
.cta-sub {
  margin: 14px 0 0;
  color: #6b7280;
  font-size: 14px;
}
.cta-actions {
  margin-top: 26px;
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}
.cta-btn {
  text-decoration: none;
  padding: 12px 18px;
  border-radius: 999px;
  background: #db1f4b;
  color: #fff;
  font-weight: 500;
  border: 1px solid transparent;
}
.cta-btn.ghost {
  background: #fff;
  color: #db1f4b;
  border-color: rgba(219, 31, 75, 0.35);
}

@media (max-width: 980px) {
  .block {
    padding: 84px 0;
  }
  .block-title {
    font-size: 34px;
  }
  .reason-grid {
    grid-template-columns: 1fr;
    gap: 22px;
  }
  .img-box {
    max-width: 520px;
    margin: 0 auto;
  }
}

@media (prefers-reduced-motion: reduce) {
  .banner-frame {
    transition: none;
  }
  .track {
    transition: none;
  }
  .reveal,
  .reveal.is-visible {
    transition: none;
    transform: none;
  }
}
</style>
