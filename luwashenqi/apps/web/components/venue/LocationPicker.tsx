'use client'

import { cn } from '@/lib/utils'

const REGIONS = [
  { key: '',          label: 'All Bay Area' },
  { key: 'sf',        label: 'San Francisco' },
  { key: 'peninsula', label: 'Peninsula' },
  { key: 'south_bay', label: 'South Bay' },
  { key: 'east_bay',  label: 'East Bay' },
  { key: 'north_bay', label: 'North Bay' },
]

interface LocationPickerProps {
  value: { region: string; city: string }
  onChange: (val: { region: string; city: string }) => void
}

export function LocationPicker({ value, onChange }: LocationPickerProps) {
  return (
    <div>
      <p className="text-sm text-[#666] mb-2">Location</p>
      <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
        {REGIONS.map((r) => {
          const isActive = value.region === r.key
          return (
            <button
              key={r.key}
              onClick={() => onChange({ region: r.key, city: '' })}
              className={cn(
                'flex-shrink-0 px-3 py-1.5 rounded-full text-xs font-medium transition-all',
                isActive
                  ? 'bg-[#1890FF] text-white'
                  : 'bg-[#F7F8FA] text-[#666] hover:bg-[#E8F4FF]'
              )}
            >
              {r.label}
            </button>
          )
        })}
      </div>
    </div>
  )
}
