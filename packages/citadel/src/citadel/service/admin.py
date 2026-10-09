from sqlalchemy.orm import Session

from citadel.auth.passwords import verify_password
from citadel.auth.tokens import create_access_token
from citadel.persistence.repos._admin import AdminRepo
from citadel.schema.auth import LoginRequest, RegisterRequest, Token


def register_spartan(request: RegisterRequest, session: Session) -> Token:
    repo = AdminRepo(session)
    spartan = repo.create_spartan(request)
    session.commit()
    session.refresh(spartan)
    return Token(access_token=create_access_token(spartan.id))


def login_spartan(request: LoginRequest, session: Session) -> Token | None:
    repo = AdminRepo(session)
    spartan = repo.fetch_spartan(request.username)
    if spartan is not None:
        verify_password(request.password, spartan.hashed_password)
        token = Token(access_token=create_access_token(spartan.id))
    else:
        token = None
    return token
