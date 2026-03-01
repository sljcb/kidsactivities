# 📋 PM · Product Requirements Document (PRD)
## KidVenture · v1.0

> **I am the PM.** My job is to translate real parent pain points into clear requirements so the entire team aims at the same target.

---

## 1. Background & Opportunity

### Pain Points

Taking kids out is stressful when you don't know where to go:

- Parks may be too far or age-inappropriate
- Indoor play places are crowded and expensive
- Different ages need completely different venues
- Parents waste time scrolling Yelp, Google, Nextdoor, and parenting Facebook groups for ideas

### Market Opportunity

- Bay Area has ~1.2M children under 12 across 9 counties
- Weekend family outings are a rigid need — weather, school schedule, and energy levels drive weekly decisions
- Existing tools (Yelp, Google Maps) have no age-based filtering — a 2-year-old and an 8-year-old need totally different places
- Indie dev wedge: **age-precise + hyperlocal + lightweight tool**

---

## 2. Target Users

### Primary Users
**Bay Area parents** with children age 0–12, looking for weekend/holiday outing ideas

| Persona | Characteristics |
|---------|----------------|
| New Parents (0–2 yr) | Anxious, need safe/clean/baby-friendly venues with good facilities |
| Active Parents (3–6 yr) | Exploratory, seek fun + educational experiences |
| Busy Parents (7–12 yr) | Efficiency-focused, kids have their own preferences, need engaging activities |

### Secondary Users
Grandparents, nannies/babysitters, family visitors from out of town

---

## 3. Core Feature Requirements

### 3.1 Must-Have (MVP)

#### F1 · Smart Venue Recommendations
- Input: child's age (dropdown) + city/neighborhood (GPS or manual)
- Output: ranked venue list sorted by "age fit score"
- Each venue card: name, distance, age fit, description, rating, photos

#### F2 · Venue Detail Page
- Info: address, hours, admission, parking, transit
- Age fit explanation ("This spot is great for 3-year-olds because…")
- Reviews (Google/Yelp data + user-submitted)
- One-tap navigation (open in Google Maps / Apple Maps)

#### F3 · Location Filtering
- Bay Area → City → Neighborhood (3-level)
- "Within X miles" radius filter
- Quick filters: "Near me", "San Francisco", "Peninsula", "South Bay", "East Bay"

#### F4 · Age-Based Tiers
- **0–1 yr**: Baby-friendly cafes, sensory play, infant swim, libraries with baby storytime
- **2–3 yr**: Indoor play gyms, toddler parks, children's museums, petting zoos
- **4–6 yr**: Science museums, children's theaters, nature centers, splash pads, bike trails
- **7–12 yr**: Rock climbing, trampoline parks, coding workshops, escape rooms, hiking trails

### 3.2 Should-Have (v1.1)

#### F5 · Favorites & Lists
- Save venues, create "Weekend Plans" lists
- Share via iMessage / WhatsApp / text

#### F6 · User Corrections
- "Info outdated?" One-tap correction submission
- Gamification: earn points for verified corrections

#### F7 · Events Calendar
- Upcoming events at venues (storytime, craft workshops, holiday specials)
- Sourced from venue websites + community submissions

### 3.3 Future (v2.0)

- AI itinerary planner ("Plan a half-day outing for my 4-year-old in SF")
- Parent community (local playdate matching)
- Venue partnerships (verified listings, deals)

---

## 4. User Stories

| ID | Story | Priority |
|----|-------|----------|
| US-01 | As a parent, I want to enter my child's age and location to quickly see recommended venues | P0 |
| US-02 | As a parent, I want to see if each venue suits my child's age, and why | P0 |
| US-03 | As a parent, I want one-tap navigation to the venue | P0 |
| US-04 | As a parent, I want to filter by distance to find places within 5 miles | P1 |
| US-05 | As a parent, I want to save venues I'm interested in for the weekend | P1 |
| US-06 | As a parent, I want to share a great venue with my friends | P1 |
| US-07 | As a parent, I want to see current hours and admission to avoid wasted trips | P0 |
| US-08 | As a parent, I want to report outdated info so others don't waste their time | P2 |
| US-09 | As a parent, I want to see "indoor" vs "outdoor" tags so I can plan around weather | P1 |
| US-10 | As a parent, I want to know about parking availability and stroller accessibility | P1 |

---

## 5. Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| Performance | Recommendation results first paint < 2s |
| Usability | Mobile-first, minimum 375px viewport |
| Data freshness | Venue info refreshed at least weekly |
| Privacy | COPPA compliant; no data collected from children; location is opt-in |
| Offline | Previously viewed venue details available offline (cache) |
| Accessibility | WCAG 2.1 AA compliant |

---

## 6. Success Metrics (KPI)

| Metric | MVP Target (first 3 months) |
|--------|-----------------------------|
| MAU | 3,000 |
| Day-1 retention | ≥ 30% |
| Avg venues viewed per session | ≥ 3 |
| Venue coverage | Bay Area, ≥ 500 venues |
| User satisfaction (NPS) | ≥ 40 |

---

## 7. Competitive Analysis

| Product | Strength | Weakness (Our Opportunity) |
|---------|----------|---------------------------|
| Yelp | Massive data, rich reviews | No age filtering, "Kids Activities" category is shallow |
| Google Maps | Navigation + hours + reviews | No age-based recommendations, not curated |
| Nextdoor | Hyperlocal community trust | Fragmented info, no structured data |
| Winnie | Parenting-focused | Pivoted away from venue discovery, outdated data |
| Red Tricycle | Good content | Blog format, not a tool; can't filter by age/distance |

**Our edge: Age-precise matching × hyperlocal Bay Area × lightweight tool**

---

## 8. Release Plan

```
v0.1 (alpha)  → SF only + basic recommendations + core info
v1.0 (beta)   → Full Bay Area + complete filtering + favorites + sharing
v1.5          → Events calendar + user corrections + gamification
v2.0          → AI itinerary planner + community features
```

---

*PM Log: pending...*
