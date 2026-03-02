"""
Corrections API — stub (auth not yet implemented)
"""
from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def submit_correction(payload: dict):
    return {"status": "ok"}
