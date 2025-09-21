from fastapi import APIRouter

from bushido.web.base import router as base_router


router = APIRouter()


router.include_router(base_router, prefix='/api')
