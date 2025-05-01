from fastapi import APIRouter

# project imports
from .endpoints import router as base_router
from .categories.lifting import router as lifting_router
from .categories.wimhof import router as wimhof_router

router = APIRouter()
router.include_router(base_router)
router.include_router(lifting_router)
router.include_router(wimhof_router)
