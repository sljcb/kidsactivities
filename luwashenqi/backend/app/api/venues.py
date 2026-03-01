"""
Venue recommendation API endpoints
"""
from fastapi import APIRouter, Query, Request, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import Optional

from app.models.venue import VenueListResponse
from app.services.recommend import RecommendService
from app.core.config import settings

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

VALID_CATEGORIES = [
    'all', 'indoor_play', 'museum', 'park', 'playground',
    'restaurant', 'library', 'sports', 'farm', 'swimming',
    'science_center', 'trampoline_park', 'nature_trail',
]

VALID_REGIONS = ['sf', 'peninsula', 'south_bay', 'east_bay', 'north_bay']


@router.get("/recommend", response_model=VenueListResponse)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def recommend_venues(
    request: Request,
    child_age: int = Query(..., ge=0, le=200, description="Child's age in months"),
    region: Optional[str] = Query(None, description="Bay Area region (sf/peninsula/south_bay/east_bay/north_bay)"),
    city: Optional[str] = Query(None, description="City, e.g., San Francisco"),
    category: Optional[str] = Query(None, description="Venue category"),
    indoor: Optional[bool] = Query(None, description="Indoor only filter"),
    free_only: Optional[bool] = Query(None, description="Free admission only"),
    lat: Optional[float] = Query(None, ge=37.0, le=38.5, description="User latitude"),
    lng: Optional[float] = Query(None, ge=-123.0, le=-121.0, description="User longitude"),
    radius_mi: Optional[float] = Query(10.0, ge=0.5, le=50.0, description="Search radius in miles"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
):
    if region and region not in VALID_REGIONS:
        raise HTTPException(status_code=400, detail=f"Invalid region: {region}")
    if category and category not in VALID_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

    service = RecommendService()
    return await service.get_recommendations(
        child_age_months=child_age,
        region=region,
        city=city,
        category=category if category != 'all' else None,
        indoor_only=indoor,
        free_only=free_only,
        user_lat=lat,
        user_lng=lng,
        radius_mi=radius_mi,
        page=page,
        page_size=page_size,
    )


@router.get("/{venue_id}")
async def get_venue_detail(venue_id: str):
    """Venue detail endpoint."""
    service = RecommendService()
    venue = await service.get_venue_by_id(venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue
