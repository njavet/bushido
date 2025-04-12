from fastapi import APIRouter

# project imports
from .base import router as base_router

router = APIRouter()
router.include_router(base_router)
