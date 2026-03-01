'use client'

import { cn } from '@/lib/utils'

const AGE_PRESETS = [
  { label: 'Baby',      sublabel: '0–1 yr',  months: 6,   icon: '🍼' },
  { label: 'Toddler',   sublabel: '2–3 yr',  months: 30,  icon: '🐣' },
  { label: 'Preschool',  sublabel: '4–6 yr', months: 60,  icon: '🎨' },
  { label: 'School Age', sublabel: '7–12 yr', months: 108, icon: '🚴' },
]

interface AgePickerProps {
  value: number
  onChange: (months: number) => void
}

export function AgePicker({ value, onChange }: AgePickerProps) {
  return (
    <div className="mb-3">
      <p className="text-sm text-[#666] mb-2">Child&apos;s Age</p>
      <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
        {AGE_PRESETS.map((preset) => {
          const isActive = value === preset.months
          return (
            <button
              key={preset.months}
              onClick={() => onChange(preset.months)}
              className={cn(
                'flex-shrink-0 flex flex-col items-center justify-center',
                'w-20 h-18 rounded-xl text-xs font-medium transition-all duration-200 py-2',
                isActive
                  ? 'bg-[#FF6B35] text-white scale-105 shadow-md'
                  : 'bg-[#F7F8FA] text-[#666] hover:bg-[#FFF0E8]'
              )}
            >
              <span className="text-xl mb-1">{preset.icon}</span>
              <span className="font-semibold">{preset.label}</span>
              <span className="text-[10px] opacity-75">{preset.sublabel}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
