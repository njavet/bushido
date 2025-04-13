from fastapi import APIRouter

# project imports
from .base import router as base_router
from .units import router as unit_router

router = APIRouter()
router.include_router(base_router)
router.include_router(unit_router)
