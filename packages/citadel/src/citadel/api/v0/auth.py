from fastapi import APIRouter, HTTPException, status

from citadel.api.v0.deps import SessionDep, SpartanDep
from citadel.auth.passwords import hash_password, verify_password
from citadel.exceptions import AdminError
from citadel.schema.auth import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    Token,
)
from citadel.schema.res import SpartanResponse
from citadel.service.admin import login_spartan, register_spartan

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, session: SessionDep) -> Token:
    try:
        token = register_spartan(body, session)
    except AdminError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e)) from e
    return token


@router.post("/login", response_model=Token)
def login(body: LoginRequest, session: SessionDep) -> Token:
    try:
        token = login_spartan(body, session)
    except Exception as e:
        # deliberately identical error for "no such user" and "wrong password" —
        # distinguishing them lets an attacker enumerate registered emails
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "login error") from e
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "login error")
    return token


@router.get("/me")
def get_me(spartan: SpartanDep) -> SpartanResponse:
    return SpartanResponse.model_validate(spartan)


@router.post("/change-password", status_code=204)
def change_password(
    request: ChangePasswordRequest,
    spartan: SpartanDep,
    session: SessionDep,
) -> None:
    if not verify_password(
        request.current_password,
        spartan.hashed_password,
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid current password",
        )

    spartan.hashed_password = hash_password(request.new_password)
    session.commit()
