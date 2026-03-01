import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/** 将月龄转换为可读文本 */
export function formatAge(months: number): string {
  if (months < 12) return `${months}个月`
  const years = Math.floor(months / 12)
  const remainMonths = months % 12
  return remainMonths > 0 ? `${years}岁${remainMonths}个月` : `${years}岁`
}

/** 根据孩子月龄获取对应年龄段标签 */
export function getAgeGroup(months: number): string {
  if (months <= 12) return '0–1岁'
  if (months <= 36) return '2–3岁'
  if (months <= 72) return '4–6岁'
  if (months <= 108) return '7–9岁'
  return '10–12岁'
}

/** 判断当前是否在营业时间内 */
export function isOpenNow(openingHoursToday: string | null): boolean {
  if (!openingHoursToday) return false
  const now = new Date()
  const currentMinutes = now.getHours() * 60 + now.getMinutes()
  const match = openingHoursToday.match(/(\d{1,2}):(\d{2})[–-](\d{1,2}):(\d{2})/)
  if (!match) return false
  const openMinutes = parseInt(match[1]) * 60 + parseInt(match[2])
  const closeMinutes = parseInt(match[3]) * 60 + parseInt(match[4])
  return currentMinutes >= openMinutes && currentMinutes < closeMinutes
}
