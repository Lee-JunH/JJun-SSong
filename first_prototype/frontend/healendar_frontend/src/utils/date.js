export function pad2(n) {
  return String(n).padStart(2, "0")
}

export function formatDate(y, m, d) {
  return `${y}-${pad2(m)}-${pad2(d)}`
}

export function monthKey(dateObj) {
  const y = dateObj.getFullYear()
  const m = dateObj.getMonth() + 1
  return `${y}-${pad2(m)}`
}

/**
 * 월 캘린더(6주 x 7일) 매트릭스 생성
 * - 반환: [{ date: Date, inMonth: boolean }...] 42개
 */
export function buildMonthGrid(year, month1to12) {
  const first = new Date(year, month1to12 - 1, 1)
  const firstDay = first.getDay() // 0=Sun
  const start = new Date(year, month1to12 - 1, 1 - firstDay)

  const grid = []
  for (let i = 0; i < 42; i++) {
    const d = new Date(start)
    d.setDate(start.getDate() + i)
    grid.push({
      date: d,
      inMonth: d.getMonth() === (month1to12 - 1),
    })
  }
  return grid
}
