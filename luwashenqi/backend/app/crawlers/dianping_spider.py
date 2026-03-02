"""
KidVenture · Data Ingestion Pipeline
Sources: Google Places API (New) + Yelp Fusion API
Target: Bay Area kid-friendly venues
"""
import asyncio
import httpx
from loguru import logger
from typing import List, Dict, Optional
from supabase import create_client
from app.core.config import settings

# Bay Area city centers for search radius
BAY_AREA_CENTERS = {
    'San Francisco':  {'lat': 37.7749, 'lng': -122.4194},
    'San Jose':       {'lat': 37.3382, 'lng': -121.8863},
    'Oakland':        {'lat': 37.8044, 'lng': -122.2712},
    'Palo Alto':      {'lat': 37.4419, 'lng': -122.1430},
    'Berkeley':       {'lat': 37.8716, 'lng': -122.2727},
    'Mountain View':  {'lat': 37.3861, 'lng': -122.0839},
    'Fremont':        {'lat': 37.5485, 'lng': -121.9886},
    'Sunnyvale':      {'lat': 37.3688, 'lng': -122.0363},
    'Walnut Creek':   {'lat': 37.9101, 'lng': -122.0652},
    'Sausalito':      {'lat': 37.8591, 'lng': -122.4853},
}

KIDS_PLACE_TYPES = [
    'amusement_park', 'aquarium', 'museum', 'park',
    'zoo', 'library', 'bowling_alley', 'swimming_pool',
]

# Maps place type → (category, min_age_months, max_age_months, venue_type)
AGE_TAG_RULES: Dict[str, tuple] = {
    'park':          ('park',       0,  144, 'outdoor'),
    'playground':    ('playground', 12, 120, 'outdoor'),
    'museum':        ('museum',     36, 144, 'indoor'),
    'library':       ('library',    0,  144, 'indoor'),
    'aquarium':      ('museum',     12, 144, 'indoor'),
    'zoo':           ('museum',     12, 144, 'outdoor'),
    'amusement_park':('indoor_play',36, 144, 'both'),
    'swimming_pool': ('swimming',   6,  144, 'both'),
    'bowling_alley': ('sports',     48, 144, 'indoor'),
}

# Maps city name → region slug
CITY_TO_REGION: Dict[str, str] = {
    'San Francisco': 'sf',
    'Daly City': 'sf',
    'South San Francisco': 'sf',
    'Oakland': 'east_bay',
    'Berkeley': 'east_bay',
    'Walnut Creek': 'east_bay',
    'Pleasanton': 'east_bay',
    'Concord': 'east_bay',
    'Fremont': 'east_bay',
    'Livermore': 'east_bay',
    'Palo Alto': 'peninsula',
    'Mountain View': 'peninsula',
    'Sunnyvale': 'peninsula',
    'Redwood City': 'peninsula',
    'Burlingame': 'peninsula',
    'San Mateo': 'peninsula',
    'San Jose': 'south_bay',
    'Santa Clara': 'south_bay',
    'Milpitas': 'south_bay',
    'Campbell': 'south_bay',
    'Los Gatos': 'south_bay',
    'Sausalito': 'north_bay',
    'Mill Valley': 'north_bay',
    'San Rafael': 'north_bay',
    'Novato': 'north_bay',
}


def region_from_city(city: str) -> Optional[str]:
    """Return region slug for a given city name."""
    return CITY_TO_REGION.get(city)


def apply_age_tags(venue: Dict) -> Dict:
    """Fill in category, min/max age, and venue_type based on place types."""
    types = venue.get("types", []) or venue.get("categories", [])
    for place_type in types:
        if place_type in AGE_TAG_RULES:
            category, min_age, max_age, venue_type = AGE_TAG_RULES[place_type]
            venue.setdefault("category", category)
            venue.setdefault("min_age_months", min_age)
            venue.setdefault("max_age_months", max_age)
            venue.setdefault("venue_type", venue_type)
            break
    # Defaults if no matching type found
    venue.setdefault("category", "park")
    venue.setdefault("min_age_months", 0)
    venue.setdefault("max_age_months", 144)
    venue.setdefault("venue_type", "outdoor")
    return venue


def deduplicate(venues: List[Dict]) -> List[Dict]:
    """Deduplicate by google_place_id first, then by (name.lower, city)."""
    seen_google: set = set()
    seen_name_city: set = set()
    result = []
    for v in venues:
        gid = v.get("google_place_id")
        key = (v.get("name", "").lower(), v.get("city", "").lower())
        if gid and gid in seen_google:
            continue
        if key in seen_name_city:
            continue
        if gid:
            seen_google.add(gid)
        seen_name_city.add(key)
        result.append(v)
    return result


async def save_to_supabase(venues: List[Dict], dry_run: bool = False) -> int:
    """Upsert venues into Supabase. Returns count of rows written."""
    if dry_run:
        logger.info(f"[DRY RUN] Would write {len(venues)} venues to Supabase")
        return 0

    client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    records = []
    for v in venues:
        records.append({
            "name": v.get("name", "")[:200],
            "city": (v.get("city") or "")[:50],
            "region": v.get("region"),
            "address": v.get("address"),
            "lat": v.get("lat"),
            "lng": v.get("lng"),
            "category": v.get("category"),
            "venue_type": v.get("venue_type", "outdoor"),
            "min_age_months": v.get("min_age_months", 0),
            "max_age_months": v.get("max_age_months", 144),
            "phone": v.get("phone"),
            "website": v.get("website"),
            "rating": v.get("rating"),
            "review_count": v.get("review_count", 0),
            "google_place_id": v.get("google_place_id"),
            "yelp_id": v.get("yelp_id"),
            "images": v.get("images", []),
            "stroller_friendly": True,
            "has_restrooms": True,
            "data_source": v.get("data_source", "google_places"),
            "is_active": True,
        })

    try:
        response = client.table("venues").upsert(
            records,
            on_conflict="google_place_id",
        ).execute()
        count = len(response.data) if response.data else 0
        logger.info(f"Saved {count} venues to Supabase")
        return count
    except Exception as e:
        logger.error(f"Supabase write error: {e}")
        raise


