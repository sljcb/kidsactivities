"""
Recommendation Service — Core Business Logic
Age matching algorithm + distance calculation + database queries
"""
import math
from typing import Optional
from datetime import datetime
from supabase import create_client, Client
from app.core.config import settings

KM_PER_MILE = 1.60934


def haversine_miles(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate distance between two points in miles."""
    R_km = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    km = R_km * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return km / KM_PER_MILE


def calculate_age_match_score(
    min_age: int, max_age: int, child_age: int,
    category: Optional[str] = None, rating: Optional[float] = None,
) -> int:
    """
    Calculate age fit score (0–100).
    child_age: child's age in months.
    """
    if child_age < min_age or child_age > max_age:
        return 0

    score = 100

    # Age center proximity
    age_range = max_age - min_age
    if age_range > 0:
        center = (min_age + max_age) / 2
        distance_ratio = abs(child_age - center) / (age_range / 2)
        score -= int(distance_ratio * 20)

    # Category bonus by age
    CATEGORY_BONUS = {
        'swimming':          {range(6, 36): 15},
        'library':           {range(0, 48): 12},
        'museum':            {range(48, 144): 10},
        'science_center':    {range(48, 144): 10},
        'rock_climbing':     {range(60, 144): 10},
        'indoor_play':       {range(6, 72): 12},
        'trampoline_park':   {range(36, 144): 8},
    }
    if category in CATEGORY_BONUS:
        for age_rng, bonus in CATEGORY_BONUS[category].items():
            if child_age in age_rng:
                score += bonus
                break

    # High-rating bonus
    if rating and rating >= 4.5:
        score += 5

    return min(max(score, 0), 100)


def get_today_hours(hours: Optional[dict]) -> Optional[str]:
    """Get today's operating hours string."""
    if not hours:
        return None
    day_map = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday',
               4: 'friday', 5: 'saturday', 6: 'sunday'}
    today_key = day_map[datetime.now().weekday()]
    return hours.get(today_key) or hours.get('default')


class RecommendService:
    def __init__(self):
        self.db: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    async def get_recommendations(
        self,
        child_age_months: int,
        region: Optional[str] = None,
        city: Optional[str] = None,
        category: Optional[str] = None,
        indoor_only: Optional[bool] = None,
        free_only: Optional[bool] = None,
        user_lat: Optional[float] = None,
        user_lng: Optional[float] = None,
        radius_mi: float = 10.0,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        query = (
            self.db.table("venues")
            .select("*")
            .eq("is_active", True)
            .lte("min_age_months", child_age_months)
            .gte("max_age_months", child_age_months)
        )

        if region:
            query = query.eq("region", region)
        if city:
            query = query.eq("city", city)
        if category:
            query = query.eq("category", category)
        if indoor_only:
            query = query.in_("venue_type", ["indoor", "both"])

        response = query.execute()
        venues = response.data or []

        enriched = []
        for v in venues:
            score = calculate_age_match_score(
                min_age=v.get('min_age_months', 0),
                max_age=v.get('max_age_months', 144),
                child_age=child_age_months,
                category=v.get('category'),
                rating=v.get('rating'),
            )

            distance = None
            if user_lat and user_lng and v.get('lat') and v.get('lng'):
                distance = haversine_miles(user_lat, user_lng, v['lat'], v['lng'])
                if distance > radius_mi:
                    continue

            # Free filter
            if free_only:
                admission = v.get('admission') or {}
                child_price = admission.get('child', 1)
                if child_price and child_price > 0:
                    continue

            enriched.append({
                **v,
                'id': str(v['id']),
                'age_match_score': score,
                'distance_mi': round(distance, 1) if distance else None,
                'hours_today': get_today_hours(v.get('hours')),
            })

        enriched.sort(key=lambda x: (-x['age_match_score'], -(x.get('rating') or 0)))

        total = len(enriched)
        start = (page - 1) * page_size
        paginated = enriched[start: start + page_size]

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "data": paginated,
        }

    async def get_venue_by_id(self, venue_id: str) -> Optional[dict]:
        response = (
            self.db.table("venues")
            .select("*")
            .eq("id", venue_id)
            .eq("is_active", True)
            .single()
            .execute()
        )
        return response.data
