// src/utils/energy.js
export function calcTdee(p) {
  if (!p) return null

  const gender = String(p.gender ?? "").toLowerCase()
  const weight = Number(p.weight)
  const height = Number(p.height)
  const age = Number(p.age)
  const activity = Number(p.activity_level)

  // 필수값 없으면 계산 불가
  if (![weight, height, age].every(v => Number.isFinite(v) && v > 0)) return null

  let base = 0
  if (gender === "male" || gender === "m") {
    base = 66.47 + 13.75 * weight + 5 * height - 6.76 * age
  } else {
    base = 655.1 + 9.56 * weight + 1.85 * height - 4.68 * age
  }

  const activityMap = { 1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9 }
  const mult = activityMap[activity] ?? 1.2

  return Math.round(base * mult)
}
