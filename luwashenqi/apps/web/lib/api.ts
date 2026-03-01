const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'https://api.kidventure.app/v1'

interface FetchVenuesParams {
  ageMonths: number
  region?: string
  city?: string
  category?: string
  indoor?: boolean
  freeOnly?: boolean
  lat?: number
  lng?: number
  radiusMi?: number
  page?: number
  pageSize?: number
}

export async function fetchVenues(params: FetchVenuesParams) {
  const searchParams = new URLSearchParams({
    child_age: String(params.ageMonths),
    page: String(params.page ?? 1),
    page_size: String(params.pageSize ?? 20),
  })

  if (params.region) searchParams.set('region', params.region)
  if (params.city) searchParams.set('city', params.city)
  if (params.category && params.category !== 'all') searchParams.set('category', params.category)
  if (params.indoor) searchParams.set('indoor', 'true')
  if (params.freeOnly) searchParams.set('free_only', 'true')
  if (params.lat) searchParams.set('lat', String(params.lat))
  if (params.lng) searchParams.set('lng', String(params.lng))
  if (params.radiusMi) searchParams.set('radius_mi', String(params.radiusMi))

  const res = await fetch(`${API_BASE}/venues/recommend?${searchParams}`)
  if (!res.ok) throw new Error(`API error: ${res.status}`)

  const json = await res.json()
  return {
    data: json.data,
    total: json.total,
    nextPage: json.page * json.page_size < json.total ? json.page + 1 : undefined,
  }
}

export async function fetchVenueById(id: string) {
  const res = await fetch(`${API_BASE}/venues/${id}`)
  if (!res.ok) throw new Error(`Venue not found: ${id}`)
  return res.json()
}

export async function toggleFavorite(venueId: string, token: string) {
  const res = await fetch(`${API_BASE}/favorites`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ venue_id: venueId }),
  })
  if (!res.ok) throw new Error('Failed to save favorite')
  return res.json()
}

export async function submitCorrection(
  venueId: string,
  field: string,
  newValue: string,
  token: string
) {
  const res = await fetch(`${API_BASE}/corrections`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ venue_id: venueId, field, new_value: newValue }),
  })
  if (!res.ok) throw new Error('Failed to submit correction')
  return res.json()
}