async def search_google_places(lat: float, lng: float, radius_meters: int = 16000) -> List[Dict]:
    """Search Google Places API (New) for kid-friendly venues."""
    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": settings.GOOGLE_PLACES_API_KEY,
        "X-Goog-FieldMask": (
            "places.id,places.displayName,places.formattedAddress,"
            "places.location,places.rating,places.userRatingCount,"
            "places.regularOpeningHours,places.photos,places.types,"
            "places.websiteUri,places.nationalPhoneNumber"
        ),
    }
    body = {
        "includedTypes": KIDS_PLACE_TYPES,
        "maxResultCount": 20,
        "locationRestriction": {
            "circle": {
                "center": {"latitude": lat, "longitude": lng},
                "radius": radius_meters,
            }
        },
        "languageCode": "en",
    }

    venues = []
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.post(url, json=body, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            for place in data.get("places", []):
                venues.append({
                    "google_place_id": place.get("id"),
                    "name": place.get("displayName", {}).get("text", ""),
                    "address": place.get("formattedAddress", ""),
                    "lat": place.get("location", {}).get("latitude"),
                    "lng": place.get("location", {}).get("longitude"),
                    "rating": place.get("rating"),
                    "review_count": place.get("userRatingCount", 0),
                    "phone": place.get("nationalPhoneNumber"),
                    "website": place.get("websiteUri"),
                    "types": place.get("types", []),
                    "source": "google",
                    "data_source": "google_places",
                })
            logger.info(f"Google Places: {len(venues)} venues near ({lat:.4f}, {lng:.4f})")
        except Exception as e:
            logger.error(f"Google Places API error: {e}")
    return venues


async def search_yelp(lat: float, lng: float, term: str = "kids activities") -> List[Dict]:
    """Search Yelp Fusion API. Free tier: 5000 calls/day."""
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {settings.YELP_API_KEY}"}
    params = {
        "term": term,
        "latitude": lat,
        "longitude": lng,
        "radius": 16000,
        "categories": "kids_activities,playgrounds,museums,zoos,aquariums",
        "sort_by": "rating",
        "limit": 50,
    }

    venues = []
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.get(url, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            for biz in data.get("businesses", []):
                loc = biz.get("location", {})
                coords = biz.get("coordinates", {})
                venues.append({
                    "yelp_id": biz.get("id"),
                    "name": biz.get("name", ""),
                    "address": ", ".join(loc.get("display_address", [])),
                    "city": loc.get("city", ""),
                    "lat": coords.get("latitude"),
                    "lng": coords.get("longitude"),
                    "rating": biz.get("rating"),
                    "review_count": biz.get("review_count", 0),
                    "phone": biz.get("display_phone"),
                    "categories": [c["alias"] for c in biz.get("categories", [])],
                    "source": "yelp",
                    "data_source": "yelp",
                })
            logger.info(f"Yelp Fusion: {len(venues)} venues near ({lat:.4f}, {lng:.4f})")
        except Exception as e:
            logger.error(f"Yelp API error: {e}")
    return venues


def merge_venues(google_venues: List[Dict], yelp_venues: List[Dict]) -> List[Dict]:
    """Merge Google + Yelp by name similarity. Google is primary."""
    merged = []
    for gv in google_venues:
        match = next(
            (yv for yv in yelp_venues
             if gv["name"].lower() in yv["name"].lower()
             or yv["name"].lower() in gv["name"].lower()),
            None
        )
        venue = {**gv}
        if match:
            venue["yelp_id"] = match.get("yelp_id")
            venue["city"] = match.get("city", "")
            if match.get("review_count", 0) > venue.get("review_count", 0):
                venue["review_count"] = match["review_count"]
        merged.append(venue)

    google_names = {v["name"].lower() for v in google_venues}
    for yv in yelp_venues:
        if yv["name"].lower() not in google_names:
            merged.append(yv)
    return merged


async def ingest_bay_area(dry_run: bool = False, limit: Optional[int] = None) -> List[Dict]:
    """Full Bay Area data ingestion. Run daily via cron or via scripts/seed.py."""
    all_venues = []
    for city, coords in BAY_AREA_CENTERS.items():
        logger.info(f"Ingesting {city}...")
        google_results = await search_google_places(lat=coords["lat"], lng=coords["lng"])
        yelp_results = await search_yelp(lat=coords["lat"], lng=coords["lng"])
        merged = merge_venues(google_results, yelp_results)

        # Attach city and region to each venue
        for v in merged:
            v.setdefault("city", city)
            v["region"] = region_from_city(v.get("city") or city)

        all_venues.extend(merged)
        await asyncio.sleep(1)  # Rate limit courtesy

    logger.info(f"Raw venues collected: {len(all_venues)}")

    # Apply age tags
    all_venues = [apply_age_tags(v) for v in all_venues]

    # Deduplicate across cities
    all_venues = deduplicate(all_venues)
    logger.info(f"Unique venues after dedup: {len(all_venues)}")

    # Optional cap
    if limit:
        all_venues = all_venues[:limit]

    # Write to Supabase
    await save_to_supabase(all_venues, dry_run=dry_run)

    return all_venues


if __name__ == "__main__":
    asyncio.run(ingest_bay_area())
