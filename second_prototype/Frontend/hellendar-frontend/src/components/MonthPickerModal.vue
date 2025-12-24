<template>
  <div class="backdrop" @click.self="$emit('close')">
    <div class="modal">
      <button class="close" type="button" @click="$emit('close')" aria-label="닫기">×</button>

      <div class="top">
        <button class="nav" type="button" @click="year--" aria-label="이전 해">‹</button>
        <div class="year">{{ year }}</div>
        <button class="nav" type="button" @click="year++" aria-label="다음 해">›</button>
      </div>

      <div class="grid">
        <button
          v-for="m in 12"
          :key="m"
          type="button"
          class="month"
          :class="{
            disabled: !isEnabled(year, m),
            selected: isSelected(year, m),
            enabled: isEnabled(year, m),
          }"
          :disabled="!isEnabled(year, m)"
          @click="selectMonth(year, m)"
        >
          {{ m }}월
        </button>
      </div>

      <p class="hint">기록이 있는 달만 선택할 수 있어요.</p>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue"

const props = defineProps({
  modelValue: { type: String, required: true }, // "YYYY-MM"
  availableMonths: { type: Array, default: () => [] }, // ["2025-01", ...]
})

const emit = defineEmits(["update:modelValue", "select", "close"])

const set = computed(() => new Set(props.availableMonths))

const year = ref(Number(props.modelValue.slice(0, 4)))

watch(
  () => props.modelValue,
  (v) => {
    if (v) year.value = Number(v.slice(0, 4))
  }
)

function pad2(n) {
  return String(n).padStart(2, "0")
}

function ym(y, m) {
  return `${y}-${pad2(m)}`
}

function isEnabled(y, m) {
  return set.value.has(ym(y, m))
}

function isSelected(y, m) {
  return props.modelValue === ym(y, m)
}

function selectMonth(y, m) {
  const v = ym(y, m)
  emit("update:modelValue", v)
  emit("select", v)
  emit("close")
}
</script>

<style scoped>
.backdrop{
  position: fixed; inset: 0;
  background: rgba(0,0,0,.35);
  backdrop-filter: blur(4px);
  display: grid; place-items: center;
  z-index: 3000;
  padding: 20px;
}

.modal{
  width: min(420px, 92vw);
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 18px 60px rgba(0,0,0,.18);
  padding: 18px 18px 14px;
  position: relative;
}

.close{
  position:absolute; top:10px; right:12px;
  border:0; background: transparent;
  font-size: 20px; cursor:pointer;
  color:#9ca3af;
}
.close:hover{ color:#374151; }

.top{
  display:flex; align-items:center; justify-content:center;
  gap: 14px;
  padding: 8px 0 14px;
}

.year{
  font-weight: 800;
  font-size: 18px;
  color:#111827;
  min-width: 90px;
  text-align:center;
}

.nav{
  border:0;
  background:#f3f4f6;
  width: 34px; height: 34px;
  border-radius: 10px;
  cursor:pointer;
  font-size: 18px;
  color:#374151;
}
.nav:hover{ background:#e5e7eb; }

.grid{
  display:grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  padding: 4px 0 10px;
}

.month{
  border: 1px solid #e5e7eb;
  background:#fff;
  border-radius: 12px;
  padding: 10px 0;
  cursor:pointer;
  font-weight: 700;
  color:#374151;
}

.month.enabled:hover{
  border-color:#db1f4b;
  color:#db1f4b;
}

.month.selected{
  background: #fff0f3;
  border-color:#db1f4b;
  color:#db1f4b;
}

.month.disabled{
  opacity:.35;
  cursor:not-allowed;
}

.hint{
  margin: 6px 0 0;
  font-size: 12px;
  color:#9ca3af;
  text-align:center;
}
</style>
