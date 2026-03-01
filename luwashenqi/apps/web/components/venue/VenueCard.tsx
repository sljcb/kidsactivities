'use client'

import { useState } from 'react'
import { MapPin, Clock, Star, Bookmark, Car, Baby } from 'lucide-react'
import { cn } from '@/lib/utils'
import type { Venue } from '@kidventure/types'

interface VenueCardProps {
  venue: Venue
  onFavoriteToggle?: (id: string) => void
  isFavorited?: boolean
}

const AGE_MATCH_CONFIG = {
  high:   { label: '✅ Perfect fit', className: 'bg-green-100 text-green-700' },
  medium: { label: '👍 Good fit',    className: 'bg-orange-100 text-orange-700' },
  low:    { label: '⚠️ Okay fit',   className: 'bg-yellow-100 text-yellow-700' },
}

function getAgeMatchLevel(score: number) {
  if (score >= 90) return AGE_MATCH_CONFIG.high
  if (score >= 70) return AGE_MATCH_CONFIG.medium
  return AGE_MATCH_CONFIG.low
}

export function VenueCard({ venue, onFavoriteToggle, isFavorited = false }: VenueCardProps) {
  const [favorited, setFavorited] = useState(isFavorited)
  const matchConfig = getAgeMatchLevel(venue.age_match_score ?? 80)

  const handleFavorite = (e: React.MouseEvent) => {
    e.stopPropagation()
    setFavorited(!favorited)
    onFavoriteToggle?.(venue.id)
  }

  return (
    <div className="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition-shadow duration-200 cursor-pointer active:scale-[0.98]">
      {/* Image */}
      <div className="relative w-full h-40 bg-[#F0F0F0]">
        {venue.images?.[0] ? (
          <img
            src={venue.images[0]}
            alt={venue.name}
            className="w-full h-full object-cover"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-4xl">
            {venue.category === 'museum' ? '🏛️' :
             venue.category === 'park' ? '🌿' :
             venue.category === 'indoor_play' ? '🎡' :
             venue.category === 'playground' ? '🛝' : '📍'}
          </div>
        )}
        <button
          onClick={handleFavorite}
          className="absolute top-3 right-3 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-md"
        >
          <Bookmark
            size={16}
            className={cn(
              'transition-colors',
              favorited ? 'fill-[#FF6B35] text-[#FF6B35]' : 'text-[#999]'
            )}
          />
        </button>
        {/* Indoor/Outdoor badge */}
        {venue.venue_type && (
          <span className="absolute top-3 left-3 text-xs px-2 py-0.5 bg-white/90 rounded-full text-[#666]">
            {venue.venue_type === 'indoor' ? '🏠 Indoor' :
             venue.venue_type === 'outdoor' ? '🌳 Outdoor' : '🔄 Both'}
          </span>
        )}
      </div>

      {/* Content */}
      <div className="p-3">
        <h3 className="font-semibold text-[#1A1A1A] text-base leading-snug mb-2">
          {venue.name}
        </h3>

        {/* Tags */}
        <div className="flex items-center gap-2 mb-2 flex-wrap">
          <span className="text-xs px-2 py-0.5 bg-[#F0F5FF] text-[#2F54EB] rounded-full capitalize">
            {venue.category?.replace('_', ' ')}
          </span>
          <span className={cn('text-xs px-2 py-0.5 rounded-full', matchConfig.className)}>
            {matchConfig.label}
          </span>
          <div className="flex items-center gap-1 ml-auto">
            <Star size={12} className="fill-[#FFB800] text-[#FFB800]" />
            <span className="text-xs text-[#666]">{venue.rating}</span>
            <span className="text-xs text-[#999]">({venue.review_count})</span>
          </div>
        </div>

        {/* Location & Distance */}
        <div className="flex items-center gap-1 mb-1">
          <MapPin size={12} className="text-[#999] flex-shrink-0" />
          <span className="text-xs text-[#999] truncate">{venue.neighborhood || venue.city}</span>
          {venue.distance_mi != null && (
            <span className="text-xs text-[#999] ml-auto flex-shrink-0">
              {venue.distance_mi.toFixed(1)} mi
            </span>
          )}
        </div>

        {/* Hours */}
        <div className="flex items-center gap-1 mb-1">
          <Clock size={12} className="text-[#52C41A] flex-shrink-0" />
          <span className="text-xs text-[#52C41A]">
            {venue.hours_today ?? 'Check hours'}
          </span>
        </div>

        {/* Amenities */}
        <div className="flex items-center gap-3 mt-1">
          {venue.parking_info && (
            <span className="text-xs text-[#999] flex items-center gap-1">
              <Car size={10} /> {venue.parking_info}
            </span>
          )}
          {venue.stroller_friendly && (
            <span className="text-xs text-[#999] flex items-center gap-1">
              <Baby size={10} /> Stroller OK
            </span>
          )}
        </div>
      </div>
    </div>
  )
}
