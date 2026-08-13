from fastapi import APIRouter

from .unit import router as unit_router

router = APIRouter(prefix="/api")
router.include_router(unit_router)
