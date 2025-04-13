from fastapi import APIRouter

# project imports
from .units import router as base_router

router = APIRouter()
router.include_router(base_router)
