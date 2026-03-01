from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # General
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"

    # Database (Supabase)
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    DATABASE_URL: str = ""

    # Cache (Upstash Redis)
    UPSTASH_REDIS_URL: str = ""
    UPSTASH_REDIS_TOKEN: str = ""

    # Google Places API
    GOOGLE_PLACES_API_KEY: str = ""

    # Yelp Fusion API
    YELP_API_KEY: str = ""

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://kidventure.app",
        "https://www.kidventure.app",
    ]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
