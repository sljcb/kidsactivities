"""
Favorites API — stub (auth not yet implemented)
"""
from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def toggle_favorite(payload: dict):
    return {"status": "ok"}
