# 🖥️ FE · Frontend Architecture
## KidVenture · v1.0

> **I am the FE (Frontend Engineer).** I build everything the user sees and touches. Solo dev principle: **use mature ecosystems, don't reinvent wheels, ship fast.**

---

## 1. Tech Stack

### Core Frameworks

| Platform | Framework | Rationale |
|----------|-----------|-----------|
| **Web** | Next.js 14 (App Router) | SSR/SSG for SEO, Vercel one-click deploy, API routes |
| **App** | React Native (Expo) | Shared React knowledge, Expo Go for testing, iOS + Android |

### Toolchain

| Purpose | Tool |
|---------|------|
| Styling | Tailwind CSS + shadcn/ui |
| State | Zustand |
| Data Fetching | TanStack Query |
| Forms | React Hook Form + Zod |
| Maps | Google Maps JavaScript API (Web) / react-native-maps (App) |
| Icons | Lucide React |
| Animation | Framer Motion (Web) / Reanimated (App) |
| Linting | ESLint + Prettier + Husky |
| Package Mgr | pnpm (monorepo) |

---

## 2. Project Structure (Monorepo)

```
kidventure/
├── apps/
│   ├── web/                        # Next.js
│   │   ├── app/
│   │   │   ├── page.tsx                # Home (recommendation list)
│   │   │   ├── venue/[id]/page.tsx     # Venue detail
│   │   │   ├── favorites/page.tsx      # My favorites
│   │   │   └── layout.tsx
│   │   ├── components/
│   │   │   ├── venue/
│   │   │   │   ├── VenueCard.tsx
│   │   │   │   ├── VenueList.tsx
│   │   │   │   ├── AgePicker.tsx
│   │   │   │   └── CategoryFilter.tsx
│   │   │   ├── common/
│   │   │   └── layout/
│   │   └── lib/
│   │       ├── api.ts
│   │       └── utils.ts
│   │
│   └── mobile/                     # Expo React Native
│       ├── app/
│       │   ├── (tabs)/
│       │   │   ├── index.tsx           # Home
│       │   │   ├── map.tsx             # Map view
│       │   │   └── profile.tsx         # Profile / Favorites
│       │   └── venue/[id].tsx
│       └── stores/
│
├── packages/
│   ├── types/                      # Shared TypeScript types
│   ├── api-client/                 # Shared API hooks
│   └── ui/                         # Shared UI primitives
│
└── package.json
```

---

## 3. Core Pages

### 3.1 Home (Recommendation List)

```
┌─────────────────────────────────┐
│  🐣 KidVenture             ≡   │
├─────────────────────────────────┤
│  Child's Age: [▼ 3 years old]  │
│  Location: [📍 San Francisco]   │
├─────────────────────────────────┤
│  [All] [Indoor] [Outdoor]       │
│  [Free] [Museums] [Parks]       │
├─────────────────────────────────┤
│  ┌────────────────────────────┐ │
│  │ 🏛️ Bay Area Discovery Museum│ │
│  │ Ages 2-8  ⭐4.7  2.3 mi   │ │
│  │ "Hands-on exhibits toddlers │ │
│  │  love!"                     │ │
│  │ Open today 9 AM – 5 PM     │ │
│  └────────────────────────────┘ │
│  ┌────────────────────────────┐ │
│  │ 🌿 Golden Gate Park Playground│
│  │ Ages 1+  ⭐4.5  3.1 mi     │ │
│  └────────────────────────────┘ │
└─────────────────────────────────┘
```

### 3.2 Venue Detail Page

```
┌─────────────────────────────────┐
│  ← Back                    💾   │
├─────────────────────────────────┤
│  [Photo carousel / 3 images]    │
├─────────────────────────────────┤
│  Bay Area Discovery Museum      │
│  ⭐4.7  📍Sausalito  2.3 mi    │
├─────────────────────────────────┤
│  👶 Age Fit                      │
│  Perfect for ages 2–8. Dedicated │
│  toddler area on ground floor.  │
├─────────────────────────────────┤
│  🕐 Today: 9 AM – 5 PM         │
│  🎫 $16 adults / $16 kids       │
│     Under 1: Free               │
│  🅿️ Free parking lot             │
│  ♿ Stroller friendly            │
├─────────────────────────────────┤
│  🗺️ [Google Map embed]          │
│  [Navigate →]                   │
├─────────────────────────────────┤
│  💬 Reviews (24)                 │
│  "Brought my 3yo and she loved  │
│   the art studio section..."    │
└─────────────────────────────────┘
```

---

## 4. State Management

```typescript
// stores/useChildStore.ts
interface ChildStore {
  children: Child[]
  activeChildId: string
  activeAgeMonths: number
  setActiveAge: (months: number) => void
  addChild: (child: Child) => void
}

// stores/useLocationStore.ts
interface LocationStore {
  region: string           // sf, peninsula, south_bay, east_bay
  city: string
  lat: number | null
  lng: number | null
  setLocation: (loc: Location) => void
  detectLocation: () => Promise<void>
}

// stores/useFavoriteStore.ts
interface FavoriteStore {
  favorites: string[]
  toggle: (id: string) => void
  syncWithServer: () => Promise<void>
}
```

---

## 5. Key Technical Details

### 5.1 Age Picker

```typescript
const AGE_PRESETS = [
  { label: 'Baby',     sublabel: '0–1 yr',  months: 6,   icon: '🍼' },
  { label: 'Toddler',  sublabel: '2–3 yr',  months: 30,  icon: '🐣' },
  { label: 'Preschool', sublabel: '4–6 yr', months: 60,  icon: '🎨' },
  { label: 'School Age', sublabel: '7–12 yr', months: 108, icon: '🚴' },
]
```

### 5.2 Google Maps Integration (Web)

```typescript
// Using @vis.gl/react-google-maps
import { APIProvider, Map, AdvancedMarker } from '@vis.gl/react-google-maps'

// Venue markers colored by age_match_score:
// 90+ = green, 70-89 = orange, < 70 = gray
```

### 5.3 Infinite Scroll

```typescript
const { data, fetchNextPage, hasNextPage } = useInfiniteQuery({
  queryKey: ['venues', filters],
  queryFn: ({ pageParam = 1 }) => fetchVenues({ ...filters, page: pageParam }),
  getNextPageParam: (lastPage) => lastPage.nextPage,
})
```

### 5.4 SEO (Web)

```typescript
export async function generateMetadata({ params }): Promise<Metadata> {
  const venue = await getVenue(params.id)
  return {
    title: `${venue.name} | KidVenture`,
    description: `${venue.name} - ${venue.age_note}. Rating: ${venue.rating}. ${venue.address}`,
  }
}
```

---

## 6. Performance Targets

| Metric | Target |
|--------|--------|
| LCP | < 2.5s |
| FID | < 100ms |
| CLS | < 0.1 |
| First load (mobile 4G) | < 3s |
| Images | WebP, lazy-loaded |

---

## 7. Deployment

```
Web (Next.js)  →  Vercel (free tier sufficient for MVP)
App (Expo)     →  EAS Build → App Store + Google Play
```

---

*FE Log: pending...*
