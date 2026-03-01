"""
KidVenture · Data Ingestion Pipeline
Sources: Google Places API (New) + Yelp Fusion API
Target: Bay Area kid-friendly venues
"""
import asyncio
import httpx
from loguru import logger
from typing import List, Dict
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


async def ingest_bay_area():
    """Full Bay Area data ingestion. Run daily via cron."""
    all_venues = []
    for city, coords in BAY_AREA_CENTERS.items():
        logger.info(f"Ingesting {city}...")
        google_results = await search_google_places(lat=coords["lat"], lng=coords["lng"])
        yelp_results = await search_yelp(lat=coords["lat"], lng=coords["lng"])
        merged = merge_venues(google_results, yelp_results)
        all_venues.extend(merged)
        await asyncio.sleep(1)  # Rate limit courtesy

    logger.info(f"Total venues ingested: {len(all_venues)}")
    # TODO: Apply age tagging rules
    # TODO: Write to Supabase staging table
    # TODO: Deduplicate across cities
    return all_venues


if __name__ == "__main__":
    asyncio.run(ingest_bay_area())
