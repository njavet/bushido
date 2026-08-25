from fastapi import APIRouter

from .base import router as base_router
from .unit import router as unit_router

router = APIRouter(prefix="/api")
router.include_router(base_router)
router.include_router(unit_router)
