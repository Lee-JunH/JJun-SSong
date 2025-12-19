<template>
  <div style="border:1px solid #3333; padding:10px; border-radius:10px; margin-top:10px;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <strong>{{ meal.meal.meal_type }}</strong>
      <span style="opacity:.7;">{{ meal.items.length }} items</span>
    </div>

    <ul style="margin-top:8px;">
      <li v-for="it in meal.items" :key="it.id" style="display:flex; justify-content:space-between; gap:8px;">
        <span>
          {{ label(it) }} / {{ it.amount_g }}g / {{ it.kcal }}kcal
        </span>
        <button type="button" @click="$emit('deleteItem', it.id)">삭제</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineEmits(["deleteItem"])
const props = defineProps({ meal: Object })

function label(it) {
  // 백엔드에서 food/custom_food 이름을 직접 안 내려주므로
  // MVP에서는 "ID 기반"으로 보여주거나,
  // 개선: MealItemSerializer에 name 필드를 추가하도록 백엔드 확장 권장
  if (it.food) return `Food#${it.food}`
  if (it.custom_food) return `CustomFood#${it.custom_food}`
  return "Item"
}
</script>
