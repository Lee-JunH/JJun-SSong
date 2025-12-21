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
          <p class="step-desc">기본 정보와 건강 목표를 입력하세요.</p>
        </div>
      </article>

      <article class="step">
        <div class="art">
          <img class="art-img" :src="start3" alt="STEP 3 첫 기록 시작 안내 이미지" />
        </div>
        <div class="meta">
          <div class="step-no">STEP 3</div>
          <div class="step-title">첫 기록 시작</div>
          <p class="step-desc">오늘의 식단과 운동을 기록해보세요.</p>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
// 확장자(.png/.jpg/.svg)는 실제 파일에 맞춰 수정하세요.
import start1 from "@/assets/start_1.png"
import start2 from "@/assets/start_2.png"
import start3 from "@/assets/start_3.png"
</script>


<style scoped>
.start {
  /* App.vue의 main padding이 30px이라서, Start 화면처럼 크게 쓰고 싶으면 여기서 추가로 확보 */
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
  overflow: hidden; /* 이미지가 넘칠 때 깔끔하게 */
}

.art-img {
  width: 100%;
  height: 100%;
  object-fit: contain; /* 전체가 보이게(잘림 없음) */
  /* 만약 "프레임을 꽉 채우고 잘려도 된다"면 cover로 변경 */
  /* object-fit: cover; */
}
.meta { margin-top: 24px; }
.step-no { font-size: 32px; font-weight: 800; color: #db1f4b; font-style: "AritaDotumKR-Bold";}
.step-title { margin-top: 12px; font-size: 20px; font-weight: 800; }
.step-desc { margin: 14px auto 0; max-width: 360px; color: #6b7280; line-height: 1.7; font-size: 14px; }

@media (max-width: 980px) {
  .steps { grid-template-columns: 1fr; gap: 44px; }
  .title { font-size: 40px; }
}
</style>
