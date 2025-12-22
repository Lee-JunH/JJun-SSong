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
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from "vue"

// 파일명/확장자는 실제 assets에 맞춰 수정
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

/* ---------- 상태 ---------- */
const active = ref(0)

const frameEl = ref(null)
const frameW = ref(0)

const isDragging = ref(false)
const dragStartX = ref(0)
const dragOffset = ref(0)      // px
const moved = ref(false)       // 드래그 중 실제 이동했는지(클릭 방지용)

const fadeOpacity = ref(1)     // 자동 전환 페이드 (1 -> 0 -> 1)

const noSlideAnim = ref(false)

/* ---------- 트랙 위치(px) ---------- */
const translateX = computed(() => {
  // 기본 위치: -active * frameW, 드래그 중이면 dragOffset 만큼 보정
  return -active.value * frameW.value + dragOffset.value
})

/* ---------- 리사이즈 대응 ---------- */
function measure() {
  if (!frameEl.value) return
  frameW.value = frameEl.value.clientWidth || 0
}

function clampIndex(i) {
  if (i < 0) return 0
  if (i > banners.length - 1) return banners.length - 1
  return i
}

/* ---------- 자동 전환(페이드) ---------- */
let autoTimer = null
let fadeTimer1 = null
let fadeTimer2 = null
const AUTO_INTERVAL = 4500
const FADE_MS = 420  // 페이드 아웃/인 시간

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

    // 2) 완전히 흐려진 뒤, "슬라이드 애니메이션 없이" 다음 인덱스로 점프
    fadeTimer1 = window.setTimeout(async () => {
      noSlideAnim.value = true          // ✅ transform transition OFF
      active.value = (active.value + 1) % banners.length
      dragOffset.value = 0

      await nextTick()                  // DOM 반영

      // 3) 다음 프레임에 애니메이션 다시 켠 뒤 페이드 인
      requestAnimationFrame(() => {
        noSlideAnim.value = false       // ✅ transform transition ON (드래그/수동용)
        fadeOpacity.value = 1
      })
    }, FADE_MS)
  }, AUTO_INTERVAL)
}

function stopAuto() {
  if (autoTimer) window.clearInterval(autoTimer)
  autoTimer = null
  clearFadeTimers()
}

/* ---------- dot 클릭 ---------- */
function go(i) {
  // dot 클릭은 “슬라이드 이동” (원하면 이 부분도 페이드로 바꿀 수 있어요)
  active.value = clampIndex(i)
  dragOffset.value = 0

  // 클릭 이후 자동 타이머 리셋
  startAuto()
}

/* ---------- 드래그 슬라이딩 ---------- */
function onPointerDown(e) {
  // 링크/버튼 클릭도 있어야 해서, drag가 “조금이라도 움직이면” 클릭을 막는 방식
  isDragging.value = true
  moved.value = false
  dragStartX.value = e.clientX
  dragOffset.value = 0

  stopAuto()

  // 포인터 캡처(드래그 중 포인터가 밖으로 나가도 이벤트 유지)
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
  const threshold = Math.max(60, frameW.value * 0.18) // 스냅 기준

  // 다음/이전 결정
  if (dx <= -threshold) active.value = clampIndex(active.value + 1)
  else if (dx >= threshold) active.value = clampIndex(active.value - 1)

  // 스냅(원위치/다음 위치로) → dragOffset 0으로
  dragOffset.value = 0
  isDragging.value = false

  // 드래그 후 자동 전환 재개
  fadeOpacity.value = 1
  startAuto()
}

// 드래그로 이동했으면 배너 안의 링크 클릭이 안 되게(의도치 않은 클릭 방지)
function onClickCapture(e) {
  if (moved.value) {
    e.preventDefault()
    e.stopPropagation()
    moved.value = false
  }
}

/* ---------- 라이프사이클 ---------- */
function onResize() {
  measure()
}

onMounted(async () => {
  await nextTick()
  measure()
  window.addEventListener("resize", onResize)
  startAuto()
})

onBeforeUnmount(() => {
  window.removeEventListener("resize", onResize)
  stopAuto()
})
</script>

<style scoped>
.banner {
  width: 100vw;
  margin-left: calc(50% - 50vw);
}

/* 프레임 */
.banner-frame {
  position: relative;
  width: 100%;
  height: clamp(360px, 52vh, 520px);
  overflow: hidden;
  background: #f3f4f6;

  /* 자동 전환은 페이드 */
  transition: opacity 420ms ease;
  touch-action: pan-y; /* 세로 스크롤은 허용 + 가로 드래그는 우리가 처리 */
}

.banner-frame.dragging {
  transition: none; /* 드래그 중에는 페이드 전환 끊기 */
}

/* 트랙 */
.track {
  height: 100%;
  display: flex;
  will-change: transform;
  transition: transform 300ms ease; /* 스냅 애니메이션 */
}

.track.dragging {
  transition: none; /* 드래그 중엔 즉시 따라오게 */
}
.track.no-anim {
  transition: none !important; /* ✅ 자동 전환 점프 시 슬라이딩 방지 */
}


/* 슬라이드 */
.slide {
  position: relative;
  flex: 0 0 100%;
  height: 100%;
}

/* 이미지 */
.banner-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  user-select: none;
}

/* 오버레이 */
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

/* CTA */
.cta {
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

/* Responsive */
@media (max-width: 900px) {
  .banner-overlay {
    left: 20px;
    right: 20px;
    max-width: none;
  }
}

/* 모션 최소화 선호 */
@media (prefers-reduced-motion: reduce) {
  .banner-frame { transition: none; }
  .track { transition: none; }
}
</style>
