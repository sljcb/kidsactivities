'use client'

import { cn } from '@/lib/utils'

const CATEGORIES = [
  { key: 'all',             label: 'All',         icon: '✨' },
  { key: 'playground',      label: 'Playground',   icon: '🛝' },
  { key: 'museum',          label: 'Museum',       icon: '🏛️' },
  { key: 'indoor_play',     label: 'Indoor Play',  icon: '🎡' },
  { key: 'park',            label: 'Park',         icon: '🌿' },
  { key: 'science_center',  label: 'Science',      icon: '🔬' },
  { key: 'swimming',        label: 'Swimming',     icon: '🏊' },
  { key: 'library',         label: 'Library',      icon: '📚' },
  { key: 'farm',            label: 'Farm',         icon: '🌻' },
  { key: 'sports',          label: 'Sports',       icon: '⛹️' },
]

interface CategoryFilterProps {
  value: string
  onChange: (val: string) => void
}

export function CategoryFilter({ value, onChange }: CategoryFilterProps) {
  return (
    <div className="flex gap-2 overflow-x-auto scrollbar-hide">
      {CATEGORIES.map((cat) => {
        const isActive = value === cat.key
        return (
          <button
            key={cat.key}
            onClick={() => onChange(cat.key)}
            className={cn(
              'flex-shrink-0 flex items-center gap-1 px-3 py-1.5 rounded-full text-xs font-medium transition-all',
              isActive
                ? 'bg-[#FF6B35] text-white'
                : 'bg-[#F7F8FA] text-[#666] hover:bg-[#FFF0E8]'
            )}
          >
            <span>{cat.icon}</span>
            <span>{cat.label}</span>
          </button>
        )
      })}
    </div>
  )
}
