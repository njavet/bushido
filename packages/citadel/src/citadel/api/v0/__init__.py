from fastapi import APIRouter

from .auth import router as auth_router
from .health import router as health_router
from .unit import router as unit_router

router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(unit_router)


__all__ = ["health_router", "router"]
