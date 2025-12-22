<template>
  <Teleport to="body">
    <div v-if="open" class="backdrop" @click.self="emit('cancel')">
      <div class="modal" role="dialog" aria-modal="true" tabindex="-1" ref="dialogEl">
        <!-- ✅ 스샷처럼 한 줄 중앙: title이 있으면 title, 없으면 message -->
        <h3 class="headline">{{ title || message }}</h3>

        <!-- ✅ title이 있고 message도 있으면, message를 보조문구로(원하면 사용) -->
        <p v-if="title && message" class="sub">{{ message }}</p>

        <div class="actions">
          <button class="btn cancel" type="button" @click="emit('cancel')">
            {{ cancelText }}
          </button>
          <button class="btn confirm" type="button" @click="emit('confirm')">
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { nextTick, ref, watch } from "vue"

const props = defineProps({
  open: { type: Boolean, default: false },
  title: { type: String, default: "" },
  message: { type: String, default: "" },
  confirmText: { type: String, default: "확인" },
  cancelText: { type: String, default: "취소" },
})

const emit = defineEmits(["confirm", "cancel"])
const dialogEl = ref(null)

watch(
  () => props.open,
  async (v) => {
    if (v) {
      await nextTick()
      dialogEl.value?.focus()
    }
  }
)
</script>

<style scoped>
.backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35); /* ✅ 너무 어둡지 않게 */
  display: grid;
  place-items: center;
  z-index: 3000;
  padding: 16px;
}

.modal {
  width: min(420px, 92vw);
  background: #ffffff;
  border-radius: 16px;               /* ✅ 둥글게 */
  border: 1px solid rgba(0, 0, 0, 0.10);
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.25);
  padding: 22px 18px 18px;
  outline: none;
}

.headline {
  margin: 6px 0 0;
  text-align: center;                /* ✅ 중앙 */
  font-size: 15px;
  font-weight: 800;
  color: #111827;
}

.sub {
  margin: 10px 0 0;
  text-align: center;
  font-size: 13px;
  line-height: 1.6;
  color: #6b7280;
}

.actions {
  margin-top: 18px;
  display: flex;
  gap: 12px;
}

.btn {
  flex: 1;                           /* ✅ 좌/우 같은 너비 */
  height: 48px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid transparent;
}

.cancel {
  background: #f3f4f6;               /* ✅ 좌측 회색 */
  color: #374151;
  border-color: rgba(0, 0, 0, 0.06);
}
.cancel:hover { background: #e5e7eb; }

.confirm {
  background: var(--primary-color, #db1f4b); /* ✅ 기존 포인트 색 유지 */
  color: #ffffff;
}
.confirm:hover { background: #c91b42; }
</style>
