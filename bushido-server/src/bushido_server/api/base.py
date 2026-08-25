from fastapi import APIRouter

router = APIRouter()


@router.get("/health/live")
def liveness() -> dict[str, str]:
    return {'status': 'ok'}


@router.get("/health/ready")
def readiness() -> dict[str, str]:
    return {'status': 'ok'}
