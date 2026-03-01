"""
KidVenture · FastAPI Backend Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api import venues, favorites, corrections
from app.core.config import settings

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="KidVenture API",
    description="Age-based kid-friendly venue recommendations for Bay Area parents",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(venues.router,      prefix="/v1/venues",      tags=["Venues"])
app.include_router(favorites.router,   prefix="/v1/favorites",   tags=["Favorites"])
app.include_router(corrections.router, prefix="/v1/corrections", tags=["Corrections"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}
