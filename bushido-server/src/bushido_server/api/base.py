from fastapi import APIRouter

router = APIRouter()


@router.get("/health/startup")
def startup() -> dict[str, str]:
    # has initialization completed ?
    return {'status': 'ok'}


@router.get("/health/live")
def liveness() -> dict[str, str]:
    # is this process broken ?
    return {'status': 'ok'}


@router.get("/health/ready")
def readiness() -> dict[str, str]:
    # should requests send now ?
    return {'status': 'ok'}
