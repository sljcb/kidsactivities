/**
 * KidVenture · Shared Type Definitions
 * Used by both Web + App
 */

export interface Venue {
  id: string
  name: string
  city: string                                // e.g., San Francisco
  neighborhood?: string                       // e.g., Mission District
  region?: string                             // sf / peninsula / south_bay / east_bay
  address?: string
  lat?: number
  lng?: number
  category?: string                           // playground, museum, indoor_play, etc.
  venue_type?: 'indoor' | 'outdoor' | 'both'
  min_age_months: number
  max_age_months: number
  age_note?: string                           // "Great for toddlers because..."
  hours?: Record<string, string>              // { monday: "9:00 AM-5:00 PM", ... }
  admission?: { adult?: number; child?: number; under1?: string; note?: string }
  phone?: string
  website?: string
  images: string[]
  rating?: number
  review_count: number
  google_place_id?: string
  yelp_id?: string
  parking_info?: string
  stroller_friendly?: boolean
  has_restrooms?: boolean

  // Computed fields from API
  age_match_score?: number
  distance_mi?: number
  hours_today?: string
}

export interface VenueListResponse {
  total: number
  page: number
  page_size: number
  data: Venue[]
}

export interface Child {
  id: string
  name: string
  birthDate: string      // YYYY-MM
  gender: 'M' | 'F'
}

export interface UserLocation {
  region?: string        // sf, peninsula, south_bay, east_bay
  city?: string
  lat?: number
  lng?: number
}

export type AgeGroup = 'Baby' | 'Toddler' | 'Preschool' | 'School Age'

export type VenueCategory =
  | 'indoor_play'
  | 'museum'
  | 'park'
  | 'playground'
  | 'restaurant'
  | 'library'
  | 'sports'
  | 'farm'
  | 'swimming'
  | 'science_center'
  | 'trampoline_park'
  | 'nature_trail'

export interface Correction {
  venue_id: string
  field: string
  new_value: string
  description?: string
}

export type BayAreaRegion = 'sf' | 'peninsula' | 'south_bay' | 'east_bay' | 'north_bay'

export const BAY_AREA_CITIES: Record<BayAreaRegion, string[]> = {
  sf: ['San Francisco'],
  peninsula: ['Palo Alto', 'Menlo Park', 'Redwood City', 'San Mateo', 'Burlingame', 'Millbrae', 'Daly City'],
  south_bay: ['San Jose', 'Cupertino', 'Sunnyvale', 'Mountain View', 'Santa Clara', 'Campbell', 'Los Gatos', 'Milpitas', 'Fremont'],
  east_bay: ['Oakland', 'Berkeley', 'Walnut Creek', 'Pleasanton', 'Dublin', 'Livermore', 'Hayward', 'Union City'],
  north_bay: ['Sausalito', 'San Rafael', 'Mill Valley', 'Novato', 'Petaluma'],
}
