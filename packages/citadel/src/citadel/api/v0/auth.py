from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from citadel.api.deps import SessionDep, SpartanDep
from citadel.auth.passwords import hash_password, verify_password
from citadel.auth.tokens import create_access_token
from citadel.persistence.models import Spartan
from citadel.schema.auth import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    Token,
)
from citadel.schema.res import SpartanResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, session: SessionDep) -> Token:
    existing = session.scalar(select(Spartan).where(Spartan.email == body.email))
    if existing is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
    spartan = Spartan(
        name=body.name, email=body.email, hashed_password=hash_password(body.password)
    )
    session.add(spartan)
    session.commit()
    session.refresh(spartan)
    return Token(access_token=create_access_token(spartan.id))


@router.post("/login", response_model=Token)
def login(body: LoginRequest, session: SessionDep) -> Token:
    spartan = session.scalar(select(Spartan).where(Spartan.email == body.email))
    if spartan is None or not verify_password(body.password, spartan.hashed_password):
        # deliberately identical error for "no such user" and "wrong password" —
        # distinguishing them lets an attacker enumerate registered emails
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    if not spartan.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account disabled")

    return Token(access_token=create_access_token(spartan.id))


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
