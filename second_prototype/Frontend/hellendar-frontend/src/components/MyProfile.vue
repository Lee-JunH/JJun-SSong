<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="profile-card fade-in-up">
      <button type="button" class="close-btn" @click="$emit('close')" aria-label="닫기">
        ✕
      </button>

      <header class="header">
        <div class="avatar-circle">
          <span class="avatar-emoji">🐣</span>
        </div>
        <h1 class="title">프로필 설정</h1>
        <p class="subtitle">
          더 정확한 분석을 위해<br />
          회원님의 정보를 알려주세요!
        </p>
      </header>

      <form class="form-body" @submit.prevent="saveProfile">
        <!-- 1. 성별 선택 -->
        <div class="form-group">
          <label class="label">성별</label>
          <div class="gender-toggle">
            <button
              type="button"
              class="gender-btn"
              :class="{ active: localForm.gender === 'male' }"
              @click="localForm.gender = 'male'"
            >
              <span class="icon">👦</span> 남성
            </button>
            <button
              type="button"
              class="gender-btn"
              :class="{ active: localForm.gender === 'female' }"
              @click="localForm.gender = 'female'"
            >
              <span class="icon">👧</span> 여성
            </button>
          </div>
        </div>

        <!-- 2. 나이 & 키 -->
        <div class="row-2">
          <div class="form-group">
            <label class="label" for="age">나이</label>
            <div class="input-wrapper">
              <input
                id="age"
                type="number"
                v-model="localForm.age"
                placeholder="0"
                class="input-box"
              />
              <span class="unit">세</span>
            </div>
          </div>
          <div class="form-group">
            <label class="label" for="height">키</label>
            <div class="input-wrapper">
              <input
                id="height"
                type="number"
                v-model="localForm.height"
                placeholder="0"
                class="input-box"
              />
              <span class="unit">cm</span>
            </div>
          </div>
        </div>

        <!-- 3. 체중 관리 섹션 -->
        <div class="weight-section">
          <label class="label">체중 기록</label>
          <div class="weight-grid">
            <div class="weight-item">
              <span class="sub-label">시작</span>
              <div class="input-wrapper sm">
                <input
                  type="number"
                  v-model="localForm.startWeight"
                  placeholder="0"
                  class="input-box"
                />
                <span class="unit">kg</span>
              </div>
            </div>
            <div class="weight-item highlight">
              <span class="sub-label">현재</span>
              <div class="input-wrapper sm">
                <input
                  type="number"
                  v-model="localForm.weight"
                  placeholder="0"
                  class="input-box bold"
                />
                <span class="unit">kg</span>
              </div>
            </div>
            <div class="weight-item">
              <span class="sub-label">목표</span>
              <div class="input-wrapper sm">
                <input
                  type="number"
                  v-model="localForm.goalWeight"
                  placeholder="0"
                  class="input-box"
                />
                <span class="unit">kg</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 4. 활동량 선택 -->
        <div class="form-group">
          <label class="label" for="activity">평소 활동량</label>
          <div class="select-wrapper">
            <select id="activity" v-model="localForm.activityLevel" class="select-box">
              <option value="" disabled>활동량을 선택해주세요</option>
              <option v-for="opt in activityOptions" :key="opt.value" :value="opt.value">
                {{ opt.emoji }} {{ opt.label }}
              </option>
            </select>
            <span class="arrow-icon">▼</span>
          </div>
          <p class="helper-text" v-if="currentActivityDesc">
            {{ currentActivityDesc }}
          </p>
        </div>

        <!-- 저장 버튼 -->
        <div class="action-area">
          <button type="submit" class="save-btn">
            저장하고 시작하기
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineEmits, defineProps, onMounted } from 'vue'

const props = defineProps({
  initialData: {
    type: Object,
    default: () => null
  }
})

const emit = defineEmits(['save', 'close'])

// 폼 데이터 (props로 받은 데이터가 있으면 초기값으로 사용)
const localForm = ref({
  gender: 'female',
  age: null,
  height: null,
  weight: null,
  startWeight: null,
  goalWeight: null,
  activityLevel: ''
})

onMounted(() => {
  if (props.initialData) {
    localForm.value = { ...props.initialData }
  }
})

const activityOptions = [
  { value: 1, emoji: '🛋️', label: '거의 없음 (숨쉬기 운동만)', desc: '앉아서 일하는 시간이 대부분이에요.' },
  { value: 2, emoji: '🚶', label: '가벼운 활동 (주 1-3회)', desc: '이동이 잦거나 가벼운 운동을 해요.' },
  { value: 3, emoji: '🏃', label: '보통 활동 (주 3-5회)', desc: '규칙적으로 운동을 즐기는 편이에요.' },
  { value: 4, emoji: '🔥', label: '매우 활동적 (주 6-7회)', desc: '격렬한 운동이나 육체 노동을 많이 해요.' },
  { value: 5, emoji: '🏋️', label: '선수급 활동 (매일 2회 이상)', desc: '전문 운동선수 수준의 활동량이에요.' }
]

