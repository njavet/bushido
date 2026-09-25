from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from bushido_server.api.deps import SessionDep
from bushido_server.auth.passwords import hash_password, verify_password
from bushido_server.auth.tokens import create_access_token
from bushido_server.persistence.models import Spartan
from bushido_server.schema.auth import (
    LoginRequest,
    RegisterRequest,
    Token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, session: SessionDep) -> Token:
    existing = session.scalar(select(Spartan).where(Spartan.email == body.email))
    if existing is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
    user = Spartan(
        name="test", email=body.email, hashed_password=hash_password(body.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return Token(access_token=create_access_token(user.id))


@router.post("/login", response_model=Token)
def login(body: LoginRequest, session: SessionDep) -> Token:
    user = session.scalar(select(Spartan).where(Spartan.email == body.email))
    if user is None or not verify_password(body.password, user.hashed_password):
        # deliberately identical error for "no such user" and "wrong password" —
        # distinguishing them lets an attacker enumerate registered emails
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account disabled")

    return Token(access_token=create_access_token(user.id))
