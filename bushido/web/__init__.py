from fastapi import APIRouter

# project imports
from .unit import router as unit_router

router = APIRouter()
router.include_router(unit_router)