const currentActivityDesc = computed(() => {
  const selected = activityOptions.find(o => o.value === localForm.value.activityLevel)
  return selected ? selected.desc : '라이프스타일에 맞는 활동량을 골라주세요.'
})

function saveProfile() {
  // 간단한 유효성 검사 (예시)
  if (!localForm.value.height || !localForm.value.weight) {
    alert("키와 몸무게는 필수입니다!")
    return
  }
  emit('save', localForm.value)
}
</script>

<style scoped>
/* 모달 백드롭 */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

/* 모달 카드 (기존 스타일 유지하되 max-height 추가) */
.profile-card {
  width: 100%;
  max-width: 420px;
  max-height: 90vh;
  overflow-y: auto;
  background: #ffffff;
  border-radius: 32px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  padding: 40px 32px;
  position: relative;
  /* 스크롤바 숨기기 */
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.profile-card::-webkit-scrollbar {
  display: none;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: none;
  border: none;
  font-size: 20px;
  color: #9ca3af;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background 0.2s;
}
.close-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

/* 애니메이션 */
.fade-in-up {
  animation: fadeInUp 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}
@keyframes fadeInUp {
  to { opacity: 1; transform: translateY(0) scale(1); }
}

/* --- 기존 내부 스타일 복사 --- */
.header { text-align: center; margin-bottom: 24px; }
.avatar-circle {
  width: 72px; height: 72px; background: #ffeef2; border-radius: 50%;
  margin: 0 auto 12px; display: flex; align-items: center; justify-content: center;
  font-size: 32px; box-shadow: 0 6px 12px rgba(219, 31, 75, 0.1);
}
.title { font-size: 22px; font-weight: 800; color: #1f2937; margin: 0; }
.subtitle { margin-top: 6px; font-size: 13px; color: #6b7280; line-height: 1.5; }

.form-body { display: flex; flex-direction: column; gap: 20px; }
.label { display: block; font-size: 13px; font-weight: 700; color: #374151; margin-bottom: 6px; }

.gender-toggle { display: flex; background: #f3f4f6; padding: 4px; border-radius: 14px; }
.gender-btn {
  flex: 1; border: none; background: transparent; padding: 10px; border-radius: 10px;
  font-weight: 600; color: #9ca3af; cursor: pointer; transition: all 0.2s;
  display: flex; align-items: center; justify-content: center; gap: 6px; font-size: 14px;
}
.gender-btn.active { background: #fff; color: #db1f4b; box-shadow: 0 2px 6px rgba(0,0,0,0.06); }

.row-2 { display: flex; gap: 12px; }
.row-2 .form-group { flex: 1; }

.input-wrapper { position: relative; display: flex; align-items: center; }
.input-box {
  width: 100%; padding: 12px 14px; padding-right: 36px; font-size: 15px;
  border: 2px solid #f3f4f6; background: #f9fafb; border-radius: 14px;
  color: #111827; outline: none; transition: all 0.2s;
}
.input-box:focus { background: #fff; border-color: #db1f4b; }
.unit { position: absolute; right: 14px; font-size: 13px; color: #9ca3af; pointer-events: none; }

.weight-section { background: #fffbfc; border: 1px solid #ffe4e8; border-radius: 18px; padding: 16px; }
.weight-grid { display: grid; grid-template-columns: 1fr 1.2fr 1fr; gap: 10px; align-items: end; }
.weight-item { text-align: center; }
.sub-label { display: block; font-size: 11px; color: #6b7280; margin-bottom: 4px; }
.weight-item.highlight .sub-label { color: #db1f4b; font-weight: 700; }
.input-wrapper.sm .input-box { padding: 8px 6px; padding-right: 26px; text-align: center; font-size: 14px; }
.input-wrapper.sm .input-box.bold { font-weight: 700; color: #db1f4b; background: #fff; border-color: #ffe4e8; }
.input-wrapper.sm .unit { right: 6px; font-size: 11px; }

.select-wrapper { position: relative; }
.select-box {
  width: 100%; padding: 12px 14px; font-size: 14px; border: 2px solid #f3f4f6;
  background: #f9fafb; border-radius: 14px; color: #1f2937; appearance: none;
}
.select-box:focus { border-color: #db1f4b; background: #fff; }
.arrow-icon { position: absolute; right: 14px; top: 50%; transform: translateY(-50%); font-size: 11px; color: #9ca3af; }
.helper-text {
  margin-top: 6px; font-size: 12px; color: #db1f4b; background: #fff0f3;
  padding: 6px 10px; border-radius: 6px; display: inline-block;
}

.action-area { margin-top: 8px; }
.save-btn {
  width: 100%; padding: 14px; border: none; border-radius: 999px;
  background: linear-gradient(90deg, #db1f4b, #f03e67); color: white;
  font-size: 15px; font-weight: 700; cursor: pointer;
  box-shadow: 0 4px 12px rgba(219, 31, 75, 0.3); transition: transform 0.1s;
}
.save-btn:active { transform: scale(0.98); }

@media (max-width: 400px) {
  .profile-card { padding: 30px 20px; }
}
</style>