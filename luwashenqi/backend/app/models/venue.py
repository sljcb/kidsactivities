"""
Venue data models (Pydantic)
Maps to database schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from uuid import UUID
from datetime import datetime


class VenueBase(BaseModel):
    name: str = Field(..., max_length=200)
    city: str = Field(..., max_length=50)
    neighborhood: Optional[str] = Field(None, max_length=100)
    region: Optional[str] = Field(None, max_length=50)   # sf/peninsula/south_bay/east_bay
    address: Optional[str] = None
    lat: Optional[float] = Field(None, ge=37.0, le=38.5)   # Bay Area lat range
    lng: Optional[float] = Field(None, ge=-123.0, le=-121.0)  # Bay Area lng range
    category: Optional[str] = Field(None, max_length=50)
    venue_type: Optional[str] = Field('outdoor', max_length=20)  # indoor/outdoor/both
    min_age_months: int = Field(0, ge=0, le=200)
    max_age_months: int = Field(144, ge=0, le=200)
    age_note: Optional[str] = None
    hours: Optional[Dict] = None
    admission: Optional[Dict] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    images: List[str] = []
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    review_count: int = 0
    google_place_id: Optional[str] = None
    yelp_id: Optional[str] = None
    parking_info: Optional[str] = None
    stroller_friendly: bool = True
    has_restrooms: bool = True


class VenueInDB(VenueBase):
    id: UUID
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VenueResponse(VenueBase):
    """API response model with computed fields."""
    id: str
    age_match_score: int = Field(0, ge=0, le=100)
    distance_mi: Optional[float] = None
    hours_today: Optional[str] = None


class VenueListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: List[VenueResponse]
