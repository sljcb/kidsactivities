# ⚙️ BE · Backend Architecture
## KidVenture · v1.0

> **I am the BE (Backend Engineer).** I handle servers, databases, APIs, and data sourcing. My principle as a solo dev: **use managed services**, spend energy on business logic, not ops.

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                      Client Layer                        │
│         Web (Next.js)         App (React Native)        │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS / REST + JSON
┌────────────────────▼────────────────────────────────────┐
│                   API Gateway (Cloudflare)                │
│              Rate limit / Auth / Cache / SSL              │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                Application Layer (FastAPI)                │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────┐  │
│  │  Recommend   │  │  Favorites    │  │  Search &   │  │
│  │  API         │  │  API          │  │  Filter     │  │
│  └──────────────┘  └───────────────┘  └─────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    Data Layer                             │
│  ┌─────────────────┐    ┌──────────────────────────┐   │
│  │ PostgreSQL       │    │ Redis (Upstash)           │   │
│  │ (Supabase)      │    │ Hot venue cache / rate     │   │
│  └─────────────────┘    │ limiting                   │   │
│                          └──────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│               Data Ingestion Pipeline                    │
│  Google Places API + Yelp Fusion API                    │
│  → Data normalization → Age tagging → Write to PG       │
│  Schedule: Daily full sync + hourly incremental          │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Framework | **Python FastAPI** | High perf, async-native, auto OpenAPI docs |
| Database | **Supabase (PostgreSQL)** | Managed, built-in auth, generous free tier |
| Cache | **Upstash Redis** | Serverless Redis, pay-per-use, indie friendly |
| Data Source 1 | **Google Places API (New)** | Best venue data, hours, photos, reviews for US |
| Data Source 2 | **Yelp Fusion API** | Rich reviews, ratings, 5000 free calls/day |
| Deployment | **Railway / Render** | Python support, one-click deploy |
| CDN/Gateway | **Cloudflare** | Free SSL + rate limiting + DDoS protection |
| Cron Jobs | **Railway Cron / GitHub Actions** | Data refresh scheduling |
| Object Storage | **Cloudflare R2** | Image storage, cheaper than S3 |

---

## 3. Database Schema

### 3.1 Core Tables

```sql
-- Venues table
CREATE TABLE venues (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(200) NOT NULL,
    city            VARCHAR(50) NOT NULL,            -- e.g., San Francisco
    neighborhood    VARCHAR(100),                    -- e.g., Mission District
    region          VARCHAR(50),                     -- e.g., South Bay, East Bay, SF, Peninsula
    address         TEXT,
    lat             DECIMAL(10, 7),
    lng             DECIMAL(10, 7),
    category        VARCHAR(50),                     -- playground, museum, indoor_play, etc.
    venue_type      VARCHAR(20) DEFAULT 'outdoor',   -- indoor / outdoor / both
    min_age_months  SMALLINT DEFAULT 0,
    max_age_months  SMALLINT DEFAULT 144,
    age_note        TEXT,                            -- "Great for toddlers because..."
    hours           JSONB,                           -- {"monday":"9:00 AM-5:00 PM",...}
    admission       JSONB,                           -- {"adult":15,"child":10,"under2":"free"}
    phone           VARCHAR(30),
    website         VARCHAR(300),
    images          TEXT[],
    rating          DECIMAL(2,1),                    -- 0-5 aggregate
    review_count    INT DEFAULT 0,
    google_place_id VARCHAR(300),                    -- for Google Places API updates
    yelp_id         VARCHAR(300),                    -- for Yelp API updates
    parking_info    TEXT,                            -- "Free lot", "Street parking"
    stroller_friendly BOOLEAN DEFAULT TRUE,
    has_restrooms   BOOLEAN DEFAULT TRUE,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- User profiles (extends Supabase Auth)
CREATE TABLE user_profiles (
    id              UUID PRIMARY KEY REFERENCES auth.users(id),
    display_name    VARCHAR(100),
    children        JSONB,  -- [{"name":"Emma","birth":"2021-03","gender":"F"}]
    home_city       VARCHAR(50),
    home_zip        VARCHAR(10),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Favorites
CREATE TABLE favorites (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES user_profiles(id),
    venue_id    UUID REFERENCES venues(id),
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, venue_id)
);

-- User corrections
CREATE TABLE venue_corrections (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    venue_id    UUID REFERENCES venues(id),
    user_id     UUID REFERENCES user_profiles(id),
    field       VARCHAR(50),
    old_value   TEXT,
    new_value   TEXT,
    status      VARCHAR(20) DEFAULT 'pending',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Reviews (sourced from Google/Yelp + user-submitted)
CREATE TABLE venue_reviews (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    venue_id    UUID REFERENCES venues(id),
    content     TEXT,
    rating      SMALLINT,
    author      VARCHAR(100),
    source      VARCHAR(30),   -- google / yelp / user
    source_date DATE,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
```

### 3.2 Key Indexes

```sql
CREATE INDEX idx_venues_region_city ON venues(region, city);
CREATE INDEX idx_venues_age ON venues(min_age_months, max_age_months);
CREATE INDEX idx_venues_location ON venues USING GIST(point(lng, lat));
CREATE INDEX idx_venues_category ON venues(category);
CREATE INDEX idx_venues_google_id ON venues(google_place_id);
```

---

## 4. API Design

### Base URL
```
https://api.kidventure.app/v1
```

### 4.1 Recommend (Core)

```http
GET /venues/recommend

Query Parameters:
  region      string  optional  Bay Area sub-region (sf/peninsula/south_bay/east_bay)
  city        string  optional  City (e.g., San Francisco)
  child_age   int     required  Child's age in months
  lat         float   optional  User latitude
  lng         float   optional  User longitude
  radius_mi   float   optional  Search radius in miles (default: 10)
  category    string  optional  Category filter (comma-separated)
  indoor      bool    optional  Indoor-only filter
  free_only   bool    optional  Free admission only
  page        int     optional  Page (default: 1)
  page_size   int     optional  Per page (default: 20, max: 50)

Response 200:
{
  "total": 48,
  "page": 1,
  "data": [
    {
      "id": "uuid",
      "name": "Bay Area Discovery Museum",
      "distance_mi": 2.3,
      "category": "museum",
      "venue_type": "both",
      "age_match_score": 95,
      "age_note": "Perfect for ages 2-8, with dedicated toddler zones",
      "rating": 4.7,
      "images": ["https://..."],
      "address": "557 McReynolds Rd, Sausalito, CA 94965",
      "admission": {"adult": 16, "child": 16, "under1": "free"},
      "hours_today": "9:00 AM – 5:00 PM",
      "parking_info": "Free parking lot",
      "stroller_friendly": true
    }
  ]
}
```

### 4.2 Venue Detail

```http
GET /venues/{venue_id}

Response: full info + latest 10 reviews + 5 nearby similar venues
```

### 4.3 Favorites

```http
POST /favorites            // Add (auth required)
DELETE /favorites/{id}     // Remove
GET /favorites             // List my favorites
```

### 4.4 Corrections

```http
POST /corrections
Body: { venue_id, field, new_value, description }
```

---

## 5. Data Ingestion

### 5.1 Data Sources

| Source | Data Type | Method | Cost |
|--------|----------|--------|------|
| Google Places API (New) | Hours, photos, location, reviews | Official API | $17/1000 detail requests |
| Yelp Fusion API | Reviews, ratings, categories | Official API | Free (5000/day) |
| Manual curation | Age notes, stroller info | Admin panel | Free (your time) |

### 5.2 Ingestion Pipeline

```
Google Places "Nearby Search" (type=amusement_park|museum|park|playground)
   ↓
Place Details (hours, reviews, photos)
   ↓
Yelp Fusion search (match by name + coordinates)
   ↓
Merge & normalize
   ↓
Age-tag using category + keyword rules
   ↓
Write to PostgreSQL staging table
   ↓
Review / auto-approve
   ↓
Merge to venues (production)
```

### 5.3 Age Tagging Rules

```python
AGE_RULES = {
    'playground':       {'min': 12, 'max': 96,  'note': 'Best for toddlers to elementary age'},
    'indoor_play':      {'min': 6,  'max': 72,  'note': 'Great for babies through kindergarten'},
    'museum':           {'min': 36, 'max': 144, 'note': 'Most engaging for 3+ year olds'},
    'science_center':   {'min': 48, 'max': 144, 'note': 'Hands-on exhibits best for 4+'},
    'nature_trail':     {'min': 24, 'max': 144, 'note': 'Stroller-friendly trails for 2+'},
    'splash_pad':       {'min': 12, 'max': 96,  'note': 'Seasonal, great for warm days'},
    'trampoline_park':  {'min': 36, 'max': 144, 'note': 'Some have dedicated toddler zones'},
    'library_storytime':{'min': 0,  'max': 60,  'note': 'Free, weekly sessions for babies to 5'},
    'swimming':         {'min': 6,  'max': 144, 'note': 'Infant swim classes from 6 months'},
    'farm':             {'min': 18, 'max': 120, 'note': 'Petting zoos great for 1.5+'},
    'rock_climbing':    {'min': 48, 'max': 144, 'note': 'Kids walls typically 4+'},
}
```

---

## 6. Age Match Scoring Algorithm (v1.0)

```python
def calculate_age_match_score(
    min_age: int, max_age: int, child_age: int,
    category: str = None, rating: float = None,
) -> int:
    """Score 0–100 for how well a venue fits a child's age."""

    if child_age < min_age or child_age > max_age:
        return 0

    score = 100

    # Age center proximity (closer to center = higher score)
    age_range = max_age - min_age
    if age_range > 0:
        center = (min_age + max_age) / 2
        distance_ratio = abs(child_age - center) / (age_range / 2)
        score -= int(distance_ratio * 20)

    # Category bonus
    CATEGORY_BONUS = {
        'swimming':    {range(6, 36): 15},
        'library_storytime': {range(0, 48): 12},
        'museum':      {range(48, 144): 10},
        'rock_climbing': {range(60, 144): 10},
    }
    if category in CATEGORY_BONUS:
        for age_range_obj, bonus in CATEGORY_BONUS[category].items():
            if child_age in age_range_obj:
                score += bonus
                break

    # High-rating bonus
    if rating and rating >= 4.5:
        score += 5

    return min(max(score, 0), 100)
```

---

## 7. Cost Estimate (Monthly)

| Service | Est. Monthly Cost |
|---------|-------------------|
| Supabase (free tier) | $0 |
| Upstash Redis (free tier) | $0 |
| Railway (BE deployment) | ~$5 |
| Cloudflare (free tier) | $0 |
| Google Places API (~2000 calls/mo) | ~$34 |
| Yelp Fusion API | $0 (free tier) |
| **Total** | **~$39/month** |

---

## 8. Security & Compliance

- All APIs rate-limited (Cloudflare + Redis token bucket)
- User location not persisted, used only for current recommendation
- COPPA compliant: no data collected from/about children under 13 directly
- CCPA compliant: user data deletion endpoint available
- Database credentials via environment variables only
- HTTPS everywhere

---

*BE Log: pending...*
