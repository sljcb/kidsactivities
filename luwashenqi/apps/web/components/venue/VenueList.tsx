'use client'

import { useInfiniteQuery } from '@tanstack/react-query'
import { useEffect, useRef } from 'react'
import { VenueCard } from './VenueCard'
import { fetchVenues } from '@/lib/api'

interface VenueListProps {
  ageMonths: number
  region: string
  city: string
  category: string
}

export function VenueList({ ageMonths, region, city, category }: VenueListProps) {
  const loadMoreRef = useRef<HTMLDivElement>(null)

  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
    isError,
  } = useInfiniteQuery({
    queryKey: ['venues', { ageMonths, region, city, category }],
    queryFn: ({ pageParam = 1 }) =>
      fetchVenues({ ageMonths, region, city, category, page: pageParam as number }),
    getNextPageParam: (lastPage) => lastPage.nextPage,
    initialPageParam: 1,
  })

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasNextPage && !isFetchingNextPage) {
          fetchNextPage()
        }
      },
      { threshold: 0.1 }
    )
    if (loadMoreRef.current) observer.observe(loadMoreRef.current)
    return () => observer.disconnect()
  }, [fetchNextPage, hasNextPage, isFetchingNextPage])

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 gap-3">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white rounded-xl h-52 animate-pulse" />
        ))}
      </div>
    )
  }

  if (isError) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-center">
        <span className="text-5xl mb-4">😅</span>
        <p className="text-[#666] text-sm">Failed to load. Please try again.</p>
      </div>
    )
  }

  const venues = data?.pages.flatMap((page) => page.data) ?? []

  if (venues.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-center">
        <span className="text-5xl mb-4">🐻</span>
        <p className="text-[#666] text-sm">No matches found</p>
        <p className="text-[#999] text-xs mt-1">Try a different area or age group?</p>
      </div>
    )
  }

  return (
    <div>
      <p className="text-xs text-[#999] mb-3">
        {data?.pages[0]?.total ?? 0} places found
      </p>
      <div className="grid grid-cols-1 gap-3">
        {venues.map((venue) => (
          <VenueCard key={venue.id} venue={venue} />
        ))}
      </div>

      <div ref={loadMoreRef} className="py-6 text-center">
        {isFetchingNextPage && (
          <p className="text-xs text-[#999]">Loading more...</p>
        )}
        {!hasNextPage && venues.length > 0 && (
          <p className="text-xs text-[#999]">— That&apos;s all! —</p>
        )}
      </div>
    </div>
  )
}
