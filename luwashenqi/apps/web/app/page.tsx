'use client'

import { useState } from 'react'
import { AgePicker } from '@/components/venue/AgePicker'
import { LocationPicker } from '@/components/venue/LocationPicker'
import { CategoryFilter } from '@/components/venue/CategoryFilter'
import { VenueList } from '@/components/venue/VenueList'
import { Header } from '@/components/layout/Header'

export default function HomePage() {
  const [selectedAgeMonths, setSelectedAgeMonths] = useState<number>(36)
  const [location, setLocation] = useState({ region: '', city: '' })
  const [selectedCategory, setSelectedCategory] = useState<string>('all')

  return (
    <main className="min-h-screen bg-[#F7F8FA]">
      <Header />

      {/* Search Area */}
      <div className="bg-white px-4 pt-4 pb-3 shadow-sm">
        <AgePicker
          value={selectedAgeMonths}
          onChange={setSelectedAgeMonths}
        />
        <LocationPicker
          value={location}
          onChange={setLocation}
        />
      </div>

      {/* Filter Bar */}
      <div className="bg-white mt-2 px-4 py-3 border-b border-[#F0F0F0]">
        <CategoryFilter
          value={selectedCategory}
          onChange={setSelectedCategory}
        />
      </div>

      {/* Venue List */}
      <div className="px-4 py-4">
        <VenueList
          ageMonths={selectedAgeMonths}
          region={location.region}
          city={location.city}
          category={selectedCategory}
        />
      </div>
    </main>
  )
}
