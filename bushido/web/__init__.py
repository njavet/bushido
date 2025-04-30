from fastapi import APIRouter

# project imports
from .endpoints import router as base_router

router = APIRouter()
router.include_router(base_router)
