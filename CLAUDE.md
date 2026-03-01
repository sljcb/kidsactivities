# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**KidVenture** (遛娃神器) — Age-based kid-friendly venue recommendations for the Bay Area. The system matches children's ages (in months) with venues like playgrounds, museums, parks, and indoor play centers.

All work lives under `luwashenqi/`. Key architecture docs are at the repo root: `02_BE_Architecture.md` and `03_FE_Architecture.md`.

## Commands

### Frontend (Next.js 14) — run from `luwashenqi/`
```bash
pnpm install          # Install all workspace dependencies
pnpm dev:web          # Start web app at http://localhost:3000
pnpm build:web        # Production build
pnpm lint             # Lint all packages
pnpm type-check       # TypeScript type check all packages
```

Or from `luwashenqi/apps/web/`:
```bash
pnpm dev              # Dev server
pnpm lint             # ESLint
pnpm type-check       # tsc --noEmit
```

### Backend (FastAPI) — run from `luwashenqi/backend/`
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload     # API at http://localhost:8000, docs at /docs
```

### Data seeding
```bash
python scripts/seed.py            # Basic seed data
python scripts/seed_fake_data.py  # Generate 500+ mock Bay Area venues
```

## Architecture

### Backend (`luwashenqi/backend/`)
- **FastAPI** with async/await throughout
- **Entry point:** `app/main.py` — mounts three routers, CORS, rate limiting (slowapi)
- **Routers:** `app/api/venues.py`, `app/api/favorites.py`, `app/api/corrections.py`
- **Core service:** `app/services/recommend.py` — `RecommendService` handles venue filtering + age match scoring
- **Models:** `app/models/venue.py` — Pydantic v2 schemas (VenueBase, VenueInDB, VenueResponse, VenueListResponse)
- **Config:** `app/core/config.py` — Settings via pydantic_settings (reads from `.env`)
- **Crawler:** `app/crawlers/dianping_spider.py` — Scrapy + Playwright scraper integrating Google Places & Yelp APIs
- **Database:** Supabase (PostgreSQL); schema in `scripts/create_venues_table.sql`
- **Cache:** Upstash Redis

**Age match scoring** (0–100): starts at 100, penalizes distance from optimal age range center (max −20), applies category bonuses (e.g., swimming for 6–36 month olds gets +15), and a rating bonus (+5 for 4.5+ stars).

**Key env vars** (see `backend/.env.example`): `SUPABASE_URL`, `SUPABASE_KEY`, `DATABASE_URL`, `UPSTASH_REDIS_URL`, `UPSTASH_REDIS_TOKEN`, `GOOGLE_PLACES_API_KEY`, `YELP_API_KEY`

### Frontend (`luwashenqi/apps/web/`)
- **Next.js 14 App Router**, Tailwind CSS, Radix UI, Zustand, TanStack Query, Framer Motion
- **Entry:** `app/layout.tsx` wraps with QueryProvider; `app/page.tsx` is the home page
- **API client:** `lib/api.ts` — `fetchVenues()`, `fetchVenueById()`, `toggleFavorite()`, `submitCorrection()`
  - Base URL from `NEXT_PUBLIC_API_URL` env var (defaults to `https://api.kidventure.app/v1`)
- **Key components:**
  - `VenueList` — infinite scroll via IntersectionObserver + `useInfiniteQuery`
  - `AgePicker` — preset age groups or custom months input
  - `LocationPicker` — Bay Area region/city selector (sf/peninsula/south_bay/east_bay/north_bay)
  - `CategoryFilter` — pill-style venue type filters

### Shared Packages (`luwashenqi/packages/`)
- `types/` — shared TypeScript types (aliased as `@kidventure/types`)
- `api-client/` — shared API hooks
- `ui/` — shared Radix UI primitives

### Infrastructure
- **Frontend:** Vercel; **Backend:** Railway or Render; **DB:** Supabase; **Cache:** Upstash Redis; **CDN/Rate limiting:** Cloudflare; **Images:** Cloudflare R2

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/venues/recommend` | Paginated venue list with age match scores. Required: `child_age` (months). Optional: `region`, `city`, `category`, `indoor`, `free_only`, `lat`, `lng`, `radius_mi`, `page`, `page_size` |
| GET | `/v1/venues/{venue_id}` | Full venue detail |
| POST/DELETE/GET | `/v1/favorites` | User favorites (auth stubs — not yet implemented) |
| POST | `/v1/corrections` | User data corrections (auth stub — not yet implemented) |
| GET | `/health` | Health check |

## Venues DB Schema

Core fields: `id` (UUID), `name`, `city`, `neighborhood`, `region`, `address`, `lat`, `lng`, `category`, `venue_type` (indoor/outdoor/both), `min_age_months`, `max_age_months`, `hours` (JSONB), `admission` (JSONB), `rating`, `review_count`, `images` (URL array), `google_place_id`, `yelp_id`, `stroller_friendly`, `has_restrooms`, `data_source`, `is_active`.
